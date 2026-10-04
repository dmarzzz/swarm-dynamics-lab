"""PC10 paired native executor; private operator supplies verified admission/transport."""
import json,os,time
from pathlib import Path
from instrument import paired,score,fingerprints
from contract import digest
from native import NativeActor,StopDispatch
from ledger import Ledger
from admission import Admission

def execute(rows,actor,out):
 records=[];stopped=False
 for p in rows:
  for condition in p['order']:
   r=dict(id=p['case']['id'],condition=condition,status='unstarted')
   if not stopped:
    try:d=actor(p['variants'][condition]['packet'])
    except StopDispatch:stopped=True
    else:
     r['trace_id']=actor.records[-1]['id'];r['status']=actor.records[-1]['status']
     if d is not None:r['decision']=d
   records.append(r);(out/'records.json').write_text(json.dumps(records,indent=2)+'\n')
 summary=score(rows,records);summary['budget']=actor.ledger.summary();(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');return summary

def run(config,transport,public_check):
 """No credential discovery. Admission must validate actual evidence before this call.

 Scope/source/public/runtime/account/ledger validation is the owning operator's
 responsibility; the artifact returned by prepare is explicitly not admission.
 This function is not exposed as a runnable CLI.
 """
 admission=Admission(config,public_check)
 transport.verify_route()
 if config.get('scope')!='pc10-q1-a1' or config.get('admitted') is not True or not admission.current():raise ValueError('not_admitted')
 if config.get('source_hashes')!=fingerprints():raise ValueError('source_drift')
 ledger=Ledger(config['ledger_path'],config['predecessor_path'])
 try:
  ledger.claim();out=Path(config['output']);out.mkdir(parents=True,exist_ok=False)
  rows=paired('Q1',admission);(out/'cases.json').write_text(json.dumps(rows,indent=2)+'\n');(out/'source.json').write_text(json.dumps(fingerprints(),indent=2)+'\n')
  with (out/'events.jsonl').open('x') as events:
   def sink(row):events.write(json.dumps(row,sort_keys=True)+'\n');events.flush();os.fsync(events.fileno())
   actor=NativeActor(transport,ledger,admission,sink,'pc10-q1-a1')
   try:return execute(rows,actor,out)
   finally:(out/'traces.json').write_text(json.dumps(actor.records,indent=2)+'\n')
 finally:ledger.db.close()


def audit_saved(path):
 from native import wire,checked
 from instrument import audit
 p=Path(path);rows=json.loads((p/'cases.json').read_text());audit(rows)
 records=json.loads((p/'records.json').read_text());traces=json.loads((p/'traces.json').read_text());byid={r['id']:r for r in traces}
 packets={(r['case']['id'],c):r['variants'][c]['packet'] for r in rows for c in ('legacy','clarified')};used=[]
 for r in records:
  if r['status']=='unstarted':continue
  t=byid[r['trace_id']];used.append(t['id']);req=wire(packets[r['id'],r['condition']])
  if t['request']!=req or t['request_sha256']!=digest(req) or t['status']!=r['status']:raise ValueError('trace_binding')
  if r['status']=='valid':
   c=t['checked'];verified=checked(dict(model=c['model'],provider=c['provider'],answers=c['safe_answers'],usage=c['usage']),req)
   if verified['decision']!=r['decision']:raise ValueError('decision_binding')
 if len(set(used))!=len(used) or set(used)!=set(byid) or len(byid)!=len(traces):raise ValueError('trace_reconciliation')
 s=score(rows,records);saved=json.loads((p/'summary.json').read_text())
 if any(saved[k]!=v for k,v in s.items()):raise ValueError('summary')
 return dict(verified=True,assigned=16,terminal=len(used),scope='safe typed outputs and deterministic scoring, not independent provider receipt verification')
