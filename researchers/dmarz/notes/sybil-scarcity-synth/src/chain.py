"""Chain driver: queue each stage behind its software gate and execute it in this process.

    python src/chain.py run --stages S0,P0,Q0,S1     exit 0 done, 3 stopped at a stage or gate, else internal error
    python src/chain.py resume                       only after a provider_credit_balance_low stop at this source hash
    python src/chain.py status                       chain-status.json plus ledger totals (one JSON line)
    python src/chain.py verify                       hub checksums, regraded rows, recomputed analysis (one JSON line)

A failed stage or a refused gate stops the chain: nothing further is queued and no stage is rerun.
The one exception is pre-registered: a stage that a billing outage stopped may be continued by
`resume`, which queues `<batch>-r<k>` with exactly the units left not started, under the same
ledger and caps, and then goes on with the stages that were requested after it.
`status` and `verify` need no model credential. Nothing here prints a secret.
"""
import argparse
import hashlib
import json
import os
import signal
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))   # runs from any working directory

import analyze
import coordinator
import provider
import study
import worker

EXIT_DONE, EXIT_INTERNAL, EXIT_USAGE, EXIT_STOPPED = 0, 1, 2, 3
STATUS_FILE = 'chain-status.json'
PAID_ENVIRONMENT = ('SWARM_MODEL_API_KEY', 'SWARM_MODEL_WORKSPACE_ID')
DRAIN_SECONDS = 600     # kept free at the end of the chain limit for in-flight calls, frames and uploads


class Terminated(BaseException):
    pass


def now():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def parse_stages(text):
    """Any ordered contiguous sub-list of S0, P0, Q0, S1."""
    stages = [s.strip().upper() for s in text.split(',') if s.strip()]
    order = list(study.STAGES)
    if not stages or any(s not in order for s in stages):
        raise ValueError('unknown_stage')
    first = order.index(stages[0])
    if stages != order[first:first + len(stages)]:
        raise ValueError('stages_must_be_ordered_and_contiguous')
    return stages


def write_status(root, status):
    """Atomic rewrite after every transition."""
    status['updated'] = now()
    tmp = root / (STATUS_FILE + '.tmp')
    with tmp.open('w') as f:
        json.dump(status, f, indent=2, sort_keys=True); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, root / STATUS_FILE)


def read_status(root):
    try:
        return json.loads((root / STATUS_FILE).read_text())
    except FileNotFoundError:
        return None


def projection_check(mean_cost_by_effort, committed_usd):
    """Before S1: S1 calls x Q0's measured mean actual cost per call, per effort, must fit in the remaining cap."""
    d = study.design()
    budget = d['budget']
    per_effort = budget['max_calls']['S1'] // len(d['efforts'])
    remaining = budget['aggregate_usd'] - committed_usd
    projected = sum(per_effort * mean_cost_by_effort[effort] for effort in d['efforts'])
    return {'q0_mean_cost_usd': dict(mean_cost_by_effort), 's1_calls_per_effort': per_effort,
            'projected_s1_usd': projected, 'committed_usd': committed_usd,
            'remaining_cap_usd': remaining, 'passed': bool(projected <= remaining)}


def projection(sr, ledger_path):
    p = study.params('Q0')
    runs = sr.runs(study.EXPERIMENT, limit=5000)
    if not coordinator.stage_passed(runs, 'Q0', p['source_hash'], p['model']):
        raise ValueError('projection_needs_exactly_one_passed_q0')
    # Q0 ran on this attempt's model, so its measured cost per call already uses that model's prices.
    metrics = (coordinator.stage_runs(runs, 'Q0', p['source_hash'], p['model'])[0][-1].get('metrics') or {})
    costs = {}
    for effort in study.design()['efforts']:
        calls, cost = metrics.get(f'stage_calls_{effort}'), metrics.get(f'stage_cost_usd_{effort}')
        if not calls or cost is None:
            raise ValueError('projection_missing_q0_usage')
        costs[effort] = cost / calls
    return projection_check(costs, provider.Ledger(ledger_path).transact()['committed_usd'])


def run_chain(stages, sr, results_root=None, ledger_path=None, opener=None, clock=None, sleep=None, resume=False):
    """Run the requested stages in order (or resume after a billing stop). Returns the process exit code."""
    root = Path(results_root) if results_root else study.results_root()
    root.mkdir(parents=True, exist_ok=True)
    try:
        return _run_chain(stages, sr, root, ledger_path, opener, clock, sleep, resume)
    except Exception as exc:
        # An internal error also leaves a truthful status file: stopped, nothing further queued.
        status = read_status(root) or {'experiment': study.EXPERIMENT, 'stages': {}}
        status.update(state='stopped_at_gate', stopped_stage=status.get('current_stage'),
                      reason='internal_error_' + type(exc).__name__, ended=now())
        write_status(root, status)
        print(f'chain: internal error {type(exc).__name__}', file=sys.stderr)
        return EXIT_INTERNAL


def _parts(entry):
    return [entry] + list(entry.get('continuations') or [])


def _run_chain(stages, sr, root, ledger_path, opener, clock, sleep, resume):
    budget = study.design()['budget']
    stop_category = budget['billing_outage']['stop_category']
    ledger_path = ledger_path or os.environ.get(provider.LEDGER_ENV)
    previous = read_status(root) or {}
    if previous.get('model') not in (None, study.model()):
        # One results directory per model attempt; the launcher points each model at its own.
        print('chain: this results directory belongs to an attempt on ' + str(previous.get('model')), file=sys.stderr)
        return EXIT_STOPPED
    resume_stage = None
    if resume:
        # Allowed only when the last run of the last executed stage was stopped by a billing outage
        # at the current source hash.
        executed = [s for s in study.STAGES if ((previous.get('stages') or {}).get(s) or {}).get('run')]
        resume_stage = executed[-1] if executed else None
        entry = (previous.get('stages') or {}).get(resume_stage) or {}
        last_part = _parts(entry)[-1] if entry else {}
        if (previous.get('state') != 'stopped_at_gate' or previous.get('source_hash') != study.source_hash()
                or last_part.get('status') != 'failed' or last_part.get('reason') != stop_category):
            print('chain: resume refused: the last stage did not stop with ' + stop_category + ' at this source hash',
                  file=sys.stderr)
            return EXIT_STOPPED
        order = list(study.STAGES)
        wanted = [order.index(s) for s in (previous.get('requested') or []) if s in order]
        stages = order[order.index(resume_stage):max(wanted + [order.index(resume_stage)]) + 1]
    status = {'experiment': study.EXPERIMENT, 'model': study.model(), 'state': 'running', 'requested': stages,
              'started': now(), 'source_hash': study.source_hash(), 'code': study.code_revision(),
              'stages': dict(previous.get('stages') or {}),
              'budget': {'max_calls': budget['max_calls'], 'max_calls_total': budget['max_attempted_calls'],
                         'usd_cap': budget['aggregate_usd']}}
    if resume:
        status['resumed'] = list(previous.get('resumed') or []) + [{'stage': resume_stage, 'at': now()}]
    elif previous.get('resumed'):
        status['resumed'] = previous['resumed']
    write_status(root, status)
    chain_deadline = time.monotonic() + budget['chain_timeout_seconds'] - DRAIN_SECONDS

    def stop(stage, reason, code=EXIT_STOPPED):
        status.update(state='stopped_at_gate', stopped_stage=stage, reason=reason, ended=now())
        write_status(root, status)
        print(f'chain stopped at {stage}: {reason}', file=sys.stderr)
        return code

    # Fail before anything is queued if a paid stage could not run.
    if any(s != 'S0' for s in stages):
        missing = [name for name in PAID_ENVIRONMENT if not os.environ.get(name)]
        if not ledger_path:
            missing.append(provider.LEDGER_ENV)
        if missing:
            return stop(stages[0], 'missing_environment:' + ','.join(missing))

    def refuse(stage, entry, reason):
        # A refused gate never erases the record of a run this stage already had.
        entry.update(status='refused', reason=reason, ended=now())
        if not (status['stages'].get(stage) or {}).get('run'):
            status['stages'][stage] = entry
        status['refused'] = dict(entry, stage=stage)
        return stop(stage, reason)

    for stage in stages:
        continuing = resume and stage == resume_stage
        base = status['stages'].get(stage) if continuing else None
        part = len(_parts(base)) if continuing else 0
        prior_dirs = [e['results_dir'] for e in _parts(base)] if continuing else []
        p = study.params(stage, part)
        entry = {'status': 'gating', 'batch': p['batch'], 'started': now()}
        status['current_stage'] = stage
        write_status(root, status)
        try:
            if stage == 'S1' and not continuing:
                entry['projection'] = projection(sr, ledger_path)
                if not entry['projection']['passed']:
                    raise ValueError('projection_exceeds_cap')
            ids = coordinator.enqueue(sr, stage, part)
        except ValueError as exc:
            return refuse(stage, entry, str(exc))
        except Exception as exc:
            # The gate could not be evaluated (for example the hub was unreachable): not passed.
            return refuse(stage, entry, 'gate_error_' + type(exc).__name__)
        run = sr.next_run(study.EXPERIMENT)
        if run is None or len(ids) != 1 or run.id != ids[0] or run.params != p or run.attempt != 1:
            if run is not None:
                run.fail('chain refused a run it did not queue; not executed', episodes=0, invalid=0, model_calls=0,
                         input_tokens=0, output_tokens=0, cost_usd=0)
            return refuse(stage, entry, 'unexpected_run_in_queue')
        if continuing:
            base.setdefault('continuations', []).append(entry)
            base['stage_status'] = 'running'
        else:
            status['stages'][stage] = base = entry
            base['stage_status'] = 'running'
        out = root / f'{run.id.replace("/", "__")}-attempt-{run.attempt}'
        entry.update(status='running', run=run.id, results_dir=str(out))
        write_status(root, status)
        summary = None
        try:
            with run:
                summary = worker.execute(run.params, out, run, ledger_path=ledger_path, opener=opener,
                                         deadline=chain_deadline, prior_dirs=prior_dirs, clock=clock, sleep=sleep)
        except worker.StageFailed as exc:
            entry.update(_usage(exc.summary), status='failed', reason=exc.reason, ended=now())
            base['stage_status'] = 'failed'
            return stop(stage, exc.reason)
        entry.update(_usage(summary), ended=now())
        if (sr.get_run(run.id) or {}).get('status') != 'done':
            entry.update(status='failed', reason='hub_did_not_record_done')
            base['stage_status'] = 'failed'
            return stop(stage, 'hub_did_not_record_done')
        entry['status'] = 'done'
        base['stage_status'] = 'done'
        write_status(root, status)
    status.update(state='completed', ended=now())
    for key in ('stopped_stage', 'reason', 'current_stage', 'refused'):
        status.pop(key, None)
    write_status(root, status)
    return EXIT_DONE


def _usage(summary):
    if not summary:
        return {'calls': None, 'input_tokens': None, 'output_tokens': None, 'cost_usd': None}
    own = summary['part_usage']
    return {'calls': own['model_calls'], 'transport_attempts': own['transport_attempts'], 'input_tokens': own['input_tokens'],
            'output_tokens': own['output_tokens'], 'cost_usd': own['cost_usd'], 'count_fallbacks': own['count_fallbacks'],
            'planned': summary['planned'], 'part_units': summary['part_units'], 'valid': summary['graded'],
            'invalid': summary['invalid'], 'failed': summary['failed'], 'not_started': summary['not_started'],
            'billing': summary['billing'], 'gate_passed': summary['gate']['passed'],
            'elapsed_seconds': summary['elapsed_seconds']}


def chain_status(results_root=None, ledger_path=None):
    root = Path(results_root) if results_root else study.results_root()
    ledger_path = ledger_path or os.environ.get(provider.LEDGER_ENV)
    ledger = provider.Ledger(ledger_path).transact() if ledger_path and Path(ledger_path).exists() else None
    status = read_status(root) or {'state': 'absent'}
    return {'chain': status, 'ledger': ledger, 'model': status.get('model') or study.model(),
            'source_hash': study.source_hash(), 'results_dir': str(root)}


class attempt_model:
    """Read a results directory as the model its attempt ran on, whatever STUDY_MODEL says now."""
    def __init__(self, name):
        self.name, self.saved = name, None

    def __enter__(self):
        self.saved = os.environ.get('STUDY_MODEL')
        if self.name in study.design()['model_ladder']:
            os.environ['STUDY_MODEL'] = self.name

    def __exit__(self, *exc):
        if self.saved is None:
            os.environ.pop('STUDY_MODEL', None)
        else:
            os.environ['STUDY_MODEL'] = self.saved
        return False


def _sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def _plain(value):
    return json.loads(json.dumps(value))


SUMMARY_KEYS = ('part', 'planned', 'part_units', 'started', 'terminal', 'graded', 'analyzed', 'invalid', 'failed',
                'not_started', 'max_failed', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd',
                'transport_attempts', 'count_fallbacks', 'part_usage', 'billing', 'by_effort', 'failure_categories',
                'qualification', 'probe', 'gate', 'failure', 'reference_cells')
HUB_METRIC_KEYS = ('episodes', 'invalid', 'failed', 'not_started', 'model_calls', 'input_tokens', 'output_tokens',
                   'cost_usd', 'transport_attempts', 'count_fallbacks', 'billing_stop', 'billing_pauses',
                   'billing_pause_seconds', 'billing_affected_calls')


def manifest_line(a):
    return f'{a["id"]} {a["prompt"]}-{a["effort"]} {a["packet_hash"]}'


def verify_part(sr, stage, entry, manifest, earlier_rows):
    """Every check for one executed run, from the saved files and the hub's artifact records.

    `earlier_rows` are the row lists of the stage's earlier parts. Returns (report, this part's rows).
    """
    checks = {}
    out = Path(entry['results_dir'])
    detail = sr.get_run(entry['run']) or {}
    hub = {a['name']: a['sha256'] for a in detail.get('artifacts') or []}
    checks['artifacts_match_hub'] = bool(hub) and all((out / n).is_file() and _sha256(out / n) == h for n, h in hub.items())
    checks['artifacts_complete'] = set(worker.ARTIFACTS) <= set(hub)
    checks['hub_status_matches'] = detail.get('status') == entry.get('status')
    try:
        assignments = analyze.read_rows(out / 'assignments.jsonl.gz')
        rows = analyze.read_rows(out / 'episodes.jsonl.gz')
        saved = json.loads((out / 'summary.json').read_text())
        analysis = json.loads((out / 'analysis.json').read_text())
    except (OSError, ValueError) as exc:
        checks['records_readable'] = False
        return {'ok': False, 'checks': checks, 'error': type(exc).__name__}, []
    checks['records_readable'] = True
    by_id = {a['id']: a for a in assignments}
    checks['assignments_match_manifest'] = [manifest_line(a) for a in assignments] == manifest['stages'][stage]['assignments']
    checks['packet_hashes_recomputed'] = all(study.digest(a['packet']) == a['packet_hash'] for a in assignments)
    try:
        stage_rows = worker.combine(earlier_rows + [rows])
        checks['no_unit_counted_twice'] = True
    except ValueError:
        stage_rows = rows
        checks['no_unit_counted_twice'] = False
    checks['rows_cover_assignments'] = (set(r['id'] for r in rows) <= set(by_id) and len({r['id'] for r in rows}) == len(rows)
                                        and sorted(r['id'] for r in stage_rows) == sorted(by_id))
    checks['grades_recomputed'] = checks['rows_cover_assignments'] and all(
        _plain(study.reference_outcomes(by_id[r['id']])) == r['reference']
        and (r['status'] != 'completed' or _plain(study.evaluate(by_id[r['id']], r['answer'])) == r['evaluation'])
        for r in rows)
    recomputed = _plain(worker.summarize(saved['params'], stage_rows, len(assignments), saved['invariants'], saved['elapsed_seconds'],
                                         saved['initial_study_accounting'], saved['study_accounting'], part_rows=rows))
    checks['summary_recomputed'] = all(recomputed[k] == saved[k] for k in SUMMARY_KEYS)
    recomputed_analysis = _plain(analyze.analyze(stage_rows))
    checks['analysis_recomputed'] = recomputed_analysis == analysis
    checks['source_hash_matches'] = saved['params']['source_hash'] == study.source_hash()
    metrics = detail.get('metrics') or {}
    expected = _plain(worker.hub_metrics(saved, analysis))
    if saved['failure'] and stage != 'S1':
        expected['qualification_passed'] = 0
    checks['hub_metrics_match'] = all(metrics.get(k) == expected.get(k) for k in HUB_METRIC_KEYS + tuple(
        k for k in expected if k.startswith('stage_') or k == 'qualification_passed'))
    report = {'ok': all(checks.values()), 'checks': checks, 'run': entry['run'], 'batch': entry.get('batch'),
              'rows': len(rows), 'stage_valid': saved['graded'], 'stage_failed': saved['failed'],
              'stage_not_started': saved['not_started'], 'model_calls': saved['part_usage']['model_calls'],
              'cost_usd': saved['part_usage']['cost_usd'], 'failure': saved['failure']}
    if stage == 'S1' and recomputed_analysis.get('primary'):
        primary = recomputed_analysis['primary']
        report['primary'] = {k: primary[k] for k in ('mean', 'interval', 'all_assigned_bounds', 'complete_case_mean',
                                                     'roots', 'complete_roots')}
    return report, rows


def verify(sr, results_root=None, manifest=None):
    root = Path(results_root) if results_root else study.results_root()
    status = read_status(root)
    report = {'experiment': study.EXPERIMENT, 'source_hash': study.source_hash(), 'ok': False, 'stages': {}}
    if not status:
        report['error'] = 'no_chain_status'
        return report
    report['state'] = status.get('state')
    report['model'] = status.get('model')
    if status.get('model') not in study.design()['model_ladder']:
        report['error'] = 'model_not_in_ladder'
        return report
    try:
        manifest = manifest or json.loads((study.ROOT / 'manifest.json').read_text())
    except (OSError, ValueError):
        report['error'] = 'manifest_unreadable'
        return report
    with attempt_model(status['model']):
        _verify_stages(sr, status, manifest, report)
    report['ok'] = bool(report['stages']) and all(s['ok'] for s in report['stages'].values())
    return report


def _verify_stages(sr, status, manifest, report):
    for stage in study.STAGES:
        base = (status.get('stages') or {}).get(stage)
        if not (base and base.get('run') and base.get('results_dir')):
            continue
        parts, earlier = [], []
        for entry in _parts(base):
            try:
                part_report, rows = verify_part(sr, stage, entry, manifest, earlier)
            except Exception as exc:
                part_report, rows = {'ok': False, 'error': type(exc).__name__, 'run': entry.get('run')}, []
            parts.append(part_report)
            earlier.append(rows)
        last = parts[-1]
        report['stages'][stage] = dict(last, ok=all(part['ok'] for part in parts), parts=len(parts))
        if len(parts) > 1:
            report['stages'][stage]['earlier_parts'] = parts[:-1]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='command', required=True)
    r = sub.add_parser('run')
    r.add_argument('--stages', required=True, help='ordered contiguous sub-list, e.g. S0,P0,Q0,S1')
    for name in ('run', 'resume', 'status', 'verify'):
        s = r if name == 'run' else sub.add_parser(name)
        s.add_argument('--results-dir', help='default: $STUDY_RESULTS_DIR, else <study>/results')
    a = ap.parse_args(argv)
    try:
        study.model()
    except ValueError:
        print('chain: STUDY_MODEL is not in the model ladder ' + ', '.join(study.design()['model_ladder']), file=sys.stderr)
        return EXIT_USAGE
    if a.command == 'status':
        print(json.dumps(chain_status(a.results_dir), sort_keys=True))
        return EXIT_DONE
    import swarm_report as sr     # the server's hub client, found on sys.path / PYTHONPATH
    if a.command == 'verify':
        report = verify(sr, a.results_dir)
        print(json.dumps(report, sort_keys=True))
        return EXIT_DONE if report['ok'] else EXIT_INTERNAL
    stages = []
    if a.command == 'run':
        try:
            stages = parse_stages(a.stages)
        except ValueError as exc:
            print(f'chain: {exc}', file=sys.stderr)
            return EXIT_USAGE

    def terminate(signum, frame):
        raise Terminated()
    signal.signal(signal.SIGTERM, terminate)
    return run_chain(stages, sr, a.results_dir, resume=a.command == 'resume')


if __name__ == '__main__':
    sys.exit(main())
