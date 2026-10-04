"""One stage as one finite batch of multi-turn episodes.

An episode is a sequence of calls; each call's input depends on the answers before it. Episodes
run in parallel, calls inside an episode one at a time. Every call is logged durably when it
ends. No answer is retried. A failed call ends its episode as failed, with its evidence.

S0, P0 and Q0 are strict: the first failed call stops the stage. In S1 dispatch continues until
more than budget.max_failed episodes have failed; an integrity failure (a ledger refusal, a
breached reservation, a wrong model id, a deadline, an internal error) stops it at once. When
a stage stops, no new call starts anywhere, calls in flight finish, episodes cut short are
recorded as interrupted and episodes never started as not started. A billing outage that
outlasts its limit stops the stage with nothing recorded as failed; S1 can then be resumed.
On success and on failure the hub run ends with episodes, invalid, model_calls, input_tokens,
output_tokens and cost_usd."""
import argparse
import gzip
import json
import os
import sys
import threading
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

import analyze
import provider
import render
import sim
import study

ARTIFACTS = ('final_frame.png', 'initial_frame.png', 'progress.png', 'replay.gif', 'assignments.jsonl.gz',
             'episodes.jsonl.gz', 'turns.jsonl.gz', 'summary.json', 'analysis.json')
HUB_KEYS = ('episodes', 'invalid', 'failed', 'model_calls', 'transport_attempts', 'input_tokens', 'output_tokens', 'cost_usd',
            'max_output_tokens_per_call', 'count_fallbacks', 'billing_pauses', 'billing_pause_seconds', 'billing_affected_calls')
STRICT = ('S0', 'P0', 'Q0')


class StageFailed(RuntimeError):
    """The stage ran to a recorded end but did not pass (invalid episodes, a stop or a failed gate)."""


def write_json(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True); f.flush(); os.fsync(f.fileno())


def upload(run, path):
    receipt = run.artifact(path, path.name)
    if not receipt or receipt.get('spooled'): raise RuntimeError('artifact_not_durably_acknowledged')


def accountings(row):
    out = [t.get('accounting') or {} for t in row.get('turns', [])]
    for key in ('failed_turn', 'billing_turn'):
        if row.get(key): out.append(row[key].get('accounting') or {})
    return out


def totals(rows, planned):
    """Stage totals. `episodes` counts episodes planned; `model_calls` counts calls dispatched."""
    acct = [a for r in rows for a in accountings(r)]
    return {'episodes': planned, 'invalid': planned - sum(r['status'] == 'completed' for r in rows),
            'failed': sum(r['status'] == 'failed' for r in rows),
            'model_calls': sum(bool(a.get('attempted')) for a in acct),
            'transport_attempts': sum(a.get('attempts', 0) for a in acct),
            'input_tokens': sum(a.get('input_tokens', 0) for a in acct),
            'output_tokens': sum(a.get('output_tokens', 0) for a in acct),
            'cost_usd': sum(a.get('actual_usd', 0) for a in acct),
            'max_output_tokens_per_call': max([a.get('output_tokens', 0) for a in acct] or [0]),
            'count_fallbacks': sum(bool(a.get('count_fallback')) for a in acct)}


def row_base(a, p, run_name):
    r = {key: a[key] for key in study.ROW_FIELDS}
    r.update(run=run_name, stage=p['stage'], batch=p['batch'], backend=p['backend'], code=p['code'], source_hash=p['source_hash'],
             status='failed', turns=[])
    return r


def run_stage(p, out, run, backend, deadline, state, opener=None, units=None, prior_rows=None):
    """`units` (episode ids) and `prior_rows` are given only for a continuation of S1 after a
    billing stop: the run then holds exactly those episodes and reports the earlier runs' rows
    and its own together."""
    stage = p['stage']; budget = study.design()['budget']; strict = stage in STRICT
    assert p['source_hash'] == study.source_hash(), 'runtime_source_mismatch'
    assert p['backend'] == ('scripted' if stage == 'S0' else 'anthropic')
    assert (units is None) == (p['batch'] == study.batch(stage)), 'batch_mismatch'
    out = Path(out); out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic(); run_name = run.id if run else out.name
    stop_at = start + budget['stage_timeout_seconds']
    if deadline is not None: stop_at = min(stop_at, deadline)
    if run: run.progress(0, 1, episodes=0, message='Preparing episodes and checking invariants')
    everything = study.assignments(stage); full = len(everything)
    assigned = everything if units is None else [a for a in everything if a['id'] in set(units)]
    assert units is None or len(assigned) == len(set(units)), 'unknown_units'
    total = len(assigned); state['total'] = total
    prior = study.combine(prior_rows or [])
    with gzip.open(out / 'assignments.jsonl.gz', 'wt') as f:
        for a in assigned: f.write(json.dumps(a, sort_keys=True) + '\n')
    violations = study.check_invariants(stage)
    ledger = None
    if p['backend'] == 'anthropic':
        path = os.environ.get('STUDY_BUDGET_LEDGER'); assert path, 'persistent_budget_required'
        assert sum(a['max_turns'] for a in assigned) <= budget['max_calls'][stage], 'possible_calls_exceed_stage_call_cap'
        ledger = provider.Ledger(path); backend = backend or provider.Anthropic(ledger, opener=opener)
    gate = getattr(backend, 'gate', None)
    initial = ledger.transact() if ledger else {}
    rows = state['rows']; reporting_errors = []
    stop = threading.Event()            # no new call starts after it is set
    control = {'reason': None, 'failed': sum(r['status'] == 'failed' for r in prior)}; control_lock = threading.Lock()
    def halt(reason):
        with control_lock:
            if control['reason'] is None: control['reason'] = reason
        stop.set()
    if violations and p['backend'] != 'scripted': halt('invariant_violations')       # structurally broken inputs: no call is made
    shown = lambda own: study.combine(prior + own) if prior else own
    render.frame(shown([]), full, stage, accounting=initial).save(out / 'initial_frame.png')
    if run: upload(run, out / 'initial_frame.png')
    turn_lock = threading.Lock()

    with (out / 'turns.jsonl').open('x') as turn_log, (out / 'episodes.jsonl').open('x') as log:
        def log_turn(a, record):
            with turn_lock:
                turn_log.write(json.dumps(dict(record, episode=a['id']), sort_keys=True) + '\n')
                turn_log.flush(); os.fsync(turn_log.fileno())

        def solve(a):
            """One whole episode: its calls in order, each input built from the answers before it."""
            r = row_base(a, p, run_name); ep = sim.Episode(a['world'], a['rules']); turns = r['turns']; current = None
            def unfinished(): r['status'] = 'interrupted' if turns else 'not_started'
            try:
                while ep.lead_turn_due() and len(turns) < a['max_turns']:
                    if stop.is_set(): unfinished(); break
                    obs = ep.observation(); current = {'round': obs['round'], 'input_hash': study.input_hash(a['condition'], obs)}
                    if time.monotonic() > stop_at: raise provider.CallFailure('stage_deadline', {'attempted': False})
                    if p['backend'] == 'scripted':
                        answer = study.validate(sim.plan(obs, a['rules'], a['planner']))
                        accounting = {'attempted': False, 'actual_usd': 0, 'reserved_usd': 0}
                    else:
                        answer, accounting = backend.call(a['condition'], obs, f'{p["batch"]}:{a["id"]}:r{obs["round"]}')
                    turn = dict(ep.step(answer['actions']), input_hash=current['input_hash'], answer=study.stored(answer), accounting=accounting)
                    turns.append(turn); log_turn(a, dict(turn, status='completed')); current = None
                else:
                    r.update(status='completed', outcome=study.finish(ep), reference=study.reference(a),
                             spawn_notes=study.spawn_notes(turns))
            except provider.CallFailure as exc:
                if exc.category == provider.CREDIT:
                    # a billing outage that outlasted its limit: not an outcome, nothing is failed
                    halt(provider.CREDIT); unfinished(); r['billing_turn'] = dict(current or {}, accounting=exc.accounting)
                    log_turn(a, dict(r['billing_turn'], status='not_started', error=exc.category))
                else:
                    r.update(error=exc.category, failed_turn=dict(current or {}, accounting=exc.accounting))
                    log_turn(a, dict(r['failed_turn'], status='failed', error=exc.category))
                    with control_lock: control['failed'] += 1; failed = control['failed']
                    if exc.category in provider.INTEGRITY: halt('integrity_failure')
                    elif strict: halt('invalid_rows')
                    elif failed > budget['max_failed']: halt('failed_units_over_limit')
            except Exception as exc:
                r.update(error='internal_' + type(exc).__name__, failed_turn=dict(current or {}, accounting={})); halt('integrity_failure')
            r['turns_not_started_max'] = 0 if r['status'] == 'completed' else \
                a['max_turns'] - len(turns) - bool(r.get('failed_turn')) - bool(r.get('billing_turn'))
            return r

        def record(r):
            r.update(completion_index=len(rows) + 1, elapsed_seconds=time.monotonic() - start,
                     study_accounting=ledger.transact() if ledger else {})
            log.write(json.dumps(r, sort_keys=True) + '\n'); log.flush(); os.fsync(log.fileno()); rows.append(r)

        index = 0; last_render = time.monotonic(); workers = 1 if p['backend'] == 'scripted' else budget['workers']
        with ThreadPoolExecutor(max_workers=workers) as pool:
            pending = {}
            def fill():
                nonlocal index
                while not stop.is_set() and index < total and len(pending) < workers:
                    a = assigned[index]; pending[pool.submit(solve, a)] = a; index += 1
            fill()
            while pending:
                done, _ = wait(pending, timeout=5, return_when=FIRST_COMPLETED)
                for f in done:
                    pending.pop(f); record(f.result())
                if run:
                    t = totals(rows, len(rows)); paused = bool(gate and gate.paused())
                    run.progress(len(rows), total, episodes=len(rows), invalid=t['invalid'], failed=t['failed'], model_calls=t['model_calls'],
                                 input_tokens=t['input_tokens'], output_tokens=t['output_tokens'], cost_usd=t['cost_usd'],
                                 **(gate.stats() if gate else {}),
                                 **({'message': 'Paused: the provider reports a credit balance error; the same call is re-sent every '
                                                f'{budget["billing_outage"]["retry_every_seconds"]} s'} if paused else {}))
                    if done and (time.monotonic() - last_render > 20 or stop.is_set()):
                        try:
                            render.frame(shown(rows), full, stage, time.monotonic() - start, rows[-1]['study_accounting'] or initial).save(out / 'progress.png')
                            upload(run, out / 'progress.png')
                        except Exception as exc: reporting_errors.append(type(exc).__name__)
                        last_render = time.monotonic()
                fill()
        for a in assigned[index:]:
            r = row_base(a, p, run_name); r.update(status='not_started', turns_not_started_max=a['max_turns']); record(r)
    for name in ('episodes.jsonl', 'turns.jsonl'):
        with gzip.open(out / (name + '.gz'), 'wb') as f: f.write((out / name).read_bytes())

    good = [r for r in rows if r['status'] == 'completed']; t = totals(rows, total); everyone = shown(rows)
    violations = violations + sorted(f'{r["id"]}:{v}' for r in good for v in r['outcome']['violations'])
    discrimination = study.discrimination(rows) if stage == 'S0' else None
    if discrimination: violations = violations + discrimination
    passed_gate = study.gate(stage, rows, violations)
    compared = [r for r in everyone if r['kind'] in analyze.KINDS]
    analysis = analyze.analyze(everyone, analyze.actor(stage)) if compared else {'cells': [], 'note': 'this stage has no comparison episodes'}
    frames = None
    try:
        final = render.frame(everyone, full, stage, time.monotonic() - start, (rows[-1]['study_accounting'] if rows else None) or initial)
        final.save(out / 'progress.png'); final.save(out / 'final_frame.png')
        frames = render.replay(everyone, everything, out, stage)
    except Exception as exc: reporting_errors.append('render_' + type(exc).__name__)
    count = lambda rr, s: sum(r['status'] == s for r in rr)
    statuses = {s: count(rows, s) for s in ('completed', 'failed', 'interrupted', 'not_started')}
    if strict:
        passed = t['invalid'] == 0 and passed_gate is not False and not violations
        reason = None if passed else 'invariant_violations' if violations else control['reason'] if control['reason'] == provider.CREDIT \
            else 'invalid_rows' if t['invalid'] else 'gate_failed'
    else:       # S1: failed episodes within the limit do not fail the stage; a stop does
        passed = control['reason'] is None and not violations and control['failed'] <= budget['max_failed']
        reason = None if passed else 'invariant_violations' if violations else control['reason'] or 'failed_units_over_limit'
    primary = analysis.get('primary') or {}
    summary = {'params': p, 'experiment': study.EXPERIMENT, 'planned': total,
               'started': sum(bool(r['turns'] or r.get('failed_turn') or r.get('billing_turn')) for r in rows), 'terminal': len(rows),
               'graded': len(good), 'analyzed': len(good), 'not_started': statuses['not_started'], 'interrupted': statuses['interrupted'],
               'turns_completed': sum(len(r['turns']) for r in rows),
               'turns_not_started_max': sum(r['turns_not_started_max'] for r in rows),
               'errors': sorted({r['error'] for r in rows if r.get('error')}), **t,
               'max_failed': None if strict else budget['max_failed'], 'failed_in_stage': control['failed'], 'stop_reason': control['reason'],
               'resumable': bool(not strict and control['reason'] == provider.CREDIT and not violations),
               **(gate.stats() if gate else {'billing_pauses': 0, 'billing_pause_seconds': 0, 'billing_affected_calls': 0}),
               'elapsed_seconds': time.monotonic() - start,
               'qualification': study.qualification(rows) if stage in ('S0', 'Q0') else None,
               'probe': study.probe_gate(rows) if stage in ('S0', 'P0') else None,
               'discrimination': discrimination, 'invariant_violations': violations,
               'qualification_passed': None if passed_gate is None else int(passed_gate), 'passed': passed, 'reason': reason,
               'request_bytes_mean': analyze.mean(a.get('request_bytes') for r in rows for a in accountings(r) if a.get('request_bytes')),
               'excess_identities': primary.get('estimate') if compared else None,
               'units_beyond_share': analysis.get('headline', {}).get('units_beyond_share') if compared else None,
               'job_completion': analysis.get('headline', {}).get('job_completion') if compared else None,
               'stage_episodes': {'assigned': full, **{s: count(everyone, s) for s in ('completed', 'failed', 'interrupted', 'not_started')}},
               'continuation': None if units is None else {'units': total, 'earlier_rows': len(prior_rows or [])},
               'study_accounting': ledger.transact() if ledger else {}, 'initial_study_accounting': initial,
               'reporting_errors': reporting_errors, 'visualization': {'mapping': 'v1', 'replay_frames': frames}}
    write_json(out / 'summary.json', summary); write_json(out / 'analysis.json', analysis)
    if run:
        for name in ARTIFACTS:
            if (out / name).exists(): upload(run, out / name)
    return summary


def hub_metrics(summary):
    m = {k: summary[k] for k in HUB_KEYS}
    for k in ('qualification_passed', 'excess_identities', 'units_beyond_share', 'job_completion'):
        if summary.get(k) is not None: m[k] = summary[k]
    return m


def execute(p, out, run=None, backend=None, deadline=None, opener=None, units=None, prior_rows=None):
    """Run one stage. Returns the summary when the stage passed; raises StageFailed when it ended
    recorded but not passed; re-raises anything unexpected. The hub run is closed in every case."""
    state = {'rows': [], 'total': 0}
    try:
        summary = run_stage(p, out, run, backend, deadline, state, opener, units, prior_rows)
    except Exception as exc:
        if run:
            t = totals(state['rows'], max(state['total'], len(state['rows'])))
            t['invalid'] = max(1, t['invalid'])
            run.fail(f'{p.get("stage")}: internal_{type(exc).__name__}; rows preserved', **t)
        raise
    stage = summary['params']['stage']
    message = (f'{stage}: {summary["graded"]}/{summary["planned"]} episodes valid, {summary["failed"]} failed'
               + (f' (limit {summary["max_failed"]})' if summary['max_failed'] is not None else '')
               + f', {summary["model_calls"]} calls, ${summary["cost_usd"]:.4f}'
               + (f', {summary["billing_pauses"]} billing pause(s) of {summary["billing_pause_seconds"]} s' if summary['billing_pauses'] else ''))
    if not summary['passed']:
        if run: run.fail(message + f'; {summary["reason"]}; rows preserved', **hub_metrics(summary))
        raise StageFailed(summary['reason'])
    if run: run.done(message=message, **hub_metrics(summary))
    return summary


def main():
    ap = argparse.ArgumentParser(description='Offline scripted stage only. Paid stages run through chain.py and its gates.')
    ap.add_argument('--stage', choices=['S0'], required=True); ap.add_argument('--attempt', required=True)
    a = ap.parse_args()
    if not a.attempt.replace('-', '').isalnum(): raise SystemExit('Offline S0 requires a fresh alphanumeric attempt name')
    try:
        summary = execute(study.params('S0'), study.results_dir() / a.attempt)
    except StageFailed as exc:
        print(json.dumps({'passed': False, 'reason': str(exc), 'directory': str(study.results_dir() / a.attempt)})); sys.exit(3)
    print(json.dumps({k: summary[k] for k in ('planned', 'graded', 'invalid', 'model_calls', 'cost_usd', 'qualification_passed', 'passed',
                                                'invariant_violations', 'elapsed_seconds')}))


if __name__ == '__main__':
    main()
