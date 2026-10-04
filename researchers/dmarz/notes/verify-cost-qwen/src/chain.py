"""The ready chain: S0 -> P0 -> Q0 -> S1 in one process, each stage one hub run behind a software gate.

  python src/chain.py run --stages S0,P0,Q0,S1   exit 0 all requested stages done, 3 stopped at a
                                                 failed stage or gate, other non-zero internal error
  python src/chain.py resume                     only after S1 stopped with provider_credit_balance_low at
                                                 this source hash: queues a continuation batch s1-001-r<n>
                                                 with exactly the units left not started; same ledger
  python src/chain.py status                     chain-status.json plus ledger totals, one JSON line
  python src/chain.py verify                     artifact checksums against the hub, every request
                                                 regenerated, every saved answer regraded, the gates and
                                                 the analysis recomputed; one JSON line

Outputs go under STUDY_RESULTS_DIR (default <study>/results). Nothing here retries a stage or queues
anything after a failed gate. status and verify need no model credential.
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
ROWS = 'episodes.jsonl.gz'


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
    return provider.Ledger(path, study.design()['budget']).transact()


def read_jsonl(path):
    with gzip.open(path, 'rt') as f: return [json.loads(line) for line in f if line.strip()]


def run_directory(run_id, attempt=1):
    return study.results_dir() / f'{run_id.replace("/", "__")}-attempt-{attempt}'


def probe_rows(sr):
    """P0's saved row, read from the results directory and checked against the hub: the one passed P0 run at
    this source hash, whose uploaded row file has the same checksum as the local one. Raises GateRefused."""
    run = coordinator.probe_run(sr)
    path = run_directory(run['run']) / ROWS
    hub = {a['name']: a for a in sr.get_run(run['run']).get('artifacts', [])}
    if not path.is_file() or ROWS not in hub or hashlib.sha256(path.read_bytes()).hexdigest() != hub[ROWS].get('sha256'):
        raise coordinator.GateRefused('probe_row_unavailable')
    rows = read_jsonl(path)
    if study.qualification_rows([], rows) is None: raise coordinator.GateRefused('probe_row_unavailable')
    return rows


def projection(sr, q0_run):
    """The two written rules checked before S1 is queued.
    Cost: Q0's measured mean cost per call x the S1 call cap must fit in what is left under the dollar cap.
    Input ceiling: P0's measured input tokens per byte of message content x the largest S1 request must not
    exceed the input ceiling."""
    b = study.design()['budget']; metrics = q0_run.get('metrics') or {}
    calls = metrics.get('model_calls') or 0
    if not calls or metrics.get('cost_usd') is None:
        return {'reason': 'q0_usage_missing', 'within_cap': False, 'input_ceiling_ok': False}
    per_call = metrics['cost_usd'] / calls; projected = per_call * b['max_calls']['S1']
    totals = ledger_totals() or {}; remaining = b['aggregate_usd'] - totals.get('committed_usd', 0.0)
    out = {'q0_cost_per_call_usd': per_call, 's1_call_cap': b['max_calls']['S1'], 'projected_usd': projected,
           'remaining_usd': remaining, 'within_cap': projected <= remaining}
    ratio = (coordinator.probe_run(sr).get('metrics') or {}).get('probe_tokens_per_byte')
    largest = max(a['content_bytes'] for a in study.assignments('S1'))
    out.update(probe_tokens_per_byte=ratio, largest_s1_content_bytes=largest, input_ceiling_tokens=b['max_input_tokens'],
               projected_input_tokens=None if ratio is None else ratio * largest,
               input_ceiling_ok=ratio is not None and ratio * largest <= b['max_input_tokens'])
    return out


def execute_run(run, entry, status, deadline, opener, **kwargs):
    """Execute one queued run in this process and record it in `entry`. Returns (outcome, exit code, reason)."""
    out = run_directory(run.id, run.attempt)
    entry.update(status='running', run=run.id, directory=str(out), started=now()); write_status(status)
    outcome, code, reason = 'done', None, None
    try:
        with run:
            worker.execute(run.params, out, run, deadline=deadline, opener=opener, **kwargs)
    except worker.StageFailed as exc:
        outcome, code, reason = 'failed', EXIT_STOPPED, str(exc)
    except Exception as exc:
        outcome, code, reason = 'failed', EXIT_INTERNAL, 'internal_' + type(exc).__name__
    entry.update(status=outcome, ended=now())
    summary_file = out / 'summary.json'
    if summary_file.exists():
        s = json.loads(summary_file.read_text())
        entry.update(calls=s['model_calls'], answered_calls=s['answered_calls'], transport_attempts=s['transport_attempts'],
                     input_tokens=s['input_tokens'], output_tokens=s['output_tokens'], cost_usd=s['cost_usd'], planned=s['planned'],
                     valid=s['graded'], invalid=s['invalid'], failed=s['failed'], not_started=s['not_started'],
                     qualification_passed=s['qualification_passed'], errors=s['errors'], billing_pauses=s['billing_pauses'],
                     billing_pause_seconds=s['billing_pause_seconds'], billing_affected_calls=s['billing_affected_calls'],
                     resumable=s['resumable'], unanswered_reservations=s['unanswered_reservations'],
                     table_minus_prose_regret=s['table_minus_prose_regret'], reason=s['reason'])
    status['ledger'] = ledger_totals(); write_status(status)
    return outcome, code, reason


def stage_rows(entry):
    """Rows of a stage's original run followed by its continuations, in run order."""
    rows = []
    for e in [entry] + list(entry.get('continuations') or []):
        if e.get('directory') and (Path(e['directory']) / ROWS).exists(): rows += read_jsonl(Path(e['directory']) / ROWS)
    return rows


def resume(sr=None, opener=None):
    """Continue S1 after a billing stop. Allowed only when the chain's last state is S1 stopped with
    provider_credit_balance_low at the current source hash. Queues one continuation run holding exactly the
    units that stop left not started and executes it under the same ledger."""
    if sr is None:
        import swarm_report as sr
    status = read_status(); entry = ((status or {}).get('stages') or {}).get('S1') or {}

    def refuse(reason):
        print(json.dumps({'state': 'resume_refused', 'reason': reason})); return EXIT_STOPPED
    if not status or status.get('source_hash') != study.source_hash(): return refuse('no_chain_at_this_source_hash')
    if status.get('state') != 'stopped_at_gate' or status.get('stopped_stage') != 'S1' or status.get('reason') != provider.BILLING_STOP:
        return refuse('last_stop_was_not_a_billing_stop_of_S1')
    prior = stage_rows(entry); final = study.combine(prior)
    units = [a['id'] for a in study.assignments('S1') if any(r['id'] == a['id'] and r['status'] == 'not_started' for r in final)]
    if not units or len(final) != len(study.assignments('S1')): return refuse('no_unfinished_units')
    n = len(entry.get('continuations') or []) + 1
    budget = study.design()['budget']; deadline = time.monotonic() + budget['chain_timeout_seconds']
    cont = {'status': 'gating', 'batch': f'{study.batch("S1")}-r{n}', 'units': len(units)}
    entry.setdefault('continuations', []).append(cont)
    status.update(state='running', stopped_stage=None, reason=None); write_status(status)

    def stop(reason, code):
        status.update(state='stopped_at_gate', stopped_stage='S1', reason=reason, ledger=ledger_totals()); write_status(status)
        print(json.dumps({'state': 'stopped_at_gate', 'stage': 'S1', 'reason': reason})); return code
    try:
        ids = coordinator.enqueue_continuation(sr, n); run = sr.next_run(study.EXPERIMENT)
    except coordinator.GateRefused as exc:
        cont['status'] = 'refused'; return stop(str(exc), EXIT_STOPPED)
    except Exception as exc:
        cont['status'] = 'failed'; return stop('internal_' + type(exc).__name__, EXIT_INTERNAL)
    if run is None or run.id != ids[0] or run.attempt != 1:
        cont.update(status='failed', run=ids[0]); return stop('queued_run_not_received', EXIT_INTERNAL)
    outcome, code, reason = execute_run(run, cont, status, deadline, opener, units=units, prior_rows=prior)
    if outcome != 'done': return stop(reason, code)
    entry.update(status='done', completed_by=cont['batch'])
    status.update(state='completed', all_stages_done=all(status['stages'].get(s, {}).get('status') == 'done' for s in study.STAGES),
                  ledger=ledger_totals())
    write_status(status)
    print(json.dumps({'state': 'completed', 'stages': ['S1'], 'continuation': cont['batch'], 'units': len(units)}))
    return EXIT_DONE


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
        extra = {}
        try:
            if time.monotonic() > deadline:
                entry['status'] = 'refused'
                return stop(stage, 'chain_deadline', EXIT_STOPPED)
            _, before = coordinator.check(sr, stage)
            if stage == 'Q0':
                extra['probe_rows'] = probe_rows(sr)
            if stage == 'S1':
                entry['projection'] = projection(sr, before)
                if not entry['projection'].get('within_cap'):
                    entry['status'] = 'refused'
                    return stop(stage, 'projection_exceeds_cap', EXIT_STOPPED)
                if not entry['projection'].get('input_ceiling_ok'):
                    entry['status'] = 'refused'
                    return stop(stage, 'input_ceiling_projection', EXIT_STOPPED)
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
        outcome, code, reason = execute_run(run, entry, status, deadline, opener, **extra)
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
    if isinstance(a, bool) or isinstance(b, bool): return a == b
    if isinstance(a, float) or isinstance(b, float):
        if a is None or b is None or isinstance(a, (str, list, dict)) or isinstance(b, (str, list, dict)): return a == b
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(close(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
    return a == b


def regrade(a, r):
    """True when the saved answer is valid for the assignment and scoring it again gives the saved evaluation."""
    if r['status'] != 'completed': return 'answer' not in r and 'evaluation' not in r
    try: answer = study.validate(r['answer'], a['legal_cells'])
    except (ValueError, KeyError, TypeError): return False
    return close(json.loads(json.dumps(study.evaluate(a, answer['inspect']))), r['evaluation'])


def verify_stage(sr, stage, entry, reference, prior_rows=None, original=True, probe=None):
    """Checks of one hub run. For a continuation, `prior_rows` are the rows of the earlier runs of the stage;
    the saved analysis then covers the earlier runs and this one together. `probe` is P0's rows, for Q0."""
    checks = {}; out = Path(entry['directory'])
    detail = sr.get_run(entry['run']); hub = {a['name']: a for a in detail.get('artifacts', [])}
    checks['hub_status_matches'] = detail.get('status') == ('failed' if entry.get('completed_by') else entry['status'])
    checks['hub_has_every_artifact'] = all(name in hub for name in worker.ARTIFACTS)
    checks['artifact_checksums'] = bool(hub) and all(
        (out / name).is_file() and hashlib.sha256((out / name).read_bytes()).hexdigest() == a['sha256'] for name, a in hub.items())
    assigned = read_jsonl(out / 'assignments.jsonl.gz'); rows = read_jsonl(out / ROWS); requests = read_jsonl(out / 'requests.jsonl.gz')
    by_id = {a['id']: a for a in assigned}; fresh = {a['id']: a for a in study.assignments(stage)}
    checks['every_unit_has_one_row'] = sorted(r['id'] for r in rows) == sorted(by_id)
    checks['inputs_regenerate'] = all(i in fresh and close(fresh[i], a) for i, a in by_id.items()) and all(
        r['input_hash'] == by_id[r['id']]['input_hash'] for r in rows if r['id'] in by_id) and all(
        q['id'] in fresh and study.digest([q['system'], q['user']]) == fresh[q['id']]['input_hash'] == q['input_hash'] for q in requests) \
        and len(requests) == len(assigned)
    listed = set(reference['stages'][stage]['ids'])
    checks['manifest_matches'] = manifest.stage_entry(assigned, stage == 'S0')['digest'] == reference['stages'][stage]['digest'] if original else \
        all(f'{a["id"]}:{a["input_hash"][:16]}' in listed for a in assigned)
    checks['answers_regraded'] = all(r['id'] in by_id and regrade(by_id[r['id']], r) for r in rows)
    summary = json.loads((out / 'summary.json').read_text()); saved = json.loads((out / 'analysis.json').read_text())
    everyone = study.combine(list(prior_rows or []) + rows)
    checks['analysis_recomputed'] = close(saved, json.loads(json.dumps(analyze.analyze(everyone))))
    t = worker.totals(rows, len(assigned))
    checks['totals_recomputed'] = all(close(float(summary[k]), float(v)) for k, v in t.items())
    gate = study.gate(stage, rows, summary.get('invariant_violations') or [], probe)
    checks['gate_recomputed'] = (None if gate is None else int(gate)) == summary['qualification_passed']
    budget = study.design()['budget']; failed = sum(r['status'] == 'failed' for r in everyone)
    stopped = any(r['status'] == 'not_started' for r in rows)
    want = (t['invalid'] == 0 and gate is True) if stage in worker.STRICT else (not stopped and failed <= budget['max_failed'])
    checks['passed_recomputed'] = summary['passed'] == (bool(want) and not summary.get('invariant_violations'))
    metrics = detail.get('metrics') or {}
    checks['hub_metrics_match'] = all(k in metrics and close(float(metrics[k]), float(t[k])) for k in
                                      ('episodes', 'invalid', 'failed', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd'))
    checks['source_hash_current'] = summary['params']['source_hash'] == study.source_hash()
    checks['call_cap_respected'] = t['answered_calls'] <= budget['max_calls'][stage] and \
        t['model_calls'] <= budget['max_calls'][stage] + worker.unanswered_reservations(prior_rows or [])
    return {'run': entry['run'], 'status': entry['status'], 'ok': all(checks.values()), 'checks': checks, 'units': len(assigned),
            'completed': sum(r['status'] == 'completed' for r in rows), 'failed': t['failed'], 'model_calls': t['model_calls'],
            'cost_usd': t['cost_usd']}, rows


def units(rows, reference):
    """S1 as a whole, from the rows of its original run and its continuations: one terminal row per unit, and
    the primary contrast with its complete-case denominator and its bounds over all assigned layouts."""
    final = study.combine(rows); count = lambda s: sum(r['status'] == s for r in final)
    a = analyze.analyze(final); p = a['primary']
    answered = sum(bool((r.get('accounting') or {}).get('usage_reported')) for r in rows)
    return {'assigned': len(final), 'completed': count('completed'), 'failed': count('failed'), 'not_started': count('not_started'),
            'every_unit_exactly_once': sorted(r['id'] for r in final) == sorted(x.split(':')[0] for x in reference['stages']['S1']['ids']),
            'answered_calls': answered, 'answered_calls_within_cap': answered <= study.design()['budget']['max_calls']['S1'],
            'no_unit_answered_twice': max([sum(bool((r.get('accounting') or {}).get('usage_reported')) for r in rows if r['id'] == i)
                                           for i in {r['id'] for r in rows}] or [0]) <= 1,
            'primary_estimate': p['estimate'], 'primary_layouts': p['layouts'], 'primary_assigned_layouts': p['assigned_layouts'],
            'primary_interval95': p['interval95'], 'primary_bounds_all_assigned': p['bounds_all_assigned'],
            'regret_prose': a['representations']['prose']['mean_regret'], 'regret_table': a['representations']['table']['mean_regret'],
            'reliable_source_flagged': len(a['reliable_source']['flagged']), 'failures_by_category': a['failures']['by_category']}


def verify(sr=None):
    if sr is None:
        import swarm_report as sr
    status = read_status()
    if not status:
        print(json.dumps({'ok': False, 'reason': 'no chain-status.json under ' + str(study.results_dir())})); return 1
    reference = manifest.load(); stages = {}; probe = None
    for stage in study.STAGES:
        entry = status['stages'].get(stage)
        if not entry or 'run' not in entry or 'directory' not in entry: continue
        try:
            stages[stage], rows = verify_stage(sr, stage, entry, reference, probe=probe if stage == 'Q0' else None)
            if stage == 'P0': probe = rows
            for n, cont in enumerate(entry.get('continuations') or [], 1):
                if 'run' not in cont or 'directory' not in cont: continue
                stages[f'{stage}-r{n}'], more = verify_stage(sr, stage, cont, reference, prior_rows=rows, original=False); rows = rows + more
            if stage == 'S1':       # the stage as a whole: every unit exactly once, with the bounds the analysis reports
                u = units(rows, reference); stages[stage]['units'] = u
                stages[stage]['ok'] = stages[stage]['ok'] and u['every_unit_exactly_once'] and u['answered_calls_within_cap'] and u['no_unit_answered_twice']
        except Exception as exc: stages[stage] = {'run': entry.get('run'), 'ok': False, 'error': type(exc).__name__ + ': ' + str(exc)[:200]}
    ok = bool(stages) and all(s['ok'] for s in stages.values())
    print(json.dumps({'ok': ok, 'state': status.get('state'), 'manifest_digest': reference['digest'], 'stages': stages}, sort_keys=True))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('run'); r.add_argument('--stages', default=','.join(study.STAGES))
    sub.add_parser('status'); sub.add_parser('verify'); sub.add_parser('resume')
    a = ap.parse_args(argv)
    if a.cmd == 'run': return run_chain(parse_stages(a.stages))
    if a.cmd == 'resume': return resume()
    if a.cmd == 'status': return show_status()
    return verify()


if __name__ == '__main__':
    sys.exit(main())
