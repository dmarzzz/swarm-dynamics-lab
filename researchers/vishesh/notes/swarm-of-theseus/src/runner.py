"""Bounded dedicated-host worker. S2 disabled; preflight precedes model creation."""
import argparse,concurrent.futures,datetime,hashlib,json,os,random,subprocess,time
from pathlib import Path
import yaml
from study import world,run_world,SCENARIOS,ARMS,digest
from provider import AnthropicPolicy
from public_plan import check
from render import image,replay
from analyze import analyze
ROOT=Path(__file__).resolve().parents[1]

def save(path,obj):Path(path).write_text(json.dumps(obj,indent=2))
def tldr(stage,scenario,arm):
    return f'TLDR: {stage} {scenario}, {arm}: tests useful procedure and arbitrary convention retention after turnover against '+('the verbatim competence ceiling and retained founders' if stage=='S0' else 'paired neither-channel and verbatim controls')+'; measures unseen-case accuracy at steps 4-5, convention retention and costs. Seeded single-model exploratory study, not confirmatory culture evidence.'

def run(a):
    import swarm_report as sr
    design=yaml.safe_load((ROOT/'design.yaml').read_text());cfg=design['stages'][a.stage]
    if a.stage=='S1':
        q=json.loads(Path(a.qualification).read_text())
        if not q.get('qualification_passed') or q.get('failed') or q.get('assigned')!=12:raise ValueError('qualification_gate')
    review=ROOT/'reviews'/f'{a.attempt}-pre.md'
    if not review.exists() or 'Status: ready' not in review.read_text():raise ValueError('committed_ready_review_required')
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    dirty=subprocess.check_output(['git','status','--porcelain','--',str(ROOT)],cwd=ROOT,text=True)
    if dirty.strip():raise ValueError('dirty_source')
    if os.environ.get('THESEUS_ALLOCATION')!='swarm-of-theseus-v1':raise ValueError('budget_allocation_required')
    if time.time()>float(os.environ['THESEUS_CLAIM_UNTIL']):raise ValueError('expired_claim')
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    assignments=[{'scenario':s,'seed':seed,'arm':arm} for s in SCENARIOS for seed in cfg['seeds'] for arm in cfg['arms']]
    random.Random(244).shuffle(assignments)
    # Each condition is publicly checked before any inference, and every assignment is frozen.
    receipts={f'{s}-{arm}':check('swarm-of-theseus',tldr(a.stage,s,arm)) for s in SCENARIOS for arm in cfg['arms']}
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.is_file() and p.suffix in ('.py','.json','.yaml','.md') and '__pycache__' not in str(p) and 'results' not in p.parts}
    manifest={'attempt':a.attempt,'stage':a.stage,'source':revision,'assignments':assignments,'source_hashes':hashes,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'allocation':'swarm-of-theseus-v1','claim':'vishesh-swarm-theseus','host':'sim-shadow','model':'claude-haiku-4-5-20251001','process_compliance':'preflight-passed'}
    save(out/'manifest.json',manifest)
    def execute(spec):
        key=f'{spec["scenario"]}-{spec["arm"]}-{spec["seed"]}';dest=out/key;dest.mkdir()
        rid=f'swarm-of-theseus/{a.attempt}-{key}'
        receipt=receipts[f'{spec["scenario"]}-{spec["arm"]}'];save(dest/'public-plan-receipt.json',receipt)
        params={**spec,'stage':a.stage,'backend':'anthropic','source_commit':revision,'attempt':a.attempt}
        hub=sr.start('swarm-of-theseus',run=rid,params=params,message=tldr(a.stage,spec['scenario'],spec['arm']))
        history=[];policy=None;started=time.time()
        with (dest/'events.jsonl').open('x') as journal:
            def emit(event):
                journal.write(json.dumps(event)+'\n');journal.flush()
                if event['kind']=='frame':
                    history.append(event);save(dest/'history.json',history)
                    frame={**spec,'history':history,'status':'running'};image(frame,dest/'final_frame.png')
                    hub.progress(event['step']+1,6,force=True,accuracy=event['accuracy'],convention=event['convention'],turnover=event['turnover'])
                    hub.artifact(dest/'final_frame.png','final_frame.png')
            try:
                if time.time()>float(os.environ['THESEUS_CLAIM_UNTIL']):raise ValueError('expired_claim')
                policy=AnthropicPolicy()
                row=run_world(world(spec['scenario'],spec['seed']),spec['arm'],policy,emit)
            except Exception as e:
                row={**spec,'status':'failed','error_type':type(e).__name__,'history':history,'missing_steps':list(range(len(history),6))}
        row['run']=rid;row['source_commit']=revision;row['elapsed_seconds']=time.time()-started
        row['usage']={k:getattr(policy,k,0) for k in ['calls','actual_usd','input_tokens','output_tokens','usage_missing']}
        row['process_compliance']='preflight-passed';save(dest/'outcome.json',row);image(row,dest/'final_frame.png');replay([row],dest/'replay.html')
        for p in [dest/'public-plan-receipt.json',dest/'outcome.json',dest/'events.jsonl',dest/'final_frame.png',dest/'replay.html',out/'manifest.json']:
            hub.artifact(p,p.name)
        if row['status']=='completed':hub.done(message='Execution complete; qualification and scientific interpretation require stage review.',accuracy=row['final_accuracy'],convention=row['final_convention'],calls=row['usage']['calls'],invalid=0)
        else:hub.fail(message='Recorded execution failure: '+row['error_type'])
        return row
    rows=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for row in pool.map(execute,assignments):rows.append(row)
    summary=analyze(rows);summary['stage']=a.stage;summary['source_commit']=revision
    save(out/'summary.json',summary);save(out/'rows.json',rows);replay(rows,out/'replay.html')
    print(json.dumps({'attempt':a.attempt,'assigned':len(rows),'failed':summary['failed'],'qualification_passed':summary['qualification_passed'],'cost':summary['cost']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--stage',choices=['S0','S1'],required=True);p.add_argument('--attempt',required=True);p.add_argument('--out',required=True);p.add_argument('--qualification');a=p.parse_args()
    try:run(a)
    except Exception as e:print(json.dumps({'status':'blocked_or_failed','error_type':type(e).__name__}));raise SystemExit(1)
