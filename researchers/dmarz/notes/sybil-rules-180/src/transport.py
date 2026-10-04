"""One reservation authority, three stateless model workers, the experiment hub as the only transport.

Coordinator side
  FastLedger     the study's only ledger (same file format and refusals as provider.Ledger, O(1) per event)
  Dispatcher     reserves every call, hands each worker session one fenced task, settles what comes back
    HubDispatcher    tasks and results travel as artifacts of the worker-session runs on the hub
    LocalDispatcher  runs the same task code in this process (selftests only)

Worker side
  PermitLedger   what the adapter sees on a worker: only the call ids of the current task, each once
  run_task       executes one task with the frozen adapter
  serve          the worker process: take one session from the hub queue, execute its tasks in order

A fence is `<session run id>#<sequence number>`. A worker executes each fence at most once and never goes
back; a task whose result does not arrive by its deadline is recorded as lost and is never re-sent.
The servers never talk to each other and the coordinator never holds the model credential.
"""
import gzip
import json
import os
import socket
import threading
import time
import types
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import provider
import study

SESSION_ROLE = 'model-worker'
TASK_VERSION = 1
LOST = 'worker_task_lost'
AMBIGUOUS = 'ambiguous_send_not_retried'


def host_name():
    return os.environ.get('SWARM_HOST') or socket.gethostname()


def request_bytes(config, system, user):
    """The exact encoded request body the adapter will send (no credential involved)."""
    shell = types.SimpleNamespace(c=config, b=config['budget'])
    return json.dumps(provider.OpenRouter.body(shell, system, user)).encode()


def reservation(config, system, user):
    """Micro-dollars, the adapter's own formula: request bytes as the input bound plus the full output limit."""
    b = config['budget']
    n = len(request_bytes(config, system, user))
    return int(n * b['input_usd_per_million'] + b['max_output_tokens'] * b['output_usd_per_million'] + 0.999999), n


# ------------------------------------------------------------------ ledgers

class FastLedger(provider.Ledger):
    """The coordinator's ledger. One process writes it; totals are kept in memory after the first read.

    File format and refusal rules are those of provider.Ledger, so `provider.Ledger(path, budget).transact()`
    recomputes the same totals from the file (a selftest and every stage summary compare them)."""

    def __init__(self, path, budget):
        super().__init__(path, budget)
        self._mem = None
        self._size = None

    def _load(self):
        reserved, settled, attempts, tokens = {}, {}, 0, [0, 0]
        if self.path.exists():
            with self.path.open(encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    e = json.loads(line)
                    if e['type'] == 'reserve':
                        reserved[e['call_id']] = e['micro_usd']
                    elif e['type'] == 'attempt':
                        attempts += 1
                    elif e['type'] == 'response':
                        settled[e['call_id']] = e['actual_micro_usd']
                        tokens[0] += e.get('input_tokens', 0); tokens[1] += e.get('output_tokens', 0)
        by_stage = {}
        for call in reserved:
            by_stage[provider.stage_of(call)] = by_stage.get(provider.stage_of(call), 0) + 1
        self._mem = {'reserved': reserved, 'settled': settled, 'attempts': attempts, 'by_stage': by_stage,
                     'committed': sum(settled.get(c, a) for c, a in reserved.items()), 'tokens': tokens}
        self._size = self.path.stat().st_size if self.path.exists() else 0

    def transact(self, event=None):
        return self.transact_many([event] if event else [])

    def transact_many(self, events):
        """All events are checked first; either every one is appended (one sync) or none is."""
        b = self.budget
        with self._lock:
            size = self.path.stat().st_size if self.path.exists() else 0
            if self._mem is None or size != self._size:
                self._load()
            m = self._mem
            new_reserved, new_settled = {}, {}
            by_stage, attempts, committed, count = dict(m['by_stage']), m['attempts'], m['committed'], len(m['reserved'])
            for event in events:
                kind, call = event['type'], event['call_id']
                known = call in m['reserved'] or call in new_reserved
                if kind == 'reserve':
                    stage = provider.stage_of(call)
                    if known: raise provider.CallFailure('duplicate_call_refused')
                    if by_stage.get(stage, 0) >= b['max_calls'].get(stage, 0): raise provider.CallFailure('stage_call_cap_reached')
                    if count >= b['max_attempted_calls']: raise provider.CallFailure('study_call_cap_reached')
                    if committed + event['micro_usd'] > int(b['aggregate_usd'] * 1_000_000):
                        raise provider.CallFailure('aggregate_budget_exhausted')
                    new_reserved[call] = event['micro_usd']
                    by_stage[stage] = by_stage.get(stage, 0) + 1
                    committed += event['micro_usd']; count += 1
                elif kind == 'attempt':
                    if not known: raise provider.CallFailure('attempt_without_reservation')
                    if attempts >= b['max_transport_attempts']: raise provider.CallFailure('transport_attempt_cap_reached')
                    attempts += 1
                elif kind == 'response':
                    if not known: raise provider.CallFailure('attempt_without_reservation')
                    reserved = new_reserved.get(call, m['reserved'].get(call))
                    committed += event['actual_micro_usd'] - new_settled.get(call, m['settled'].get(call, reserved))
                    new_settled[call] = event['actual_micro_usd']
                else:
                    raise provider.CallFailure('unknown_ledger_event')
            if events:
                with self.path.open('a', encoding='utf-8') as f:
                    os.chmod(self.path, 0o600)
                    f.write(''.join(json.dumps(e, sort_keys=True) + '\n' for e in events)); f.flush(); os.fsync(f.fileno())
                m['reserved'].update(new_reserved); m['settled'].update(new_settled)
                m['by_stage'], m['attempts'], m['committed'] = by_stage, attempts, committed
                for e in events:
                    if e['type'] == 'response':
                        m['tokens'][0] += e.get('input_tokens', 0); m['tokens'][1] += e.get('output_tokens', 0)
                self._size = self.path.stat().st_size
            return {'attempted_calls': len(m['reserved']), 'calls_by_stage': dict(m['by_stage']),
                    'transport_attempts': m['attempts'], 'usage_reported_calls': len(m['settled']),
                    'reserved_usd': sum(m['reserved'].values()) / 1e6, 'actual_usd': sum(m['settled'].values()) / 1e6,
                    'committed_usd': m['committed'] / 1e6, 'input_tokens': m['tokens'][0], 'output_tokens': m['tokens'][1],
                    'cap_usd': b['aggregate_usd'], 'cap_calls': b['max_attempted_calls'],
                    'cap_transport_attempts': b['max_transport_attempts']}


class PermitLedger:
    """The adapter's ledger on a worker: accepts only the permitted call ids, each once, at the permitted amount."""

    def __init__(self, permits, max_attempts_per_call):
        self.permits, self.max = dict(permits), max_attempts_per_call
        self.used, self.attempts = set(), {}
        self._lock = threading.Lock()

    def transact(self, event=None):
        with self._lock:
            if event is None:
                return {}
            call, kind = event['call_id'], event['type']
            if kind == 'reserve':
                if call not in self.permits: raise provider.CallFailure('no_permit')
                if call in self.used: raise provider.CallFailure('duplicate_call_refused')
                if event['micro_usd'] != self.permits[call]: raise provider.CallFailure('permit_reservation_mismatch')
                self.used.add(call)
            elif kind == 'attempt':
                if call not in self.used: raise provider.CallFailure('attempt_without_reservation')
                self.attempts[call] = self.attempts.get(call, 0) + 1
                if self.attempts[call] > self.max: raise provider.CallFailure('transport_attempt_cap_reached')
            elif kind != 'response':
                raise provider.CallFailure('unknown_ledger_event')
            return {}


def max_attempts_per_call(budget):
    o = budget['billing_outage']
    return budget['retry']['transport_retries'] + 1 + int(o['max_wait_seconds'] // max(o['retry_every_seconds'], 1)) + 2


# ------------------------------------------------------------------ worker side

STOPPING = tuple(provider.INTEGRITY) + (provider.BILLING_STOP, 'no_permit', 'permit_reservation_mismatch')


def _object(obj):
    if not isinstance(obj, dict):
        raise ValueError('not_an_object')
    return obj


def run_task(task, api):
    """Execute one task. Returns the result value. Never raises for a failed call."""
    budget = api.b
    api.ledger = PermitLedger({c['call_id']: c['micro_usd'] for c in task['calls']}, max_attempts_per_call(budget))
    before = dict(api.billing)
    stop = threading.Event()
    started = time.time()

    def one(c):
        row = {'call_id': c['call_id'], 'ok': False, 'category': None, 'answer': None, 'accounting': {},
               'started': time.time()}
        if stop.is_set():
            row['category'] = 'not_started'
            return row
        try:
            answer, account = api.call(task['systems'][c['system']], c['user'], c['call_id'], _object)
            row.update(ok=True, answer=answer, accounting=account)
        except provider.CallFailure as exc:
            row.update(category=exc.category, accounting=exc.accounting)
            if exc.category in STOPPING:
                stop.set()
        except Exception as exc:
            row.update(category='internal_' + type(exc).__name__)
        row['ended'] = time.time()
        return row

    with ThreadPoolExecutor(max_workers=max(1, int(task['in_flight']))) as pool:
        rows = list(pool.map(one, task['calls']))
    return {'version': TASK_VERSION, 'fence': task['fence'], 'seq': task['seq'], 'host': host_name(), 'results': rows,
            'billing': {k: api.billing[k] - before.get(k, 0) for k in api.billing},
            'started': started, 'ended': time.time()}


def _write_gz(path, value):
    tmp = Path(str(path) + '.tmp')
    with gzip.open(tmp, 'wt', encoding='utf-8') as f:
        json.dump(value, f)
    os.replace(tmp, path)


def _read_gz(path):
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        return json.load(f)


def _fetch(sr, run_id, name, dest):
    """Download an artifact of a run, or return None while it does not exist (or the hub cannot be reached)."""
    try:
        sr.download('/a/' + urllib.parse.quote(run_id) + '/' + urllib.parse.quote(name), dest)
        return _read_gz(dest)
    except Exception:
        try:
            Path(dest).unlink()
        except OSError:
            pass
        return None


def _upload(sr, run_id, path, name, sleep=time.sleep, tries=40):
    """Upload until the hub acknowledges it durably (a spooled upload is not an acknowledgement)."""
    for _ in range(tries):
        try:
            receipt = sr.upload(run_id, path, name)
            if receipt and not receipt.get('spooled'):
                return receipt
            sr.flush(quiet=True)
        except Exception:
            pass
        sleep(3)
    raise RuntimeError('artifact_not_durably_acknowledged')


def serve(sr, work_dir, opener=None, poll=1.0, attach_seconds=None, idle_seconds=10800, sleep=time.sleep, stop=None,
          api_clock=time.monotonic, api_sleep=time.sleep):
    """The model worker. Returns a process exit code: 0 session closed, 4 refused, 5 nothing to attach to."""
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    budget = study.design()['budget']
    attach_seconds = budget['worker_attach_seconds'] if attach_seconds is None else attach_seconds
    waited = 0.0
    run = None
    while run is None:
        if stop is not None and stop.is_set():
            return 5
        try:
            run = sr.next_run(study.EXPERIMENT)
        except Exception:
            run = None
        if run is None:
            if waited >= attach_seconds:
                return 5
            sleep(min(5.0, max(poll, 0.05))); waited += min(5.0, max(poll, 0.05))
    p = run.params or {}
    if p.get('role') != SESSION_ROLE or p.get('source_hash') != study.source_hash():
        run.fail('worker refused this run: not a worker session at this source hash', model_calls=0)
        return 4
    try:
        api = provider.OpenRouter(PermitLedger({}, 0), study.provider_config(), opener, api_clock, api_sleep)
    except provider.CallFailure as exc:
        run.fail('worker cannot start: ' + exc.category, model_calls=0)
        return 4
    journal = work_dir / (run.id.replace('/', '__') + '.journal.jsonl')
    seen = {}
    if journal.exists():
        for line in journal.read_text().splitlines():
            if line.strip():
                e = json.loads(line)
                seen[e['seq']] = e['state']
    totals = {'model_calls': 0, 'input_tokens': 0, 'output_tokens': 0, 'cost_usd': 0.0, 'failed_calls': 0, 'tasks': 0}

    def note(seq, state):
        with journal.open('a') as f:
            f.write(json.dumps({'seq': seq, 'state': state, 'time': time.time()}) + '\n'); f.flush(); os.fsync(f.fileno())
        seen[seq] = state

    seq, idle = 1, 0.0
    with run:
        while True:
            if stop is not None and stop.is_set():
                run.fail('worker stopped before its session was closed', **totals)
                return 5
            task = _fetch(sr, run.id, f'task-{seq:06d}.json.gz', work_dir / f'{run.id.replace("/", "__")}-task-{seq:06d}.json.gz')
            if task is None:
                if idle >= idle_seconds:
                    run.fail('worker idle limit reached before its session was closed', **totals)
                    return 5
                sleep(poll); idle += poll
                continue
            idle = 0.0
            if task.get('fence') != f'{run.id}#{seq:06d}' or task.get('source_hash') != study.source_hash():
                run.fail('worker refused a task with a wrong fence or source hash', **totals)
                return 4
            if task['kind'] == 'close':
                run.done(message=f'session closed after {totals["tasks"]} tasks', **totals)
                return 0
            result_path = work_dir / f'{run.id.replace("/", "__")}-result-{seq:06d}.json.gz'
            if seen.get(seq) == 'finished' and result_path.exists():
                result = _read_gz(result_path)            # executed before a restart: report it again, never re-send
            elif seq in seen:
                # Started before a restart and never finished: which calls were sent is unknown. Nothing is re-sent.
                result = {'version': TASK_VERSION, 'fence': task['fence'], 'seq': seq, 'host': host_name(),
                          'results': [{'call_id': c['call_id'], 'ok': False, 'category': AMBIGUOUS, 'answer': None,
                                       'accounting': {}} for c in task['calls']], 'billing': {}}
            else:
                note(seq, 'started')
                result = run_task(task, api)
                _write_gz(result_path, result)
                note(seq, 'finished')
                for r in result['results']:
                    a = r.get('accounting') or {}
                    totals['model_calls'] += bool(a.get('attempted'))
                    totals['input_tokens'] += a.get('input_tokens', 0) or 0
                    totals['output_tokens'] += a.get('output_tokens', 0) or 0
                    totals['cost_usd'] += a.get('actual_usd', 0) or 0
                    totals['failed_calls'] += not r['ok']
                totals['tasks'] += 1
            if not result_path.exists():
                _write_gz(result_path, result)
            _upload(sr, run.id, result_path, f'result-{seq:06d}.json.gz', sleep)
            pauses = (result.get('billing') or {}).get('billing_pauses', 0)
            run.progress(seq, None, force=True, message=f'task {seq} ({task.get("label")}): {len(result["results"])} calls'
                         + (f', {pauses} billing pause' if pauses else ''), **totals)
            for path in (result_path, work_dir / f'{run.id.replace("/", "__")}-task-{seq:06d}.json.gz'):
                try:
                    path.unlink()                         # the hub holds both; the worker keeps only its journal
                except OSError:
                    pass
            seq += 1


# ------------------------------------------------------------------ coordinator side

class StageStop(Exception):
    """Dispatch must stop: an integrity failure, a billing stop, a lost task over the limit, a deadline."""
    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


class Dispatcher:
    """Reserve, hand out, settle. Subclasses implement `_exchange(tasks, timeout)`."""

    def __init__(self, ledger, config, slots):
        self.ledger, self.config, self.slots = ledger, config, slots
        self.seq = [0] * slots
        self.hosts = [None] * slots
        self.attempts = 0
        self.billing = {'billing_pauses': 0, 'billing_pause_seconds': 0.0, 'billing_affected_calls': 0}

    def fence(self, slot):
        raise NotImplementedError

    def dispatch(self, batch, calls, in_flight, label=''):
        """calls: [{'unit', 'slot', 'system', 'user'}]. Returns {unit: {'ok', 'category', 'answer', 'accounting', 'host'}}.

        Raises StageStop only when a reservation is refused before anything is sent."""
        systems = study.SYSTEMS
        per_slot = [[] for _ in range(self.slots)]
        events, permits = [], []
        for c in calls:
            micro, n = reservation(self.config, systems[c['system']], c['user'])
            if n > self.config['budget']['max_input_bytes']:
                raise StageStop('input_size_limit')
            call_id = f'{batch}:{c["unit"]}'
            events.append({'type': 'reserve', 'call_id': call_id, 'micro_usd': micro, 'time': time.time()})
            permits.append((c, call_id, micro))
        try:
            self.ledger.transact_many(events)              # refused as a whole batch: nothing is sent
        except provider.CallFailure as exc:
            raise StageStop(exc.category) from None
        for c, call_id, micro in permits:
            per_slot[c['slot']].append({'call_id': call_id, 'system': c['system'], 'user': c['user'], 'micro_usd': micro})
        tasks = {}
        for slot, items in enumerate(per_slot):
            if not items:
                continue
            self.seq[slot] += 1
            tasks[slot] = {'version': TASK_VERSION, 'kind': 'calls', 'fence': self.fence(slot), 'seq': self.seq[slot],
                           'batch': batch, 'label': label, 'source_hash': study.source_hash(), 'in_flight': in_flight,
                           'systems': {k: systems[k] for k in sorted({i['system'] for i in items})}, 'calls': items,
                           'issued': time.time()}
        results = self._exchange(tasks, self.config['budget']['task_timeout_seconds'])
        out, settle = {}, []
        for slot, task in tasks.items():
            result = results.get(slot)
            rows = {r['call_id']: r for r in (result or {}).get('results', [])} if result and result.get('fence') == task['fence'] else {}
            host = (result or {}).get('host')
            if host:
                self.hosts[slot] = host
            for k in self.billing:
                self.billing[k] += ((result or {}).get('billing') or {}).get(k, 0)
            for item in task['calls']:
                r = rows.get(item['call_id'])
                unit = item['call_id'].split(':', 1)[1]
                if r is None:
                    out[unit] = {'ok': False, 'category': LOST, 'answer': None, 'accounting': {}, 'host': host, 'slot': slot}
                    continue
                a = r.get('accounting') or {}
                for n in range(int(a.get('attempts', 0) or 0)):
                    settle.append({'type': 'attempt', 'call_id': item['call_id'], 'n': n + 1, 'time': time.time()})
                if a.get('usage_reported'):
                    settle.append({'type': 'response', 'call_id': item['call_id'],
                                   'actual_micro_usd': int(round(a['actual_usd'] * 1e6)),
                                   'input_tokens': a['input_tokens'], 'output_tokens': a['output_tokens']})
                out[unit] = {'ok': bool(r['ok']), 'category': r.get('category'), 'answer': r.get('answer'), 'accounting': a,
                             'host': host, 'slot': slot, 'started': r.get('started'), 'ended': r.get('ended')}
        try:
            self.ledger.transact_many(settle)
        except provider.CallFailure as exc:
            raise StageStop(exc.category) from None
        return out

    def close(self):
        pass


class LocalDispatcher(Dispatcher):
    """Executes tasks in this process with the frozen adapter and a supplied opener. Selftests only."""

    def __init__(self, ledger, config, slots, opener, clock=time.monotonic, sleep=time.sleep):
        super().__init__(ledger, config, slots)
        self.apis = [provider.OpenRouter(PermitLedger({}, 0), config, opener, clock, sleep) for _ in range(slots)]

    def fence(self, slot):
        return f'local-w{slot}#{self.seq[slot]:06d}'

    def _exchange(self, tasks, timeout):
        return {slot: run_task(task, self.apis[slot]) for slot, task in tasks.items()}


class HubDispatcher(Dispatcher):
    """Tasks and results are artifacts of three worker-session runs on the hub."""

    def __init__(self, sr, ledger, config, slots, work_dir, chain_id, poll=1.0, sleep=time.sleep, clock=time.monotonic,
                 allow_shared_host=False):
        super().__init__(ledger, config, slots)
        self.sr, self.work, self.poll, self.sleep, self.clock = sr, Path(work_dir), poll, sleep, clock
        self.work.mkdir(parents=True, exist_ok=True)
        self.sessions = [f'{study.EXPERIMENT}/workers-{chain_id}-w{k}' for k in range(slots)]
        self.allow_shared_host = allow_shared_host
        self.attached = False
        self.queued = False
        self.closed = False

    def fence(self, slot):
        return f'{self.sessions[slot]}#{self.seq[slot]:06d}'

    def attach(self, timeout):
        """Queue the worker sessions and wait until three workers on three different hosts hold them."""
        params = [{'role': SESSION_ROLE, 'slot': k, 'source_hash': study.source_hash(), 'code': study.code_revision()}
                  for k in range(self.slots)]
        self.sr.enqueue(study.EXPERIMENT, params, tags=['worker-session'], run_ids=self.sessions)
        self.queued = True
        waited = 0.0
        while True:
            detail = [self.sr.get_run(s) or {} for s in self.sessions]
            if all(d.get('status') == 'running' for d in detail):
                break
            if any(d.get('status') in ('failed', 'done') for d in detail) or waited >= timeout:
                raise StageStop('workers_not_attached')
            self.sleep(self.poll); waited += self.poll
        self.hosts = [d.get('host') for d in detail]
        if len(set(self.hosts)) != self.slots and not self.allow_shared_host:
            raise StageStop('workers_share_a_host')
        self.attached = True
        return list(self.hosts)

    def _put(self, slot, task):
        path = self.work / f'w{slot}-task-{task["seq"]:06d}.json.gz'
        _write_gz(path, task)
        _upload(self.sr, self.sessions[slot], path, f'task-{task["seq"]:06d}.json.gz', self.sleep)
        path.unlink()

    def _exchange(self, tasks, timeout):
        for slot, task in tasks.items():
            self._put(slot, task)
        results, deadline = {}, self.clock() + timeout
        while len(results) < len(tasks) and self.clock() < deadline:
            for slot, task in tasks.items():
                if slot in results:
                    continue
                dest = self.work / f'w{slot}-result-{task["seq"]:06d}.json.gz'
                got = _fetch(self.sr, self.sessions[slot], f'result-{task["seq"]:06d}.json.gz', dest)
                if got is not None:
                    results[slot] = got
                    dest.unlink()
            if len(results) < len(tasks):
                self.sleep(self.poll)
        return results

    def close(self):
        """Tell every worker its session is over, including a worker that takes a session later. Safe to call twice."""
        if not self.queued or self.closed:
            return
        self.closed = True
        for slot in range(self.slots):
            self.seq[slot] += 1
            try:
                self._put(slot, {'version': TASK_VERSION, 'kind': 'close', 'fence': self.fence(slot), 'seq': self.seq[slot],
                                 'source_hash': study.source_hash(), 'calls': [], 'issued': time.time()})
            except Exception:
                pass
