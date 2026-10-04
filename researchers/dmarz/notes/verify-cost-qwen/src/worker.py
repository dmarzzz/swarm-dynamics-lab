"""One stage as one finite batch of single stateless calls.

Every unit is logged durably when it ends, as completed, failed or not_started. No answer is retried.

S0, P0 and Q0 are strict: the first failed call stops new dispatch and the stage fails. In S1 a call
without a valid answer is recorded as failed with its evidence and dispatch continues until more than
budget.max_failed units have failed; an integrity failure (a ledger refusal, a breached reservation, a
model or provider mismatch, a deadline, an internal error) stops dispatch at once. When dispatch
stops, calls in flight finish and every unit not started is recorded as not started. A billing outage
that outlasts its limit stops the stage with nothing recorded as failed; S1 can then be resumed.
On success and on failure the hub run ends with episodes, invalid, model_calls, input_tokens,
output_tokens and cost_usd.

This is the role PC5's engine.py played (reserve before any wire effect, one durable terminal record
per assignment, grade from the saved records), rebuilt on the reference adapter and ledger.
"""
import argparse
import copy
import gzip
import json
import math
import os
import sys
import threading
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

import analyze
import provider
import render
import study

ARTIFACTS = ('final_frame.png', 'initial_frame.png', 'replay.gif', 'assignments.jsonl.gz', 'episodes.jsonl.gz',
             'requests.jsonl.gz', 'summary.json', 'analysis.json', 'failures.json')
HUB_KEYS = ('episodes', 'invalid', 'failed', 'model_calls', 'transport_attempts', 'input_tokens', 'output_tokens', 'cost_usd',
            'billing_pauses', 'billing_pause_seconds', 'billing_affected_calls')
STRICT = ('S0', 'P0', 'Q0')
# Failures that stop a stage at once, whatever the number of failed units.
STOP_NOW = tuple(provider.INTEGRITY) + ('stage_deadline', 'input_size_limit')
CLOCK, SLEEP = time.monotonic, time.sleep       # the adapter's clock and sleep; the rehearsal replaces both so no wait is real
NO_BILLING = {'billing_pauses': 0, 'billing_pause_seconds': 0.0, 'billing_affected_calls': 0}


class StageFailed(RuntimeError):
    """The stage ran to a recorded end but did not pass (invalid rows, a stop or a failed gate)."""


def write_json(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True); f.flush(); os.fsync(f.fileno())


def upload(run, path):
    receipt = run.artifact(path, path.name)
    if not receipt or receipt.get('spooled'): raise RuntimeError('artifact_not_durably_acknowledged')


def totals(rows, planned):
    """Stage totals. `episodes` counts units planned; `model_calls` counts calls reserved in the ledger."""
    acct = [r.get('accounting') or {} for r in rows]
    return {'episodes': planned, 'invalid': planned - sum(r['status'] == 'completed' for r in rows),
            'failed': sum(r['status'] == 'failed' for r in rows),
            'model_calls': sum(bool(a.get('attempted')) for a in acct),
            'answered_calls': sum(bool(a.get('usage_reported')) for a in acct),
            'transport_attempts': sum(a.get('attempts', 0) for a in acct),
            'input_tokens': sum(a.get('input_tokens', 0) for a in acct),
            'output_tokens': sum(a.get('output_tokens', 0) for a in acct),
            'cost_usd': math.fsum(a.get('actual_usd', 0) for a in acct)}


def unanswered_reservations(rows):
    """Units left not started by a billing stop whose call already holds a ledger reservation (no model ran)."""
    return sum(r['status'] == 'not_started' and bool((r.get('accounting') or {}).get('attempted')) for r in rows)


def ledger_budget(budget, stage, reissued):
    """The frozen budget; for a continuation after a billing stop the stage cap and the study cap are raised by
    the number of unanswered reservations being re-sent, and by nothing else."""
    if not reissued: return budget
    assert budget['billing_outage']['resume_reissues_unanswered_reservations'] is True
    b = copy.deepcopy(budget)
    b['max_calls'][stage] += reissued; b['max_attempted_calls'] += reissued
    return b


def row_base(a, p, run_name):
    r = {key: a[key] for key in study.ROW_FIELDS}
    r.update(run=run_name, stage=p['stage'], batch=p['batch'], backend=p['backend'], code=p['code'], source_hash=p['source_hash'],
             status='not_started')
    return r


def run_stage(p, out, run, backend, deadline, state, opener=None, units=None, prior_rows=None, probe_rows=None):
    """`units` (ids) and `prior_rows` are given only for a continuation of S1 after a billing stop: the run then
    holds exactly those units and reports the earlier runs' rows and its own together. `probe_rows` is P0's
    saved row, given to Q0, whose gate is evaluated over all 24 qualification rows."""
    stage = p['stage']; d = study.design(); budget = d['budget']; strict = stage in STRICT
    assert p['source_hash'] == study.source_hash(), 'runtime_source_mismatch'
    assert stage in study.STAGES and p['backend'] == d['stages'][stage]['backend'], 'stage_backend_mismatch'
    assert (units is None) == (p['batch'] == study.batch(stage)), 'batch_mismatch'
    assert units is None or stage == 'S1', 'only_the_main_stage_continues'
    scripted = p['backend'] == 'scripted'
    out = Path(out); out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic(); run_name = run.id if run else out.name
    stop_at = start + budget['stage_timeout_seconds']
    if deadline is not None: stop_at = min(stop_at, deadline)
    if run: run.progress(0, 1, episodes=0, message='Preparing requests and checking invariants')
    everything = study.assignments(stage); full = len(everything)
    assigned = everything if units is None else [a for a in everything if a['id'] in set(units)]
    assert units is None or len(assigned) == len(set(units)) == len(units), 'unknown_units'
    total = len(assigned); state['total'] = total
    prior = study.combine(prior_rows or [])
    with gzip.open(out / 'assignments.jsonl.gz', 'wt') as f:
        for a in assigned: f.write(json.dumps(a, sort_keys=True) + '\n')
    with gzip.open(out / 'requests.jsonl.gz', 'wt') as f:
        for a in assigned: f.write(json.dumps({'id': a['id'], 'input_hash': a['input_hash'], 'system': study.SYSTEM, 'user': study.user_for(a)}, sort_keys=True) + '\n')
    violations = study.check_invariants(stage)
    ledger = None
    if not scripted:
        path = os.environ.get(provider.LEDGER_ENV); assert path, 'persistent_budget_required'
        reissued = unanswered_reservations(prior_rows or [])     # every earlier row left not started that holds a reservation
        assert total + (0 if units is None else sum(r['status'] != 'not_started' for r in prior)) <= budget['max_calls'][stage], 'units_exceed_stage_call_cap'
        ledger = provider.Ledger(path, ledger_budget(budget, stage, reissued))
        backend = backend or provider.OpenRouter(ledger, study.provider_config(), opener, CLOCK, SLEEP)
    billing = lambda: dict(getattr(backend, 'billing', None) or NO_BILLING)
    initial = ledger.transact() if ledger else {}
    rows = state['rows']; reporting_errors = []
    stop = threading.Event()            # no new call starts after it is set
    control = {'reason': None, 'failed': sum(r['status'] == 'failed' for r in prior)}; control_lock = threading.Lock()

    def halt(reason):
        with control_lock:
            if control['reason'] is None: control['reason'] = reason
        stop.set()
    if violations and not scripted: halt('invariant_violations')       # broken inputs: no call is made
    shown = lambda own: study.combine(prior + own) if prior else own
    render.frame(shown([]), full, stage, accounting=initial).save(out / 'initial_frame.png')
    if run: upload(run, out / 'initial_frame.png')

    def solve(a):
        r = row_base(a, p, run_name)
        if stop.is_set():
            r['stop'] = control['reason']; return r
        try:
            if time.monotonic() > stop_at: raise provider.CallFailure('stage_deadline', {'attempted': False})
            if scripted:
                answer = study.validate({'inspect': study.policy('optimal', a)}, a['legal_cells'])
                accounting = {'attempted': False, 'usage_reported': False, 'attempts': 0, 'actual_usd': 0, 'reserved_usd': 0}
            else:
                answer, accounting = backend.call(study.SYSTEM, study.user_for(a), f'{p["batch"]}:{a["id"]}',
                                                  lambda obj: study.validate(obj, a['legal_cells']))
            r.update(status='completed', answer=answer, accounting=accounting, evaluation=study.evaluate(a, answer['inspect']))
        except provider.CallFailure as exc:
            if exc.category == provider.BILLING_STOP:
                # a billing outage that outlasted its limit: not an outcome, nothing is failed
                halt(provider.BILLING_STOP); r.update(stop=provider.BILLING_STOP, accounting=exc.accounting)
            else:
                r.update(status='failed', failure=exc.category, accounting=exc.accounting)
                with control_lock: control['failed'] += 1; failed = control['failed']
                if exc.category in STOP_NOW: halt('integrity_failure')
                elif strict: halt('invalid_rows')
                elif failed > budget['max_failed']: halt('failed_units_over_limit')
        except Exception as exc:
            r.update(status='failed', failure='internal_' + type(exc).__name__, accounting={})
            with control_lock: control['failed'] += 1
            halt('integrity_failure')
        return r

    with (out / 'episodes.jsonl').open('x') as log:
        def record(r):
            r.update(completion_index=len(rows) + 1, elapsed_seconds=time.monotonic() - start,
                     study_accounting=ledger.transact() if ledger else {})
            log.write(json.dumps(r, sort_keys=True) + '\n'); log.flush(); os.fsync(log.fileno()); rows.append(r)

        index = 0; last_render = time.monotonic(); workers = 1 if scripted else budget['workers']
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
                    t = totals(rows, len(rows)); b = billing(); paused = bool(getattr(backend, '_paused', False))
                    run.progress(len(rows), total, episodes=len(rows), invalid=t['invalid'], failed=t['failed'], model_calls=t['model_calls'],
                                 input_tokens=t['input_tokens'], output_tokens=t['output_tokens'], cost_usd=t['cost_usd'], **b,
                                 **({'message': 'Paused: the provider reports a credit or balance error; the same call is re-sent every '
                                                f'{budget["billing_outage"]["retry_every_seconds"]} s'} if paused else {}))
                    if done and (time.monotonic() - last_render > 20 or stop.is_set()):
                        try:
                            render.frame(shown(rows), full, stage, time.monotonic() - start, rows[-1]['study_accounting'] or initial).save(out / 'progress.png')
                            upload(run, out / 'progress.png')
                        except Exception as exc: reporting_errors.append(type(exc).__name__)
                        last_render = time.monotonic()
                fill()
        for a in assigned[index:]:
            r = row_base(a, p, run_name); r['stop'] = control['reason']; record(r)
    with gzip.open(out / 'episodes.jsonl.gz', 'wb') as f: f.write((out / 'episodes.jsonl').read_bytes())

    summary, analysis = summarize(p, rows, total, violations, control, prior, probe_rows, units is not None)
    everyone = shown(rows)
    summary.update(elapsed_seconds=time.monotonic() - start, **billing(), study_accounting=ledger.transact() if ledger else {},
                   initial_study_accounting=initial, continuation=None if units is None else {'units': total, 'earlier_rows': len(prior_rows or [])})
    frames = None
    try:
        final = render.frame(everyone, full, stage, summary['elapsed_seconds'], summary['study_accounting'] or initial)
        final.save(out / 'final_frame.png')
        frames = render.replay(everyone, full, out, stage)
    except Exception as exc: reporting_errors.append('render_' + type(exc).__name__)
    summary.update(reporting_errors=reporting_errors, visualization={'mapping': 'v1', 'replay_frames': frames})
    write_json(out / 'summary.json', summary); write_json(out / 'analysis.json', analysis)
    write_json(out / 'failures.json', failures(rows, probe_rows, summary))
    if run:
        for name in ARTIFACTS:
            if (out / name).exists(): upload(run, out / name)
    return summary


def summarize(p, rows, total, violations, control, prior, probe_rows, continuation):
    """The part of the summary that `chain.py verify` recomputes from the saved rows. Returns (summary, analysis)."""
    stage = p['stage']; budget = study.design()['budget']; strict = stage in STRICT
    t = totals(rows, total); everyone = study.combine(list(prior) + rows) if prior else rows
    violations = list(violations)
    calibration = analyze.calibration() if stage == 'S0' else None
    if stage == 'S0': violations += analyze.discrimination()
    passed_gate = study.gate(stage, rows, violations, probe_rows)
    analysis = analyze.analyze(everyone)
    count = lambda rr, s: sum(r['status'] == s for r in rr)
    if strict:
        passed = t['invalid'] == 0 and passed_gate is True and not violations
        reason = None if passed else 'invariant_violations' if violations else control['reason'] if control['reason'] in (provider.BILLING_STOP, 'integrity_failure') \
            else 'invalid_rows' if t['invalid'] else 'probe_row_unavailable' if stage == 'Q0' and study.qualification_rows(rows, probe_rows) is None \
            else 'gate_failed'
    else:       # S1: failed units within the limit do not fail the stage; a stop does
        passed = control['reason'] is None and not violations and control['failed'] <= budget['max_failed'] and count(rows, 'not_started') == 0
        reason = None if passed else 'invariant_violations' if violations else control['reason'] or 'failed_units_over_limit'
    both = study.qualification_rows(rows, probe_rows) if stage == 'Q0' else None
    primary = analysis.get('primary') or {}; reps = analysis.get('representations') or {}
    summary = {'params': p, 'experiment': study.EXPERIMENT, 'planned': total,
               'started': sum(bool((r.get('accounting') or {}).get('attempted')) or r['status'] != 'not_started' for r in rows),
               'terminal': len(rows), 'graded': count(rows, 'completed'), 'analyzed': count(rows, 'completed'),
               'not_started': count(rows, 'not_started'), 'errors': sorted({r['failure'] for r in rows if r.get('failure')}), **t,
               'max_failed': None if strict else budget['max_failed'], 'failed_in_stage': control['failed'], 'stop_reason': control['reason'],
               'resumable': bool(not strict and control['reason'] == provider.BILLING_STOP and not violations),
               'unanswered_reservations': unanswered_reservations(rows),
               'qualification': study.scripted_qualification(rows) if stage == 'S0' else study.qualification(both) if both else None,
               'probe': study.probe_gate(rows) if stage == 'P0' else None, 'calibration': calibration,
               'invariant_violations': violations,
               'qualification_passed': None if passed_gate is None else int(passed_gate), 'passed': passed, 'reason': reason,
               'largest_request_bytes': study.largest_request_bytes(stage),
               'content_bytes_mean': analyze.mean(r['content_bytes'] for r in rows),
               'regret_prose': (reps.get('prose') or {}).get('mean_regret'), 'regret_table': (reps.get('table') or {}).get('mean_regret'),
               'table_minus_prose_regret': primary.get('estimate'), 'table_minus_prose_bounds': primary.get('bounds_all_assigned'),
               'stage_units': {'assigned': len(study.assignments(stage)), **{s: count(everyone, s) for s in ('completed', 'failed', 'not_started')}}}
    return summary, analysis


def failures(rows, probe_rows, summary):
    """The failure report: every unit without a valid answer with its evidence, and, for qualification, the
    rendered request and the returned answer of every miss (read these before any repair)."""
    report = dict(analyze.failure_report(rows), stage=summary['params']['stage'], reason=summary['reason'], stop_reason=summary['stop_reason'])
    misses = []
    if summary['params']['stage'] in ('P0', 'Q0'):
        for r in (list(probe_rows or []) if summary['params']['stage'] == 'Q0' else []) + list(rows):
            if r['status'] == 'completed' and not r['evaluation']['optimal']:
                misses.append({'id': r['id'], 'answer': r['answer'], 'optimal_cell': r['evaluation']['optimal_cell'],
                               'optimal_action': r['evaluation']['optimal_action'], 'margin': r['evaluation']['margin'],
                               'system': study.SYSTEM, 'user': study.user_for(r)})
    report['qualification_misses'] = misses
    return report


def hub_metrics(summary):
    m = {k: summary[k] for k in HUB_KEYS}
    for k in ('qualification_passed', 'regret_prose', 'regret_table', 'table_minus_prose_regret'):
        if summary.get(k) is not None: m[k] = summary[k]
    if (summary.get('probe') or {}).get('tokens_per_byte') is not None: m['probe_tokens_per_byte'] = summary['probe']['tokens_per_byte']
    return m


def execute(p, out, run=None, backend=None, deadline=None, opener=None, units=None, prior_rows=None, probe_rows=None):
    """Run one stage. Returns the summary when the stage passed; raises StageFailed when it ended recorded but
    not passed; re-raises anything unexpected. The hub run is closed in every case, with its metrics."""
    state = {'rows': [], 'total': 0}
    try:
        summary = run_stage(p, out, run, backend, deadline, state, opener, units, prior_rows, probe_rows)
    except Exception as exc:
        if run:
            t = totals(state['rows'], max(state['total'], len(state['rows'])))
            t['invalid'] = max(1, t['invalid'])
            run.fail(f'{p.get("stage")}: internal_{type(exc).__name__}; rows preserved', **dict(NO_BILLING, **t))
        raise
    stage = summary['params']['stage']
    message = (f'{stage}: {summary["graded"]}/{summary["planned"]} units valid, {summary["failed"]} failed'
               + (f' (limit {summary["max_failed"]})' if summary['max_failed'] is not None else '')
               + (f', {summary["not_started"]} not started' if summary['not_started'] else '')
               + f', {summary["model_calls"]} calls, ${summary["cost_usd"]:.6f}'
               + (f', {summary["billing_pauses"]} billing pause(s) of {summary["billing_pause_seconds"]:.0f} s' if summary['billing_pauses'] else ''))
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
