"""Local software fixtures only; no OCR, model packages, network or real receipts."""
import argparse,json,os,signal,subprocess,sys,time
from pathlib import Path
from telemetry import Phases,PHASES

p=argparse.ArgumentParser();p.add_argument('--mode',required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--phases',type=Path,required=True);a=p.parse_args()
f=Phases(a.phases)
for name in PHASES[:6]:f.emit(name)
os.write(1,b'PRIVATE_STDOUT_FIXTURE\n');os.write(2,b'PRIVATE_STDERR_FIXTURE\n')
if a.mode=='error':sys.exit(7)
if a.mode=='signal':os.kill(os.getpid(),signal.SIGTERM)
if a.mode in ('timeout','descendant'):
    if a.mode=='descendant':
        code="import pathlib,time; p=pathlib.Path('"+str(a.out.parent/'child-heartbeat')+"');\nwhile True:\n p.write_text(str(time.monotonic())); time.sleep(.02)"
        child=subprocess.Popen([sys.executable,'-c',code]);(a.out.parent/'child-pid').write_text(str(child.pid))
    time.sleep(30)
if a.mode=='slow':time.sleep(.15)
for name in PHASES[6:]:f.emit(name)
f.close()
if a.mode=='partial_phase':
    with a.phases.open('ab') as h:h.write(b'{"seq":11,')
if a.mode=='duplicate_phase':
    with a.phases.open('ab') as h:h.write(a.phases.read_bytes().splitlines()[0]+b'\n')
if a.mode=='symlink_output':
    a.out.symlink_to(a.phases);sys.exit(0)
if a.mode=='invalid_output':a.out.write_text('{bad');sys.exit(0)
a.out.write_text(json.dumps({'candidate':{'status':'ok','value':'10.00','contract':'anchor-row-v2','evidence':[],'reasons':[]},'raw_words':[]}))
