"""One finite stage: durable per-row log, no answer retries.

Every assignment ends as completed, failed or not_started. S0, P0 and Q0 are strict: the first
failed call stops new dispatch and fails the stage. S1 tolerates failed calls (failure rule of
2026-10-04): a call without a valid answer is recorded as failed with its evidence and dispatch
continues; dispatch stops when failed calls exceed `budget.max_failed.S1`, at once on an integrity
failure, and on a billing outage that outlasts its limit (`provider_credit_balance_low`, whose
unfinished calls are recorded as not started and may be resumed by a continuation run).

Both endings of a hub run report episodes, invalid, model_calls, input_tokens, output_tokens and
cost_usd. A continuation run (`<batch>-r<k>`) executes exactly the units earlier parts left not
started; gates, summary and analysis are computed over the original run and its continuations
together, and no unit is counted twice.
"""
import argparse
import gzip
import json
import math
import os
import re
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

import analyze
import provider
import render
import study

ARTIFACTS = ('final_frame.png', 'replay.gif', 'initial_frame.png', 'assignments.jsonl.gz', 'episodes.jsonl.gz',
             'worlds.jsonl.gz', 'summary.json', 'analysis.json')
REQUIRED_METRICS = ('episodes', 'invalid', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd')


class StageFailed(RuntimeError):
    """The stage ended failed and was reported as failed. Carries the summary when one was written."""
    def __init__(self, reason, summary=None):
        super().__init__(reason)
        self.reason, self.summary = reason, summary


def write_json(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2); f.flush(); os.fsync(f.fileno())


def upload(run, path):
    receipt = run.artifact(path, path.name)
    if not receipt or receipt.get('spooled'):
        raise RuntimeError('artifact_not_durably_acknowledged')


def billing_stop_category():
    return study.design()['budget']['billing_outage']['stop_category']


def is_integrity(category):
    return category in provider.INTEGRITY_FAILURES or str(category).startswith('internal_')


def usage_metrics(rows, total):
    """Counts and usage over the given rows; `total` is the number of units they are measured against."""
    acc = [r.get('accounting') or {} for r in rows]
    completed = sum(r['status'] == 'completed' for r in rows)
    return {'episodes': total, 'invalid': total - completed,
            'model_calls': sum(bool(a.get('attempted')) for a in acc),
            'input_tokens': sum(a.get('input_tokens', 0) for a in acc),
            'output_tokens': sum(a.get('output_tokens', 0) for a in acc),
            'cost_usd': math.fsum(a.get('actual_usd', 0) for a in acc),
            'transport_attempts': sum(a.get('attempts', 0) for a in acc),
            'count_fallbacks': sum(bool(a.get('count_fallback')) for a in acc),
            'completed': completed, 'failed': sum(r['status'] == 'failed' for r in rows),
            'not_started': sum(r['status'] == 'not_started' for r in rows)}


def billing_metrics(rows):
    """Billing pauses seen in these rows: distinct pauses, their length and the calls they held up."""
    pauses = {}
    affected = 0
    for r in rows:
        a = r.get('accounting') or {}
        if a.get('billing_waits'):
            affected += 1
            key = (r.get('batch'), a.get('billing_pause'))
            pauses[key] = max(pauses.get(key, 0), a.get('billing_wait_seconds', 0))
    return {'billing_pauses': len(pauses), 'billing_pause_seconds': math.fsum(pauses.values()),
            'billing_affected_calls': affected}


def by_effort(rows):
    """Calls with reported usage, by effort: the basis of the projection gate and of the resource report."""
    out = {}
    for effort in study.design()['efforts']:
        acc = [r['accounting'] for r in rows if r.get('effort') == effort and (r.get('accounting') or {}).get('usage_reported')]
        latency = [a['latency_seconds'] for a in acc if a.get('latency_seconds') is not None]
        out[effort] = {'calls': len(acc), 'cost_usd': math.fsum(a['actual_usd'] for a in acc),
                       'input_tokens': sum(a['input_tokens'] for a in acc),
                       'output_tokens': sum(a['output_tokens'] for a in acc),
                       'max_output_tokens': max([a['output_tokens'] for a in acc], default=None),
                       'mean_latency_seconds': study.mean(latency), 'max_latency_seconds': max(latency, default=None)}
    return out


def combine(parts):
    """One row per unit over the original run and its continuations, in recorded order.

    A unit left not started by an earlier part is replaced by its row from a later part. A unit
    with a terminal row (completed or failed) in two parts is an error.
    """
    latest, order = {}, []
    for rows in parts:
        for r in rows:
            if r['id'] not in latest:
                order.append(r['id'])
                latest[r['id']] = r
            elif latest[r['id']]['status'] == 'not_started':
                latest[r['id']] = r
            elif r['status'] != 'not_started':
                raise ValueError('unit_recorded_twice')
    terminal = [latest[i] for i in order if latest[i]['status'] != 'not_started']
    return terminal + [latest[i] for i in order if latest[i]['status'] == 'not_started']


def part_of(p):
    """0 for the original run of a stage, k for its continuation `<batch>-r<k>`."""
    if p.get('model') != study.stage_model(p['stage']):
        # One model per attempt: the queued run must be for the model this process was started with.
        raise RuntimeError('model_mismatch_with_environment')
    base = study.base_batch(p['stage'])
    if p['batch'] == base and 'continues' not in p:
        return 0
    match = re.fullmatch(re.escape(base) + r'-r([1-9][0-9]*)', p['batch'])
    if not match or p.get('continues') != base or p['stage'] == 'S0':
        raise RuntimeError('batch_mismatch')
    return int(match.group(1))


def execute(p, out, run=None, backend=None, ledger_path=None, opener=None, deadline=None, prior_dirs=(),
            clock=None, sleep=None):
    """Run one stage, or one continuation of it, into the fresh directory `out`.

    Returns the summary or raises StageFailed. `deadline` is an absolute time.monotonic() value
    from the chain; no call is dispatched after it. `prior_dirs` are the results directories of
    the original run and earlier continuations, in order. `clock` and `sleep` are passed to the
    provider (tests inject them so that waits take no time).
    """
    rows = []
    try:
        return _execute(p, Path(out), run, backend, ledger_path, opener, deadline, [Path(d) for d in prior_dirs],
                        clock, sleep, rows)
    except StageFailed:
        raise
    except BaseException as exc:
        # A crash still reports usage: nothing recorded so far is lost from the hub's accounting.
        reason = 'internal_' + type(exc).__name__
        if run:
            total = max(len(rows), study.design()['stages'].get(p.get('stage'), {}).get('assignments', 0))
            metrics = dict(usage_metrics(rows, total), billing_stop=0)
            if p.get('stage') != 'S1':
                metrics['qualification_passed'] = 0
            run.fail(f'{p.get("stage")}: {reason}', **metrics)
        raise StageFailed(reason) from exc


def _execute(p, out, run, backend, ledger_path, opener, deadline, prior_dirs, clock, sleep, rows):
    d = study.design()
    budget = d['budget']
    stage = p['stage']
    if p['source_hash'] != study.source_hash():
        raise RuntimeError('runtime_source_mismatch')
    if stage not in study.STAGES or p['backend'] != ('scripted' if stage == 'S0' else 'anthropic'):
        raise RuntimeError('stage_backend_mismatch')
    part = part_of(p)
    if part != len(prior_dirs):
        raise RuntimeError('continuation_parts_mismatch')
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    stage_deadline = start + budget['stage_timeout_seconds']
    if deadline is not None:
        stage_deadline = min(stage_deadline, deadline)

    def preparing(kind, task):
        if run:
            run.progress(0, 1, episodes=0, message=f'Preparing recorded inputs: {kind} world {task}')

    assigned = study.assignments(stage, out, preparing)
    total = len(assigned)
    with gzip.open(out / 'assignments.jsonl.gz', 'wt') as f:
        for a in assigned:
            f.write(json.dumps(a, sort_keys=True) + '\n')

    prior_parts = [analyze.read_rows(d_ / 'episodes.jsonl.gz') for d_ in prior_dirs]
    prior = combine(prior_parts) if prior_parts else []
    if {r['id'] for r in prior} - {a['id'] for a in assigned}:
        raise RuntimeError('prior_rows_not_in_manifest')
    settled = {r['id'] for r in prior if r['status'] != 'not_started'}
    todo = [a for a in assigned if a['id'] not in settled]
    if part:
        # A continuation exists only after a billing stop, and only for units that stop left not started.
        previous = json.loads((prior_dirs[-1] / 'summary.json').read_text())
        if previous['failure'] != billing_stop_category() or previous['params']['source_hash'] != p['source_hash'] or not todo:
            raise RuntimeError('nothing_to_resume')

    ledger = None
    if p['backend'] == 'anthropic':
        path = ledger_path or os.environ.get(provider.LEDGER_ENV)
        if not path:
            raise RuntimeError('persistent_budget_ledger_required')
        ledger = provider.Ledger(path)
        if backend is None:
            extra = {k: v for k, v in (('clock', clock), ('sleep', sleep)) if v is not None}
            backend = provider.Anthropic(ledger, opener, **extra)
    billing = getattr(backend, 'billing', None)
    initial = ledger.transact() if ledger else {}
    reporting_errors = []
    render.frame(prior, total, stage, accounting=initial).save(out / 'initial_frame.png')
    if run:
        upload(run, out / 'initial_frame.png')

    invariants = None
    if stage == 'S0':
        if run:
            run.progress(0, total, episodes=0, message='Checking instrument invariants')
        invariants = study.check_invariants()

    strict = stage != 'S1'
    max_failed = budget['max_failed'].get(stage, 0)
    failed_before = sum(r['status'] == 'failed' for r in prior)
    stop_reason = None

    def base(a):
        r = {k: a[k] for k in study.ROW_KEYS}
        r.update(run=run.id if run else out.name, stage=stage, backend=p['backend'], batch=p['batch'], code=p['code'],
                 source_hash=p['source_hash'], model=p['model'])
        return r

    def solve(a):
        r = base(a)
        r['status'] = 'failed'
        try:
            if time.monotonic() > stage_deadline:
                raise provider.CallFailure('stage_deadline')
            if p['backend'] == 'scripted':
                answer = study.reference_answer(a['packet'], a['prompt'])
                accounting = {'attempted': False, 'actual_usd': 0, 'reserved_usd': 0}
            else:
                answer, accounting = backend.call(a['packet'], p['batch'] + ':' + a['id'], a['prompt'], a['effort'])
            r.update(answer=answer, accounting=accounting, evaluation=study.evaluate(a, answer), status='completed')
        except provider.CallFailure as exc:
            r.update(error=exc.category, accounting=exc.accounting)
        except Exception as exc:
            r.update(error='internal_' + type(exc).__name__)
        if r.get('error') == billing_stop_category():
            # A billing outage is not a model or packet failure: the unit is not started.
            r.update(status='not_started', stopped_by=r.pop('error'))
        return r

    with (out / 'episodes.jsonl').open('x') as log:
        def record(r):
            r.update(completion_index=len(rows) + 1, elapsed_seconds=time.monotonic() - start,
                     study_accounting=ledger.transact() if ledger else {})
            log.write(json.dumps(r, sort_keys=True) + '\n'); log.flush(); os.fsync(log.fileno())
            rows.append(r)

        index = 0
        last_render = time.monotonic()
        workers = 1 if p['backend'] == 'scripted' else budget['workers']
        with ThreadPoolExecutor(max_workers=workers) as pool:
            pending = {}

            def fill():
                nonlocal index
                # During a billing pause no new call starts in any thread.
                while (stop_reason is None and index < len(todo) and len(pending) < workers
                       and not (billing and billing.paused())):
                    a = todo[index]
                    pending[pool.submit(solve, a)] = a
                    index += 1

            fill()
            while pending:
                done, _ = wait(pending, timeout=5, return_when=FIRST_COMPLETED)
                if not done:
                    if run:
                        note = None
                        if billing and billing.paused():
                            note = ('Billing pause: the provider reports the credit balance is too low; '
                                    're-sending the same call on the slow schedule')
                        run.progress(len(settled) + len(rows), total, episodes=len(rows), message=note)
                    fill()
                    continue
                for f in done:
                    pending.pop(f)
                    r = f.result()
                    record(r)
                    if r.get('stopped_by') == billing_stop_category():
                        stop_reason = stop_reason or r['stopped_by']
                    elif r['status'] == 'failed':
                        failures = failed_before + sum(x['status'] == 'failed' for x in rows)
                        if is_integrity(r['error']):
                            stop_reason = stop_reason or 'integrity:' + r['error']
                        elif strict:
                            stop_reason = stop_reason or 'invalid_rows:' + r['error']    # first failure stops dispatch
                        elif failures > max_failed:
                            stop_reason = stop_reason or f'failed_calls_exceed_limit:{failures}'
                if run:
                    m = usage_metrics(rows, len(rows))
                    run.progress(len(settled) + len(rows), total, episodes=len(rows), invalid=m['invalid'], model_calls=m['model_calls'],
                                 input_tokens=m['input_tokens'], output_tokens=m['output_tokens'], cost_usd=m['cost_usd'])
                    if time.monotonic() - last_render > 20 or stop_reason:
                        try:
                            render.frame(combine(prior_parts + [rows]), total, stage, time.monotonic() - start,
                                         rows[-1]['study_accounting']).save(out / 'progress.png')
                            upload(run, out / 'progress.png')
                        except Exception as exc:
                            reporting_errors.append(type(exc).__name__)
                        last_render = time.monotonic()
                fill()
        for a in todo[index:]:
            r = base(a)
            r['status'] = 'not_started'
            record(r)

    with gzip.open(out / 'episodes.jsonl.gz', 'wb') as f:
        f.write((out / 'episodes.jsonl').read_bytes())
    stage_rows = combine(prior_parts + [rows])
    final = ledger.transact() if ledger else {}
    summary = summarize(p, stage_rows, total, invariants, time.monotonic() - start, initial, final, part_rows=rows)
    summary['reporting_errors'] = reporting_errors
    summary['visualization'] = {'mapping': 'v1', 'frames': render.replay(stage_rows, out, stage, total, initial)}
    write_json(out / 'summary.json', summary)
    analysis = analyze.analyze(stage_rows)
    write_json(out / 'analysis.json', analysis)
    metrics = hub_metrics(summary, analysis)
    failure = summary['failure']
    if run:
        try:
            for name in ARTIFACTS:
                upload(run, out / name)
        except Exception as exc:
            failure = failure or 'artifact_upload_' + type(exc).__name__
    counts = f'{summary["graded"]}/{total} valid, {summary["failed"]} failed, {summary["not_started"]} not started'
    if failure:
        if stage != 'S1':
            metrics['qualification_passed'] = 0
        if run:
            run.fail(f'{stage}: {failure}; {counts}', **metrics)
        raise StageFailed(failure, summary)
    if run:
        run.done(message=f'{stage}: {counts}; {metrics["model_calls"]} model calls in this run, USD {metrics["cost_usd"]:.4f}', **metrics)
    return summary


def hub_metrics(summary, analysis):
    """Final hub metrics of a run: stage-level outcome counts, this run's own usage."""
    own = summary['part_usage']
    m = {'episodes': summary['planned'], 'invalid': summary['invalid'], 'failed': summary['failed'],
         'not_started': summary['not_started'],
         'model_calls': own['model_calls'], 'input_tokens': own['input_tokens'], 'output_tokens': own['output_tokens'],
         'cost_usd': own['cost_usd'], 'transport_attempts': own['transport_attempts'],
         'count_fallbacks': own['count_fallbacks'],
         'billing_stop': int(summary['failure'] == billing_stop_category())}
    m.update(summary['billing'])
    stage = summary['params']['stage']
    for effort, e in summary['by_effort'].items():
        m[f'stage_calls_{effort}'] = e['calls']
        m[f'stage_cost_usd_{effort}'] = e['cost_usd']
    if stage != 'S1':
        m['qualification_passed'] = int(bool(summary['gate']['passed']))
    else:
        primary = (analysis or {}).get('primary')
        overall = (analysis or {}).get('overall') or {}
        for name in ('rare_fabricated', 'rare_accuracy'):
            if overall.get(name) is not None:
                m[name] = overall[name]
        if primary and primary['mean'] is not None:
            m['primary_contrast_pp'] = primary['mean'] * 100
    return m


def summarize(p, rows, total, invariants, elapsed, initial, final, part_rows=None):
    """Recomputable from the saved rows: `chain.py verify` calls this again and compares.

    `rows` are the stage's rows over the original run and its continuations (one per unit);
    `part_rows` are the rows this run recorded itself.
    """
    stage = p['stage']
    budget = study.design()['budget']
    part_rows = rows if part_rows is None else part_rows
    m = usage_metrics(rows, total)
    q = study.qualification(rows) if stage in ('S0', 'Q0') else None
    probe = study.probe_gate(rows) if stage == 'P0' else None
    max_failed = budget['max_failed'].get(stage, 0)
    covered = len(rows) == total
    valid = m['completed'] == total and covered
    errors = [r.get('error') for r in rows if r['status'] == 'failed']
    integrity = next((e for e in errors if is_integrity(e)), None)
    failure = None
    if any(r.get('stopped_by') == billing_stop_category() for r in rows if r['status'] == 'not_started'):
        failure = billing_stop_category()
    elif integrity:
        failure = 'integrity:' + integrity
    elif stage == 'S1' and m['failed'] > max_failed:
        failure = f'failed_calls_exceed_limit:{m["failed"]}'
    elif stage != 'S1' and errors:
        failure = 'invalid_rows:' + errors[0]
    elif m['not_started'] or not covered:
        failure = 'incomplete_rows'
    if stage == 'S0':
        gate = {'passed': bool(valid and q['passed'] and invariants and invariants['passed'])}
        if failure is None and not (invariants and invariants['passed']):
            failure = 'invariant_failed:' + ','.join(sorted(k for k, ok in (invariants or {'checks': {}})['checks'].items() if not ok))
    elif stage == 'P0':
        gate = {'passed': bool(valid and probe['passed'])}
    elif stage == 'Q0':
        gate = {'passed': bool(valid and q['passed'])}
    else:
        gate = {'passed': None}
    if failure is None and gate['passed'] is False:
        failure = 'qualification_failed'
    own = usage_metrics(part_rows, len(part_rows))
    summary = {'params': p, 'model': p['model'], 'part': part_of(p), 'planned': total, 'part_units': len(part_rows),
               'started': total - m['not_started'], 'terminal': len(rows),
               'graded': m['completed'], 'analyzed': m['completed'], 'invalid': m['invalid'],
               'failed': m['failed'], 'not_started': m['not_started'], 'max_failed': max_failed,
               'model_calls': m['model_calls'], 'input_tokens': m['input_tokens'], 'output_tokens': m['output_tokens'],
               'cost_usd': m['cost_usd'], 'transport_attempts': m['transport_attempts'],
               'count_fallbacks': m['count_fallbacks'],
               'part_usage': {k: own[k] for k in ('model_calls', 'input_tokens', 'output_tokens', 'cost_usd',
                                                  'transport_attempts', 'count_fallbacks', 'completed', 'failed', 'not_started')},
               'billing': billing_metrics(rows), 'by_effort': by_effort(rows),
               'failure_categories': sorted(set(e for e in errors if e)),
               'elapsed_seconds': elapsed,
               'qualification': q, 'probe': probe, 'invariants': invariants, 'gate': gate, 'failure': failure,
               'reference_cells': study.reference_cell_means(rows) if stage in ('S0', 'S1') else None,
               'study_accounting': final, 'initial_study_accounting': initial}
    if stage == 'P0' and rows and rows[0]['status'] == 'completed':
        acc = rows[0]['accounting']
        calls = budget['max_attempted_calls']
        summary['probe_measurement'] = {
            'input_tokens': acc['input_tokens'], 'counted_input_tokens': acc['counted_input_tokens'],
            'output_tokens': acc['output_tokens'], 'latency_seconds': acc.get('latency_seconds'),
            'cost_usd': acc['actual_usd'], 'reserved_usd': acc['reserved_usd'],
            'chain_projection_usd_at_probe_cost': acc['actual_usd'] * calls,
            'chain_ceiling_usd_at_full_reservation': acc['reserved_usd'] * calls}
    return summary


def main():
    ap = argparse.ArgumentParser(description='Offline scripted S0 only. Paid stages run through chain.py.')
    ap.add_argument('--stage', choices=['S0'], required=True)
    ap.add_argument('--attempt', required=True)
    ap.add_argument('--results-dir')
    a = ap.parse_args()
    if not a.attempt.replace('-', '').isalnum():
        raise SystemExit('Offline S0 requires a fresh attempt name (letters, digits, hyphens)')
    root = Path(a.results_dir) if a.results_dir else study.results_root()
    try:
        summary = execute(study.params('S0'), root / a.attempt)
    except StageFailed as exc:
        print(json.dumps({'stage': 'S0', 'passed': False, 'failure': exc.reason}))
        raise SystemExit(1)
    print(json.dumps({k: summary[k] for k in ('planned', 'graded', 'invalid', 'model_calls', 'cost_usd', 'gate',
                                               'failure', 'invariants', 'qualification', 'reference_cells', 'elapsed_seconds')}))


if __name__ == '__main__':
    main()
