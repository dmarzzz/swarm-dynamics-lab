#!/usr/bin/env python3
"""Finite worker; no automatic reruns. Every response is durably logged before advancing."""
import argparse
import json
import os
import time
from pathlib import Path
import common
import sim
import render
from policy import Policy,mock_opener
from provider import Anthropic,Ledger

def execute_bundle(p,out,ledger_path=None,run=None):
    if p['backend'] not in ('mock','anthropic'):raise ValueError('unknown_backend')
    if any(p[k]!=v for k,v in common.hashes().items()):raise ValueError('source_mismatch')
    if run and run.attempt!=1:raise ValueError('retry_refused')
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    d=common.design();cfg={**d['cfg'],'rounds':p['rounds']};records=[];visual_errors=[]
    ledger=Ledger(ledger_path if p['backend']=='anthropic' else out/'mock-ledger.jsonl')
    client=Anthropic(ledger,opener=mock_opener,key='offline',workspace='offline') if p['backend']=='mock' else Anthropic(ledger)
    identity=f"{p['attempt_id']}:{p['task_id']}:{p['seed']}:{p['regulator']}"
    policy=Policy(client,out/'calls.jsonl',identity,p['backend'],d['budget']['stage_timeout_seconds'])
    selected={arm:{'task_id':p['task_id'],'seed':p['seed'],'world':p['regulator'],'dose':p['threshold'],'arm':arm,
                   'cfg':cfg,'market':sim.task(p['task_id']),'backend':p['backend'],'trace':[],
                   'validity':{'ok':False,'reason':'pending'}} for arm in p['arms']}
    last_upload=0
    def progress(arm,trace):
        nonlocal last_upload
        selected[arm]['trace']=trace
        if run:
            run.progress(sum(len(r['trace']) for r in selected.values()),len(p['arms'])*p['rounds'],force=True,
                         **policy.metrics(),round=trace[-1]['round'])
            if time.monotonic()-last_upload>=12:
                try:
                    render.frame(list(selected.values()),step=trace[-1]['round']).save(out/'progress.png')
                    receipt=run.artifact(out/'progress.png','progress.png')
                    if not receipt or receipt.get('spooled'):raise RuntimeError('unconfirmed_upload')
                except Exception as e:visual_errors.append({'phase':'progress','type':type(e).__name__})
                last_upload=time.monotonic()
    for arm in p['arms']:
        arm_cfg={**cfg,'max_firms':1 if arm=='neutral_locked' else cfg['max_firms']}
        rec=sim.run_episode(p['task_id'],p['seed'],p['regulator'],p['threshold'],[arm],arm_cfg,policy,on_step=progress)[0]
        rec.update(backend=p['backend'],stage=p['stage'],attempt_id=p['attempt_id'],run=run.id if run else out.name,
                   code=p['code'],engine_sha256=p['engine_sha256'],design_sha256=p['design_sha256'],
                   model=d['model'] if p['backend']=='anthropic' else None,**policy.metrics(arm))
        ref=sim.run_episode(p['task_id'],p['seed'],p['regulator'],p['threshold'],['merged'],arm_cfg)[0]
        rec['competence_profit_ratio']=rec['evaluation']['profit']/ref['evaluation']['profit'] if ref['evaluation']['profit']>0 else None
        records.append(rec);selected[arm]=rec
        with (out/'episodes.jsonl').open('a') as f:
            f.write(json.dumps(rec,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
    metrics={'episodes':len(records),'invalid':sum(not r['validity']['ok'] for r in records),**policy.metrics()}
    for rec in records:
        name='dynamic' if rec['arm']=='neutral_dynamic' else 'locked'
        metrics['fragmentation_'+name]=int(rec['evaluation']['strategic_fragmentation'])
        metrics['profit_'+name]=rec['evaluation']['profit']
        metrics['firms_'+name]=rec['evaluation']['final_firm_count']
    qualified=all(r['validity']['ok'] and r['evaluation']['profit']>0 and r['competence_profit_ratio'] is not None and r['competence_profit_ratio']>=d['qualification']['min_profit_ratio'] for r in records)
    if p['stage'] in ('S0','Q0'):metrics['qualification_pass']=int(qualified)
    names=[]
    try:names=render.save_bundle(records,out)
    except Exception as e:visual_errors.append({'phase':'final','type':type(e).__name__})
    metrics['visual_ok']=int(len(names)==2 and not visual_errors)
    common.dump(out/'visualization-errors.json',visual_errors)
    common.dump(out/'summary.json',{'params':p,'metrics':metrics,'ledger':ledger.transact(),
                                   'selected_task':p['task_id'],'selected_seed':p['seed'],'mapping':'market-split-api-v1'})
    if run:
        receipts={}
        for name in [*names,'episodes.jsonl','calls.jsonl','summary.json','visualization-errors.json']:
            receipt=run.artifact(out/name,name)
            if not receipt or receipt.get('spooled'):raise RuntimeError('unconfirmed_upload')
            receipts[name]=receipt['sha256']
        common.dump(out/'upload-receipts.json',receipts)
        if metrics['invalid'] or not metrics['visual_ok'] or (p['stage']=='Q0' and not qualified):
            run.fail(message='Qualification or execution failed; all traces retained; advancement blocked.',**metrics)
            raise RuntimeError('qualification_failed')
        run.done(message='Neutral model outcomes retained; exploratory evidence only.' if p['backend']=='anthropic' else 'Offline API rehearsal; zero model calls.',**metrics)
    return metrics

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--local-mock',action='store_true');ap.add_argument('--attempt',required=True)
    ap.add_argument('--ledger',default='/srv/swarm/market-split-api/accounting/ledger.jsonl');ap.add_argument('--max-runs',type=int,default=18)
    a=ap.parse_args();common.frozen(a.attempt)
    if a.local_mock:
        from coordinator import plans
        for i,p in enumerate(plans('S0',a.attempt)):
            m=execute_bundle(p,common.ROOT/'results'/a.attempt/f'cell-{i:02d}')
            if m['invalid'] or not m['visual_ok']:raise SystemExit('mock qualification failed')
        print('Offline API rehearsal passed; zero model calls.');return
    if not os.environ.get('SWARM_SOURCE'):raise SystemExit('SWARM_SOURCE required')
    import swarm_report as sr
    start=time.monotonic();completed=0
    while completed<a.max_runs:
        if time.monotonic()-start>common.design()['budget']['stage_timeout_seconds']:raise SystemExit('stage wall-time cap')
        run=sr.next_run(common.EXP)
        if run is None:break
        with run:
            if run.params['attempt_id']!=a.attempt:raise ValueError('wrong_attempt')
            execute_bundle(run.params,common.ROOT/'results'/'hub'/run.id.replace('/','__'),a.ledger,run)
        completed+=1
    print(f'completed {completed} finite runs',flush=True)
if __name__=='__main__':main()
