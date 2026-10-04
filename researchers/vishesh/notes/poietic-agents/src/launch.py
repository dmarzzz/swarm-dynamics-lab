"""One native entry point. No paid smoke/test bypass; S1/S2 intentionally unadmitted."""
import argparse
import contextlib
import json
import math
import os
import resource
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from admission import BASE, inventory, verify, verify_public
from budget import Budget
from common import append, canonical, digest, save
from native import request, response, reserve_nano, verify_catalog
from qualification import ROLES, assignments, make_case, probe, apply, analyze


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): raise ValueError('redirect_refused')


def quiet(fn,*args,**kwargs):
    with open(os.devnull,'w') as sink,contextlib.redirect_stdout(sink),contextlib.redirect_stderr(sink):
        return fn(*args,**kwargs)


def read_json(opener,url):
    with opener.open(url,timeout=30) as stream:
        return json.loads(stream.read(1000000))


def source_check(config):
    repo=BASE.parents[3]
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
    if head!=config['source_commit']: raise ValueError('deployed_commit')


def run(config_path,out):
    config=json.loads(config_path.read_text())
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    verify(config,actual_host=socket.gethostname().split('.')[0])
    source_check(config)
    # This file is imported by its checked, established repository location, not an arbitrary plugin.
    sys.path.insert(0,str(BASE.parent/'experiment-documentation'))
    import public_plan
    plan_receipt=verify_public(config,public_plan.check)
    models=json.loads((BASE/'models.json').read_text())['models']
    opener=urllib.request.build_opener(NoRedirect())
    routes={role:verify_catalog(read_json(opener,c['catalog_url']),c) for role,c in models.items()}
    verify(config,actual_host=socket.gethostname().split('.')[0])
    # The credential must be injected by the approved allocation-specific launcher; never an env fallback.
    key=os.environ.pop('POIETIC_OPENROUTER_KEY','')
    if not key or '\n' in key: raise ValueError('credential_unavailable')
    out.mkdir(parents=True,exist_ok=False)
    save(out/'admission.json',config);save(out/'public-plan.json',plan_receipt);save(out/'route-check.json',routes)
    save(out/'assignments.json',assignments())
    # Study-wide path on one dedicated host; one admission lock prevents independent worker ledgers.
    authority_dir=Path('/srv/swarm/poietic-agents-authority')
    authority_dir.mkdir(parents=True,exist_ok=True)
    import fcntl
    lock=(authority_dir/'worker.lock').open('a')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    auth=config['authorization']
    budget=Budget(authority_dir/'budget.sqlite',digest(auth),config['allocation']['host'],5_000_000_000,288,auth['deadline'])
    os.environ.update(SWARM_SOURCE='vishesh/codex-heterogeneous',SWARM_HOST=config['allocation']['host'])
    import swarm_report as sr
    runs={}; records=[]; stop=None; start=time.monotonic()
    try:
        # Three condition-specific run descriptions, one shared physical budget and assignment authority.
        for role in ROLES:
            run_id=f'poietic-S0-01-{role}'
            params=dict(stage='S0',contract=role,source_commit=config['source_commit'],assignment_sha256=digest(assignments()))
            if quiet(sr.report,'start','poietic-agents',run_id,params=params,message=config['condition_tldrs'][role],strict=True) is not True:
                raise ValueError('hub_start_unacknowledged')
            runs[role]=sr.Run(run_id,'poietic-agents',params)
        for role in ROLES:
            contract=models[role]
            for case in range(12):
                state=make_case(case)
                state['engine'].actors['agent-0'].model=role
                for step in range(4):
                    call_id=f'S0-01:{role}:{case}:{step}'
                    row=dict(id=call_id,role=role,case=case,step=step,status='not_started',started=False)
                    if stop or time.time()>=auth['deadline']-45:
                        stop=stop or 'stage_deadline';records.append(row);continue
                    packet=probe(state,step,role)
                    req=request(contract,packet['sections'],packet['choices'])
                    row.update(request_sha256=digest(req),request=req,context_receipt=packet['context_receipt'])
                    for attempt in range(2):
                        physical_id=call_id+f':physical-{attempt}'
                        try:
                            budget.reserve(physical_id,digest(req),reserve_nano(contract))
                        except ValueError:
                            stop='budget_guard'; break
                        row.update(started=True,status='failed')
                        append(out/'call-starts.jsonl',dict(id=physical_id,logical_id=call_id,request_sha256=digest(req),utc=time.time()))
                        suffix='/api/alpha/decisions' if contract['kind']=='decision' else '/api/v1/chat/completions'
                        wire=urllib.request.Request('https://openrouter.ai'+suffix,canonical(req).encode(),
                               {'Authorization':'Bearer '+key,'Content-Type':'application/json'})
                        began=time.monotonic()
                        try:
                            with opener.open(wire,timeout=45) as stream:
                                raw=json.loads(stream.read(1000000))
                            # Save only public response fields; no headers, endpoint URLs or request authorization.
                            row['raw_response']={k:raw[k] for k in ('id','model','provider','choices','answers','usage') if k in raw}
                            checked=response(raw,contract,packet['choices'])
                            actual=math.ceil(checked['usage']['cost_usd']*1e9)
                            budget.settle(physical_id,actual)
                            row.update(checked=checked,**apply(state,step,checked['action'],packet['expected']))
                            row['status']='valid' if row['schema_valid'] else 'invalid'
                        except urllib.error.HTTPError as exc:
                            budget.settle(physical_id)
                            row['failure_code']='http_'+str(exc.code)
                            # 429 is a rejected dispatch. Ambiguous timeout/5xx is never retried.
                            if exc.code==429 and attempt==0:
                                append(out/'transport.jsonl',dict(id=physical_id,status='rejected_429',elapsed_s=time.monotonic()-began))
                                continue
                        except Exception as exc:
                            # Settlement may already be known if only local action execution failed.
                            try: budget.settle(physical_id)
                            except ValueError: pass
                            safe=str(exc) if isinstance(exc,ValueError) and str(exc).replace('_','').isalnum() else type(exc).__name__
                            row.update(status='invalid' if isinstance(exc,(ValueError,KeyError,TypeError)) else 'failed',failure_code=safe)
                        row['elapsed_s']=time.monotonic()-began
                        break
                    records.append(row);append(out/'responses.jsonl',row)
                    current=analyze(records)
                    quiet(runs[role].progress,4*case+step+1,48,correct=current['contracts'][role]['correct'],
                          valid=current['contracts'][role]['schema_valid'],cost_usd=budget.summary()['charged_upper_usd'])
                    if step==3:
                        from render import qualification_png
                        frame=out/f'frame-{role}-{case:02d}.png'
                        qualification_png(current,frame)
                        quiet(runs[role].artifact,str(frame),'live.png')
                    if row.get('protected_access_violation') or row.get('failure_code') in ('actual_route_mismatch','billing_exceeds_reserve'):
                        stop='integrity_guard'
        # Every assigned outcome, including unstarted ones, is present in the durable terminal record.
        save(out/'records.json',records)
        summary=analyze(records)
        summary.update(budget=budget.summary(),elapsed_s=time.monotonic()-start,stop_reason=stop,
                       source_commit=config['source_commit'],file_hashes=config['file_hashes'],model_config_sha256=digest(models),
                       infrastructure_usd=(time.monotonic()-start)/3600*config['allocation']['allocated_usd_per_hour'])
        save(out/'summary.json',summary)
        from render import qualification_frame, qualification_png
        qualification_frame(summary,out/'final_frame.svg')
        qualification_png(summary,out/'final_frame.png')
        reporting=[]
        for role,run in runs.items():
            for name in ('summary.json','records.json','assignments.json','final_frame.png'):
                ack=quiet(run.artifact,str(out/name),name)
                reporting.append(dict(contract=role,name=name,acknowledged=isinstance(ack,dict) and not ack.get('spooled')))
            method=run.done if summary['contracts'][role]['passed'] else run.fail
            quiet(method,message='S0 qualification '+('passed' if summary['contracts'][role]['passed'] else 'failed')+'; no swarm efficacy result',correct=summary['contracts'][role]['correct'])
        save(out/'post-mortem.json',dict(disposition='prepare-S1' if summary['qualification_passed'] else 'diagnose-with-fresh-development',
             execution='reconciled',qualification=summary['qualification_passed'],scientific_conclusion='none',
             process_compliance='admitted-S0-only',reporting=reporting,
             next_action='Owner reviews all retained failures, usage and interface controls before any escalation'))
        print(canonical({k:summary[k] for k in ('assigned','started','terminal','qualification_passed','stop_reason')}))
    except Exception as exc:
        have={r['id'] for r in records}
        records.extend(dict(a,status='not_started',started=False) for a in assignments() if a['id'] not in have)
        save(out/'records.json',records)
        save(out/'failure.json',dict(error_type=type(exc).__name__,budget=budget.summary(),records_retained=len(records)))
        save(out/'post-mortem.json',dict(disposition='blocked-repair',error_type=type(exc).__name__,
             reconciliation=analyze(records),budget=budget.summary(),scientific_conclusion='none',
             next_action='Inspect retained records; diagnose on development and use a fresh prospective attempt'))
        for run in runs.values(): quiet(run.fail,message='S0 stopped; failure and spend retained')
        raise
    finally:
        for run in runs.values(): run._alive.set()
        budget.close();lock.close();key=''


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['check','run'])
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    try:
        if args.command=='check':
            print(canonical(verify(json.loads(args.config.read_text()),actual_host=socket.gethostname().split('.')[0])))
        else:
            if not args.out: parser.error('--out is required')
            run(args.config,args.out)
    except Exception as exc:
        # Exception text from transports may contain private endpoints; never print it.
        safe=str(exc) if isinstance(exc,ValueError) and str(exc).replace('_','').isalnum() else type(exc).__name__
        print(canonical(dict(launch_or_worker_blocked=safe)));return 1
    return 0


if __name__=='__main__': raise SystemExit(main())
