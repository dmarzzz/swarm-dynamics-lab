#!/usr/bin/env python3
"""Finite, single-worker scripted runner. Imports reporting only in hub mode."""
from __future__ import annotations
import argparse
import json
import os
import time
from pathlib import Path
from common import ROOT,EXP,plans,assert_frozen,source_hash,design_hash,dump
import sim
import render


def metrics(records):
    m={'episodes':len(records),'invalid':sum(not r['validity']['ok'] for r in records),'model_calls':0,'api_cost_usd':0}
    for arm in sim.ARMS:
        rs=[r for r in records if r['arm']==arm];valid=[r for r in rs if r['validity']['ok']]
        if not rs: continue
        m['evasion_'+arm]=sum(r['evaluation']['behavioral_evasion'] for r in rs)/len(rs)
        if valid: m['profit_'+arm]=sum(r['evaluation']['profit'] for r in valid)/len(valid)
    if 'profit_split_control' in m and 'profit_merged' in m:
        m['profit_lift_split_control']=m['profit_split_control']-m['profit_merged']
    return m


def execute_bundle(p,out,run=None):
    if p.get('backend')!='scripted': raise ValueError('paid backend disabled')
    if p['engine_sha256']!=source_hash() or p['design_sha256']!=design_hash(): raise ValueError('queued source/config does not match worker')
    if run and getattr(run,'attempt',1)>1: raise ValueError('automatic retry refused; reconcile original artifacts')
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    records=[];selected=[];visual_errors=[];start=time.monotonic();last_upload=0
    total=len(p['tasks'])*len(p['seeds']);done=0
    active={arm:{'task_id':p['tasks'][0],'seed':p['seeds'][0],'world':p['regulator'],'dose':p['threshold'],
                 'arm':arm,'cfg':p['cfg'],'market':sim.task(p['tasks'][0]),'trace':[],
                 'validity':{'ok':False,'reason':'pending'}} for arm in p['arms']}
    def progress(arm,trace):
        nonlocal last_upload
        active[arm]['trace']=trace
        if run and time.monotonic()-last_upload>=3:
            try:
                render.frame(list(active.values()),step=trace[-1]['round']).save(out/'progress.png')
                result=run.artifact(out/'progress.png','progress.png')
                if not result or result.get('spooled'): raise RuntimeError('progress upload unconfirmed')
                last_upload=time.monotonic()
            except Exception as e:
                visual_errors.append({'phase':'progress','type':type(e).__name__});last_upload=time.monotonic()
    with (out/'episodes.jsonl').open('x') as f:
        for t in p['tasks']:
            for seed in p['seeds']:
                if time.monotonic()-start>1200: raise TimeoutError('stage runtime cap')
                first=(t,seed)==(p['tasks'][0],p['seeds'][0])
                recs=sim.run_episode(t,seed,p['regulator'],p['threshold'],p['arms'],p['cfg'],on_step=progress if first and run else None)
                for r in recs:
                    r.update({'run':run.id if run else out.name,'attempt':getattr(run,'attempt',1),
                              'attempt_id':p['attempt_id'],'stage':p['stage'],'split':'dev',
                              'code':p['code'],'engine_sha256':p['engine_sha256'],'design_sha256':p['design_sha256'],
                              'worker':os.environ.get('SWARM_SOURCE','dmarz/market-split')})
                    f.write(json.dumps(r,allow_nan=False)+'\n');f.flush();records.append(r)
                if first: selected=recs
                done+=1
                if run: run.progress(done,total,force=True,**metrics(records))
    names=[]
    try: names=render.save_bundle(selected,out)
    except Exception as e: visual_errors.append({'phase':'final','type':type(e).__name__})
    summary={'params':p,'metrics':metrics(records),'visualization':'market-split-v1',
             'selected_task':p['tasks'][0],'selected_seed':p['seeds'][0],
             'wall_seconds':round(time.monotonic()-start,3),'visualization_errors':visual_errors}
    summary['metrics']['visual_ok']=int(not visual_errors and len(names)==2)
    dump(out/'summary.json',summary)
    dump(out/'visualization-errors.json',visual_errors)
    if run:
        receipts={}
        for name in [*names,'episodes.jsonl','summary.json','visualization-errors.json']:
            response=run.artifact(out/name,name)
            if not response or response.get('spooled'): raise RuntimeError('artifact upload not confirmed')
            receipts[name]=response.get('sha256')
        dump(out/'upload-receipts.json',receipts)
        if summary['metrics']['invalid'] or visual_errors:
            raise RuntimeError('qualification failed; raw results and failure record retained')
        run.done(message='Scripted qualification only; zero model calls; replay and final frame uploaded.',**summary['metrics'])
    return summary


def execute(run):
    assert_frozen(run.params['attempt_id'])
    execute_bundle(run.params,ROOT/'results'/'hub'/run.id.replace('/','__'),run)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--local',choices=['S0','S1']);ap.add_argument('--attempt')
    a=ap.parse_args()
    if a.local:
        if not a.attempt: ap.error('--attempt required locally')
        assert_frozen(a.attempt)
        root=ROOT/'results'/a.attempt;root.mkdir(parents=True,exist_ok=False)
        summaries=[]
        for i,p in enumerate(plans(a.local,a.attempt)):
            summaries.append(execute_bundle(p,root/f'cell-{i:02d}'))
            print(json.dumps(summaries[-1]['metrics']),flush=True)
        with (root/'episodes.jsonl').open('x') as combined:
            for child in sorted(root.glob('cell-*/episodes.jsonl')): combined.write(child.read_text())
        dump(root/'summary.json',summaries)
        if any(s['metrics']['invalid'] or not s['metrics']['visual_ok'] for s in summaries): raise SystemExit('local qualification failed')
        return
    if not os.environ.get('SWARM_SOURCE'): raise SystemExit('set SWARM_SOURCE')
    import swarm_report as sr
    count=sr.work(EXP,execute,max_runs=12,stop_when_empty=True)
    print(f'completed {count} finite scripted run(s)')


if __name__=='__main__': main()
