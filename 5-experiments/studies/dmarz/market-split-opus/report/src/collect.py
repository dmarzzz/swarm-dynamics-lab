#!/usr/bin/env python3
"""Collect a complete, single frozen S1 cohort without pooling earlier attempts."""
import argparse,json,hashlib
from pathlib import Path

def collect(base,attempt,out):
    records=[];bundles=[];versions=set();identities=set()
    for folder in sorted(Path(base).iterdir()):
        if not (folder/'summary.json').is_file():continue
        summary=json.loads((folder/'summary.json').read_text());p=summary['params']
        if p.get('attempt_id')!=attempt:continue
        if p['stage']!='S1':raise ValueError('not_S1')
        if summary['metrics']['invalid'] or not summary['metrics']['visual_ok']:raise ValueError('failed_bundle')
        receipts=json.loads((folder/'upload-receipts.json').read_text())
        for name,digest in receipts.items():
            if hashlib.sha256((folder/name).read_bytes()).hexdigest()!=digest:raise ValueError('artifact_hash')
        rs=[json.loads(x) for x in (folder/'episodes.jsonl').read_text().splitlines()]
        if len(rs)!=2:raise ValueError('incomplete_bundle')
        for r in rs:
            if r['attempt_id']!=attempt or not r['validity']['ok'] or len(r['trace'])!=24:raise ValueError('incomplete_episode')
            if r['model_calls']!=24 or r['unpriced_calls']:raise ValueError('incomplete_accounting')
            k=(r['task_id'],r['seed'],r['world'],r['arm'])
            if k in identities:raise ValueError('duplicate_episode')
            identities.add(k);versions.add((r['model'],r['engine_sha256'],r['design_sha256']))
        records.extend(rs);bundles.append({'run':rs[0]['run'],'params':p,'artifacts':receipts})
    expected={(t,41,reg,arm) for t in range(110,116) for reg in ('none','firm','owner') for arm in ('neutral_dynamic','neutral_locked')}
    if identities!=expected or len(versions)!=1:raise ValueError('incomplete_or_mixed_cohort')
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    (out/'episodes.jsonl').write_text(''.join(json.dumps(r,allow_nan=False)+'\n' for r in records))
    (out/'receipts.json').write_text(json.dumps(bundles,indent=2)+'\n')
    print(json.dumps({'attempt':attempt,'bundles':len(bundles),'episodes':len(records),'model_calls':sum(r['model_calls'] for r in records),'api_cost_usd':sum(r['api_cost_usd'] for r in records)}))

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('base');a.add_argument('attempt');a.add_argument('out');v=a.parse_args();collect(v.base,v.attempt,v.out)
