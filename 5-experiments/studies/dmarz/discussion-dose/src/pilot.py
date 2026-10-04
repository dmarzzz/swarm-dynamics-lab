"""Frozen first Anthropic qualification plan; emits no credentials."""
import argparse
import json
from pathlib import Path

MODEL='claude-haiku-4-5-20251001'
ROOT=Path(__file__).resolve().parent.parent

def plan(smoke=False):
    tasks=[6] if smoke else list(range(6))
    calls=170*len(tasks)
    config={'model':MODEL,'max_calls':calls,'max_output_tokens':1500,'max_input_bytes':60000,
            'timeout':120,'max_cost_usd':round(calls*.10,2),
            'input_usd_per_million':1,'output_usd_per_million':5}
    return {'stage':'S0','tasks':tasks,'seeds':[1],'n_agents':3,'rounds':[0,1,3,6],
            'backend':'anthropic','private_control':False,'model_config':config,
            'batch':'haiku45-preflight-v2' if smoke else 'haiku45-qualification-v3'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--smoke',action='store_true');p.add_argument('--enqueue',action='store_true');a=p.parse_args()
    params=plan(a.smoke)
    if not a.enqueue: print(json.dumps(params,indent=2));return
    import swarm_report as sr
    existing=sr.runs('discussion-dose',limit=5000)
    if any(r.get('params',{}).get('batch')==params['batch'] for r in existing):
        raise SystemExit('Batch already submitted; inspect it instead of resubmitting outcomes')
    print(json.dumps(sr.enqueue('discussion-dose',[params],tags=['S0','exploratory','anthropic'])))

if __name__=='__main__': main()
