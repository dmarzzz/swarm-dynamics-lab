"""Offline rehearsal of the whole chain against a throwaway hub on 127.0.0.1 and a local model stub.

    python3 src/rehearse.py --hub-dir <dir with hub.py and swarm_report.py>

Runs the chain three times, each on a fresh hub, in fresh temporary result and ledger directories:
  (a) S0, P0, Q0, S1 to completion with a stub that answers every call by the private-evidence
      reference policy (and posts claims by the scripted rule), then `chain verify`;
  (b) with a stub that skips on any suspicious inspection, which must fail Q0, stop the chain with
      exit 3, and leave no S1 run on the hub;
  (c) with the reference stub and one HTTP 500 during S1, which must end that episode, stop new
      dispatch, record every remaining call as not started and still report usage.

The stub reads the request exactly as the provider sends it, so each later round's answer depends
on the board that earlier stub answers produced. It refuses any hub that is not on 127.0.0.1 and
blocks every other network destination for the process. A rehearsal answer is never a sample and
never leaves the machine. No model call is made.
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

import analyze
import chain
import coordinator
import provider
import study
import worker

LOCAL = '127.0.0.1'


class _Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class Stub:
    """Stands in for the model endpoint. Answers count_tokens and messages requests in the real
    response shape: a thinking block before one text block, model id, stop reason and usage.

    mode 'private': the private-evidence reference decision for the packet in the request, with
                    claims by the scripted rule.
    mode 'jumpy':   skip on any suspicious inspection (an over-cautious agent); fails Q0.
    `fail_at`: the n-th messages request of the chain is answered with HTTP 500 (scenario c).
    """
    def __init__(self, mode='private', output_tokens=600, fail_at=None, hold=0.002):
        self.mode, self.output_tokens, self.fail_at, self.hold = mode, output_tokens, fail_at, hold
        self.lock = threading.Lock()
        self.count_calls = self.message_calls = self.in_flight = self.max_in_flight = 0

    def __call__(self, request, timeout=None):
        url = request.full_url
        if url not in (provider.COUNT_URL, provider.MESSAGES_URL):
            raise AssertionError('stub_unexpected_url')
        headers = {k.lower(): v for k, v in request.header_items()}
        if not headers.get('x-api-key') or headers.get('anthropic-version') != '2023-06-01':
            raise AssertionError('stub_missing_headers')
        body = json.loads(request.data)
        tokens = len(request.data) // 3            # rough: about 3 characters per token for this JSON
        if url == provider.COUNT_URL:
            if tuple(body) != tuple(k for k in provider.REQUEST_KEYS if k != 'max_tokens'):
                raise AssertionError('stub_count_body_keys')
            with self.lock:
                self.count_calls += 1
            return _Response(json.dumps({'input_tokens': tokens}).encode())
        if tuple(body) != provider.REQUEST_KEYS or set(body['output_config']) != {'effort', 'format'}:
            raise AssertionError('stub_message_body_keys')
        if body['system'] != study.SYSTEM or body['output_config']['format']['schema'] != study.schema():
            raise AssertionError('stub_prompt_or_schema')
        packet = json.loads(body['messages'][0]['content'])
        with self.lock:
            self.message_calls += 1
            n = self.message_calls
            self.in_flight += 1
            self.max_in_flight = max(self.max_in_flight, self.in_flight)
        try:
            time.sleep(self.hold)                   # long enough for concurrent requests to overlap
            if self.fail_at is not None and n == self.fail_at:
                raise urllib.error.HTTPError(url, 500, 'stub failure', {}, io.BytesIO(b'{}'))
            answer = study.jumpy_answer(packet) if self.mode == 'jumpy' else study.scripted_answer(packet, 'private', True)
            answer['rationale'] = 'Stub answer from own inspection counts.'
        finally:
            with self.lock:
                self.in_flight -= 1
        return _Response(json.dumps({
            'id': f'msg_stub_{n:06d}', 'type': 'message', 'role': 'assistant', 'model': body['model'],
            'content': [{'type': 'thinking', 'thinking': '', 'signature': 'stub'},
                        {'type': 'text', 'text': json.dumps(answer)}],
            'stop_reason': 'end_turn', 'stop_sequence': None,
            'usage': {'input_tokens': tokens, 'output_tokens': self.output_tokens,
                      'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0}}).encode())


def block_network():
    """Every urllib request of this process must go to 127.0.0.1."""
    original = urllib.request.urlopen

    def guarded(target, *args, **kwargs):
        url = target.full_url if isinstance(target, urllib.request.Request) else target
        if urllib.parse.urlparse(url).hostname != LOCAL:
            raise RuntimeError('rehearsal_network_blocked')
        return original(target, *args, **kwargs)
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


def stage_runs(sr):
    return {(r.get('params') or {}).get('stage'): r for r in sr.runs(study.EXPERIMENT, limit=5000)}


def scenario(sr, hub_dir, tmp, name, stub, stages, verify=False):
    """One chain on a fresh hub, fresh results directory and fresh ledger."""
    base = tmp / name
    base.mkdir()
    with (base / 'hub.log').open('w') as log:
        proc = start_hub(hub_dir, base / 'hubdata', log)
        try:
            require_local(sr)
            wait_for_hub(sr, proc)
            started = time.monotonic()
            code = chain.run_chain(stages, sr, base / 'results', base / 'ledger' / 'ledger.jsonl', opener=stub)
            elapsed = time.monotonic() - started
            status = chain.read_status(base / 'results')
            runs = stage_runs(sr)
            report = None
            replay_refused = None
            if verify:
                started_verify = time.monotonic()
                report = chain.verify(sr, base / 'results')
                report['seconds'] = time.monotonic() - started_verify
            if name == 'a':
                try:
                    coordinator.enqueue(sr, 'S0')
                    replay_refused = False
                except ValueError as exc:
                    replay_refused = str(exc) == 'batch_exists_no_replay'
            rows = None
            entry = ((status or {}).get('stages') or {}).get('S1')
            if entry and entry.get('results_dir') and (Path(entry['results_dir']) / 'episodes.jsonl.gz').exists():
                rows = analyze.read_rows(Path(entry['results_dir']) / 'episodes.jsonl.gz')
            ledger = provider.Ledger(base / 'ledger' / 'ledger.jsonl').transact()
            return {'exit': code, 'seconds': elapsed, 'status': status, 'runs': runs, 'verify': report,
                    'replay_refused': replay_refused, 'ledger': ledger, 's1_rows': rows,
                    'stub_messages': stub.message_calls, 'stub_counts': stub.count_calls,
                    'max_in_flight': stub.max_in_flight}
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--hub-dir', required=True, help='directory with hub.py and swarm_report.py (not part of this repo)')
    ap.add_argument('--keep', action='store_true', help='keep the temporary directory and print its path')
    a = ap.parse_args(argv)
    hub_dir = Path(a.hub_dir).resolve()
    if not (hub_dir / 'hub.py').is_file() or not (hub_dir / 'swarm_report.py').is_file():
        raise SystemExit('rehearse: --hub-dir needs hub.py and swarm_report.py')
    tmp = Path(tempfile.mkdtemp(prefix='false-alarm-rehearsal-'))
    if study.ROOT in tmp.resolve().parents:
        raise SystemExit('rehearse: temporary directory is inside the study tree')
    # The client reads these; nothing points outside this machine and the model key is a dummy.
    os.environ.update(SWARM_HUB_URL=f'http://{LOCAL}:1', SWARM_HUB_TOKEN='unset-until-hub-starts',
                      SWARM_SOURCE='rehearsal/local', SWARM_SPOOL=str(tmp / 'spool'), SWARM_NO_AUTO_REFRESH='1',
                      SWARM_MODEL_API_KEY='rehearsal-stub-not-a-key', SWARM_MODEL_WORKSPACE_ID='rehearsal-stub')
    os.environ.pop(provider.LEDGER_ENV, None)
    os.environ.pop('STUDY_RESULTS_DIR', None)
    block_network()
    sys.path.insert(0, str(hub_dir))
    import swarm_report as sr
    require_local(sr)

    stages = list(study.STAGES)
    d = study.design()
    budget = d['budget']
    required = set(worker.REQUIRED_METRICS)
    paid_before_s1 = budget['max_calls']['P0'] + budget['max_calls']['Q0']
    per_round = len(d['world']['members']) - 1
    checks = {}
    try:
        a_run = scenario(sr, hub_dir, tmp, 'a', Stub('private'), stages, verify=True)
        runs = a_run['runs']
        checks['a_exit_zero'] = a_run['exit'] == 0
        checks['a_state_completed'] = (a_run['status'] or {}).get('state') == 'completed'
        checks['a_all_stages_done'] = all(runs.get(s, {}).get('status') == 'done' for s in stages)
        checks['a_metrics_reported'] = all(required <= set(runs.get(s, {}).get('metrics') or {}) for s in stages)
        checks['a_calls_per_stage'] = {s: (runs.get(s, {}).get('metrics') or {}).get('model_calls') for s in stages} == budget['max_calls']
        checks['a_gates_passed'] = all((runs.get(s, {}).get('metrics') or {}).get('qualification_passed') == 1 for s in stages[:3])
        checks['a_ledger_total_calls'] = a_run['ledger']['attempted_calls'] == budget['max_attempted_calls'] == a_run['stub_messages']
        checks['a_verify_ok'] = bool(a_run['verify'] and a_run['verify']['ok'])
        checks['a_replay_refused'] = a_run['replay_refused'] is True
        s1 = (runs.get('S1', {}).get('metrics') or {})
        checks['a_team_episodes_complete'] = s1.get('team_episodes') == s1.get('team_episodes_complete') == d['stages']['S1']['episodes']
        checks['a_requests_in_flight_within_limit'] = 1 < a_run['max_in_flight'] <= budget['workers']
        # The stub is the private-evidence policy, so the paired contrast must be exactly zero.
        checks['a_reference_stub_shows_zero_effect'] = s1.get('residual_avoidance_pp') == 0 and s1.get('cascade_size_pp') == 0
        rows = a_run['s1_rows'] or []
        boards = [len(r['packet']['board']) for r in rows if r.get('packet') and r['round'] == d['world']['rounds']]
        checks['a_later_rounds_carry_earlier_answers'] = bool(boards) and min(boards) > 0 and all(
            len(r['packet']['your_decisions']['r01']) == r['round'] - 1 for r in rows)

        b_run = scenario(sr, hub_dir, tmp, 'b', Stub('jumpy'), stages)
        runs = b_run['runs']
        status = b_run['status'] or {}
        checks['b_exit_stopped'] = b_run['exit'] == chain.EXIT_STOPPED
        checks['b_state_stopped_at_gate'] = status.get('state') == 'stopped_at_gate' and status.get('stopped_stage') == 'Q0'
        checks['b_no_s1_run_on_hub'] = 'S1' not in runs and 'S1' not in (status.get('stages') or {})
        checks['b_q0_failed_with_metrics'] = (runs.get('Q0', {}).get('status') == 'failed'
                                              and required <= set(runs.get('Q0', {}).get('metrics') or {})
                                              and (runs['Q0']['metrics']).get('qualification_passed') == 0)
        checks['b_s0_p0_done'] = all(runs.get(s, {}).get('status') == 'done' for s in ('S0', 'P0'))
        checks['b_calls_stopped_before_s1'] = b_run['ledger']['attempted_calls'] == paid_before_s1 == b_run['stub_messages']

        fail_at = paid_before_s1 + 2 * per_round + 3          # the third call of the third S1 round dispatched
        c_run = scenario(sr, hub_dir, tmp, 'c', Stub('private', fail_at=fail_at), stages, verify=True)
        runs = c_run['runs']
        status = c_run['status'] or {}
        rows = c_run['s1_rows'] or []
        failed = [r for r in rows if r['status'] == 'failed']
        checks['c_exit_stopped'] = c_run['exit'] == chain.EXIT_STOPPED
        checks['c_stopped_at_s1'] = (status.get('state') == 'stopped_at_gate' and status.get('stopped_stage') == 'S1'
                                     and status.get('reason') == 'invalid_rows:http_500')
        checks['c_s1_failed_with_metrics'] = (runs.get('S1', {}).get('status') == 'failed'
                                              and required <= set(runs.get('S1', {}).get('metrics') or {}))
        checks['c_one_failed_call_rest_accounted'] = (
            len(rows) == budget['max_calls']['S1'] and len(failed) == 1 and failed[0].get('error') == 'http_500'
            and sum(r['status'] == 'not_started' for r in rows) + sum(r['status'] == 'completed' for r in rows) + 1 == len(rows))
        # No round was dispatched after the failure: at most the calls of the two episodes in flight.
        started = len(rows) - sum(r['status'] == 'not_started' for r in rows)
        checks['c_dispatch_stopped'] = started <= fail_at - paid_before_s1 + budget['workers'] and started == c_run['stub_messages'] - paid_before_s1
        episode = failed[0]['episode'] if failed else None
        later = [r for r in rows if r['episode'] == episode and r['round'] > failed[0]['round']] if failed else []
        checks['c_failed_episode_ends_there'] = bool(later) and all(r['status'] == 'not_started' and 'packet' not in r for r in later)
        checks['c_verify_ok_on_partial_stage'] = bool(c_run['verify'] and c_run['verify']['ok'])
        checks['c_usage_reported'] = (runs.get('S1', {}).get('metrics') or {}).get('model_calls') == started

        checks['nothing_spooled'] = not list((tmp / 'spool').glob('*.json')) if (tmp / 'spool').exists() else True
        checks['committed_tree_untouched'] = not (study.ROOT / 'results').exists() or not any((study.ROOT / 'results').iterdir())

        def brief(run):
            stages_out = {}
            for s, e in ((run['status'] or {}).get('stages') or {}).items():
                stages_out[s] = {k: e.get(k) for k in ('status', 'reason', 'calls', 'input_tokens', 'output_tokens', 'cost_usd',
                                                      'planned', 'valid', 'elapsed_seconds') if e.get(k) is not None}
            return {'exit': run['exit'], 'seconds': round(run['seconds'], 1), 'state': (run['status'] or {}).get('state'),
                    'stopped_stage': (run['status'] or {}).get('stopped_stage'), 'reason': (run['status'] or {}).get('reason'),
                    'stages': stages_out, 'ledger_calls': run['ledger']['attempted_calls'],
                    'max_requests_in_flight': run['max_in_flight'],
                    'stub_cost_usd_not_real': run['ledger']['actual_usd']}
        result = {'rehearsal': 'passed' if all(checks.values()) else 'FAILED', 'checks': checks,
                  'source_hash': study.source_hash(), 'model_calls_made': 0,
                  'full_chain': brief(a_run), 'verify_seconds': round(a_run['verify']['seconds'], 1) if a_run['verify'] else None,
                  'verify_stages': {s: v.get('ok') for s, v in (a_run['verify'] or {}).get('stages', {}).items()},
                  'failed_qualification_chain': brief(b_run), 'failed_call_chain': brief(c_run)}
    finally:
        if a.keep:
            print(f'rehearsal files kept in {tmp}', file=sys.stderr)
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    print(json.dumps(result, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
