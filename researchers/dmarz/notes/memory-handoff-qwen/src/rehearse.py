"""Offline rehearsal of the whole chain against a throwaway hub on 127.0.0.1 and a local model stub.

  python3 src/rehearse.py --hub-dir <directory holding hub.py and swarm_report.py>

No request leaves the machine: the hub is a local process, every other urllib destination is
blocked, and the model endpoint is replaced by an in-process stub injected as the adapter's
opener. The stub answers in the OpenRouter chat-completions shape (choices[0].message.content,
finish_reason, usage.prompt_tokens, usage.completion_tokens, model, provider) and rejects any
request body that is not the frozen template plus messages. A rehearsal answer is never a sample.
Backoff and billing waits use an injected clock, so nothing sleeps. The chain runs five times,
each on its own hub and in fresh temporary result and ledger directories:
  (a) all four stages with a stub that answers by the scripted reference actor, computed from the
      message it receives, and writes its answers in a rotating mix of the tolerated variants
      (value as 45.0 or "45", repeated source IDs, an extra key, missing or malformed working
      fields, working fields after the value, `current` as a string, sources null, pretty-printed);
      every one must be valid and scored as usual; then `chain verify`; queueing S0 again must be refused;
  (b) with a stub that repeats the predecessor's note whatever else the message holds: it fails
      qualification; the chain must stop at Q0 with exit 3, state stopped_at_gate and no S1 run;
  (c) a credit error on the probe twice, then success (one billing pause, nothing failed), and one
      failed call in S1 (HTTP 500): S1 ends done with one failed call and the primary contrast
      reported with bounds; `chain verify`;
  (d) every S1 call fails: dispatch stops when failed calls exceed budget.max_failed; S1 ends failed;
  (e) from some point in S1 every request returns a credit error: the stage stops with
      provider_credit_balance_low and nothing failed; `chain resume` with a healthy stub then
      completes the stage; every assignment is counted exactly once; `chain verify`.
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
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import chain        # noqa: E402
import coordinator  # noqa: E402
import manifest     # noqa: E402
import provider     # noqa: E402
import sim          # noqa: E402
import study        # noqa: E402
import worker       # noqa: E402

LOCAL = '127.0.0.1'
CREDIT_BODY = json.dumps({'error': {'code': 402, 'message': 'Insufficient credits. (rehearsal)'}}).encode()
ERROR_BODY = json.dumps({'error': {'code': 500, 'message': 'rehearsal injected failure'}}).encode()


def require_local(url):
    if urllib.parse.urlparse(url or '').hostname != LOCAL:
        raise SystemExit('rehearsal refused: the hub URL host must be 127.0.0.1')
    return url


def block_network():
    """Every urllib request of this process must go to 127.0.0.1."""
    original = urllib.request.urlopen

    def guarded(target, *args, **kwargs):
        url = target.full_url if isinstance(target, urllib.request.Request) else target
        if urllib.parse.urlparse(url).hostname != LOCAL:
            raise RuntimeError('rehearsal_network_blocked')
        return original(target, *args, **kwargs)
    urllib.request.urlopen = guarded


class Response(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False


class Clock:
    """Real monotonic time plus every wait the adapter asked for; a wait costs no real time."""
    def __init__(self): self.offset = 0.0; self.waits = []; self.lock = threading.Lock()
    def now(self):
        with self.lock: return time.monotonic() + self.offset
    def sleep(self, seconds):
        with self.lock: self.offset += seconds; self.waits.append(seconds)


class Stub:
    """Stands in for the provider endpoint. Its answer is computed from the request alone: it never
    sees the assignment, the memory state, the handoff policy or the evaluator.

    mode 'reference'      the scripted reference actor on the message it received
    mode 'trust_memory'   repeats the first note about the requested fact (fails qualification)
    variants=True         the answer text rotates through the tolerated variants of preregistration A5
    Faults, by the ordinal of the request (the probe is 1, Q0 is 2 to 24, S1 starts at 25):
      credit_at (ordinal, times)   that many requests from that ordinal on return a credit error
      fail_messages                ordinals that return HTTP 500
      fail_from                    every request from this ordinal on returns HTTP 500
      credit_from                  every request from this ordinal on returns a credit error"""

    def __init__(self, mode='reference', credit_at=None, fail_messages=(), fail_from=None, credit_from=None, variants=False):
        assert mode in ('reference', 'trust_memory')
        self.mode = mode; self.variants = variants; self.lock = threading.Lock(); self.requests = 0; self.answered = 0
        self.credit_at = list(credit_at) if credit_at else None
        self.fail_messages = set(fail_messages); self.fail_from = fail_from; self.credit_from = credit_from

    def __call__(self, request, timeout=None):
        url = request.full_url
        if url != provider.URL:
            raise AssertionError('the rehearsal stub only answers the provider endpoint')
        headers = {k.lower(): v for k, v in request.header_items()}
        body = json.loads(request.data); template = study.design()['request_template']
        if (not headers.get('authorization', '').startswith('Bearer ') or tuple(body) != provider.BODY_KEYS
                or {k: body[k] for k in body if k != 'messages'} != template
                or [m['role'] for m in body['messages']] != ['system', 'user'] or body['messages'][0]['content'] != study.SYSTEM):
            raise urllib.error.HTTPError(url, 400, 'Bad Request', {}, io.BytesIO(b'{"error":{"message":"request is not the frozen template"}}'))
        with self.lock:
            self.requests += 1; n = self.requests
            credit = bool(self.credit_at and n >= self.credit_at[0] and self.credit_at[1] > 0)
            if credit: self.credit_at[1] -= 1
        if credit or (self.credit_from is not None and n >= self.credit_from):
            raise urllib.error.HTTPError(url, 402, 'Payment Required', {'x-request-id': 'req_rehearsal'}, io.BytesIO(CREDIT_BODY))
        if n in self.fail_messages or (self.fail_from is not None and n >= self.fail_from):
            raise urllib.error.HTTPError(url, 500, 'Internal Server Error', {'x-request-id': 'req_rehearsal'}, io.BytesIO(ERROR_BODY))
        packet = json.loads(body['messages'][1]['content'])
        answer = sim.control(packet, self.mode)
        with self.lock: self.answered += 1
        text = tolerated_text(answer, n) if self.variants else json.dumps(answer)
        return Response(json.dumps({
            'id': f'gen-rehearsal-{n:06d}', 'object': 'chat.completion', 'model': study.design()['canonical_model'], 'provider': 'Alibaba',
            'choices': [{'index': 0, 'finish_reason': 'stop', 'message': {'role': 'assistant', 'content': text}}],
            'usage': {'prompt_tokens': max(1, len(request.data) // 3), 'completion_tokens': max(1, len(text) // 3),
                      'total_tokens': len(request.data) // 3 + len(text) // 3,
                      'completion_tokens_details': {'reasoning_tokens': 0}}}).encode())


TOLERATED_VARIANTS = ('plain', 'value_as_float', 'value_as_string', 'duplicate_sources', 'extra_key', 'work_missing',
                      'work_after_value', 'current_as_string', 'work_malformed', 'sources_null_or_pretty')


def tolerated_text(answer, n):
    """The answer written as the n-th tolerated variant (preregistration A5). Each is one JSON object
    with the same value and the same set of sources as `answer`."""
    kind = TOLERATED_VARIANTS[n % len(TOLERATED_VARIANTS)]; a = json.loads(json.dumps(answer))
    if kind == 'value_as_float' and a['value'] is not None: a['value'] = float(a['value'])
    elif kind == 'value_as_string' and a['value'] is not None: a['value'] = f' {a["value"]}'
    elif kind == 'duplicate_sources': a['sources'] = a['sources'] + a['sources'][:1]
    elif kind == 'extra_key': a['note'] = 'applied the source policy'
    elif kind == 'work_missing': a = {'value': a['value'], 'sources': a['sources']}
    elif kind == 'work_after_value': a = {k: a[k] for k in ('value', 'sources', 'records', 'counting_values', 'distinct_origins') if k in a}
    elif kind == 'current_as_string':
        for r in a.get('records', []): r['current'] = 'true' if r['current'] else 'false'
    elif kind == 'work_malformed': a['records'] = 'see the message'; a.pop('counting_values', None); a['distinct_origins'] = 'one'
    elif kind == 'sources_null_or_pretty':
        if a['value'] is None: a['sources'] = None
        return '\n' + json.dumps(a, indent=2) + '\n'
    return json.dumps(a)


def free_port():
    with socket.socket() as s:
        s.bind((LOCAL, 0)); return s.getsockname()[1]


def start_hub(hub_dir, work, token):
    port = free_port()
    log = open(Path(work) / 'hub.log', 'w')
    proc = subprocess.Popen([sys.executable, str(Path(hub_dir) / 'hub.py'), '--data', str(Path(work) / 'hubdata'), '--bind', LOCAL,
                             '--port', str(port)], env=dict(os.environ, SWARM_HUB_TOKEN=token), stdout=log, stderr=subprocess.STDOUT)
    for _ in range(100):
        if proc.poll() is not None: raise SystemExit('the throwaway hub exited at start; see ' + log.name)
        try:
            with socket.create_connection((LOCAL, port), timeout=0.2): break
        except OSError: time.sleep(0.1)
    else:
        proc.terminate(); raise SystemExit('the throwaway hub did not start')
    return proc, f'http://{LOCAL}:{port}'


KEYS = ('work', 'status', 'calls', 'answered_calls', 'planned', 'valid', 'invalid', 'failed', 'not_started', 'cost_usd', 'qualification_passed',
        'billing_pauses', 'billing_pause_seconds', 'billing_affected_calls', 'resumable', 'elapsed_seconds')


def chain_once(label, stub, hub_dir, base, sr, resume_with=None, verify=False, replay_check=False):
    work = Path(base) / label; work.mkdir()
    token = 'rehearsal-' + secrets.token_hex(12)
    proc, url = start_hub(hub_dir, work, token)
    os.environ.update(SWARM_HUB_URL=require_local(url), SWARM_HUB_TOKEN=token, SWARM_SOURCE='dmarz/pipeline-memory-rehearsal',
                      SWARM_SPOOL=str(work / 'spool'), SWARM_NO_AUTO_REFRESH='1', STUDY_RESULTS_DIR=str(work / 'results'),
                      STUDY_BUDGET_LEDGER=str(work / 'ledger' / 'ledger.jsonl'))
    os.environ[provider.KEY_ENV] = 'rehearsal-stub-not-a-credential'
    require_local(sr._config().get('SWARM_HUB_URL'))
    started = time.monotonic(); clock = Clock(); result = {'label': label, 'stub': stub.mode}

    def snapshot():
        status = chain.read_status(); runs = sr.runs(study.EXPERIMENT, limit=5000); s1 = status['stages'].get('S1') or {}
        out = dict(state=status['state'], stopped_stage=status.get('stopped_stage'), reason=status.get('reason'),
                   stages={s: {k: e.get(k) for k in KEYS} for s, e in status['stages'].items()},
                   projection=s1.get('projection'),
                   continuations=[{k: e.get(k) for k in KEYS + ('batch', 'units')} for e in s1.get('continuations') or []],
                   hub_runs=sorted([(r.get('params') or {}).get('batch'), r['status']] for r in runs),
                   hub_final_metrics_present=all(all(k in (r.get('metrics') or {}) for k in worker.REQUIRED_METRICS) for r in runs),
                   ledger=chain.ledger_totals())
        if s1.get('directory'): out['s1_units'] = chain.units(chain.stage_rows(s1), manifest.load())
        return out
    try:
        result['exit'] = chain.run_chain(list(study.STAGES), sr=sr, opener=stub, clock=clock.now, sleep=clock.sleep)
        result.update(snapshot(), stub_requests=stub.requests, stub_answered=stub.answered)
        if replay_check:
            try: coordinator.enqueue(sr, 'S0'); result['replay_refused'] = False
            except coordinator.GateRefused as exc: result['replay_refused'] = str(exc) == 'batch_exists_no_replay'
        if resume_with is not None:
            result['first_stop'] = {k: result[k] for k in ('exit', 'state', 'stopped_stage', 'reason', 'stages', 's1_units', 'ledger')}
            result['resume_exit'] = chain.resume(sr=sr, opener=resume_with, clock=clock.now, sleep=clock.sleep)
            result.update(snapshot(), resume_stub_requests=resume_with.requests)
        if verify:
            t = time.monotonic(); result['verify_exit'] = chain.verify(sr); result['verify_seconds'] = round(time.monotonic() - t, 1)
        result['spool_empty'] = not list((work / 'spool').glob('*.json')) if (work / 'spool').exists() else True
        result['waits'] = len(clock.waits); result['waited_seconds_not_slept'] = sum(clock.waits)
    finally:
        proc.terminate()
        try: proc.wait(timeout=10)
        except subprocess.TimeoutExpired: proc.kill()
        shutil.rmtree(work / 'hubdata', ignore_errors=True)       # keep the disk footprint small between scenarios
    result['seconds'] = round(time.monotonic() - started, 1)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--hub-dir', required=True); ap.add_argument('--keep', action='store_true', help='keep the temporary directory')
    ap.add_argument('--tmp', help='parent directory for the temporary files')
    a = ap.parse_args()
    hub_dir = Path(a.hub_dir).resolve()
    if not (hub_dir / 'hub.py').is_file() or not (hub_dir / 'swarm_report.py').is_file():
        raise SystemExit('--hub-dir must hold hub.py and swarm_report.py')
    # Set a local address before the client is imported, and check it again before every use.
    os.environ['SWARM_HUB_URL'] = f'http://{LOCAL}:9'; os.environ['SWARM_HUB_TOKEN'] = 'rehearsal-not-started-yet'
    block_network()
    sys.path.insert(0, str(hub_dir))
    import swarm_report as sr
    base = tempfile.mkdtemp(prefix='memory-handoff-rehearsal-', dir=a.tmp)
    if study.ROOT in Path(base).resolve().parents: raise SystemExit('the temporary directory is inside the study tree')
    started = time.monotonic()
    budget = study.design()['budget']; total = sum(budget['max_calls'].values()); limit = budget['max_failed']
    n_s1 = budget['max_calls']['S1']; first_s1 = 2 + budget['max_calls']['Q0']       # request ordinal of the first S1 call
    outage = budget['billing_outage']; near = lambda x, y: x is not None and abs(x - y) < 1.0
    try:
        full = chain_once('a-full-chain', Stub('reference', variants=True), hub_dir, base, sr, verify=True, replay_check=True)
        gate = chain_once('b-failed-qualification', Stub('trust_memory'), hub_dir, base, sr)
        one = chain_once('c-billing-pause-and-one-failed-call', Stub('reference', credit_at=(1, 2), fail_messages={first_s1 + 2 + 60}),
                         hub_dir, base, sr, verify=True)
        many = chain_once('d-failed-calls-over-the-limit', Stub('reference', fail_from=first_s1), hub_dir, base, sr)
        bill = chain_once('e-billing-stop-and-resume', Stub('reference', credit_from=first_s1 + 40), hub_dir, base, sr,
                          resume_with=Stub('reference'), verify=True)
    finally:
        if not a.keep: shutil.rmtree(base, ignore_errors=True)
    calls = full.get('stages', {})
    done4 = sorted([study.batch(s), 'done'] for s in study.STAGES)
    c, d, e = one.get('stages', {}), many.get('stages', {}), bill.get('stages', {})
    first = bill.get('first_stop', {}); cont = (bill.get('continuations') or [{}])[0]
    fu, cu, eu = full.get('s1_units') or {}, one.get('s1_units') or {}, bill.get('s1_units') or {}
    first_units = first.get('s1_units') or {}; first_s1_stage = first.get('stages', {}).get('S1', {})
    voided = (first.get('ledger') or {}).get('voided_calls') or 0
    batch = study.batch; wa = calls.get('S1', {}).get('work') or {}
    checks = {
        'a_exit_0': full.get('exit') == 0, 'a_state_completed': full.get('state') == 'completed',
        'a_four_done_runs': full.get('hub_runs') == done4,
        'a_calls_per_stage': {s: calls.get(s, {}).get('calls') for s in study.STAGES} == budget['max_calls'],
        'a_ledger_calls': (full.get('ledger') or {}).get('attempted_calls') == total == full.get('stub_requests'),
        'a_gates_passed': all(calls.get(s, {}).get('qualification_passed') == 1 for s in ('S0', 'P0', 'Q0')),
        'a_projection_checked': (full.get('projection') or {}).get('within_cap') is True and (full.get('projection') or {}).get('input_ceiling_ok') is True,
        'a_reference_primary': fu.get('primary_estimate') == -0.5 and fu.get('completed') == n_s1 and fu.get('every_unit_exactly_once') is True,
        'a_hub_metrics_present': full.get('hub_final_metrics_present') is True,
        'a_verify_exit_0': full.get('verify_exit') == 0, 'a_spool_empty': full.get('spool_empty') is True,
        'a_replay_refused': full.get('replay_refused') is True,
        'a_tolerated_variants_valid_and_counted': calls.get('S1', {}).get('valid') == n_s1 and wa.get('answers') == n_s1
            and all(wa.get(k, 0) > 0 for k in ('value_as_float', 'value_as_string', 'duplicate_sources', 'sources_null', 'extra_keys', 'work_missing',
                                                 'work_malformed', 'current_as_string'))
            and 0 < wa.get('work_before_value', 0) < n_s1 and (calls.get('Q0', {}).get('work') or {}).get('work_malformed', 0) > 0,
        'b_exit_3': gate.get('exit') == 3, 'b_state_stopped_at_gate': gate.get('state') == 'stopped_at_gate',
        'b_stopped_at_Q0': gate.get('stopped_stage') == 'Q0' and gate.get('reason') == 'qualification_failed',
        'b_no_S1_run_on_hub': all(not str(batch).startswith('s1') for batch, _ in gate.get('hub_runs', [('s1', '')])) and 'S1' not in gate.get('stages', {'S1': 1}),
        'b_hub_runs': gate.get('hub_runs') == [[batch('P0'), 'done'], [batch('Q0'), 'failed'], [batch('S0'), 'done']],
        'b_q0_failed_with_metrics': gate.get('hub_final_metrics_present') is True and gate.get('stages', {}).get('Q0', {}).get('qualification_passed') == 0
            and gate.get('stages', {}).get('Q0', {}).get('valid') == budget['max_calls']['Q0'],
        'b_calls_stopped_at_24': gate.get('stub_requests') == 1 + budget['max_calls']['Q0'] == (gate.get('ledger') or {}).get('attempted_calls'),
        'c_exit_0_and_completed': one.get('exit') == 0 and one.get('state') == 'completed' and one.get('hub_runs') == done4,
        'c_billing_pause_in_probe_and_nothing_failed_there': c.get('P0', {}).get('billing_pauses') == 1 and c.get('P0', {}).get('failed') == 0
            and near(c.get('P0', {}).get('billing_pause_seconds'), 2 * outage['retry_every_seconds']) and c.get('P0', {}).get('status') == 'done'
            and c.get('P0', {}).get('billing_affected_calls') == 1,
        'c_s1_done_with_one_failed_call': c.get('S1', {}).get('status') == 'done' and c.get('S1', {}).get('failed') == 1
            and c.get('S1', {}).get('invalid') == 1 and c.get('S1', {}).get('not_started') == 0,
        'c_bounds_reported': cu.get('failed') == 1 and cu.get('completed') == n_s1 - 1 and cu.get('every_unit_exactly_once') is True
            and cu.get('primary_bounds_all_assigned') not in (None, [None, None])
            and cu['primary_bounds_all_assigned'][0] <= -0.5 <= cu['primary_bounds_all_assigned'][1],
        'c_verify_exit_0': one.get('verify_exit') == 0,
        'd_exit_3_stopped_at_S1': many.get('exit') == 3 and many.get('state') == 'stopped_at_gate' and many.get('stopped_stage') == 'S1'
            and many.get('reason') == 'failed_units_over_limit',
        'd_dispatch_stopped': limit < (d.get('S1', {}).get('failed') or 0) <= limit + budget['workers']
            and (d.get('S1', {}).get('not_started') or 0) >= n_s1 - limit - 2 * budget['workers']
            and many.get('stub_answered') == 1 + budget['max_calls']['Q0'],
        'd_hub_s1_failed': [batch('S1'), 'failed'] in many.get('hub_runs', []) and many.get('hub_final_metrics_present') is True,
        'e_first_stop_is_a_billing_stop': first.get('exit') == 3 and first.get('reason') == provider.BILLING_STOP and first.get('stopped_stage') == 'S1'
            and first_s1_stage.get('failed') == 0 and first_s1_stage.get('resumable') is True
            and first_units.get('failed') == 0 and first_units.get('not_started', 0) > 0
            and near(first_s1_stage.get('billing_pause_seconds'), outage['max_wait_seconds']),
        'e_resume_completes': bill.get('resume_exit') == 0 and bill.get('state') == 'completed' and e.get('S1', {}).get('status') == 'done'
            and cont.get('batch') == batch('S1') + '-r1' and cont.get('status') == 'done' and cont.get('failed') == 0,
        'e_every_unit_exactly_once': eu.get('every_unit_exactly_once') is True and eu.get('completed') == n_s1 and eu.get('assigned') == n_s1
            and cont.get('units') == first_units.get('not_started') and eu.get('answered_calls') == n_s1 and eu.get('primary_estimate') == -0.5,
        'e_hub_runs': bill.get('hub_runs') == sorted([[batch(s), 'done'] for s in ('S0', 'P0', 'Q0')] + [[batch('S1'), 'failed'], [batch('S1') + '-r1', 'done']]),
        'e_answered_calls_within_caps': (bill.get('ledger') or {}).get('usage_reported_calls') == total
            and (bill.get('ledger') or {}).get('attempted_calls') == total and (bill.get('ledger') or {}).get('calls_by_batch', {}).get(batch('S1')) == n_s1
            and (bill.get('ledger') or {}).get('voided_calls') == voided and 0 < voided <= budget['workers']
            and (bill.get('ledger') or {}).get('transport_attempts', 10 ** 9) <= budget['max_transport_attempts'],
        'e_verify_exit_0': bill.get('verify_exit') == 0,
        'no_real_wait': sum(r.get('waits', 0) for r in (one, bill)) > 0 and time.monotonic() - started < 900,
        'committed_tree_untouched': not (study.ROOT / 'results').exists() or not any((study.ROOT / 'results').iterdir()),
    }
    ok = all(checks.values())
    brief = lambda r: {k: r.get(k) for k in ('label', 'exit', 'state', 'stopped_stage', 'reason', 'stages', 'continuations', 'hub_runs', 's1_units',
                                             'ledger', 'stub_requests', 'stub_answered', 'resume_exit', 'verify_exit', 'verify_seconds',
                                             'waits', 'waited_seconds_not_slept', 'seconds', 'projection', 'first_stop') if r.get(k) is not None}
    print(json.dumps({'ok': ok, 'rehearsal': 'passed' if ok else 'FAILED', 'checks': checks, 'checks_passed': sum(bool(v) for v in checks.values()),
                      'checks_total': len(checks), 'source_hash': study.source_hash(), 'model_calls_made': 0,
                      'full_chain': brief(full), 'failed_qualification': brief(gate), 'one_failed_call': brief(one),
                      'over_the_failure_limit': brief(many), 'billing_stop_and_resume': brief(bill),
                      'seconds': round(time.monotonic() - started, 1),
                      'note': 'stub answers only; nothing here is a sample and nothing left this machine'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
