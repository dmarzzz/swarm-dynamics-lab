#!/usr/bin/env python3
"""Publish saved S1 analysis only. Never enqueue cases or call a model provider."""
import hashlib,json,sys
from pathlib import Path
import swarm_report as sr
root=Path(sys.argv[1]);commit=sys.argv[2]
assert len(commit)==40 and all(c in '0123456789abcdef' for c in commit)
study='market-split-api';ident=study+'/s1-002-analysis'
existing=sr.runs(study,limit=500)
assert not any(r['run']==ident for r in existing),'analysis_already_exists_inspect_before_retry'
cohort=[r for r in existing if r['params'].get('attempt_id')=='s1-002']
assert len(cohort)==18 and all(r['status']=='done' and r['metrics']['invalid']==0 for r in cohort)
assert sum(r['metrics']['model_calls'] for r in cohort)==864
params={'stage':'S1','kind':'analysis','attempt_id':'s1-002-analysis','analysis_of':'s1-002','report_commit':commit,'backend':'saved_records'}
receipts=[]
with sr.start(study,run=ident,params=params,message='Complete original Sonnet cohort: saved-data analysis; zero new model calls.') as run:
    for name in ('final_frame.png','analysis.json','episode-results.csv','usage.json','lifetime-accounting.json','post-mortem.md','records.zip','RESULTS.md'):
        p=root/name;receipt=run.artifact(p,name)
        assert receipt and not receipt.get('spooled') and receipt['sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
        receipts.append({'name':name,'sha256':receipt['sha256'],'bytes':p.stat().st_size})
    run.done(message='36/36 valid episodes. Flexible Sonnet split and met sustained evasion in 6/6 firm-regulated markets, 0/6 owner and 0/6 unregulated. Main usage $14.125788. Six related tasks; exploratory. Next plan published, unstarted.',model_calls=0,api_cost_usd=0,observed_calls=864,observed_api_cost_usd=14.125788,observed_episodes=36,observed_task_clusters=6,observed_firm_evasion=6,observed_owner_evasion=0,visual_ok=1)
print(json.dumps({'run':ident,'report_commit':commit,'artifacts':receipts},indent=2))
