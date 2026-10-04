from pathlib import Path
import json,sys,collections,hashlib
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'src'))
from live_design import development,RANDOM_CHECK_INDICES
from cases import digest
from jev import request
from protocol import episode,ARMS,summarize
from policies import ExactReference
out=Path(sys.argv[1]) if len(sys.argv)>1 else P/'results/s1-a1';rows=json.loads((out/'records.json').read_text());summary=json.loads((out/'summary.json').read_text());calls=json.loads((out/'calls.json').read_text());tape={x['request_sha256']:x for x in calls}
assert summary['missing']==0 and len(rows)==420
per_condition={};per_scenario={};logical={};replayed=[]
for arm in ARMS:
 selected=[r for r in rows if r['arm']==arm];s=summarize(selected)
 for k,v in s.items():assert summary['by_arm'][arm][k]==v,(arm,k)
 per_condition[arm]={c:summarize([r for r in selected if r['condition']==c]) for c in sorted({r['condition'] for r in selected})}
 per_scenario[arm]={c:summarize([r for r in selected if r['scenario']==c]) for c in ('bridge','build','alarm')}
 used=[]
 def policy(phase,packet):
  h=digest(request(phase,packet));x=tape[h];used.append(x.get('checked',{}))
  if x['status']!='completed':
   from live_worker import TransportFailure
   raise TransportFailure('saved_failure')
  return x['checked']['action']
 replay=[]
 for i,c in enumerate(development()):
  result=episode(c,arm,ExactReference() if arm=='exact-reference' else policy,random_check=i in RANDOM_CHECK_INDICES if arm=='matched-random' else None)
  for row in result:row['condition']=c['condition'];row['seed']=c['seed']
  replay.extend(result)
 key=lambda r:(r['case_id'],r['actor']['task']['now'])
 assert sorted(replay,key=key)==sorted(selected,key=key),arm
 logical[arm]={'logical_calls':len(used),'failed_logical_calls':sum(not x for x in used),'counterfactual_input_tokens':sum(x.get('input_tokens',0) for x in used),'counterfactual_api_cost_usd':sum(x.get('cost_usd',0) for x in used)}
assert sum(x['logical_calls'] for x in logical.values())==summary['logical_calls']
lookup={(r['arm'],r['case_id'],r['actor']['task']['now']):r for r in rows};contrasts={}
for comparator in ('majority','always-check','exact-reference','matched-random','pooled','blind-veto'):
 a=[r for r in rows if r['arm']=='evidence-gate'];b=[lookup[(comparator,r['case_id'],r['actor']['task']['now'])] for r in a]
 contrasts[comparator]={'evidence_gate_better':sum(x['correct_completion'] and not y['correct_completion'] for x,y in zip(a,b)),'evidence_gate_worse':sum(y['correct_completion'] and not x['correct_completion'] for x,y in zip(a,b)),'net_correct':sum(x['correct_completion']-y['correct_completion'] for x,y in zip(a,b)),'net_checks':sum(x['checks']-y['checks'] for x,y in zip(a,b))}
temporal={a:{'assigned':12,'correct':sum(r['correct_completion'] for r in rows if r['arm']==a and r['scenario']=='alarm'),'closures':dict(collections.Counter(r['closure'] for r in rows if r['arm']==a and r['scenario']=='alarm')),'fresh_epoch_correct':sum(r['correct_completion'] for r in rows if r['arm']==a and r['scenario']=='alarm' and r['actor']['task']['now']==3)} for a in ARMS}
loss={str(w):{a:round(w*s['wrong_proceed']+s['unnecessary_hold']+2*s['unresolved']+0.1*s['checks'],3) for a,s in summary['by_arm'].items()} for w in (1,5,10)}
result={'reconciliation':'420 saved rows exactly match replay of saved native decisions; no new model calls','by_condition':per_condition,'by_scenario':per_scenario,'evidence_gate_paired_contrasts':contrasts,'per_policy_counterfactual_api':logical,'temporal':temporal,'illustrative_loss_sensitivity':loss,'loss_note':'Wrong PROCEED weights1,5,10; unnecessary HOLD1; DEFER/deadline2; checks0.1. Design preferences, not empirical utilities. Counterfactual policy API costs reuse saved responses; actual joint cost stays in summary.'}
(out/'analysis.json').write_text(json.dumps(result,indent=2));print(json.dumps({'contrasts':contrasts,'logical_calls':logical,'temporal':temporal,'loss':loss}))
