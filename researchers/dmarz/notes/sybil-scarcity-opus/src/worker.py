"""One finite stage: durable per-row log, no answer retries, first failure stops new dispatch.

Every assignment ends as completed, failed or not_started. The hub run ends `done` only when
all rows are valid and, for S0, P0 and Q0, the stage gate passed; otherwise it ends `failed`.
Both endings report episodes, invalid, model_calls, input_tokens, output_tokens and cost_usd.
"""
import argparse
import gzip
import json
import math
import os
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


def usage_metrics(rows, total):
    """The numbers every ending of a stage reports to the hub."""
    acc = [r.get('accounting') or {} for r in rows]
    completed = sum(r['status'] == 'completed' for r in rows)
    return {'episodes': total, 'invalid': total - completed,
            'model_calls': sum(bool(a.get('attempted')) for a in acc),
            'input_tokens': sum(a.get('input_tokens', 0) for a in acc),
            'output_tokens': sum(a.get('output_tokens', 0) for a in acc),
            'cost_usd': math.fsum(a.get('actual_usd', 0) for a in acc),
            'transport_attempts': sum(a.get('attempts', 0) for a in acc),
            'completed': completed, 'failed': sum(r['status'] == 'failed' for r in rows),
            'not_started': sum(r['status'] == 'not_started' for r in rows)}


def execute(p, out, run=None, backend=None, ledger_path=None, opener=None, deadline=None):
    """Run one stage into the fresh directory `out`. Returns the summary or raises StageFailed.

    `deadline` is an absolute time.monotonic() value from the chain; no call is dispatched after it.
    """
    rows, total = [], 0
    try:
        return _execute(p, Path(out), run, backend, ledger_path, opener, deadline, rows)
    except StageFailed:
        raise
    except BaseException as exc:
        # A crash still reports usage: nothing recorded so far is lost from the hub's accounting.
        reason = 'internal_' + type(exc).__name__
        if run:
            total = max(len(rows), study.design()['stages'].get(p.get('stage'), {}).get('assignments', 0))
            metrics = usage_metrics(rows, total)
            if p.get('stage') != 'S1':
                metrics['qualification_passed'] = 0
            run.fail(f'{p.get("stage")}: {reason}', **metrics)
        raise StageFailed(reason) from exc


def _execute(p, out, run, backend, ledger_path, opener, deadline, rows):
    d = study.design()
    budget = d['budget']
    stage = p['stage']
    if p['source_hash'] != study.source_hash():
        raise RuntimeError('runtime_source_mismatch')
    if stage not in study.STAGES or p['backend'] != ('scripted' if stage == 'S0' else 'anthropic'):
        raise RuntimeError('stage_backend_mismatch')
    if p['batch'] != study.params(stage)['batch']:
        raise RuntimeError('batch_mismatch')
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

    ledger = None
    if p['backend'] == 'anthropic':
        path = ledger_path or os.environ.get(provider.LEDGER_ENV)
        if not path:
            raise RuntimeError('persistent_budget_ledger_required')
        ledger = provider.Ledger(path)
        backend = backend or provider.Anthropic(ledger, opener)
    initial = ledger.transact() if ledger else {}
    stopped = False
    reporting_errors = []
    render.frame([], total, stage, accounting=initial).save(out / 'initial_frame.png')
    if run:
        upload(run, out / 'initial_frame.png')

    invariants = None
    if stage == 'S0':
        if run:
            run.progress(0, total, episodes=0, message='Checking instrument invariants')
        invariants = study.check_invariants()

    def base(a):
        r = {k: a[k] for k in study.ROW_KEYS}
        r.update(run=run.id if run else out.name, stage=stage, backend=p['backend'], batch=p['batch'], code=p['code'],
                 source_hash=p['source_hash'], scripted_evaluation=study.evaluate(a, study.scripted(a['packet'])))
        return r

    def solve(a):
        r = base(a)
        r['status'] = 'failed'
        try:
            if time.monotonic() > stage_deadline:
                raise provider.CallFailure('stage_deadline')
            if p['backend'] == 'scripted':
                answer = study.scripted(a['packet'])
                accounting = {'attempted': False, 'actual_usd': 0, 'reserved_usd': 0}
            else:
                answer, accounting = backend.call(a['packet'], p['batch'] + ':' + a['id'])
            r.update(answer=answer, accounting=accounting, evaluation=study.evaluate(a, answer), status='completed')
        except provider.CallFailure as exc:
            r.update(error=exc.category, accounting=exc.accounting)
        except Exception as exc:
            r.update(error='internal_' + type(exc).__name__)
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
                while not stopped and index < total and len(pending) < workers:
                    a = assigned[index]
                    pending[pool.submit(solve, a)] = a
                    index += 1

            fill()
            while pending:
                done, _ = wait(pending, timeout=5, return_when=FIRST_COMPLETED)
                if not done:
                    if run:
                        run.progress(len(rows), total, episodes=len(rows), invalid=int(stopped))
                    continue
                for f in done:
                    pending.pop(f)
                    r = f.result()
                    record(r)
                    if r['status'] != 'completed':
                        stopped = True      # first failure: no new dispatch, in-flight calls finish
                if run:
                    m = usage_metrics(rows, len(rows))
                    run.progress(len(rows), total, episodes=len(rows), invalid=m['invalid'], model_calls=m['model_calls'],
                                 input_tokens=m['input_tokens'], output_tokens=m['output_tokens'], cost_usd=m['cost_usd'])
                    if time.monotonic() - last_render > 20 or stopped:
                        try:
                            render.frame(rows, total, stage, time.monotonic() - start, rows[-1]['study_accounting']).save(out / 'progress.png')
                            upload(run, out / 'progress.png')
                        except Exception as exc:
                            reporting_errors.append(type(exc).__name__)
                        last_render = time.monotonic()
                fill()
        for a in assigned[index:]:
            r = base(a)
            r['status'] = 'not_started'
            record(r)

    with gzip.open(out / 'episodes.jsonl.gz', 'wb') as f:
        f.write((out / 'episodes.jsonl').read_bytes())
    summary = summarize(p, rows, total, invariants, time.monotonic() - start, initial, ledger.transact() if ledger else {})
    summary['reporting_errors'] = reporting_errors
    summary['visualization'] = {'mapping': 'v1', 'frames': render.replay(rows, out, stage, total, initial)}
    write_json(out / 'summary.json', summary)
    analysis = analyze.analyze(rows)
    write_json(out / 'analysis.json', analysis)
    metrics = usage_metrics(rows, total)
    if stage != 'S1':
        metrics['qualification_passed'] = int(summary['gate']['passed'])
    else:
        primary = analysis['primary']
        good = [r for r in rows if r['status'] == 'completed']
        if good:
            metrics['rare_accuracy'] = study.mean(r['evaluation']['rare_accuracy'] for r in good)
        if primary and primary['mean'] is not None:
            metrics['primary_contrast_pp'] = primary['mean'] * 100
    failure = summary['failure']
    if run:
        try:
            for name in ARTIFACTS:
                upload(run, out / name)
        except Exception as exc:
            failure = failure or 'artifact_upload_' + type(exc).__name__
    if failure:
        if stage != 'S1':
            metrics['qualification_passed'] = 0
        if run:
            run.fail(f'{stage}: {failure}; {metrics["completed"]}/{total} valid, {metrics["failed"]} failed, {metrics["not_started"]} not started', **metrics)
        raise StageFailed(failure, summary)
    if run:
        run.done(message=f'{stage}: {metrics["completed"]}/{total} valid; {metrics["model_calls"]} model calls, USD {metrics["cost_usd"]:.4f}', **metrics)
    return summary


def summarize(p, rows, total, invariants, elapsed, initial, final):
    """Recomputable from the saved rows: `chain.py verify` calls this again and compares."""
    stage = p['stage']
    m = usage_metrics(rows, total)
    q = study.qualification(rows) if stage in ('S0', 'Q0') else None
    probe = study.probe_gate(rows) if stage == 'P0' else None
    valid = m['completed'] == total and len(rows) == total
    if stage == 'S0':
        gate = {'passed': bool(valid and q['passed'] and invariants and invariants['passed'])}
    elif stage == 'P0':
        gate = {'passed': bool(valid and probe['passed'])}
    elif stage == 'Q0':
        gate = {'passed': bool(valid and q['passed'])}
    else:
        gate = {'passed': None}
    failure = None
    if not valid:
        first = next((r.get('error') for r in rows if r['status'] == 'failed'), None)
        failure = f'invalid_rows:{first}' if first else 'incomplete_rows'
    elif stage == 'S0' and not (invariants and invariants['passed']):
        failure = 'invariant_failed:' + ','.join(sorted(k for k, ok in (invariants or {'checks': {}})['checks'].items() if not ok))
    elif gate['passed'] is False:
        failure = 'qualification_failed'
    summary = {'params': p, 'planned': total, 'started': total - m['not_started'], 'terminal': len(rows),
               'graded': m['completed'], 'analyzed': m['completed'], 'invalid': m['invalid'],
               'failed': m['failed'], 'not_started': m['not_started'],
               'model_calls': m['model_calls'], 'input_tokens': m['input_tokens'], 'output_tokens': m['output_tokens'],
               'cost_usd': m['cost_usd'], 'transport_attempts': m['transport_attempts'], 'elapsed_seconds': elapsed,
               'qualification': q, 'probe': probe, 'invariants': invariants, 'gate': gate, 'failure': failure,
               'study_accounting': final, 'initial_study_accounting': initial}
    if stage == 'P0' and rows and rows[0]['status'] == 'completed':
        acc = rows[0]['accounting']
        calls = study.design()['budget']['max_attempted_calls']
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
                                               'failure', 'invariants', 'qualification', 'elapsed_seconds')}))


if __name__ == '__main__':
    main()
