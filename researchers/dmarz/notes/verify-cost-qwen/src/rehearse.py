"""Offline rehearsal of the whole chain against a throwaway hub on 127.0.0.1 and a local model stub.

  python3 src/rehearse.py --hub-dir <directory holding hub.py and swarm_report.py>

No request leaves the machine: the hub is a local process, and the model endpoint is replaced by an
in-process stub injected as the adapter's opener. A rehearsal answer is never a sample. The adapter's
clock and sleep are replaced, so backoff and billing waits take no real time. The chain runs five
times, each in fresh temporary result and ledger directories and on its own hub:
  (a) all four stages with a stub that answers by the analytic reference policy, computed from the
      request text alone (it parses the prose or the table it is sent), then `chain verify`;
  (b) with a stub that always picks the first listed cell, which is right in 6 of 12 fixtures per
      representation: the chain must stop at Q0 with exit 3, state stopped_at_gate, and no S1 run
      on the hub;
  (c) a credit error on the probe twice, then success (one billing pause, nothing failed), and one
      failed call in S1 (HTTP 500): S1 ends done with one failed unit and the primary contrast
      reported with bounds; `chain verify`;
  (d) every S1 call fails: dispatch stops when the failed units exceed budget.max_failed and S1 ends
      failed;
  (e) from some point in S1 every request returns a credit error: the stage stops with
      provider_credit_balance_low and nothing failed; `chain resume` with a healthy stub then
      completes the stage; every unit is counted exactly once; `chain verify`.
It refuses to run unless the hub URL host is 127.0.0.1.
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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import chain     # noqa: E402
import manifest  # noqa: E402
import provider  # noqa: E402
import study     # noqa: E402
import worker    # noqa: E402


def require_local(url):
    host = urllib.parse.urlparse(url or '').hostname
    if host != '127.0.0.1':
        raise SystemExit('rehearsal refused: the hub URL host must be 127.0.0.1')
    return url


class Response(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False


class Clock:
    """Real monotonic time plus every wait the adapter asked for: waits pass at once but are counted."""
    def __init__(self): self.offset = 0.0; self.waits = []; self.lock = threading.Lock()
    def now(self): return time.monotonic() + self.offset
    def sleep(self, seconds):
        with self.lock: self.offset += seconds; self.waits.append(seconds)


CREDIT_BODY = json.dumps({'error': {'code': 402, 'message': 'Insufficient credits. Add more using https://openrouter.ai/credits (rehearsal)'}}).encode()
ERROR_BODY = json.dumps({'error': {'code': 500, 'message': 'rehearsal injected failure'}}).encode()
TEMPLATE_KEYS = {'model', 'provider', 'reasoning', 'max_tokens', 'response_format'}


def reference_answer(user, mode):
    """The stub's answer, from the request text alone."""
    first, second = re.search(r'Allowed cells, in this order: (\d,\d); (\d,\d)\.', user).groups()
    if mode == 'always_first': return {'inspect': first}
    report = re.search(r'Report, older \(1 cell\): cell (\d,\d) is', user).group(1)
    error = float(re.search(r'The report is wrong with probability (\d\.\d\d)\.', user).group(1))
    _, block, _ = study.split_block(user)
    records = (study.parse_table if block.startswith(study.TABLE_HEADER) else study.parse_prose)(block)
    unknown_cost = float(next(r['cost'] for r in records if r['outcome'] == 'unknown'))
    other = second if report == first else first
    return {'inspect': report if error > unknown_cost else other}


class Stub:
    """Stands in for the chat-completions endpoint. It answers in the provider's response shape and rejects
    any request body that is not exactly the frozen template plus messages.

    Faults. A request rejected with a credit error is not counted as a message; the others are counted from 1
    (the probe is message 1, the 23 qualification calls are messages 2 to 24, S1 starts at 25):
      credit_first    the first N requests return a credit error (HTTP 402), then the endpoint is healthy
      fail_messages   ordinals of messages that return HTTP 500
      fail_from       every message from this ordinal on returns HTTP 500
      credit_from     once this many messages minus one have been counted, every request returns a credit error"""

    def __init__(self, mode, credit_first=0, fail_messages=(), fail_from=None, credit_from=None):
        assert mode in ('optimal', 'always_first')
        self.mode = mode; self.lock = threading.Lock(); self.requests = 0; self.messages = 0; self.answered = 0
        self.credit_first = credit_first; self.fail_messages = set(fail_messages); self.fail_from = fail_from; self.credit_from = credit_from

    def __call__(self, request, timeout=None):
        if request.full_url != provider.URL: raise AssertionError('the rehearsal stub only answers the chat-completions endpoint')
        body = json.loads(request.data); template = study.design()['request_template']
        if tuple(body) != provider.BODY_KEYS or {k: body[k] for k in TEMPLATE_KEYS} != template \
                or [m['role'] for m in body['messages']] != ['system', 'user']:
            raise urllib.error.HTTPError(provider.URL, 400, 'Bad Request', {}, io.BytesIO(b'{"error":{"code":400,"message":"unexpected request body"}}'))
        with self.lock:
            self.requests += 1
            credit = self.requests <= self.credit_first or (self.credit_from is not None and self.messages + 1 >= self.credit_from)
            if not credit: self.messages += 1
            n = self.messages
        if credit:
            raise urllib.error.HTTPError(provider.URL, 402, 'Payment Required', {'x-request-id': 'req_rehearsal'}, io.BytesIO(CREDIT_BODY))
        if n in self.fail_messages or (self.fail_from is not None and n >= self.fail_from):
            raise urllib.error.HTTPError(provider.URL, 500, 'Internal Server Error', {'x-request-id': 'req_rehearsal'}, io.BytesIO(ERROR_BODY))
        with self.lock: self.answered += 1
        system, user = (m['content'] for m in body['messages'])
        tokens = max(1, (len(system) + len(user)) // 3)
        return Response(json.dumps({
            'id': 'gen-rehearsal', 'object': 'chat.completion', 'model': study.design()['canonical_model'], 'provider': 'Alibaba',
            'choices': [{'index': 0, 'finish_reason': 'stop', 'native_finish_reason': 'stop',
                         'message': {'role': 'assistant', 'content': json.dumps(reference_answer(user, self.mode)), 'refusal': None, 'reasoning': None}}],
            'usage': {'prompt_tokens': tokens, 'completion_tokens': 9, 'total_tokens': tokens + 9,
                      'completion_tokens_details': {'reasoning_tokens': 0}}}).encode())


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
    os.environ.update(SWARM_HUB_URL=require_local(url), SWARM_HUB_TOKEN=token, SWARM_SOURCE='dmarz/pipeline-verify-rehearsal',
                      SWARM_SPOOL=str(work / 'spool'), STUDY_RESULTS_DIR=str(work / 'results'),
                      STUDY_BUDGET_LEDGER=str(work / 'ledger' / 'ledger.jsonl'))
    os.environ[provider.KEY_ENV] = 'rehearsal-stub-not-a-credential'
    require_local(sr._config().get('SWARM_HUB_URL'))
    started = time.monotonic(); result = {'label': label, 'stub': stub.mode}

    def snapshot():
        status = chain.read_status(); runs = sr.runs(study.EXPERIMENT, limit=5000); s1 = status['stages'].get('S1') or {}
        keys = ('status', 'calls', 'answered_calls', 'planned', 'valid', 'invalid', 'failed', 'not_started', 'cost_usd', 'qualification_passed',
                'billing_pauses', 'billing_pause_seconds', 'billing_affected_calls', 'resumable', 'unanswered_reservations', 'reason',
                'table_minus_prose_regret')
        out = dict(state=status['state'], stopped_stage=status.get('stopped_stage'), reason=status.get('reason'),
                   stages={s: {k: e.get(k) for k in keys} for s, e in status['stages'].items()},
                   projection=s1.get('projection'),
                   continuations=[{k: e.get(k) for k in keys + ('batch', 'units')} for e in s1.get('continuations') or []],
                   hub_runs=sorted(((r.get('params') or {}).get('batch'), r['status']) for r in runs),
                   hub_final_metrics_present=all(all(k in (r.get('metrics') or {}) for k in
                       ('episodes', 'invalid', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd')) for r in runs),
                   ledger=chain.ledger_totals())
        if s1.get('directory'): out['s1_units'] = chain.units(chain.stage_rows(s1), manifest.load())
        return out
    try:
        result['exit'] = chain.run_chain(list(study.STAGES), sr=sr, opener=stub)
        result.update(snapshot(), stub_messages=stub.messages, stub_requests=stub.requests, stub_answered=stub.answered)
        if resume_with is not None:
            result['first_stop'] = {k: result.get(k) for k in ('exit', 'state', 'stopped_stage', 'reason', 'stages', 's1_units')}
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
    ap.add_argument('--tmp', help='parent directory for the temporary rehearsal directory')
    a = ap.parse_args()
    hub_dir = Path(a.hub_dir).resolve()
    if not (hub_dir / 'hub.py').is_file() or not (hub_dir / 'swarm_report.py').is_file():
        raise SystemExit('--hub-dir must hold hub.py and swarm_report.py')
    # Set a local address before the client is imported, and check it again before every use.
    os.environ['SWARM_HUB_URL'] = 'http://127.0.0.1:9'; os.environ['SWARM_HUB_TOKEN'] = 'rehearsal-not-started-yet'
    sys.path.insert(0, str(hub_dir))
    import swarm_report as sr
    clock = Clock(); worker.CLOCK, worker.SLEEP = clock.now, clock.sleep       # no backoff or billing wait takes real time
    base = tempfile.mkdtemp(prefix='verify-cost-qwen-rehearsal-', dir=a.tmp); started = time.monotonic()
    budget = study.design()['budget']; total = budget['max_attempted_calls']; limit = budget['max_failed']
    n_s1 = budget['max_calls']['S1']; first_s1 = 2 + budget['max_calls']['Q0']       # message ordinal of the first S1 call
    try:
        full = chain_once('a-full-chain', Stub('optimal'), hub_dir, base, sr, verify=True)
        gate = chain_once('b-failed-qualification', Stub('always_first'), hub_dir, base, sr)
        one = chain_once('c-billing-pause-and-one-failed-unit', Stub('optimal', credit_first=2, fail_messages={first_s1 + 60}),
                         hub_dir, base, sr, verify=True)
        many = chain_once('d-failed-units-over-the-limit', Stub('optimal', fail_from=first_s1), hub_dir, base, sr)
        bill = chain_once('e-billing-stop-and-resume', Stub('optimal', credit_from=first_s1 + 40), hub_dir, base, sr,
                          resume_with=Stub('optimal'), verify=True)
    finally:
        if not a.keep: shutil.rmtree(base, ignore_errors=True)
    calls = full.get('stages', {}); made = sum((e.get('calls') or 0) for e in calls.values())
    done4 = [(study.batch(s), 'done') for s in sorted(study.STAGES)]
    c, d, e = one.get('stages', {}), many.get('stages', {}), bill.get('stages', {})
    first = bill.get('first_stop', {}); cont = (bill.get('continuations') or [{}])[0]
    fu = first.get('s1_units') or {}; orphans = (first.get('stages', {}).get('S1') or {}).get('unanswered_reservations')
    checks = {
        'a_exit_0': full.get('exit') == 0, 'a_state_completed': full.get('state') == 'completed',
        'a_four_done_runs': full.get('hub_runs') == done4,
        'a_calls_equal_caps': {s: (e_.get('calls'), e_.get('valid')) for s, e_ in calls.items()} ==
                              {'S0': (0, 144), 'P0': (1, 1), 'Q0': (budget['max_calls']['Q0'], budget['max_calls']['Q0']), 'S1': (n_s1, n_s1)},
        'a_ledger_calls': (full.get('ledger') or {}).get('attempted_calls') == made == total and full.get('stub_messages') == made,
        'a_reference_policy_has_zero_regret': calls.get('S1', {}).get('table_minus_prose_regret') == 0
                                              and (full.get('s1_units') or {}).get('regret_prose') == 0 and (full.get('s1_units') or {}).get('regret_table') == 0,
        'a_projection_gates_evaluated': (full.get('projection') or {}).get('within_cap') is True and (full.get('projection') or {}).get('input_ceiling_ok') is True,
        'a_hub_metrics_present': full.get('hub_final_metrics_present') is True,
        'a_verify_exit_0': full.get('verify_exit') == 0, 'a_spool_empty': full.get('spool_empty') is True,
        'b_exit_3': gate.get('exit') == 3, 'b_state_stopped_at_gate': gate.get('state') == 'stopped_at_gate',
        'b_stopped_at_Q0': gate.get('stopped_stage') == 'Q0' and gate.get('reason') == 'gate_failed',
        'b_no_S1_run_on_hub': all(not str(batch).startswith('s1') for batch, _ in gate.get('hub_runs', [('s1', '')])),
        'b_hub_runs': gate.get('hub_runs') == [('p0-001', 'done'), ('q0-001', 'failed'), ('s0-001', 'done')],
        'b_hub_metrics_present': gate.get('hub_final_metrics_present') is True,
        'b_only_p0_and_q0_calls': gate.get('stub_messages') == 1 + budget['max_calls']['Q0']
                                  and gate.get('stages', {}).get('Q0', {}).get('valid') == budget['max_calls']['Q0'],
        'c_exit_0_and_completed': one.get('exit') == 0 and one.get('state') == 'completed' and one.get('hub_runs') == done4,
        'c_billing_pause_in_probe_and_nothing_failed_there': c.get('P0', {}).get('billing_pauses') == 1 and c.get('P0', {}).get('failed') == 0
                                                             and 120 <= (c.get('P0', {}).get('billing_pause_seconds') or 0) < 125
                                                             and c.get('P0', {}).get('status') == 'done' and c.get('P0', {}).get('calls') == 1,
        'c_s1_done_with_one_failed_unit': c.get('S1', {}).get('status') == 'done' and c.get('S1', {}).get('failed') == 1 and c.get('S1', {}).get('invalid') == 1
                                          and c.get('S1', {}).get('not_started') == 0,
        'c_bounds_reported': (one.get('s1_units') or {}).get('failed') == 1 and (one.get('s1_units') or {}).get('completed') == n_s1 - 1
                             and (one.get('s1_units') or {}).get('primary_layouts') == 23
                             and (one.get('s1_units') or {}).get('primary_bounds_all_assigned') not in (None, [None, None], [0, 0], [0.0, 0.0])
                             and (one.get('s1_units') or {}).get('failures_by_category') == {'http_500': 1}
                             and (one.get('s1_units') or {}).get('every_unit_exactly_once') is True,
        'c_verify_exit_0': one.get('verify_exit') == 0,
        'd_exit_3_stopped_at_S1': many.get('exit') == 3 and many.get('state') == 'stopped_at_gate' and many.get('stopped_stage') == 'S1'
                                  and many.get('reason') == 'failed_units_over_limit',
        'd_dispatch_stopped': limit < (d.get('S1', {}).get('failed') or 0) <= limit + budget['workers']
                              and (d.get('S1', {}).get('not_started') or 0) >= n_s1 - limit - budget['workers']
                              and many.get('stub_answered') == 1 + budget['max_calls']['Q0'],
        'd_hub_s1_failed': ('s1-001', 'failed') in many.get('hub_runs', []) and many.get('hub_final_metrics_present') is True,
        'e_first_stop_is_a_billing_stop': first.get('exit') == 3 and first.get('reason') == provider.BILLING_STOP and first.get('stopped_stage') == 'S1'
                                          and first.get('stages', {}).get('S1', {}).get('failed') == 0 and first.get('stages', {}).get('S1', {}).get('resumable') is True
                                          and fu.get('failed') == 0 and fu.get('not_started', 0) > 0 and fu.get('completed') == 40,
        'e_unanswered_reservations_counted': isinstance(orphans, int) and 1 <= orphans <= budget['workers'],
        'e_resume_completes': bill.get('resume_exit') == 0 and bill.get('state') == 'completed' and e.get('S1', {}).get('status') == 'done'
                              and cont.get('batch') == 's1-001-r1' and cont.get('status') == 'done' and cont.get('failed') == 0,
        'e_every_unit_exactly_once': (bill.get('s1_units') or {}).get('every_unit_exactly_once') is True and (bill.get('s1_units') or {}).get('completed') == n_s1
                                     and (bill.get('s1_units') or {}).get('assigned') == n_s1 and cont.get('units') == fu.get('not_started')
                                     and (bill.get('s1_units') or {}).get('answered_calls') == n_s1 and (bill.get('s1_units') or {}).get('no_unit_answered_twice') is True,
        'e_hub_runs': bill.get('hub_runs') == sorted(done4[:3] + [('s1-001', 'failed'), ('s1-001-r1', 'done')]),
        'e_ledger_holds_only_the_reissued_reservations_beyond_the_cap': isinstance(orphans, int)
            and ((bill.get('ledger') or {}).get('calls_by_stage') or {}).get('S1') == n_s1 + orphans
            and (bill.get('ledger') or {}).get('usage_reported_calls') == total
            and (bill.get('ledger') or {}).get('transport_attempts', 10 ** 9) <= budget['max_transport_attempts'],
        'e_verify_exit_0': bill.get('verify_exit') == 0,
        'no_real_wait': time.monotonic() - started < 600 and len(clock.waits) > 0,
    }
    ok = all(checks.values())
    print(json.dumps({'ok': ok, 'checks': checks, 'full_chain': full, 'failed_qualification': gate, 'one_failed_unit': one,
                      'over_the_failure_limit': many, 'billing_stop_and_resume': bill, 'waits_replaced': len(clock.waits),
                      'waited_seconds_replaced': sum(clock.waits), 'seconds': round(time.monotonic() - started, 1),
                      'note': 'stub answers only; nothing here is a sample and nothing left this machine'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
