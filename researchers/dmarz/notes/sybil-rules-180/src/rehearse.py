"""Offline rehearsal of the whole chain: a throwaway hub on 127.0.0.1, three worker threads, a local model stub.

    python3 src/rehearse.py --hub-dir <dir with hub.py and swarm_report.py> [--only a,b,c,d]

Scenarios, each on a fresh hub, results directory and ledger:
  a  S0, P0, Q0, X0, S1, D1 to completion with three workers and a stub policy that sometimes splits;
     then `chain verify`, and a second chain on the same hub must be refused (no replay).
  b  a stub that produces nothing fails the ordinary-profit gate: the chain stops at Q0 and no later stage exists.
  c  a billing outage (HTTP 402) during Q0 that ends: dispatch pauses, the same call is re-sent, the stage passes.
  d  a billing outage that never ends: the stage stops with provider_credit_balance_low and the chain stops.
  e  a stub that returns unusable answers for a third of the owners in one branch: that branch stops under the
     material rule, the other branches and the cue diagnostic still run, the chain exits 3.

It refuses any hub that is not on 127.0.0.1 and blocks every other network destination for the process.
A rehearsal answer is never a sample and never leaves the machine. No model call is made.
"""
import argparse
import io
import json
import os
import re
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
import provider
import study
import transport
import worker

LOCAL = '127.0.0.1'


class _Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def stub_action(obs, mode='mixed'):
    """A policy that sees only what a model sees. It sometimes splits a product across two firms."""
    firms = obs['portfolio']['firms']
    reserve = obs['portfolio']['reserve']
    start = firms[0]['product']
    other = 'B' if start == 'A' else 'A'
    me = obs['you']
    market, letter = int(me[4:6]), me[6]
    splits = (letter == 'a' and market % 5 in (1, 2, 4)) or (letter != 'a' and market % 4 == 0)
    same = [f for f in firms if f['product'] == start]
    others = [f for f in firms if f['product'] == other]
    room = len(firms) < obs['portfolio']['max_firms']
    admin = {'command': 'noop'}
    check = obs.get('interface_check')
    if check:
        admin = json.loads(re.search(r'command: (\{.*\})\. Choose', check).group(1))
    elif splits and len(same) == 1 and room:
        admin = {'command': 'register', 'product': start}
    elif splits and len(same) == 2 and same[1]['capacity'] == 0 and same[0]['capacity'] >= 2:
        admin = {'command': 'transfer', 'from': same[0]['firm'], 'to': same[1]['firm'], 'amount': same[0]['capacity'] // 2}
    elif not others and room:
        admin = {'command': 'register', 'product': other}
    elif others and reserve[other] > 0:
        admin = {'command': 'transfer', 'from': 'reserve', 'to': others[0]['firm'], 'amount': reserve[other]}
    production = {}
    for f in firms:
        cap = f['capacity']
        if admin['command'] == 'transfer' and admin['from'] == f['firm']:
            cap -= admin['amount']
        total = sum(x['capacity'] for x in firms if x['product'] == f['product'])
        production[f['firm']] = 0 if mode == 'idle' else int(cap * (0.65 if total >= 300 else 1.0))
    message = ''
    if 'message_recipients' in obs and splits and len(same) == 2 and obs['round'] % 3 == 0:
        message = 'Two firms in the same product keep the published concentration under the threshold.'
    return {'memo': f'round {obs["round"]}: keep plan', 'admin': admin, 'production': production, 'message': message}


class Stub:
    """Stands in for the provider endpoint, in the real response shape (model, provider, choices, usage with cost).

    mode 'mixed'   stub_action
    mode 'idle'    stub_action producing nothing (fails the ordinary-profit gate)
    `billing`      (first_call, count): calls from `first_call` on get HTTP 402 `count` times (None = for ever)
    `garbage`      a function of the observation; where true the answer is text that is not JSON
    """
    def __init__(self, mode='mixed', billing=None, garbage=None):
        self.mode, self.billing, self.garbage = mode, billing, garbage
        self.lock = threading.Lock()
        self.calls = self.billing_responses = 0
        self.max_in_flight = self.in_flight = 0

    def __call__(self, request, timeout=None):
        if request.full_url != provider.URL:
            raise AssertionError('stub_unexpected_url')
        headers = {k.lower(): v for k, v in request.header_items()}
        if not headers.get('authorization', '').startswith('Bearer '):
            raise AssertionError('stub_missing_headers')
        body = json.loads(request.data)
        if tuple(body) != provider.BODY_KEYS:
            raise AssertionError('stub_body_keys')
        with self.lock:
            self.in_flight += 1
            self.max_in_flight = max(self.max_in_flight, self.in_flight)
            n = self.calls + 1
            blocked = bool(self.billing and n >= self.billing[0] and (self.billing[1] is None or self.billing_responses < self.billing[1]))
            if blocked:
                self.billing_responses += 1
            else:
                self.calls = n
        try:
            if blocked:
                raise urllib.error.HTTPError(provider.URL, 402, 'Payment Required', {'x-request-id': 'stub'},
                                             io.BytesIO(b'{"error":{"code":402,"message":"Insufficient credits"}}'))
            obs = json.loads(body['messages'][1]['content'])
            text = json.dumps(stub_action(obs, self.mode))
            if self.garbage and self.garbage(obs):
                text = 'I cannot answer in the requested format'
            tokens_in, tokens_out = len(request.data) // 4, len(text) // 4
            return _Response(json.dumps({
                'id': f'gen-stub-{n:06d}', 'model': study.design()['canonical_model'], 'provider': 'Alibaba',
                'choices': [{'finish_reason': 'stop', 'message': {'role': 'assistant', 'content': text}}],
                'usage': {'prompt_tokens': tokens_in, 'completion_tokens': tokens_out, 'total_tokens': tokens_in + tokens_out,
                          'cost': (tokens_in * 0.03 + tokens_out * 0.13) / 1e6,
                          'completion_tokens_details': {'reasoning_tokens': 0}}}).encode())
        finally:
            with self.lock:
                self.in_flight -= 1


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


def scenario(sr, hub_dir, tmp, name, stub, stages, verify=False):
    """One chain with three worker threads on a fresh hub, results directory and ledger."""
    base = tmp / name
    base.mkdir()
    with (base / 'hub.log').open('w') as log:
        proc = start_hub(hub_dir, base / 'hubdata', log)
        stop = threading.Event()
        clock = JumpClock()
        exits = [None] * 3

        def work(k):
            exits[k] = transport.serve(sr, base / f'worker-{k}', opener=stub, poll=0.2, attach_seconds=600, stop=stop,
                                       api_clock=clock.now, api_sleep=clock.sleep)
        threads = [threading.Thread(target=work, args=(k,), daemon=True) for k in range(3)]
        try:
            require_local(sr)
            wait_for_hub(sr, proc)
            for t in threads:
                t.start()
            started = time.monotonic()
            ledger = base / 'ledger' / 'ledger.jsonl'
            code = chain.run_chain(stages, sr, base / 'results', ledger, allow_shared_host=True, poll=0.05)
            elapsed = time.monotonic() - started
            for t in threads:
                t.join(timeout=30)
            status = chain.read_status(base / 'results')
            runs = {(r.get('params') or {}).get('stage') or r['run']: r for r in sr.runs(study.EXPERIMENT, limit=5000)}
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
                    'max_in_flight': stub.max_in_flight, 'worker_exits': exits,
                    'spooled': list((tmp / 'spool').glob('*.json')) if (tmp / 'spool').exists() else []}
        finally:
            stop.set()
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()


def brief(run):
    status = run['status'] or {}
    stages = {s: {k: e.get(k) for k in ('status', 'reason', 'calls', 'accepted', 'void', 'rejected_commands', 'cost_usd',
                                        'elapsed_seconds', 'in_flight_per_host', 'billing') if e.get(k) is not None}
              for s, e in (status.get('stages') or {}).items()}
    return {'exit': run['exit'], 'seconds': round(run['seconds'], 1), 'state': status.get('state'),
            'stopped_stage': status.get('stopped_stage'), 'reason': status.get('reason'), 'stages': stages,
            'ledger_calls': (run['ledger'] or {}).get('attempted_calls'), 'stub_calls': run['stub_calls'],
            'max_in_flight_seen_by_stub': run['max_in_flight'], 'worker_exits': run['worker_exits'],
            'stub_cost_usd_not_real': (run['ledger'] or {}).get('actual_usd')}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--hub-dir', required=True, help='directory with hub.py and swarm_report.py (not part of this repo)')
    ap.add_argument('--only', default='a,b,c,d,e')
    ap.add_argument('--keep', action='store_true', help='keep the temporary directory and print its path')
    a = ap.parse_args(argv)
    hub_dir = Path(a.hub_dir).resolve()
    if not (hub_dir / 'hub.py').is_file() or not (hub_dir / 'swarm_report.py').is_file():
        raise SystemExit('rehearse: --hub-dir needs hub.py and swarm_report.py')
    tmp = Path(tempfile.mkdtemp(prefix='rules180-rehearsal-'))
    if study.ROOT in tmp.resolve().parents:
        raise SystemExit('rehearse: temporary directory is inside the study tree')
    os.environ.update(SWARM_HUB_URL=f'http://{LOCAL}:1', SWARM_HUB_TOKEN='unset-until-hub-starts',
                      SWARM_SOURCE='rehearsal/local', SWARM_SPOOL=str(tmp / 'spool'), SWARM_NO_AUTO_REFRESH='1',
                      SWARM_OPENROUTER_API_KEY='rehearsal-stub-not-a-key')
    os.environ.pop(provider.LEDGER_ENV, None)
    os.environ.pop('STUDY_RESULTS_DIR', None)
    block_network()
    sys.path.insert(0, str(hub_dir))
    import swarm_report as sr
    require_local(sr)
    only = set(a.only.split(','))
    all_stages = list(study.STAGES)
    budget = study.design()['budget']
    required = set(worker.REQUIRED_METRICS)
    checks, result = {}, {}
    try:
        if 'a' in only:
            run = scenario(sr, hub_dir, tmp, 'a', Stub('mixed'), all_stages, verify=True)
            runs, status = run['runs'], run['status'] or {}
            checks['a_exit_zero'] = run['exit'] == 0
            checks['a_state_completed'] = status.get('state') == 'completed'
            checks['a_all_stages_done'] = all(runs.get(s, {}).get('status') == 'done' for s in all_stages)
            checks['a_metrics_reported'] = all(required <= set(runs.get(s, {}).get('metrics') or {}) for s in all_stages)
            checks['a_calls_per_stage'] = {s: (runs.get(s, {}).get('metrics') or {}).get('model_calls') for s in all_stages} == budget['max_calls']
            checks['a_ledger_total_calls'] = run['ledger']['attempted_calls'] == budget['max_attempted_calls'] == run['stub_calls']
            checks['a_three_workers_closed'] = run['worker_exits'] == [0, 0, 0]
            checks['a_three_sessions_done'] = sum(r.get('status') == 'done' and (r.get('params') or {}).get('role') == transport.SESSION_ROLE
                                                  for r in runs.values()) == 3
            checks['a_in_flight_within_nine'] = 0 < run['max_in_flight'] <= 3 * budget['in_flight_per_host_max']
            s1 = (status.get('stages') or {}).get('S1', {})
            checks['a_checkpoint_fork'] = (sorted(s1.get('branches') or {}) == ['A', 'A2', 'B', 'C'] and
                                           {b['restored_hash'] for b in s1['branches'].values()} == {s1.get('checkpoint_hash')})
            checks['a_verify_ok'] = bool(run['verify'] and run['verify']['ok'])
            checks['a_replay_refused'] = run['replay_refused'] is True
            checks['a_nothing_spooled'] = not run['spooled']
            result['full_chain'] = brief(run)
            result['verify'] = {'seconds': round(run['verify']['seconds'], 1), 'ledger': run['verify'].get('ledger'),
                                'stages': {s: v.get('ok') for s, v in run['verify']['stages'].items()},
                                'failed_checks': {s: [k for k, ok in v.get('checks', {}).items() if ok is not True]
                                                  for s, v in run['verify']['stages'].items() if not v.get('ok')}}
        if 'b' in only:
            run = scenario(sr, hub_dir, tmp, 'b', Stub('idle'), all_stages)
            runs, status = run['runs'], run['status'] or {}
            checks['b_exit_stopped'] = run['exit'] == chain.EXIT_STOPPED
            checks['b_stopped_at_q0'] = status.get('state') == 'stopped_at_gate' and status.get('stopped_stage') == 'Q0'
            checks['b_no_later_stage'] = not any(s in runs or s in (status.get('stages') or {}) for s in ('X0', 'S1', 'D1'))
            checks['b_q0_failed_with_metrics'] = (runs.get('Q0', {}).get('status') == 'failed' and required <= set(runs['Q0'].get('metrics') or {})
                                                  and runs['Q0']['metrics'].get('qualification_passed') == 0)
            checks['b_calls_stopped_at_186'] = run['ledger']['attempted_calls'] == 186 == run['stub_calls']
            checks['b_workers_released'] = run['worker_exits'] == [0, 0, 0]
            result['failed_qualification_chain'] = brief(run)
        if 'c' in only:
            run = scenario(sr, hub_dir, tmp, 'c', Stub('mixed', billing=(40, 3)), ['S0', 'P0', 'Q0'])
            status = run['status'] or {}
            q0 = (status.get('stages') or {}).get('Q0', {})
            checks['c_exit_zero'] = run['exit'] == 0
            checks['c_pause_recorded'] = (q0.get('billing') or {}).get('billing_pauses', 0) >= 1 and (q0.get('billing') or {}).get('billing_pause_seconds', 0) >= 60
            checks['c_no_call_lost'] = q0.get('accepted') == q0.get('calls') == budget['max_calls']['Q0'] and q0.get('void') == 0
            checks['c_resent_not_recounted'] = run['ledger']['attempted_calls'] == 186 == run['stub_calls'] and run['stub_billing_responses'] == 3
            result['billing_pause_chain'] = brief(run)
        if 'd' in only:
            run = scenario(sr, hub_dir, tmp, 'd', Stub('mixed', billing=(40, None)), ['S0', 'P0', 'Q0', 'X0'])
            runs, status = run['runs'], run['status'] or {}
            checks['d_exit_stopped'] = run['exit'] == chain.EXIT_STOPPED
            checks['d_reason_billing'] = status.get('stopped_stage') == 'Q0' and status.get('reason') == provider.BILLING_STOP
            checks['d_no_later_stage'] = 'X0' not in runs
            checks['d_waited_twenty_minutes'] = ((status.get('stages') or {}).get('Q0', {}).get('billing') or {}).get('billing_pause_seconds', 0) >= 1200
            result['billing_stop_chain'] = brief(run)
        if 'e' in only:
            def garbage(obs):
                # a third of the owners, in the owner-level branch only (its rule text names beneficial owners), from round 6
                return 'beneficial owners' in obs['rules']['text'] and obs['round'] >= 6 and 'message_recipients' in obs \
                    and len(obs['market']['owners']) == 3 and int(obs['you'][4:6]) % 3 == 0 and obs['you'].startswith('own-') \
                    and obs['market']['owners'][0][:6] in [f'own-{m:02d}' for m in range(60)] and len(obs.get('history', [])) == 3 \
                    and obs['portfolio']['max_firms'] == 4 and len(obs['portfolio']['firms']) < 4 and not obs.get('interface_check') and obs['round'] <= 12 and _is_main(obs)
            run = scenario(sr, hub_dir, tmp, 'e', Stub('mixed', garbage=garbage), all_stages, verify=True)
            runs, status = run['runs'], run['status'] or {}
            s1 = (status.get('stages') or {}).get('S1', {})
            branches = s1.get('branches') or {}
            checks['e_exit_stopped'] = run['exit'] == chain.EXIT_STOPPED
            checks['e_state'] = status.get('state') == 'completed_with_stopped_branch'
            checks['e_only_C_stopped'] = {b: i.get('status') for b, i in branches.items()} == {'A': 'completed', 'A2': 'completed', 'B': 'completed', 'C': 'stopped'}
            checks['e_C_reason'] = str(branches.get('C', {}).get('reason', '')).startswith('round_void_limit')
            checks['e_s1_failed_but_diagnostic_ran'] = runs.get('S1', {}).get('status') == 'failed' and runs.get('D1', {}).get('status') == 'done'
            checks['e_verify_ok'] = bool(run['verify'] and run['verify']['ok'])
            result['stopped_branch_chain'] = brief(run)
            result['stopped_branch_verify_failed_checks'] = {s: [k for k, ok in v.get('checks', {}).items() if ok is not True]
                                                             for s, v in run['verify']['stages'].items() if not v.get('ok')}
        checks['committed_tree_untouched'] = not (study.ROOT / 'results').exists() or not any((study.ROOT / 'results').iterdir())
    finally:
        if a.keep:
            print(f'rehearsal files kept in {tmp}', file=sys.stderr)
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    result = dict({'rehearsal': 'passed' if checks and all(checks.values()) else 'FAILED', 'scenarios': sorted(only), 'checks': checks,
                   'source_hash': study.source_hash(), 'model_calls_made': 0}, **result)
    print(json.dumps(result, sort_keys=True))
    return 0 if checks and all(checks.values()) else 1


def _is_main(obs):
    """The 60-market economy is the only one whose owners list four message recipients."""
    return len(obs.get('message_recipients', [])) == 4


if __name__ == '__main__':
    sys.exit(main())
