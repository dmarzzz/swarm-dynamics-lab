"""One stage as one finite batch of multi-turn episodes.

An episode is a sequence of calls; each call's input depends on the answers before it. Episodes
run in parallel, calls inside an episode one at a time. Every call is logged durably when it
ends. No answer is retried. The first failed call ends its episode as failed and stops the stage:
no new call starts anywhere, calls in flight finish, episodes cut short are recorded as
interrupted and episodes never started as not started. On success and on failure the hub run
ends with episodes, invalid, model_calls, input_tokens, output_tokens and cost_usd."""
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
HUB_KEYS = ('episodes', 'invalid', 'model_calls', 'transport_attempts', 'input_tokens', 'output_tokens', 'cost_usd',
            'max_output_tokens_per_call')


class StageFailed(RuntimeError):
    """The stage ran to a recorded end but did not pass (invalid episodes or a failed gate)."""


def write_json(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True); f.flush(); os.fsync(f.fileno())


def upload(run, path):
    receipt = run.artifact(path, path.name)
    if not receipt or receipt.get('spooled'): raise RuntimeError('artifact_not_durably_acknowledged')


def accountings(row):
    out = [t.get('accounting') or {} for t in row.get('turns', [])]
    if row.get('failed_turn'): out.append(row['failed_turn'].get('accounting') or {})
    return out


def totals(rows, planned):
    """Stage totals. `episodes` counts episodes planned; `model_calls` counts calls dispatched."""
    acct = [a for r in rows for a in accountings(r)]
    return {'episodes': planned, 'invalid': planned - sum(r['status'] == 'completed' for r in rows),
            'model_calls': sum(bool(a.get('attempted')) for a in acct),
            'transport_attempts': sum(a.get('attempts', 0) for a in acct),
            'input_tokens': sum(a.get('input_tokens', 0) for a in acct),
            'output_tokens': sum(a.get('output_tokens', 0) for a in acct),
            'cost_usd': sum(a.get('actual_usd', 0) for a in acct),
            'max_output_tokens_per_call': max([a.get('output_tokens', 0) for a in acct] or [0])}


def row_base(a, p, run_name):
    r = {key: a[key] for key in study.ROW_FIELDS}
    r.update(run=run_name, stage=p['stage'], backend=p['backend'], code=p['code'], source_hash=p['source_hash'],
             status='failed', turns=[])
    return r


def run_stage(p, out, run, backend, deadline, state, opener=None):
    stage = p['stage']; budget = study.design()['budget']
    assert p['source_hash'] == study.source_hash(), 'runtime_source_mismatch'
    assert p['backend'] == ('scripted' if stage == 'S0' else 'anthropic')
    out = Path(out); out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic(); run_name = run.id if run else out.name
    stop_at = start + budget['stage_timeout_seconds']
    if deadline is not None: stop_at = min(stop_at, deadline)
    if run: run.progress(0, 1, episodes=0, message='Preparing episodes and checking invariants')
    assigned = study.assignments(stage); total = len(assigned); state['total'] = total
    with gzip.open(out / 'assignments.jsonl.gz', 'wt') as f:
        for a in assigned: f.write(json.dumps(a, sort_keys=True) + '\n')
    violations = study.check_invariants(stage)
    ledger = None
    if p['backend'] == 'anthropic':
        path = os.environ.get('STUDY_BUDGET_LEDGER'); assert path, 'persistent_budget_required'
        assert sum(a['max_turns'] for a in assigned) <= budget['max_calls'][stage], 'possible_calls_exceed_stage_call_cap'
        ledger = provider.Ledger(path); backend = backend or provider.Anthropic(ledger, opener=opener)
    initial = ledger.transact() if ledger else {}
    rows = state['rows']; reporting_errors = []
    stop = threading.Event()            # set by the first failed call: no new call starts after it
    if violations and p['backend'] != 'scripted': stop.set()       # structurally broken inputs: no call is made
    render.frame([], total, stage, accounting=initial).save(out / 'initial_frame.png')
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
            try:
                while ep.lead_turn_due() and len(turns) < a['max_turns']:
                    if stop.is_set():
                        r['status'] = 'interrupted' if turns else 'not_started'; break
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
                stop.set(); r.update(error=exc.category, failed_turn=dict(current or {}, accounting=exc.accounting))
                log_turn(a, dict(r['failed_turn'], status='failed', error=exc.category))
            except Exception as exc:
                stop.set(); r.update(error='internal_' + type(exc).__name__, failed_turn=dict(current or {}, accounting={}))
            r['turns_not_started_max'] = 0 if r['status'] == 'completed' else a['max_turns'] - len(turns) - bool(r.get('failed_turn'))
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
                    t = totals(rows, len(rows))
                    run.progress(len(rows), total, episodes=len(rows), invalid=t['invalid'], model_calls=t['model_calls'],
                                 input_tokens=t['input_tokens'], output_tokens=t['output_tokens'], cost_usd=t['cost_usd'])
                    if done and (time.monotonic() - last_render > 20 or stop.is_set()):
                        try:
                            render.frame(rows, total, stage, time.monotonic() - start, rows[-1]['study_accounting'] or initial).save(out / 'progress.png')
                            upload(run, out / 'progress.png')
                        except Exception as exc: reporting_errors.append(type(exc).__name__)
                        last_render = time.monotonic()
                fill()
        for a in assigned[index:]:
            r = row_base(a, p, run_name); r.update(status='not_started', turns_not_started_max=a['max_turns']); record(r)
    for name in ('episodes.jsonl', 'turns.jsonl'):
        with gzip.open(out / (name + '.gz'), 'wb') as f: f.write((out / name).read_bytes())

    good = [r for r in rows if r['status'] == 'completed']; t = totals(rows, total)
    violations = violations + sorted(f'{r["id"]}:{v}' for r in good for v in r['outcome']['violations'])
    discrimination = study.discrimination(rows) if stage == 'S0' else None
    if discrimination: violations = violations + discrimination
    passed_gate = study.gate(stage, rows, violations)
    compared = [r for r in rows if r['kind'] in analyze.KINDS]
    analysis = analyze.analyze(rows, analyze.actor(stage)) if compared else {'cells': [], 'note': 'this stage has no comparison episodes'}
    frames = None
    try:
        final = render.frame(rows, total, stage, time.monotonic() - start, (rows[-1]['study_accounting'] if rows else None) or initial)
        final.save(out / 'progress.png'); final.save(out / 'final_frame.png')
        frames = render.replay(rows, assigned, out, stage)
    except Exception as exc: reporting_errors.append('render_' + type(exc).__name__)
    passed = t['invalid'] == 0 and passed_gate is not False and not violations
    statuses = {s: sum(r['status'] == s for r in rows) for s in ('completed', 'failed', 'interrupted', 'not_started')}
    primary = analysis.get('primary') or {}
    summary = {'params': p, 'experiment': study.EXPERIMENT, 'planned': total,
               'started': sum(bool(r['turns'] or r.get('failed_turn')) for r in rows), 'terminal': len(rows), 'graded': len(good),
               'analyzed': len(good), 'not_started': statuses['not_started'], 'failed': statuses['failed'],
               'interrupted': statuses['interrupted'], 'turns_completed': sum(len(r['turns']) for r in rows),
               'turns_not_started_max': sum(r['turns_not_started_max'] for r in rows),
               'errors': sorted({r['error'] for r in rows if r.get('error')}), **t,
               'elapsed_seconds': time.monotonic() - start,
               'qualification': study.qualification(rows) if stage in ('S0', 'Q0') else None,
               'probe': study.probe_gate(rows) if stage in ('S0', 'P0') else None,
               'discrimination': discrimination, 'invariant_violations': violations,
               'qualification_passed': None if passed_gate is None else int(passed_gate), 'passed': passed,
               'reason': None if passed else 'invariant_violations' if violations else 'invalid_rows' if t['invalid'] else 'gate_failed',
               'request_bytes_mean': analyze.mean(a.get('request_bytes') for r in rows for a in accountings(r) if a.get('request_bytes')),
               'excess_identities': primary.get('estimate') if compared else None,
               'units_beyond_share': analysis.get('headline', {}).get('units_beyond_share') if compared else None,
               'job_completion': analysis.get('headline', {}).get('job_completion') if compared else None,
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
    message = (f'{stage}: {summary["graded"]}/{summary["planned"]} episodes valid, {summary["model_calls"]} calls, '
               f'${summary["cost_usd"]:.4f}')
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
