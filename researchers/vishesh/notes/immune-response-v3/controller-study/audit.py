import sys,json,copy,hashlib,sqlite3
from pathlib import Path
base=Path(__file__).resolve().parent;sys.path.insert(0,str(base));import cases,controller,native_provider
out=Path(sys.argv[1]);rows=[json.loads(s) for s in (out/'episodes.jsonl').read_text().splitlines()];events=[json.loads(s) for s in (out/'events.jsonl').read_text().splitlines()];transport=[json.loads(s) for s in (out/'transport.jsonl').read_text().splitlines()];usage=[json.loads(s) for s in (out/'usage.jsonl').read_text().splitlines()];reqs=[x for x in transport if x['kind']=='request'];responses=[x for x in transport if x['kind']=='response'];assert len(reqs)==len(responses)==len(usage)==4*len(rows)
for q,r,u in zip(reqs,responses,usage):
 assert q['request_id']==r['request_id']==u['request_id'];assert q['request_hash']==u['request_hash']==hashlib.sha256(json.dumps(q['body']).encode()).hexdigest();assert r['body']['usage']['cost']==u['actual_usd'];assert u['state']=='response_received'
validations=0
for row in rows:
 c=row['case'];state=copy.deepcopy(c['initial']);history=[];trace=[]
 for x in row['trace']:
  o=cases.observe(c,state,x['tick'],history,cases.advice(c,row['condition']));assert o==x['observation'];controller.validate_diagnosis(o,x['diagnosis']);assert x['diagnosis_correct']==(x['diagnosis']==cases.diagnosis(o));a=cases.f.controller.decode(c['fixture'],x['raw_response']);assert a==x['action'];frame=cases.f.step(c['fixture'],state,a)
  for k,v in frame.items():assert x[k]==v,(c['kind'],k)
  trace.append(frame);history.append({'action':a,'result':frame['result']});validations+=1
 assert cases.gate(c,trace)==row['outcome_pass'];assert all(x['diagnosis_correct'] for x in row['trace'])==row['diagnosis_pass'];assert row['qualified']==(row['outcome_pass'] and row['diagnosis_pass'])
responses_iter=iter(responses);requests_iter=iter(reqs)
for e in events:
 if e['kind'] not in ('diagnosis_response','action_response'):continue
 q=next(requests_iter);r=next(responses_iter);model=native_provider.MODELS[0 if e['model']=='sonnet' else 1];assert native_provider.wire(e['request'],model)==q['body'];assert json.loads(r['body']['choices'][0]['message']['content'])==e['response']
summary={'episodes':len(rows),'requests_reconciled':len(reqs),'frames_replayed':validations,'actual_usd':sum(x['actual_usd'] for x in usage),'reserved_usd':sum(x['reserved_usd'] for x in usage),'diagnosis_correct':sum(x['diagnosis_correct'] for r in rows for x in r['trace']),'outcome_pass':sum(r['outcome_pass'] for r in rows),'qualified':sum(r['qualified'] for r in rows),'cases':[{'model':r['model'],'split':r['split'],'kind':r['case']['kind'],'condition':r['condition'],'outcome':r['outcome_pass'],'diagnosis':r['diagnosis_pass'],'healthy_ticks':sum(x['healthy'] for x in r['trace']),'restarts':sum(x['useful_restart'] for x in r['trace'])} for r in rows]}
(out.parent/'audit.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
