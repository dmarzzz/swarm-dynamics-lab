"""One-shot A3 launch after orbital-one dispatch; credentials arrive only on stdin."""
import argparse, hashlib, json, os, re, resource, sqlite3, subprocess, sys
from pathlib import Path

ROOT = Path('/srv/swarm/immune-response')
BASE = ROOT / 'researchers/vishesh/notes/immune-response-v3/evidence-study'
LEDGER_HASH = 'bb610d0eabc3c40dd5b8aec8d558ae77064c6b337cfbe1f4dbb5a13190adf243'

def payload(raw):
    value = json.loads(raw)
    if not isinstance(value, dict) or set(value) != {'key', 'workspace'}:
        raise ValueError('credential_payload_fields')
    if not isinstance(value['key'], str) or not re.fullmatch(r'sk-ant-[A-Za-z0-9_-]{40,}', value['key']):
        raise ValueError('credential_format')
    if not isinstance(value['workspace'], str) or not re.fullmatch(r'wrkspc_[A-Za-z0-9]+', value['workspace']):
        raise ValueError('routing_format')
    return value

def main():
    p = argparse.ArgumentParser(); p.add_argument('--expected-commit', required=True); a = p.parse_args()
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r'[0-9a-f]{40}', a.expected_commit) or head != a.expected_commit:
        raise ValueError('source_mismatch')
    if subprocess.check_output(['git', 'diff', '--name-only', 'HEAD'], cwd=ROOT).strip():
        raise ValueError('source_dirty')
    ledger = ROOT / 'scenario-budget.sqlite'
    if hashlib.sha256(ledger.read_bytes()).hexdigest() != LEDGER_HASH:
        raise ValueError('ledger_changed_or_attempt_already_dispatched')
    with sqlite3.connect(ledger) as conn:
        if conn.execute('pragma integrity_check').fetchone()[0] != 'ok':
            raise ValueError('ledger_integrity')
    sys.path.insert(0, str(BASE)); from worker import allocation
    receipt = allocation(ROOT / 'receipt-allocation.json')
    if receipt.get('cloud_account_verified') is not True:
        raise ValueError('account_not_verified')
    out = ROOT / 'receipt-native-a3'
    if out.exists(): raise ValueError('attempt_exists')
    # Reserve a one-shot dispatch marker without consuming API budget.
    marker = ROOT / 'receipt-native-a3.dispatch'
    with marker.open('x') as f: f.write(head + '\n')
    os.chmod(marker, 0o600)
    # Sender selects the authorized project-specific store; no fallback here.
    data = payload(sys.stdin.buffer.read(8193))
    env = {k: os.environ[k] for k in ('PATH','HOME','USER','LANG') if k in os.environ}
    env.update(PYTHONPATH='/usr/local/lib/swarm', SWARM_SOURCE='vishesh/codex-immune',
               SWARM_MODEL_BASE_URL='https://api.anthropic.com/v1',
               SWARM_MODEL_CONFIG_FILE=str(BASE/'model-config.json'),
               SWARM_BUDGET_LEDGER=str(ledger), SWARM_MODEL_API_KEY=data['key'],
               SWARM_MODEL_WORKSPACE_ID=data['workspace'])
    with (ROOT/'receipt-native-a3.log').open('xb') as log:
        os.chmod(log.name, 0o600)
        result = subprocess.run([str(ROOT/'.venv/bin/python'), str(BASE/'worker.py'),
                                 '--out', str(out), '--receipt', str(ROOT/'receipt-allocation.json')],
                                cwd=ROOT, env=env, stdout=log, stderr=log)
    env.clear(); data.clear()
    print(json.dumps({'attempt':'receipt-native-a3','worker_exit':result.returncode}))
    return result.returncode

if __name__ == '__main__':
    try: raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({'launch_stopped':type(exc).__name__})); raise SystemExit(1)
