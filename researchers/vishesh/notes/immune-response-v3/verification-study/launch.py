"""Verification v1 process-group watchdog. No automatic restart or credential transfer."""
import argparse,json,os,signal,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--admission',required=True);a=p.parse_args()
    out=Path(a.out);assert not out.exists()
    env={k:os.environ[k] for k in ['PATH','HOME','USER','LANG','SWARM_BUDGET_LEDGER','SWARM_MODEL_BASE_URL'] if k in os.environ}
    env.update(PYTHONPATH='/usr/local/lib/swarm',SWARM_SOURCE='vishesh/codex-immune')
    with Path(str(out)+'.log').open('xb') as log:
        os.chmod(log.name,0o600)
        proc=subprocess.Popen([sys.executable,str(BASE/'worker.py'),'--out',str(out),'--admission',a.admission],env=env,stdout=log,stderr=log,start_new_session=True)
        try:code=proc.wait(timeout=3600)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGTERM)
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
            code=124
    print(json.dumps({'worker_exit':code}));raise SystemExit(code)
