"""Durable budget and call ledger for the whole study.

One JSONL file shared by every stage and process, appended under an exclusive file lock with
fsync. Before a request is sent the controller reserves its worst-case cost; after the response
the reservation is replaced by the billed amount. A call whose outcome is unknown keeps its full
reservation for ever. Committed spend = billed amounts + open reservations, and a reservation is
refused if it would take committed spend past a cap.

Two pools are capped separately (plan section 6): 'public' covers the first pass, discussion and
public final; 'aux' covers the auxiliary private final. A private probe can never use calls or
dollars reserved for the public decision.
"""
import fcntl
import json
import os
import threading
import time
from pathlib import Path

POOLS = ('public', 'aux')


class BudgetError(Exception):
    def __init__(self, category):
        super().__init__(category)
        self.category = category


class Ledger:
    def __init__(self, path, caps, durable=True):
        """caps: {'study_micro_usd', 'pool_micro_usd': {pool: n},
                  'stages': {stage: {'public': calls, 'aux': calls, 'attempts': transport attempts}}}"""
        self.path = Path(path)
        self.caps = caps
        self.durable = durable
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self._thread_lock = threading.Lock()
        self._offset = 0
        self._calls = {}       # call_id -> [stage, pool, reserved, state, billed]
        self._attempts = {}    # stage -> transport attempts
        self._count = {}       # (stage, pool) -> logical calls
        self._committed = {p: 0 for p in POOLS}   # billed amounts + open and unknown reservations
        self._billed = 0
        self._unknown = 0
        self._tokens = {'input': 0, 'output': 0}

    def _apply(self, e):
        kind = e['type']
        if kind == 'reserve':
            self._calls[e['call_id']] = [e['stage'], e['pool'], e['micro_usd'], 'open', 0]
            self._count[(e['stage'], e['pool'])] = self._count.get((e['stage'], e['pool']), 0) + 1
            self._committed[e['pool']] += e['micro_usd']
        elif kind == 'attempt':
            self._attempts[e['stage']] = self._attempts.get(e['stage'], 0) + 1
        elif kind == 'settle':
            call = self._calls[e['call_id']]
            self._committed[call[1]] += e['micro_usd'] - call[2]
            self._billed += e['micro_usd']
            call[3], call[4] = 'settled', e['micro_usd']
            self._tokens['input'] += e.get('input_tokens', 0)
            self._tokens['output'] += e.get('output_tokens', 0)
        elif kind == 'unknown':
            self._calls[e['call_id']][3] = 'unknown'
            self._unknown += 1

    def _check(self, e):
        kind = e['type']
        if kind == 'reserve':
            if e['call_id'] in self._calls:
                raise BudgetError('duplicate_call_refused')
            if e['pool'] not in POOLS:
                raise BudgetError('unknown_pool')
            stage_caps = self.caps['stages'].get(e['stage'])
            if stage_caps is None:
                raise BudgetError('stage_not_budgeted')
            if self._count.get((e['stage'], e['pool']), 0) >= stage_caps[e['pool']]:
                raise BudgetError('call_budget_exhausted')
            if self._committed[e['pool']] + e['micro_usd'] > self.caps['pool_micro_usd'][e['pool']]:
                raise BudgetError('dollar_budget_exhausted')
            if sum(self._committed.values()) + e['micro_usd'] > self.caps['study_micro_usd']:
                raise BudgetError('dollar_budget_exhausted')
        elif kind == 'attempt':
            if e['call_id'] not in self._calls:
                raise BudgetError('attempt_without_reservation')
            stage_caps = self.caps['stages'].get(e['stage'])
            if stage_caps is None or self._attempts.get(e['stage'], 0) >= stage_caps['attempts']:
                raise BudgetError('attempt_budget_exhausted')
        elif kind in ('settle', 'unknown'):
            call = self._calls.get(e['call_id'])
            if call is None or call[3] != 'open':
                raise BudgetError('settle_without_open_reservation')

    def _transact(self, event=None):
        with self._thread_lock:
            with self.path.open('a+', encoding='utf-8') as f:
                os.chmod(self.path, 0o600)
                fcntl.flock(f, fcntl.LOCK_EX)
                f.seek(self._offset)
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if not line.endswith('\n'):
                        raise BudgetError('ledger_partial_write')  # fail closed
                    self._apply(json.loads(line))
                self._offset = f.tell()
                if event is not None:
                    self._check(event)
                    event = dict(event, time=time.time())
                    f.seek(0, 2)
                    f.write(json.dumps(event, sort_keys=True) + '\n')
                    f.flush()
                    if self.durable:
                        os.fsync(f.fileno())
                    self._offset = f.tell()
                    self._apply(event)

    def totals(self):
        self._transact()
        committed = sum(self._committed.values())
        stages = sorted({stage for stage, _ in self._count})
        return {
            'logical_calls': len(self._calls),
            'transport_attempts': sum(self._attempts.values()),
            'billed_usd': self._billed / 1e6,
            'open_reserved_usd': (committed - self._billed) / 1e6,
            'committed_usd': committed / 1e6,
            'committed_usd_by_pool': {p: self._committed[p] / 1e6 for p in POOLS},
            'unknown_cost_calls': self._unknown,
            'input_tokens': self._tokens['input'], 'output_tokens': self._tokens['output'],
            'calls_by_stage': {s: {p: self._count.get((s, p), 0) for p in POOLS} for s in stages},
            'attempts_by_stage': dict(self._attempts),
        }

    def reserve(self, call_id, stage, pool, micro_usd):
        return self._transact({'type': 'reserve', 'call_id': call_id, 'stage': stage, 'pool': pool,
                               'micro_usd': int(micro_usd)})

    def attempt(self, call_id, stage):
        return self._transact({'type': 'attempt', 'call_id': call_id, 'stage': stage})

    def settle(self, call_id, micro_usd, input_tokens=0, output_tokens=0):
        return self._transact({'type': 'settle', 'call_id': call_id, 'micro_usd': int(micro_usd),
                               'input_tokens': input_tokens, 'output_tokens': output_tokens})

    def unknown(self, call_id):
        return self._transact({'type': 'unknown', 'call_id': call_id})

    def reserved_for(self, call_id):
        return self._calls[call_id][2]


def caps_for(stage_counts, execution, scripted=False):
    """Ledger caps from the execution amendment. stage_counts: {stage: {'public': n, 'aux': n}} for
    the stage being run. Paid stages must equal the declared per-stage caps exactly; the ledger
    then carries the declared caps of every paid stage, because the file is shared by all of them."""
    b = execution['budget']
    stages = {}
    if not scripted:
        for stage, declared in b['stages'].items():
            stages[stage] = {'public': declared['public'], 'aux': declared['aux'],
                             'attempts': declared['max_calls'] + declared['retry_allowance']}
            if declared['public'] + declared['aux'] != declared['max_calls']:
                raise BudgetError('declared_caps_inconsistent')
    for stage, counts in stage_counts.items():
        if scripted:
            stages[stage] = {'public': counts['public'], 'aux': counts['aux'],
                             'attempts': counts['public'] + counts['aux']}
        elif stage not in stages or (counts['public'], counts['aux']) != (stages[stage]['public'], stages[stage]['aux']):
            raise BudgetError('manifest_disagrees_with_declared_caps')
    return {'study_micro_usd': int(b['study_usd_cap'] * 1e6),
            'pool_micro_usd': {'public': int(b['public_path_usd'] * 1e6), 'aux': int(b['auxiliary_private_usd'] * 1e6)},
            'stages': stages}
