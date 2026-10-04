"""Bounded direct launcher; exact source/ledger/receipt and stdin-only key."""
import argparse,datetime,hashlib,json,os,re,resource,signal,socket,sqlite3,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
BASE=Path(__file__).resolve().parent

def validate(value):
 if not isinstance(value,dict) or set(value)!={'key','workspace'}:raise ValueError('unexpected_payload_fields')
 if not isinstance(value['key'],str) or not re.fullmatch(r'sk-ant-[A-Za-z0-9_-]{40,}',value['key']):raise ValueError('invalid_key')
 if not isinstance(value['workspace'],str) or not re.fullmatch(r'wrkspc_[A-Za-z0-9]+',value['workspace']):raise ValueError('invalid_routing')
 return value

def main():
 p=argparse.ArgumentParser();p.add_argument('--commit',required=True);p.add_argument('--ledger-sha',required=True);p.add_argument('--attempt',choices=['freshness-a5'],required=True);a=p.parse_args()
 root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=BASE,text=True).strip());resource.setrlimit(resource.RLIMIT_CORE,(0,0))
 assert re.fullmatch(r'[0-9a-f]{40}',a.commit) and subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()==a.commit
 assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=root).strip()
 ledger=root/'scenario-budget.sqlite';assert re.fullmatch(r'[0-9a-f]{64}',a.ledger_sha) and hashlib.sha256(ledger.read_bytes()).hexdigest()==a.ledger_sha
 with sqlite3.connect('file:'+str(ledger)+'?mode=ro',uri=True) as db:
  cap,reserved,calls=db.execute('select cap,reserved,calls from budget').fetchone();assert cap==8 and reserved+1.14432<=8 and db.execute('pragma integrity_check').fetchone()[0]=='ok'
 allocation=json.loads((root/'receipt-allocation.json').read_text());assert allocation['host']==socket.gethostname() and allocation['experiment']=='immune-response-v3' and allocation['cloud_account_verified'] is True and allocation['api_quota_usd']==8
 assert datetime.datetime.fromisoformat(allocation['expires'].replace('Z','+00:00'))-datetime.datetime.now(datetime.timezone.utc)>datetime.timedelta(minutes=70)
 sys.path.insert(0,str(BASE.parent.parent/'experiment-documentation'));from public_plan import check
 receipt=check('immune-response-v3','Freshness diagnostic, raw versus checked provenance,12 episodes60 calls, healthy ticks and unnecessary mutation; constructed-case limits.')
 assert receipt['commit']==a.commit and receipt['plan_sha256']==hashlib.sha256((BASE/'README.md').read_bytes()).hexdigest()
 out=root/a.attempt;assert not out.exists();fd=os.open(str(out)+'.dispatch',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.close(fd)
 env={k:os.environ[k] for k in ['PATH','HOME','USER','LANG'] if k in os.environ};env.update(PYTHONPATH='/usr/local/lib/swarm',SWARM_SOURCE='vishesh/codex-immune',SWARM_MODEL_BASE_URL='http://127.0.0.1:18765',SWARM_MODEL_CONFIG_FILE=str(BASE/'model-config.json'),SWARM_BUDGET_LEDGER=str(ledger))
 with (root/(a.attempt+'.log')).open('xb') as log:
  os.chmod(log.name,0o600);proc=subprocess.Popen([str(root/'.venv/bin/python'),str(BASE/'worker.py'),'--out',str(out),'--receipt',str(root/'receipt-allocation.json'),'--attempt',a.attempt,'--seed','9401'],env=env,cwd=root,stdout=log,stderr=log,start_new_session=True)
  env.clear()
  try:code=proc.wait(timeout=3600)
  except subprocess.TimeoutExpired:
   os.killpg(proc.pid,signal.SIGTERM)
   try:proc.wait(timeout=10)
   except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
   code=124
 print(json.dumps({'attempt':a.attempt,'worker_exit':code}));return code
if __name__=='__main__':
 try:raise SystemExit(main())
 except Exception as e:print(json.dumps({'launch_stopped':type(e).__name__}));raise SystemExit(1)
