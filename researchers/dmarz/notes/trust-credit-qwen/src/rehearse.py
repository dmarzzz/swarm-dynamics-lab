"""Offline rehearsal of the chain against a throwaway hub on 127.0.0.1 and a local model stub.

  python3 src/rehearse.py --hub-dir <directory holding hub.py and swarm_report.py>

No request leaves the machine: the hub is a local process and the model endpoint is replaced by
an in-process stub injected as the adapter's opener. A rehearsal answer is never a sample. Three
chains run in fresh temporary result and ledger directories:
  (a) all four stages with a stub that answers by the reference policy, then `chain verify`;
  (b) a stub that never abstains, which must fail qualification: exit 3, stopped_at_gate at Q0 and
      no S1 run on the hub;
  (c) a stub whose account runs out of credit during S1 and stays out: the stage must stop with
      provider_credit_balance_low and nothing failed; then, with credit restored, `chain resume`
      must finish S1 with every unit recorded exactly once, and `chain verify` must pass.
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
import provider  # noqa: E402
import study     # noqa: E402


def require_local(url):
    host = urllib.parse.urlparse(url or '').hostname
    if host != '127.0.0.1':
        raise SystemExit('rehearsal refused: the hub URL host must be 127.0.0.1')
    return url


class Response(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False


class Stub:
    """Stands in for the OpenRouter chat-completions endpoint and answers in its response shape.
    It rejects any request body that is not exactly the frozen template plus messages.
    credit_after: from that many answered S1-sized requests on, every request gets HTTP 402 until
    `restore()` is called."""

    def __init__(self, mode='reference', credit_after=None):
        assert mode in ('reference', 'never_abstain')
        self.mode = mode; self.lock = threading.Lock(); self.answered = 0; self.refused = 0
        self.credit_after = credit_after; self.out_of_credit = False

    def restore(self):
        with self.lock: self.out_of_credit = False; self.credit_after = None

    def __call__(self, request, timeout=None):
        if request.full_url != provider.URL:
            raise AssertionError('the rehearsal stub only answers the provider endpoint')
        body = json.loads(request.data)
        d = study.design()
        if tuple(body) != provider.BODY_KEYS or {k: body[k] for k in body if k != 'messages'} != d['request_template'] \
                or [m['role'] for m in body['messages']] != ['system', 'user']:
            raise urllib.error.HTTPError(provider.URL, 400, 'bad request', {}, io.BytesIO(b'{"error":{"message":"unexpected parameter"}}'))
        with self.lock:
            if self.credit_after is not None and self.answered >= self.credit_after: self.out_of_credit = True
            if self.out_of_credit:
                self.refused += 1
                raise urllib.error.HTTPError(provider.URL, 402, 'payment required', {},
                                             io.BytesIO(b'{"error":{"code":402,"message":"Insufficient credits. Add more to continue."}}'))
            self.answered += 1
        answer = study.scripted(json.loads(body['messages'][1]['content']))
        if self.mode == 'never_abstain':
            answer = {'values': {k: (0 if v is None else v) for k, v in answer['values'].items()}}
        tokens = int(len(request.data) * 0.45)
        return Response(json.dumps({
            'id': 'gen-rehearsal', 'model': d['canonical_model'], 'provider': 'Alibaba', 'object': 'chat.completion',
            'choices': [{'index': 0, 'finish_reason': 'stop', 'message': {'role': 'assistant', 'content': json.dumps(answer)}}],
            'usage': {'prompt_tokens': tokens, 'completion_tokens': 40, 'total_tokens': tokens + 40,
                      'completion_tokens_details': {'reasoning_tokens': 0}}}).encode())


class FakeClock:
    """Injected into the adapter so the billing-outage schedule does not wait in real time."""
    def __init__(self): self.offset = 0.0; self.lock = threading.Lock()
    def now(self):
        with self.lock: return time.monotonic() + self.offset
    def sleep(self, seconds):
        with self.lock: self.offset += seconds


def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0)); return s.getsockname()[1]


def start_hub(hub_dir, data_dir, token):
    port = free_port()
    log = open(Path(data_dir) / 'hub.log', 'w')
    proc = subprocess.Popen([sys.executable, str(Path(hub_dir) / 'hub.py'), '--data', str(Path(data_dir) / 'hubdata'), '--port', str(port)],
                            env=dict(os.environ, SWARM_HUB_TOKEN=token), stdout=log, stderr=subprocess.STDOUT)
    for _ in range(100):
        if proc.poll() is not None: raise SystemExit('the throwaway hub exited at start; see ' + log.name)
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=0.2): break
        except OSError: time.sleep(0.1)
    else:
        proc.terminate(); raise SystemExit('the throwaway hub did not start')
    return proc, f'http://127.0.0.1:{port}'


def snapshot(sr, stub):
    status = chain.read_status(); runs = sr.runs(study.EXPERIMENT, limit=5000)
    return {'state': status['state'], 'stopped_stage': status.get('stopped_stage'), 'reason': status.get('reason'),
            'stages': {s: {k: e.get(k) for k in ('status', 'calls', 'planned', 'valid', 'failed', 'not_started', 'cost_usd', 'qualification_passed', 'billing_pauses')}
                       for s, e in status['stages'].items()},
            'continuations': [{k: c.get(k) for k in ('batch', 'status', 'units', 'calls', 'valid')} for c in status['stages'].get('S1', {}).get('continuations', [])],
            'hub_runs': sorted(((r.get('params') or {}).get('batch'), r['status']) for r in runs),
            'hub_final_metrics_present': all(all(k in (r.get('metrics') or {}) for k in
                                                 ('episodes', 'invalid', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd')) for r in runs),
            'stub_answered': stub.answered, 'stub_refused': stub.refused, 'ledger': chain.ledger_totals()}


def chain_once(label, stub, hub_dir, base, sr, then_resume=False):
    work = Path(base) / label; work.mkdir()
    token = 'rehearsal-' + secrets.token_hex(12)
    proc, url = start_hub(hub_dir, work, token)
    os.environ.update(SWARM_HUB_URL=require_local(url), SWARM_HUB_TOKEN=token, SWARM_SOURCE='dmarz/pipeline-split-rehearsal',
                      SWARM_SPOOL=str(work / 'spool'), STUDY_RESULTS_DIR=str(work / 'results'),
                      STUDY_BUDGET_LEDGER=str(work / 'ledger' / 'ledger.jsonl'))
    os.environ[provider.KEY_ENV] = 'rehearsal-stub-not-a-credential'
    require_local(sr._config().get('SWARM_HUB_URL'))
    started = time.monotonic(); clock = FakeClock(); result = {'label': label, 'stub': stub.mode}
    try:
        result['exit'] = chain.run_chain(list(study.STAGES), sr=sr, opener=stub, clock=clock.now, sleep=clock.sleep)
        result.update(snapshot(sr, stub))
        if then_resume:
            stub.restore()
            result['resume_exit'] = chain.resume(sr=sr, opener=stub, clock=clock.now, sleep=clock.sleep)
            result['after_resume'] = snapshot(sr, stub)
        if result['exit'] == 0 or then_resume:
            result['verify_exit'] = chain.verify(sr)
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
    ap.add_argument('--tmp', help='parent directory for the temporary files')
    a = ap.parse_args()
    hub_dir = Path(a.hub_dir).resolve()
    if not (hub_dir / 'hub.py').is_file() or not (hub_dir / 'swarm_report.py').is_file():
        raise SystemExit('--hub-dir must hold hub.py and swarm_report.py')
    os.environ['SWARM_HUB_URL'] = 'http://127.0.0.1:9'; os.environ['SWARM_HUB_TOKEN'] = 'rehearsal-not-started-yet'
    sys.path.insert(0, str(hub_dir))
    import swarm_report as sr
    base = tempfile.mkdtemp(prefix='trust-credit-rehearsal-', dir=a.tmp); started = time.monotonic()
    b = study.design()['budget']; total = sum(b['max_calls'].values()); q = b['max_calls']['P0'] + b['max_calls']['Q0']; cut = q + 150
    try:
        full = chain_once('a-full-chain', Stub('reference'), hub_dir, base, sr)
        gate = chain_once('b-failed-qualification', Stub('never_abstain'), hub_dir, base, sr)
        bill = chain_once('c-billing-stop-and-resume', Stub('reference', credit_after=cut), hub_dir, base, sr, then_resume=True)
    finally:
        if not a.keep: shutil.rmtree(base, ignore_errors=True)
    batches = [study.batch(s) for s in study.STAGES]; after = bill.get('after_resume') or {}
    checks = {
        'a_exit_0': full.get('exit') == 0, 'a_state_completed': full.get('state') == 'completed',
        'a_four_done_runs': full.get('hub_runs') == sorted((x, 'done') for x in batches),
        'a_calls_equal_caps': {s: e.get('calls') for s, e in full.get('stages', {}).items()} == b['max_calls'],
        'a_ledger_calls': (full.get('ledger') or {}).get('attempted_calls') == total and full.get('stub_answered') == total,
        'a_hub_metrics_present': full.get('hub_final_metrics_present') is True,
        'a_verify_exit_0': full.get('verify_exit') == 0, 'a_spool_empty': full.get('spool_empty') is True,
        'b_exit_3': gate.get('exit') == 3, 'b_state_stopped_at_gate': gate.get('state') == 'stopped_at_gate',
        'b_stopped_at_Q0': gate.get('stopped_stage') == 'Q0' and gate.get('reason') == 'gate_failed',
        'b_no_S1_run_on_hub': all(not str(x).startswith('s1') for x, _ in gate.get('hub_runs', [('s1', '')])),
        'b_only_qualification_calls': gate.get('stub_answered') == q,
        'c_stop_exit_3': bill.get('exit') == 3 and bill.get('reason') == provider.BILLING_STOP and bill.get('stopped_stage') == 'S1',
        'c_nothing_failed_at_stop': (bill.get('stages') or {}).get('S1', {}).get('failed') == 0
                                    and (bill.get('stages') or {}).get('S1', {}).get('valid') == 150
                                    and (bill.get('stages') or {}).get('S1', {}).get('billing_pauses') == 1,
        'c_resume_exit_0': bill.get('resume_exit') == 0 and after.get('state') == 'completed',
        'c_continuation_holds_the_rest': [(c['batch'], c['status'], c['units'], c['valid']) for c in after.get('continuations', [])]
                                         == [(study.batch('S1') + '-r1', 'done', 504 - 150, 504 - 150)],
        'c_every_unit_answered_once': after.get('stub_answered') == total,
        'c_s1_calls_inside_the_exact_cap': (after.get('ledger') or {}).get('calls_by_batch', {}).get(study.batch('S1')) == b['max_calls']['S1']
                                           and (after.get('ledger') or {}).get('voided_calls', 0) >= 1
                                           and (after.get('ledger') or {}).get('attempted_calls') == total,
        'c_verify_exit_0': bill.get('verify_exit') == 0,
    }
    ok = all(checks.values())
    print(json.dumps({'ok': ok, 'checks': checks, 'full_chain': full, 'failed_qualification': gate, 'billing_stop_and_resume': bill,
                      'seconds': round(time.monotonic() - started, 1),
                      'note': 'stub answers only; nothing here is a sample and nothing left this machine'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
