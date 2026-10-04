"""Chain driver: queue each stage behind its software gate and execute it in this process.

    python src/chain.py run --stages S0,P0,Q0,S1     exit 0 done, 3 stopped at a stage or gate, else internal error
    python src/chain.py status                       chain-status.json plus ledger totals (one JSON line)
    python src/chain.py verify                       hub checksums, regraded rows, recomputed analysis (one JSON line)

A failed stage or a refused gate stops the chain: nothing further is queued and there are no
retries. `status` and `verify` need no model credential. Nothing here prints a secret.
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
import manifest as mf
import provider
import study
import worker

EXIT_DONE, EXIT_INTERNAL, EXIT_STOPPED = 0, 1, 3
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


def projection_check(q0_mean_cost_usd, committed_usd):
    """Before S1: S1 calls x Q0's measured mean actual cost per call x the growth factor for longer
    boards must fit in the remaining cap."""
    budget = study.design()['budget']
    remaining = budget['aggregate_usd'] - committed_usd
    growth = budget['projection_growth_factor']
    projected = budget['max_calls']['S1'] * q0_mean_cost_usd * growth
    return {'q0_mean_cost_usd': q0_mean_cost_usd, 's1_calls': budget['max_calls']['S1'], 'growth_factor': growth,
            'projected_s1_usd': projected, 'committed_usd': committed_usd,
            'remaining_cap_usd': remaining, 'passed': bool(projected <= remaining)}


def projection(sr, ledger_path):
    p = study.params('Q0')
    runs = [r for r in sr.runs(study.EXPERIMENT, limit=5000)
            if (r.get('params') or {}).get('stage') == 'Q0' and (r.get('params') or {}).get('source_hash') == p['source_hash']
            and r.get('status') == 'done']
    if len(runs) != 1:
        raise ValueError('projection_needs_exactly_one_passed_q0')
    metrics = runs[0].get('metrics') or {}
    calls, cost = metrics.get('model_calls'), metrics.get('cost_usd')
    if not calls or cost is None:
        raise ValueError('projection_missing_q0_usage')
    return projection_check(cost / calls, provider.Ledger(ledger_path).transact()['committed_usd'])


def run_chain(stages, sr, results_root=None, ledger_path=None, opener=None):
    """Run the requested stages in order. Returns the process exit code."""
    root = Path(results_root) if results_root else study.results_root()
    root.mkdir(parents=True, exist_ok=True)
    try:
        return _run_chain(stages, sr, root, ledger_path, opener)
    except Exception as exc:
        # An internal error also leaves a truthful status file: stopped, nothing further queued.
        status = read_status(root) or {'experiment': study.EXPERIMENT, 'stages': {}}
        status.update(state='stopped_at_gate', stopped_stage=status.get('current_stage'),
                      reason='internal_error_' + type(exc).__name__, ended=now())
        write_status(root, status)
        print(f'chain: internal error {type(exc).__name__}', file=sys.stderr)
        return EXIT_INTERNAL


def _run_chain(stages, sr, root, ledger_path, opener):
    budget = study.design()['budget']
    ledger_path = ledger_path or os.environ.get(provider.LEDGER_ENV)
    previous = read_status(root) or {}
    status = {'experiment': study.EXPERIMENT, 'state': 'running', 'requested': stages, 'started': now(),
              'source_hash': study.source_hash(), 'code': study.code_revision(),
              'stages': dict(previous.get('stages') or {}),
              'budget': {'max_calls': budget['max_calls'], 'max_calls_total': budget['max_attempted_calls'],
                         'usd_cap': budget['aggregate_usd']}}
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
        p = study.params(stage)
        entry = {'status': 'gating', 'batch': p['batch'], 'started': now()}
        status['current_stage'] = stage
        write_status(root, status)
        try:
            if stage == 'S1':
                entry['projection'] = projection(sr, ledger_path)
                if not entry['projection']['passed']:
                    raise ValueError('projection_exceeds_cap')
            ids = coordinator.enqueue(sr, stage)
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
        status['stages'][stage] = entry
        out = root / f'{run.id.replace("/", "__")}-attempt-{run.attempt}'
        entry.update(status='running', run=run.id, results_dir=str(out))
        write_status(root, status)
        summary = None
        try:
            with run:
                summary = worker.execute(run.params, out, run, ledger_path=ledger_path, opener=opener,
                                         deadline=chain_deadline)
        except worker.StageFailed as exc:
            entry.update(_usage(exc.summary), status='failed', reason=exc.reason, ended=now())
            return stop(stage, exc.reason)
        entry.update(_usage(summary), ended=now())
        if (sr.get_run(run.id) or {}).get('status') != 'done':
            entry.update(status='failed', reason='hub_did_not_record_done')
            return stop(stage, 'hub_did_not_record_done')
        entry['status'] = 'done'
        write_status(root, status)
    status.update(state='completed', ended=now())
    for key in ('stopped_stage', 'reason', 'current_stage', 'refused'):
        status.pop(key, None)
    write_status(root, status)
    return EXIT_DONE


def _usage(summary):
    if not summary:
        return {'calls': None, 'input_tokens': None, 'output_tokens': None, 'cost_usd': None}
    return {'calls': summary['model_calls'], 'transport_attempts': summary['transport_attempts'], 'input_tokens': summary['input_tokens'],
            'output_tokens': summary['output_tokens'], 'cost_usd': summary['cost_usd'],
            'planned': summary['planned'], 'valid': summary['graded'], 'invalid': summary['invalid'],
            'gate_passed': summary['gate']['passed'], 'elapsed_seconds': summary['elapsed_seconds']}


def chain_status(results_root=None, ledger_path=None):
    root = Path(results_root) if results_root else study.results_root()
    ledger_path = ledger_path or os.environ.get(provider.LEDGER_ENV)
    ledger = provider.Ledger(ledger_path).transact() if ledger_path and Path(ledger_path).exists() else None
    return {'chain': read_status(root) or {'state': 'absent'}, 'ledger': ledger,
            'source_hash': study.source_hash(), 'results_dir': str(root)}


def _sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def _plain(value):
    return json.loads(json.dumps(value))


SUMMARY_KEYS = ('planned', 'started', 'terminal', 'graded', 'analyzed', 'invalid', 'failed', 'not_started', 'model_calls',
                'input_tokens', 'output_tokens', 'cost_usd', 'transport_attempts', 'qualification', 'probe', 'gate', 'failure')


def replay(units, by_id):
    """Rebuild every actor input from the fixed inputs and the saved answers, and regrade.

    Returns (packets_ok, grades_ok). A saved packet must equal the packet the instrument builds
    from the episode's fixed inputs and the saved answers of the rounds before; a row after the
    point where its episode stopped must carry no packet."""
    packets_ok = grades_ok = True
    for unit in units:
        if unit['type'] == 'fixture':
            r = by_id[study.slots(unit)[0][0]]
            if 'packet' in r:
                packets_ok &= r['packet'] == unit['packet'] and study.digest(r['packet']) == r['packet_hash'] == unit['packet_hash']
            if r['status'] == 'completed':
                grades_ok &= _plain(study.evaluate(unit['context'], unit['packet'], r['answer'])) == r['evaluation']
            continue
        ep = study.Episode(unit['root'], unit['condition'])
        packets_ok &= study.digest(ep.fixed_inputs()) == unit['fixed_hash'] == study.digest(unit['fixed_inputs'])
        context, alive = ep.context(), True
        for t in range(1, ep.rounds + 1):
            answers = {}
            for m in ep.models:
                r = by_id[f'{unit["id"]}.{m}.r{t}']
                if not alive:
                    packets_ok &= 'packet' not in r and r['status'] == 'not_started'
                    continue
                if 'packet' in r:
                    packet = ep.packet(m, t)
                    packets_ok &= r['packet'] == _plain(packet) and study.digest(packet) == r['packet_hash']
                    if r['status'] == 'completed':
                        grades_ok &= _plain(study.evaluate(context, packet, r['answer'])) == r['evaluation']
                        answers[m] = r['answer']
                else:
                    packets_ok &= r['status'] == 'not_started'
            if alive and len(answers) == len(ep.models):
                ep.apply(t, answers)
            else:
                alive = False
    return bool(packets_ok), bool(grades_ok)


def verify_stage(sr, stage, entry, manifest):
    """Every check for one executed stage, from the saved files and the hub's artifact records."""
    checks = {}
    out = Path(entry['results_dir'])
    detail = sr.get_run(entry['run']) or {}
    hub = {a['name']: a['sha256'] for a in detail.get('artifacts') or []}
    checks['artifacts_match_hub'] = bool(hub) and all((out / n).is_file() and _sha256(out / n) == h for n, h in hub.items())
    checks['artifacts_complete'] = set(worker.ARTIFACTS) <= set(hub)
    checks['hub_status_matches'] = detail.get('status') == entry.get('status')
    try:
        units = analyze.read_rows(out / 'assignments.jsonl.gz')
        rows = analyze.read_rows(out / 'episodes.jsonl.gz')
        saved = json.loads((out / 'summary.json').read_text())
        analysis = json.loads((out / 'analysis.json').read_text())
    except (OSError, ValueError) as exc:
        checks['records_readable'] = False
        return {'ok': False, 'checks': checks, 'error': type(exc).__name__}
    checks['records_readable'] = True
    by_id = {r['id']: r for r in rows}
    planned = [slot[0] for unit in units for slot in study.slots(unit)]
    checks['assignments_match_manifest'] = [mf.line(u) for u in units] == manifest['stages'][stage]['units']
    checks['rows_cover_assignments'] = sorted(by_id) == sorted(planned) and len(rows) == len(planned)
    packets_ok, grades_ok = replay(units, by_id) if checks['rows_cover_assignments'] else (False, False)
    checks['packets_replayed_from_saved_answers'] = packets_ok
    checks['grades_recomputed'] = grades_ok
    recomputed = _plain(worker.summarize(saved['params'], rows, len(planned), saved['invariants'], saved['elapsed_seconds'],
                                         saved['initial_study_accounting'], saved['study_accounting']))
    checks['summary_recomputed'] = all(recomputed[k] == saved[k] for k in SUMMARY_KEYS)
    checks['analysis_recomputed'] = _plain(analyze.analyze(rows)) == analysis
    checks['source_hash_matches'] = saved['params']['source_hash'] == study.source_hash()
    metrics = detail.get('metrics') or {}
    checks['hub_metrics_match'] = (metrics.get('episodes') == saved['planned'] and metrics.get('invalid') == saved['invalid']
                                   and all(metrics.get(k) == saved[k] for k in ('model_calls', 'input_tokens', 'output_tokens', 'cost_usd')))
    return {'ok': all(checks.values()), 'checks': checks, 'run': entry['run'],
            'rows': len(rows), 'valid': saved['graded'], 'model_calls': saved['model_calls'], 'cost_usd': saved['cost_usd']}


def verify(sr, results_root=None):
    root = Path(results_root) if results_root else study.results_root()
    status = read_status(root)
    report = {'experiment': study.EXPERIMENT, 'source_hash': study.source_hash(), 'ok': False, 'stages': {}}
    if not status:
        report['error'] = 'no_chain_status'
        return report
    report['state'] = status.get('state')
    try:
        manifest = json.loads((study.ROOT / 'manifest.json').read_text())
    except (OSError, ValueError):
        report['error'] = 'manifest_unreadable'
        return report
    for stage in study.STAGES:
        entry = (status.get('stages') or {}).get(stage)
        if entry and entry.get('run') and entry.get('results_dir'):
            try:
                report['stages'][stage] = verify_stage(sr, stage, entry, manifest)
            except Exception as exc:
                report['stages'][stage] = {'ok': False, 'error': type(exc).__name__}
    report['ok'] = bool(report['stages']) and all(s['ok'] for s in report['stages'].values())
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='command', required=True)
    r = sub.add_parser('run')
    r.add_argument('--stages', required=True, help='ordered contiguous sub-list, e.g. S0,P0,Q0,S1')
    for name in ('run', 'status', 'verify'):
        s = r if name == 'run' else sub.add_parser(name)
        s.add_argument('--results-dir', help='default: $STUDY_RESULTS_DIR, else <study>/results')
    a = ap.parse_args(argv)
    if a.command == 'status':
        print(json.dumps(chain_status(a.results_dir), sort_keys=True))
        return EXIT_DONE
    import swarm_report as sr     # the server's hub client, found on sys.path / PYTHONPATH
    if a.command == 'verify':
        report = verify(sr, a.results_dir)
        print(json.dumps(report, sort_keys=True))
        return EXIT_DONE if report['ok'] else EXIT_INTERNAL
    try:
        stages = parse_stages(a.stages)
    except ValueError as exc:
        print(f'chain: {exc}', file=sys.stderr)
        return 2

    def terminate(signum, frame):
        raise Terminated()
    signal.signal(signal.SIGTERM, terminate)
    return run_chain(stages, sr, a.results_dir)


if __name__ == '__main__':
    sys.exit(main())
