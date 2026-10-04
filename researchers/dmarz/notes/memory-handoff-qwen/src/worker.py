"""One stage as one finite batch of single-call assignments.

Every assignment ends as completed, failed or not_started; each row is logged durably when it
ends, and every step (handoff, call start, response or failure, terminal) goes into a
hash-chained journal. No answer is ever retried.

S0, P0 and Q0 are strict: the first failed call stops the stage and the gate needs every row.
In S1 a call without a valid answer is recorded as failed with its evidence and dispatch
continues until failed calls exceed budget.max_failed; an integrity failure (a ledger refusal, a
breached reservation, a model or provider mismatch, the input ceiling, a deadline, an internal
error) stops dispatch at once. A billing outage that outlasts its limit stops the stage with
`provider_credit_balance_low`: the affected and unfinished calls are recorded as not started,
nothing counts as failed, and S1 can be resumed (`chain.py resume`).

On success and on failure the hub run ends with episodes, invalid, model_calls, input_tokens,
output_tokens and cost_usd.
"""
import argparse
import copy
import gzip
import hashlib
import json
import math
import os
import sys
import threading
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analyze      # noqa: E402
import journal      # noqa: E402
import provider     # noqa: E402
import render       # noqa: E402
import sim          # noqa: E402
import study        # noqa: E402

ARTIFACTS = ('final_frame.png', 'initial_frame.png', 'progress.png', 'replay.gif', 'replay.html', 'assignments.jsonl.gz',
             'episodes.jsonl.gz', 'events.jsonl.gz', 'summary.json', 'analysis.json')
REQUIRED_METRICS = ('episodes', 'invalid', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd')
HUB_KEYS = REQUIRED_METRICS + ('failed', 'answered_calls', 'transport_attempts', 'retrieval_count', 'retrieval_bytes',
                               'billing_pauses', 'billing_pause_seconds', 'billing_affected_calls')
# Failures that stop a stage at once, whatever the number of failed calls.
STOP_NOW = tuple(provider.INTEGRITY) + ('input_size_limit', 'input_ceiling_exceeded', 'packet_mismatch', 'unknown_ledger_event')
NO_BILLING = {'billing_pauses': 0, 'billing_pause_seconds': 0.0, 'billing_affected_calls': 0}
SCRIPTED_ACCOUNT = {'attempted': False, 'usage_reported': False, 'attempts': 0, 'actual_usd': 0, 'reserved_usd': 0}


class StageFailed(RuntimeError):
    """The stage ran to a recorded end but did not pass (invalid rows, a stop or a failed gate)."""


def write_json(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True); f.flush(); os.fsync(f.fileno())


def upload(run, path):
    receipt = run.artifact(path, path.name)
    if not receipt or receipt.get('spooled'):
        raise RuntimeError('artifact_not_durably_acknowledged')


def totals(rows, planned):
    """Stage totals. `model_calls` counts calls dispatched with a standing reservation in the ledger (a
    call that a billing stop left unanswered has its reservation voided and is not counted);
    `answered_calls` counts calls for which the provider reported usage."""
    acct = [r.get('accounting') or {} for r in rows]
    logs = [r.get('retrieval') or {} for r in rows if r['status'] != 'not_started']
    return {'episodes': planned, 'invalid': planned - sum(r['status'] == 'completed' for r in rows),
            'failed': sum(r['status'] == 'failed' for r in rows),
            'model_calls': sum(bool(a.get('attempted')) and not a.get('voided') for a in acct),
            'voided_calls': sum(bool(a.get('voided')) for a in acct),
            'answered_calls': sum(bool(a.get('usage_reported')) for a in acct),
            'transport_attempts': sum(a.get('attempts', 0) for a in acct),
            'input_tokens': sum(a.get('input_tokens', 0) for a in acct),
            'output_tokens': sum(a.get('output_tokens', 0) for a in acct),
            'cost_usd': math.fsum(a.get('actual_usd', 0) for a in acct),
            'max_output_tokens_per_call': max([a.get('output_tokens', 0) for a in acct] or [0]),
            'retrieval_count': sum(x.get('registry_lookups', 0) + x.get('records_retrieved', 0) for x in logs),
            'retrieval_bytes': sum(x.get('bytes', 0) for x in logs)}


def load_probe_row(sr=None):
    """P0's saved row for the Q0 gate: read from the results directory of this chain, at this source
    hash, and (when a hub client is given) checked against the hub's record of the P0 run."""
    status = json.loads((study.results_dir() / 'chain-status.json').read_text())
    entry = status['stages']['P0']
    if status.get('source_hash') != study.source_hash() or entry.get('status') != 'done':
        raise ValueError('no passed P0 at this source hash')
    path = Path(entry['directory']) / 'episodes.jsonl.gz'
    rows = study.read_rows(entry['directory'])
    q = study.design()['qualification']
    expected = study.qualification_fixtures(q['set'])[q['probe_fixture']]
    if len(rows) != 1 or rows[0]['id'] != expected['id'] or rows[0]['source_hash'] != study.source_hash() \
            or rows[0]['packet_hash'] != expected['packet_hash']:
        raise ValueError('saved P0 row does not match the probe fixture')
    if sr is not None:
        detail = sr.get_run(entry['run']); hub = {a['name']: a for a in detail.get('artifacts', [])}
        if detail.get('status') != 'done' or (detail.get('params') or {}).get('source_hash') != study.source_hash() \
                or hub.get('episodes.jsonl.gz', {}).get('sha256') != hashlib.sha256(path.read_bytes()).hexdigest():
            raise ValueError('saved P0 row differs from the hub record')
    return rows[0]


WORK_FLAGS = ('value_as_float', 'value_as_string', 'duplicate_sources', 'sources_null', 'work_malformed', 'work_before_value',
              'current_as_string')
WORK_REPORT = ('listing_given', 'listing_matches_message', 'follows_from_own_listing', 'counting_values_consistent',
               'distinct_origins_consistent')


def work_totals(rows):
    """Counts over completed rows of the tolerated answer variants and of what the working fields
    show. Reported, never gated."""
    done = [r for r in rows if r['status'] == 'completed']
    out = {'answers': len(done)}
    for k in WORK_FLAGS:
        out[k] = sum(int(bool((r.get('tolerated') or {}).get(k))) for r in done)
    out['extra_keys'] = sum(int(bool((r.get('tolerated') or {}).get('extra_keys'))) for r in done)
    out['work_missing'] = sum(int(bool((r.get('tolerated') or {}).get('work_missing'))) for r in done)
    for k in WORK_REPORT:
        out[k] = sum(int((r.get('work_report') or {}).get(k) == 1) for r in done)
    out['supported_and_follows_own_listing'] = sum(
        int(r['evaluation']['supported'] == 1 and (r.get('work_report') or {}).get('follows_from_own_listing') == 1) for r in done)
    out['unsupported_but_follows_own_listing'] = sum(
        int(r['evaluation']['supported'] == 0 and (r.get('work_report') or {}).get('follows_from_own_listing') == 1) for r in done)
    return out


def replay_units(everything, rows):
    by_id = {r['id']: r for r in rows}; out = []
    for a in everything:
        r = by_id.get(a['id']) or {'status': 'not_started'}
        view = study.unit_view(a)
        out.append({'id': a['id'], 'root': a['root'], 'family': a['family'], 'state': a['state'], 'policy': a['policy'],
                    'key': view['key'], 'truth': view['truth'], 'truth_answer': view['truth_answer'], 'store': view['store'],
                    'notes': view['notes'], 'packet': a['packet'], 'retrieval': r.get('retrieval') or a['retrieval'],
                    'status': r['status'], 'answer': r.get('answer'), 'evaluation': r.get('evaluation'),
                    'reference': sim.reference(a['packet']), 'error': r.get('error')})
    return out


def run_stage(p, out, run, backend, deadline, state, opener=None, units=None, prior_rows=None, sr=None, clock=None, sleep=None,
              probe_row=None):
    """`units` (assignment ids) and `prior_rows` are given only for a continuation of S1 after a
    billing stop: the run then holds exactly those assignments and reports the earlier runs' rows
    and its own together."""
    stage = p.get('stage'); d = study.design(); budget = d['budget']; strict = stage in study.STRICT
    if p.get('source_hash') != study.source_hash(): raise RuntimeError('runtime_source_mismatch')
    if stage not in study.STAGES or p.get('backend') != ('scripted' if stage == 'S0' else study.BACKEND):
        raise RuntimeError('stage_backend_mismatch')
    if (units is None) != (p.get('batch') == study.batch(stage)) or (units is not None and stage != 'S1'):
        raise RuntimeError('batch_mismatch')
    scripted = p['backend'] == 'scripted'
    out = Path(out); out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic(); run_name = run.id if run else out.name
    stop_at = start + budget['stage_timeout_seconds']
    if deadline is not None: stop_at = min(stop_at, deadline)
    if run: run.progress(0, 1, episodes=0, message='Preparing assignments and checking invariants')
    everything = study.assignments(stage); full = len(everything)
    assigned = everything if units is None else [a for a in everything if a['id'] in set(units)]
    if units is not None and len(assigned) != len(set(units)): raise RuntimeError('unknown_units')
    total = len(assigned); state['total'] = total
    prior = list(prior_rows or [])
    with gzip.open(out / 'assignments.jsonl.gz', 'wt') as f:
        for a in assigned: f.write(json.dumps(a, sort_keys=True) + '\n')
    invariants = study.check_invariants() if stage == 'S0' else None
    log_book = journal.Journal(out / 'events.jsonl')
    log_book.emit('stage_start', stage=stage, batch=p['batch'], source_hash=p['source_hash'], assignments=total,
                  continuation=None if units is None else {'units': total, 'earlier_rows': len(prior)})

    stop = threading.Event()            # no new call starts after it is set
    control = {'reason': None, 'failed': sum(r['status'] == 'failed' for r in study.combine(prior))}; control_lock = threading.Lock()

    def halt(reason):
        with control_lock:
            if control['reason'] is None: control['reason'] = reason
        stop.set()

    probe = None
    if stage == 'Q0':
        try:
            probe = probe_row or load_probe_row(sr)
        except Exception as exc:        # no call is made without the probe's row
            halt('probe_row_unavailable'); log_book.emit('probe_row_unavailable', error=type(exc).__name__)
    if invariants is not None and not invariants['passed']:
        log_book.emit('invariants_failed', checks=sorted(k for k, ok in invariants['checks'].items() if not ok))

    ledger = None
    if not scripted:
        path = os.environ.get(provider.LEDGER_ENV)
        if not path: raise RuntimeError('persistent_budget_ledger_required')
        if total > budget['max_calls'][stage]: raise RuntimeError('assignments_exceed_stage_call_cap')
        ledger = provider.Ledger(path, budget)
        if backend is None:
            extra = {k: v for k, v in (('clock', clock), ('sleep', sleep)) if v is not None}
            try:
                backend = provider.OpenRouter(ledger, study.provider_config(), opener, **extra)
            except provider.CallFailure as exc:
                raise RuntimeError(exc.category) from None
    billing = lambda: dict(getattr(backend, 'billing', None) or NO_BILLING)
    initial = ledger.transact() if ledger else {}
    rows = state['rows']; reporting_errors = []
    shown = lambda own: study.combine(prior + own) if prior else own
    render.frame(shown([]), everything, stage, accounting=initial, scripted=scripted).save(out / 'initial_frame.png')
    if run: upload(run, out / 'initial_frame.png')

    def base(a):
        r = {k: a[k] for k in study.ROW_KEYS}
        r.update(run=run_name, stage=stage, backend=p['backend'], batch=p['batch'], code=p['code'], source_hash=p['source_hash'],
                 retrieval=dict(a['retrieval']), reference=sim.reference(a['packet']), packet_summary=study.packet_summary(a),
                 status='not_started')
        return r

    def solve(a):
        """One assignment: the handoff is rebuilt and timed, then one call. Returns the row."""
        r = base(a)
        if stop.is_set(): return r
        call_id = f'{p["batch"]}:{a["id"]}'; started = False
        try:
            if time.monotonic() > stop_at:
                halt('stage_deadline'); r['error'] = 'stage_deadline'; return r
            packet, log = sim.handoff(sim.world(a['root'], study.cfg()), a['state'], a['policy'], study.cfg())
            if study.packet_hash(packet) != a['packet_hash'] or {k: log[k] for k in a['retrieval']} != a['retrieval']:
                raise provider.CallFailure('packet_mismatch', dict(SCRIPTED_ACCOUNT))
            r['retrieval'] = dict(a['retrieval'], seconds=log['seconds'])
            log_book.emit('handoff', id=a['id'], state=a['state'], policy=a['policy'], packet_hash=a['packet_hash'], retrieval=r['retrieval'])
            log_book.emit('call_start', id=a['id'], call_id=call_id, packet_hash=a['packet_hash']); started = True
            if scripted:
                full = study.scripted(a); accounting = dict(SCRIPTED_ACCOUNT)
            else:
                full, accounting = backend.call(study.SYSTEM, study.user_text(packet), call_id, study.validate)
            r.update(**study.stored(full), accounting=accounting, work_report=sim.work_report(packet, full),
                     evaluation=study.evaluate(a, full), status='completed')
            log_book.emit('call_response', id=a['id'], call_id=call_id, answer=r['answer'],
                          usage={k: accounting.get(k) for k in ('input_tokens', 'output_tokens', 'actual_usd', 'attempts')})
        except provider.CallFailure as exc:
            r.update(error=exc.category, accounting=exc.accounting)
            log_book.emit('provider_failure' if started else 'not_dispatched', id=a['id'], call_id=call_id, category=exc.category,
                          http_status=exc.accounting.get('http_status'))
            if exc.category == provider.BILLING_STOP:
                halt(provider.BILLING_STOP)          # not an outcome: the row stays not_started, nothing is failed
            else:
                r['status'] = 'failed'
                with control_lock: control['failed'] += 1; failed = control['failed']
                if exc.category in STOP_NOW: halt('integrity_failure:' + exc.category)
                elif strict: halt('invalid_rows')
                elif failed > budget['max_failed']: halt('failed_units_over_limit')
        except Exception as exc:
            r.update(status='failed', error='internal_' + type(exc).__name__)
            log_book.emit('provider_failure' if started else 'not_dispatched', id=a['id'], call_id=call_id, category=r['error'], http_status=None)
            with control_lock: control['failed'] += 1
            halt('integrity_failure:' + r['error'])
        return r

    with (out / 'episodes.jsonl').open('x') as log:
        def record(r):
            r.update(completion_index=len(rows) + 1, elapsed_seconds=time.monotonic() - start,
                     study_accounting=ledger.transact() if ledger else {})
            log.write(json.dumps(r, sort_keys=True) + '\n'); log.flush(); os.fsync(log.fileno()); rows.append(r)
            log_book.emit('terminal', id=r['id'], status=r['status'], error=r.get('error'),
                          outcome=(r.get('evaluation') or {}).get('outcome'))

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
                    t = totals(rows, len(rows)); paused = bool(getattr(backend, '_paused', False))
                    message = ({'message': 'Paused: the provider reports a credit or balance error; the same call is re-sent every '
                                           f'{budget["billing_outage"]["retry_every_seconds"]} s'} if paused else {})
                    run.progress(len(rows), total, episodes=len(rows), invalid=t['invalid'], failed=t['failed'], model_calls=t['model_calls'],
                                 input_tokens=t['input_tokens'], output_tokens=t['output_tokens'], cost_usd=t['cost_usd'], **billing(), **message)
                    if done and (time.monotonic() - last_render > 20 or stop.is_set()):
                        try:
                            render.frame(shown(rows), everything, stage, time.monotonic() - start,
                                         rows[-1]['study_accounting'] or initial, scripted=scripted).save(out / 'progress.png')
                            upload(run, out / 'progress.png')
                        except Exception as exc: reporting_errors.append(type(exc).__name__)
                        last_render = time.monotonic()
                fill()
        for a in assigned[index:]:
            record(base(a))
    log_book.emit('stage_end', rows=len(rows), stop_reason=control['reason']); log_book.close()
    for name in ('episodes.jsonl', 'events.jsonl'):
        with gzip.open(out / (name + '.gz'), 'wb') as f: f.write((out / name).read_bytes())

    summary = summarize(p, rows, total, invariants, probe, control, time.monotonic() - start, initial,
                        ledger.transact() if ledger else {}, billing(), prior, units)
    everyone = shown(rows)
    analysis = analyze.analyze(everyone)
    headline = headline_lines(stage, summary, analysis)
    frames = None
    try:
        final = render.frame(everyone, everything, stage, time.monotonic() - start, (rows[-1]['study_accounting'] if rows else None) or initial,
                             scripted=scripted, headline=headline)
        final.save(out / 'progress.png'); final.save(out / 'final_frame.png')
        frames = render.replay(everyone, everything, out, stage, scripted=scripted, headline=headline)
        journal.replay_html(replay_units(everything, everyone), out / 'replay.html', scripted)
    except Exception as exc: reporting_errors.append('render_' + type(exc).__name__)
    summary.update(reporting_errors=reporting_errors, visualization={'mapping': 'v1', 'replay_frames': frames},
                   headline=analyze.headline(analysis))
    write_json(out / 'summary.json', summary); write_json(out / 'analysis.json', analysis)
    if run:
        for name in ARTIFACTS:
            if (out / name).exists(): upload(run, out / name)
    return summary


def headline_lines(stage, summary, analysis):
    if stage != 'S1' or not analysis.get('cells'):
        gate = summary['qualification_passed']
        return [f'gate: {"passed" if gate == 1 else "FAILED" if gate == 0 else "none"}']
    p = analysis['primary']; g = analysis['utility_guard']['by_policy']
    fmt = lambda v: 'n/a' if v is None else f'{v:+.3f}'
    lines = ['primary (content - metadata):', f' {fmt(p["estimate"])} on {p["roots"]}/{p["assigned_roots"]} roots',
             f' bounds {fmt(p["bounds_all_assigned"][0])} to {fmt(p["bounds_all_assigned"][1])}', 'clean correct:']
    lines += [f' {policy}: {g[policy]["correct"]}/{g[policy]["observed"]}' for policy in sim.POLICIES]
    return lines


def gate_of(stage, rows, invariants, probe):
    """(passed or None, details). S1 has no gate."""
    valid = all(r['status'] == 'completed' for r in rows)
    if stage == 'S0':
        qa = study.qualification([r for r in rows if r['kind'] == 'qualification_a'])
        qb = study.qualification([r for r in rows if r['kind'] == 'qualification_b'])
        return bool(valid and qa['passed'] and qb['passed'] and invariants and invariants['passed']), {'qualification_a': qa, 'qualification_b': qb}
    if stage == 'P0':
        g = study.probe_gate(rows)
        return bool(valid and g['passed']), {'probe': g}
    if stage == 'Q0':
        q = study.qualification(([probe] if probe else []) + rows)
        return bool(valid and probe is not None and q['passed']), {'qualification': q, 'probe_row': probe['id'] if probe else None}
    return None, {}


def summarize(p, rows, total, invariants, probe, control, elapsed, initial, final, billing, prior, units):
    """Everything here except the measured times is recomputable from the saved rows; `chain.py verify` does so."""
    stage = p['stage']; budget = study.design()['budget']; strict = stage in study.STRICT
    t = totals(rows, total); gate, details = gate_of(stage, rows, invariants, probe)
    count = lambda rr, s: sum(r['status'] == s for r in rr)
    everyone = study.combine(list(prior) + rows) if prior else rows
    failed_in_stage = count(everyone, 'failed')
    if strict:
        passed = bool(t['invalid'] == 0 and gate and control['reason'] is None)
        first = next((r.get('error') for r in rows if r['status'] == 'failed'), None)
        if passed: reason = None
        elif control['reason'] and control['reason'] != 'invalid_rows': reason = control['reason']
        elif first: reason = f'invalid_rows:{first}'
        elif t['invalid']: reason = 'incomplete_rows'
        elif invariants is not None and not invariants['passed']:
            reason = 'invariant_failed:' + ','.join(sorted(k for k, ok in invariants['checks'].items() if not ok))
        else: reason = 'qualification_failed'
    else:       # S1: failed calls within the limit do not fail the stage; a stop does
        passed = bool(control['reason'] is None and failed_in_stage <= budget['max_failed'] and count(rows, 'not_started') == 0)
        reason = None if passed else control['reason'] or 'incomplete_rows'
    measured = [r for r in ([probe] if probe else []) + rows if (r.get('accounting') or {}).get('usage_reported')]
    summary = {'params': p, 'experiment': study.EXPERIMENT, 'planned': total, 'started': total - count(rows, 'not_started'),
               'terminal': len(rows), 'graded': count(rows, 'completed'), 'analyzed': count(rows, 'completed'),
               'not_started': count(rows, 'not_started'), **t,
               'errors': sorted({r['error'] for r in rows if r.get('error')}),
               'max_failed': None if strict else budget['max_failed'], 'failed_in_stage': failed_in_stage,
               'stop_reason': control['reason'], 'resumable': bool(stage == 'S1' and control['reason'] == provider.BILLING_STOP),
               **{k: billing.get(k, 0) for k in NO_BILLING},
               'elapsed_seconds': elapsed, 'gate': details, 'invariants': invariants,
               'qualification_passed': None if gate is None else int(gate), 'passed': passed, 'reason': reason,
               'tokens_per_byte_max': study.tokens_per_byte(measured),
               'cost_per_call_usd': (math.fsum(r['accounting']['actual_usd'] for r in measured) / len(measured)) if measured else None,
               'request_bytes_max': max([r['request_bytes'] for r in rows] or [0]),
               'stage_units': {'assigned': len(everyone), **{s: count(everyone, s) for s in ('completed', 'failed', 'not_started')}},
               'continuation': None if units is None else {'units': total, 'earlier_rows': len(prior)},
               'work': work_totals(rows),
               'study_accounting': final, 'initial_study_accounting': initial}
    if stage == 'P0' and rows and rows[0].get('accounting'):
        acc = rows[0]['accounting']       # the raw response metadata of the probe call
        summary['probe_response'] = {
            'response_model': acc.get('response_model'), 'response_provider': acc.get('response_provider'),
            'response_id': acc.get('response_id'), 'finish_reason': acc.get('finish_reason'),
            'reasoning_tokens': acc.get('reasoning_tokens'), 'latency_seconds': acc.get('latency_seconds'),
            'provider_reported_usd': acc.get('provider_reported_usd'), 'computed_usd': acc.get('computed_usd'),
            'actual_usd': acc.get('actual_usd'), 'reserved_usd': acc.get('reserved_usd'),
            'input_tokens': acc.get('input_tokens'), 'output_tokens': acc.get('output_tokens'),
            'request_bytes': acc.get('request_bytes'), 'tokens_per_byte': study.tokens_per_byte(rows),
            'http_status': acc.get('http_status'), 'error': rows[0].get('error')}
    return summary


def hub_metrics(summary):
    m = {k: summary[k] for k in HUB_KEYS}
    for k in ('qualification_passed', 'tokens_per_byte_max', 'cost_per_call_usd', 'max_output_tokens_per_call'):
        if summary.get(k) is not None: m[k] = summary[k]
    m.update(summary.get('headline') or {})
    for k in ('work_malformed', 'listing_matches_message', 'follows_from_own_listing'):
        m[k] = summary['work'][k]
    for k, v in (summary.get('probe_response') or {}).items():       # the hub stores numbers; the names go into the run's message
        if isinstance(v, (int, float)) and not isinstance(v, bool): m['probe_' + k] = v
    return m


def execute(p, out, run=None, backend=None, deadline=None, opener=None, units=None, prior_rows=None, sr=None, clock=None, sleep=None,
            probe_row=None):
    """Run one stage. Returns the summary when the stage passed; raises StageFailed when it ended
    recorded but not passed, or when it could not start. The hub run is closed in every case."""
    state = {'rows': [], 'total': 0}
    try:
        summary = run_stage(p, out, run, backend, deadline, state, opener, units, prior_rows, sr, clock, sleep, probe_row)
    except Exception as exc:
        reason = str(exc) if isinstance(exc, RuntimeError) and str(exc).replace('_', '').isalnum() else 'internal_' + type(exc).__name__
        if run:
            t = totals(state['rows'], max(state['total'], len(state['rows'])))
            t['invalid'] = max(1, t['invalid'])
            metrics = {k: t[k] for k in HUB_KEYS if k in t}
            if p.get('stage') != 'S1': metrics['qualification_passed'] = 0
            run.fail(f'{p.get("stage")}: {reason}; rows preserved', **metrics)
        raise StageFailed(reason) from exc
    stage = summary['params']['stage']; pr = summary.get('probe_response')
    message = (f'{stage}: {summary["graded"]}/{summary["planned"]} valid, {summary["failed"]} failed'
               + (f' (limit {summary["max_failed"]})' if summary['max_failed'] is not None else '')
               + f', {summary["not_started"]} not started, {summary["model_calls"]} calls, USD {summary["cost_usd"]:.4f}'
               + (f', {summary["billing_pauses"]} billing pause(s) of {summary["billing_pause_seconds"]:.0f} s' if summary['billing_pauses'] else '')
               + (f'; probe response: model {pr.get("response_model")}, provider {pr.get("response_provider")}, id {pr.get("response_id")}, '
                  f'finish {pr.get("finish_reason")}, reasoning tokens {pr.get("reasoning_tokens")}' if pr else ''))
    if not summary['passed']:
        metrics = hub_metrics(summary)
        if stage != 'S1': metrics['qualification_passed'] = 0
        if run: run.fail(message + f'; {summary["reason"]}; rows preserved', **metrics)
        raise StageFailed(summary['reason'])
    if run: run.done(message=message, **hub_metrics(summary))
    return summary


def main():
    ap = argparse.ArgumentParser(description='Offline scripted stage only. Paid stages run through chain.py and its gates.')
    ap.add_argument('--stage', choices=['S0'], required=True); ap.add_argument('--attempt', required=True)
    a = ap.parse_args()
    if not a.attempt.replace('-', '').isalnum(): raise SystemExit('Offline S0 requires a fresh attempt name (letters, digits, hyphens)')
    directory = study.results_dir() / a.attempt
    try:
        summary = execute(study.params('S0'), directory)
    except StageFailed as exc:
        print(json.dumps({'stage': 'S0', 'passed': False, 'reason': str(exc), 'directory': str(directory)})); sys.exit(3)
    inv = summary['invariants']
    print(json.dumps({'stage': 'S0', 'passed': summary['passed'], 'planned': summary['planned'], 'graded': summary['graded'],
                      'invalid': summary['invalid'], 'model_calls': summary['model_calls'], 'cost_usd': summary['cost_usd'],
                      'qualification_passed': summary['qualification_passed'],
                      'qualification_a': {k: summary['gate']['qualification_a'][k] for k in ('fixtures', 'valid', 'supported', 'passed')},
                      'qualification_b': {k: summary['gate']['qualification_b'][k] for k in ('fixtures', 'valid', 'supported', 'passed')},
                      'invariants_passed': inv['passed'], 'invariant_checks': len(inv['checks']),
                      'reference_primary': inv['control_table']['reference']['primary'],
                      'control_primaries': {k: v['primary'] for k, v in inv['control_table'].items()},
                      'sizes': inv['sizes'], 'elapsed_seconds': round(summary['elapsed_seconds'], 2), 'directory': str(directory)}))


if __name__ == '__main__':
    main()
