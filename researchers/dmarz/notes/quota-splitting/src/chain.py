"""The ready chain: S0 -> P0 -> Q0 -> S1 in one process, each stage one hub run behind a software gate.

  python src/chain.py run --stages S0,P0,Q0,S1   exit 0 all requested stages done, 3 stopped at a
                                                 failed stage or gate, other non-zero internal error
  python src/chain.py status                     chain-status.json plus ledger totals, one JSON line
  python src/chain.py verify                     artifact checksums against the hub, every episode
                                                 replayed from its saved answers, the gates and the
                                                 analysis recomputed; one JSON line

Outputs go under STUDY_RESULTS_DIR (default <study>/results). Nothing here retries a stage or
queues anything after a failed gate. status and verify need no model credential.
"""
import argparse
import gzip
import hashlib
import json
import math
import os
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analyze      # noqa: E402
import coordinator  # noqa: E402
import manifest     # noqa: E402
import provider     # noqa: E402
import study        # noqa: E402
import worker       # noqa: E402

EXIT_DONE, EXIT_STOPPED, EXIT_INTERNAL = 0, 3, 1


def now():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def status_path():
    return study.results_dir() / 'chain-status.json'


def write_status(status):
    path = status_path(); path.parent.mkdir(parents=True, exist_ok=True)
    status['updated'] = now()
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix='.chain-status-', suffix='.tmp')
    with os.fdopen(fd, 'w') as f:
        json.dump(status, f, indent=2, sort_keys=True); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def read_status():
    path = status_path()
    return json.loads(path.read_text()) if path.exists() else None


def parse_stages(text):
    stages = [s.strip().upper() for s in text.split(',') if s.strip()]
    order = list(study.STAGES)
    if not stages or any(s not in order for s in stages): raise SystemExit('stages must be taken from ' + ','.join(order))
    first = order.index(stages[0])
    if stages != order[first:first + len(stages)]: raise SystemExit('stages must be an ordered contiguous sub-list of ' + ','.join(order))
    return stages


def ledger_totals():
    path = os.environ.get('STUDY_BUDGET_LEDGER')
    if not path or not Path(path).exists(): return None
    return provider.Ledger(path).transact()


def projection(q0_run):
    """The two written rules checked before S1 is queued, both from Q0's measured usage.
    Cost: Q0's cost per call x the frozen growth factor x the S1 call cap must fit in what is left
    under the dollar cap. Output room: no Q0 call may have used more than the frozen share of
    max_output_tokens, because one response cut off at the limit would end S1."""
    b = study.design()['budget']; metrics = q0_run.get('metrics') or {}
    calls = metrics.get('model_calls') or 0
    if not calls or metrics.get('cost_usd') is None or metrics.get('max_output_tokens_per_call') is None:
        return {'projected_usd': None, 'reason': 'q0_usage_missing'}
    per_call = metrics['cost_usd'] / calls
    projected = per_call * b['projection_growth_factor'] * b['max_calls']['S1']
    totals = ledger_totals() or {}
    remaining = b['aggregate_usd'] - totals.get('committed_usd', 0.0)
    room = b['output_headroom_fraction'] * b['max_output_tokens']
    return {'projected_usd': projected, 'remaining_usd': remaining, 'q0_cost_per_call_usd': per_call,
            'growth_factor': b['projection_growth_factor'], 's1_call_cap': b['max_calls']['S1'], 'within_cap': projected <= remaining,
            'q0_max_output_tokens_per_call': metrics['max_output_tokens_per_call'], 'output_tokens_allowed_in_q0': room,
            'output_room_ok': metrics['max_output_tokens_per_call'] <= room}


def run_chain(stages, sr=None, opener=None):
    if sr is None:
        import swarm_report as sr
    budget = study.design()['budget']; deadline = time.monotonic() + budget['chain_timeout_seconds']
    status = read_status()
    if status and status.get('source_hash') != study.source_hash():
        # records of another source version are kept beside the new status, never mixed into it
        os.replace(status_path(), status_path().with_name(f'chain-status-{str(status.get("source_hash"))[:12]}.json'))
        status = None
    status = status or {'experiment': study.EXPERIMENT, 'contract': 'ready-chain-v1', 'stages': {}}
    status.update(state='running', source_hash=study.source_hash(), code=study.code_revision(), requested=stages,
                  started=status.get('started') or now(), stopped_stage=None, reason=None)
    write_status(status)

    def stop(stage, reason, code):
        status.update(state='stopped_at_gate', stopped_stage=stage, reason=reason, ledger=ledger_totals())
        write_status(status)
        print(json.dumps({'state': 'stopped_at_gate', 'stage': stage, 'reason': reason}))
        return code

    for stage in stages:
        entry = {'status': 'gating', 'batch': study.batch(stage)}; status['stages'][stage] = entry; write_status(status)
        try:
            if time.monotonic() > deadline:
                entry['status'] = 'refused'
                return stop(stage, 'chain_deadline', EXIT_STOPPED)
            _, before = coordinator.check(sr, stage)
            if stage == 'S1':
                entry['projection'] = projection(before)
                if not entry['projection'].get('within_cap'):
                    entry['status'] = 'refused'
                    return stop(stage, 'projection_exceeds_cap', EXIT_STOPPED)
                if not entry['projection'].get('output_room_ok'):
                    entry['status'] = 'refused'
                    return stop(stage, 'output_room_too_small', EXIT_STOPPED)
            ids = coordinator.enqueue(sr, stage)
            run = sr.next_run(study.EXPERIMENT)
        except coordinator.GateRefused as exc:
            entry['status'] = 'refused'
            return stop(stage, str(exc), EXIT_STOPPED)
        except Exception as exc:        # hub unreachable, unreadable manifest, ...: nothing was executed
            entry['status'] = 'failed'
            return stop(stage, 'internal_' + type(exc).__name__, EXIT_INTERNAL)
        if run is None or run.id != ids[0] or run.attempt != 1:
            entry.update(status='failed', run=ids[0])
            return stop(stage, 'queued_run_not_received', EXIT_INTERNAL)
        out = study.results_dir() / f'{run.id.replace("/", "__")}-attempt-{run.attempt}'
        entry.update(status='running', run=run.id, directory=str(out), started=now()); write_status(status)
        outcome, code = 'done', None
        try:
            with run:
                worker.execute(run.params, out, run, deadline=deadline, opener=opener)
        except worker.StageFailed as exc:
            outcome, code, reason = 'failed', EXIT_STOPPED, str(exc)
        except Exception as exc:
            outcome, code, reason = 'failed', EXIT_INTERNAL, 'internal_' + type(exc).__name__
        entry.update(status=outcome, ended=now())
        summary_file = out / 'summary.json'
        if summary_file.exists():
            s = json.loads(summary_file.read_text())
            entry.update(calls=s['model_calls'], transport_attempts=s['transport_attempts'], input_tokens=s['input_tokens'],
                         max_output_tokens_per_call=s.get('max_output_tokens_per_call'),
                         output_tokens=s['output_tokens'], cost_usd=s['cost_usd'], planned=s['planned'], valid=s['graded'],
                         invalid=s['invalid'], not_started=s['not_started'], qualification_passed=s['qualification_passed'],
                         errors=s['errors'])
        status['ledger'] = ledger_totals(); write_status(status)
        if outcome != 'done':
            return stop(stage, reason, code)
    status.update(state='completed', all_stages_done=all(status['stages'].get(s, {}).get('status') == 'done' for s in study.STAGES),
                  ledger=ledger_totals())
    write_status(status)
    print(json.dumps({'state': 'completed', 'stages': stages}))
    return EXIT_DONE


def show_status():
    status = read_status()
    print(json.dumps({'chain': status, 'ledger': ledger_totals(), 'results_dir': str(study.results_dir()),
                      'source_hash': study.source_hash()}, sort_keys=True))
    return 0


def close(a, b):
    if isinstance(a, float) or isinstance(b, float):
        if a is None or b is None or isinstance(a, (str, list, dict)) or isinstance(b, (str, list, dict)): return a == b
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(close(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
    return a == b


def read_jsonl(path):
    with gzip.open(path, 'rt') as f: return [json.loads(line) for line in f if line.strip()]


def regrade(a, r):
    """True when replaying the saved answers through the engine gives the saved turn records,
    input hashes, outcome and reference outcomes."""
    try: turns, outcome = study.replay(a, [t['answer'] for t in r['turns']])
    except (ValueError, AssertionError, KeyError, TypeError): return False
    same_turns = len(turns) == len(r['turns']) and all(
        close(t['results'], s['results']) and t['clean'] == s['clean'] and t['input_hash'] == s['input_hash'] and t['round'] == s['round']
        for t, s in zip(turns, r['turns']))
    if r['status'] != 'completed': return same_turns
    return same_turns and close(outcome, r['outcome']) and close(study.reference(a), r['reference']) \
        and close(study.spawn_notes(r['turns']), r['spawn_notes'])


def verify_stage(sr, stage, entry, reference):
    checks = {}; out = Path(entry['directory'])
    detail = sr.get_run(entry['run']); hub = {a['name']: a for a in detail.get('artifacts', [])}
    checks['hub_status_matches'] = detail.get('status') == entry['status']
    checks['hub_has_every_artifact'] = all(name in hub for name in worker.ARTIFACTS)
    checks['artifact_checksums'] = bool(hub) and all(
        (out / name).is_file() and hashlib.sha256((out / name).read_bytes()).hexdigest() == a['sha256'] for name, a in hub.items())
    assigned = read_jsonl(out / 'assignments.jsonl.gz'); rows = read_jsonl(out / 'episodes.jsonl.gz'); calls = read_jsonl(out / 'turns.jsonl.gz')
    by_id = {a['id']: a for a in assigned}
    checks['every_episode_has_one_row'] = sorted(r['id'] for r in rows) == sorted(by_id)
    fresh = {a['id']: a for a in (study.assignment(*(a[k] for k in study.ID_FIELDS), a['max_turns']) for a in assigned)}
    checks['fixed_inputs_regenerate'] = all(close(json.loads(json.dumps(fresh[i])), a) for i, a in by_id.items()) and all(
        r['fixed_hash'] == by_id[r['id']]['fixed_hash'] for r in rows if r['id'] in by_id)
    checks['manifest_matches'] = manifest.stage_entry(assigned)['digest'] == reference['stages'][stage]['digest']
    good = [r for r in rows if r['status'] == 'completed']
    checks['episodes_replayed'] = all(regrade(by_id[r['id']], r) for r in rows if r['turns'])
    logged = sorted((c['episode'], c['round']) for c in calls)
    checks['turn_log_complete'] = logged == sorted((r['id'], t['round']) for r in rows for t in r['turns'] + ([r['failed_turn']] if r.get('failed_turn') and 'round' in r['failed_turn'] else []))
    summary = json.loads((out / 'summary.json').read_text()); saved = json.loads((out / 'analysis.json').read_text())
    compared = [r for r in rows if r['kind'] in analyze.KINDS]
    checks['analysis_recomputed'] = close(saved, json.loads(json.dumps(analyze.analyze(rows, analyze.actor(stage))))) if compared else saved.get('cells') == []
    t = worker.totals(rows, len(assigned))
    checks['totals_recomputed'] = all(close(float(summary[k]), float(v)) for k, v in t.items())
    violations = [v for v in summary.get('invariant_violations') or []]
    gate = study.gate(stage, rows, violations)
    checks['gate_recomputed'] = (None if gate is None else int(gate)) == summary['qualification_passed']
    metrics = detail.get('metrics') or {}
    checks['hub_metrics_match'] = all(k in metrics and close(float(metrics[k]), float(t[k])) for k in
                                      ('episodes', 'invalid', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd'))
    checks['source_hash_current'] = summary['params']['source_hash'] == study.source_hash()
    checks['call_cap_respected'] = t['model_calls'] <= study.design()['budget']['max_calls'][stage]
    return {'run': entry['run'], 'status': entry['status'], 'ok': all(checks.values()), 'checks': checks,
            'episodes': len(assigned), 'completed': len(good), 'model_calls': t['model_calls'], 'cost_usd': t['cost_usd']}


def verify(sr=None):
    if sr is None:
        import swarm_report as sr
    status = read_status()
    if not status:
        print(json.dumps({'ok': False, 'reason': 'no chain-status.json under ' + str(study.results_dir())})); return 1
    reference = manifest.load(); stages = {}
    for stage in study.STAGES:
        entry = status['stages'].get(stage)
        if not entry or 'run' not in entry or 'directory' not in entry: continue
        try: stages[stage] = verify_stage(sr, stage, entry, reference)
        except Exception as exc: stages[stage] = {'run': entry.get('run'), 'ok': False, 'error': type(exc).__name__ + ': ' + str(exc)[:200]}
    ok = bool(stages) and all(s['ok'] for s in stages.values())
    print(json.dumps({'ok': ok, 'state': status.get('state'), 'manifest_digest': reference['digest'], 'stages': stages}, sort_keys=True))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('run'); r.add_argument('--stages', default=','.join(study.STAGES))
    sub.add_parser('status'); sub.add_parser('verify')
    a = ap.parse_args(argv)
    if a.cmd == 'run': return run_chain(parse_stages(a.stages))
    if a.cmd == 'status': return show_status()
    return verify()


if __name__ == '__main__':
    sys.exit(main())
