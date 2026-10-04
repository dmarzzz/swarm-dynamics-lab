"""Offline rehearsal of the whole chain against a throwaway hub on 127.0.0.1 and a local model stub.

  python3 src/rehearse.py --hub-dir <directory holding hub.py and swarm_report.py>

No request leaves the machine: the hub is a local process, and the model endpoint is replaced by
an in-process stub injected as the adapter's opener. A rehearsal answer is never a sample. The
chain runs twice in fresh temporary result and ledger directories:
  (a) all four stages with a stub that answers every turn by the scripted `parallel` reference
      planner, computed from the request it receives, then `chain verify`;
  (b) with a stub that never creates a subagent, which must fail qualification (no job without
      a quota can be finished by one identity): the chain must stop at Q0 with a non-zero exit,
      state stopped_at_gate, and no S1 run on the hub.
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


class Stub:
    """Stands in for the two provider endpoints. It answers in the real response shape, with a
    thinking block before the text block, and rejects any request body the real model would
    reject for carrying a key outside the contract. Its answer to a turn is computed from the
    request alone: the system prompt names the rules, the user message is the state."""

    def __init__(self, mode):
        assert mode in ('parallel', 'never_spawn')
        self.mode = mode; self.lock = threading.Lock(); self.counts = 0; self.messages = 0

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
            with self.lock: self.counts += 1
            return Response(json.dumps({'input_tokens': tokens}).encode())
        with self.lock: self.messages += 1
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


def chain_once(label, mode, hub_dir, base, sr):
    work = Path(base) / label; work.mkdir()
    token = 'rehearsal-' + secrets.token_hex(12)
    proc, url = start_hub(hub_dir, work, token)
    os.environ.update(SWARM_HUB_URL=require_local(url), SWARM_HUB_TOKEN=token, SWARM_SOURCE='dmarz/pipeline-quota-rehearsal',
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
        if mode == 'parallel':
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
    base = tempfile.mkdtemp(prefix='quota-splitting-rehearsal-'); started = time.monotonic()
    budget = study.design()['budget']; total = budget['max_attempted_calls']
    try:
        full = chain_once('a-full-chain', 'parallel', hub_dir, base, sr)
        gate = chain_once('b-failed-qualification', 'never_spawn', hub_dir, base, sr)
    finally:
        if not a.keep: shutil.rmtree(base, ignore_errors=True)
    calls = full.get('stages', {}); made = sum((e.get('calls') or 0) for e in calls.values())
    checks = {
        'a_exit_0': full.get('exit') == 0, 'a_state_completed': full.get('state') == 'completed',
        'a_four_done_runs': full.get('hub_runs') == [(s, 'done') for s in sorted(study.STAGES)],
        'a_calls_within_caps': all(0 <= (e.get('calls') if e.get('calls') is not None else -1) <= budget['max_calls'][s] for s, e in calls.items()) and len(calls) == 4,
        'a_paid_stages_called': calls.get('S0', {}).get('calls') == 0 and calls.get('P0', {}).get('calls') == 1
                                and (calls.get('Q0', {}).get('calls') or 0) > 0 and (calls.get('S1', {}).get('calls') or 0) > 0,
        'a_ledger_calls': (full.get('ledger') or {}).get('attempted_calls') == made and full.get('stub_messages') == made and 0 < made <= total,
        'a_hub_metrics_present': full.get('hub_final_metrics_present') is True,
        'a_verify_exit_0': full.get('verify_exit') == 0, 'a_spool_empty': full.get('spool_empty') is True,
        'b_exit_3': gate.get('exit') == 3, 'b_state_stopped_at_gate': gate.get('state') == 'stopped_at_gate',
        'b_stopped_at_Q0': gate.get('stopped_stage') == 'Q0',
        'b_no_S1_run_on_hub': all(stage != 'S1' for stage, _ in gate.get('hub_runs', [('S1', '')])),
        'b_hub_runs': gate.get('hub_runs') == [('P0', 'done'), ('Q0', 'failed'), ('S0', 'done')],
        'b_hub_metrics_present': gate.get('hub_final_metrics_present') is True,
        'b_only_p0_and_q0_calls': gate.get('stub_messages') == sum((gate.get('stages', {}).get(s, {}).get('calls') or 0) for s in ('P0', 'Q0'))
                                  and 1 < (gate.get('stub_messages') or 0) <= budget['max_calls']['P0'] + budget['max_calls']['Q0'],
    }
    ok = all(checks.values())
    print(json.dumps({'ok': ok, 'checks': checks, 'full_chain': full, 'failed_qualification': gate,
                      'seconds': round(time.monotonic() - started, 1),
                      'note': 'stub answers only; nothing here is a sample and nothing left this machine'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
