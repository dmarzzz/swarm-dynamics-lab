"""Offline rehearsal of the whole chain against a throwaway hub on 127.0.0.1 and a local model stub.

  python3 src/rehearse.py --hub-dir <directory holding hub.py and swarm_report.py>

No request leaves the machine: the hub is a local process, and the model endpoint is replaced by
an in-process stub injected as the adapter's opener. A rehearsal answer is never a sample. The
chain runs twice in fresh temporary result and ledger directories:
  (a) all four stages with a stub that answers by the plurality rule, then `chain verify`;
  (b) with a stub that never abstains, which must fail qualification: the chain must stop at Q0
      with a non-zero exit, state stopped_at_gate, and no S1 run on the hub.
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
    """Stands in for the two provider endpoints. It answers in the real response shape, with a
    thinking block before the text block, and rejects any request body the real model would
    reject for carrying a key outside the contract."""

    def __init__(self, mode):
        assert mode in ('plurality', 'never_abstain')
        self.mode = mode; self.lock = threading.Lock(); self.counts = 0; self.messages = 0

    def __call__(self, request, timeout=None):
        url = request.full_url
        if url not in (provider.MESSAGES_URL, provider.COUNT_URL):
            raise AssertionError('the rehearsal stub only answers the two provider endpoints')
        body = json.loads(request.data)
        allowed = set(provider.BODY_KEYS) - ({'max_tokens'} if url == provider.COUNT_URL else set())
        if set(body) != allowed or set(body['output_config']) != {'effort', 'format'}:
            raise urllib.error.HTTPError(url, 400, 'invalid_request_error', {}, io.BytesIO(b'{}'))
        tokens = max(1, len(body['messages'][0]['content']) // 2 + len(body['system']) // 4)
        if url == provider.COUNT_URL:
            with self.lock: self.counts += 1
            return Response(json.dumps({'input_tokens': tokens}).encode())
        with self.lock: self.messages += 1
        answer = study.scripted(json.loads(body['messages'][0]['content']))
        if self.mode == 'never_abstain':
            answer = {'values': {k: (0 if v is None else v) for k, v in answer['values'].items()}}
        return Response(json.dumps({
            'id': 'msg_rehearsal', 'type': 'message', 'role': 'assistant', 'model': body['model'],
            'content': [{'type': 'thinking', 'thinking': '', 'signature': 'rehearsal'},
                        {'type': 'text', 'text': json.dumps(answer)}],
            'stop_reason': 'end_turn', 'stop_sequence': None,
            'usage': {'input_tokens': tokens, 'output_tokens': 40, 'cache_creation_input_tokens': 0,
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


def chain_once(label, mode, hub_dir, base, sr):
    work = Path(base) / label; work.mkdir()
    token = 'rehearsal-' + secrets.token_hex(12)
    proc, url = start_hub(hub_dir, work, token)
    os.environ.update(SWARM_HUB_URL=require_local(url), SWARM_HUB_TOKEN=token, SWARM_SOURCE='dmarz/pipeline-split-rehearsal',
                      SWARM_SPOOL=str(work / 'spool'), STUDY_RESULTS_DIR=str(work / 'results'),
                      STUDY_BUDGET_LEDGER=str(work / 'ledger' / 'ledger.jsonl'),
                      SWARM_MODEL_API_KEY='rehearsal-stub-not-a-credential', SWARM_MODEL_WORKSPACE_ID='rehearsal-stub')
    require_local(sr._config().get('SWARM_HUB_URL'))
    stub = Stub(mode); started = time.monotonic(); result = {'label': label, 'stub': mode}
    try:
        result['exit'] = chain.run_chain(list(study.STAGES), sr=sr, opener=stub)
        status = chain.read_status(); runs = sr.runs(study.EXPERIMENT, limit=5000)
        result.update(state=status['state'], stopped_stage=status.get('stopped_stage'), reason=status.get('reason'),
                      stages={s: {k: e.get(k) for k in ('status', 'calls', 'planned', 'valid', 'cost_usd', 'qualification_passed')}
                              for s, e in status['stages'].items()},
                      hub_runs=sorted(((r.get('params') or {}).get('stage'), r['status']) for r in runs),
                      hub_final_metrics_present=all(all(k in (r.get('metrics') or {}) for k in
                          ('episodes', 'invalid', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd')) for r in runs),
                      stub_messages=stub.messages, stub_counts=stub.counts, ledger=chain.ledger_totals())
        if mode == 'plurality':
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
    a = ap.parse_args()
    hub_dir = Path(a.hub_dir).resolve()
    if not (hub_dir / 'hub.py').is_file() or not (hub_dir / 'swarm_report.py').is_file():
        raise SystemExit('--hub-dir must hold hub.py and swarm_report.py')
    # Set a local address before the client is imported, and check it again before every use.
    os.environ['SWARM_HUB_URL'] = 'http://127.0.0.1:9'; os.environ['SWARM_HUB_TOKEN'] = 'rehearsal-not-started-yet'
    sys.path.insert(0, str(hub_dir))
    import swarm_report as sr
    base = tempfile.mkdtemp(prefix='sybil-split-rehearsal-'); started = time.monotonic()
    budget = study.design()['budget']; total = budget['max_attempted_calls']
    try:
        full = chain_once('a-full-chain', 'plurality', hub_dir, base, sr)
        gate = chain_once('b-failed-qualification', 'never_abstain', hub_dir, base, sr)
    finally:
        if not a.keep: shutil.rmtree(base, ignore_errors=True)
    checks = {
        'a_exit_0': full.get('exit') == 0, 'a_state_completed': full.get('state') == 'completed',
        'a_four_done_runs': full.get('hub_runs') == [(s, 'done') for s in sorted(study.STAGES)],
        'a_calls_equal_caps': {s: e.get('calls') for s, e in full.get('stages', {}).items()} == budget['max_calls'],
        'a_ledger_calls': (full.get('ledger') or {}).get('attempted_calls') == total and full.get('stub_messages') == total,
        'a_hub_metrics_present': full.get('hub_final_metrics_present') is True,
        'a_verify_exit_0': full.get('verify_exit') == 0, 'a_spool_empty': full.get('spool_empty') is True,
        'b_exit_3': gate.get('exit') == 3, 'b_state_stopped_at_gate': gate.get('state') == 'stopped_at_gate',
        'b_stopped_at_Q0': gate.get('stopped_stage') == 'Q0',
        'b_no_S1_run_on_hub': all(stage != 'S1' for stage, _ in gate.get('hub_runs', [('S1', '')])),
        'b_hub_runs': gate.get('hub_runs') == [('P0', 'done'), ('Q0', 'failed'), ('S0', 'done')],
        'b_hub_metrics_present': gate.get('hub_final_metrics_present') is True,
        'b_only_p0_and_q0_calls': gate.get('stub_messages') == budget['max_calls']['P0'] + budget['max_calls']['Q0'],
    }
    ok = all(checks.values())
    print(json.dumps({'ok': ok, 'checks': checks, 'full_chain': full, 'failed_qualification': gate,
                      'seconds': round(time.monotonic() - started, 1),
                      'note': 'stub answers only; nothing here is a sample and nothing left this machine'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
