"""Template-derived registration and idempotent, bounded stage queueing."""
import argparse
import json
from pathlib import Path
import yaml
import worker

ROOT=Path(__file__).resolve().parent.parent


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('command',choices=['register','stage','status'])
    ap.add_argument('stage',nargs='?',choices=['S0','S1','S2']); ap.add_argument('--dry-run',action='store_true')
    a=ap.parse_args()
    if a.command=='stage' and a.stage=='S2': raise SystemExit('S2 disabled: reviewed survey and accepted hypothesis required')
    if a.command=='stage' and not a.stage: raise SystemExit('Specify S0 or S1')
    if a.command=='stage' and a.dry_run:
        p=worker.params(a.stage); print(json.dumps({'runs':len(p),'arm_episodes':sum(len(x['tasks'])*4 for x in p),'model_calls':0})); return
    import swarm_report as sr
    exp=yaml.safe_load((ROOT/'experiment.yaml').read_text())
    if a.command=='register': sr.register(exp.pop('id'),**exp); print('Registered sybil-specialists'); return
    runs=sr.runs('sybil-specialists',limit=5000)
    if a.command=='status':
        print(json.dumps([{'run':r['run'],'status':r['status'],'stage':r.get('params',{}).get('stage')} for r in runs],indent=2)); return
    if a.stage=='S1':
        desired=worker.params('S0')
        for p in desired:
            if not any(r.get('params')==p and r['status']=='done' and r.get('metrics',{}).get('invalid')==0 for r in runs):
                raise SystemExit('S1 blocked: every exact-source S0 cell must be done with zero invalid episodes')
    wanted=worker.params(a.stage)
    existing=[p for p in wanted if any(r.get('params')==p for r in runs)]
    pending=[p for p in wanted if p not in existing]
    if existing: print('Existing assignments retained:',len(existing))
    if pending: print('Queued:',len(sr.enqueue('sybil-specialists',pending,tags=[a.stage,'scripted','exploratory'])))

if __name__=='__main__': main()
