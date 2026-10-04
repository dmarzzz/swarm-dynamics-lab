#!/usr/bin/env python3
"""Template-derived coordinator. Dry runs are offline; S2 and paid backends fail closed."""
import argparse
import json
from common import ROOT,EXP,load,plans,assert_frozen,source_hash,design_hash


def s0_qualified(runs):
    # All three S0 regulator cells with this exact engine/design must qualify.
    valid=[r for r in runs if r['params'].get('stage')=='S0' and r['params'].get('engine_sha256')==source_hash()
           and r['params'].get('design_sha256')==design_hash() and r['status']=='done'
           and r.get('metrics',{}).get('invalid')==0 and r.get('metrics',{}).get('visual_ok')==1
           and r.get('metrics',{}).get('episodes')==18/3]
    return set(r['params'].get('regulator') for r in valid)==set(load('design.yaml')['regulators'])


def main():
    ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('register');sub.add_parser('status')
    s=sub.add_parser('stage');s.add_argument('stage',choices=['S0','S1','S2']);s.add_argument('--attempt',default='preview')
    s.add_argument('--dry-run',action='store_true')
    a=ap.parse_args()
    if a.cmd=='stage':
        ps=plans(a.stage,a.attempt)
        if a.dry_run:
            print(json.dumps({'stage':a.stage,'runs':len(ps),'episodes':sum(len(p['tasks'])*len(p['seeds'])*len(p['arms']) for p in ps),'model_calls':0,'api_cost_usd':0,'example':ps[0]},indent=2));return
        assert_frozen(a.attempt)
    import swarm_report as sr
    if a.cmd=='register':
        spec=load('experiment.yaml');sr.register(EXP,**{k:v for k,v in spec.items() if k!='id'});print('registered market-split');return
    runs=sr.runs(EXP,limit=5000)
    if a.cmd=='status':
        for r in runs: print(r['run'],r['params'].get('stage'),r['status'],r.get('metrics',{}))
        return
    if any(r['params'].get('attempt_id')==a.attempt for r in runs): raise SystemExit('attempt already exists; do not enqueue twice')
    if a.stage=='S1' and not s0_qualified(runs): raise SystemExit('S1 refused: all matching S0 cells must pass with verified visuals')
    ids=sr.enqueue(EXP,ps,tags=['scripted','engineering-only',a.stage]);print(json.dumps({'queued':ids,'model_calls':0}))


if __name__=='__main__': main()
