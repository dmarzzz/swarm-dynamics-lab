"""Offline contracts and request export. No paid model calls, no credentials."""
import argparse,json
from pathlib import Path
from cases import development_examples,digest
from protocol import actor_packet,episode,summarize,ARMS
from policies import ExactReference,TapePolicy
from jev import request


def fixture_bundle():
    cases=development_examples(); episodes=[]
    from cases import make_case
    missing=make_case('bridge',1104,'no_check');missing['title']='The Missing Bridge — unavailable inspection'
    cases.append(missing)
    for case in cases:
        for arm in ('majority','blind-veto','always-check','evidence-gate','pooled','exact-reference'):
            trace=episode(case,arm,ExactReference())
            episodes.append({'case_id':case['case_id'],'title':case['title'],'scenario':case['scenario'],
                'arm':arm,'records':trace,'summary':summarize(trace)})
    def failing_policy(*args):raise RuntimeError('injected fixture failure')
    c=cases[0];trace=episode(c,'evidence-gate',failing_policy)
    episodes.append({'case_id':c['case_id']+'-failure','title':'The Missing Bridge — injected model failure','scenario':'bridge','arm':'evidence-gate','records':trace,'summary':summarize(trace)})
    return {'schema':'right-dissenter-replay-v1','mode':'unit-test-fixtures',
            'notice':'SCRIPTED SOFTWARE FIXTURES — NOT JEV RESULTS',
            'plan_version':'RD-1','episodes':episodes}


def qualification_requests():
    # Development contract probes only. Reserved qualification/holdout is not generated here.
    out=[]
    for c in development_examples():
        packet=actor_packet(c)
        private=dict(packet); private['votes']=[]; private['challenge']=None
        for phase,p in [('private',private),('admission',packet)]:
            req=request(phase,p);out.append({'phase':phase,'request_sha256':digest(req),'request':req})
    return {'mode':'development-wire-contracts','native_dispatch':False,'requests':out}


def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['fixtures','requests','replay']);p.add_argument('--out',required=True)
    p.add_argument('--tape');p.add_argument('--snapshot');a=p.parse_args()
    if a.command=='fixtures':data=fixture_bundle()
    elif a.command=='requests':data=qualification_requests()
    else:
        if not a.tape or not a.snapshot:p.error('replay requires --tape and --snapshot')
        tape=json.loads(Path(a.tape).read_text());policy=TapePolicy(tape['entries'],a.snapshot)
        records=[]
        for c in development_examples():records.extend(episode(c,'evidence-gate',policy))
        data={'mode':'native-tape-replay','records':records,'summary':summarize(records),'consumed_hashes':policy.seen}
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('x') as f:json.dump(data,f,indent=2,allow_nan=False)
    print(f'Wrote {a.command}: {out}')
if __name__=='__main__':main()
