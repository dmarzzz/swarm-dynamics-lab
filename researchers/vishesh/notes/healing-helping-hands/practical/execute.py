"""Bounded, fail-closed saved-tape runner. Never initializes a model provider."""
import argparse,collections,hashlib,json,platform,subprocess,sys,time
from pathlib import Path
from engine import ARMS,SCENARIOS,rollout
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent.parent/'experiment-documentation'))
from public_plan import check

def write(p,d):
 temp=p.with_suffix(p.suffix+'.tmp');temp.write_text(json.dumps(d,separators=(',',':')));temp.replace(p)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def source_check(commit):
 repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=HERE,text=True).strip())
 rel=HERE.relative_to(repo);tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',commit,'--',str(rel)],cwd=repo,text=True).splitlines();out={}
 for name in tracked:
  p=repo/name
  if p.read_bytes()!=subprocess.check_output(['git','show',commit+':'+name],cwd=repo):raise ValueError('source_mismatch')
  out[str(p.relative_to(HERE))]=sha(p)
 if not tracked or any(str(p.relative_to(repo)) not in tracked for p in HERE.glob('*.py')):raise ValueError('untracked_source')
 return out

def inputs(parent):
 expected=json.loads((HERE/'input-hashes.json').read_text());loaded={}
 for name,wanted in expected.items():
  p=parent/name
  if sha(p)!=wanted:raise ValueError('input_hash_mismatch')
  loaded[name]=json.loads(p.read_text())
 if loaded['qualification.json']['jev']['status']!='passed':raise ValueError('parent_unqualified')
 for seed in (8701,8702,8703):
  c=loaded[f'corpus-{seed}.json'];t=loaded[f'tapes-{seed}.json']['jev']
  if len(t)!=200 or t!=[d['label'] for d in c['docs']]:raise ValueError('unexpected_parent_tape')
 return loaded,expected

def assignments():return [{'id':f'{s}-{s+offset}-{scenario}-{arm}','seed':s,'layout':s+offset,'scenario':scenario,'arm':arm,'status':'planned'} for s in (8701,8702,8703) for offset in (10000,20000) for scenario in SCENARIOS for arm in ARMS]

def run(out,parent,tldr,hook=lambda kind,data:None,timeout=900):
 receipt=check('healing-helping-hands',tldr)
 if not receipt['url'].endswith('/practical/PLAN.md'):raise ValueError('wrong_plan')
 sources=source_check(receipt['commit']);loaded,hashes=inputs(parent)
 out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
 manifest={'attempt':'practical-01','parent_attempt':'pilot-03','stage':'S0','status':'running','plan':receipt,'source_hashes':sources,'input_hashes':hashes,'assignments':assignments(),'python':platform.python_version(),'model_calls':0,'inference_cost_usd':0,'host':'sim-vishesh','claim':'vishesh-healing-practical-01','started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
 write(out/'manifest.json',manifest);summary=[]
 for name,obj in loaded.items():write(out/name,obj)
 try:
  for a in manifest['assignments']:
   if time.monotonic()-start>timeout:raise TimeoutError('attempt_deadline')
   a['status']='running';write(out/'manifest.json',manifest);frames=[]
   try:
    def checkpoint(f):
     if time.monotonic()-start>timeout:raise TimeoutError('attempt_deadline')
     frames.append(f)
    result=rollout(loaded[f'corpus-{a["seed"]}.json'],loaded[f'tapes-{a["seed"]}.json']['jev'],a['layout'],a['arm'],a['scenario'],checkpoint)
    a['status']='completed';write(out/(a['id']+'.json'),{**a,**result});summary.append({**a,**result['metrics']})
   except BaseException as e:
    a.update(status='failed',error_type=type(e).__name__);write(out/(a['id']+'.json'),{**a,'frames':frames});raise
   finally:write(out/'manifest.json',manifest);write(out/'summary.json',summary)
   progress={'completed':len(summary),'assigned':180,'last_id':a['id']};write(out/'progress.json',progress);hook('progress',progress)
  manifest['status']='completed'
 except BaseException as e:manifest.update(status='failed',error_type=type(e).__name__)
 finally:
  for a in manifest['assignments']:
   if a['status']=='planned':a.update(status='not_run',reason='attempt_stopped');write(out/(a['id']+'.json'),a)
  manifest.update(seconds=time.monotonic()-start,terminal_counts=dict(collections.Counter(a['status'] for a in manifest['assignments'])))
  write(out/'manifest.json',manifest);write(out/'summary.json',summary)
 return manifest
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--run-tldr',required=True);a=p.parse_args()
 try:
  m=run(a.out,a.parent,a.run_tldr,lambda k,d:print(json.dumps(d),flush=True) if d['completed']%30==0 else None);print(json.dumps({k:m[k] for k in ('status','terminal_counts','seconds')}));sys.exit(m['status']!='completed')
 except Exception as e:print(json.dumps({'launch_error':type(e).__name__}));sys.exit(1)
