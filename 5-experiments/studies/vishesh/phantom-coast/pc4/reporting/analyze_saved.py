"""Post-run reporting only; no network, new assignments or model calls."""
import json,sys,statistics,math,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from contract import reconstruct
from design import contrasts,loss

def analyze(out):
 out=Path(out);es=json.loads((out/'episodes.json').read_text());rs=json.loads((out/'records.json').read_text());s=json.loads((out/'summary.json').read_text());a=contrasts(es)
 a['native_vs_deterministic']={'consensus_label_disagreements':sum(sum(e['endpoint']['map'][c]!=v for c,v in reconstruct(e['packet']).items()) for e in es),'episode_count':len(es),'label_count':len(es)*36}
 a['policy_costs']={p:{'calls':sum(r['policy']==p and r['status']!='not-started' for r in rs),'valid':sum(r['policy']==p and r['status']=='valid' for r in rs),'known_usd':sum(r.get('checked',{}).get('usage',{}).get('cost',0) for r in rs if r['policy']==p),'input_tokens':sum(r.get('checked',{}).get('usage',{}).get('input_tokens',0) for r in rs if r['policy']==p)} for p in ('q0','q2','q4','uniform')}
 a['paired_policy_contrasts']=[]
 for false in (0,2,4):
  for policy in ('q0','q2','q4'):
   xs=[];dw=[];du=[]
   for seed in sorted({e['seed'] for e in es}):
    t=next(e for e in es if e['seed']==seed and e['policy']==policy and e['false_count']==false);c=next(e for e in es if e['seed']==seed and e['policy']=='uniform' and e['false_count']==false)
    xs.append(loss(t)-loss(c));dw.append(t['endpoint']['whole']['wrong']-c['endpoint']['whole']['wrong']);du.append(t['endpoint']['whole']['missing']-c['endpoint']['whole']['missing'])
   se=statistics.stdev(xs)/math.sqrt(len(xs));a['paired_policy_contrasts'].append(dict(policy=policy,false_count=false,mean=statistics.mean(xs),se=se,descriptive_t31_interval=[statistics.mean(xs)-2.039513*se,statistics.mean(xs)+2.039513*se],total_wrong_difference=sum(dw),total_unknown_difference=sum(du),abstention_break_even=-sum(dw)/sum(du) if sum(du) else None))
 a.update(assigned=s['assigned'],valid=s['valid'],complete_episodes=s['complete_episodes'],wall_seconds=s['wall_seconds'],known_cost_usd=sum(r.get('checked',{}).get('usage',{}).get('cost',0) for r in rs),call_seconds=sum(r.get('elapsed_seconds',0) for r in rs),analysis_scope='Prespecified metrics with post-run descriptive decomposition; same-operator saved-data analysis, no new model calls.')
 return a
if __name__=='__main__':print(json.dumps(analyze(sys.argv[1]),indent=2))
