#!/usr/bin/env python3
"""Prepare Q0 offline; admitted run API consumes an authorized credential supplier."""
import argparse,json,os,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent;sys.path.insert(0,str(BASE/'src'))
from contract import digest
from qualification import assignments,cases,grade,summarize
from native import NativeActor,DecisionTransport,StopDispatch
from q0_ledger import Ledger,PRIOR_NANO,PREDECESSOR
from q0_admission import Admission,fingerprint

def prepare():
 return dict(scope='pc9-q0-a1',stage='Q0',assignments=assignments(),assignments_sha256=digest(assignments()),instrument=fingerprint(),max_calls=8,max_questions=40,exact_questions=38,prior_exposure_nano=PRIOR_NANO,predecessor_sha256=PREDECESSOR,native_calls=0,admission='not granted',owner_scope_approved=False)

def execute(rows,actor,out):
 records=[]
 for case in rows:
  try:decision=actor(case['packet'])
  except StopDispatch:
   records.extend(dict(id=c['id'],kind=c['kind'],status='unstarted') for c in rows[len(records):]);break
  if decision is None:r=dict(id=case['id'],kind=case['kind'],status=actor.records[-1]['status'],trace_id=actor.records[-1]['id'])
  else:r=dict(id=case['id'],kind=case['kind'],status='valid',decision=decision,grade=grade(case,decision),trace_id=actor.records[-1]['id'])
  records.append(r)
  (out/'records.json').write_text(json.dumps(records,indent=2)+'\n')
 (out/'records.json').write_text(json.dumps(records,indent=2)+'\n');result=summarize(records);result['budget']=actor.ledger.summary();(out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');return result

def run_q0(config,credential_supplier,public_check):
 """Only live entry point; private operations bootstrap supplies these arguments.

 public_check is the shared public_plan.check; credential_supplier is the approved
 local memory consumer/relay. This API has no env/default-file credential fallback.
 """
 admission=Admission(config,public_check)
 transport=DecisionTransport(credential_supplier);route=transport.verify_route()
 ledger=Ledger(config['ledger_path'],config['predecessor_path'])
 try:
  ledger.claim();out=Path(config['output']);out.mkdir(parents=True,exist_ok=False)
  (out/'public-plan.json').write_text(json.dumps(admission.public,indent=2)+'\n');(out/'route.json').write_text(json.dumps(route,indent=2)+'\n')
  (out/'provenance.json').write_text(json.dumps(dict(source_commit=config['source_commit'],instrument=fingerprint()),indent=2)+'\n')
  rows=cases('Q0',admission);(out/'cases.json').write_text(json.dumps(rows,indent=2)+'\n')
  with (out/'events.jsonl').open('x') as events:
   def sink(row):
    events.write(json.dumps(row,sort_keys=True)+'\n');events.flush();os.fsync(events.fileno())
   actor=NativeActor(transport,ledger,admission,sink,'pc9-q0-a1')
   try:result=execute(rows,actor,out)
   finally:(out/'traces.json').write_text(json.dumps(actor.records,indent=2)+'\n')
  return result
 finally:ledger.db.close()

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('operation',choices=['prepare']);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 with a.output.open('x') as f:json.dump(prepare(),f,indent=2)
 print('Assignments prepared; reserved packets unopened; no launch admitted or model calls.')

def audit_saved(path):
 """Offline recomputation; does not open new reserved cases or trust saved grades."""
 from native import checked,wire
 from policies import exact,posterior,action_risk
 p=Path(path);rows=json.loads((p/'cases.json').read_text());rs=json.loads((p/'records.json').read_text());traces=json.loads((p/'traces.json').read_text());trace={r['id']:r for r in traces}
 if len(rows)!=8 or [r['id'] for r in rs]!=[r['id'] for r in rows]:raise ValueError('assignment_reconciliation')
 fresh=[]
 for case,r in zip(rows,rs):
  packet=case['packet'];expect=exact(packet)['map'];accepted=[]
  if packet['remaining_inspections']:
   order=packet['tie_order'];q=posterior(packet);qs=tuple(q[s] for s in order);values=[action_risk(qs,packet['remaining_inspections'],i) for i in range(4)];accepted=[s for s,v in zip(order,values) if abs(v-min(values))<1e-12]
  if expect!=case['expected_map'] or accepted!=case['accepted_inspections'] or digest(packet)!=case['packet_sha256']:raise ValueError('case_scoring')
  if r['status']=='unstarted':fresh.append(r);continue
  t=trace[r['trace_id']]
  if t['request']!=wire(packet) or digest(t['request'])!=t['request_sha256'] or t['status']!=r['status']:raise ValueError('trace_binding')
  if r['status']=='valid':
   c=t['checked'];raw=dict(model=c['model'],provider=c['provider'],answers=c['safe_answers'],usage=c['usage']);verified=checked(raw,t['request'])
   if verified['decision']!=r['decision'] or grade(case,r['decision'])!=r['grade']:raise ValueError('grade')
  fresh.append(r)
 s=summarize(fresh);saved=json.loads((p/'summary.json').read_text())
 if any(saved[k]!=v for k,v in s.items()):raise ValueError('summary')
 if len(trace)!=len(traces) or len(trace)!=sum(r['status']!='unstarted' for r in rs):raise ValueError('extra_or_missing_trace')
 return dict(verified=True,assigned=8,terminal=len(trace),native_qualification_passed=s['qualification_passed'],scope='saved typed outputs and deterministic scoring; not independent provider receipt verification')
