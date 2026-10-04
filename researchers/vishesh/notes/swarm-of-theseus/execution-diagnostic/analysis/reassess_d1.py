"""Post-hoc saved-evidence audit. No model calls; never overwrite D1 scores."""
import collections, hashlib, json, tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'results/D1';m=json.loads((p/'manifest.json').read_text());s=json.loads((p/'summary.json').read_text())
with tarfile.open(p/'evidence.tar.gz') as archive:
 def read(name):return json.load(archive.extractfile('D1/'+name))
 by_id={x['assignment']:x for x in s['results']};mismatches=[];request_mismatches=[];failures=[];arm_world=collections.defaultdict(collections.Counter);cost=collections.Counter();tokens=collections.Counter();legacy_alias={'correct':0,'assigned':0};truncated=0
 for a in m['assignments']:
  start=read('calls/'+a['id']+'-started.json');raw=read('calls/'+a['id']+'-finished.json');v=raw['value'];saved=by_id[a['id']];ds=v.get('decisions',[]) if isinstance(v,dict) else []
  digest=hashlib.sha256(json.dumps(a['request'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
  if start['request']!=a['request'] or start['request_sha256']!=digest:request_mismatches.append(a['id'])
  commands={'none':'console1/none',**{x:'console1/'+x for x in ('probe','ledger','canary')}} if a['context']=='incident' else ({'ship':'console2/commit-ready','hold':'console2/park-review'} if a['context']=='migration-new' else {'ship':'console1/ship','hold':'console1/hold'})
  notes=a['arm'] in ('A','B','C');valid=raw.get('error') is None and isinstance(v,dict) and set(v)==({'decisions','notebook'} if notes else {'decisions'}) and isinstance(ds,list)
  if notes:valid=valid and isinstance(v.get('notebook'),str) and len(v.get('notebook',''))<=700
  wellformed=isinstance(ds,list) and all(isinstance(x,dict) and set(x)=={'id','command'} and isinstance(x['id'],str) and isinstance(x['command'],str) for x in ds)
  emitted={x['id']:x['command'] for x in ds} if wellformed else {}
  valid=valid and wellformed and len(ds)==len(a['cases']) and len(emitted)==len(ds) and set(emitted)=={c['id'] for c in a['cases']} and all(x in commands.values() for x in emitted.values())
  for case,row in zip(a['cases'],saved['rows']):
   ev=case['evidence'][a['rule'][case['class']]]
   meaning=(a['rule'][case['class']] if ev['signal'] else 'none') if a['context']=='incident' else ('ship' if ev['signal'] and ev['fresh'] else 'hold')
   correct=bool(valid and emitted.get(case['id'])==commands[meaning])
   if correct!=row['correct']:mismatches.append(a['id']+'/'+case['id'])
   arm_world[a['arm']][str(a['seed'])]+=correct
   if a['arm']=='A' and not valid and emitted.get(case['id']) in ('ship','hold'):
    legacy_alias['assigned']+=1;legacy_alias['correct']+=emitted[case['id']]==meaning
   if a['arm']=='D' and not correct:failures.append({'world':a['seed'],'family':'incident' if a['context']=='incident' else 'release','context':a['context'],'case_id':case['id'],'class':case['class'],'governing_source':a['rule'][case['class']],'position':a['cases'].index(case)+1,'truth':meaning,'action':row['action'],'evidence':case['evidence']})
  cost[a['arm']]+=raw['actual_usd'];tokens[a['arm']+'/input']+=raw['usage']['input_tokens'];tokens[a['arm']+'/output']+=raw['usage']['output_tokens'];truncated+=raw.get('stop_reason')=='max_tokens'
 unique=collections.defaultdict(list)
 for f in failures:unique[(f['world'],f['family'],f['case_id'])].append(f['context'])
 # Canonical release + incident gives each task family one vote; retrospective sensitivity only.
 dedup={};ship={}
 for arm in 'ABCDE':
  canonical=[r for result in s['results'] if result['arm']==arm and result['context'] in ('release','incident') for r in result['rows']]
  positives=[r for result in s['results'] if result['arm']==arm and result['context']=='release' for r in result['rows'] if r['truth']=='ship']
  dedup[arm]={'correct':sum(r['correct'] for r in canonical),'assigned':len(canonical)}
  ship[arm]={'correct':sum(r['correct'] for r in positives),'assigned':len(positives)}
 result={'status':'POST-HOC SAVED-EVIDENCE AUDIT; no new model calls','request_hash_mismatches':request_mismatches,'full_strict_score_mismatches':mismatches,'audit_scope':'Same-author independent calculation from raw outputs; not independent researcher review. Includes full response contract, unlike the initial partial-command agreement audit.','D_failures':failures,'D_distinct_failures':[{'world':k[0],'family':k[1],'case_id':k[2],'contexts':v} for k,v in unique.items()],'canonical_family_accuracy':dedup,'canonical_release_ship_recall':ship,'legacy_alias_posthoc':legacy_alias,'model_cost_by_arm':dict(cost),'tokens_by_arm':dict(tokens),'max_tokens_stops':truncated,'world_correct_totals':dict(arm_world),'limitations':['Retrospective analyses do not change the frozen primary score or qualification gate.','Order, canary source and distractor conflict are confounded in the observed release errors.','Fresh calls share a finite Boolean task family; apparent sample count overstates diversity.']}
 (ROOT/'analysis/D1-REASSESSMENT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['full_strict_score_mismatches','request_hash_mismatches','canonical_family_accuracy','canonical_release_ship_recall','max_tokens_stops']}))
