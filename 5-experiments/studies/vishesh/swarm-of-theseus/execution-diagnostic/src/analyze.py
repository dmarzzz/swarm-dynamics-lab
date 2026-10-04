"""All-assigned analysis with independent truth/command decoding; missing stays visible."""
import collections,json
from pathlib import Path
from instrument import score

def reference(a,result):
 value=result.get('value');keys={'decisions','notebook'} if a['arm'] in 'ABC' else {'decisions'};ds=value.get('decisions',[]) if isinstance(value,dict) and set(value)==keys else [];ds=ds if isinstance(ds,list) else []
 out={d.get('id'):d.get('command') for d in ds if isinstance(d,dict) and set(d)=={'id','command'} and isinstance(d.get('id'),str) and isinstance(d.get('command'),str)}
 verdict={}
 for c in a['cases']:
  source=a['rule'][c['class']];signal=c['evidence'][source]['signal'];fresh=c['evidence'][source]['fresh']
  if a['context']=='incident':expected='console1/'+(source if signal else 'none')
  elif a['context']=='migration-new':expected='console2/'+('commit-ready' if signal and fresh else 'park-review')
  else:expected='console1/'+('ship' if signal and fresh else 'hold')
  verdict[c['id']]=out.get(c['id'])==expected
 return verdict

def summarize(root):
 root=Path(root);m=json.loads((root/'manifest.json').read_text());cells=collections.defaultdict(collections.Counter);issues=[];results=[];calls=0;cost=0;usage_missing=0;equiv=collections.defaultdict(list)
 for a in m['assignments']:
  f=root/'calls'/(a['id']+'-finished.json');result=json.loads(f.read_text()) if f.exists() else {'error':'not_completed','value':None}
  calls+=int(f.exists());cost+=result.get('actual_usd') or 0;usage_missing+=int(f.exists() and result.get('actual_usd') is None)
  scored=score(a,result);ref=reference(a,result)
  for r in scored['rows']:
   if r['partial_correct']!=ref[r['id']]:issues.append(a['id']+'/'+r['id'])
   key=f"{a['seed']}/{a['context']}/{a['arm']}";cell=cells[key];cell['assigned']+=1;cell['correct']+=int(r['correct']);cell['observed']+=int(r['observed']);cell['valid_response_decisions']+=int(r['valid_response']);cell['command_valid']+=int(r['command_valid']);cell['recognized_semantic_correct']+=int(r['recognized_semantic_correct']);cell['false_hold']+=int(r['truth']=='ship' and r['action']=='hold');cell['false_ship']+=int(r['truth']=='hold' and r['action']=='ship')
  for c,r in zip(a['cases'],scored['rows']):
   ev=c['evidence'][a['rule'][c['class']]]
   if a['context']=='incident':equiv[(a['seed'],a['context'],a['arm'],c['class'],ev['signal'])].append(r)
  results.append({'assignment':a['id'],'seed':a['seed'],'context':a['context'],'arm':a['arm'],'errors':scored['errors'],'rows':scored['rows']})
 contrasts={}
 for seed in sorted({a['seed'] for a in m['assignments']}):
  for ctx in sorted({a['context'] for a in m['assignments']}):
   for before,after in zip('ABCD','BCDE'):
    x,y=cells[f'{seed}/{ctx}/{before}'],cells[f'{seed}/{ctx}/{after}'];contrasts[f'{seed}/{ctx}/{after}-{before}']=y['correct']/y['assigned']-x['correct']/x['assigned']
 invariance=[{'group':list(k),'assigned':len(rows),'valid_observed':sum(r['observed'] and r['valid_response'] for r in rows),'inconsistent':len({r['action'] for r in rows if r['observed'] and r['valid_response']})>1} for k,rows in equiv.items() if len(rows)>1]
 migration={}
 for seed in sorted({a['seed'] for a in m['assignments']}):
  for arm in 'ABCDE':
   old,new=cells[f'{seed}/migration-old/{arm}'],cells[f'{seed}/migration-new/{arm}']
   migration[f'{seed}/{arm}']={key:new[key]/new['assigned']-old[key]/old['assigned'] for key in ('correct','recognized_semantic_correct','command_valid')}
 candidate={arm:all(c['correct']/c['assigned']>=.9 and c['valid_response_decisions']==c['assigned'] for k,c in cells.items() if k.endswith('/'+arm)) for arm in 'BCDE'}
 return {'status':'measured' if m.get('evidence_type')=='measured_model_outputs' else 'SCRIPTED SOFTWARE FIXTURE, NOT MODEL EVIDENCE','assigned_calls':len(m['assignments']),'completed_call_records':calls,'assigned_decisions':sum(c['assigned'] for c in cells.values()),'cells':dict(cells),'paired_descriptive_contrasts':contrasts,'candidate_for_separate_confirmation':candidate,'migration_new_minus_old':migration,'incident_equivalent_input_groups':invariance,'audit_disagreements':issues,'estimated_actual_usd':cost,'usage_missing':usage_missing,'results':results,'limitation':'Three worlds; no inference from rows as independent samples; no automatic pilot admission.'}
if __name__=='__main__':
 import sys
 root=Path(sys.argv[1]);out=summarize(root);(root/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('results','cells','paired_descriptive_contrasts')}))
