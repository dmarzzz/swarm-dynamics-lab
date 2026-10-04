"""PC-1L bounded worker; requires external authorization, allocation and public plan."""
import argparse,contextlib,datetime,hashlib,json,os,subprocess,sys,time,urllib.error,urllib.request
from pathlib import Path
from budget import Budget
from instrument import canonical,digest,world,request_for_assignment
from native import MODEL,SNAPSHOT,RATE,RESERVE_NANO,request,validate,schedule,qualification,analyze_history

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*a,**k):raise ValueError('redirect_refused')

def save(path,obj):
    tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(obj,indent=2,allow_nan=False));tmp.replace(path)

def quiet(fn,*args,**kwargs):
    with open(os.devnull,'w') as sink,contextlib.redirect_stdout(sink),contextlib.redirect_stderr(sink):return fn(*args,**kwargs)

def verify_config(c,stage,root):
    if c.get('experiment')!='phantom-coast' or c.get('stage')!=stage or c.get('design')!='PC-1L':raise ValueError('configuration_binding')
    cap=c.get('api_cap_usd')
    if c.get('spending_authorized') is not True or type(cap) not in (int,float) or not 0<cap<=20 or not c.get('authorization_reference'):raise ValueError('spending_authorization_required')
    if c.get('exploratory_launch_authorized') is not True:raise ValueError('exploratory_scope_required')
    if not c.get('host') or not c.get('claim_id') or c.get('claim_exclusive') is not True:raise ValueError('exclusive_allocation_required')
    now=datetime.datetime.now(datetime.timezone.utc)
    if datetime.datetime.fromisoformat(c['claim_until'].replace('Z','+00:00'))<now+datetime.timedelta(hours=2):raise ValueError('claim_too_short')
    # A receipt is issued only by a fresh private-fleet check, not by the worker itself.
    checked=datetime.datetime.fromisoformat(c['claim_checked_utc'].replace('Z','+00:00'))
    if not datetime.timedelta(0)<=now-checked<datetime.timedelta(minutes=5):raise ValueError('fresh_claim_check_required')
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    if c.get('source_commit')!=head:raise ValueError('source_commit')
    required=['src/instrument.py','src/native.py','src/budget.py','src/live_worker.py','src/live_render.py','LIVE-PLAN.md']
    base=root/'researchers/vishesh/notes/phantom-coast'
    if set(c.get('file_hashes',{}))!=set(required):raise ValueError('source_manifest')
    for name in required:
        if hashlib.sha256((base/name).read_bytes()).hexdigest()!=c['file_hashes'][name]:raise ValueError('source_hash')
    if c.get('assignment_sha256')!=digest(schedule(stage)):raise ValueError('assignment_hash')
    if stage=='S0':
        q=json.loads(Path(c['qualification_result']).read_text())
        if q.get('qualification_passed') is not True or q.get('model')!=SNAPSHOT or q.get('design')!='PC-1L' or q.get('source_commit')!=head:raise ValueError('qualification_required')
    return cap

def check_route(opener):
    with opener.open('https://openrouter.ai/api/v1/models/typesafe/jev-1.13/endpoints',timeout=25) as r:data=json.load(r)['data']
    routes=data.get('endpoints',[])
    if len(routes)!=1:raise ValueError('route_count')
    r=routes[0];p=r['pricing']
    if r['provider_name']!='TypeSafe' or r['tag']!='typesafe' or r['status']!=0 or SNAPSHOT not in r['name']:raise ValueError('route_changed')
    if float(p['prompt'])>RATE or float(p['completion'])!=0 or float(p.get('request',0))!=0 or r['context_length']>32000:raise ValueError('price_or_context_changed')
    return {'snapshot':SNAPSHOT,'provider':'TypeSafe','input_rate':float(p['prompt']),'output_rate':0,'reservation_usd':RESERVE_NANO/1e9}

def run(a):
    root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
    c=json.loads(a.config.read_text());cap=verify_config(c,a.stage,root)
    sys.path.insert(0,str(root/'researchers/vishesh/notes/experiment-documentation'));import public_plan
    receipt=public_plan.check('phantom-coast',c['run_tldr'])
    if receipt['url']!=c['plan_url'] or receipt['plan_sha256']!=c['plan_sha256']:raise ValueError('public_plan_binding')
    if a.credential_file.stat().st_mode&0o077:raise ValueError('credential_permissions')
    key=a.credential_file.read_text().strip()
    if not key:raise ValueError('credential_absent')
    opener=urllib.request.build_opener(NoRedirect());route=check_route(opener)
    a.out.mkdir(parents=True,exist_ok=False)
    save(a.out/'config.json',c);save(a.out/'public-plan.json',receipt);save(a.out/'route.json',route)
    rows=schedule(a.stage);save(a.out/'manifest.json',{'stage':a.stage,'assignments':rows,'sha256':digest(rows)})
    records=[dict(id=x['id'],seed=x['seed'],kind=x['kind'],step=x['step'],actor=x['actor'],history=x.get('history'),communication=x.get('communication'),state=x.get('state'),status='not-started') for x in rows]
    save(a.out/'records.json',records)
    budget=Budget(a.ledger,round(cap*1e9));before=budget.summary();completed={};start=time.monotonic();failures=0;stop_reason=None
    os.environ.update(SWARM_SOURCE='vishesh/codex-phantom-coast',SWARM_HOST=c['host'])
    import swarm_report as sr
    hub=sr.Run(c['run_id'],'phantom-coast',{'stage':a.stage,'design':'PC-1L','source':c['source_commit']})
    try:
        if quiet(sr.report,'start','phantom-coast',c['run_id'],params=hub.params,message=c['run_tldr'],strict=True) is not True:raise ValueError('hub_start_unacknowledged')
    except Exception:
        budget.close();raise
    try:
        for index,(item,row) in enumerate(zip(rows,records)):
            if time.monotonic()-start>3600 or failures>=5:stop_reason='time_or_consecutive_failures';break
            w=world(item['seed'],stage=a.stage);previous=None
            if item['kind']!='clean' and item['step']>0:
                prior=lambda actor:completed.get((item['seed'],item['kind'],item['history'],item['communication'],item['state'],item['step']-1,actor))
                previous=prior(0) if item['kind']=='pooled' else [prior(i) for i in range(3)]
            req=request(request_for_assignment(w,item,previous))
            row.update(request=req,request_sha256=digest(req))
            try:budget.reserve(a.stage+':'+item['id'])
            except Exception:
                stop_reason='budget_or_duplicate_guard';break
            row.update(status='started',started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());save(a.out/'records.json',records)
            t=time.monotonic()
            try:
                wire=urllib.request.Request('https://openrouter.ai/api/alpha/decisions',canonical(req).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
                with opener.open(wire,timeout=45) as r:raw=json.loads(r.read(1_000_000))
                checked=validate(raw,req);budget.finish(a.stage+':'+item['id'],round(checked['usage']['cost']*1e9))
                row.update(status='valid',checked=checked,response_sha256=digest(raw));failures=0
            except Exception as e:
                safe='http_'+str(e.code) if isinstance(e,urllib.error.HTTPError) else type(e).__name__
                row.update(status='timeout' if isinstance(e,TimeoutError) else ('invalid' if isinstance(e,ValueError) else 'failed'),failure_code=safe)
                budget.finish(a.stage+':'+item['id']);failures+=1
            row['elapsed_seconds']=time.monotonic()-t
            if item['kind']!='clean':completed[(item['seed'],item['kind'],item['history'],item['communication'],item['state'],item['step'],item['actor'])]=row.get('checked',{}).get('response')
            save(a.out/'records.json',records)
            current=qualification(records) if a.stage=='Q0' else analyze_history(records)
            error_upper=current['upper'] if a.stage=='Q0' else sum(t['error']['upper'] for wd in current['worlds'] for t in wd['trajectories'] if t['step']==2)/48
            metrics={'error_upper':error_upper,'assigned_maps':len(rows),'valid_maps':sum(r['status']=='valid' for r in records),'cost_usd':budget.summary()['known_cost_usd']}
            quiet(hub.progress,index+1,len(rows),**metrics)
            if (index+1)%6==0:
                from live_render import render
                try:render(records,a.out,a.stage,animate=False);quiet(hub.artifact,str(a.out/'final_frame.png'),'final_frame.png')
                except Exception:save(a.out/'render-status.json',{'available':False,'reason':'render_or_upload_failed'})
        summary=qualification(records) if a.stage=='Q0' else analyze_history(records)
        summary['error_upper']=summary['upper'] if a.stage=='Q0' else sum(t['error']['upper'] for wd in summary['worlds'] for t in wd['trajectories'] if t['step']==2)/48
        summary.update(model=SNAPSHOT,design='PC-1L',source_commit=c['source_commit'],stage=a.stage,stop_reason=stop_reason,budget=budget.summary(),budget_before=before)
        save(a.out/'summary.json',summary)
        try:
            from live_render import render
            render(records,a.out,a.stage)
        except Exception:save(a.out/'render-status.json',{'available':False,'reason':'render_failed'})
        for p in a.out.iterdir():
            if p.suffix in ('.json','.png','.gif'):
                ack=quiet(hub.artifact,str(p),p.name)
                if not isinstance(ack,dict) or ack.get('spooled'):raise ValueError('artifact_upload_unacknowledged')
        quiet(hub.done,message='Exploratory '+a.stage+' execution reconciled; qualification '+str(summary.get('qualification_passed','not evaluated')),valid_maps=summary['valid'],assigned_maps=summary['assigned'],error_upper=summary['error_upper'],cost_usd=budget.summary()['known_cost_usd'])
        print(json.dumps({'stage':a.stage,'assigned':summary['assigned'],'valid':summary['valid'],'qualification_passed':summary.get('qualification_passed'),'stop_reason':stop_reason}))
    except Exception as e:
        save(a.out/'worker-failure.json',{'error_type':type(e).__name__});quiet(hub.fail,message='Worker failed: '+type(e).__name__);raise
    finally:hub._alive.set();budget.close()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--stage',choices=['Q0','S0'],required=True);p.add_argument('--config',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--ledger',type=Path,required=True);p.add_argument('--credential-file',type=Path,required=True)
    try:run(p.parse_args())
    except Exception as e:print(json.dumps({'launch_or_worker_failed':type(e).__name__}));raise SystemExit(1)
