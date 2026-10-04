"""One finite stage: durable per-row log, no answer retries, and the failure-handling rule.

A row is one agent call (one member, one round). A team episode is 30 rows: its rounds run in
order because each round's inputs contain the board and the decisions of the rounds before; the
five calls of a round are sent together.

Failure-handling rule (required by dmarz/fleet-monitor, 2026-10-04):
- S0, P0 and Q0 are strict: the first failed call stops new dispatch and the stage fails its gate.
- In S1 a failed call ends its episode (the episode's remaining calls are recorded as not started)
  and dispatch continues. Dispatch stops when failed episodes exceed `budget.max_failed`.
- An integrity failure (ledger refusal, reservation bound, model mismatch, deadline, internal
  error) stops dispatch at once in every stage.
- A billing outage that outlasts its wait stops the stage as `provider_credit_balance_low`: the
  affected calls and everything unfinished are recorded as not started, nothing counts as a failed
  unit, and `chain.py resume` may run exactly those rows later at the same source hash.

The hub run ends `done` when S0, P0 or Q0 passed its gate with every row valid, or when S1
finished within the failure limit; otherwise it ends `failed`. Both endings report episodes (call
rows), invalid, model_calls, input_tokens, output_tokens and cost_usd.
"""
import argparse
import gzip
import json
import math
import os
import threading
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

import analyze
import provider
import render
import sim
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
    """The numbers every ending of a stage reports to the hub. `episodes` counts call rows."""
    acc = [r.get('accounting') or {} for r in rows]
    completed = sum(r['status'] == 'completed' for r in rows)
    return {'episodes': total, 'invalid': total - completed,
            'model_calls': sum(bool(a.get('attempted')) for a in acc),
            'input_tokens': sum(a.get('input_tokens', 0) for a in acc),
            'output_tokens': sum(a.get('output_tokens', 0) for a in acc),
            'cost_usd': math.fsum(a.get('actual_usd', 0) for a in acc),
            'transport_attempts': sum(a.get('attempts', 0) for a in acc),
            'completed': completed, 'failed': sum(r['status'] == 'failed' for r in rows),
            'not_started': sum(r['status'] == 'not_started' for r in rows),
            'failed_episodes': len(study.failed_units(rows)),
            'count_fallbacks': sum(bool(a.get('count_fallback')) for a in acc),
            'billing_pauses': sum(a.get('billing_pauses_led', 0) for a in acc),
            'billing_pause_seconds': sum(a.get('billing_wait_seconds', 0) for a in acc),
            'billing_affected_calls': sum(bool(a.get('billing_rejections')) for a in acc),
            'billing_stop': int(any(r.get('interrupted') == provider.CREDIT_STOP for r in rows))}


def execute(p, out, run=None, backend=None, ledger_path=None, opener=None, deadline=None, prior=None, sleep=None):
    """Run one stage into the fresh directory `out`. Returns the summary or raises StageFailed.

    `deadline` is an absolute time.monotonic() value from the chain; no call is dispatched after it.
    `prior` holds the saved rows of the run this one continues (S1 continuation batches only).
    `sleep` replaces time.sleep in the provider (rehearsal and tests, so that nothing waits).
    """
    rows = []
    try:
        return _execute(p, Path(out), run, backend, ledger_path, opener, deadline, rows, prior, sleep)
    except StageFailed:
        raise
    except BaseException as exc:
        # A crash still reports usage: nothing recorded so far is lost from the hub's accounting.
        reason = 'internal_' + type(exc).__name__
        if run:
            total = max(len(rows), study.design()['stages'].get(p.get('stage'), {}).get('rows', 0))
            metrics = usage_metrics(list(rows), total)
            if p.get('stage') != 'S1':
                metrics['qualification_passed'] = 0
            run.fail(f'{p.get("stage")}: {reason}', **metrics)
        raise StageFailed(reason) from exc


def unit_record(unit):
    """What is saved about a unit before any call: the fixed inputs of an episode, or the fixture.
    A continuation unit also lists the rows it runs (`only`); saved answers are not copied."""
    if unit['type'] == 'fixture':
        return dict(unit)
    ep = study.Episode(unit['root'], unit['condition'])
    return dict({k: v for k, v in unit.items() if k != 'known'}, fixed_inputs=ep.fixed_inputs())


def _execute(p, out, run, backend, ledger_path, opener, deadline, rows, prior, sleep):
    d = study.design()
    budget = d['budget']
    stage = p['stage']
    if p['source_hash'] != study.source_hash():
        raise RuntimeError('runtime_source_mismatch')
    if stage not in study.STAGES or p['backend'] != ('scripted' if stage == 'S0' else 'anthropic'):
        raise RuntimeError('stage_backend_mismatch')
    continuation = study.continuation_index(stage, p['batch'])      # raises on any other batch name
    if bool(continuation) != (prior is not None):
        raise RuntimeError('continuation_needs_prior_rows')
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    stage_deadline = start + budget['stage_timeout_seconds']
    if deadline is not None:
        stage_deadline = min(stage_deadline, deadline)

    if run:
        run.progress(0, 1, episodes=0, message='Preparing recorded inputs')
    if continuation:
        units = study.continuation_units(prior)
        total = sum(len(study.slots(u)) for u in units)
        prior_failed = len(study.failed_units(prior))
    else:
        plan = study.plan(stage)
        units, total, prior_failed = plan['units'], plan['rows'], 0
    with gzip.open(out / 'assignments.jsonl.gz', 'wt') as f:
        for unit in units:
            f.write(json.dumps(unit_record(unit), sort_keys=True) + '\n')
    with gzip.open(out / 'worlds.jsonl.gz', 'wt') as f:
        for root in sorted({u['root'] for u in units}):
            f.write(json.dumps(sim.make_world(root, d['world']), sort_keys=True) + '\n')

    ledger = None
    scripted = p['backend'] == 'scripted'
    if not scripted:
        path = ledger_path or os.environ.get(provider.LEDGER_ENV)
        if not path:
            raise RuntimeError('persistent_budget_ledger_required')
        ledger = provider.Ledger(path)
        backend = backend or provider.Anthropic(ledger, opener, sleep=sleep)
    initial = ledger.transact() if ledger else {}
    reporting_errors = []
    render.frame([], total, stage, accounting=initial).save(out / 'initial_frame.png')
    if run:
        upload(run, out / 'initial_frame.png')

    invariants = None
    if stage == 'S0':
        if run:
            run.progress(0, total, episodes=0, message='Checking instrument invariants')
        invariants = study.check_invariants()

    lock = threading.Lock()
    strict = stage != 'S1'
    state = {'stopped': False, 'failed_units': prior_failed}
    log = (out / 'episodes.jsonl').open('x')

    def base(unit, slot):
        r = study.row_base(unit, slot)
        r.update(run=run.id if run else out.name, stage=stage, backend=p['backend'], batch=p['batch'], code=p['code'],
                 source_hash=p['source_hash'])
        return r

    def record(r):
        with lock:
            r.update(completion_index=len(rows) + 1, elapsed_seconds=time.monotonic() - start,
                     study_accounting=ledger.transact() if ledger else {})
            log.write(json.dumps(r, sort_keys=True) + '\n'); log.flush(); os.fsync(log.fileno())
            rows.append(r)
        return r

    def call(unit, slot, packet, context):
        """One row: the packet, the answer and its grade, or the failure category with its evidence."""
        r = base(unit, slot)
        r.update(packet=packet, packet_hash=study.digest(packet), status='failed')
        try:
            if time.monotonic() > stage_deadline:
                raise provider.CallFailure('stage_deadline')
            if scripted:
                policy, posting = study.actor_policy(unit['actor'])
                answer = study.normalize(study.scripted_answer(packet, policy, posting))
                accounting = {'attempted': False, 'actual_usd': 0, 'reserved_usd': 0}
            else:
                answer, accounting = backend.call(packet, p['batch'] + ':' + r['id'])
            r.update(answer=answer, accounting=accounting, evaluation=study.evaluate(context, packet, answer),
                     status='completed')
        except provider.CallFailure as exc:
            if exc.category == provider.CREDIT_STOP:
                # A billing outage: not an outcome. The row is not started and may be resumed.
                r.update(status='not_started', interrupted=exc.category, accounting=exc.accounting)
            else:
                r.update(error=exc.category, accounting=exc.accounting)
        except Exception as exc:
            r.update(error='internal_' + type(exc).__name__)
        return record(r)

    def settle(done):
        """Apply the failure rule to the rows of one unit step. Returns True if the unit goes on."""
        with lock:
            if any(r.get('interrupted') for r in done):
                state['stopped'] = True             # billing stop: everything unfinished stays not started
                return False
            errors = [r['error'] for r in done if r['status'] == 'failed']
            if not errors:
                return True
            if any(provider.is_integrity(e) for e in errors):
                state['stopped'] = True             # integrity failure: stop at once
            else:
                state['failed_units'] += 1          # one failed unit, however many of its calls failed
                if strict or state['failed_units'] > budget['max_failed']:
                    state['stopped'] = True
            return False

    def run_unit(unit, pool):
        try:
            (run_episode if unit['type'] == 'episode' else run_fixture)(unit, pool)
        except BaseException:
            state['stopped'] = True         # an internal error: nothing new is dispatched anywhere
            raise

    def run_fixture(unit, pool):
        if not state['stopped']:
            settle([call(unit, study.slots(unit)[0], unit['packet'], unit['context'])])

    def run_episode(unit, pool):
        ep = study.Episode(unit['root'], unit['condition'])
        context = ep.context()
        known = unit.get('known', {})       # answers saved by the run this one continues
        for t in range(1, ep.rounds + 1):
            answers = {m: known[f'{unit["id"]}.{m}.r{t}'] for m in ep.models if f'{unit["id"]}.{m}.r{t}' in known}
            jobs = [(m, (f'{unit["id"]}.{m}.r{t}', m, t), ep.packet(m, t)) for m in ep.models if m not in answers]
            if jobs:
                if state['stopped']:
                    return                  # no new round once dispatch has stopped
                if pool is None:
                    done = [call(unit, slot, packet, context) for _, slot, packet in jobs]
                else:
                    done = [f.result() for f in [pool.submit(call, unit, slot, packet, context) for _, slot, packet in jobs]]
                if not settle(done):
                    return                  # this episode ends here; its later rounds are never built
                answers.update({m: r['answer'] for (m, _, _), r in zip(jobs, done)})
            ep.apply(t, answers)

    def snapshot():
        with lock:
            return list(rows)

    episodes = any(u['type'] == 'episode' for u in units)
    unit_workers = 1 if scripted else budget['episode_workers'] if episodes else budget['fixture_workers']
    assert scripted or unit_workers * (len(d['world']['members']) - 1 if episodes else 1) <= budget['workers']
    call_pool = None if scripted or not episodes else ThreadPoolExecutor(max_workers=budget['workers'])
    index = 0
    last_render = time.monotonic()
    try:
        with ThreadPoolExecutor(max_workers=unit_workers) as pool:
            pending = {}

            def fill():
                nonlocal index
                while not state['stopped'] and index < len(units) and len(pending) < unit_workers:
                    unit = units[index]
                    pending[pool.submit(run_unit, unit, call_pool)] = unit
                    index += 1

            try:
                fill()
                while pending:
                    done, _ = wait(pending, timeout=5, return_when=FIRST_COMPLETED)
                    for f in done:
                        pending.pop(f)
                        f.result()              # an internal error in a unit ends the stage as a crash
                    if run:
                        seen = snapshot()
                        m = usage_metrics(seen, len(seen))
                        billing = backend.billing_state() if hasattr(backend, 'billing_state') else None
                        note = {'message': 'Paused: provider credit balance low; the same call is re-sent on the slow schedule'} if billing == 'paused' else {}
                        run.progress(len(seen), total, episodes=len(seen), invalid=m['invalid'], model_calls=m['model_calls'],
                                     input_tokens=m['input_tokens'], output_tokens=m['output_tokens'], cost_usd=m['cost_usd'],
                                     billing_pauses=m['billing_pauses'], **note)
                        if seen and (time.monotonic() - last_render > 20 or (state['stopped'] and done)):
                            try:
                                render.frame(seen, total, stage, time.monotonic() - start, seen[-1]['study_accounting']).save(out / 'progress.png')
                                upload(run, out / 'progress.png')
                            except Exception as exc:
                                reporting_errors.append(type(exc).__name__)
                            last_render = time.monotonic()
                    fill()
            except BaseException:
                # A crash of this loop or a termination signal: no new unit and no new round anywhere.
                # Set before the pool is left, because leaving it waits for the units in flight.
                state['stopped'] = True
                raise

        # Every planned row that never started is recorded, in plan order.
        started = {r['id'] for r in rows}
        for unit in units:
            for slot in study.slots(unit):
                if slot[0] not in started:
                    r = base(unit, slot)
                    r['status'] = 'not_started'
                    record(r)
    finally:
        if call_pool:
            call_pool.shutdown(wait=True)
        log.close()

    with gzip.open(out / 'episodes.jsonl.gz', 'wb') as f:
        f.write((out / 'episodes.jsonl').read_bytes())
    summary = summarize(p, rows, total, invariants, time.monotonic() - start, initial, ledger.transact() if ledger else {}, prior_failed)
    summary['reporting_errors'] = reporting_errors
    # A continuation is analysed and drawn together with the run it continues: every row exactly once.
    everything = study.merge_rows([prior, rows]) if continuation else rows
    summary['visualization'] = {'mapping': 'v1', 'frames': render.replay(everything, out, stage, len(everything) if continuation else total, initial)}
    write_json(out / 'summary.json', summary)
    analysis = analyze.analyze(everything)
    write_json(out / 'analysis.json', analysis)
    metrics = usage_metrics(rows, total)
    if stage != 'S1':
        metrics['qualification_passed'] = int(summary['gate']['passed'])
    else:
        model = analysis['actors'].get('model') or {}
        metrics['team_episodes'] = model.get('team_episodes', 0)
        metrics['team_episodes_complete'] = model.get('team_episodes_complete', 0)
        metrics['failed_episodes'] = summary['failed_units']
        primary = analysis['primary']
        if primary and primary['mean'] is not None:
            metrics['residual_avoidance_pp'] = primary['mean'] * 100
        cascade = (model.get('secondary') or {}).get('cascade_size', {}).get('C0-FA')
        if cascade and cascade['mean'] is not None:
            metrics['cascade_size_pp'] = cascade['mean'] * 100
    failure = summary['failure']
    if run:
        try:
            for name in ARTIFACTS:
                upload(run, out / name)
        except Exception as exc:
            failure = failure or 'artifact_upload_' + type(exc).__name__
    counts = f'{metrics["completed"]}/{total} valid, {metrics["failed"]} failed, {metrics["not_started"]} not started'
    if failure:
        if stage != 'S1':
            metrics['qualification_passed'] = 0
        if run:
            run.fail(f'{stage}: {failure}; {counts}', **metrics)
        raise StageFailed(failure, summary)
    if run:
        limit = f'; {summary["failed_units"]} failed episodes, limit {summary["max_failed"]}' if stage == 'S1' else ''
        run.done(message=f'{stage}: {counts}{limit}; {metrics["model_calls"]} model calls, USD {metrics["cost_usd"]:.4f}', **metrics)
    return summary


def summarize(p, rows, total, invariants, elapsed, initial, final, prior_failed=0):
    """Recomputable from the saved rows: `chain.py verify` calls this again and compares."""
    stage = p['stage']
    budget = study.design()['budget']
    m = usage_metrics(rows, total)
    q = study.qualification(rows) if stage in ('S0', 'Q0') else None
    probe = study.probe_gate(rows) if stage == 'P0' else None
    valid = m['completed'] == total and len(rows) == total
    failed_here = study.failed_units(rows)
    failed_units = prior_failed + len(failed_here)
    integrity = next((r['error'] for r in rows if r['status'] == 'failed' and provider.is_integrity(r.get('error'))), None)
    billing_stop = bool(m['billing_stop'])
    if stage == 'S0':
        # Scripted rows carry no usage; the scripted probe is checked on its decisions alone.
        probe = {'passed': bool(any(r['kind'] == 'probe' and r['status'] == 'completed'
                                    and r['evaluation']['unanimous']['matched'] == r['evaluation']['unanimous']['total'] >= 2
                                    for r in rows)), 'rows': sum(r['kind'] == 'probe' for r in rows)}
        gate = {'passed': bool(valid and q['passed'] and probe['passed'] and invariants and invariants['passed'])}
    elif stage == 'P0':
        gate = {'passed': bool(valid and probe['passed'])}
    elif stage == 'Q0':
        gate = {'passed': bool(valid and q['passed'])}
    else:
        gate = {'passed': None}
    failure = None
    if billing_stop:
        failure = provider.CREDIT_STOP                  # a billing outage outlasted its wait: resumable in S1
    elif stage == 'S1':
        # A failed call ends its episode; the stage is done while failed episodes stay within the limit.
        stray = any(r['status'] == 'not_started' and study.unit_of(r) not in failed_here for r in rows)
        if integrity:
            failure = 'integrity_failure:' + integrity
        elif failed_units > budget['max_failed']:
            failure = 'failed_units_exceed_limit'
        elif len(rows) != total or stray:
            failure = 'incomplete_rows'
    elif not valid:
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
               'failed_units': failed_units, 'prior_failed_units': prior_failed, 'max_failed': budget['max_failed'],
               'integrity_failure': integrity, 'count_fallbacks': m['count_fallbacks'],
               'billing': {'pauses': m['billing_pauses'], 'pause_seconds': m['billing_pause_seconds'],
                           'affected_calls': m['billing_affected_calls'], 'stopped': billing_stop,
                           'interrupted_rows': sum(bool(r.get('interrupted')) for r in rows)},
               'continuation': study.continuation_index(stage, p['batch']),
               'qualification': q, 'probe': probe, 'invariants': invariants, 'gate': gate, 'failure': failure,
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
                                               'failure', 'invariants', 'qualification', 'probe', 'elapsed_seconds')}))


if __name__ == '__main__':
    main()
