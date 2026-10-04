"""Publish analysis and correct dashboard classification; no scientific re-execution."""
import argparse,json
from pathlib import Path


def main():
    import swarm_report as sr
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--analysis',type=Path,required=True);a=ap.parse_args()
    exp='adaptive-quorum-api-v2';url='https://github.com/dmarzzz/swarm-lab/tree/main/researchers/vishesh/notes/adaptive-quorum-v2/repair-v3'
    sr.register(exp,title='Antsy',description='When should a swarm commit? Guarded local Laya agents choose synthetic APIs under delayed or misleading evidence. The repaired study shows conditional quorum tradeoffs, not universal adaptive superiority.',url=url)
    for stage in ('D0','Q1','Q2','S1'):
        attempts=(1,2) if stage=='S1' else (1,)
        for attempt in attempts:
            rid=f'{exp}/repair-v3-{stage}-attempt-{attempt}'
            sr.report('metric',exp,rid,params={'kind':'experiment' if stage=='S1' else 'diagnostic' if stage=='D0' else 'qualification'},url=url,strict=True)
    old=f'{exp}/repair-v3-S1-attempt-1'
    for name in ('failure.json','manifest.json','episodes.jsonl.gz','receipts.json','invocations.json.gz','guard-events.json.gz'):
        sr.upload(old,a.root/'S1-attempt-1'/name,name)
    sr.report('progress',exp,old,step=25,total=384,status='failed',message='GIF duration TypeError after 25 preserved blocks. Fixed and resumed without rerolling in repair-v3-S1-attempt-2; original failure retained.',strict=True)
    rid=f'{exp}/repair-v3-S1-attempt-2'
    for p in a.analysis.iterdir():
        if p.suffix in ('.png','.json','.csv','.md'):sr.upload(rid,p,p.name)
    sr.report('metric',exp,rid,metrics={'qualified':1,'episodes':2688,'invalid':0},message='384/384 paired blocks complete; 25 recovered unchanged. Zero actor errors. Adaptive helps with late correction and hurts with late misinformation; all policy choices match symbolic baseline.',strict=True)
    # Confirm status and artifact availability without returning private endpoints/config.
    result=sr.get_run(rid)
    print(json.dumps({'status':result['status'],'artifacts':[x['name'] for x in result.get('artifacts',[])],'run':rid}))


if __name__=='__main__':main()
