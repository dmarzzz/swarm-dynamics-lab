"""Chain driver (coordinator process): each stage behind its software gate, executed in this process.

    python src/chain.py run --stages S0,P0,Q0,X0,S1   exit 0 done, 3 stopped at a stage or gate, else internal error
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

import coordinator
import openai_provider as provider
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
    if stages and stages[-1] == 'D1':
        stages = stages[:-1]           # the ready-chain stage list ends with D1; this study does not use it
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
              'source_hash': study.source_hash(), 'code': study.code_revision(), 'model': study.model_name(),

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
        prior = {}
        try:
            runs = sr.runs(study.EXPERIMENT, limit=5000)
            coordinator.gate(runs, stage, p)
            if stage == 'Q0':
                p0 = coordinator.stage_runs(runs, 'P0', p['source_hash'], p['model'])
                prior['p0_correct'] = int(((p0[0].get('metrics') or {}) if len(p0) == 1 else {}).get('p0_correct') or 0)
            if stage == 'S1':
                x0 = coordinator.stage_runs(runs, 'X0', p['source_hash'], p['model'])
                metrics = (x0[0].get('metrics') or {}) if len(x0) == 1 else {}
                prior['batches_admitted'] = int(metrics.get('batches_admitted') or 0)
                entry['batches_admitted'] = prior['batches_admitted']
                if prior['batches_admitted'] < 1:
                    raise ValueError('no_batches_admitted')
        except ValueError as exc:
            return refuse(stage, entry, str(exc))
        except Exception as exc:
            return refuse(stage, entry, 'gate_error_' + type(exc).__name__)
        dispatcher = holder.get('dispatcher')
        if stage != 'S0' and dispatcher is None:
            dispatcher = transport.HubDispatcher(sr, transport.FastLedger(ledger_path, study.ledger_budget()), study.provider_config(),
                                                 d['workers'], root / 'transport', d['attempt'] + '-' + p['batch'],
                                                 poll=poll, allow_shared_host=allow_shared_host,
                                                 **{k: v for k, v in (transport_options or {}).items() if k not in ('dispatch_stop_seconds', 'governor_scale')})
            g = budget['governor']
            scale = (transport_options or {}).get('governor_scale', 1)       # rehearsal only: a faster stub quota
            dispatcher.governor = {'token_limit_per_minute': g['token_limit_per_minute'] * scale,
                                   'request_limit_per_minute': g['request_limit_per_minute'] * scale, 'fraction': g['fraction'],
                                   'workers': d['workers'], 'max_completion_tokens': budget['max_output_tokens']}
            holder['dispatcher'] = dispatcher
            try:
                status['worker_hosts'] = dispatcher.attach(budget['worker_attach_seconds'])
                status['worker_sessions'] = dispatcher.sessions
                status['distinct_hosts'] = len(set(status['worker_hosts'])) == len(status['worker_hosts'])
            except transport.StageStop as exc:
                return refuse(stage, entry, exc.reason)
        if stage != 'S0' and dispatcher.stop_at is None:
            # The execution clock starts at the first paid request (P0): new requests stop at T0 + 52 minutes.
            t0 = time.time()
            dispatcher.stop_at = t0 + (transport_options or {}).get('dispatch_stop_seconds', budget['dispatch_stop_seconds'])
            status['t0'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t0))
            status['dispatch_stop'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(dispatcher.stop_at))
        run_id = f'{study.EXPERIMENT}/{p["batch"]}'
        run = sr.start(study.EXPERIMENT, run=run_id, params=p, message=f'{stage} started by the chain')
        status['stages'][stage] = entry
        out = root / f'{run.id.replace("/", "__")}'
        entry.update(status='running', run=run.id, results_dir=str(out), in_flight_per_host=in_flight)
        write_status(root, status)
        summary, failed = None, None
        try:
            with run:
                summary = worker.execute(p, out, run, dispatcher, chain_deadline, prior)
        except worker.StageFailed as exc:
            summary, failed = exc.summary, exc.reason
        entry.update(_usage(summary), ended=now())
        if failed:
            entry.update(status='failed', reason=failed)
            write_status(root, status)
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
           'rejected_commands': summary['rejected_commands'], 'normalized': summary.get('normalized'),
           'dropped_zero_orders': summary.get('dropped_zero_orders'), 'normalizations': summary.get('normalizations'), 'gate_passed': summary['gate']['passed'],
           'elapsed_seconds': summary['elapsed_seconds'], 'hosts': summary.get('hosts'), 'billing': summary.get('billing'),
           'transport': {k: v for k, v in (summary.get('transport') or {}).items() if k != 'events'} or None}
    detail = summary.get('detail') or {}
    for key in ('batches_admitted', 'choices', 'opening_wave', 'mature_wave', 'mature_mean_cost_usd', 'seeders_passed', 'rounds_completed', 'valid_actions',
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


def resimulate_s1(calls, rounds, detail):
    """Re-run S1 from the frozen scientific worlds with the saved answers; compare every saved round record."""
    d = study.design()
    answers = {c['unit']: c for c in calls}
    saved = {}
    for rec in rounds:
        saved[(rec['econ'], rec['round'], rec['market'])] = {k: v for k, v in rec.items() if k not in ('econ', 'label')}
    state = {'same': True, 'missing': 0}

    def replay(econ):
        sim.begin_round(econ.state)
        responses, failures = {}, {}
        for oid, o in econ.state['owners'].items():
            if o['inactive']:
                continue
            c = answers.get(econ.unit(oid))
            if c is None:
                state['missing'] += 1
                responses[oid] = None
                continue
            responses[oid] = c['answer'] if c['ok'] else None
            if not c['ok']:
                failures[oid] = 'call_failed:' + str(c.get('category'))
        for rec in sim.step(econ.state, responses, failures):
            state['same'] = state['same'] and _plain(rec) == saved.get((econ.key, rec['round'], rec['market']))
    names = detail.get('batches') or []
    checks = {}
    openings = [study.Economy(f'{b}.open', study.scientific_world(b), [], slot=i) for i, b in enumerate(names)]
    for r in range(d['opening_rounds']):
        for e in openings:
            replay(e)
    for e, b in zip(openings, names):
        checks[f'checkpoint_{b}'] = sim.state_hash(e.state) == (detail.get('checkpoints') or {}).get(b, {}).get('state_hash')
        for arm in 'ABCD':
            econ = study.Economy(f'{b}.{arm}', sim.fork(sim.dumps(e.state), arm), [], slot=0)
            for r in range((detail.get('rounds_completed') or {}).get(econ.key, 0)):
                replay(econ)
    checks['rounds_resimulated'] = state['same'] and state['missing'] == 0
    return checks


def verify_stage(sr, stage, entry):
    checks = {}
    out = Path(entry['results_dir'])
    detail = sr.get_run(entry['run']) or {}
    hub = {a['name']: a['sha256'] for a in detail.get('artifacts') or []}
    checks['artifacts_match_hub'] = bool(hub) and all((out / n).is_file() and _sha256(out / n) == h for n, h in hub.items())
    checks['artifacts_complete'] = set(worker.ARTIFACTS) <= set(hub)
    checks['hub_status_matches'] = detail.get('status') == entry.get('status')
    try:
        calls = _rows(out / 'calls.jsonl.gz')
        rounds = _rows(out / 'rounds.jsonl.gz')
        saved = json.loads((out / 'summary.json').read_text())
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
    checks['call_ids_unique'] = len({c['call_id'] for c in calls}) == len(calls)
    checks['prompts_match_their_hashes'] = all(c['user'] is None or sim.digest(c['user']) == c['user_sha256'] for c in calls)
    if stage == 'S1':
        checks.update(resimulate_s1(calls, rounds, saved.get('detail') or {}))
    metrics = detail.get('metrics') or {}
    checks['hub_metrics_match'] = all(metrics.get(k) == saved[k] for k in ('model_calls', 'input_tokens', 'output_tokens', 'cost_usd'))
    return {'ok': all(v is True for v in checks.values()), 'checks': checks, 'run': entry['run'], 'calls': len(calls),
            'accepted': saved['accepted'], 'void': saved['void'], 'model_calls': saved['model_calls'], 'cost_usd': saved['cost_usd']}


def _rows(path):
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


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
    r.add_argument('--stages', required=True, help='ordered contiguous sub-list, e.g. S0,P0,Q0,X0,S1')
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
