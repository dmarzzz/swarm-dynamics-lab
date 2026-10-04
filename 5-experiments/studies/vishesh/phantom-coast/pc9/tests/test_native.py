import copy,hashlib,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
B=Path(__file__).resolve().parents[1];sys.path.insert(0,str(B/'src'));sys.path.insert(0,str(B))
from qualification import cases,assignments,grade,summarize
from policies import exact
from native import NativeActor,checked,wire,StopDispatch,SNAPSHOT
from q0_ledger import Ledger
from q0_admission import Admission
from q0 import prepare,execute,audit_saved
from scenario_fixtures import fixture
class Current:
 def current(self):return True
class Meter:
 def __init__(self):self.calls={}
 def reserve(self,i,n):
  if i in self.calls:raise ValueError('duplicate')
  self.calls[i]=dict(reserved=n,actual=None)
 def finish(self,i,n):self.calls[i]['actual']=n
 def summary(self):return copy.deepcopy(self.calls)
def provider(req):
 d=exact(req['state']);answers={}
 for k,q in req['questions'].items():
  v=d['inspect'] if k=='inspect' else d['map'][k[4:]];answers[k]=dict(type='choice',choice=v,probabilities={label:float(label==v) for label in q['criteria']},confidence=1.)
 return dict(model=SNAPSHOT,provider='TypeSafe',answers=answers,usage=dict(cost=.000001,input_tokens=10,output_tokens=0),ignored='never retained')
class Native(unittest.TestCase):
 def test_prepare_does_not_materialize_reserved_packets(self):
  p=prepare();self.assertEqual(p['native_calls'],0);self.assertNotIn('packet',json.dumps(p));self.assertFalse(p['owner_scope_approved'])
  with self.assertRaises(ValueError):cases('Q0')
 def test_reachable_histories_only(self):
  for c in cases():
   p=c['packet'];self.assertEqual(len(p['observations']),p['time']);self.assertEqual(len(p['own_maps']),p['time']);self.assertTrue(all(r['time']<=p['time'] for r in p['observations']));self.assertEqual(grade(c,exact(p))['map_correct'],4)
 def test_all_optimal_ties_accepted(self):
  c=cases()[0];self.assertEqual(len(c['accepted_inspections']),4)
  for s in c['accepted_inspections']:
   d=exact(c['packet']);d['inspect']=s;self.assertTrue(grade(c,d)['inspection_correct'])
 def test_correction_after_consensus(self):
  c=cases()[6];p=c['packet'];target=p['observations'][-1]['site'];truth=p['observations'][-1]['label'];peers=[s['map'][target] for s in p['peer_slots'] if s['status']=='valid'];self.assertTrue(all(v!=truth and v!='UNKNOWN' for v in peers));self.assertEqual(c['expected_map'][target],truth)
 def test_missing_evidence_not_gold_guess(self):
  c=cases()[7];self.assertEqual(sum(v=='UNKNOWN' for v in c['expected_map'].values()),3);self.assertEqual(len({r['site'] for r in c['packet']['observations']}),1)
 def test_exact_question_envelope(self):
  self.assertEqual(sum(len(wire(c['packet'])['questions']) for c in cases()),38);self.assertEqual(sum(x['questions'] for x in assignments()),38)
 def test_safe_response_filter_and_route(self):
  req=wire(cases()[0]['packet']);raw=provider(req);good=checked(raw,req);self.assertNotIn('ignored',json.dumps(good));self.assertEqual(good['decision'],exact(req['state']));raw['provider']='other'
  with self.assertRaises(ValueError):checked(raw,req)
 def test_invalid_probabilities_cost_and_nan(self):
  req=wire(cases()[0]['packet'])
  for field in ('cost','probabilities','confidence'):
   raw=provider(req)
   if field=='cost':raw['usage']['cost']=float('nan')
   elif field=='probabilities':next(iter(raw['answers'].values()))['probabilities']={'UNKNOWN':1}
   else:next(iter(raw['answers'].values()))['confidence']=True
   with self.assertRaises(ValueError):checked(raw,req)
 def test_stops_after_two_failures_and_retains_reservations(self):
  trace=[];m=Meter()
  def fail(_):raise ValueError('DO_NOT_LOG_THIS_BODY')
  actor=NativeActor(fail,m,Current(),trace.append,'test')
  p=cases()[0]['packet'];self.assertIsNone(actor(p));self.assertIsNone(actor(p))
  with self.assertRaises(StopDispatch):actor(p)
  self.assertEqual(len(m.calls),2);self.assertTrue(all(r['actual'] is None for r in m.calls.values()));self.assertNotIn('DO_NOT_LOG',json.dumps(trace))
 def test_expired_admission_dispatches_nothing(self):
  class Expired:
   def current(self):return False
  m=Meter();actor=NativeActor(provider,m,Expired(),lambda r:None,'test')
  with self.assertRaises(StopDispatch):actor(cases()[0]['packet'])
  self.assertFalse(m.calls)
 def test_complete_mock_qualification_and_failed_gate(self):
  m=Meter();actor=NativeActor(provider,m,Current(),lambda r:None,'test')
  with tempfile.TemporaryDirectory() as td:
   summary=execute(cases(),actor,Path(td));self.assertTrue(summary['qualification_passed']);self.assertEqual(summary['inspection_correct'],6)
   rs=json.loads((Path(td)/'records.json').read_text());rs[0]['grade']['map_correct']=3;self.assertFalse(summarize(rs)['qualification_passed'])
 def test_saved_audit_recomputes_and_rejects_tampering(self):
  rows=cases();actor=NativeActor(provider,Meter(),Current(),lambda r:None,'test')
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);execute(rows,actor,p);(p/'cases.json').write_text(json.dumps(rows));(p/'traces.json').write_text(json.dumps(actor.records));self.assertTrue(audit_saved(p)['verified'])
   rs=json.loads((p/'records.json').read_text());rs[0]['grade']['map_correct']=3;(p/'records.json').write_text(json.dumps(rs))
   with self.assertRaisesRegex(ValueError,'grade'):audit_saved(p)
 def test_reserve_and_durable_start_precede_transport(self):
  m=Meter();events=[]
  def call(req):
   self.assertEqual(len(m.calls),1);self.assertEqual(events[0]['status'],'started');return provider(req)
  actor=NativeActor(call,m,Current(),events.append,'test');actor(cases()[0]['packet']);self.assertEqual(events[-1]['status'],'valid')
 def test_unstarted_cases_remain_assigned(self):
  actor=NativeActor(lambda r:None,Meter(),Current(),lambda r:None,'test')
  with tempfile.TemporaryDirectory() as td:
   s=execute(cases(),actor,Path(td));rs=json.loads((Path(td)/'records.json').read_text());self.assertEqual(s['assigned'],8);self.assertEqual(sum(r['status']=='unstarted' for r in rs),6);self.assertFalse(s['qualification_passed'])
 def test_ledger_lineage_duplicate_and_cap(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);prior=p/'prior';prior.write_bytes(b'offline test lineage')
   with self.assertRaises(ValueError):Ledger(p/'wrong.sqlite',prior)
   with patch('q0_ledger.PREDECESSOR',hashlib.sha256(prior.read_bytes()).hexdigest()):
    ledger=Ledger(p/'meter.sqlite',prior)
    with self.assertRaises(ValueError):ledger.reserve('unclaimed',1)
    ledger.claim()
    with self.assertRaises(Exception):ledger.claim()
    for i in range(8):ledger.reserve(str(i),6720000);ledger.finish(str(i),None)
    with self.assertRaises(ValueError):ledger.reserve('ninth',1)
    self.assertEqual(ledger.summary()['cumulative_exposure_nano'],912088842);ledger.db.close()
 def test_missing_scope_is_not_admission(self):
  with self.assertRaises(ValueError):Admission({},lambda *a: self.fail('public checker must not run'))
 def test_added_scenarios_have_distinct_witnesses(self):
  correction=fixture('consensus-correction');gap=fixture('missing-evidence');positive=fixture('false-positive')
  self.assertEqual(positive['episodes'][0]['world']['truth']['Moor'],'WATER')
  for e in correction['episodes']:self.assertEqual(e['summary']['timeline'][-1]['after_target_receipt']['wrong'],0);self.assertEqual(e['summary']['first_target_inspection'],2)
  for e in gap['episodes']:self.assertEqual(e['summary']['unique_coverage'],1);self.assertEqual(e['summary']['repeat_slots'],1)

if __name__=='__main__':unittest.main()
