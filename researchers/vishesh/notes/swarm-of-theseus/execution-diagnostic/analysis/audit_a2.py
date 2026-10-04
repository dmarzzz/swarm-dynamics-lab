from pathlib import Path
import json,sys,hashlib,collections
root=Path(sys.argv[1]);base=Path(__file__).resolve().parents[1];sys.path.insert(0,str(base/'a2'))
from design import digest,label,candidates,execution_request,d1
from scoring import policy_score,action_score
from openrouter import wire
from analyze import summarize
s=summarize(root);m=json.loads((root/'manifest.json').read_text());learn={};failures=[];learning=[];wire_bad=[];cost=0.;served=collections.Counter();traces=[]
for a in m['assignments']:
 sp=root/'calls'/(a['id']+'-started.json');fp=root/'calls'/(a['id']+'-finished.json')
 if not fp.exists():continue
 st=json.loads(sp.read_text());r=json.loads(fp.read_text());served[(r.get('served_model'),r.get('served_provider'))]+=1;cost+=r.get('actual_usd') or 0
 if st.get('provider_wire_request')!=wire(st['request']) or st.get('provider_wire_sha256')!=digest(st.get('provider_wire_request')):wire_bad.append(a['id'])
 traces.append({'id':a['id'],'request_sha256':hashlib.sha256(sp.read_bytes()).hexdigest(),'response_sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),'model':r.get('served_model'),'provider':r.get('served_provider'),'error':r.get('error')})
 if a['kind']=='learn':
  p=policy_score(a,r);learn[a['id']]=p
  witnesses=[]
  for cls in 'AB':
   asserted=(r.get('value') or {}).get('mapping',{}).get(cls)
   witnesses.extend({'class':cls,'id':h['case']['id'],'observed':h['outcome'],'asserted_source_prediction':label(h['case'],asserted,a['context'])} for h in a['history'] if h['case']['class']==cls and asserted in d1.SOURCES and label(h['case'],asserted,a['context'])!=h['outcome'])
  learning.append({'id':a['id'],'expected':a['rule'],'returned':r['value'],'qualified':p['qualified'],'mapping_valid':p['mapping_valid'],'exact_mapping':p['exact_mapping'],'support_valid':p['support_valid'],'visible_history':a['history'],'compatible_sources':{cls:candidates(a['history'],cls,a['context']) for cls in 'AB'},'contradictions':witnesses})
 else:
  score=action_score(a,r)
  if not score['correct']:
   mapping=a['rule'] if a['arm']=='ceiling' else learn[a['parent']]['mapping'];following=d1.truth(a['cases'][0],a['context'],mapping) if mapping else None
   failures.append({'id':a['id'],'arm':a['arm'],'case':a['cases'][0],'true_policy':a['rule'],'supplied_policy':mapping,'correct_action':score['truth'],'returned_action':score['action'],'action_under_supplied_policy':following,'classification':'policy_induced' if score['action']==following and mapping!=a['rule'] else 'executor_failure','raw_text':r['raw_text'],'valid_response':score['valid_response']})
audit={'cohort':'A2 OpenRouter Anthropic Haiku4.5','source_commit':m['source_commit'],'actor_operator_context_shared':False,'actual_calls':len(traces),'wire_disagreements':wire_bad,'served_routes':[{'model':k[0],'provider':k[1],'count':v} for k,v in served.items()],'cost_sum_usd':cost,'learner_records':learning,'wrong_decisions':failures,'failure_classes':dict(collections.Counter(x['classification'] for x in failures)),'trace_hashes':traces}
(root/'trace-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
lines=['# A2 native trace review','', 'All started request/response pairs were checked for request hashes, provider translation, served route, accounting and raw-text scoring. All twelve learner outputs and every qualification miss are represented below. This is the owning-agent audit; no independent review claimed. Operator prompts and transcripts were excluded.','', '## Learner outputs and visible counterexamples','']
for a in learning:
 lines += ['### '+a['id'],'','Expected '+json.dumps(a['expected'])+'; returned '+json.dumps(a['returned'])+'.','', 'Qualified: '+str(a['qualified'])+'. Compatible sources: '+json.dumps(a['compatible_sources'])+'.','', 'Counterexamples to asserted mapping: '+json.dumps(a['contradictions'])+'.','']
lines+=['## Incorrect executor decisions','']
for a in failures:lines+=['- '+json.dumps(a)]
lines+=['','All-class counts: '+json.dumps(audit['failure_classes'])+'. Citations were checked semantically against visible history; valid IDs alone were not accepted. Returned objects reveal wrong policies, not hidden reasoning.','']
(root/'TRACE-REVIEW.md').write_text('\n'.join(lines))
print(json.dumps({'summary':s,'wrong_classification':audit['failure_classes'],'wire_disagreements':len(wire_bad),'cost_sum':cost,'routes':audit['served_routes']}))
