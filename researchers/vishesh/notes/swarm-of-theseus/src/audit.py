"""Recompute scores independently from recorded requests/responses, not saved truth."""
import argparse,collections,json
from pathlib import Path

def audit(root):
    root=Path(root);manifest=json.loads((root/'manifest.json').read_text());issues=[];checked=0;total_frames=0
    for spec in manifest['assignments']:
        key=f'{spec["scenario"]}-{spec["arm"]}-{spec["seed"]}';p=root/key
        if not (p/'outcome.json').exists():issues.append([key,'missing_outcome']);continue
        row=json.loads((p/'outcome.json').read_text());events=[json.loads(l) for l in (p/'events.jsonl').read_text().splitlines()]
        checked+=1;requests=[e for e in events if e['kind']=='request'];frames=[e for e in events if e['kind']=='frame']
        total_frames+=len(frames)
        if row['status']!='completed':issues.append([key,'failed_outcome'])
        if row['status']=='completed' and (len(requests)!=24 or len(frames)!=6):issues.append([key,'call_or_frame_count'])
        for t in [f["step"] for f in frames]:
            req=[e for e in requests if e['step']==t and e['operation']=='solve']
            ans=[e['output'] for e in events if e['kind']=='response' and e['step']==t and e['operation']=='solve']
            if len(req)!=3 or len(ans)!=3:issues.append([key,t,'missing_actor']);continue
            labels=['dax','wug'] if spec['seed']%2==0 else ['wug','dax']
            if spec['scenario']=='repair-dock' and t>=4:labels=labels[::-1]
            expected=[]
            for c in req[0]['request']['observation']['cases']:
                if spec['scenario']=='observatory':
                    roots={v['root']:v['signal'] for v in c['reports']};bit=1 if sum(roots.values())*2>len(roots) else 0
                else:bit=0 if c['assay'][0]==c['assay'][1] else 1
                expected.append(labels[bit])
            correct=0
            for j,want in enumerate(expected):
                case_id=req[0]['request']['observation']['cases'][j]['id']
                counts=collections.Counter((a['answers'][j] if 'answers' in a else next(x['label'] for x in a['work'] if x['case_id']==case_id)) for a in ans)
                correct+=counts[want]>=2
            norm=['amber reed','violet stone'][spec['seed']%2]
            con=sum(a['convention']==norm for a in ans)/3
            frame=next(f for f in frames if f['step']==t)
            if frame['accuracy']!=correct/4 or frame['convention']!=con:issues.append([key,t,'score_mismatch'])
            expected_founders=3 if spec['arm']=='founders' else max(0,3-t)
            if frame['original_count']!=expected_founders:issues.append([key,t,'turnover_mismatch'])
            for e in req:
                obs=e['request']['observation']
                if 'expected' in obs or 'truth' in obs:issues.append([key,t,'label_leak'])
                if e['actor']==f'new-{t}' and 1<=t<=3:
                    if obs['private_notebook']:issues.append([key,t,'newcomer_memory_leak'])
                    if spec['arm']=='neither' and obs['onboarding']:issues.append([key,t,'channel_leak'])
        receipt=json.loads((p/'public-plan-receipt.json').read_text())
        if receipt['checked_utc']>manifest['created_utc']:issues.append([key,'late_preflight'])
    result={'assigned':len(manifest['assignments']),'checked':checked,'frames':total_frames,'issues':issues,'passed':not issues}
    (root/'audit.json').write_text(json.dumps(result,indent=2));return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root');a=p.parse_args();print(json.dumps(audit(a.root)))
