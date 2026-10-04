"""Native worker-local stage supervisor; no SSH tunnel or automatic model retry.

Run under a detached systemd service. Credential must be a mode-0600 file on
/dev/shm; relay unlinks it after reading. Original budget authority must already
be exclusively transferred and recorded before invocation.
"""
import argparse,json,os,signal,subprocess,sys,time,urllib.request
from pathlib import Path
from runtime import HERE,ATTEMPT,preflight

def main(a):
    if not str(a.credential.resolve()).startswith('/dev/shm/'):
        raise ValueError('credential_must_be_ephemeral')
    authority=json.loads(a.authority.read_text())
    if authority.get('attempt')!=ATTEMPT or authority.get('active_writer')!=os.uname().nodename or authority.get('local_dispatch_disabled') is not True:
        raise ValueError('single_writer_authority_required')
    if a.out.exists():raise ValueError('attempt_already_exists')
    preflight(json.loads(a.admission.read_text()),a.stage,a.parent)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    log_path=a.out.parent/(a.out.name+'-transport.jsonl')
    def interrupted(signum,frame):raise InterruptedError('supervisor_stopped')
    signal.signal(signal.SIGTERM,interrupted)
    with log_path.open('x') as log:
        relay=subprocess.Popen([sys.executable,str(HERE/'relay.py'),'--stage',a.stage,'--ledger',str(a.ledger),'--credential-file',str(a.credential),'--unlink-credential'],stdout=log,stderr=log)
        worker=None
        try:
            ready=False
            for _ in range(60):
                if relay.poll() is not None:raise RuntimeError('relay_startup_failed')
                try:
                    with urllib.request.urlopen('http://127.0.0.1:18443/health',timeout=1) as r:h=json.load(r)
                    ready=h.get('ready') and h.get('pid')==relay.pid and h.get('attempt')==ATTEMPT and h.get('stage')==a.stage
                except OSError:pass
                if ready:break
                time.sleep(.5)
            if not ready:raise RuntimeError('relay_startup_timeout')
            cmd=[sys.executable,str(HERE/'worker.py'),'--stage',a.stage,'--admission',str(a.admission),'--out',str(a.out)]
            if a.parent:cmd+=['--parent',str(a.parent)]
            worker=subprocess.Popen(cmd,stdout=log,stderr=log)
            end=time.monotonic()+(960 if a.stage=='S0' else 3660)
            while worker.poll() is None:
                if relay.poll() is not None or time.monotonic()>end:
                    worker.terminate()
                    raise RuntimeError('stage_transport_or_deadline_failure')
                time.sleep(.5)
            manifest=json.loads((a.out/'manifest.json').read_text())
            if worker.returncode or manifest['status']!='completed':raise RuntimeError('stage_failed_preserved')
            print(json.dumps({'stage':a.stage,'status':'completed','attempt':ATTEMPT}))
        finally:
            for process in (worker,relay):
                if process and process.poll() is None:
                    process.terminate()
                    try:process.wait(timeout=10)
                    except subprocess.TimeoutExpired:process.kill();process.wait()
            if a.credential.exists():a.credential.unlink()

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('credential','ledger','authority','admission','out'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--stage',choices=['S0','S1'],required=True);p.add_argument('--parent',type=Path)
    try:main(p.parse_args())
    except Exception as e:print(json.dumps({'supervisor_failed':type(e).__name__}));raise SystemExit(1)
