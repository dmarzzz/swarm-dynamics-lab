"""Offline rehearsal of the whole chain against a throwaway hub on 127.0.0.1 and a local model stub.

  python3 src/rehearse.py --hub-dir <directory holding hub.py and swarm_report.py>

No request leaves the machine: the hub is a local process, and the model endpoint is replaced by
an in-process stub injected as the adapter's opener. A rehearsal answer is never a sample. Waits
(backoff, billing re-sends) are replaced by a no-op, so nothing sleeps. The chain runs five times,
each in fresh temporary result and ledger directories and on its own hub:
  (a) all four stages with a stub that answers every turn by the scripted `parallel` reference
      planner, computed from the request it receives, then `chain verify`;
  (b) with a stub that never creates a subagent, which must fail qualification (no job without
      a quota can be finished by one identity): the chain must stop at Q0 with a non-zero exit,
      state stopped_at_gate, and no S1 run on the hub;
  (c) a credit-balance error on the probe's token-counting request twice, then success (one
      billing pause, nothing failed), and one failed call in S1 (HTTP 500): S1 ends done with one
      failed episode and the primary contrast reported with bounds; `chain verify`;
  (d) every S1 call fails: dispatch stops when the failed episodes exceed budget.max_failed and
      S1 ends failed;
  (e) from some point in S1 every request returns a credit-balance error: the stage stops with
      provider_credit_balance_low and nothing failed; `chain resume` with a healthy stub then
      completes the stage; every episode is counted exactly once; `chain verify`.
It refuses to run unless the hub URL host is 127.0.0.1.
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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import chain     # noqa: E402
import manifest  # noqa: E402
import provider  # noqa: E402
import sim       # noqa: E402
import study     # noqa: E402


def require_local(url):
    host = urllib.parse.urlparse(url or '').hostname
    if host != '127.0.0.1':
        raise SystemExit('rehearsal refused: the hub URL host must be 127.0.0.1')
    return url


class Response(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False


CREDIT_BODY = json.dumps({'type': 'error', 'error': {'type': 'invalid_request_error',
                          'message': 'Your credit balance is too low to access the Anthropic API. (rehearsal)'}}).encode()
ERROR_BODY = json.dumps({'type': 'error', 'error': {'type': 'api_error', 'message': 'rehearsal injected failure'}}).encode()


class Stub:
    """Stands in for the two provider endpoints. It answers in the real response shape, with a
    thinking block before the text block, and rejects any request body the real model would
    reject for carrying a key outside the contract. Its answer to a turn is computed from the
    request alone: the system prompt names the rules, the user message is the state.

    Faults, by the ordinal of the request on its endpoint (the probe is message 1, the sixteen
    qualification episodes of the `parallel` stub are messages 2 to 97, S1 starts at 98):
      credit_count      (first ordinal, times): that many token-counting requests from that
                        ordinal on return a credit-balance error, then the endpoint is healthy
      fail_messages     ordinals of message requests that return HTTP 500
      fail_from         every message request from this ordinal on returns HTTP 500
      credit_from       every message request from this ordinal on returns a credit-balance error"""

    def __init__(self, mode, credit_count=None, fail_messages=(), fail_from=None, credit_from=None):
        assert mode in ('parallel', 'never_spawn')
        self.mode = mode; self.lock = threading.Lock(); self.counts = 0; self.messages = 0; self.answered = 0
        self.credit_count = list(credit_count) if credit_count else None
        self.fail_messages = set(fail_messages); self.fail_from = fail_from; self.credit_from = credit_from

    def answer(self, system, obs):
        spec = study.design()['conditions'][study.condition_of(system)]
        rules = {'quota': spec['quota'], 'spawn': spec['spawn'] and self.mode != 'never_spawn', 'fee': obs.get('spawn_fee', 0),
                 'max_subagents': obs['max_subagents']}
        return sim.plan(obs, rules, 'parallel')

    def __call__(self, request, timeout=None):
        url = request.full_url
        if url not in (provider.MESSAGES_URL, provider.COUNT_URL):
            raise AssertionError('the rehearsal stub only answers the two provider endpoints')
        body = json.loads(request.data)
        allowed = set(provider.BODY_KEYS) - ({'max_tokens'} if url == provider.COUNT_URL else set())
        if set(body) != allowed or set(body['output_config']) != {'effort', 'format'} or [m['role'] for m in body['messages']] != ['user']:
            raise urllib.error.HTTPError(url, 400, 'invalid_request_error', {}, io.BytesIO(b'{}'))
        tokens = max(1, len(body['messages'][0]['content']) // 3 + len(body['system']) // 4)
        if url == provider.COUNT_URL:
            with self.lock:
                self.counts += 1
                credit = bool(self.credit_count and self.counts >= self.credit_count[0] and self.credit_count[1] > 0)
                if credit: self.credit_count[1] -= 1
            if credit: raise urllib.error.HTTPError(url, 400, 'Bad Request', {'request-id': 'req_rehearsal'}, io.BytesIO(CREDIT_BODY))
            return Response(json.dumps({'input_tokens': tokens}).encode())
        with self.lock: self.messages += 1; n = self.messages
        if self.credit_from is not None and n >= self.credit_from:
            raise urllib.error.HTTPError(url, 400, 'Bad Request', {'request-id': 'req_rehearsal'}, io.BytesIO(CREDIT_BODY))
        if n in self.fail_messages or (self.fail_from is not None and n >= self.fail_from):
            raise urllib.error.HTTPError(url, 500, 'Internal Server Error', {'request-id': 'req_rehearsal'}, io.BytesIO(ERROR_BODY))
        with self.lock: self.answered += 1
        answer = self.answer(body['system'], json.loads(body['messages'][0]['content']))
        return Response(json.dumps({
            'id': 'msg_rehearsal', 'type': 'message', 'role': 'assistant', 'model': body['model'],
            'content': [{'type': 'thinking', 'thinking': '', 'signature': 'rehearsal'},
                        {'type': 'text', 'text': json.dumps(answer)}],
            'stop_reason': 'end_turn', 'stop_sequence': None,
            'usage': {'input_tokens': tokens, 'output_tokens': 120, 'cache_creation_input_tokens': 0,
                      'cache_read_input_tokens': 0}}).encode())


def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0)); return s.getsockname()[1]


def start_hub(hub_dir, data_dir, token):
    port = free_port()
    env = dict(os.environ, SWARM_HUB_TOKEN=token)
    log = open(Path(data_dir) / 'hub.log', 'w')
    proc = subprocess.Popen([sys.executable, str(Path(hub_dir) / 'hub.py'), '--data', str(Path(data_dir) / 'hubdata'),
                             '--port', str(port)], env=env, stdout=log, stderr=subprocess.STDOUT)
    for _ in range(100):
        if proc.poll() is not None: raise SystemExit('the throwaway hub exited at start; see ' + log.name)
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=0.2): break
        except OSError: time.sleep(0.1)
    else:
        proc.terminate(); raise SystemExit('the throwaway hub did not start')
    return proc, f'http://127.0.0.1:{port}'


def chain_once(label, stub, hub_dir, base, sr, resume_with=None, verify=False):
    work = Path(base) / label; work.mkdir()
    token = 'rehearsal-' + secrets.token_hex(12)
    proc, url = start_hub(hub_dir, work, token)
    os.environ.update(SWARM_HUB_URL=require_local(url), SWARM_HUB_TOKEN=token, SWARM_SOURCE='dmarz/pipeline-quota-rehearsal',
                      SWARM_SPOOL=str(work / 'spool'), STUDY_RESULTS_DIR=str(work / 'results'),
                      STUDY_BUDGET_LEDGER=str(work / 'ledger' / 'ledger.jsonl'),
                      SWARM_MODEL_API_KEY='rehearsal-stub-not-a-credential', SWARM_MODEL_WORKSPACE_ID='rehearsal-stub')
    require_local(sr._config().get('SWARM_HUB_URL'))
    started = time.monotonic(); result = {'label': label, 'stub': stub.mode}
    def snapshot():
        status = chain.read_status(); runs = sr.runs(study.EXPERIMENT, limit=5000); s1 = status['stages'].get('S1') or {}
        keys = ('status', 'calls', 'planned', 'valid', 'invalid', 'failed', 'not_started', 'cost_usd', 'qualification_passed',
                'billing_pauses', 'billing_pause_seconds', 'count_fallbacks', 'resumable')
        out = dict(state=status['state'], stopped_stage=status.get('stopped_stage'), reason=status.get('reason'),
                   stages={s: {k: e.get(k) for k in keys} for s, e in status['stages'].items()},
                   continuations=[{k: e.get(k) for k in keys + ('batch', 'units')} for e in s1.get('continuations') or []],
                   hub_runs=sorted(((r.get('params') or {}).get('batch'), r['status']) for r in runs),
                   hub_final_metrics_present=all(all(k in (r.get('metrics') or {}) for k in
                       ('episodes', 'invalid', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd')) for r in runs),
                   ledger=chain.ledger_totals())
        if s1.get('directory'): out['s1_units'] = chain.units(chain.stage_rows(s1), manifest.load())
        return out
    try:
        result['exit'] = chain.run_chain(list(study.STAGES), sr=sr, opener=stub)
        result.update(snapshot(), stub_messages=stub.messages, stub_counts=stub.counts, stub_answered=stub.answered)
        if resume_with is not None:
            result['first_stop'] = {k: result[k] for k in ('exit', 'state', 'stopped_stage', 'reason', 'stages', 's1_units')}
            result['resume_exit'] = chain.resume(sr=sr, opener=resume_with)
            result.update(snapshot(), resume_stub_messages=resume_with.messages)
        if verify: result['verify_exit'] = chain.verify(sr)
        result['spool_empty'] = not list((work / 'spool').glob('*.json')) if (work / 'spool').exists() else True
    finally:
        proc.terminate()
        try: proc.wait(timeout=10)
        except subprocess.TimeoutExpired: proc.kill()
    result['seconds'] = round(time.monotonic() - started, 1)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--hub-dir', required=True); ap.add_argument('--keep', action='store_true', help='keep the temporary directory')
    a = ap.parse_args()
    hub_dir = Path(a.hub_dir).resolve()
    if not (hub_dir / 'hub.py').is_file() or not (hub_dir / 'swarm_report.py').is_file():
        raise SystemExit('--hub-dir must hold hub.py and swarm_report.py')
    # Set a local address before the client is imported, and check it again before every use.
    os.environ['SWARM_HUB_URL'] = 'http://127.0.0.1:9'; os.environ['SWARM_HUB_TOKEN'] = 'rehearsal-not-started-yet'
    sys.path.insert(0, str(hub_dir))
    import swarm_report as sr
    waits = []; provider.SLEEP = waits.append          # no backoff or billing wait takes real time
    base = tempfile.mkdtemp(prefix='quota-splitting-rehearsal-'); started = time.monotonic()
    budget = study.design()['budget']; total = budget['max_attempted_calls']; limit = budget['max_failed']
    episodes = len(study.cells('S1')); first_s1 = 2 + budget['max_calls']['Q0']       # message ordinal of the first S1 call
    try:
        full = chain_once('a-full-chain', Stub('parallel'), hub_dir, base, sr, verify=True)
        gate = chain_once('b-failed-qualification', Stub('never_spawn'), hub_dir, base, sr)
        one = chain_once('c-billing-pause-and-one-failed-episode', Stub('parallel', credit_count=(1, 2), fail_messages={first_s1 + 60}),
                         hub_dir, base, sr, verify=True)
        many = chain_once('d-failed-episodes-over-the-limit', Stub('parallel', fail_from=first_s1), hub_dir, base, sr)
        bill = chain_once('e-billing-stop-and-resume', Stub('parallel', credit_from=first_s1 + 40), hub_dir, base, sr,
                          resume_with=Stub('parallel'), verify=True)
    finally:
        if not a.keep: shutil.rmtree(base, ignore_errors=True)
    calls = full.get('stages', {}); made = sum((e.get('calls') or 0) for e in calls.values())
    done4 = [(study.batch(s), 'done') for s in sorted(study.STAGES)]
    c, d, e = one.get('stages', {}), many.get('stages', {}), bill.get('stages', {})
    first = bill.get('first_stop', {}); cont = (bill.get('continuations') or [{}])[0]
    checks = {
        'a_exit_0': full.get('exit') == 0, 'a_state_completed': full.get('state') == 'completed',
        'a_four_done_runs': full.get('hub_runs') == done4,
        'a_calls_within_caps': all(0 <= (e_.get('calls') if e_.get('calls') is not None else -1) <= budget['max_calls'][s] for s, e_ in calls.items()) and len(calls) == 4,
        'a_paid_stages_called': calls.get('S0', {}).get('calls') == 0 and calls.get('P0', {}).get('calls') == 1
                                and (calls.get('Q0', {}).get('calls') or 0) > 0 and (calls.get('S1', {}).get('calls') or 0) > 0,
        'a_ledger_calls': (full.get('ledger') or {}).get('attempted_calls') == made and full.get('stub_messages') == made and 0 < made <= total,
        'a_hub_metrics_present': full.get('hub_final_metrics_present') is True,
        'a_verify_exit_0': full.get('verify_exit') == 0, 'a_spool_empty': full.get('spool_empty') is True,
        'b_exit_3': gate.get('exit') == 3, 'b_state_stopped_at_gate': gate.get('state') == 'stopped_at_gate',
        'b_stopped_at_Q0': gate.get('stopped_stage') == 'Q0',
        'b_no_S1_run_on_hub': all(not str(batch).startswith('s1') for batch, _ in gate.get('hub_runs', [('s1', '')])),
        'b_hub_runs': gate.get('hub_runs') == [('p0-001', 'done'), ('q0-001', 'failed'), ('s0-001', 'done')],
        'b_hub_metrics_present': gate.get('hub_final_metrics_present') is True,
        'b_only_p0_and_q0_calls': gate.get('stub_messages') == sum((gate.get('stages', {}).get(s, {}).get('calls') or 0) for s in ('P0', 'Q0'))
                                  and 1 < (gate.get('stub_messages') or 0) <= budget['max_calls']['P0'] + budget['max_calls']['Q0'],
        'c_exit_0_and_completed': one.get('exit') == 0 and one.get('state') == 'completed' and one.get('hub_runs') == done4,
        'c_billing_pause_in_probe_and_nothing_failed_there': c.get('P0', {}).get('billing_pauses') == 1 and c.get('P0', {}).get('failed') == 0
                                                             and c.get('P0', {}).get('billing_pause_seconds') == 120 and c.get('P0', {}).get('status') == 'done',
        'c_s1_done_with_one_failed_episode': c.get('S1', {}).get('status') == 'done' and c.get('S1', {}).get('failed') == 1 and c.get('S1', {}).get('invalid') == 1
                                             and c.get('S1', {}).get('not_started') == 0,
        'c_bounds_reported': (one.get('s1_units') or {}).get('failed') == 1 and (one.get('s1_units') or {}).get('completed') == episodes - 1
                             and (one.get('s1_units') or {}).get('primary_bounds_all_assigned') not in (None, [None, None])
                             and (one.get('s1_units') or {}).get('every_unit_exactly_once') is True,
        'c_verify_exit_0': one.get('verify_exit') == 0,
        'd_exit_3_stopped_at_S1': many.get('exit') == 3 and many.get('state') == 'stopped_at_gate' and many.get('stopped_stage') == 'S1'
                                  and many.get('reason') == 'failed_units_over_limit',
        'd_dispatch_stopped': limit < (d.get('S1', {}).get('failed') or 0) <= limit + budget['workers'] and (d.get('S1', {}).get('not_started') or 0) >= episodes - limit - 2 * budget['workers']
                              and many.get('stub_answered') == 1 + budget['max_calls']['Q0'],
        'd_hub_s1_failed': ('s1-001', 'failed') in many.get('hub_runs', []) and many.get('hub_final_metrics_present') is True,
        'e_first_stop_is_a_billing_stop': first.get('exit') == 3 and first.get('reason') == provider.CREDIT and first.get('stopped_stage') == 'S1'
                                          and first.get('stages', {}).get('S1', {}).get('failed') == 0 and first.get('stages', {}).get('S1', {}).get('resumable') is True
                                          and (first.get('s1_units') or {}).get('failed') == 0 and (first.get('s1_units') or {}).get('not_started', 0) > 0,
        'e_resume_completes': bill.get('resume_exit') == 0 and bill.get('state') == 'completed' and e.get('S1', {}).get('status') == 'done'
                              and cont.get('batch') == 's1-001-r1' and cont.get('status') == 'done' and cont.get('failed') == 0,
        'e_every_unit_exactly_once': (bill.get('s1_units') or {}).get('every_unit_exactly_once') is True and (bill.get('s1_units') or {}).get('completed') == episodes
                                     and (bill.get('s1_units') or {}).get('assigned') == episodes
                                     and cont.get('units') == (first.get('s1_units') or {}).get('interrupted', 0) + (first.get('s1_units') or {}).get('not_started', 0),
        'e_hub_runs': bill.get('hub_runs') == sorted(done4[:3] + [('s1-001', 'failed'), ('s1-001-r1', 'done')]),
        'e_same_ledger_within_caps': ((bill.get('ledger') or {}).get('calls_by_stage') or {}).get('S1', 10 ** 9) <= budget['max_calls']['S1']
                                     and (bill.get('ledger') or {}).get('transport_attempts', 10 ** 9) <= budget['max_transport_attempts'],
        'e_verify_exit_0': bill.get('verify_exit') == 0,
        'no_real_wait': time.monotonic() - started < 600 and len(waits) > 0,
    }
    ok = all(checks.values())
    print(json.dumps({'ok': ok, 'checks': checks, 'full_chain': full, 'failed_qualification': gate, 'one_failed_episode': one,
                      'over_the_failure_limit': many, 'billing_stop_and_resume': bill, 'waits_replaced': len(waits),
                      'seconds': round(time.monotonic() - started, 1),
                      'note': 'stub answers only; nothing here is a sample and nothing left this machine'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
