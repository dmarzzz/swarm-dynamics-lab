"""RD-4 bounded executor: all-assigned outcomes and fail-closed native admission."""
import argparse,collections,datetime,hashlib,json,os,platform,subprocess,sys,time
from pathlib import Path
from cases import digest
from live_worker import save,quiet,NativePolicy
from live_design import SNAPSHOT
from protocol import summarize
from rd4_design import ARMS,DOMAINS,assignments,qualification,trajectories,execute,wire,frozen_requests

EXPERIMENT='right-dissenter-rd4'

def verify(config,stage):
    if config.get('stage')!=stage or config.get('budget_approved') is not True:raise ValueError('launch_config')
    if config.get('allocation_verified') is not True or platform.node()!=config['host'] or config['host']!='sim-shadow' or len(config.get('allocation_receipt_sha256',''))!=64:raise ValueError('allocation_identity_mismatch')
    if datetime.datetime.fromisoformat(config['claim_until'].replace('Z','+00:00'))<=datetime.datetime.now(datetime.timezone.utc):raise ValueError('claim_expired')
    if subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()!=config['source_commit']:raise ValueError('source_commit_mismatch')
    root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
    for file,h in config['file_hashes'].items():
        if hashlib.sha256((root/file).read_bytes()).hexdigest()!=h:raise ValueError('source_hash_mismatch')
    if config['assignment_sha256']!=digest(assignments(stage)):raise ValueError('assignment_mismatch')
    sys.path.insert(0,str(root/'researchers/vishesh/notes/experiment-documentation'))
    import public_plan
    receipt=public_plan.check(EXPERIMENT,config['run_tldr'])
    if receipt['url']!=config['plan_url'] or receipt['plan_sha256']!=config['plan_sha256']:raise ValueError('plan_binding_mismatch')
    if stage=='S4':
        path=Path(config['qualification_result']);q=json.loads(path.read_text())
        if hashlib.sha256(path.read_bytes()).hexdigest()!=config['qualification_sha256'] or q.get('qualification_passed') is not True or q['served_model']!=SNAPSHOT or q['instrument_sha256']!=config['instrument_sha256']:raise ValueError('qualification_binding')
    return receipt

def analyze(stage,rows,calls,logical,config,elapsed):
    assigned=24 if stage=='Q4' else 576
    report={'stage':stage,'assigned':assigned,'terminal':len(rows),'missing':assigned-len(rows),'unique_requests':len(calls),'valid_requests':sum(x['status']=='completed' for x in calls),'errors':dict(collections.Counter(x.get('error') for x in calls if x['status']!='completed')),'logical_calls':logical,'cost_usd':sum(x.get('checked',{}).get('cost_usd',0) for x in calls),'input_tokens':sum(x.get('checked',{}).get('input_tokens',0) for x in calls),'elapsed_seconds':elapsed,'served_model':SNAPSHOT,'instrument_sha256':config['instrument_sha256']}
    if stage=='Q4':
        per={d:{'assigned':6,'correct':sum(r['correct'] for r in rows if r['scenario']==d and r['arm']=='clean'),'valid':sum(r['status']=='completed' for r in rows if r['scenario']==d and r['arm']=='clean')} for d in DOMAINS}
        report.update(by_scenario=per,uncertainty_correct=sum(r['correct'] for r in rows if r['arm']=='uncertainty'),correct=sum(r['correct'] for r in rows))
        report['qualification_passed']=sum(x['valid'] for x in per.values())>=17 and sum(x['correct'] for x in per.values())>=16 and all(x['correct']>=5 for x in per.values()) and report['uncertainty_correct']==6 and len(rows)==24
    else:
        report['by_arm']={arm:summarize([r for r in rows if r['arm']==arm]) for arm in ARMS}
        for arm,stats in report['by_arm'].items():
            own=[r for r in rows if r['arm']==arm];stats.update(counterfactual_settled_cost=sum(r['counterfactual_settled_cost'] for r in own),logical_calls=sum(r['model_calls'] for r in own),repeat_correct=sum(r['correct_completion'] for r in own if r['epoch'] in (1,2)),repeat_checks=sum(r['checks'] for r in own if r['epoch'] in (1,2)),recovery_correct=sum(r['correct_completion'] for r in own if r['epoch']==3 and r['direction']=='recovery'),deterioration_correct=sum(r['correct_completion'] for r in own if r['epoch']==3 and r['direction']=='deterioration'))
        indexed={(r['case_id'],r['epoch'],r['arm']):r for r in rows}
        report['paired']={}
        for a,b in [('symmetric-gate','original-gate'),('symmetric-gate','always-check'),('original-gate','always-check')]:
            pairs=[(indexed[(c['case_id'],epoch,a)],indexed[(c['case_id'],epoch,b)]) for c in trajectories() for epoch in range(4) if (c['case_id'],epoch,a) in indexed and (c['case_id'],epoch,b) in indexed]
            report['paired'][a+'_vs_'+b]={'pairs':len(pairs),'improved':sum(x['correct_completion'] and not y['correct_completion'] for x,y in pairs),'worsened':sum(y['correct_completion'] and not x['correct_completion'] for x,y in pairs)}
        report['losses']={arm:{f'harm{harm}_check{cost}':v['wrong_proceed']*harm+v['unnecessary_hold']+v['unresolved']*2+v['checks']*cost for harm in (1,5,10) for cost in (0,.1,1)} for arm,v in report['by_arm'].items()}
        report['failures']=[{k:r[k] for k in ('case_id','scenario','arm','epoch','final','reason','condition','direction')} for r in rows if not r['correct_completion']]
    return report

def main(a):
    config=json.loads(a.config.read_text());receipt=verify(config,a.stage);a.out.mkdir(parents=True,exist_ok=False)
    save(a.out/'configuration.json',config);save(a.out/'public-plan-receipt.json',receipt)
    assigned=assignments(a.stage)
    for x in assigned:x['status']='planned'
    manifest={'stage':a.stage,'assignments':assigned,'total_opportunities':24 if a.stage=='Q4' else 576,'scripted_votes':a.stage=='S4','origin':'native-jev'}
    save(a.out/'manifest.json',manifest);rows=[];save(a.out/'records.json',rows)
    native=NativePolicy(a.out,frozen_requests(a.stage),request_builder=wire)
    os.environ.update(SWARM_SOURCE='vishesh/codex-decision-models',SWARM_HOST=config['host'])
    import swarm_report as sr
    run=quiet(sr.start,EXPERIMENT,run=config['run_id'],params={'stage':a.stage,'design':'RD-4','source':config['source_commit'],'plan_url':config['plan_url'],'scripted_votes':a.stage=='S4'},message=config['run_tldr']);quiet(run.__enter__)
    quiet(sr.report,'log',experiment=EXPERIMENT,run=config['run_id'],url=config['plan_url'],message='Prospective immutable RD-4 plan.')
    cases={c['case_id']:c for c in (qualification(native=True) if a.stage=='Q4' else trajectories())}
    for item in assigned:
        if native.consecutive>=5 or time.monotonic()-native.started>2700:break
        item['status']='started';save(a.out/'manifest.json',manifest);c=cases[item['case_id']];before=native.logical_calls
        if a.stage=='Q4':
            try:action=native('private',c['packet']);status='completed'
            except Exception:action='DEFER';status='failed'
            rows.append({k:c[k] for k in ('case_id','scenario','arm','expected')}|dict(final=action,status=status,correct=action==c['expected'] and status=='completed'))
        else:
            arm_rows=execute(c,item['arm'],native)
            rows.extend(arm_rows)
        item['status']='terminal';save(a.out/'manifest.json',manifest);save(a.out/'records.json',rows)
        quiet(run.progress,len(rows),manifest['total_opportunities'],terminal=len(rows))
    report=analyze(a.stage,rows,native.calls,native.logical_calls,config,time.monotonic()-native.started)
    save(a.out/'summary.json',report)
    from rd4_render import render
    render(a.out)
    for f in a.out.iterdir():
        if f.suffix in ('.json','.png','.gif'):quiet(run.artifact,str(f),f.name)
    quiet(run.fail if report['missing'] else run.done,message='RD-4 '+a.stage+' complete; qualification '+str(report.get('qualification_passed','not applicable'))+'. All saved failures retained.',terminal=len(rows),cost_usd=report['cost_usd'])
    print(json.dumps({k:v for k,v in report.items() if k not in ('failures','losses')}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--stage',choices=['Q4','S4'],required=True);p.add_argument('--config',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    try:main(p.parse_args())
    except Exception as e:print(json.dumps({'worker_failed':type(e).__name__}));raise SystemExit(1)
