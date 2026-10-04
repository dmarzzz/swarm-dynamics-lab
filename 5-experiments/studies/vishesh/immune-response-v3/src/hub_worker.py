"""Dedicated-host native launch, live images, and explicit qualification status."""
import argparse,datetime,gzip,hashlib,json,os,socket,sys
from pathlib import Path
import runner

def allocation(path):
    d=json.loads(Path(path).read_text())
    if d.get('host')!=socket.gethostname() or d.get('experiment')!='immune-response-v3':raise ValueError('allocation_host_or_study_mismatch')
    if not d.get('exclusive_claim_id') or not d.get('budget_grant_id') or d.get('api_quota_usd')!=8:raise ValueError('allocation_or_budget_grant_missing')
    expiry=datetime.datetime.fromisoformat(d['expires'].replace('Z','+00:00'))
    if expiry<=datetime.datetime.now(datetime.timezone.utc):raise ValueError('allocation_expired')
    return d

def upload(job,out):
    index=[]
    for name in ['manifest.json','events.jsonl','episodes.jsonl','summary.json','allocation-receipt.json','public-plan-receipt.json','replay.html','visualization-provenance.json']:
        p=out/name
        if not p.exists():continue
        raw=p.read_bytes();payload=gzip.compress(raw,mtime=0);parts=[]
        for n in range(0,len(payload),850000):
            chunk=out/(name+f'.gz.part{n//850000:04d}');chunk.write_bytes(payload[n:n+850000]);job.artifact(chunk,chunk.name);parts.append(chunk.name)
        index.append({'file':name,'sha256':hashlib.sha256(raw).hexdigest(),'encoding':'gzip','parts':parts})
    for name in ['live_frame.png','final_frame.png','replay.gif']:
        p=out/name
        if p.exists():job.artifact(p,name)
    runner.write_json(out/'artifact-index.json',index);job.artifact(out/'artifact-index.json','artifact-index.json')

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--allocation-receipt',required=True);a=p.parse_args()
    receipt=allocation(a.allocation_receipt)
    sys.path.insert(0,str(runner.ROOT.parent/'experiment-documentation'))
    from public_plan import check
    tldr='Fresh native qualification of keyed record choices after the v2 duplicate-fact failure; task 6700 compares Q11, Q10F and CLEAN with recorded live repair traces.'
    public=check('immune-response-v3',tldr)
    import swarm_report as sr
    from live import LiveFrames
    from visualize import render
    plan=json.loads((runner.ROOT/'design.json').read_text())['plans']['native-repair'];out=Path(a.out)
    job=sr.start('immune-response-v3',params={'stage':'native-repair','backend':'anthropic','tasks':plan['tasks'],'worlds':plan['worlds'],'arms':plan['arms'],'design_hash':hashlib.sha256((runner.ROOT/'design.json').read_bytes()).hexdigest()},message=tldr)
    frames=LiveFrames(job,out,plan['arms'])
    try:
        summary=runner.execute(out,'native-repair','anthropic',frames)
        runner.write_json(out/'allocation-receipt.json',receipt);runner.write_json(out/'public-plan-receipt.json',public)
        render(out,out,world='shared_evidence',task=6700)
        summary['live_reporting_failures']=frames.errors;runner.write_json(out/'summary.json',summary)
        upload(job,out)
        metrics={k:summary[k] for k in ['invalid','execution_qualified','clean_qualified']};metrics.update(episodes=summary['recorded'],model_backed=1)
        if summary['execution_qualified'] and summary['clean_qualified']:job.done(message='Native qualification passed; effect remains exploratory and task-specific',**metrics)
        else:job.fail('Qualification failed; preserve outcomes and diagnose before any new attempt',**metrics)
    except Exception as exc:
        try:
            if out.exists():upload(job,out)
        except Exception:pass
        job.fail('Execution or reporting interrupted: '+type(exc).__name__)
        raise

if __name__=='__main__':
    try:main()
    except Exception as exc:print('Worker stopped: '+type(exc).__name__,file=sys.stderr);raise SystemExit(1)
