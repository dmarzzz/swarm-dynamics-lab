"""Chain driver (coordinator process): each stage behind its software gate, executed in this process.

    python src/chain.py run --stages S0,P0,Q0,X0,S1,D1   exit 0 done, 3 stopped at a stage or gate, else internal error
    python src/chain.py status                            chain-status.json plus ledger totals (one JSON line)
    python src/chain.py verify                            hub checksums, re-simulated rounds, recomputed analysis (one JSON line)

This process owns the world state, the round clock and the only ledger. It never calls the model and needs
no model credential: three workers (`python src/worker.py serve`, one per server) make the calls. A failed
stage or a refused gate stops the chain; nothing is retried. Nothing here prints a secret.
"""
import argparse
import gzip
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
import sim
import study
import transport
import worker

EXIT_DONE, EXIT_INTERNAL, EXIT_STOPPED = 0, 1, 3
STATUS_FILE = 'chain-status.json'
DRAIN_SECONDS = 600


class Terminated(BaseException):
    pass


def now():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def parse_stages(text):
    """Any ordered contiguous sub-list of the stages."""
    stages = [s.strip().upper() for s in text.split(',') if s.strip()]
    order = list(study.STAGES)
    if not stages or any(s not in order for s in stages):
        raise ValueError('unknown_stage')
    first = order.index(stages[0])
    if stages != order[first:first + len(stages)]:
        raise ValueError('stages_must_be_ordered_and_contiguous')
    return stages


def write_status(root, status):
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


def projection_check(mean_cost_usd, committed_usd):
    """Before S1: S1 and D1 calls x the measured mean cost of a maximum-context call must fit in the remaining cap."""
    budget = study.design()['budget']
    calls = budget['max_calls']['S1'] + budget['max_calls']['D1']
    remaining = budget['aggregate_usd'] - committed_usd
    projected = calls * mean_cost_usd
    return {'mean_cost_usd': mean_cost_usd, 'calls': calls, 'projected_usd': projected, 'committed_usd': committed_usd,
            'remaining_cap_usd': remaining, 'passed': bool(projected <= remaining)}


def run_chain(stages, sr, results_root=None, ledger_path=None, allow_shared_host=False, poll=None, transport_options=None):
    """Run the requested stages in order. Returns the process exit code."""
    root = Path(results_root) if results_root else study.results_root()
    root.mkdir(parents=True, exist_ok=True)
    holder = {}
    try:
        return _run_chain(stages, sr, root, ledger_path, allow_shared_host, poll, holder, transport_options)
    except Exception as exc:
        status = read_status(root) or {'experiment': study.EXPERIMENT, 'stages': {}}
        status.update(state='stopped_at_gate', stopped_stage=status.get('current_stage'),
                      reason='internal_error_' + type(exc).__name__, ended=now())
        write_status(root, status)
        print(f'chain: internal error {type(exc).__name__}', file=sys.stderr)
        return EXIT_INTERNAL
    finally:
        if holder.get('dispatcher'):
            holder['dispatcher'].close()      # workers end their sessions and exit


def _run_chain(stages, sr, root, ledger_path, allow_shared_host, poll, holder, transport_options=None):
    d = study.design()
    budget = d['budget']
    ledger_path = ledger_path or os.environ.get(provider.LEDGER_ENV)
    previous = read_status(root) or {}
    status = {'experiment': study.EXPERIMENT, 'state': 'running', 'requested': stages, 'started': now(),
              'source_hash': study.source_hash(), 'code': study.code_revision(),
              'stages': dict(previous.get('stages') or {}),
              'budget': {'max_calls': budget['max_calls'], 'max_calls_total': budget['max_attempted_calls'],
                         'usd_cap': budget['aggregate_usd']}}
    write_status(root, status)
    chain_deadline = time.monotonic() + budget['chain_timeout_seconds'] - DRAIN_SECONDS
    soft = []

    def stop(stage, reason, code=EXIT_STOPPED):
        status.update(state='stopped_at_gate', stopped_stage=stage, reason=reason, ended=now())
        write_status(root, status)
        print(f'chain stopped at {stage}: {reason}', file=sys.stderr)
        return code

    if any(s != 'S0' for s in stages) and not ledger_path:
        return stop(stages[0], 'missing_environment:' + provider.LEDGER_ENV)

    def refuse(stage, entry, reason):
        entry.update(status='refused', reason=reason, ended=now())
        if not (status['stages'].get(stage) or {}).get('run'):
            status['stages'][stage] = entry
        status['refused'] = dict(entry, stage=stage)
        return stop(stage, reason)

    coordinator.register(sr)
    for stage in stages:
        p = study.params(stage)
        entry = {'status': 'gating', 'batch': p['batch'], 'started': now()}
        status['current_stage'] = stage
        write_status(root, status)
        in_flight = None
        try:
            runs = sr.runs(study.EXPERIMENT, limit=5000)
            coordinator.gate(runs, stage, p)
            if stage in ('S1', 'D1'):
                x0 = coordinator.stage_runs(runs, 'X0', p['source_hash'])
                metrics = (x0[0].get('metrics') or {}) if len(x0) == 1 else {}
                in_flight = int(metrics.get('in_flight_selected') or budget['in_flight_per_host'])
                if not budget['in_flight_per_host'] <= in_flight <= budget['in_flight_per_host_max']:
                    raise ValueError('in_flight_out_of_range')
                if stage == 'S1':
                    if not metrics.get('model_calls') or metrics.get('cost_usd') is None:
                        raise ValueError('projection_missing_x0_usage')
                    committed = transport.FastLedger(ledger_path, study.ledger_budget()).transact()['committed_usd']
                    entry['projection'] = projection_check(metrics['cost_usd'] / metrics['model_calls'], committed)
                    if not entry['projection']['passed']:
                        raise ValueError('projection_exceeds_cap')
        except ValueError as exc:
            return refuse(stage, entry, str(exc))
        except Exception as exc:
            return refuse(stage, entry, 'gate_error_' + type(exc).__name__)
        dispatcher = holder.get('dispatcher')
        if stage != 'S0' and dispatcher is None:
            dispatcher = transport.HubDispatcher(sr, transport.FastLedger(ledger_path, study.ledger_budget()), study.provider_config(),
                                                 d['economy']['hosts'], root / 'transport', d['attempt'] + '-' + p['batch'],
                                                 poll=poll, allow_shared_host=allow_shared_host, **(transport_options or {}))
            holder['dispatcher'] = dispatcher
            try:
                status['worker_hosts'] = dispatcher.attach(budget['worker_attach_seconds'])
                status['worker_sessions'] = dispatcher.sessions
                status['distinct_hosts'] = len(set(status['worker_hosts'])) == len(status['worker_hosts'])
            except transport.StageStop as exc:
                return refuse(stage, entry, exc.reason)
        run_id = f'{study.EXPERIMENT}/{p["batch"]}'
        run = sr.start(study.EXPERIMENT, run=run_id, params=p, message=f'{stage} started by the chain')
        status['stages'][stage] = entry
        out = root / f'{run.id.replace("/", "__")}'
        entry.update(status='running', run=run.id, results_dir=str(out), in_flight_per_host=in_flight)
        write_status(root, status)
        summary, failed = None, None
        try:
            with run:
                summary = worker.execute(p, out, run, dispatcher, chain_deadline, in_flight)
        except worker.StageFailed as exc:
            summary, failed = exc.summary, exc.reason
        entry.update(_usage(summary), ended=now())
        if failed:
            entry.update(status='failed', reason=failed)
            write_status(root, status)
            # A branch stopped under the pre-registered material rule does not block the cue diagnostic.
            if stage == 'S1' and failed.startswith('branch_stopped:'):
                soft.append(f'S1:{failed}')
                continue
            return stop(stage, failed)
        if (sr.get_run(run.id) or {}).get('status') != 'done':
            entry.update(status='failed', reason='hub_did_not_record_done')
            return stop(stage, 'hub_did_not_record_done')
        entry['status'] = 'done'
        write_status(root, status)
    for key in ('stopped_stage', 'reason', 'current_stage', 'refused'):
        status.pop(key, None)
    if soft:
        status.update(state='completed_with_stopped_branch', reason=';'.join(soft), ended=now())
        write_status(root, status)
        return EXIT_STOPPED
    status.update(state='completed', ended=now())
    write_status(root, status)
    return EXIT_DONE


def _usage(summary):
    if not summary:
        return {'calls': None, 'input_tokens': None, 'output_tokens': None, 'cost_usd': None}
    out = {'calls': summary['model_calls'], 'transport_attempts': summary['transport_attempts'],
           'input_tokens': summary['input_tokens'], 'output_tokens': summary['output_tokens'], 'cost_usd': summary['cost_usd'],
           'planned': summary['planned'], 'asked': summary['asked'], 'accepted': summary['accepted'], 'void': summary['void'],
           'rejected_commands': summary['rejected_commands'], 'normalized': summary.get('normalized'), 'gate_passed': summary['gate']['passed'],
           'elapsed_seconds': summary['elapsed_seconds'], 'hosts': summary.get('hosts'), 'billing': summary.get('billing'),
           'transport': {k: v for k, v in (summary.get('transport') or {}).items() if k != 'events'} or None}
    detail = summary.get('detail') or {}
    for key in ('in_flight_selected', 'calls_per_second', 'projected_s1_seconds', 'planning_marker_met', 'max_prompt_tokens', 'valid_actions',
                'measurement', 'checkpoint_hash', 'branches', 'warmup'):
        if key in detail:
            out[key] = detail[key]
    return out


def chain_status(results_root=None, ledger_path=None):
    root = Path(results_root) if results_root else study.results_root()
    ledger_path = ledger_path or os.environ.get(provider.LEDGER_ENV)
    budget = study.design()['budget']
    ledger = provider.Ledger(ledger_path, study.ledger_budget()).transact() if ledger_path and Path(ledger_path).exists() else None
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


def resimulate(stage, calls, rounds, checkpoint=None):
    """Re-run the engine from the saved answers and compare every saved round record. Returns a dict of checks."""
    answers = {c['unit']: c for c in calls}
    saved = {}
    for rec in rounds:
        saved.setdefault(rec['econ'], {})[(rec['round'], rec['market'])] = {k: v for k, v in rec.items() if k not in ('econ', 'label')}

    def replay(econ, rules, rounds_wanted):
        same = True
        for _ in range(rounds_wanted):
            r = econ.state['round'] + 1
            if not any(k[0] == r for k in saved.get(econ.key, {})):
                break                       # this round was not cleared in the saved run
            sim.begin_round(econ.state)
            responses, failures = {}, {}
            for oid in econ.state['owners']:
                if oid in econ.natives:
                    c = answers.get(econ.unit(oid))
                    if c is None:
                        return False
                    responses[oid] = c['answer'] if c['ok'] else None
                    if not c['ok']:
                        failures[oid] = 'call_failed:' + str(c.get('category'))
                else:
                    responses[oid] = sim.scripted(econ.state, oid, econ.rival_policy)
            for rec in sim.step(econ.state, responses, rules, failures):
                same = same and _plain(rec) == saved[econ.key].get((rec['round'], rec['market']))
        return same

    d = study.design()
    checks = {}
    if stage == 'S1':
        e = d['economy']
        world = study.main_world()
        natives = list(world['owners'])
        checks['warmup_rounds_resimulated'] = replay(study.Economy('warm', world, natives, 'messages'), study.branch_rules('warm'), e['warmup_rounds'])
        if checkpoint is not None:
            checks['checkpoint_recomputed'] = sim.dumps(world) == checkpoint
            for branch in study.branch_order():
                if branch in saved:
                    econ = study.Economy(branch, json.loads(checkpoint), natives, 'messages')
                    checks[f'branch_{branch}_resimulated'] = replay(econ, study.branch_rules(branch), e['branch_rounds'])
    elif stage == 'D1':
        rules = {'regime': 'firm', 'prohibition': False}
        checks['episodes_resimulated'] = all(replay(econ, rules, d['fixtures']['diagnostic_rounds']) for econ in study.diagnostic_economies())
    return checks


def verify_stage(sr, stage, entry):
    checks = {}
    out = Path(entry['results_dir'])
    detail = sr.get_run(entry['run']) or {}
    hub = {a['name']: a['sha256'] for a in detail.get('artifacts') or []}
    final = {n: h for n, h in hub.items() if n not in ('progress.png', 'initial_frame.png')}
    checks['artifacts_match_hub'] = bool(final) and all((out / n).is_file() and _sha256(out / n) == h for n, h in final.items())
    checks['artifacts_complete'] = set(worker.ARTIFACTS) - {'final_frame.png'} <= set(hub)
    checks['hub_status_matches'] = detail.get('status') == entry.get('status')
    try:
        calls = analyze.read_rows(out / 'calls.jsonl.gz')
        rounds = analyze.read_rows(out / 'rounds.jsonl.gz')
        saved = json.loads((out / 'summary.json').read_text())
        analysis = json.loads((out / 'analysis.json').read_text())
    except (OSError, ValueError) as exc:
        checks['records_readable'] = False
        return {'ok': False, 'checks': checks, 'error': type(exc).__name__}
    checks['records_readable'] = True
    checks['source_hash_matches'] = saved['params']['source_hash'] == study.source_hash()
    acc = [c.get('accounting') or {} for c in calls]
    checks['usage_recomputed'] = (sum(bool(a.get('attempted')) for a in acc) == saved['model_calls']
                                  and sum(a.get('input_tokens', 0) or 0 for a in acc) == saved['input_tokens']
                                  and sum(a.get('output_tokens', 0) or 0 for a in acc) == saved['output_tokens']
                                  and len(calls) == saved['asked'])
    checks['call_ids_unique_and_branch_qualified'] = len({c['call_id'] for c in calls}) == len(calls) and all(
        c['call_id'] == f'{saved["params"]["batch"]}:{c["economy"]}.r{c["round"]:02d}.{c["owner"]}' for c in calls)
    checks['prompts_match_their_hashes'] = all(c['user'] is None or sim.digest(c['user']) == c['user_sha256'] for c in calls)
    checks['analysis_recomputed'] = _plain(worker.analysis_of(stage, rounds)) == analysis
    checkpoint = None
    if (out / 'checkpoint.json.gz').exists():
        with gzip.open(out / 'checkpoint.json.gz', 'rt', encoding='utf-8') as f:
            checkpoint = f.read()
        d = saved.get('detail') or {}
        expected = d.get('checkpoint_hash') if stage == 'S1' else (d.get('S1') or {}).get('checkpoint_hash')   # S0 nests S1
        checks['checkpoint_hash_matches'] = hashlib.sha256(checkpoint.encode()).hexdigest() == expected
    if stage in ('S1', 'D1'):
        checks.update(resimulate(stage, calls, rounds, checkpoint))
    metrics = detail.get('metrics') or {}
    checks['hub_metrics_match'] = (metrics.get('episodes') == saved['planned'] and metrics.get('invalid') == saved['planned'] - saved['accepted']
                                   and all(metrics.get(k) == saved[k] for k in ('model_calls', 'input_tokens', 'output_tokens', 'cost_usd')))
    return {'ok': all(v is True for v in checks.values()), 'checks': checks, 'run': entry['run'], 'calls': len(calls),
            'accepted': saved['accepted'], 'void': saved['void'], 'model_calls': saved['model_calls'], 'cost_usd': saved['cost_usd']}


def verify(sr, results_root=None, ledger_path=None):
    root = Path(results_root) if results_root else study.results_root()
    status = read_status(root)
    report = {'experiment': study.EXPERIMENT, 'source_hash': study.source_hash(), 'ok': False, 'stages': {}}
    if not status:
        report['error'] = 'no_chain_status'
        return report
    report['state'] = status.get('state')
    for stage in study.STAGES:
        entry = (status.get('stages') or {}).get(stage)
        if entry and entry.get('run') and entry.get('results_dir'):
            try:
                report['stages'][stage] = verify_stage(sr, stage, entry)
            except Exception as exc:
                report['stages'][stage] = {'ok': False, 'error': type(exc).__name__}
    ledger_path = ledger_path or os.environ.get(provider.LEDGER_ENV)
    if ledger_path and Path(ledger_path).exists():
        budget = study.design()['budget']
        slow = provider.Ledger(ledger_path, study.ledger_budget()).transact()
        mine = {study.params(s)['batch'] for s in study.STAGES}
        earlier = 0                          # reservations of earlier attempts in the same ledger file (attempt 001: one P0 call)
        for line in Path(ledger_path).read_text().splitlines():
            e = json.loads(line) if line.strip() else {}
            if e.get('type') == 'reserve' and not e['call_id'].startswith(transport.REISSUE_PREFIX) \
                    and e['call_id'].split(':', 1)[0] not in mine:
                earlier += 1
        fast = transport.FastLedger(ledger_path, study.ledger_budget()).transact()
        calls = sum(s.get('model_calls', 0) for s in report['stages'].values())
        report['ledger'] = {'totals_agree': slow == fast, 'attempted_calls': slow['attempted_calls'],
                            'actual_usd': slow['actual_usd'], 'committed_usd': slow['committed_usd'],
                            'reissued_calls': slow['calls_by_stage'].get('REISSUE', 0),
                            'carried_from_earlier_attempts': earlier,
                            'calls_match_stage_records': slow['attempted_calls'] - slow['calls_by_stage'].get('REISSUE', 0) - earlier == calls}
    report['ok'] = bool(report['stages']) and all(s['ok'] for s in report['stages'].values()) and \
        (report.get('ledger') or {'totals_agree': True}).get('totals_agree', True)
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='command', required=True)
    r = sub.add_parser('run')
    r.add_argument('--stages', required=True, help='ordered contiguous sub-list, e.g. S0,P0,Q0,X0,S1,D1')
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
