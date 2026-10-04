"""One stage as one finite batch with a durable per-row log and no answer retries.

S0, P0 and Q0 are strict: the first failed call stops new dispatch and the gate needs every row
valid. In S1 a failed call is recorded with its evidence and dispatch continues until more than
budget.max_failed calls have failed; an integrity failure (a ledger refusal, a model or provider
mismatch, a breached reservation, a deadline, an internal error) stops dispatch at once. A billing
outage that outlasts its limit stops the stage with nothing recorded as failed: the affected and
unfinished calls are recorded as not started and S1 can be resumed (chain.py resume).
On every ending the hub run reports episodes, invalid, failed, model_calls, transport_attempts,
input_tokens, output_tokens and cost_usd.
"""
import argparse
import gzip
import json
import os
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

import analyze
import openai_provider
import provider
import render
import study

# Failure types and integrity categories of both reference adapters (each chain uses one of them).
FAILURES = (provider.CallFailure, openai_provider.CallFailure)
INTEGRITY = set(provider.INTEGRITY) | set(openai_provider.INTEGRITY)

ARTIFACTS = ('final_frame.png', 'initial_frame.png', 'progress.png', 'replay.gif', 'assignments.jsonl.gz',
             'episodes.jsonl.gz', 'audits.jsonl.gz', 'summary.json', 'analysis.json')
STRICT = ('S0', 'P0', 'Q0')
HUB_KEYS = ('episodes', 'invalid', 'failed', 'model_calls', 'transport_attempts', 'input_tokens', 'output_tokens',
            'cost_usd', 'billing_pauses', 'billing_pause_seconds', 'billing_affected_calls')


class StageFailed(RuntimeError):
    """The stage ran to a recorded end but did not pass."""


def write_json(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True); f.flush(); os.fsync(f.fileno())


def upload(run, path):
    receipt = run.artifact(path, path.name)
    if not receipt or receipt.get('spooled'): raise RuntimeError('artifact_not_durably_acknowledged')


def totals(rows, planned):
    acct = [r.get('accounting') or {} for r in rows]
    return {'episodes': planned, 'invalid': planned - sum(r['status'] == 'completed' for r in rows),
            'failed': sum(r['status'] == 'failed' for r in rows),
            # a call whose reservation was voided by a billing stop never reached the model
            'model_calls': sum(bool(a.get('attempted')) and not a.get('voided') for a in acct),
            'transport_attempts': sum(a.get('attempts', 0) for a in acct),
            'input_tokens': sum(a.get('input_tokens', 0) for a in acct),
            'output_tokens': sum(a.get('output_tokens', 0) for a in acct),
            'cost_usd': sum(a.get('actual_usd', 0) for a in acct)}


def tokens_per_byte(rows):
    ratios = [r['accounting']['input_tokens'] / r['request_bytes'] for r in rows
              if (r.get('accounting') or {}).get('input_tokens') and r.get('request_bytes')]
    return max(ratios) if ratios else None


def row_base(a, p, run_name):
    r = {key: a[key] for key in study.ROW_FIELDS}
    r.update(run=run_name, stage=p['stage'], batch=p['batch'], backend=p['backend'], code=p['code'], source_hash=p['source_hash'],
             model=p['model'], diagnostics=a['diagnostics'], answers=a['answers'], expected=a['expected'], status='failed')
    return r


def merge(prior_rows, rows):
    """One row per unit: a continuation's row replaces the earlier not-started row of the same unit."""
    latest = {r['id']: r for r in prior_rows or []}
    for r in rows:
        assert r['id'] not in latest or latest[r['id']]['status'] == 'not_started', 'unit_recorded_twice'
        latest[r['id']] = r
    return list(latest.values())


def run_stage(p, out, run, backend, deadline, state, opener=None, earlier_rows=(), units=None, prior_rows=None, clock=None, sleep=None):
    stage = p['stage']; budget = study.budget(); strict = stage in STRICT
    assert p['source_hash'] == study.source_hash(), 'runtime_source_mismatch'
    assert p['backend'] == ('scripted' if stage == 'S0' else study.spec()['api']) and p['model'] == study.model()
    assert (units is None) == ('continuation' not in p) and (units is None or stage == 'S1')
    out = Path(out); out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic(); run_name = run.id if run else out.name
    stop_at = start + budget['stage_timeout_seconds']
    if deadline is not None: stop_at = min(stop_at, deadline)
    def preparing(message):
        if run: run.progress(0, 1, episodes=0, message='Preparing recorded inputs: ' + message)
    assigned = study.assignments(stage, out, preparing)
    if units is not None: assigned = [a for a in assigned if a['id'] in set(units)]
    total = len(assigned); state['total'] = total
    with gzip.open(out / 'assignments.jsonl.gz', 'wt') as f:
        for a in assigned: f.write(json.dumps(a, sort_keys=True) + '\n')
    violations = study.check_invariants(stage)
    ledger = None
    if p['backend'] != 'scripted':
        path = os.environ.get(provider.LEDGER_ENV); assert path, 'persistent_budget_required'
        path = study.ledger_path(path); route = study.route()
        # A continuation runs under the unchanged caps: the ledger voided the reservations of the calls
        # a billing stop left unanswered, and a continuation batch shares its original batch's allowance.
        config = study.adapter_config()
        assert total <= config['budget']['max_calls'][stage], 'assignments_exceed_stage_call_cap'
        ledger = route.Ledger(path, config['budget'])
        backend = backend or study.make_backend(ledger, config, opener, clock, sleep)
    initial = ledger.transact() if ledger else {}
    rows = state['rows']; reporting_errors = []
    control = {'reason': 'invariant_violations' if violations and not strict else None, 'failed': 0}
    stopped = bool(violations) and p['backend'] != 'scripted'      # structurally broken inputs: no call is made
    render.frame(merge(prior_rows, []), len(prior_rows or []) or total, stage, accounting=initial).save(out / 'initial_frame.png')
    if run: upload(run, out / 'initial_frame.png')

    def solve(a):
        r = row_base(a, p, run_name)
        try:
            if time.monotonic() > stop_at: raise provider.CallFailure('stage_deadline', {'attempted': False})
            if p['backend'] == 'scripted':
                answer = study.scripted(a['packet']); accounting = {'attempted': False, 'actual_usd': 0, 'reserved_usd': 0}
            else:
                answer, accounting = backend.call(study.SYSTEM, study.user_text(a['packet']), p['batch'] + ':' + a['id'], study.validate)
            r.update(answer=answer, accounting=accounting, evaluation=study.evaluate(a, answer),
                     reference_evaluation=study.evaluate(a, study.scripted(a['packet'])), status='completed')
        except FAILURES as exc:
            r.update(error=exc.category, accounting=exc.accounting)
        except Exception as exc:
            r.update(error='internal_' + type(exc).__name__, accounting={})
        return r

    with (out / 'episodes.jsonl').open('x') as log:
        def record(r):
            r.update(completion_index=len(rows) + 1, elapsed_seconds=time.monotonic() - start,
                     study_accounting=ledger.transact() if ledger else {})
            log.write(json.dumps(r, sort_keys=True) + '\n'); log.flush(); os.fsync(log.fileno()); rows.append(r)
        index = 0; last_render = time.monotonic(); workers = 1 if p['backend'] == 'scripted' else budget['workers']
        with ThreadPoolExecutor(max_workers=workers) as pool:
            pending = {}
            def fill():
                nonlocal index
                while not stopped and index < total and len(pending) < workers:
                    a = assigned[index]; pending[pool.submit(solve, a)] = a; index += 1
            fill()
            while pending:
                done, _ = wait(pending, timeout=5, return_when=FIRST_COMPLETED)
                for f in done:
                    pending.pop(f); r = f.result()
                    if r['status'] != 'completed':
                        category = r['error']
                        if category in study.BILLING_STOPS:
                            # not a model outcome: the unit is not started and can be resumed
                            r['status'] = 'not_started'; stopped = True; control['reason'] = category
                        elif category in INTEGRITY or category == 'stage_deadline' or category.startswith('internal_'):
                            control['failed'] += 1; stopped = True; control['reason'] = control['reason'] or 'integrity_failure:' + category
                        else:
                            control['failed'] += 1
                            if strict: stopped = True
                            elif control['failed'] > budget['max_failed']:
                                stopped = True; control['reason'] = control['reason'] or 'failed_units_over_limit'
                    record(r)
                if run:
                    t = totals(rows, len(rows)); paused = getattr(backend, '_paused', False)
                    run.progress(len(rows), total, episodes=len(rows), invalid=t['invalid'], failed=t['failed'], model_calls=t['model_calls'],
                                 input_tokens=t['input_tokens'], output_tokens=t['output_tokens'], cost_usd=t['cost_usd'],
                                 **({'message': 'billing outage: dispatch paused, the same call is re-sent every '
                                                f'{budget["billing_outage"]["retry_every_seconds"]} s'} if paused else {}))
                    if done and (time.monotonic() - last_render > 20 or stopped):
                        try:
                            render.frame(merge(prior_rows, rows), len(prior_rows or []) or total, stage, time.monotonic() - start,
                                         rows[-1]['study_accounting'] or initial).save(out / 'progress.png')
                            upload(run, out / 'progress.png')
                        except Exception as exc: reporting_errors.append(type(exc).__name__)
                        last_render = time.monotonic()
                fill()
        for a in assigned[index:]:
            r = row_base(a, p, run_name); r.update(status='not_started', accounting={}); record(r)
    with gzip.open(out / 'episodes.jsonl.gz', 'wb') as f: f.write((out / 'episodes.jsonl').read_bytes())
    good = [r for r in rows if r['status'] == 'completed']; t = totals(rows, total)
    if stage == 'S0': violations = violations + study.degeneracy(rows)
    passed_gate = study.gate(stage, rows, violations, earlier_rows)
    whole = merge(prior_rows, rows)
    grid = [r for r in whole if r['kind'] == 'pilot']
    analysis = analyze.analyze(whole) if grid else {'cells': [], 'note': 'this stage has no comparison rows'}
    billing = dict(backend.billing) if hasattr(backend, 'billing') else {'billing_pauses': 0, 'billing_pause_seconds': 0.0, 'billing_affected_calls': 0}
    frames = None
    try:
        render.frame(whole, len(whole), stage, time.monotonic() - start, (rows[-1]['study_accounting'] if rows else None) or initial).save(out / 'progress.png')
        frames = render.replay(whole, out, stage, len(whole), initial)
    except Exception as exc: reporting_errors.append('render_' + type(exc).__name__)
    if strict:
        passed = t['invalid'] == 0 and passed_gate is True and not violations
        reason = None if passed else 'invariant_violations' if violations else 'invalid_rows' if t['invalid'] else 'gate_failed'
    else:
        passed = control['reason'] is None and not violations and control['failed'] <= budget['max_failed'] and not t['invalid'] - t['failed']
        reason = None if passed else control['reason'] or ('invariant_violations' if violations else 'unfinished_units')
    probe = study.probe_gate(rows) if stage == 'P0' else None
    summary = {'params': p, 'experiment': study.hub_experiment(), 'planned': total,
               'started': sum(r['status'] != 'not_started' or bool((r.get('accounting') or {}).get('attempted')) for r in rows),
               'terminal': len(rows), 'graded': len(good), 'analyzed': len(good),
               'not_started': sum(r['status'] == 'not_started' for r in rows),
               'errors': sorted({r['error'] for r in rows if r.get('error')}), **t, **billing,
               'max_failed': None if strict else budget['max_failed'], 'stop_reason': control['reason'],
               'resumable': int(stage == 'S1' and control['reason'] in study.BILLING_STOPS),
               'elapsed_seconds': time.monotonic() - start,
               'qualification': study.qualification(rows) if stage in ('S0', 'Q0') else None, 'model': p['model'],
               'probe': probe, 'max_tokens_per_byte': tokens_per_byte(rows),
               'fixture_exact': int(bool(good and good[0]['evaluation']['exact_packet'])) if stage == 'P0' else None,
               'invariant_violations': violations,
               'qualification_passed': None if passed_gate is None else int(passed_gate), 'passed': passed, 'reason': reason,
               'max_request_bytes': max((a['request_bytes'] for a in assigned), default=0),
               'primary_contrast_pp': analysis.get('primary', {}).get('estimate_pp') if grid else None,
               'rare_accuracy': analyze.mean(r['evaluation']['rare_accuracy'] for r in whole if r['kind'] == 'pilot' and r['status'] == 'completed'),
               'normalized_answers': sum(bool((r.get('answer') or {}).get('normalized')) for r in rows),
               'continuation': None if units is None else {'units': total, 'earlier_rows': len(prior_rows or [])},
               'voided_calls': sum(bool((r.get('accounting') or {}).get('voided')) for r in rows),
               'study_accounting': ledger.transact() if ledger else {}, 'initial_study_accounting': initial,
               'reporting_errors': reporting_errors, 'visualization': {'mapping': 'v1', 'frames': frames}}
    write_json(out / 'summary.json', summary); write_json(out / 'analysis.json', analysis)
    if run:
        for name in ARTIFACTS:
            if (out / name).exists(): upload(run, out / name)
    return summary


def hub_metrics(summary):
    m = {k: summary[k] for k in HUB_KEYS}
    for k in ('input_tokens', 'output_tokens', 'reasoning_tokens', 'latency_seconds', 'provider_reported_usd', 'tokens_per_byte'):
        if isinstance((summary.get('probe') or {}).get(k), (int, float)): m['probe_' + k] = summary['probe'][k]
    for k in ('qualification_passed', 'primary_contrast_pp', 'rare_accuracy', 'max_tokens_per_byte', 'fixture_exact', 'resumable', 'normalized_answers'):
        if summary.get(k) is not None: m[k] = summary[k]
    return m


def execute(p, out, run=None, backend=None, deadline=None, opener=None, earlier_rows=(), units=None, prior_rows=None, clock=None, sleep=None):
    """Run one stage. Returns the summary when the stage passed; raises StageFailed when it ended
    recorded but not passed; re-raises anything unexpected. The hub run is closed in every case."""
    state = {'rows': [], 'total': 0}
    try:
        summary = run_stage(p, out, run, backend, deadline, state, opener, earlier_rows, units, prior_rows, clock, sleep)
    except Exception as exc:
        if run:
            t = totals(state['rows'], max(state['total'], len(state['rows'])))
            t['invalid'] = max(1, t['invalid'])
            run.fail(f'{p.get("stage")}: internal_{type(exc).__name__}; rows preserved', **t)
        raise
    stage = summary['params']['stage']
    message = (f'{stage}: {summary["graded"]}/{summary["planned"]} valid, {summary["failed"]} failed'
               + (f' (limit {summary["max_failed"]})' if summary['max_failed'] is not None else '')
               + f', {summary["model_calls"]} calls, ${summary["cost_usd"]:.4f}'
               + (f', {summary["billing_pauses"]} billing pause(s) of {summary["billing_pause_seconds"]:.0f} s' if summary['billing_pauses'] else ''))
    probe = summary.get('probe')
    if probe:       # the probe's raw response metadata, in words because hub metrics are numbers
        message += (f'; probe response model={probe["response_model"]} provider={probe["response_provider"]} id={probe["response_id"]} '
                    f'finish={probe["finish_reason"]} reasoning_tokens={probe["reasoning_tokens"]} input_tokens={probe["input_tokens"]} '
                    f'output_tokens={probe["output_tokens"]} provider_reported_usd={probe["provider_reported_usd"]} '
                    f'request_bytes={probe["request_bytes"]} error={probe["error"]} http_status={probe["http_status"]}')
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
                                               'invariant_violations', 'primary_contrast_pp', 'elapsed_seconds')}))


if __name__ == '__main__':
    main()
