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

A task fence is `<session run id>#<sequence number>`; a decision fence is the call id
`<batch>:<economy>.r<round>.<owner>`, reserved once in the coordinator's ledger. A worker executes each task
fence at most once, never sends a call id twice, and never sends a call after the task's `expires` time.

Lost tasks (reviewer requirement 2). A task is lost when its result has not arrived by the task deadline, or
earlier when the worker's session stops heart-beating on the hub for `worker_silent_seconds` (or leaves the
running state). The coordinator then re-issues, once, only that task's call ids that have no recorded response,
with the same call ids, to a surviving worker (the same one only if no other is alive), and stops giving the
silent worker work. Each re-issued call id also gets a reservation `reissue-<batch>:<unit>` in the ledger
(stage key REISSUE, its own cap), because the lost send may have been billed. The first response recorded
for a call id is the only one ever used; a late result of an abandoned task is never read. A call id with no
response after the re-issue is recorded as lost (`worker_task_lost`): in S1 a forced null owner-round.

Hub polling (reviewer requirement 3): every `hub_poll_seconds` (3 s); after any hub error the interval
doubles up to `hub_backoff_max_seconds` and returns to 3 s after the next clean poll.

One reservation authority (reviewer requirement 7): the coordinator's FastLedger is the only ledger of the
study. Workers hold no ledger: each task carries per-call permits (call id and reserved amount) and the
adapter on a worker can reserve only those, each once. The adapter's billing pause is per worker process.
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
EXPIRED = 'task_expired_not_sent'
REISSUE_PREFIX = 'reissue-'


class HubTrouble(Exception):
    """The hub did not answer properly (as opposed to: the artifact does not exist yet)."""


class Poller:
    """Fixed polling interval; after a hub error the interval doubles up to `cap`, then returns to `base`."""

    def __init__(self, base, cap, sleep=time.sleep):
        self.base, self.cap, self.sleep = float(base), float(cap), sleep
        self.delay, self.errors = float(base), 0

    def wait(self, trouble=False):
        if trouble:
            self.errors += 1
            self.delay = min(self.cap, max(self.base, self.delay * 2))
        else:
            self.delay = self.base
        self.sleep(self.delay)
        return self.delay


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


def run_task(task, api, sent=None, clock=time.time):
    """Execute one task. Returns the result value. Never raises for a failed call.

    `sent`: call ids this worker has already sent (a set it shares across tasks); such a call is never sent
    again. A call is not sent after the task's `expires` time."""
    budget = api.b
    sent = set() if sent is None else sent
    api.ledger = PermitLedger({c['call_id']: c['micro_usd'] for c in task['calls']}, max_attempts_per_call(budget))
    before = dict(api.billing)
    stop = threading.Event()
    guard = threading.Lock()
    started = time.time()

    def one(c):
        row = {'call_id': c['call_id'], 'ok': False, 'category': None, 'answer': None, 'accounting': {},
               'started': time.time()}
        if stop.is_set():
            row['category'] = 'not_started'
            return row
        if task.get('expires') is not None and clock() > task['expires']:
            row['category'] = EXPIRED
            return row
        with guard:
            if c['call_id'] in sent:
                row['category'] = AMBIGUOUS
                return row
            sent.add(c['call_id'])
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
    """Download an artifact of a run. None while it does not exist (HTTP 404); HubTrouble on any other failure."""
    try:
        sr.download('/a/' + urllib.parse.quote(run_id) + '/' + urllib.parse.quote(name), dest)
        return _read_gz(dest)
    except Exception as exc:
        try:
            Path(dest).unlink()
        except OSError:
            pass
        if ': 404' in str(exc):
            return None
        raise HubTrouble(type(exc).__name__) from None


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


def serve(sr, work_dir, opener=None, poll=None, attach_seconds=None, idle_seconds=10800, sleep=time.sleep, stop=None,
          api_clock=time.monotonic, api_sleep=time.sleep, backoff_max=None):
    """The model worker. Returns a process exit code: 0 session closed, 4 refused, 5 nothing to attach to."""
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    budget = study.design()['budget']
    attach_seconds = budget['worker_attach_seconds'] if attach_seconds is None else attach_seconds
    poll = budget['hub_poll_seconds'] if poll is None else poll
    poller = Poller(poll, budget['hub_backoff_max_seconds'] if backoff_max is None else backoff_max, sleep)
    waited = 0.0
    run = None
    while run is None:
        if stop is not None and stop.is_set():
            return 5
        trouble = False
        try:
            run = sr.next_run(study.session_experiment())
        except Exception:
            run, trouble = None, True
        if run is None:
            if waited >= attach_seconds:
                return 5
            waited += poller.wait(trouble)
    p = run.params or {}
    if p.get('role') != SESSION_ROLE or p.get('source_hash') != study.source_hash() or p.get('model') != study.model_name():
        run.fail('worker refused this run: not a worker session at this source hash and model', model_calls=0)
        return 4
    try:
        api = provider.OpenRouter(PermitLedger({}, 0), study.provider_config(), opener, api_clock, api_sleep)
    except (provider.CallFailure, ValueError) as exc:
        exc.category = getattr(exc, 'category', str(exc))
        run.fail('worker cannot start: ' + exc.category, model_calls=0)
        return 4
    journal = work_dir / (run.id.replace('/', '__') + '.journal.jsonl')
    seen, sent = {}, set()
    if journal.exists():
        for line in journal.read_text().splitlines():
            if line.strip():
                e = json.loads(line)
                seen[e['seq']] = e['state']
                sent.update(e.get('calls') or [])      # a call id this worker may have sent is never sent again
    totals = {'model_calls': 0, 'input_tokens': 0, 'output_tokens': 0, 'cost_usd': 0.0, 'failed_calls': 0, 'tasks': 0}

    def note(seq, state, calls=None):
        with journal.open('a') as f:
            f.write(json.dumps({'seq': seq, 'state': state, 'time': time.time(), 'calls': calls or []}) + '\n')
            f.flush(); os.fsync(f.fileno())
        seen[seq] = state

    seq, idle = 1, 0.0
    with run:
        while True:
            if stop is not None and stop.is_set():
                run.fail('worker stopped before its session was closed', **totals)
                return 5
            try:
                task, trouble = _fetch(sr, run.id, f'task-{seq:06d}.json.gz', work_dir / f'{run.id.replace("/", "__")}-task-{seq:06d}.json.gz'), False
            except HubTrouble:
                task, trouble = None, True
            if task is None:
                if idle >= idle_seconds:
                    run.fail('worker idle limit reached before its session was closed', **totals)
                    return 5
                idle += poller.wait(trouble)
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
                note(seq, 'started', [c['call_id'] for c in task['calls']])
                result = run_task(task, api, sent)
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
    """Dispatch must stop: an integrity failure, a billing stop, no live worker, a deadline."""
    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


class Dispatcher:
    """Reserve, hand out, re-issue lost assignments once, settle. Subclasses implement `_exchange(tasks, timeout)`."""

    def __init__(self, ledger, config, slots):
        self.ledger, self.config, self.slots = ledger, config, slots
        self.seq = [0] * slots
        self.hosts = [None] * slots
        self.dead = set()                  # slots whose worker was lost; they get no further work
        self.attempts = 0
        self.billing = {'billing_pauses': 0, 'billing_pause_seconds': 0.0, 'billing_affected_calls': 0}
        self.transport = {'tasks': 0, 'lost_tasks': 0, 'reissued_calls': 0, 'reissue_refused': None,
                          'lost_calls_after_reissue': 0, 'rerouted_calls': 0, 'hub_errors': 0, 'events': []}

    def fence(self, slot):
        raise NotImplementedError

    def _task(self, slot, batch, label, in_flight, items):
        systems = study.SYSTEMS
        self.seq[slot] += 1
        issued = time.time()
        self.transport['tasks'] += 1
        return {'version': TASK_VERSION, 'kind': 'calls', 'fence': self.fence(slot), 'seq': self.seq[slot],
                'batch': batch, 'label': label, 'source_hash': study.source_hash(), 'in_flight': in_flight,
                'systems': {k: systems[k] for k in sorted({i['system'] for i in items})}, 'calls': items,
                'issued': issued, 'expires': issued + self.config['budget']['task_timeout_seconds']}

    def _live(self, exclude=()):
        live = [k for k in range(self.slots) if k not in self.dead and k not in exclude]
        return live or [k for k in range(self.slots) if k not in self.dead]

    def _route(self, items_by_planned_slot, exclude=()):
        """Planned slot when its worker is alive, else the live slot with the fewest assignments so far."""
        live = self._live(exclude)
        if not live:
            raise StageStop('no_live_worker')
        out = {}
        for slot, items in sorted(items_by_planned_slot.items()):
            if slot in live:
                out.setdefault(slot, []).extend(items)
        for slot, items in sorted(items_by_planned_slot.items()):
            if slot not in live:
                for it in items:
                    k = min(live, key=lambda j: (len(out.get(j, [])), j))
                    self.transport['rerouted_calls'] += 1
                    out.setdefault(k, []).append(it)
        return out

    def dispatch(self, batch, calls, in_flight, label=''):
        """calls: [{'unit', 'slot', 'system', 'user'}]. Returns {unit: {'ok', 'category', 'answer', 'accounting', 'host', ...}}.

        Raises StageStop when a reservation is refused before anything is sent, or when no worker is alive."""
        systems = study.SYSTEMS
        per_slot = {}
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
            per_slot.setdefault(c['slot'], []).append({'call_id': call_id, 'system': c['system'], 'user': c['user'], 'micro_usd': micro})
        tasks = {slot: self._task(slot, batch, label, in_flight, items) for slot, items in self._route(per_slot).items()}
        recorded = {}                                      # call id -> (row, slot, host, reissued); the first response only
        lost_items = self._collect(tasks, self._exchange(tasks, self.config['budget']['task_timeout_seconds']), recorded, False)
        if lost_items:
            lost_items = self._reissue(batch, label, in_flight, lost_items, recorded)
        return self._settle(permits, recorded, lost_items)

    def _collect(self, tasks, results, recorded, reissued):
        """Record the rows of returned tasks; mark slots without a result as lost. Returns {slot: [items without a row]}."""
        missing = {}
        for slot, task in tasks.items():
            result = results.get(slot)
            ok = bool(result) and result.get('fence') == task['fence']
            if not ok:
                self.dead.add(slot)
                self.transport['lost_tasks'] += 1
                self.transport['events'].append({'event': 'task_lost', 'fence': task['fence'], 'calls': len(task['calls']),
                                                 'reissue': reissued, 'time': time.time()})
                missing[slot] = list(task['calls'])
                continue
            host = result.get('host')
            if host:
                self.hosts[slot] = host
            for k in self.billing:
                self.billing[k] += (result.get('billing') or {}).get(k, 0)
            rows = {r['call_id']: r for r in result.get('results', [])}
            for item in task['calls']:
                r = rows.get(item['call_id'])
                if r is None:
                    missing.setdefault(slot, []).append(item)
                elif item['call_id'] not in recorded:
                    recorded[item['call_id']] = (r, slot, host, reissued)
        return missing

    def _reissue(self, batch, label, in_flight, lost_items, recorded):
        """Once: the lost call ids, same ids, to surviving workers. Returns {slot: [items still without a row]}."""
        items = [it for its in lost_items.values() for it in its if it['call_id'] not in recorded]
        if not items:
            return {}
        shadow = [{'type': 'reserve', 'call_id': REISSUE_PREFIX + it['call_id'], 'micro_usd': it['micro_usd'], 'time': time.time()}
                  for it in items]
        try:
            self.ledger.transact_many(shadow)
        except provider.CallFailure as exc:
            self.transport['reissue_refused'] = exc.category   # those calls stay lost: forced null rounds in S1
            return lost_items
        self.transport['reissued_calls'] += len(items)
        exclude = set(lost_items)
        routed = self._route({min(exclude): items}, exclude=exclude)
        tasks = {slot: self._task(slot, batch, label, in_flight, its) for slot, its in routed.items()}
        self.transport['events'].append({'event': 'reissue', 'calls': len(items), 'to': sorted(tasks), 'time': time.time()})
        missing = self._collect(tasks, self._exchange(tasks, self.config['budget']['task_timeout_seconds']), recorded, True)
        n = sum(len(v) for v in missing.values())
        self.transport['lost_calls_after_reissue'] += n
        return missing

    def _settle(self, permits, recorded, lost_items):
        out, settle = {}, []
        for c, call_id, micro in permits:
            unit = c['unit']
            if call_id not in recorded:
                out[unit] = {'ok': False, 'category': LOST, 'answer': None, 'accounting': {}, 'host': None, 'slot': None,
                             'transport': {'reissued': True, 'lost': True}}
                continue
            r, slot, host, reissued = recorded[call_id]
            a = r.get('accounting') or {}
            for n in range(int(a.get('attempts', 0) or 0)):
                settle.append({'type': 'attempt', 'call_id': call_id, 'n': n + 1, 'time': time.time()})
            if a.get('usage_reported'):
                settle.append({'type': 'response', 'call_id': call_id, 'actual_micro_usd': int(round(a['actual_usd'] * 1e6)),
                               'input_tokens': a['input_tokens'], 'output_tokens': a['output_tokens']})
            out[unit] = {'ok': bool(r['ok']), 'category': r.get('category'), 'answer': r.get('answer'), 'accounting': a,
                         'host': host, 'slot': slot, 'started': r.get('started'), 'ended': r.get('ended'),
                         'transport': {'reissued': reissued, 'served_slot': slot, 'planned_slot': c['slot']}}
        try:
            self.ledger.transact_many(settle)
        except provider.CallFailure as exc:
            raise StageStop(exc.category) from None
        return out

    def stats(self):
        return dict(self.transport, dead_slots=sorted(self.dead), events=self.transport['events'][-50:])

    def close(self):
        pass


class LocalDispatcher(Dispatcher):
    """Executes tasks in this process with the frozen adapter and a supplied opener. Selftests only.

    `lose`: a set of (slot, seq) whose results are dropped, to exercise the lost-task path."""

    def __init__(self, ledger, config, slots, opener, clock=time.monotonic, sleep=time.sleep, lose=()):
        super().__init__(ledger, config, slots)
        self.apis = [provider.OpenRouter(PermitLedger({}, 0), config, opener, clock, sleep) for _ in range(slots)]
        self.sent = [set() for _ in range(slots)]
        self.lose = set(lose)

    def fence(self, slot):
        return f'local-w{slot}#{self.seq[slot]:06d}'

    def _exchange(self, tasks, timeout):
        out = {}
        for slot, task in tasks.items():
            result = run_task(task, self.apis[slot], self.sent[slot])
            if (slot, task['seq']) not in self.lose:
                out[slot] = result
        return out


class HubDispatcher(Dispatcher):
    """Tasks and results are artifacts of three worker-session runs on the hub."""

    def __init__(self, sr, ledger, config, slots, work_dir, chain_id, poll=None, sleep=time.sleep, clock=time.monotonic,
                 allow_shared_host=False, silent_seconds=None, live_every=None, backoff_max=None):
        super().__init__(ledger, config, slots)
        b = config['budget']
        self.sr, self.work, self.sleep, self.clock = sr, Path(work_dir), sleep, clock
        self.poll = b['hub_poll_seconds'] if poll is None else poll
        self.backoff_max = b['hub_backoff_max_seconds'] if backoff_max is None else backoff_max
        self.silent = b['worker_silent_seconds'] if silent_seconds is None else silent_seconds
        self.live_every = b['liveness_check_seconds'] if live_every is None else live_every
        self.work.mkdir(parents=True, exist_ok=True)
        self.sessions = [f'{study.session_experiment()}/workers-{chain_id}-w{k}' for k in range(slots)]
        self.allow_shared_host = allow_shared_host
        self.attached = False
        self.queued = False
        self.closed = False
        self.heard = [None] * slots        # (hub 'updated' value, local clock when it last changed)

    def fence(self, slot):
        return f'{self.sessions[slot]}#{self.seq[slot]:06d}'

    def attach(self, timeout):
        """Queue the worker sessions and wait until three workers on three different hosts hold them."""
        params = [{'role': SESSION_ROLE, 'slot': k, 'source_hash': study.source_hash(), 'code': study.code_revision(),
                   'model': study.model_name()}
                  for k in range(self.slots)]
        self.sr.enqueue(study.session_experiment(), params, tags=['worker-session'], run_ids=self.sessions)
        self.queued = True
        poller = Poller(self.poll, self.backoff_max, self.sleep)
        waited = 0.0
        while True:
            trouble = False
            try:
                detail = [self.sr.get_run(s) or {} for s in self.sessions]
            except Exception:
                detail, trouble = [{} for _ in self.sessions], True
                self.transport['hub_errors'] += 1
            if all(d.get('status') == 'running' for d in detail):
                break
            if any(d.get('status') in ('failed', 'done') for d in detail) or waited >= timeout:
                raise StageStop('workers_not_attached')
            waited += poller.wait(trouble)
        self.hosts = [d.get('host') for d in detail]
        if len(set(self.hosts)) != self.slots and not self.allow_shared_host:
            raise StageStop('workers_share_a_host')
        now = self.clock()
        self.heard = [(d.get('updated'), now) for d in detail]
        self.attached = True
        return list(self.hosts)

    def _alive(self, slot):
        """False when the session left the running state or its hub record has not changed for `silent` seconds."""
        try:
            d = self.sr.get_run(self.sessions[slot]) or {}
        except Exception:
            self.transport['hub_errors'] += 1
            raise HubTrouble('get_run') from None
        now = self.clock()
        if d.get('status') not in ('running', 'assigned'):
            return False
        last = self.heard[slot]
        if last is None or d.get('updated') != last[0]:
            self.heard[slot] = (d.get('updated'), now)
            return True
        return now - last[1] <= self.silent

    def _put(self, slot, task):
        path = self.work / f'w{slot}-task-{task["seq"]:06d}.json.gz'
        _write_gz(path, task)
        _upload(self.sr, self.sessions[slot], path, f'task-{task["seq"]:06d}.json.gz', self.sleep)
        path.unlink()

    def _exchange(self, tasks, timeout):
        for slot, task in tasks.items():
            self._put(slot, task)
        results, given_up = {}, set()
        start = self.clock()
        deadline, next_check = start + timeout, start + self.live_every
        poller = Poller(self.poll, self.backoff_max, self.sleep)
        while len(results) + len(given_up) < len(tasks) and self.clock() < deadline:
            trouble = False
            for slot, task in tasks.items():
                if slot in results or slot in given_up:
                    continue
                dest = self.work / f'w{slot}-result-{task["seq"]:06d}.json.gz'
                try:
                    got = _fetch(self.sr, self.sessions[slot], f'result-{task["seq"]:06d}.json.gz', dest)
                except HubTrouble:
                    got, trouble = None, True
                    self.transport['hub_errors'] += 1
                if got is not None:
                    results[slot] = got
                    dest.unlink()
            if self.clock() >= next_check:
                next_check = self.clock() + self.live_every
                for slot in tasks:
                    if slot in results or slot in given_up:
                        continue
                    try:
                        if not self._alive(slot):
                            given_up.add(slot)
                            self.transport['events'].append({'event': 'worker_silent', 'slot': slot, 'fence': tasks[slot]['fence'],
                                                             'time': time.time()})
                    except HubTrouble:
                        trouble = True
            if len(results) + len(given_up) < len(tasks):
                poller.wait(trouble)
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
