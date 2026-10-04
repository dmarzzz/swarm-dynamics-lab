"""Offline rehearsal of the whole chain: a throwaway hub on 127.0.0.1, one worker thread per design worker, an
OpenAI-shaped stub model. No model call; nothing leaves the machine.

    python3 src/rehearse.py --hub-dir <dir with hub.py and swarm_report.py> [--only a,b,d]

  a  S0, P0, Q0, X0, S1 to completion; the stub's usage makes the cost rule admit exactly N = 1; `chain verify`
     (including the S1 re-simulation) must pass and a second chain must be refused (no replay).
  b  a stub that answers the mechanics questions wrongly: Q0 fails, the chain stops at Q0, X0 and S1 never start.
  d  the T+52 stop moved to a few seconds after S1 starts: S1 stops with `dispatch_deadline`, records are kept,
     continuations report fewer than 20 rounds.
Branch, fork and inbox isolation are checked in S0 (which runs inside every scenario); the governor is tested in
src/selftest.py with a simulated limit.
"""
import argparse
import io
import json
import os
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import chain
import coordinator
import openai_provider
import study
import transport
import worker

LOCAL = '127.0.0.1'
QA = {c['question']: c['answer'] for c in study.mechanics_cases()}


class _Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def stub_action(obs, seeder):
    """Sees only the packet. Ordinary: produce full listed capacity, pass. Seeder: register, move half, produce both."""
    p = obs['portfolio']
    firms = [f for f in p['firms'] if f['status'] == 'active']
    admin = {'action': 'none'}
    production = {f['firm']: f['capacity'] for f in firms}
    if seeder:
        if len(p['firms']) == 1 and not p['in_transit']:
            admin = {'action': 'register'}
        elif len(firms) == 2 and min(f['capacity'] for f in firms) == 0 and not p['in_transit']:
            src = max(firms, key=lambda f: f['capacity'])
            dst = min(firms, key=lambda f: f['capacity'])
            half = round(src['capacity'] / 2, 3)
            admin = {'action': 'transfer', 'from': src['firm'], 'to': dst['firm'], 'units': half}
            production[src['firm']] = round(src['capacity'] - half, 3)
    inv = None
    spend = p['unit_cost'] * sum(production.values()) + (20 if admin['action'] == 'register' else 0) + 3 * len(p['firms'])
    budget = min(p['investment_allowance'], p['cash'] - spend - 1)
    if budget > 1 and firms:
        target = max(firms, key=lambda f: f['capacity'])
        inv = {'firm': target['firm'], 'units': int(budget / 200 * 1000) / 1000}
        if inv['units'] <= 0:
            inv = None
    com = {'action': 'pass'}
    if obs['channel']['available'] and obs['round'] % 3 == 0:
        rows = obs['owners_table']['rows']
        com = {'action': 'send', 'to': rows[0][0] if rows[0][0] != obs['you'] else rows[1][0], 'text': 'How is your margin this round?'}
    return {'summary': 'stub', 'rule_check': 'stub', 'production': production, 'investment': inv, 'admin': admin,
            'communication': com, 'memo': f'round {obs["round"]}'}


class Stub:
    """OpenAI Chat Completions shape: no cost field; usage sized so the cost rule admits N = 1 (about USD 0.018 a call)."""
    def __init__(self, mode='good'):
        self.mode = mode
        self.lock = threading.Lock()
        self.calls = self.billing_responses = 0
        self.max_in_flight = self.in_flight = 0
        self.release = threading.Event()

    def for_worker(self, k):
        return lambda request, timeout=None: self(request, timeout)

    def __call__(self, request, timeout=None):
        if request.full_url != openai_provider.URL:
            raise AssertionError('stub_unexpected_url')
        body = json.loads(request.data)
        if tuple(body) != openai_provider.BODY_KEYS or body['reasoning_effort'] != 'low':
            raise AssertionError('stub_body')
        with self.lock:
            self.calls += 1
            n = self.calls
            self.in_flight += 1
            self.max_in_flight = max(self.max_in_flight, self.in_flight)
        try:
            system, user = body['messages'][0]['content'], json.loads(body['messages'][1]['content'])
            if 'question' in user:
                ans = QA[user['question']]
                if self.mode == 'wrong':
                    ans = (not ans) if isinstance(ans, bool) else ans + 7
                text = json.dumps({'answer': ans})
            else:
                text = json.dumps(stub_action(user, 'Role overlay' in system))
            prompt = len(request.data) // 4
            return _Response(json.dumps({
                'id': f'chatcmpl-stub-{n:06d}', 'object': 'chat.completion', 'model': body['model'] + '-2026-09-30',
                'choices': [{'index': 0, 'finish_reason': 'stop', 'message': {'role': 'assistant', 'content': text, 'refusal': None}}],
                'usage': {'prompt_tokens': prompt, 'completion_tokens': 900, 'total_tokens': prompt + 900,
                          'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0},
                          'completion_tokens_details': {'reasoning_tokens': 600}}}).encode())
        finally:
            with self.lock:
                self.in_flight -= 1


FAST_TRANSPORT = {'silent_seconds': 30.0, 'live_every': 2.0, 'backoff_max': 1.0}


class JumpClock:
    """A clock whose sleeps advance it at once, so a 20-minute billing wait takes no real time."""
    def __init__(self):
        self.offset, self.lock = 0.0, threading.Lock()

    def now(self):
        with self.lock:
            return time.monotonic() + self.offset

    def sleep(self, seconds):
        with self.lock:
            self.offset += seconds


def block_network():
    """Every urllib request of this process must go to 127.0.0.1, one at a time.

    One at a time because the throwaway hub shares one SQLite connection between its request threads, and the
    SQLite build of this machine's Python (THREADSAFE=2) corrupts that connection under concurrent requests.
    All four hub clients of a rehearsal (coordinator and three workers) live in this process, so a lock here
    is enough. It says nothing about the production hub under three real workers."""
    original = urllib.request.urlopen
    gate = threading.Lock()

    class _Held:
        def __init__(self, response):
            self.response = response

        def __enter__(self):
            return self

        def __exit__(self, *a):
            try:
                self.response.close()
            finally:
                gate.release()
            return False

        def read(self, *a):
            return self.response.read(*a)

        def __getattr__(self, name):
            return getattr(self.response, name)

    def guarded(target, *args, **kwargs):
        url = target.full_url if isinstance(target, urllib.request.Request) else target
        if urllib.parse.urlparse(url).hostname != LOCAL:
            raise RuntimeError('rehearsal_network_blocked')
        gate.acquire()
        try:
            return _Held(original(target, *args, **kwargs))
        except BaseException:
            gate.release()
            raise
    urllib.request.urlopen = guarded


def free_port():
    with socket.socket() as s:
        s.bind((LOCAL, 0))
        return s.getsockname()[1]


def start_hub(hub_dir, data_dir, log):
    port, token = free_port(), secrets.token_hex(16)
    proc = subprocess.Popen([sys.executable, str(hub_dir / 'hub.py'), '--data', str(data_dir), '--bind', LOCAL,
                             '--port', str(port)], env={**os.environ, 'SWARM_HUB_TOKEN': token},
                            stdout=log, stderr=subprocess.STDOUT)
    os.environ.update(SWARM_HUB_URL=f'http://{LOCAL}:{port}', SWARM_HUB_TOKEN=token)
    return proc


def require_local(sr):
    urls = [os.environ.get('SWARM_HUB_URL', '')]
    if hasattr(sr, '_config'):
        urls.append(sr._config().get('SWARM_HUB_URL', ''))
    if any(urllib.parse.urlparse(u).hostname != LOCAL for u in urls):
        raise SystemExit('rehearse: refusing to run: the hub is not on 127.0.0.1')


def wait_for_hub(sr, proc):
    for _ in range(100):
        if proc.poll() is not None:
            raise SystemExit('rehearse: the throwaway hub exited')
        try:
            sr.runs(study.EXPERIMENT, limit=1)
            return
        except Exception:
            time.sleep(0.1)
    raise SystemExit('rehearse: the throwaway hub did not answer')


FAST_TRANSPORT = {'silent_seconds': 3.0, 'live_every': 0.5, 'backoff_max': 1.0}


def scenario(sr, hub_dir, tmp, name, stub, stages, verify=False, transport_options=None):
    """One chain with three worker threads on a fresh hub, results directory and ledger."""
    base = tmp / name
    base.mkdir()
    with (base / 'hub.log').open('w') as log:
        proc = start_hub(hub_dir, base / 'hubdata', log)
        stop = threading.Event()
        clock = JumpClock()
        workers = study.design()['workers']
        exits = [None] * workers

        def work(k):
            exits[k] = transport.serve(sr, base / f'worker-{k}', opener=stub.for_worker(k), poll=0.2, attach_seconds=600, stop=stop,
                                       api_clock=clock.now, api_sleep=clock.sleep, backoff_max=1.0)
        threads = [threading.Thread(target=work, args=(k,), daemon=True, name=f'rehearsal-worker-{k}') for k in range(workers)]
        try:
            require_local(sr)
            wait_for_hub(sr, proc)
            for t in threads:
                t.start()
            started = time.monotonic()
            ledger = base / 'ledger' / 'ledger.jsonl'
            code = chain.run_chain(stages, sr, base / 'results', ledger, allow_shared_host=True, poll=0.05,
                                   transport_options=dict(FAST_TRANSPORT, **(transport_options or {})))
            elapsed = time.monotonic() - started
            for t in threads:
                t.join(timeout=30)
            status = chain.read_status(base / 'results')
            runs = {(r.get('params') or {}).get('stage') or r['run']: r for r in sr.runs(study.EXPERIMENT, limit=5000)}
            session_runs = []
            report, replay = None, None
            if verify:
                t0 = time.monotonic()
                report = chain.verify(sr, base / 'results', ledger)
                report['seconds'] = time.monotonic() - t0
                try:
                    coordinator.gate(sr.runs(study.EXPERIMENT, limit=5000), 'S0', study.params('S0'))
                    replay = False
                except ValueError as exc:
                    replay = str(exc) == 'batch_exists_no_replay'
            totals = transport.FastLedger(ledger, study.design()['budget']).transact() if ledger.exists() else None
            return {'exit': code, 'seconds': elapsed, 'status': status, 'runs': runs, 'verify': report, 'replay_refused': replay,
                    'ledger': totals, 'stub_calls': stub.calls, 'stub_billing_responses': stub.billing_responses,
                    'max_in_flight': stub.max_in_flight, 'worker_exits': exits, 'session_runs': session_runs,
                    'spooled': list((tmp / 'spool').glob('*.json')) if (tmp / 'spool').exists() else []}
        finally:
            stub.release.set()
            stop.set()
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()


def brief(run):
    status = run['status'] or {}
    stages = {s: {k: e.get(k) for k in ('status', 'reason', 'calls', 'accepted', 'void', 'cost_usd', 'elapsed_seconds',
                                        'batches_admitted') if e.get(k) is not None}
              for s, e in (status.get('stages') or {}).items()}
    return {'exit': run['exit'], 'seconds': round(run['seconds'], 1), 'state': status.get('state'),
            'stopped_stage': status.get('stopped_stage'), 'reason': status.get('reason'), 'stages': stages,
            'ledger_calls': (run['ledger'] or {}).get('attempted_calls'), 'stub_calls': run['stub_calls'],
            'max_in_flight_seen_by_stub': run['max_in_flight'], 'worker_exits': run['worker_exits']}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--hub-dir', required=True)
    ap.add_argument('--only', default='a,b,d')
    a = ap.parse_args(argv)
    hub_dir = Path(a.hub_dir).resolve()
    tmp = Path(tempfile.mkdtemp(prefix='gp200-rehearsal-'))
    if study.ROOT in tmp.resolve().parents:
        raise SystemExit('rehearse: temporary directory is inside the study tree')
    for k in ('STUDY_MODEL', 'STUDY_PROVIDER', 'STUDY_REPLICATION', openai_provider.LEDGER_ENV, 'STUDY_RESULTS_DIR'):
        os.environ.pop(k, None)
    os.environ.update(SWARM_HUB_URL=f'http://{LOCAL}:1', SWARM_HUB_TOKEN='unset-until-hub-starts', SWARM_SOURCE='rehearsal/local',
                      SWARM_SPOOL=str(tmp / 'spool'), SWARM_NO_AUTO_REFRESH='1', SWARM_OPENAI_API_KEY='rehearsal-stub-not-a-key')
    block_network()
    sys.path.insert(0, str(hub_dir))
    import swarm_report as sr
    require_local(sr)
    only = set(a.only.split(','))
    stages = list(study.STAGES)
    budget = study.design()['budget']
    checks, result = {}, {}
    try:
        if 'a' in only:
            run = scenario(sr, hub_dir, tmp, 'a', Stub('good'), stages, verify=True)
            runs, status = run['runs'], run['status'] or {}
            s1 = (status.get('stages') or {}).get('S1', {})
            x0 = (status.get('stages') or {}).get('X0', {})
            checks['a_exit_zero'] = run['exit'] == 0 and status.get('state') == 'completed'
            checks['a_all_stages_done'] = all(runs.get(s, {}).get('status') == 'done' for s in stages)
            checks['a_admitted_one_batch'] = x0.get('batches_admitted') == 1 and s1.get('batches_admitted') == 1
            checks['a_s1_calls'] = (runs.get('S1', {}).get('metrics') or {}).get('model_calls') == 17000
            checks['a_qualification_calls'] = sum((runs.get(s, {}).get('metrics') or {}).get('model_calls', 0) for s in ('P0', 'Q0', 'X0')) == 3096
            checks['a_twenty_rounds_each'] = s1.get('rounds_completed') and all(v == 20 for v in s1['rounds_completed'].values()) and len(s1['rounds_completed']) == 4
            checks['a_in_flight_at_most_128'] = 0 < run['max_in_flight'] <= budget['governor']['max_in_flight_total']
            checks['a_t0_and_stop_recorded'] = bool(status.get('t0') and status.get('dispatch_stop'))
            checks['a_verify_ok'] = bool(run['verify'] and run['verify']['ok'])
            checks['a_replay_refused'] = run['replay_refused'] is True
            checks['a_workers_closed'] = all(e == 0 for e in run['worker_exits'])
            result['full_chain'] = brief(run)
            result['verify_failed_checks'] = {s: [k for k, ok in v.get('checks', {}).items() if ok is not True]
                                              for s, v in (run['verify'] or {}).get('stages', {}).items() if not v.get('ok')}
        if 'b' in only:
            run = scenario(sr, hub_dir, tmp, 'b', Stub('wrong'), stages)
            runs, status = run['runs'], run['status'] or {}
            checks['b_stopped_at_q0'] = run['exit'] == chain.EXIT_STOPPED and status.get('stopped_stage') == 'Q0'
            checks['b_no_later_stage'] = not any(s in runs for s in ('X0', 'S1'))
            result['failed_gate_chain'] = brief(run)
        if 'd' in only:
            run = scenario(sr, hub_dir, tmp, 'd', Stub('good'), stages, transport_options={'dispatch_stop_seconds': 25})
            runs, status = run['runs'], run['status'] or {}
            s1 = (status.get('stages') or {}).get('S1') or {}
            checks['d_stopped_by_deadline'] = run['exit'] == chain.EXIT_STOPPED and str(status.get('reason')).startswith(('dispatch_deadline', 'gate_failed', 'no_batches')) is not None
            checks['d_stop_reason'] = status.get('reason') == 'dispatch_deadline'
            checks['d_records_kept'] = bool(s1.get('results_dir')) and (Path(s1['results_dir']) / 'rounds.jsonl.gz').exists()
            result['deadline_chain'] = brief(run)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    result = dict({'rehearsal': 'passed' if checks and all(checks.values()) else 'FAILED', 'checks': checks,
                   'source_hash': study.source_hash(), 'model_calls_made': 0}, **result)
    print(json.dumps(result, sort_keys=True, default=str))
    return 0 if checks and all(checks.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
