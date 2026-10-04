"""The ready chain: S0 -> P0 -> Q0 -> S1 in one process, each stage one hub run behind a software gate.

  python src/chain.py run --stages S0,P0,Q0,S1   exit 0 all requested stages done, 3 stopped at a
                                                 failed stage or gate, other non-zero internal error
  python src/chain.py resume                     only after S1 stopped with provider_credit_balance_low
                                                 at this source hash: queues a continuation batch
                                                 s1-<attempt>-r<n> holding exactly the units not started
  python src/chain.py status                     chain-status.json plus ledger totals, one JSON line
  python src/chain.py verify                     artifact checksums against the hub, every grade, total,
                                                 gate and the analysis recomputed from saved rows
  python src/chain.py summarize                  the S1 analysis headline from saved rows, one JSON line

Outputs go under STUDY_RESULTS_DIR (default <study>/results). Nothing here retries a stage or
queues anything after a failed gate. status, verify and summarize need no model credential.
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
    path = os.environ.get(provider.LEDGER_ENV)
    if not path or not Path(path).exists(): return None
    return study.route().Ledger(path, study.adapter_config()['budget']).transact()


def read_jsonl(path):
    with gzip.open(path, 'rt') as f: return [json.loads(line) for line in f if line.strip()]


def run_directory(run_id):
    return study.results_dir() / f'{run_id.replace("/", "__")}-attempt-1'


def probe_rows(sr):
    """P0's saved row, taken from the results directory and checked against the hub: the run must
    be the single passed P0 run at this source hash, and the saved row must agree with the hub's
    record of whether the probe's answer was exactly right."""
    run = coordinator.passed_run(sr, 'P0')
    if run is None: return []
    path = run_directory(run.get('run') or run.get('id')) / 'episodes.jsonl.gz'
    if not path.exists(): return []
    rows = [r for r in read_jsonl(path) if r['kind'] == 'qualification' and r['status'] == 'completed']
    if len(rows) != 1 or rows[0]['source_hash'] != study.source_hash(): return []
    if int(bool(rows[0]['evaluation']['exact_packet'])) != (run.get('metrics') or {}).get('fixture_exact'): return []
    return rows


def input_ceiling(sr, stage):
    """Largest request of the stage in tokens, projected from the tokens per byte measured in the
    paid stages that have run (P0, and Q0 once it has run). None when nothing was measured."""
    measured = [m for m in ((coordinator.passed_run(sr, s) or {}).get('metrics', {}).get('max_tokens_per_byte') for s in ('P0', 'Q0')) if m]
    if not measured: return {'within_ceiling': False, 'reason': 'no_measured_tokens_per_byte'}
    largest = manifest.load()['stages'][stage]['max_request_bytes']; ceiling = study.adapter_config()['budget']['max_input_tokens']
    projected = max(measured) * largest
    return {'tokens_per_byte': max(measured), 'largest_request_bytes': largest, 'projected_input_tokens': projected,
            'ceiling': ceiling, 'within_ceiling': projected <= ceiling}


def cost_projection(q0_run):
    """Projected S1 spend: S1 calls times Q0's measured cost per call (requests have the same size)."""
    b = study.adapter_config()['budget']; metrics = q0_run.get('metrics') or {}; calls = metrics.get('model_calls') or 0
    if not calls: return {'projected_usd': None, 'within_cap': False, 'reason': 'q0_usage_missing'}
    per_call = (metrics.get('cost_usd') or 0) / calls; n = manifest.load()['stages']['S1']['assignments']
    remaining = b['aggregate_usd'] - (ledger_totals() or {}).get('committed_usd', 0.0)
    return {'projected_usd': n * per_call, 'remaining_usd': remaining, 'q0_cost_per_call_usd': per_call, 's1_calls': n,
            'within_cap': n * per_call <= remaining}


def record(entry, out):
    f = Path(out) / 'summary.json'
    if f.exists():
        s = json.loads(f.read_text())
        entry.update(calls=s['model_calls'], transport_attempts=s['transport_attempts'], input_tokens=s['input_tokens'],
                     output_tokens=s['output_tokens'], cost_usd=s['cost_usd'], planned=s['planned'], valid=s['graded'],
                     invalid=s['invalid'], failed=s['failed'], not_started=s['not_started'], qualification_passed=s['qualification_passed'],
                     errors=s['errors'], billing_pauses=s['billing_pauses'], billing_pause_seconds=s['billing_pause_seconds'],
                     resumable=s['resumable'], stop_reason=s['stop_reason'])


def run_chain(stages, sr=None, opener=None, clock=None, sleep=None):
    if sr is None:
        import swarm_report as sr
    budget = study.design()['budget']; deadline = time.monotonic() + budget['chain_timeout_seconds']
    status = read_status()
    if status and status.get('source_hash') != study.source_hash():
        os.replace(status_path(), status_path().with_name(f'chain-status-{str(status.get("source_hash"))[:12]}.json'))
        status = None
    if status and status.get('model') != study.model_name():
        # another model's chain record: kept beside, never mixed (the launcher gives each model its own results directory)
        os.replace(status_path(), status_path().with_name(f'chain-status-{str(status.get("model")).replace("/", "_")}.json'))
        status = None
    status = status or {'experiment': study.EXPERIMENT, 'contract': 'ready-chain-v1', 'stages': {}, 'model': study.model_name()}
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
        earlier = []
        try:
            if time.monotonic() > deadline:
                entry['status'] = 'refused'; return stop(stage, 'chain_deadline', EXIT_STOPPED)
            _, before = coordinator.check(sr, stage)
            if stage in ('Q0', 'S1'):
                entry['input_ceiling'] = input_ceiling(sr, stage)
                if not entry['input_ceiling'].get('within_ceiling'):
                    entry['status'] = 'refused'; return stop(stage, 'input_ceiling_projection', EXIT_STOPPED)
            if stage == 'S1':
                entry['projection'] = cost_projection(before)
                if not entry['projection'].get('within_cap'):
                    entry['status'] = 'refused'; return stop(stage, 'projection_exceeds_cap', EXIT_STOPPED)
            ids = coordinator.enqueue(sr, stage)
            run = sr.next_run(study.EXPERIMENT)
        except coordinator.GateRefused as exc:
            entry['status'] = 'refused'; return stop(stage, str(exc), EXIT_STOPPED)
        except Exception as exc:        # hub unreachable, unreadable manifest, ...: nothing was executed
            entry['status'] = 'failed'; return stop(stage, 'internal_' + type(exc).__name__, EXIT_INTERNAL)
        if run is None or run.id != ids[0] or run.attempt != 1:
            entry.update(status='failed', run=ids[0]); return stop(stage, 'queued_run_not_received', EXIT_INTERNAL)
        out = run_directory(run.id)
        entry.update(status='running', run=run.id, directory=str(out), started=now()); write_status(status)
        outcome, code = 'done', None
        try:
            with run:
                worker.execute(run.params, out, run, deadline=deadline, opener=opener, earlier_rows=earlier, clock=clock, sleep=sleep)
        except worker.StageFailed as exc:
            outcome, code, reason = 'failed', EXIT_STOPPED, str(exc)
        except Exception as exc:
            outcome, code, reason = 'failed', EXIT_INTERNAL, 'internal_' + type(exc).__name__
        entry.update(status=outcome, ended=now()); record(entry, out)
        status['ledger'] = ledger_totals(); write_status(status)
        if outcome != 'done':
            return stop(stage, reason, code)
    status.update(state='completed', all_stages_done=all(stage_done(status['stages'].get(s, {})) for s in study.STAGES),
                  ledger=ledger_totals())
    write_status(status)
    print(json.dumps({'state': 'completed', 'stages': stages}))
    return EXIT_DONE


def stage_done(entry):
    return entry.get('status') == 'done' or bool(entry.get('completed_by_continuation'))


def stage_rows(entry):
    """Rows of a stage's original run merged with its continuations: one row per unit."""
    rows = []
    for e in [entry] + list(entry.get('continuations') or []):
        if e.get('directory') and (Path(e['directory']) / 'episodes.jsonl.gz').exists():
            rows = worker.merge(rows, read_jsonl(Path(e['directory']) / 'episodes.jsonl.gz'))
    return rows


def resume(sr=None, opener=None, clock=None, sleep=None):
    """Continue S1 after a billing stop. Allowed only when the chain's last state is S1 stopped with
    provider_credit_balance_low at the current source hash. Queues one continuation run holding
    exactly the units not started, under the same ledger and caps."""
    if sr is None:
        import swarm_report as sr
    status = read_status()
    def refuse(reason):
        print(json.dumps({'state': 'resume_refused', 'reason': reason})); return EXIT_STOPPED
    if not status or status.get('source_hash') != study.source_hash(): return refuse('no_chain_status_at_this_source_hash')
    if not (status.get('state') == 'stopped_at_gate' and status.get('stopped_stage') == 'S1' and status.get('reason') == study.route().BILLING_STOP):
        return refuse('last_stop_was_not_a_billing_stop_of_S1')
    entry = status['stages']['S1']; prior = stage_rows(entry)
    units = [r['id'] for r in prior if r['status'] == 'not_started']
    if not units: return refuse('nothing_left_to_resume')
    n = len(entry.get('continuations') or []) + 1
    cont = {'status': 'gating', 'batch': f'{entry["batch"]}-r{n}', 'units': len(units)}
    try:
        ids = coordinator.enqueue_continuation(sr, n); run = sr.next_run(study.EXPERIMENT)
    except coordinator.GateRefused as exc:
        return refuse(str(exc))
    if run is None or run.id != ids[0] or run.attempt != 1: return refuse('queued_run_not_received')
    out = run_directory(run.id); cont.update(status='running', run=run.id, directory=str(out), started=now())
    entry.setdefault('continuations', []).append(cont)
    status.update(state='running', stopped_stage=None, reason=None); write_status(status)
    deadline = time.monotonic() + study.design()['budget']['chain_timeout_seconds']
    outcome, code, reason = 'done', EXIT_DONE, None
    try:
        with run:
            worker.execute(run.params, out, run, deadline=deadline, opener=opener, units=units, prior_rows=prior, clock=clock, sleep=sleep)
    except worker.StageFailed as exc:
        outcome, code, reason = 'failed', EXIT_STOPPED, str(exc)
    except Exception as exc:
        outcome, code, reason = 'failed', EXIT_INTERNAL, 'internal_' + type(exc).__name__
    cont.update(status=outcome, ended=now()); record(cont, out); status['ledger'] = ledger_totals()
    if outcome != 'done':
        status.update(state='stopped_at_gate', stopped_stage='S1', reason=reason); write_status(status)
        print(json.dumps({'state': 'stopped_at_gate', 'stage': 'S1', 'reason': reason, 'continuation': cont['batch']})); return code
    entry['completed_by_continuation'] = cont['batch']      # the original run keeps its own status
    status.update(state='completed', all_stages_done=all(stage_done(status['stages'].get(s, {})) for s in study.STAGES))
    write_status(status)
    print(json.dumps({'state': 'completed', 'stages': ['S1'], 'continuation': cont['batch'], 'units': len(units)}))
    return EXIT_DONE


def show_status():
    print(json.dumps({'chain': read_status(), 'ledger': ledger_totals(), 'results_dir': str(study.results_dir()),
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


def verify_run(sr, stage, entry, reference, prior_rows, earlier_rows):
    checks = {}; out = Path(entry['directory']); budget = study.design()['budget']
    detail = sr.get_run(entry['run']); hub = {a['name']: a for a in detail.get('artifacts', [])}
    checks['hub_status_matches'] = detail.get('status') == entry['status']
    checks['hub_has_every_artifact'] = all(name in hub for name in worker.ARTIFACTS)
    checks['artifact_checksums'] = bool(hub) and all(
        (out / name).is_file() and hashlib.sha256((out / name).read_bytes()).hexdigest() == a['sha256'] for name, a in hub.items())
    assigned = read_jsonl(out / 'assignments.jsonl.gz'); rows = read_jsonl(out / 'episodes.jsonl.gz')
    by_id = {a['id']: a for a in assigned}
    checks['every_assignment_has_one_row'] = sorted(r['id'] for r in rows) == sorted(by_id)
    checks['packet_hashes'] = all(study.digest(a['packet']) == a['packet_hash'] for a in assigned) and all(
        r['packet_hash'] == by_id[r['id']]['packet_hash'] for r in rows if r['id'] in by_id)
    listed = {x.split(':')[0] for x in reference['stages'][stage]['ids']}
    checks['manifest_matches'] = (manifest.stage_entry(assigned)['digest'] == reference['stages'][stage]['digest']) if prior_rows is None else set(by_id) <= listed
    good = [r for r in rows if r['status'] == 'completed']
    checks['grades_recomputed'] = all(
        close(r['evaluation'], study.evaluate(by_id[r['id']], r['answer']))
        and close(r['scripted_evaluation'], study.evaluate(by_id[r['id']], study.scripted(by_id[r['id']]['packet'])))
        and close(r['identity_evaluation'], study.evaluate(by_id[r['id']], study.scripted(by_id[r['id']]['packet'], by_identity=True)))
        and r['model'] == study.model_name() for r in good)
    checks['failed_rows_keep_evidence'] = all(r.get('error') and isinstance(r.get('accounting'), dict) for r in rows if r['status'] == 'failed')
    summary = json.loads((out / 'summary.json').read_text()); saved = json.loads((out / 'analysis.json').read_text())
    whole = worker.merge(prior_rows, rows)
    grid = [r for r in whole if r['kind'] == 'pilot']
    checks['analysis_recomputed'] = close(saved, json.loads(json.dumps(analyze.analyze(whole)))) if grid else saved.get('cells') == []
    t = worker.totals(rows, len(assigned))
    checks['totals_recomputed'] = all(close(float(summary[k]), float(v)) for k, v in t.items())
    gate = study.gate(stage, rows, [v for v in summary.get('invariant_violations') or []], earlier_rows)
    checks['gate_recomputed'] = (None if gate is None else int(gate)) == summary['qualification_passed']
    if stage in worker.STRICT:
        want = t['invalid'] == 0 and gate is True
    else:
        want = summary['stop_reason'] is None and t['failed'] <= budget['max_failed'] and t['invalid'] == t['failed']
    checks['outcome_recomputed'] = want == summary['passed'] == (entry['status'] == 'done')
    metrics = detail.get('metrics') or {}
    checks['hub_metrics_match'] = all(k in metrics and close(float(metrics[k]), float(t[k])) for k in t)
    checks['source_hash_current'] = summary['params']['source_hash'] == study.source_hash()
    checks['call_cap_respected'] = t['model_calls'] <= budget['max_calls'][stage]
    return {'run': entry['run'], 'batch': entry.get('batch'), 'status': entry['status'], 'ok': all(checks.values()), 'checks': checks,
            'assigned': len(assigned), 'completed': len(good), 'failed': t['failed'], 'model_calls': t['model_calls'], 'cost_usd': t['cost_usd']}, rows


def s1_whole(entry, reference):
    """S1 as a whole, from its original run and continuations: every unit exactly once."""
    rows = stage_rows(entry); listed = sorted(x.split(':')[0] for x in reference['stages']['S1']['ids'])
    a = analyze.analyze(rows) if rows else None
    everything = [r for e in [entry] + list(entry.get('continuations') or []) if e.get('directory') and (Path(e['directory']) / 'episodes.jsonl.gz').exists()
                  for r in read_jsonl(Path(e['directory']) / 'episodes.jsonl.gz')]
    calls = sum(bool((r.get('accounting') or {}).get('attempted')) and not (r.get('accounting') or {}).get('voided') for r in everything)
    return {'every_unit_exactly_once': sorted(r['id'] for r in rows) == listed,
            'model_calls_all_runs': calls, 'calls_within_cap': calls <= study.design()['budget']['max_calls']['S1'],
            'completed': sum(r['status'] == 'completed' for r in rows), 'failed': sum(r['status'] == 'failed' for r in rows),
            'not_started': sum(r['status'] == 'not_started' for r in rows),
            'model': study.model_name(),
            'primary': None if not a else {k: a['primary'][k] for k in ('estimate', 'interval', 'by_family', 'assigned_roots', 'bounds_all_assigned')},
            'versus_parent': None if not a else a.get('versus_parent', {}).get('primary'),
            'test_retest': None if not a else a['test_retest']}


def verify(sr=None):
    if sr is None:
        import swarm_report as sr
    status = read_status()
    if not status:
        print(json.dumps({'ok': False, 'reason': 'no chain-status.json under ' + str(study.results_dir())})); return 1
    reference = manifest.load(); stages = {}; earlier = []
    for stage in study.STAGES:
        entry = status['stages'].get(stage)
        if not entry or 'run' not in entry or 'directory' not in entry: continue
        try:
            stages[stage], rows = verify_run(sr, stage, entry, reference, None, earlier if stage == 'Q0' else ())
            if stage == 'P0': earlier = [r for r in rows if r['status'] == 'completed']
            prior = rows
            for n, cont in enumerate(entry.get('continuations') or [], 1):
                if 'directory' not in cont: continue
                stages[f'{stage}-r{n}'], more = verify_run(sr, stage, cont, reference, prior, ())
                prior = worker.merge(prior, more)
        except Exception as exc:
            stages[stage] = {'run': entry.get('run'), 'ok': False, 'error': type(exc).__name__ + ': ' + str(exc)[:200]}
    whole = s1_whole(status['stages']['S1'], reference) if 'directory' in status['stages'].get('S1', {}) else None
    ok = bool(stages) and all(s['ok'] for s in stages.values()) and (whole is None or (whole['every_unit_exactly_once'] and whole['calls_within_cap']))
    print(json.dumps({'ok': ok, 'state': status.get('state'), 'manifest_digest': reference['digest'], 'stages': stages, 'S1': whole}, sort_keys=True))
    return 0 if ok else 1


def summarize():
    status = read_status()
    if not status or 'directory' not in status['stages'].get('S1', {}):
        print(json.dumps({'ok': False, 'reason': 'no S1 run recorded under ' + str(study.results_dir())})); return 1
    print(json.dumps({'ok': True, 'state': status.get('state'), 'S1': s1_whole(status['stages']['S1'], manifest.load())}, sort_keys=True))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('run'); r.add_argument('--stages', default=','.join(study.STAGES))
    for name in ('status', 'verify', 'resume', 'summarize'): sub.add_parser(name)
    a = ap.parse_args(argv)
    if a.cmd == 'run': return run_chain(parse_stages(a.stages))
    if a.cmd == 'resume': return resume()
    if a.cmd == 'status': return show_status()
    if a.cmd == 'summarize': return summarize()
    return verify()


if __name__ == '__main__':
    sys.exit(main())
