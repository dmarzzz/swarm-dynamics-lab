"""Offline R60 planning/trace primitives; not a native launcher."""
from collections import Counter
from decimal import Decimal
import hashlib,json
LABELS={'Supported','Refuted','Not Enough Evidence','Conflicting Evidence/Cherrypicking'}
def actor_only(case):
 out={k:case[k] for k in ('case_id','claim','claim_date')}
 fields=('evidence_id','question','answer','explanation','document_id','source_host')
 out['evidence']=[{k:e[k] for k in fields} for e in case['evidence']]
 # Deep copy prevents later evaluator-side mutations entering actor context.
 return json.loads(json.dumps(out))
def validate_answer(answer,actor):
 if set(answer)!={'verdict','confidence','citations','unresolved','justification'}:raise ValueError('schema')
 if answer['verdict'] not in LABELS:raise ValueError('verdict')
 if not isinstance(answer['confidence'],(int,float)) or isinstance(answer['confidence'],bool) or not 0<=answer['confidence']<=1:raise ValueError('confidence')
 if not isinstance(answer['justification'],str) or not isinstance(answer['unresolved'],str):raise ValueError('text')
 if not isinstance(answer['citations'],list) or not answer['citations']:raise ValueError('citations')
 ev={e['evidence_id']:e for e in actor['evidence']}
 for c in answer['citations']:
  if set(c)!={'evidence_id','field','quote'}:raise ValueError('citation_schema')
  if c['evidence_id'] not in ev or c['field'] not in ('answer','explanation'):raise ValueError('citation_target')
  if not isinstance(c['quote'],str) or not c['quote'].strip() or c['quote'] not in ev[c['evidence_id']][c['field']]:raise ValueError('nonliteral_quote')
 return True # Entailment is NOT established by this function.
def aggregate(ballots,assigned):
 if len(ballots)>assigned:raise ValueError('extra_votes')
 valid=[b for b in ballots if b in LABELS]
 required={1:1,6:6,60:54}[assigned]
 if len(valid)<required:return {'verdict':None,'status':'incomplete','assigned':assigned,'valid':len(valid)}
 counts=Counter(valid);top=max(counts.values());winners=[k for k,v in counts.items() if v==top]
 return {'verdict':winners[0] if len(winners)==1 else None,'status':'complete' if len(winners)==1 else 'tie_abstain','assigned':assigned,'valid':len(valid)}
def board(reports,max_items=8):
 groups={}
 for r in sorted(reports,key=lambda x:x['agent_id']):
  key=(r['answer']['verdict'],tuple(sorted({c['evidence_id'] for c in r['answer']['citations']})))
  groups.setdefault(key,[]).append(r)
 # Round-robin verdict categories protects minority categories within the item cap.
 buckets={k:[] for k in sorted(LABELS)}
 for key,rs in sorted(groups.items()):buckets[key[0]].append(rs)
 selected=[]
 while len(selected)<max_items and any(buckets.values()):
  for v in buckets:
   if buckets[v] and len(selected)<max_items:selected.append(buckets[v].pop(0))
 return {'items':[{'representative':rs[0],'matching_report_count':len(rs)} for rs in selected], 'omitted_groups':sum(len(v) for v in buckets.values()),'total_reports':len(reports),'independence_claim':False}
def assignments(roots):
 rows=[]
 for root in roots:
  for size in (1,6,60):
   for agent in range(size):
    first=f'{root}/n{size}/a{agent}/initial';rows.append({'id':first,'parent':None})
    for arm in (('peer','private') if size==60 else ('private',) if size==1 else ('peer',)):
     rows.append({'id':f'{root}/n{size}/a{agent}/{arm}','parent':first})
 return rows
def envelope():
 calls=6*7+8*(1*2+6*2+60*3)
 unit=Decimal(4000)*Decimal('0.000002')+Decimal(2048)*Decimal('0.000010')
 return {'qualification_calls':42,'pilot_calls':1552,'max_calls':calls,'input_limit':4000,'output_including_reasoning_limit':2048,'per_call_usd':str(unit),'new_api_max_usd':str(unit*calls),'prior_api_exposure_usd':'1.61753496','historical_infra_upper_bound_usd':'1','new_infra_max_usd':'0.50','cumulative_upper_bound_usd':str(unit*calls+Decimal('1.61753496')+Decimal('1.50')),'ceiling_usd':'50','native_calls':0}
if __name__=='__main__': print(json.dumps(envelope(),indent=2))
