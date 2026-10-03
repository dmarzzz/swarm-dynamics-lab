"""Hub registration and bounded queues. S2 is deliberately unavailable before review."""
import argparse
import json
import os
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['register','queue','status']);p.add_argument('--stage',choices=['S0','S1'],default='S0')
    p.add_argument('--backend',choices=['scripted','http','anthropic'],default='scripted');p.add_argument('--dry-run',action='store_true');a=p.parse_args()
    spec=json.loads((ROOT/'experiment.yaml').read_text());design=json.loads((ROOT/'design.yaml').read_text());st=design['stages'][a.stage]
    params={'stage':a.stage,'tasks':st['tasks'],'seeds':st['seeds'],'n_agents':design['n_agents'],
            'rounds':design['rounds'],'backend':a.backend,'private_control':False}
    if a.backend!='scripted': params['model_config']=json.loads(os.environ.get('SWARM_MODEL_CONFIG','{}'))
    if a.dry_run: print(json.dumps(params,indent=2));return
    import swarm_report as sr
    if a.command=='register':
        sr.register(spec['id'],**{k:v for k,v in spec.items() if k!='id'});print('Registered exploratory discussion-dose')
    elif a.command=='queue':
        existing=sr.runs(spec['id'],limit=5000)
        if any(r.get('params',{})==params for r in existing): raise SystemExit('This batch was already submitted; create a documented new batch instead of retrying outcomes')
        print(json.dumps(sr.enqueue(spec['id'],[params],tags=[a.stage,'exploratory',a.backend])))
    else:
        print(json.dumps([{'run':r['run'],'status':r['status'],'params':r.get('params'),'metrics':r.get('metrics')} for r in sr.runs(spec['id'],limit=100)],indent=2))
if __name__=='__main__':main()
