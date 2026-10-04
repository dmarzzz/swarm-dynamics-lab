"""Single-worker exploratory runner. Strict source/public/allocation receipts required."""
import argparse,contextlib,datetime,json,os,subprocess,sys,time,urllib.request,urllib.error
from pathlib import Path
from cases import digest
from jev import request
from live_design import SNAPSHOT,qualification,development,assignments,frozen_requests
from protocol import episode,summarize,ARMS
from policies import ExactReference

def save(path,value):
    tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,indent=2,allow_nan=False));tmp.replace(path)

def quiet(fn,*args,**kwargs):
    # Hub diagnostics may contain private addresses; never send them to a log.
    with open(os.devnull,'w') as sink,contextlib.redirect_stderr(sink),contextlib.redirect_stdout(sink):return fn(*args,**kwargs)

class TransportFailure(RuntimeError):pass

class NativePolicy:
    def __init__(self,out,allowed):self.out=out;self.allowed=allowed;self.cache={};self.calls=[];self.logical_calls=0;self.started=time.monotonic();self.consecutive=0
    def __call__(self,phase,packet):
        req=request(phase,packet);h=digest(req);self.logical_calls+=1
        if h not in self.allowed or req!=self.allowed[h]:raise ValueError('request_not_frozen')
        if h not in self.cache:
            row={'request_sha256':h,'request':req,'status':'started'};self.calls.append(row);save(self.out/'calls.json',self.calls)
            before=time.monotonic()
            try:
                if time.monotonic()-self.started>2700 or self.consecutive>=5:raise TransportFailure('attempt_stopped')
                wire=urllib.request.Request('http://127.0.0.1:18449/decision',json.dumps(req).encode(),{'Content-Type':'application/json'})
                try:
                    with urllib.request.urlopen(wire,timeout=45) as r:data=json.load(r)
                except urllib.error.HTTPError as e:
                    data=json.loads(e.read(2000));raise TransportFailure(data.get('error','relay_error'))
                checked=data['checked']
                if checked['request_sha256']!=h or checked['served_model']!=SNAPSHOT or checked['action'] not in req['questions']['action']['criteria']:raise TransportFailure('checked_contract')
                row.update(status='completed',checked=checked);self.consecutive=0
            except Exception as e:
                safe=str(e) if isinstance(e,TransportFailure) and str(e) in ('attempt_stopped','relay_error','checked_contract','duplicate_request','ValueError','TimeoutError','URLError','http_400','http_401','http_402','http_403','http_404','http_408','http_429','http_500','http_502','http_503','http_504') else type(e).__name__
                row.update(status='failed',error=safe);self.consecutive+=1
            row['elapsed_seconds']=time.monotonic()-before;self.cache[h]=row;save(self.out/'calls.json',self.calls)
        row=self.cache[h]
        if row['status']!='completed':raise TransportFailure('saved_failure')
        return row['checked']['action']

def verify_config(config,stage):
    if config['stage']!=stage or config.get('budget_approved') is not True or config['host']!='sim-right-dissenter':raise ValueError('launch_config')
    if datetime.datetime.fromisoformat(config['claim_until'].replace('Z','+00:00'))<=datetime.datetime.now(datetime.timezone.utc):raise ValueError('claim_expired')
    head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    if head!=config['source_commit']:raise ValueError('source_commit_mismatch')
    root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
    import hashlib
    for name,h in config['file_hashes'].items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=h:raise ValueError('source_hash_mismatch')
    if digest(assignments(stage))!=config['assignment_sha256']:raise ValueError('assignment_mismatch')
    sys.path.insert(0,str(root/'researchers/vishesh/notes/experiment-documentation'))
    import public_plan
    receipt=public_plan.check('right-dissenter',config['run_tldr'])
    if receipt['url']!=config['plan_url'] or receipt['plan_sha256']!=config['plan_sha256']:raise ValueError('plan_binding_mismatch')
    if stage=='S1':
        q=json.loads(Path(config['qualification_result']).read_text())
        if q.get('qualification_passed') is not True or q['served_model']!=SNAPSHOT:raise ValueError('qualification_required')
    return receipt

def main(a):
    config=json.loads(a.config.read_text());receipt=verify_config(config,a.stage)
    a.out.mkdir(parents=True,exist_ok=False)
    save(a.out/'public-plan-receipt.json',receipt);save(a.out/'configuration.json',config)
    assigned=assignments(a.stage);total=sum(x['opportunities'] for x in assigned)
    manifest={'stage':a.stage,'origin':'native-jev','scripted_initial_votes':a.stage=='S1','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assignments':assigned,'assignment_sha256':digest(assigned),'total_opportunities':total}
    for row in assigned:row['status']='planned'
    save(a.out/'manifest.json',manifest);rows=[];save(a.out/'records.json',rows)
    policy=NativePolicy(a.out,frozen_requests(a.stage));exact=ExactReference()
    os.environ.update(SWARM_SOURCE='vishesh/codex-decision-models',SWARM_HOST='sim-right-dissenter')
    import swarm_report as sr
    # Fixed strings only; reporter errors never printed with private endpoints.
    run=quiet(sr.start,'right-dissenter',run=config['run_id'],params={'stage':a.stage,'design':'RD-2','source':config['source_commit'],'plan_url':config['plan_url'],'scripted_votes':a.stage=='S1'},message=config['run_tldr'])
    quiet(run.__enter__)
    try:
        cases={x['case_id']:x for x in (qualification() if a.stage=='Q0' else development())}
        for item in assigned:
            if policy.consecutive>=5 or time.monotonic()-policy.started>2700:break
            item['status']='started';save(a.out/'manifest.json',manifest);c=cases[item['case_id']]
            if a.stage=='Q0':
                try:action=policy('private',c['packet']);status='completed'
                except Exception:action='DEFER';status='failed'
                result={'case_id':c['case_id'],'scenario':c['scenario'],'arm':'private','final':action,'status':status,'expected':c['expected'],'correct':action==c['expected'] and status=='completed'}
                rows.append(result)
            else:
                results=episode(c,item['arm'],exact if item['arm']=='exact-reference' else policy,random_check=item['random_check'] if item['arm']=='matched-random' else None)
                for row in results:row['condition']=c['condition'];row['seed']=c['seed']
                rows.extend(results)
            item['status']='completed';save(a.out/'records.json',rows);save(a.out/'manifest.json',manifest)
            correct=sum(x.get('correct',x.get('correct_completion',False)) for x in rows)
            quiet(run.progress,len(rows),total,correct_all_assigned=correct/total,terminal=len(rows))
        if a.stage=='Q0':
            per={s:{'correct':sum(x['correct'] for x in rows if x['scenario']==s),'valid':sum(x['status']=='completed' for x in rows if x['scenario']==s),'assigned':6} for s in ('bridge','build','alarm')}
            correct=sum(x['correct'] for x in rows);valid=sum(x['status']=='completed' for x in rows)
            report={'assigned':18,'terminal':len(rows),'correct':correct,'valid':valid,'by_scenario':per,'qualification_passed':valid>=17 and correct>=16 and all(v['correct']>=5 for v in per.values())}
        else:
            report={'assigned':total,'terminal':len(rows),'by_arm':{arm:summarize([x for x in rows if x['arm']==arm]) for arm in ARMS}}
            for arm,values in report['by_arm'].items():
                values['observed_decisions']=values['assigned_decisions'];values['missing']=60-values['observed_decisions'];values['assigned_decisions']=60;values['correct_on_time_rate']=values['correct_on_time']/60
        report.update(stage=a.stage,served_model=SNAPSHOT,unique_requests=len(policy.calls),completed_calls=sum(x['status']=='completed' for x in policy.calls),logical_calls=policy.logical_calls,cost_usd=sum(x.get('checked',{}).get('cost_usd',0) for x in policy.calls),input_tokens=sum(x.get('checked',{}).get('input_tokens',0) for x in policy.calls),elapsed_seconds=time.monotonic()-policy.started,missing=total-len(rows))
        save(a.out/'summary.json',report)
        from live_render import render
        render(a.out)
        for p in a.out.iterdir():
            if p.is_file() and p.suffix in ('.json','.png','.gif'):quiet(run.artifact,str(p),p.name)
        finish=run.fail if report['missing'] else run.done
        message=('Incomplete exploratory ' if report['missing'] else 'Completed exploratory ')+a.stage+'; qualification '+str(report.get('qualification_passed','not applicable'))
        quiet(finish,message=message,correct_all_assigned=(report.get('correct',sum(x.get('correct_completion',False) for x in rows)))/total,terminal=len(rows),cost_usd=report['cost_usd'])
        print(json.dumps(report),flush=True)
    except Exception as e:
        quiet(run.fail,message='Study execution failed: '+type(e).__name__);raise

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--stage',choices=['Q0','S1'],required=True);p.add_argument('--config',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    try:main(p.parse_args())
    except Exception as e:print(json.dumps({'worker_failed':type(e).__name__}));raise SystemExit(1)
