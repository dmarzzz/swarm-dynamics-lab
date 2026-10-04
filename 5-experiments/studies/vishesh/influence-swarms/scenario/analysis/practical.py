"""Describe measured workflow cost and decision sensitivity without new model claims."""
import argparse,copy,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from dossier import evaluate

def analyze(root):
    root=Path(root);rows=json.loads((root/'outcomes.json').read_text());costs=[];sensitivity=[]
    for file in sorted(root.glob('case-*.json'),key=lambda p:int(p.stem.split('-')[1])):
        i=file.stem.split('-')[1];case=json.loads(file.read_text())
        events=[json.loads(x) for x in (root/f'events-{i}.jsonl').read_text().splitlines()]
        solo=False;team_usd=solo_usd=0;team_calls=solo_calls=0;team_end=None;solo_start=None;solo_end=None
        for event in events:
            if event['kind']=='request' and event['request']['observation'].get('role')=='generalist':
                solo=True;solo_start=event['elapsed_seconds']
            if event['kind']=='response':
                u=event.get('usage',{});dollars=u.get('actual_usd',0);calls=u.get('calls',0)
                if solo:solo_usd+=dollars;solo_calls+=calls
                else:team_usd+=dollars;team_calls+=calls
            if event['kind']=='terminal':
                if event['outcome']['arm']=='solo':solo_end=event['elapsed_seconds']
                else:team_end=event['elapsed_seconds']
        costs.append({'case':case['case_id'],'world':case['world'],'team_both_chairs_actual_usd':team_usd,'solo_actual_usd':solo_usd,
                      'team_both_chairs_api_attempts':team_calls,'solo_api_attempts':solo_calls,'team_collection_seconds':team_end,
                      'solo_collection_seconds':solo_end-solo_start if solo_end is not None and solo_start is not None else None})
        for r in [r for r in rows if r['case_id']==case['case_id'] and r['world']==case['world']]:
            if not r['valid']:continue
            variants=[]
            for labor in (.5,1,1.5):
                for tolerance in (0,.03,.1):
                    variant=copy.deepcopy(case);variant['brief']['human_cost_per_unresolved_ticket']*=labor;variant['brief']['cost_tolerance_fraction']=tolerance
                    e=evaluate(variant,r['decision']);variants.append({'labor_multiplier':labor,'tolerance':tolerance,'acceptable':e['acceptable_decision'],'dollar_regret':e['cost_regret_usd']})
            sensitivity.append({'case':case['case_id'],'world':case['world'],'arm':r['arm'],'choice':r['decision']['choice'],'acceptable_across_all':all(v['acceptable'] for v in variants),'variants':variants})
    summary=json.loads((root/'summary.json').read_text());receipted=sum(c['team_both_chairs_actual_usd']+c['solo_actual_usd'] for c in costs)
    return {'costs':costs,'recorded_response_usd':receipted,'summary_usd':summary['actual_usd'],'usage_reconciles':abs(receipted-summary['actual_usd'])<1e-8,
            'sensitivity':sensitivity,'limits':'Both team chair forks are charged together, not independent teams. Timing includes instrumentation. Sensitivity regrades the recorded choice under alternative assumptions; it is not a new model response. Failed calls without responses may lack per-workflow usage receipts.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('run');p.add_argument('out');a=p.parse_args();Path(a.out).write_text(json.dumps(analyze(a.run),indent=2)+'\n')
