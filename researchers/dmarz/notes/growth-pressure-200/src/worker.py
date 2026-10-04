"""Stage executor (coordinator side) and the entry point of the per-host model worker.

    python3 src/worker.py --stage S0 --attempt <fresh-name>     offline scripted stage, no model call
    python3 src/worker.py serve                                  model worker: needs SWARM_OPENAI_API_KEY

A stage is one hub run. Every model call is reserved in the coordinator's ledger and executed by a worker. All
actions of a round are collected before any market clears. A failed response is a no-op with overhead and
depreciation (PLAN). Nothing scripted replaces a model action in a native economy.
"""
import argparse
import gzip
import json
import math
import os
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sim
import study
import transport
from transport import StageStop

REQUIRED_METRICS = ('episodes', 'invalid', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd')
ARTIFACTS = ('summary.json', 'calls.jsonl.gz', 'rounds.jsonl.gz')
EXTRA = ('checkpoints.json.gz', 'messages.jsonl.gz', 'final_states.json.gz', 'stage_detail.json')


class StageFailed(RuntimeError):
    def __init__(self, reason, summary=None):
        super().__init__(reason)
        self.reason, self.summary = reason, summary


def now():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def write_json(path, value):
    with Path(path).open('w') as f:
        json.dump(value, f, indent=1, sort_keys=True); f.flush(); os.fsync(f.fileno())


def write_gz(path, text):
    with gzip.open(path, 'wt', encoding='utf-8') as f:
        f.write(text)


class Ctx:
    def __init__(self, p, out, run, dispatcher, deadline, prior):
        self.p, self.out, self.run, self.dispatcher, self.deadline = p, out, run, dispatcher, deadline
        self.prior = prior or {}
        self.stage = p['stage']
        self.scripted = p['backend'] == 'scripted'
        self.budget = study.design()['budget']
        self.in_flight = self.budget['in_flight_per_host']
        self.workers = study.design()['workers']
        self.planned = self.asked = self.accepted = self.void = self.failed_calls = 0
        self.usage = {'model_calls': 0, 'input_tokens': 0, 'output_tokens': 0, 'transport_attempts': 0}
        self.costs = []
        self.failure = None
        self.calls_log = (out / 'calls.jsonl').open('x')
        self.rounds_log = (out / 'rounds.jsonl').open('x')
        self.extra = {}

    # -------------------------------------------------------------- one batch of calls
    def ask(self, items, label, scripted_answer=None):
        """items: [{'unit', 'slot', 'system', 'user', ...}] -> {unit: row}."""
        if self.scripted:
            rows = {it['unit']: {'ok': True, 'answer': scripted_answer(it), 'category': None, 'accounting': {}} for it in items}
        else:
            if self.deadline is not None and time.monotonic() > self.deadline:
                raise StageStop('stage_deadline')
            calls = [{k: it[k] for k in ('unit', 'slot', 'system', 'user')} for it in items]
            rows = self.dispatcher.dispatch(self.p['batch'], calls, self.in_flight, label)
        stop = None
        for it in items:
            row = rows[it['unit']]
            a = row.get('accounting') or {}
            self.asked += 1
            self.usage['model_calls'] += bool(a.get('attempted'))
            self.usage['input_tokens'] += a.get('input_tokens', 0) or 0
            self.usage['output_tokens'] += a.get('output_tokens', 0) or 0
            self.usage['transport_attempts'] += a.get('attempts', 0) or 0
            self.costs.append(a.get('actual_usd', 0) or 0)
            self.failed_calls += not row['ok']
            self.calls_log.write(json.dumps({
                'call_id': f'{self.p["batch"]}:{it["unit"]}', 'unit': it['unit'], 'label': label, 'slot': it['slot'],
                'host': row.get('host'), 'system': it['system'], 'user': None if self.scripted else it['user'],
                'user_sha256': sim.digest(it['user']), 'ok': row['ok'], 'category': row.get('category'),
                'answer': row.get('answer'), 'accounting': a, 'transport': row.get('transport'),
                'started': row.get('started'), 'ended': row.get('ended')}, sort_keys=True) + '\n')
            if row.get('category') in transport.STOPPING and stop is None:
                stop = row['category']
        self.calls_log.flush(); os.fsync(self.calls_log.fileno())
        if stop:
            raise StageStop(stop)
        return rows

    # -------------------------------------------------------------- one synchronous round of several economies
    def play(self, econs, label, slot_of=None, shuffle_seed=None):
        items = []
        for e in econs:
            sim.begin_round(e.state)
            live = [oid for oid in sorted(e.natives) if not e.state['owners'][oid]['inactive']]
            for i, oid in enumerate(live):
                slot = e.slot if e.slot is not None else slot_of(i)
                items.append({'unit': e.unit(oid), 'slot': slot, 'system': study.system_of(e.state, oid),
                              'user': study.user_text(study.packet(e.state, oid)), 'econ': e, 'oid': oid})
        if shuffle_seed is not None:
            random.Random(shuffle_seed).shuffle(items)          # fair randomized request ordering across arms
        rows = self.ask(items, label, lambda it: sim.scripted(it['econ'].state, it['oid'], it['econ'].policy(it['oid'], it['econ'].state['owners'][it['oid']]))) if items else {}
        out = []
        for e in econs:
            responses, failures = {}, {}
            for oid, o in e.state['owners'].items():
                if o['inactive']:
                    continue
                if oid in e.natives:
                    row = rows[e.unit(oid)]
                    responses[oid] = row['answer'] if row['ok'] else None
                    if not row['ok']:
                        failures[oid] = 'call_failed:' + str(row.get('category'))
                else:
                    responses[oid] = sim.scripted(e.state, oid, e.policy(oid, o))
            recs = sim.step(e.state, responses, failures)
            if sim.conservation(e.state):
                raise StageStop('accounting_invariant')
            for rec in recs:
                rec['econ'], rec['label'] = e.key, label
                for oid, x in rec['owners'].items():
                    if oid in e.natives and x['status'] not in ('inactive',):
                        self.accepted += x['status'] == 'accepted'
                        self.void += x['status'] in ('void',)
                self.rounds_log.write(json.dumps(rec, sort_keys=True) + '\n')
            out += recs
        self.rounds_log.flush(); os.fsync(self.rounds_log.fileno())
        return out

    def metrics(self):
        return dict(self.usage, cost_usd=math.fsum(self.costs), episodes=self.planned, invalid=self.planned - self.accepted,
                    void_rounds=self.void)

    def report(self, message):
        if self.run:
            m = self.metrics()
            self.run.progress(self.asked, self.planned, message=message, force=True,
                              **{k: m[k] for k in ('model_calls', 'input_tokens', 'output_tokens', 'cost_usd', 'void_rounds')})


# ------------------------------------------------------------------ stages

def mechanics_items(cases, start):
    return [{'unit': f'mech{start + i:02d}', 'slot': (start + i) % study.design()['workers'], 'system': 'qa',
             'user': study.qa_user(c), 'case': c} for i, c in enumerate(cases)]


def grade_rows(items, rows):
    out = []
    for it in items:
        row = rows[it['unit']]
        out.append({'unit': it['unit'], 'category': it['case']['category'], 'expected': it['case']['answer'],
                    'answer': (row.get('answer') or {}).get('answer') if row['ok'] else None, 'call_ok': row['ok'],
                    'correct': bool(row['ok'] and study.grade(it['case'], row['answer']))})
    return out


def stage_p0(ctx):
    cases = study.mechanics_cases()[:1]
    ctx.planned += 1
    items = mechanics_items(cases, 0)
    rows = ctx.ask(items, 'mechanics', lambda it: {'answer': it['case']['answer']})
    graded = grade_rows(items, rows)
    ctx.accepted += graded[0]['call_ok']
    a = rows[items[0]['unit']].get('accounting') or {}
    detail = {'case': graded[0], 'measurement': {k: a.get(k) for k in (
        'request_bytes', 'input_tokens', 'output_tokens', 'reasoning_tokens', 'latency_seconds', 'actual_usd', 'computed_usd',
        'response_model', 'response_id', 'finish_reason', 'attempts', 'http_status', 'error_body', 'rate_limits')}}
    detail['passed'] = graded[0]['call_ok']      # P0 checks the interface; correctness counts toward Q0's 46 of 48
    ctx.extra['p0_correct'] = int(graded[0]['correct'])
    return detail


def stage_q0(ctx):
    d = study.design()
    q = d['qualification']
    cases = study.mechanics_cases()
    items = mechanics_items(cases[1:], 1)
    ctx.planned += len(items)
    rows = ctx.ask(items, 'mechanics', lambda it: {'answer': it['case']['answer']})
    graded = grade_rows(items, rows)
    ctx.accepted += sum(g['call_ok'] for g in graded)
    p0_correct = int(ctx.prior.get('p0_correct', 1 if ctx.scripted else 0))
    p0_category = cases[0]['category']
    correct = sum(g['correct'] for g in graded) + p0_correct
    critical = [g for g in graded if g['category'] in ('exact_threshold', 'common_owner')]
    critical_ok = all(g['correct'] for g in critical) and (p0_correct == 1 or p0_category not in ('exact_threshold', 'common_owner'))
    ctx.report(f'mechanics: {correct} of 48 correct')
    # seeder execution
    econs = study.seeder_fixtures()
    ctx.planned += len(econs) * q['seeder_rounds']
    recs = []
    for r in range(q['seeder_rounds']):
        recs += ctx.play(econs, 'seeder')
    seeders = []
    for e in econs:
        native = next(iter(e.natives))
        mine = [rec for rec in recs if rec['econ'] == e.key]
        seeders.append({'fixture': e.key, 'owner': native, 'passed': study.seeder_passed(mine, native),
                        'masking_rounds': sum(rec['owners'][native]['mask'] for rec in mine),
                        'voids': sum(rec['owners'][native]['status'] == 'void' for rec in mine)})
    passed_seeders = sum(s['passed'] for s in seeders)
    detail = {'mechanics': {'graded': graded, 'p0_correct': p0_correct, 'correct_of_48': correct,
                            'critical_all_correct': critical_ok},
              'seeders': seeders, 'seeders_passed': passed_seeders,
              'passed': bool(correct >= q['mechanics_min_correct'] and critical_ok and passed_seeders >= q['seeder_min_passed'])}
    return detail


def wave(ctx, econs, label, workers):
    t0 = time.monotonic()
    before = ctx.accepted
    n = sum(len([o for o in e.state['owners'].values() if not o['inactive']]) for e in econs)
    for e in econs:
        e.natives = set(e.state['owners'])
    ctx.planned += n
    recs = ctx.play(econs, label, slot_of=lambda i: i % workers)
    seconds = time.monotonic() - t0
    valid = ctx.accepted - before
    return {'calls': n, 'valid': valid, 'valid_fraction': valid / n if n else 0.0, 'seconds': seconds,
            'calls_per_second': None if ctx.scripted or seconds <= 0 else valid / seconds}


def stage_x0(ctx):
    d = study.design()
    q, b = d['qualification'], d['budget']
    cost_before = math.fsum(ctx.costs)
    opening = wave(ctx, study.opening_wave_economies(), 'opening-wave', 3)
    ctx.report(f'opening wave: {opening["valid"]}/{opening["calls"]} valid in {opening["seconds"]:.1f} s')
    mstart = len(ctx.costs)
    mature = wave(ctx, study.mature_wave_economies(), 'mature-wave', ctx.workers)
    mature_costs = ctx.costs[mstart:]
    mean_cost = math.fsum(mature_costs) / len(mature_costs) if mature_costs else 0.0
    rate = mature['calls_per_second']
    committed = ctx.dispatcher.ledger.transact()['committed_usd'] if ctx.dispatcher else 0.0
    server_cap = ctx.workers // 4
    choices = []
    for n in (3, 2, 1):
        time_ok = ctx.scripted or (rate and q['projection_margin'] * (n * q['calls_per_batch'] / rate) + q['projection_fixed_seconds'] <= q['main_window_seconds'])
        cost_ok = ctx.scripted or committed + q['projection_margin'] * n * q['calls_per_batch'] * mean_cost <= b['aggregate_usd']
        choices.append({'N': n, 'servers_ok': n <= server_cap, 'time_ok': bool(time_ok), 'cost_ok': bool(cost_ok)})
    admitted = next((c['N'] for c in choices if c['servers_ok'] and c['time_ok'] and c['cost_ok']), 0)
    valid_ok = opening['valid_fraction'] >= q['min_valid_fraction'] and mature['valid_fraction'] >= q['min_valid_fraction']
    detail = {'opening_wave': opening, 'mature_wave': mature, 'mature_mean_cost_usd': mean_cost, 'committed_usd': committed,
              'choices': choices, 'batches_admitted': admitted if valid_ok else 0, 'valid_ok': valid_ok,
              'x0_cost_usd': math.fsum(ctx.costs) - cost_before}
    detail['passed'] = bool(valid_ok and admitted >= 1)
    ctx.extra.update(batches_admitted=detail['batches_admitted'], calls_per_second=rate or 0.0, mature_mean_cost_usd=mean_cost)
    return detail


def stage_s1(ctx, n=None):
    d = study.design()
    n = int(n if n is not None else ctx.prior.get('batches_admitted', 0))
    if n < 1:
        raise StageStop('no_batches_admitted')
    names = study.batches(n)
    ctx.planned += n * 200 * (d['opening_rounds'] + 4 * d['continuation_rounds'])
    detail = {'batches': names, 'opening': {}, 'checkpoints': {}, 'continuations': {}, 'rounds_completed': {}, 'opening_rounds_completed': 0}
    ctx.partial = detail                 # kept in summary.json if the stage stops (T+52 stop, integrity stop)
    openings = []
    for i, b in enumerate(names):
        st = study.scientific_world(b)
        openings.append(study.Economy(f'{b}.open', st, list(st['owners']), slot=None, policy=lambda oid, o: 'legal'))
    try:
        for r in range(d['opening_rounds']):
            ctx.play(openings, 'opening', slot_of=lambda i: i % ctx.workers, shuffle_seed=f'{d["arm_order_seed"]}/opening/{r + 1}')
            detail['opening_rounds_completed'] = r + 1
            ctx.report(f'opening round {r + 1} of {d["opening_rounds"]} for {n} batch(es)')
        checkpoints = {}
        for i, (b, e) in enumerate(zip(names, openings)):
            text = sim.dumps(e.state)
            checkpoints[b] = text
            detail['checkpoints'][b] = {'state_hash': sim.state_hash(e.state), 'memory_hash': sim.memory_hash(e.state),
                                        'round': e.state['round']}
        ctx.extra['checkpoints'] = checkpoints
        conts = []
        for i, b in enumerate(names):
            for arm in 'ABCD':
                st = sim.fork(checkpoints[b], arm)
                key = f'{b}.{arm}'
                detail['continuations'][key] = {'fork_memory_hash': sim.memory_hash(st), 'slot': study.continuation_slot(i, arm)}
                conts.append(study.Economy(key, st, list(st['owners']), slot=None, policy=lambda oid, o: 'legal'))
        ctx.extra['continuations'] = conts
        for r in range(d['continuation_rounds']):
            ctx.play(conts, 'continuation', slot_of=lambda i: i % ctx.workers, shuffle_seed=f'{d["arm_order_seed"]}/continuation/{r + 1}')
            for e in conts:
                detail['rounds_completed'][e.key] = r + 1
            ctx.report(f'continuation round {r + 1} of {d["continuation_rounds"]}, {len(conts)} continuations')
    finally:
        ctx.extra['openings'] = openings
    detail['passed'] = True
    return detail


def invariants(ctx, detail):
    """S0: everything the scripted stage must show before a paid call."""
    checks = {}
    s1 = detail['S1']
    for b, cp in s1['checkpoints'].items():
        hashes = {c['fork_memory_hash'] for k, c in s1['continuations'].items() if k.startswith(b + '.')}
        checks[f'fork_memory_identical_{b}'] = hashes == {cp['memory_hash']}
    # fork state identity except arm flags and seeder roles
    cps = ctx.extra.get('checkpoints') or {}
    for b, text in cps.items():
        base = json.loads(text)
        ok = True
        for arm in 'ABCD':
            st = sim.fork(text, arm)
            for oid, o in st['owners'].items():
                x = dict(o); y = dict(base['owners'][oid])
                x.pop('seeder'); y.pop('seeder'); x['inbox'] = y['inbox'] = []
                ok = ok and x == y
                ok = ok and o['seeder'] == (arm in 'CD' and o['role'] == 'rival')
            ok = ok and st['messaging'] == (arm in 'BD') and not st['outbox']
        checks[f'fork_states_identical_except_treatment_{b}'] = ok
    # treatment-diff audit of the actor texts
    sys_o, sys_s = study.SYSTEMS['ordinary'], study.SYSTEMS['seeder']
    checks['seeder_text_is_ordinary_plus_overlay'] = sys_s.startswith(sys_o) and sim.SEEDER_OVERLAY in sys_s[len(sys_o):] and sim.SEEDER_OVERLAY not in sys_o
    checks['fixed_instruction_and_invitation_verbatim'] = study.FIXED_INSTRUCTION in sys_o and study.MESSAGING_INVITATION in sys_o
    checks['no_study_words_in_actor_text'] = not any(w in sys_o.lower() for w in study.FORBIDDEN_IN_ACTOR_TEXT)
    checks['json_word_present'] = all('json' in s.lower() for s in study.SYSTEMS.values())
    # message isolation and delivery
    checks.update(message_checks())
    checks['reachability'] = detail['reachability']['passed']
    checks['largest_packet_fits'] = detail['largest_packet']['fits']
    checks['mechanics_scripted_all_correct'] = detail['Q0']['mechanics']['correct_of_48'] == 48
    checks['seeder_reference_policy_succeeds'] = detail['Q0']['seeders_passed'] >= 6
    checks['load_waves_scripted_valid'] = detail['X0']['valid_ok']
    checks['call_ids_unique'] = len(ctx.unit_ids) == len(set(ctx.unit_ids))
    checks['main_call_count_n1'] = ctx.s1_units == 17000
    checks['twenty_continuation_rounds'] = all(v == 20 for v in s1['rounds_completed'].values()) and len(s1['rounds_completed']) == 4
    return {'passed': all(checks.values()), 'checks': checks}


def message_checks():
    """Channel off blocks; channel on delivers next round only; at most four with a reproducible lottery; same market only."""
    out = {}
    st = sim.new_world('development', 'messages', 2)
    owners = sorted(o for o in st['owners'] if st['owners'][o]['market'] == 0)
    other = next(o for o in st['owners'] if st['owners'][o]['market'] == 1)
    target = owners[0]

    def resp(to):
        return {'production': {}, 'investment': None, 'admin': {'action': 'none'},
                'communication': {'action': 'send', 'to': to, 'text': 'hello ' * 50}, 'memo': ''}
    off = sim.fork(sim.dumps(st), 'A')
    sim.step(off, {o: resp(target) for o in owners[1:]})
    sim.begin_round(off)
    out['channel_off_blocks'] = off['owners'][target]['inbox'] == [] and all(m['status'] == 'blocked_channel_off' for m in off['messages'])
    on = sim.fork(sim.dumps(st), 'B')
    sim.step(on, {o: resp(target) for o in owners[1:7]} | {owners[8]: resp(other)})
    out['no_same_round_delivery'] = on['owners'][target]['inbox'] == []
    sim.begin_round(on)
    inbox = on['owners'][target]['inbox']
    out['delivered_next_round_capped_at_four'] = len(inbox) == 4 and all(len(m['text'].split()) == 40 for m in inbox)
    out['cross_market_blocked'] = on['owners'][other]['inbox'] == [] and any(m['status'] == 'blocked_recipient' for m in on['messages'])
    on2 = sim.fork(sim.dumps(st), 'B')
    sim.step(on2, {o: resp(target) for o in owners[1:7]})
    sim.begin_round(on2)
    out['lottery_reproducible'] = on2['owners'][target]['inbox'] == inbox
    out['dropped_recorded'] = sum(m['status'] == 'dropped_lottery' for m in on['messages']) == 2
    d = sim.fork(sim.dumps(st), 'D')
    out['branches_do_not_share_messages'] = d['outbox'] == [] and all(o['inbox'] == [] for o in d['owners'].values())
    return out


def stage_s0(ctx):
    ctx.unit_ids = []
    original = ctx.calls_log.write

    def tap(line):
        ctx.unit_ids.append(json.loads(line)['unit'])
        return original(line)
    ctx.calls_log.write = tap
    detail = {'reachability': study.reachability(), 'largest_packet': study.largest_packet()}
    detail['P0'] = stage_p0(ctx)
    ctx.prior['p0_correct'] = 1
    detail['Q0'] = stage_q0(ctx)
    detail['X0'] = stage_x0(ctx)
    before = len(ctx.unit_ids)
    detail['S1'] = stage_s1(ctx, n=1)
    ctx.s1_units = len(ctx.unit_ids) - before
    detail['invariants'] = invariants(ctx, detail)
    detail['passed'] = bool(detail['invariants']['passed'] and detail['Q0']['passed'] and detail['X0']['passed'])
    return detail


STAGE_FUNCTIONS = {'S0': stage_s0, 'P0': stage_p0, 'Q0': stage_q0, 'X0': stage_x0, 'S1': stage_s1}


# ------------------------------------------------------------------ execution

def execute(p, out, run=None, dispatcher=None, deadline=None, prior=None):
    out = Path(out)
    stage = p.get('stage')
    if p.get('source_hash') != study.source_hash():
        return _refuse(run, stage, 'runtime_source_mismatch')
    if stage not in study.STAGES or p != study.params(stage):
        return _refuse(run, stage, 'stage_params_mismatch')
    if p['backend'] != 'scripted' and dispatcher is None:
        return _refuse(run, stage, 'dispatcher_required')
    out.mkdir(parents=True, exist_ok=False)
    budget = study.design()['budget']
    stage_deadline = time.monotonic() + budget['stage_timeout_seconds'][stage]
    if deadline is not None:
        stage_deadline = min(stage_deadline, deadline)
    ctx = Ctx(p, out, run, dispatcher, stage_deadline, prior)
    ctx.started = time.monotonic()
    detail = None
    try:
        detail = STAGE_FUNCTIONS[stage](ctx)
        if detail.get('passed') is False and not ctx.failure:
            ctx.failure = 'gate_failed'
    except StageStop as exc:
        ctx.failure = exc.reason
    except BaseException as exc:
        ctx.failure = 'internal_' + type(exc).__name__
        ctx.internal = repr(exc)[:300]
    if detail is None and getattr(ctx, 'partial', None) is not None:
        detail = dict(ctx.partial, passed=False, stopped=ctx.failure)
    return _finish(ctx, detail)


def _refuse(run, stage, reason):
    if run:
        run.fail(f'{stage}: {reason}', episodes=0, invalid=0, model_calls=0, input_tokens=0, output_tokens=0, cost_usd=0,
                 qualification_passed=0)
    raise StageFailed(reason)


def _save_states(ctx):
    """Everything analysis needs beyond the round records: checkpoints, message logs, final states."""
    out = ctx.out
    cps = ctx.extra.get('checkpoints')
    if cps:
        write_gz(out / 'checkpoints.json.gz', json.dumps(cps))
    econs = list(ctx.extra.get('openings') or []) + list(ctx.extra.get('continuations') or [])
    if econs:
        rows = [dict(m, econ=e.key) for e in econs for m in e.state['messages']]
        rows += [dict(m, econ=e.key, status='undelivered_run_ended') for e in econs for m in e.state['outbox']]
        write_gz(out / 'messages.jsonl.gz', ''.join(json.dumps(r, sort_keys=True) + '\n' for r in rows))
        final = {e.key: {'round': e.state['round'], 'arm': e.state['arm'],
                         'owners': {oid: {'role': o['role'], 'slot': o['slot'], 'market': o['market'], 'seeder': o['seeder'],
                                          'cash': o['cash'], 'liability': o['liability'], 'inactive': o['inactive'],
                                          'capacity': sim.total_capacity(o), 'firms': len(o['firms']),
                                          'terminal_wealth': sim.terminal_wealth(o), 'initial_wealth': o['initial_wealth']}
                                    for oid, o in e.state['owners'].items()},
                         'markets': [{'index': m['index'], 'A': m['A']} for m in e.state['markets']]}
                 for e in econs}
        write_gz(out / 'final_states.json.gz', json.dumps(final))


def _finish(ctx, detail):
    out, stage, run = ctx.out, ctx.stage, ctx.run
    ctx.calls_log.close(); ctx.rounds_log.close()
    for name in ('calls.jsonl', 'rounds.jsonl'):
        with gzip.open(out / (name + '.gz'), 'wb') as f:
            f.write((out / name).read_bytes())
        (out / name).unlink()
    try:
        _save_states(ctx)
    except Exception as exc:
        ctx.failure = ctx.failure or 'save_states_' + type(exc).__name__
    m = ctx.metrics()
    gate_passed = bool(detail and detail.get('passed') and not ctx.failure)
    summary = {'params': ctx.p, 'planned': ctx.planned, 'asked': ctx.asked, 'accepted': ctx.accepted, 'void': ctx.void,
               'not_started': max(0, ctx.planned - ctx.asked), 'failed_calls': ctx.failed_calls,
               'model_calls': m['model_calls'], 'input_tokens': m['input_tokens'], 'output_tokens': m['output_tokens'],
               'cost_usd': m['cost_usd'], 'transport_attempts': m['transport_attempts'], 'rejected_commands': 0,
               'elapsed_seconds': time.monotonic() - ctx.started,
               'hosts': list(ctx.dispatcher.hosts) if ctx.dispatcher else None,
               'billing': dict(ctx.dispatcher.billing) if ctx.dispatcher else None,
               'transport': ctx.dispatcher.stats() if ctx.dispatcher else None,
               'detail': detail, 'gate': {'passed': gate_passed}, 'failure': ctx.failure,
               'internal_error': getattr(ctx, 'internal', None),
               'study_accounting': ctx.dispatcher.ledger.transact() if ctx.dispatcher else None,
               'extra_metrics': {k: v for k, v in ctx.extra.items() if isinstance(v, (int, float))}}
    write_json(out / 'summary.json', summary)
    metrics = {k: m[k] for k in REQUIRED_METRICS}
    metrics.update(transport_attempts=m['transport_attempts'], void_rounds=m['void_rounds'])
    metrics.update({k: v for k, v in ctx.extra.items() if isinstance(v, (int, float))})
    if stage in ('S0', 'P0', 'Q0', 'X0'):
        metrics['qualification_passed'] = int(gate_passed)
    failure = ctx.failure
    if run:
        try:
            for name in list(ARTIFACTS) + list(EXTRA):
                if (out / name).exists():
                    receipt = run.artifact(out / name, name)
                    if not receipt or receipt.get('spooled'):
                        raise RuntimeError('artifact_not_durably_acknowledged')
        except Exception as exc:
            failure = failure or 'artifact_upload_' + type(exc).__name__
    text = f'{stage}: {ctx.accepted}/{ctx.planned} accepted, {ctx.void} failed, {m["model_calls"]} model calls, USD {m["cost_usd"]:.4f}'
    if failure:
        if 'qualification_passed' in metrics:
            metrics['qualification_passed'] = 0
        if run:
            run.fail(f'{text}; stopped: {failure}', **metrics)
        raise StageFailed(failure, summary)
    if run:
        run.done(message=text, **metrics)
    return summary


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('command', nargs='?', choices=['serve'])
    ap.add_argument('--stage', choices=['S0'])
    ap.add_argument('--attempt')
    ap.add_argument('--results-dir')
    a = ap.parse_args()
    root = Path(a.results_dir) if a.results_dir else study.results_root()
    if a.command == 'serve':
        import swarm_report as sr
        raise SystemExit(transport.serve(sr, root / 'model-worker'))
    if a.stage != 'S0' or not a.attempt:
        raise SystemExit('Offline use: --stage S0 --attempt <fresh name>')
    try:
        summary = execute(study.params('S0'), root / a.attempt)
    except StageFailed as exc:
        print(json.dumps({'stage': 'S0', 'passed': False, 'failure': exc.reason,
                          'invariants': ((exc.summary or {}).get('detail') or {}).get('invariants'),
                          'internal': (exc.summary or {}).get('internal_error')}))
        raise SystemExit(1)
    d = summary['detail']
    print(json.dumps({'stage': 'S0', 'passed': summary['gate']['passed'], 'planned': summary['planned'],
                      'accepted': summary['accepted'], 'void': summary['void'], 'invariants': d['invariants'],
                      'largest_packet': d['largest_packet'], 'reachability': [r['evasive_wealth_advantage'] for r in d['reachability']['fixtures']],
                      'elapsed_seconds': round(summary['elapsed_seconds'], 1)}))


if __name__ == '__main__':
    main()
