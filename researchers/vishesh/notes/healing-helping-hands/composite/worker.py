"""Explicitly admitted, bounded C1 stages. No inference during import."""
import argparse,collections,hashlib,json,os,platform,subprocess,sys,time,urllib.request
from pathlib import Path
from definition import HERE,ARMS,SEEDS,LABELS,cases,request,wire,digest,assess
from qwen_trace import Qwen
from jev import validate
sys.path.insert(0,str(HERE.parent/'practical'))
from engine import ARMS as POLICIES,SCENARIOS,rollout
from reporting import Reporter
sys.path.insert(0,str(HERE.parent.parent/'experiment-documentation'))
from public_plan import check
from reference import corpus

def write(p,x):
    t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(x,indent=2));t.replace(p)
def append(p,x):
    with p.open('a') as f:f.write(json.dumps(x)+'\n');f.flush();os.fsync(f.fileno())
def sources(commit):
    root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=HERE,text=True).strip());out={}
    for folder in (HERE,HERE.parent/'src',HERE.parent/'practical'):
        for p in sorted(folder.glob('*.py')):
            rel=str(p.relative_to(root));expected=subprocess.check_output(['git','show',commit+':'+rel],cwd=root)
            if p.read_bytes()!=expected:raise ValueError('source_mismatch')
            out[rel]=hashlib.sha256(expected).hexdigest()
    return out

def admission(a,stage,now=None):
    now=time.time() if now is None else now
    if a.get('stage')!=stage or a.get('decision')!=('diagnostic-only' if stage=='S0' else 'ready'):raise ValueError('stage_not_admitted')
    if not 0<=now-a.get('checked_epoch',0)<=300:raise ValueError('stale_admission')
    for field in ('exclusive_claim_verified','workload_verified','budget_verified','page_verified'):
        if a.get(field) is not True:raise ValueError('missing_'+field)
    if a.get('claim_expires_epoch',0)<now+(1200 if stage=='S0' else 3900):raise ValueError('claim_too_short')
    if a.get('cumulative_usd_cap')!=.1:raise ValueError('budget_changed')
    if a.get('remaining_usd',0)<.001344:raise ValueError('budget_exhausted')
    if not a.get('host') or not a.get('claim_id'):raise ValueError('allocation_missing')
    return True

def run(out,stage,admit_path,parent=None):
    a=json.loads(admit_path.read_text());admission(a,stage)
    tldr=f'TLDR: C1 {stage}, Qwen 0.6B + Jev versus paired Qwen-only/Jev-only; measure correct labels, correction and anchoring before 200-curator repair. Synthetic feasibility, no independent-agent replication claim.'
    receipt=check('healing-helping-hands',tldr)
    if receipt['url']!=a['plan_url'] or receipt['plan_sha256']!=a['plan_sha256']:raise ValueError('wrong_registered_plan')
    if not receipt['url'].endswith('/composite/PLAN.md') or receipt['commit']!=a['source_commit']:raise ValueError('wrong_plan_source')
    hashes=sources(a['source_commit'])
    if stage=='S1':
        if parent is None:raise ValueError('qualification_required')
        q=json.loads((parent/'summary.json').read_text());pm=json.loads((parent/'manifest.json').read_text())
        if not q['admit_s1'] or pm['source_hashes']!=hashes:raise ValueError('unqualified_instrument')
    out.mkdir(parents=True,exist_ok=False);write(out/'admission.json',a);write(out/'plan-receipt.json',receipt)
    import swarm_report as sdk
    reporter=Reporter(sdk,'healing-helping-hands',f'healing-helping-hands/C1-{stage}',out/'reporting.jsonl')
    reporter.emit('start',url=receipt['url'],params={'attempt_id':'C1','stage':stage,'arm':'qwen+jev'},message=tldr)
    started=time.monotonic();deadline=started+(900 if stage=='S0' else 3600);counts={'qwen':0,'jev':0};limits={'qwen':60 if stage=='S0' else 600,'jev':120 if stage=='S0' else 1200}
    rows=[];worlds=[];manifest={'stage':stage,'attempt':'C1-'+stage,'plan':receipt,'source_hashes':hashes,'host':a['host'],'claim':a['claim_id'],'python':platform.python_version(),'status':'running','calls':counts}
    observations=[]
    if stage=='S0':observations=[{**c,'scope':'C1-S0','index':i} for i,c in enumerate(cases())]
    else:
        for seed in SEEDS:
            c=corpus(seed);write(out/f'corpus-{seed}.json',c)
            observations.extend({'id':f'{seed}-{i}','seed':seed,'index':i,'scope':f'C1-S1-{seed}','claim':c['claims'][d['claim']],'report':d['text'],'expected':d['label']} for i,d in enumerate(c['docs']))
        worlds=[{'id':f'{s}-{m}-{policy}-{scenario}','seed':s,'model':m,'arm':policy,'scenario':scenario,'layout':s+10000,'status':'planned'} for s in SEEDS for m in ARMS for policy in POLICIES for scenario in SCENARIOS]
    rows=[{**o,'labels':{},'status':'planned'} for o in observations];write(out/'observations.json',rows);write(out/'world-assignments.json',worlds);write(out/'manifest.json',manifest)
    def call(model,payload,fn):
        if time.monotonic()>=deadline or counts[model]>=limits[model]:raise RuntimeError('budget_exhausted')
        counts[model]+=1;cid=f'{model}-{counts[model]}';t=time.monotonic()
        append(out/'calls.jsonl',{'type':'start','id':cid,'model':model,'payload':payload,'payload_hash':digest(payload)})
        try:
            value=fn(min(30,deadline-time.monotonic()));append(out/'calls.jsonl',{'type':'completed','id':cid,'model':model,'result':value,'seconds':time.monotonic()-t});return value
        except Exception as e:
            append(out/'calls.jsonl',{'type':'failed','id':cid,'model':model,'error_type':type(e).__name__,'seconds':time.monotonic()-t});raise
    try:
        backend=Qwen();manifest['qwen_metadata']=backend.metadata
        for r in rows:
            r['status']='running';write(out/'observations.json',rows);obs={k:r[k] for k in ('claim','report')};i=r['index']
            # The journal saves report/seed plus pinned provider source; provider determines exact Qwen schema.
            q=call('qwen',{'observation':obs,'index':i},lambda timeout:backend.predict(obs,i,timeout));r['labels']['qwen']=q['label']
            for arm in (('jev','qwen+jev') if i%2==0 else ('qwen+jev','jev')):
                payload=request(obs,i,r['scope'],q['label'] if arm=='qwen+jev' else None)
                def infer(timeout):
                    with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:18443/decision',wire(payload),{'Content-Type':'application/json'}),timeout=timeout) as response:raw=json.load(response)
                    return {**validate(raw),'raw':raw}
                value=call('jev',payload,infer);r['labels'][arm]=value['label']
            r['status']='completed';write(out/'observations.json',rows)
            if sum(x['status']=='completed' for x in rows)%10==0:reporter.emit('metric',step=sum(x['status']=='completed' for x in rows),metrics={'completed_cases':sum(x['status']=='completed' for x in rows),'assigned_cases':len(rows),'model_calls':sum(counts.values())})
        write(out/'summary.json',assess(rows))
        if stage=='S1':
            for s in SEEDS:
                tapes={m:[r['labels'][m] for r in rows if r['seed']==s] for m in ARMS};write(out/f'tapes-{s}.json',tapes);c=json.loads((out/f'corpus-{s}.json').read_text())
                for w in (x for x in worlds if x['seed']==s):
                    if time.monotonic()>=deadline:raise TimeoutError('stage_deadline')
                    w['status']='running';write(out/'world-assignments.json',worlds)
                    result=rollout(c,tapes[w['model']],w['layout'],w['arm'],w['scenario'],cap=16)
                    w['status']='completed';write(out/(w['id']+'.json'),{**w,**result});write(out/'world-assignments.json',worlds)
                    n=sum(x['status']=='completed' for x in worlds)
                    if n%15==0:reporter.emit('metric',step=len(rows)+n,metrics={'completed_worlds':n,'assigned_worlds':270})
        manifest['status']='completed'
    except BaseException as e:
        manifest.update(status='failed',error_type=type(e).__name__)
    finally:
        for r in rows+worlds:
            if r['status']=='running':r['status']='failed'
            elif r['status']=='planned':r['status']='not_run'
        write(out/'observations.json',rows);write(out/'world-assignments.json',worlds);write(out/'summary.json',assess(rows))
        manifest.update(seconds=time.monotonic()-started,observation_counts=dict(collections.Counter(r['status'] for r in rows)),world_counts=dict(collections.Counter(w['status'] for w in worlds)));write(out/'manifest.json',manifest)
    reporter.emit('metric' if manifest['status']=='completed' else 'fail',metrics={'completed_cases':manifest['observation_counts'].get('completed',0)},message='C1 computation terminal; qualification and publication assessment follows.')
    print(json.dumps({'status':manifest['status'],'cases':manifest['observation_counts'],'worlds':manifest['world_counts'],'calls':counts}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--stage',choices=['S0','S1'],required=True);p.add_argument('--admission',type=Path,required=True);p.add_argument('--parent',type=Path);a=p.parse_args()
    try:run(a.out,a.stage,a.admission,a.parent)
    except Exception as e:print(json.dumps({'launch_failed':type(e).__name__}));raise SystemExit(1)
