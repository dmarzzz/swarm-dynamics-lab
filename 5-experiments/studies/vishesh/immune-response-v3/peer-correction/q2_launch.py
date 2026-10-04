"""Central operator's bounded process-group launcher. No key transfer or retry."""
import argparse
import json
import os
import signal
import subprocess
import sys
from pathlib import Path

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--admission',required=True);p.add_argument('--ledger',required=True);a=p.parse_args()
    receipt=json.loads(Path(a.admission).read_text())
    limits={'peer-contract-q2':900}
    if receipt.get('stage') not in limits:raise ValueError('unknown_stage')
    env={k:os.environ[k] for k in ('PATH','HOME','USER','LANG') if k in os.environ}
    env.update(PYTHONPATH='/usr/local/lib/swarm',SWARM_SOURCE='vishesh/codex-immune')
    with Path(str(a.out)+'.log').open('xb') as log:
        os.chmod(log.name,0o600)
        proc=subprocess.Popen([sys.executable,str(Path(__file__).with_name('q2_worker.py')),'--out',a.out,'--admission',a.admission,'--ledger',a.ledger],env=env,stdout=log,stderr=log,start_new_session=True)
        try:code=proc.wait(timeout=limits[receipt['stage']])
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGTERM)
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
            code=124
    print(json.dumps({'worker_exit':code}));raise SystemExit(code)
