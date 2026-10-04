#!/usr/bin/env python3
"""Publish the saved S1 analysis as one hub run. Never enqueues cases or calls a model provider.

Stage totals go under observed_ keys only; model_calls and api_cost_usd are zero here so the hub's
summed spend is not double-counted."""
import hashlib,json,sys
from pathlib import Path
import swarm_report as sr
root=Path(sys.argv[1]);commit=sys.argv[2];message=sys.argv[3]
assert len(commit)==40 and all(c in '0123456789abcdef' for c in commit)
study='market-split-opus';ident=study+'/s1-001-analysis'
existing=sr.runs(study,limit=500)
assert not any(r['run']==ident for r in existing),'analysis_already_exists_inspect_before_retry'
cohort=[r for r in existing if r['params'].get('attempt_id')=='s1-001']
analysis=json.loads((root/'analysis.json').read_text());usage=json.loads((root/'usage.json').read_text())
assert len(cohort)==18 and all(r['status']=='done' and r['metrics']['invalid']==0 for r in cohort)
assert sum(r['metrics']['model_calls'] for r in cohort)==864==usage['attempted_calls']
cells={(c['regulator'],c['arm']):c for c in analysis['cells']}
ev={reg:int(round(cells[(reg,'neutral_dynamic')]['fragmentation_lower']*cells[(reg,'neutral_dynamic')]['attempted'])) for reg in ('none','firm','owner')}
params={'stage':'S1','kind':'analysis','attempt_id':'s1-001-analysis','analysis_of':'s1-001','report_commit':commit,'backend':'saved_records'}
receipts=[]
with sr.start(study,run=ident,params=params,message='Saved-data analysis of the Opus cohort; zero new model calls.') as run:
    for name in ('final_frame.png','analysis.json','episode-results.csv','paired-task-results.csv','usage.json','lifetime-accounting.json','model-comparison.json','records.zip'):
        p=root/name;receipt=run.artifact(p,name)
        assert receipt and not receipt.get('spooled') and receipt['sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
        receipts.append({'name':name,'sha256':receipt['sha256'],'bytes':p.stat().st_size})
    run.done(message=message,model_calls=0,api_cost_usd=0,observed_calls=864,observed_api_cost_usd=usage['api_cost_usd'],observed_episodes=36,observed_task_clusters=6,
             observed_firm_fragmentation=ev['firm'],observed_owner_fragmentation=ev['owner'],observed_none_fragmentation=ev['none'],visual_ok=1)
print(json.dumps({'run':ident,'report_commit':commit,'artifacts':receipts},indent=2))
