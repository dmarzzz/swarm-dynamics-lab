"""Fail-closed Q-A runner. No credentials are inspected until after launch checks."""
import argparse
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
from tasks import generate,qualification_manifest,evaluate,operational

REQUIRED=('expected_served_model','expected_served_provider','stage_cap_microdollars',
          'episode_cap_microdollars','spending_authorization','independent_review_commit',
          'exclusive_machine_claim','public_plan_receipt','authorized_total_microdollars')


def launch_errors(config):
    errors=[f'missing:{k}' for k in REQUIRED if not config.get(k)]
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
    args.output.mkdir(parents=True,exist_ok=False)
    assignments=[row for row in qualification_manifest() if row['stage']=='Q-A']
    (args.output/'assigned.json').write_text(json.dumps(assignments,indent=2)+'\n')
    bank=Budget(args.budget_ledger,config['stage_cap_microdollars'])
    for row in qualification_manifest():
        if row['stage']!='Q-A':continue
        episode=row['id'];target=args.output/(hashlib.sha256(episode.encode()).hexdigest()[:16])
        target.mkdir(exist_ok=False);lock=threading.Lock()
        tldr=f"TLDR: Q-A {row['family']} {row['structure']} root {row['root']}, N=1 under screening caps; single-agent calibration reference for later matched-N comparisons. Metrics: verified on-time success, quality, cost and latency. Exploratory synthetic tasks; not a size-effect result."
        (target/'assignment.json').write_text(json.dumps(row|{'commit':commit,'run_tldr':tldr,'status':'assigned'},indent=2)+'\n')
        def journal(event):
            with lock:
                with (target/'trace.jsonl').open('a') as handle:
                    handle.write(json.dumps(event)+'\n');handle.flush();os.fsync(handle.fileno())
        reporter=Reporter(config['experiment_id'],row,tldr)
        completed=0
        def measured_event(event):
            nonlocal completed
            journal(event)
            if event['kind']=='work_complete':
                completed+=1
                reporter.progress(completed)
        task=generate(row['family'],row['structure'],row['root'])
        runtime=Provider(config,bank,episode,journal)
        record=execute(task.public,1,config['slots'],config['screening_deadline_s'],config['integration_reserve_s'],runtime,measured_event)
        result=evaluate(task,record['artifact'] or '{}')
        exposure=bank.exposure(episode)
        record.update(assignment=row,commit=commit,evaluation=result,exposure_microdollars=exposure,
                      operational_success=operational(result,record['elapsed_s'],exposure,config['screening_deadline_s'],config['episode_cap_microdollars']))
        with (target/'outcome.json').open('x') as handle:json.dump(record,handle,indent=2)
        render(target/'trace.jsonl',target/'replay.html')
        reporter.finish(target,record)
        print(json.dumps({'episode':episode,'terminal':True,'success':record['operational_success']}),flush=True)
        if not bank.healthy():break
    print('Q-A terminal. Q-B requires the calibration assessment and a separately frozen configuration.')
    return 0

if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:
        # Avoid displaying provider bodies, URLs containing credentials or process environments.
        print('Launch stopped: '+(str(exc) if isinstance(exc,ValueError) else type(exc).__name__))
        raise SystemExit(2)
