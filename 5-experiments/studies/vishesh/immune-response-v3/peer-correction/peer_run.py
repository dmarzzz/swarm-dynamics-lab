"""Disabled native runner; admission precedes ledger claim and every paid request."""
import argparse
import datetime
import json
import os
from pathlib import Path
import peer_native
import peer_admission
import peer_qualification
import peer_collection


def execute(out,admission,ledger,on_event=None):
    if not peer_native.DISPATCH_ENABLED:raise ValueError('native_dispatch_disabled_pending_grant')
    receipt=peer_admission.verify(admission,ledger)
    out=Path(out);out.mkdir(parents=True,exist_ok=False,mode=0o700)
    (out/'admission.json').write_text(json.dumps(receipt,indent=2))
    minutes=15 if receipt['stage']=='peer-correction-q1' else 40
    now=datetime.datetime.now(datetime.timezone.utc)
    deadline=min((now+datetime.timedelta(minutes=minutes)).timestamp(),peer_admission.stamp(receipt['allocation']['expires']).timestamp()-300)
    policy=peer_native.Policy(ledger,out/'usage.jsonl',receipt['stage'],receipt['packet_sha256'],deadline)
    final=None
    with (out/'events.jsonl').open('x') as events:
        def emit(row):
            nonlocal final
            events.write(json.dumps(row)+'\n');events.flush();os.fsync(events.fileno())
            if row['kind']=='closeout':final=row
            if on_event is not None:on_event(row)
        try:
            result=peer_qualification.collect(policy,emit) if receipt['stage']=='peer-correction-q1' else peer_collection.collect(policy,emit,repeats=1)
            (out/'episodes.json').write_text(json.dumps(result['episodes'],indent=2)+'\n')
        finally:
            summary={'stage':receipt['stage'],'collection':final,'api_calls':policy.calls,
                     'actual_usd':policy.actual_usd,'usage_missing':policy.usage_missing,
                     'scientific_review':'pending','successor_authorized':False,
                     'required_closeout':'Run offline experiment finalize and complete authored scientific assessment; collection exit is not study completion.'}
            (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--admission',required=True);p.add_argument('--ledger',required=True);a=p.parse_args()
    try:execute(a.out,a.admission,a.ledger)
    except Exception as error:
        print(json.dumps({'stopped':type(error).__name__,'model_dispatch_enabled':peer_native.DISPATCH_ENABLED}));raise SystemExit(1)
