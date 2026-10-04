"""Admitted hub worker. Publish aggregate summary only; retain native traces privately."""
import argparse
import json
import os
import sys
from pathlib import Path
import q2_admission as peer_admission
import q2_native as peer_native
import q2_run as peer_run


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--admission',required=True);p.add_argument('--ledger',required=True);a=p.parse_args()
    if not peer_native.DISPATCH_ENABLED:raise ValueError('native_dispatch_disabled')
    receipt=peer_admission.verify(a.admission,a.ledger)
    out=Path(a.out)
    if out.exists():raise ValueError('prior_output_exists')
    fd=os.open(str(out)+'.dispatch',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.close(fd)
    sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
    count=4
    job=sr.start('immune-response-v3',params={'stage':receipt['stage'],'runtime_commit':receipt['commit'],'max_calls':receipt['stage_max_calls'],'episodes':count},message=receipt['condition_tldr'])
    print(json.dumps({'run':job.id}),flush=True)
    completed=0
    def event(row):
        nonlocal completed
        if row['kind']=='episode':
            completed+=1
            job.progress(completed,count,message='Collection in progress; scientific review pending.',force=True)
    def publish():
        path=out/'summary.json'
        if path.exists():job.artifact(path,'summary.json')
    try:
        summary=peer_run.execute(out,a.admission,a.ledger,event)
        publish()
        job.done(message='Collection complete; authored qualification/scientific review pending. No automatic successor.',episodes=completed,api_calls=summary['api_calls'],actual_usd=summary['actual_usd'],scientific_review_complete=0)
    except Exception as error:
        try:publish()
        except Exception:pass
        job.fail('Collection stopped; retain all assignments: '+type(error).__name__)
        raise


if __name__=='__main__':
    try:main()
    except Exception as error:print(json.dumps({'stopped':type(error).__name__}));raise SystemExit(1)
