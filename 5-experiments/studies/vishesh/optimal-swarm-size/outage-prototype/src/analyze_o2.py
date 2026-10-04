"""Offline O2 evidence recomputation; never calls a model or modifies outcomes."""
import json,sys,hashlib
from pathlib import Path
study=Path(__file__).resolve().parents[2];sys.path.insert(0,str(study/'outage-prototype/src'))
from checker import grade
from world import make_case,digest
root=Path(sys.argv[1]);summary=json.loads((root/'summary.json').read_text());rows=[];coverage=[];trace_review=[]
for p in sorted(root.glob('[0-9][0-9]')):
 if not (p/'outcome.json').exists():continue
 r=json.loads((p/'outcome.json').read_text());a=json.loads((p/'assignment.json').read_text());events=[json.loads(l) for l in (p/'trace.jsonl').read_text().splitlines()]
 steps=[e for e in events if e['kind']=='step'];requests=[e for e in events if e['kind']=='request_context'];answers=[e for e in events if e['kind']=='model_response'];decisions={(e['tick'],e['actor']):e['answer'] for e in events if e['kind']=='decision'}
 assert r['case_sha256']==digest(make_case(a['root'],a['changing'],a['replica'],a['service_count']))
 if r['failure'] is None:assert grade(steps[-1]['state'],8)==r['evaluation']
 for e in requests:
  assert hashlib.sha256(e['serialized_request'].encode()).hexdigest()==e['sha256']
  body=json.loads(e['serialized_request']);packet=json.loads(body['messages'][-1]['content']);actor=int(e['call'].split('/')[-1]);assert packet['actor']==actor and packet['max_actions']==a['service_count']//a['n']
  if a['ownership']:assert packet['ownership']['owned_services']==packet['observation']['service_ids'][actor::a['n']]
 for e in answers:
  _,tick,actor=e['call'].rsplit('/',2)
  if (int(tick),int(actor)) in decisions:assert json.loads(e['text'])==decisions[int(tick),int(actor)]
 healthy=[s['tick'] for s in steps if all(s['health'].values())]
 row={k:r.get(k) for k in ['id','label','stage','changing','evaluation','model_calls','elapsed_s','stale_writes','duplicate_patch_targets','ownership_violations','exposure_microdollars','failure']}
 row.update(first_all_healthy_tick=min(healthy) if healthy else None,healthy_service_ticks=sum(sum(s['health'].values()) for s in steps),observed_service_ticks=len(steps)*a['service_count'],tool_operations=r['actions'])
 trace_review.append({'id':r['id'],'rounds':[{'tick':e['tick'],'health':e['health'],'actions':[{'actor':x['actor'],'action':x['action'],'status':x['result']['status']} for x in e['receipts']]} for e in steps]})
 rows.append(row);coverage.append({'id':r['id'],'requests':len(requests),'responses':len(answers),'all_request_hashes_verified':True,'request_ownership_and_capacity_verified':True,'all_visible_decisions_reconciled':len(answers)==len(decisions),'grade_recomputed':r['failure'] is None})
result={'attempt':'outage-o2','execution_source':summary['source_commit'],'planned':summary['planned'],'terminal':len(rows),'unstarted':summary['unstarted'],'stop_reason':summary['stop_reason'],'records':rows,'trace_coverage':coverage,'model_calls':sum(r['model_calls'] for r in rows),'exposure_microdollars':summary['exposure_microdollars'],'claim_scope':'one authored endpoint template with stable/changing variants; descriptive diagnostic, no optimal-N or population inference'}
(root/'trace-review.json').write_text(json.dumps(trace_review,indent=2)+'\n')
(root/'analysis.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
