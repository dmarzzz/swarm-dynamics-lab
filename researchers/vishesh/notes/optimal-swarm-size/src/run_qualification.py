"""Fail-closed Q-A runner. No credentials are inspected until after launch checks."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import threading
import urllib.request
from budget import Budget
from engine import execute
from provider import Provider
from replay import render
from reporting import Reporter
from tasks import generate,qualification_manifest,evaluate,operational,digest
from failures import SafeFailure,safe_code
from response_contract import VERSION,LEGACY

REQUIRED=('expected_served_model','expected_served_provider','stage_cap_microdollars',
          'episode_cap_microdollars','spending_authorization','independent_review_commit',
          'exclusive_machine_claim','public_plan_receipt','authorized_total_microdollars')


def launch_errors(config):
    errors=[f'missing:{k}' for k in REQUIRED if not config.get(k)]
    if config.get('response_contract') not in (VERSION,LEGACY):errors.append('response_contract_unconfigured')
    if config.get('status')!='ready':errors.append('config_not_ready')
    for k in ('stage_cap_microdollars','episode_cap_microdollars'):
        v=config.get(k)
        if v is not None and (type(v) is not int or v<=0):errors.append('invalid:'+k)
    authorization=json.loads((Path(__file__).parent.parent/'SPENDING-AUTHORIZATION.json').read_text())
    if config.get('spending_authorization')!=authorization['authorization_id'] or config.get('authorized_total_microdollars')!=authorization['authorized_total_microdollars']:
        errors.append('authorization_record_mismatch')
    allowed=authorization['authorized_total_microdollars']
    stage=config.get('stage_cap_microdollars')
    episode=config.get('episode_cap_microdollars')
    if type(allowed) is not int or allowed<=0: errors.append('invalid:authorized_total_microdollars')
    elif type(stage) is int and stage>allowed: errors.append('stage_exceeds_authorization')
    if type(stage) is int and type(episode) is int and episode>stage: errors.append('episode_exceeds_stage')
    return errors


def preflight(config,source_root):
    errors=launch_errors(config)
    if errors:raise ValueError(';'.join(errors))
    if subprocess.check_output(['git','status','--porcelain'],cwd=source_root,text=True).strip():
        raise ValueError('source_not_clean')
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=source_root,text=True).strip()
    receipt=json.loads(Path(config['public_plan_receipt']).read_text())
    if receipt.get('experiment')!=config['experiment_id'] or receipt.get('commit')!=commit:
        raise ValueError('public_registration_not_current_source')
    url=receipt['url']
    if not re.fullmatch(r'https://github.com/dmarzzz/swarm-lab/blob/[0-9a-f]{40}/.+\.md',url):
        raise ValueError('immutable_plan_required')
    raw=url.replace('https://github.com/','https://raw.githubusercontent.com/').replace('/blob/','/')
    with urllib.request.urlopen(raw,timeout=20) as r:markdown=r.read().decode()
    if hashlib.sha256(markdown.encode()).hexdigest()!=receipt['plan_sha256']:
        raise ValueError('public_plan_mismatch')
    if not receipt.get('registered_tldr','').startswith('TLDR: '):raise ValueError('registered_tldr_missing')
    # Claim/review references must have been independently verified before config promotion.
    # This file does not manufacture reviews or allocate a server.
    return commit


def assignments_for(config):
    if config.get('stage')=='canary':
        if config.get('attempt_id')!='q-a3-canary' or config.get('attempt_cap_microdollars')!=5000000 or config.get('episode_cap_microdollars')!=1250000 or config.get('response_contract')!=VERSION:raise ValueError('invalid_canary_config')
        rows=[]
        for family,structure in [('evidence','parallel'),('repository','chain'),('evidence','chain'),('repository','parallel')]:
            task=generate(family,structure,0,width=2)
            identity=config['attempt_id']+'/'+task.public['id']+'/width2/n1'
            rows.append(dict(id=identity,parent_id=task.public['id'],root_id=task.public['id']+'/width2',root=0,n=1,stage='canary',family=family,structure=structure,width=2,attempt_id=config['attempt_id'],public_task_sha256=digest(task.public)))
        return rows
    if config.get('stage')=='full-width':
        if config.get('attempt_id')!='q-a4' or config.get('attempt_cap_microdollars')!=8000000 or config.get('episode_cap_microdollars')!=2000000 or config.get('response_contract')!=VERSION:raise ValueError('invalid_full_width_config')
        rows=[]
        for root in range(4):
            for family,structure in [('evidence','parallel'),('repository','chain'),('evidence','chain'),('repository','parallel')]:
                task=generate(family,structure,root,width=16)
                rows.append(dict(id='q-a4/'+task.public['id']+'/width16/n1',parent_id=task.public['id'],root_id=task.public['id']+'/width16',root=root,n=1,stage='full-width',family=family,structure=structure,width=16,attempt_id='q-a4',public_task_sha256=digest(task.public)))
        return rows
    rows=[row for row in qualification_manifest() if row['stage']=='Q-A']
    attempt=config.get('attempt_id')
    if attempt is not None:
        if not isinstance(attempt,str) or not re.fullmatch(r'q-a[2-9][0-9]*',attempt):
            raise ValueError('invalid_attempt_id')
        rows=[dict(row,id=attempt+'/'+row['id'],parent_id=row['id'],attempt_id=attempt) for row in rows]
    return rows


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--budget-ledger',type=Path)
    args=parser.parse_args();config=json.loads(args.config.read_text())
    errors=launch_errors(config)
    if args.check:
        print(json.dumps({'ready':not errors,'blockers':errors},indent=2));return 0 if not errors else 2
    if not args.output or not args.budget_ledger:raise ValueError('output_and_shared_ledger_required')
    source_root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
    commit=preflight(config,source_root)
    assignments=assignments_for(config)
    args.output.mkdir(parents=True,exist_ok=False)
    (args.output/'assigned.json').write_text(json.dumps(assignments,indent=2)+'\n')
    return run_batch(config,commit,args.output,args.budget_ledger,assignments)


def save_json(path,data):
    pending=path.with_suffix(path.suffix+'.tmp')
    with pending.open('w') as handle:
        json.dump(data,handle,indent=2);handle.flush();os.fsync(handle.fileno())
    pending.replace(path)


def run_batch(config,commit,output,ledger,assignments):
    states=[];bank=None;stop_reason=None;consecutive_malformed=0
    for row in assignments:
        target=output/hashlib.sha256(row['id'].encode()).hexdigest()[:16]
        target.mkdir(exist_ok=False)
        tldr=f"TLDR: {row.get('attempt_id','Q-A')} {row['family']} {row['structure']} root {row['root']}, width={row.get('width',16)}, N=1 under screening caps; single-agent calibration reference for later matched-N comparisons. Metrics: verified on-time success, quality, cost and latency. Exploratory synthetic tasks; not a size-effect result."
        save_json(target/'assignment.json',row|{'commit':commit,'run_tldr':tldr,'status':'assigned'})
        states.append({'episode':row['id'],'directory':target.name,'execution':'not_started','reason':None,'exposure_microdollars':0,'publication':'not_started'})
    try:
        bank=Budget(ledger,config['stage_cap_microdollars'],config['attempt_id'] if config.get('stage') in ('canary','full-width') else None,config.get('attempt_cap_microdollars') if config.get('stage') in ('canary','full-width') else None)
        for row,state in zip(assignments,states):
            target=output/state['directory'];lock=threading.Lock();completed=0
            def journal(event):
                with lock:
                    with (target/'trace.jsonl').open('a') as handle:
                        handle.write(json.dumps(event)+'\n');handle.flush();os.fsync(handle.fileno())
            try:
                state['execution']='admission_pending';save_json(target/'state.json',state)
                assignment=json.loads((target/'assignment.json').read_text())
                reporter=Reporter(config['experiment_id'],row,assignment['run_tldr'])
                state['execution']='started';save_json(target/'state.json',state)
                progress_pool=concurrent.futures.ThreadPoolExecutor(max_workers=1)
                pending_progress=None
                def send_progress(count):
                    try:
                        report=reporter.progress(count)
                        if not isinstance(report,dict) or report.get('code'):
                            journal({'kind':'reporting_failure','operation':'progress','code':'reporting_failed'})
                    except Exception:
                        journal({'kind':'reporting_failure','operation':'progress','code':'reporting_failed'})
                def measured_event(event):
                    nonlocal completed,pending_progress
                    journal(event)
                    if event['kind']=='work_complete':
                        completed+=1
                        # At most one update in flight; reporting never blocks actor work.
                        if pending_progress is None or pending_progress.done():
                            pending_progress=progress_pool.submit(send_progress,completed)
                task=generate(row['family'],row['structure'],row['root'],width=row.get('width',16))
                if row.get('public_task_sha256') and digest(task.public)!=row['public_task_sha256']:raise ValueError('task_hash_mismatch')
                runtime=Provider(config,bank,row['id'],journal,task.public)
                try:
                    record=execute(task.public,1,config['slots'],config['screening_deadline_s'],config['integration_reserve_s'],runtime,measured_event,strict_contract=config.get('stage') in ('canary','full-width'))
                finally:
                    progress_pool.shutdown(wait=True,cancel_futures=True)
                result=evaluate(task,record['artifact'] or '{}');exposure=bank.exposure(row['id'])
                record.update(assignment=row,commit=commit,evaluation=result,exposure_microdollars=exposure,
                              operational_success=operational(result,record['elapsed_s'],exposure,config['screening_deadline_s'],config['episode_cap_microdollars']))
                save_json(target/'outcome.json',record)
                state.update(execution='terminal',reason=record['failure'],exposure_microdollars=exposure,publication='pending')
                save_json(target/'state.json',state)
                render(target/'trace.jsonl',target/'replay.html')
                receipt=reporter.finish(target,record)
                acknowledged=isinstance(receipt,dict) and receipt.get('complete') is True
                state['publication']='acknowledged' if acknowledged else 'incomplete'
                save_json(target/'state.json',state)
                print(json.dumps({'episode':row['id'],'terminal':True,'success':record['operational_success'],'publication':state['publication']}),flush=True)
                if not acknowledged:stop_reason='publication_incomplete';break
                if record.get('fatal'):stop_reason=record['failure'];break
                if config.get('stage') in ('canary','full-width') and (record['failure'] or record['work_failures']):
                    stop_reason=record['failure'] or 'work_contract_failed';break
                consecutive_malformed=consecutive_malformed+1 if record['failure']=='malformed_output' else 0
                if config.get('attempt_id') and consecutive_malformed>=2:
                    stop_reason='repeated_malformed_output';break
                if not bank.healthy():stop_reason='budget_overrun';break
            except Exception as exc:
                stop_reason=safe_code(exc)
                if state['execution']=='admission_pending':state['execution']='admission_failed'
                elif state['execution']=='started':state['execution']='interrupted'
                elif state['execution']=='terminal':state['publication']='incomplete'
                state['reason']=stop_reason
                save_json(target/'state.json',state)
                break
    except KeyboardInterrupt:
        stop_reason='operator_interrupted'
    except Exception as exc:
        stop_reason=safe_code(exc)
    finally:
        for state in states:
            if state['execution'] in ('started','admission_pending'):
                state.update(execution='interrupted',reason=stop_reason or 'execution_failed')
            if state['execution']=='not_started':state['reason']=stop_reason
            if bank is not None:
                try:state['exposure_microdollars']=bank.exposure(state['episode'])
                except Exception:state['exposure_microdollars']=None
            target=output/state['directory']
            state['outcome_present']=(target/'outcome.json').exists()
            save_json(target/'state.json',state)
        terminal=sum(s['execution']=='terminal' for s in states)
        reconciliation={'assigned':len(states),'terminal':terminal,'execution_complete':terminal==len(states),
                        'publication_complete':all(s['publication']=='acknowledged' for s in states),
                        'stop_reason':stop_reason,'episodes':states,
                        'executed_publication_complete':terminal>0 and all(s['publication']=='acknowledged' for s in states if s['execution']=='terminal'),
                        'unstarted':sum(s['execution']=='not_started' for s in states)}
        save_json(output/'reconciliation.json',reconciliation)
    print(json.dumps({'stage':'Q-A','terminal':terminal,'assigned':len(states),'stop_reason':stop_reason}),flush=True)
    return 0 if stop_reason is None and terminal==len(states) else 2

if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:
        # Avoid displaying provider bodies, URLs containing credentials or process environments.
        print('Launch stopped: '+(str(exc) if isinstance(exc,ValueError) else type(exc).__name__))
        raise SystemExit(2)
