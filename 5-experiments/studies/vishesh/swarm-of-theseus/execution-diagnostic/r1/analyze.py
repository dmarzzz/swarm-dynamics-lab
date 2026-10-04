import json,collections,csv,html
from pathlib import Path
from design import d1,digest
from scoring import reference

def summarize(root):
 root=Path(root);manifest=json.loads((root/'manifest.json').read_text());design=manifest['assignments'];rows=[];mismatches=[];requests=[];completed=started=0;cost=0;unknown=0;arm_cost=collections.defaultdict(float);arm_calls=collections.Counter();provider_errors=[]
 for a in design:
  sf=root/'calls'/(a['id']+'-started.json');rf=root/'calls'/(a['id']+'-finished.json');result={'value':None,'error':'not_started','response_received':False}
  if sf.exists():
   started+=1;s=json.loads(sf.read_text())
   if s['request']!=a['request'] or s['request_sha256']!=digest(a['request']):requests.append(a['id'])
  if rf.exists():
   completed+=1;result=json.loads(rf.read_text());arm_calls[a['arm']]+=1
   if result['actual_usd'] is None:unknown+=1
   else:cost+=result['actual_usd'];arm_cost[a['arm']]+=result['actual_usd']
   if result.get('error'):provider_errors.append({'id':a['id'],'error':result['error']})
  ref=reference(a,result);primary=d1.score(dict(a,arm='E'),result)['rows']
  for r,p,c in zip(ref,primary,a['cases']):
   if r['correct']!=p['correct'] or r['valid_response']!=p['valid_response']:mismatches.append({'assignment':a['id'],'case':r['id']})
   # Missing records remain assigned strict failures.
   rows.append(dict(r,assignment=a['id'],seed=a['seed'],arm=a['arm'],context=a['context'],order=a['order'],repeat=a['repeat'],position=a['positions'][r['id']],source=a['rule'][c['class']],conflict=any(c['evidence'][s]!=c['evidence'][a['rule'][c['class']]] for s in c['evidence'] if s!=a['rule'][c['class']]),terminal=rf.exists()))
 arms={}
 for arm in ('E','F'):
  rs=[r for r in rows if r['arm']==arm];worlds={str(s):sum(r['correct'] for r in rs if r['seed']==s) for s in sorted({r['seed'] for r in rs})};families={f:sum(r['correct'] for r in rs if r['context']==f) for f in ('release','incident')};pos=[r for r in rs if r['truth']=='ship'];false_releases=sum(r['action']=='ship' and r['truth']=='hold' for r in rs);correct=sum(r['correct'] for r in rs);contracts=sum(r['valid_response'] for r in rs)
  passed=arm_calls[arm]==192 and contracts==192 and correct>=189 and min(worlds.values())>=31 and min(families.values())>=92 and sum(r['correct'] for r in pos)>=23 and false_releases==0 and not any(r['context']=='incident' and r['truth']=='none' and r['action'] not in (None,'none') for r in rs) and not mismatches and not requests and not unknown and not provider_errors
  arms[arm]={'correct':correct,'assigned':192,'valid_contract_decisions':contracts,'world_correct_out_of_32':worlds,'family_correct_out_of_96':families,'valid_release_correct':sum(r['correct'] for r in pos),'valid_release_assigned':24,'false_releases':false_releases,'incident_false_activation':sum(r['context']=='incident' and r['truth']=='none' and r['action'] not in (None,'none') for r in rs),'calls':arm_calls[arm],'actual_model_usd':arm_cost[arm],'qualified':passed}
 diffs={s:(arms['F']['world_correct_out_of_32'][s]-arms['E']['world_correct_out_of_32'][s])/32 for s in arms['E']['world_correct_out_of_32']};gain=sum(diffs.values())/6
 candidate=('E' if arms['E']['actual_model_usd']<=arms['F']['actual_model_usd'] else 'F') if all(a['qualified'] for a in arms.values()) else next((k for k,v in arms.items() if v['qualified']),None)
 paired=[]
 for arm in ('E','F'):
  groups=collections.defaultdict(list)
  for r in rows:
   if r['arm']==arm:groups[(r['seed'],r['context'],r['id'])].append(r)
  for key,rs in groups.items():paired.append({'arm':arm,'seed':key[0],'context':key[1],'id':key[2],'strict_successes_out_of_2':sum(r['correct'] for r in rs),'actions':{r['order']+'-'+str(r['repeat']):r['action'] for r in rs},'order_effect_interpretable':False})
 summary={'evidence_type':manifest.get('evidence_type'),'assigned_calls':384,'started_calls':started,'terminal_calls':completed,'assigned_decisions':384,'scored_decisions':len(rows),'actual_model_usd':cost,'usage_unknown_calls':unknown,'provider_errors':provider_errors,'audit_disagreements':mismatches,'request_mismatches':requests,'arms':arms,'world_F_minus_E':diffs,'mean_F_minus_E':gain,'material_repair_advantage':gain>=.03 and sum(v>0 for v in diffs.values())>=4,'candidate_executor':candidate,'independent_worlds':6,'distinct_case_family_pairs':96,'paired_cases':paired}
 (root/'summary.json').write_text(json.dumps(summary,indent=2))
 with (root/'decisions.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 # Lightweight complete evidence view, static and reproducible; no visualization RNG.
 label='SCRIPTED — NOT MODEL EVIDENCE' if manifest.get('evidence_type')!='measured_model_outputs' else 'Measured R1 model outputs'
 headings=['assignment','id','source','position','truth','action','correct','valid_response','terminal']
 table=''.join('<tr>'+''.join('<td>'+html.escape(str(r[k]))+'</td>' for k in headings)+'</tr>' for r in rows)
 (root/'replay.html').write_text('<!doctype html><meta charset="utf-8"><title>Theseus R1 evidence</title><style>body{font:15px system-ui;margin:30px}td,th{padding:5px;border-bottom:1px solid #ccc}th{position:sticky;top:0;background:white}</style><h1>'+label+'</h1><p>Six worlds. 96 distinct case/family pairs; repeated assignments are dependent. Truth is evaluator-only. False terminal means unstarted or unresolved, not a measured wrong answer.</p><pre>'+html.escape(json.dumps({k:v for k,v in summary.items() if k!='paired_cases'},indent=2))+'</pre><table><tr>'+''.join('<th>'+k+'</th>' for k in headings)+'</tr>'+table+'</table>')
 return summary
if __name__=='__main__':
 import sys
 s=summarize(sys.argv[1]);print(json.dumps({k:v for k,v in s.items() if k not in ('paired_cases',)}))
