"""One stage as one finite batch: durable per-row log, no answer retries, first failure stops new
dispatch and the remaining assignments are recorded as not started. On success and on failure the
hub run ends with episodes, invalid, model_calls, input_tokens, output_tokens and cost_usd."""
import argparse
import gzip
import json
import os
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

import analyze
import provider
import render
import study

ARTIFACTS = ('final_frame.png', 'initial_frame.png', 'progress.png', 'replay.gif', 'assignments.jsonl.gz',
             'episodes.jsonl.gz', 'worlds.jsonl.gz', 'summary.json', 'analysis.json')


class StageFailed(RuntimeError):
    """The stage ran to a recorded end but did not pass (invalid rows or a failed gate)."""


def write_json(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True); f.flush(); os.fsync(f.fileno())


def upload(run, path):
    receipt = run.artifact(path, path.name)
    if not receipt or receipt.get('spooled'): raise RuntimeError('artifact_not_durably_acknowledged')


def totals(rows, planned):
    acct = [r.get('accounting') or {} for r in rows]
    return {'episodes': planned, 'invalid': planned - sum(r['status'] == 'completed' for r in rows),
            'model_calls': sum(bool(a.get('attempted')) for a in acct),
            'transport_attempts': sum(a.get('attempts', 0) for a in acct),
            'input_tokens': sum(a.get('input_tokens', 0) for a in acct),
            'output_tokens': sum(a.get('output_tokens', 0) for a in acct),
            'cost_usd': sum(a.get('actual_usd', 0) for a in acct)}


def row_base(a, p, run_name):
    r = {key: a[key] for key in study.ROW_FIELDS}
    r.update(run=run_name, stage=p['stage'], backend=p['backend'], code=p['code'], source_hash=p['source_hash'],
             admission=a['admission'], status='failed')
    return r


def run_stage(p, out, run, backend, deadline, state, opener=None):
    stage = p['stage']; budget = study.design()['budget']
    assert p['source_hash'] == study.source_hash(), 'runtime_source_mismatch'
    assert p['backend'] == ('scripted' if stage == 'S0' else 'anthropic')
    out = Path(out); out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic(); run_name = run.id if run else out.name
    stop_at = start + budget['stage_timeout_seconds']
    if deadline is not None: stop_at = min(stop_at, deadline)
    def preparing(message):
        if run: run.progress(0, 1, episodes=0, message='Preparing recorded inputs: ' + message)
    assigned = study.assignments(stage, out, preparing); total = len(assigned); state['total'] = total
    with gzip.open(out / 'assignments.jsonl.gz', 'wt') as f:
        for a in assigned: f.write(json.dumps(a, sort_keys=True) + '\n')
    violations = study.check_invariants(stage)
    ledger = None
    if p['backend'] == 'anthropic':
        path = os.environ.get('STUDY_BUDGET_LEDGER'); assert path, 'persistent_budget_required'
        assert total <= budget['max_calls'][stage], 'assignments_exceed_stage_call_cap'
        ledger = provider.Ledger(path); backend = backend or provider.Anthropic(ledger, opener=opener)
    initial = ledger.transact() if ledger else {}
    rows = state['rows']; reporting_errors = []
    stopped = bool(violations) and p['backend'] != 'scripted'      # structurally broken inputs: no call is made
    render.frame([], total, stage, accounting=initial).save(out / 'initial_frame.png')
    if run: upload(run, out / 'initial_frame.png')

    def solve(a):
        r = row_base(a, p, run_name)
        try:
            if time.monotonic() > stop_at: raise provider.CallFailure('stage_deadline', {'attempted': False})
            if p['backend'] == 'scripted':
                answer = study.scripted(a['packet']); accounting = {'attempted': False, 'actual_usd': 0, 'reserved_usd': 0}
            else:
                answer, accounting = backend.call(a['packet'], p['batch'] + ':' + a['id'])
            r.update(answer=answer, accounting=accounting, evaluation=study.evaluate(a, answer),
                     scripted_evaluation=study.evaluate(a, study.scripted(a['packet'])),
                     identity_evaluation=study.evaluate(a, study.scripted(a['packet'], by_identity=True)), status='completed')
        except provider.CallFailure as exc:
            r.update(error=exc.category, accounting=exc.accounting)
        except Exception as exc:
            r.update(error='internal_' + type(exc).__name__, accounting=r.get('accounting', {}))
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
                    pending.pop(f); r = f.result(); record(r)
                    if r['status'] != 'completed': stopped = True
                if run:
                    t = totals(rows, len(rows))
                    run.progress(len(rows), total, episodes=len(rows), invalid=t['invalid'], model_calls=t['model_calls'],
                                 input_tokens=t['input_tokens'], output_tokens=t['output_tokens'], cost_usd=t['cost_usd'])
                    if done and (time.monotonic() - last_render > 20 or stopped):
                        try:
                            render.frame(rows, total, stage, time.monotonic() - start, rows[-1]['study_accounting'] or initial).save(out / 'progress.png')
                            upload(run, out / 'progress.png')
                        except Exception as exc: reporting_errors.append(type(exc).__name__)
                        last_render = time.monotonic()
                fill()
        for a in assigned[index:]:
            r = row_base(a, p, run_name); r.update(status='not_started'); record(r)
    with gzip.open(out / 'episodes.jsonl.gz', 'wb') as f: f.write((out / 'episodes.jsonl').read_bytes())
    good = [r for r in rows if r['status'] == 'completed']; t = totals(rows, total)
    if stage == 'S0': violations = violations + study.degeneracy(rows)
    passed_gate = study.gate(stage, rows, violations)
    pilot = [r for r in rows if r['kind'] == 'pilot']
    analysis = analyze.analyze(rows) if pilot else {'cells': [], 'note': 'this stage has no comparison rows'}
    frames = None
    try:
        render.frame(rows, total, stage, time.monotonic() - start, (rows[-1]['study_accounting'] if rows else None) or initial).save(out / 'progress.png')
        frames = render.replay(rows, out, stage, total, initial)
    except Exception as exc: reporting_errors.append('render_' + type(exc).__name__)
    passed = t['invalid'] == 0 and passed_gate is not False and not violations
    summary = {'params': p, 'experiment': study.EXPERIMENT, 'planned': total,
               'started': sum(r['status'] != 'not_started' for r in rows), 'terminal': len(rows), 'graded': len(good),
               'analyzed': len(good), 'not_started': sum(r['status'] == 'not_started' for r in rows),
               'failed': sum(r['status'] == 'failed' for r in rows),
               'errors': sorted({r['error'] for r in rows if r.get('error')}), **t,
               'elapsed_seconds': time.monotonic() - start,
               'qualification': study.qualification(rows) if stage in ('S0', 'Q0') else None,
               'probe': study.probe_gate(rows) if stage in ('S0', 'P0') else None,
               'invariant_violations': violations,
               'qualification_passed': None if passed_gate is None else int(passed_gate), 'passed': passed,
               'reason': None if passed else 'invariant_violations' if violations else 'invalid_rows' if t['invalid'] else 'gate_failed',
               'request_bytes_mean': (sum(len(json.dumps(a['packet'], sort_keys=True)) for a in assigned) / total) if total else 0,
               'primary_contrast': analysis.get('primary', {}).get('estimate') if pilot else None,
               'rare_wrong': analyze.mean(r['evaluation']['rare_wrong'] for r in good if r['kind'] == 'pilot'),
               'rare_accuracy': analyze.mean(r['evaluation']['rare_accuracy'] for r in good if r['kind'] == 'pilot'),
               'study_accounting': ledger.transact() if ledger else {}, 'initial_study_accounting': initial,
               'reporting_errors': reporting_errors, 'visualization': {'mapping': 'v1', 'frames': frames}}
    write_json(out / 'summary.json', summary); write_json(out / 'analysis.json', analysis)
    if run:
        for name in ARTIFACTS:
            if (out / name).exists(): upload(run, out / name)
    return summary


def hub_metrics(summary):
    m = {k: summary[k] for k in ('episodes', 'invalid', 'model_calls', 'transport_attempts', 'input_tokens', 'output_tokens', 'cost_usd')}
    for k in ('qualification_passed', 'primary_contrast', 'rare_wrong', 'rare_accuracy'):
        if summary.get(k) is not None: m[k] = summary[k]
    return m


def execute(p, out, run=None, backend=None, deadline=None, opener=None):
    """Run one stage. Returns the summary when the stage passed; raises StageFailed when it ended
    recorded but not passed; re-raises anything unexpected. The hub run is closed in every case."""
    state = {'rows': [], 'total': 0}
    try:
        summary = run_stage(p, out, run, backend, deadline, state, opener)
    except Exception as exc:
        if run:
            t = totals(state['rows'], max(state['total'], len(state['rows'])))
            t['invalid'] = max(1, t['invalid'])
            run.fail(f'{p.get("stage")}: internal_{type(exc).__name__}; rows preserved', **t)
        raise
    stage = summary['params']['stage']
    message = f'{stage}: {summary["graded"]}/{summary["planned"]} valid, {summary["model_calls"]} calls, ${summary["cost_usd"]:.4f}'
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
