"""Immutable D0/D1 diagnostic runner. No hosted or local model calls."""
import argparse,collections,gzip,hashlib,json,random,subprocess,sys,time
from pathlib import Path
from repair import Board,Observation,VARIANTS,decide
V4=Path(__file__).resolve().parents[2]/'antsy-verification-v4'
sys.path.append(str(V4/'src'))
from policies import calibrate

def read(path):
 data=gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes()
 return json.loads(data) if path.name.removesuffix('.gz').endswith('.json') else [json.loads(x) for x in data.splitlines()]
def mean(xs):return sum(xs)/len(xs) if xs else None
def board(record,cal):return Board({m:r['observations'] for m,r in record['modes'].items()},cal['bias'])
def truth(record,choice):return record['modes'][choice]['evaluation']['recall']
def purchase(record,action):return Observation(*action,record['modes'][action[0]]['evaluation']['regions'][action[1]])

def d0(records,cal):
 by_id={r['id']:r for r in records};rows=[];traces=[]
 for backend,run in [('Laya','S1-attempt-1'),('Jev','S1-jev-attempt-1')]:
  episodes=read(V4/'results'/run/'episodes.jsonl.gz');assert [b['id'] for b in episodes]==list(range(30,100))
  for block in episodes:
   r=by_id[block['id']]
   for arm,result in block['arms'].items():
    b=board(r,cal);events=[{'step':0,'scores':{v:b.scores(v) for v in VARIANTS},'check':None}]
    for c in result['checks']:
     obs=Observation(**c);assert obs==purchase(r,(obs.mode,obs.region));b.buy(obs)
     events.append({'step':len(b.checks),'scores':{v:b.scores(v) for v in VARIANTS},'check':c})
    for v in VARIANTS:
     choice=cal['best_fixed'] if arm=='best-fixed' else b.choose(v)
     if v=='original':assert choice==result['choice'] and abs(truth(r,choice)-result['metrics']['quality'])<1e-12
     rows.append({'id':r['id'],'backend':backend,'arm':arm,'estimator':v,'choice':choice,'quality':truth(r,choice),'regret':max(truth(r,m) for m in 'ABC')-truth(r,choice),'checks':len(b.checks),'initial_quality':truth(r,board(r,cal).choose()),'original_quality':result['metrics']['quality']})
    if arm=='swarm-adaptive':traces.append({'id':r['id'],'backend':backend,'events':events,'truth':{m:truth(r,m) for m in 'ABC'}})
 summary=[]
 for backend in ['Laya','Jev']:
  for arm in episodes[0]['arms']:
   for v in VARIANTS:
    rs=[r for r in rows if (r['backend'],r['arm'],r['estimator'])==(backend,arm,v)]
    summary.append({'backend':backend,'arm':arm,'estimator':v,'n':len(rs),'quality':mean([r['quality'] for r in rs]),'regret':mean([r['regret'] for r in rs]),'harms':sum(r['quality']<r['initial_quality']-1e-12 for r in rs),'helps':sum(r['quality']>r['initial_quality']+1e-12 for r in rs),'delta_original':mean([r['quality']-r['original_quality'] for r in rs])})
 return rows,{'conditions':summary,'interpretation':'Retrospective fixed-purchase estimator intervention; no new agent behavior or independent efficacy estimate'},traces

def d1(records,cal):
 calibration=records[:20];assert [r['id'] for r in calibration]==list(range(20));rows=[]
 for r in records[30:100]:
  for cost in [0,.01,.02,.05,.10]:
   for arm in ['confidence-only','random-two','forced-two','cost-aware']:
    b=board(r,cal);events=[];rng=random.Random(f"{r['id']}:71")
    if arm!='confidence-only':
     for step in range(2):
      if arm=='random-two':action=rng.choice(b.available());values={}
      else:action,values=decide(b,calibration,cost,forced=arm=='forced-two')
      ev={'step':step,'scores_before':b.scores(),'choice_before':b.choose(),'action':action,'projected_gains':{f'{m}:{j}':v for (m,j),v in values.items()},'cost':cost}
      if action is None:ev.update(stop=True);events.append(ev);break
      obs=purchase(r,action);before=b.scores();b.buy(obs)
      if obs.quality is None:assert b.scores()==before
      ev.update(stop=False,response=vars(obs),scores_after=b.scores(),choice_after=b.choose());events.append(ev)
    choice=b.choose();quality=truth(r,choice)
    rows.append({'id':r['id'],'arm':arm,'cost':cost,'choice':choice,'quality':quality,'regret':max(truth(r,m) for m in 'ABC')-quality,'checks':len(b.checks),'utility':quality-cost*len(b.checks),'null_checks':sum(c.quality is None for c in b.checks),'events':events})
 summary=[]
 for cost in [0,.01,.02,.05,.10]:
  for arm in ['confidence-only','random-two','forced-two','cost-aware']:
   rs=[r for r in rows if (r['cost'],r['arm'])==(cost,arm)]
   summary.append({'cost':cost,'arm':arm,'n':len(rs),'quality':mean([r['quality'] for r in rs]),'checks':mean([r['checks'] for r in rs]),'utility':mean([r['utility'] for r in rs]),'stopped_before_two':sum(r['checks']<2 for r in rs),'null_checks':sum(r['null_checks'] for r in rs)})
 return rows,{'conditions':summary,'interpretation':'Development diagnostic on previously evaluated receipts; cost assumptions, ideal QA, approximate calibration scenarios; no independent generalization claim'},[]

def main():
 p=argparse.ArgumentParser();p.add_argument('--stage',choices=['D0','D1'],required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--report',action='store_true');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 source=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();rid='antsy-verification-v5/'+a.out.name
 manifest={'source':source,'stage':a.stage,'parent':'antsy-verification-v4','ids':list(range(30,100)),'complete':False,'model_calls':0,'utc_start':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())};start=time.monotonic()
 def save(): (a.out/'manifest.json').write_text(json.dumps(manifest,indent=2))
 save()
 if a.report:
  import swarm_report as sr
  sr.report('start','antsy-verification-v5',rid,params={'stage':a.stage,'kind':'diagnostic'},url=f'https://github.com/dmarzzz/swarm-lab/tree/{source}/researchers/vishesh/notes/antsy-verification-v5',message=f'{a.stage}: frozen retrospective engineering diagnostic; zero model calls, 70 old receipt units, no fresh efficacy claim.',strict=True)
 try:
  corpus=V4/'results/measured.jsonl.gz';records=read(corpus);assert [r['id'] for r in records]==list(range(100))
  manifest['corpus_sha256']=hashlib.sha256(gzip.decompress(corpus.read_bytes())).hexdigest();cal=calibrate(records[:20]);rows,summary,traces=(d0 if a.stage=='D0' else d1)(records,cal)
  for name,obj in [('rows.json',rows),('summary.json',summary),('traces.json',traces)]: (a.out/name).write_text(json.dumps(obj,indent=2))
  from render import render
  render(a.out,a.stage,summary,traces,rows)
  manifest.update(complete=True,receipts=70,rows=len(rows),wall_s=time.monotonic()-start);save()
  if a.report:
   for path in sorted(a.out.iterdir()):sr.upload(rid,path,path.name)
   sr.report('done','antsy-verification-v5',rid,metrics={'receipts':70,'model_calls':0,'rows':len(rows)},message=f'{a.stage} engineering diagnostic complete. Fixed data and cost assumptions; see post-mortem before promotion.',strict=True)
  print(json.dumps({'manifest':manifest,'summary':summary}))
 except Exception as e:
  manifest.update(error=type(e).__name__,wall_s=time.monotonic()-start);save()
  if a.report:sr.report('fail','antsy-verification-v5',rid,message=type(e).__name__,strict=True)
  raise
if __name__=='__main__':main()
