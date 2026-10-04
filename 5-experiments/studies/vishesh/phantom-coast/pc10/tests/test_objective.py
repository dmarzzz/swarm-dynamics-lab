import sys,json,copy,unittest
from pathlib import Path
B=Path(__file__).resolve().parents[1];sys.path.insert(0,str(B))
from instrument import paired,audit,score,prepare,NEW,enumerate_action
from policies import exact
class Objective(unittest.TestCase):
 def test_pair_evidence_and_arithmetic(self):self.assertTrue(audit(paired())['verified'])
 def test_report_signs_and_regret(self):
  a=audit(paired())['diagnostics']
  for i in (1,2):self.assertAlmostEqual(min(a[i]['mean_expected_losses']),.1125);self.assertAlmostEqual(max(a[i]['mean_expected_losses']),.125)
 def test_counterbalanced_and_envelope(self):
  ps=paired();self.assertEqual(sum(p['order'][0]=='legacy' for p in ps),4);self.assertEqual(sum(len(v['request']['questions']) for p in ps for v in p['variants'].values()),76)
 def test_reserved_requires_admission(self):
  with self.assertRaises(ValueError):paired('Q1')
  self.assertEqual(prepare()['native_calls'],0);self.assertNotIn('packet',json.dumps(prepare()))
 def test_no_reuse_of_released_ids(self):
  old=json.loads((B.parent/'pc9/results/Q0-A1/cases.json').read_text());oldsites={s for c in old for s in c['packet']['sites']}
  self.assertFalse(oldsites & {s for p in paired() for s in p['case']['packet']['sites']})
 def test_gate_and_missingness(self):
  ps=paired();rs=[dict(id=p['case']['id'],condition=c,status='valid',decision=exact(p['variants'][c]['packet'])) for p in ps for c in ('legacy','clarified')]
  self.assertTrue(score(ps,rs)['clarified_gate_passed']);rs[3]={'id':rs[3]['id'],'condition':rs[3]['condition'],'status':'unstarted'};r=score(ps,rs);self.assertFalse(r['clarified_gate_passed']);self.assertIsNone(r['optimal_count_difference'])
  with self.assertRaises(ValueError):score(ps,rs[:-1])
 def test_packet_tamper_rejected(self):
  ps=paired();ps[1]['variants']['clarified']['packet']['private_reports'][0]['label']='WATER'
  with self.assertRaises(AssertionError):audit(ps)
 def test_renaming_and_order_invariance(self):
  p=paired()[1]['case']['packet'];a=exact(p);q=copy.deepcopy(p);rename={s:'renamed-'+str(i) for i,s in enumerate(p['sites'])};q['sites']=[rename[s] for s in reversed(p['sites'])];q['tie_order']=[rename[s] for s in p['tie_order']]
  for r in q['private_reports']:r['site']=rename[r['site']]
  b=exact(q);self.assertEqual(b['inspect'],rename[a['inspect']]);self.assertEqual(b['map'],{rename[s]:v for s,v in a['map'].items()})
 def test_clarification_defines_control_not_answer(self):
  self.assertIn('you alone control',NEW);self.assertIn('own four-location map only',NEW);self.assertIn('No additional private reports or peer maps',NEW);self.assertNotIn('.1125',NEW);self.assertNotIn('inspect an unknown',NEW)
if __name__=='__main__':unittest.main()

class Executor(unittest.TestCase):
 def test_partial_pairs_retained(self):
  import tempfile
  from runner import execute
  from native import NativeActor
  class Admission:
   def current(self):return True
  class Ledger:
   def reserve(self,*a):pass
   def finish(self,*a):pass
   def summary(self):return {}
  actor=NativeActor(lambda req:None,Ledger(),Admission(),lambda row:None,'test')
  with tempfile.TemporaryDirectory() as td:
   summary=execute(paired(),actor,Path(td));rows=json.loads((Path(td)/'records.json').read_text());self.assertEqual(len(rows),16);self.assertEqual(sum(r['status']=='unstarted' for r in rows),14);self.assertFalse(summary['clarified_gate_passed'])
 def test_ledger_cumulative_cap_and_duplicate(self):
  import tempfile,hashlib
  from unittest.mock import patch
  from ledger import Ledger
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);prior=p/'prior';prior.write_bytes(b'test predecessor')
   with patch('ledger.PREDECESSOR',hashlib.sha256(prior.read_bytes()).hexdigest()):
    l=Ledger(p/'ledger',prior);l.claim()
    with self.assertRaises(Exception):l.claim()
    for i in range(16):l.reserve(str(i),6720000);l.finish(str(i),None)
    with self.assertRaises(ValueError):l.reserve('extra',1)
    self.assertEqual(l.summary()['cumulative_exposure_nano'],966341754);l.db.close()

class AdmissionBoundary(unittest.TestCase):
 def test_incomplete_configuration_does_not_dispatch(self):
  from runner import run
  with self.assertRaises(ValueError):run({},None,lambda *a:self.fail('No public call expected'))

class SavedAudit(unittest.TestCase):
 def test_mock_roundtrip_and_tampered_decision(self):
  import tempfile
  from runner import execute,audit_saved
  from native import NativeActor,SNAPSHOT
  class A:
   def current(self):return True
  class L:
   def reserve(self,*a):pass
   def finish(self,*a):pass
   def summary(self):return {}
  def provider(req):
   d=exact(req['state']);ans={}
   for k,q in req['questions'].items():
    v=d['inspect'] if k=='inspect' else d['map'][k[4:]];ans[k]=dict(type='choice',choice=v,probabilities={x:float(x==v) for x in q['criteria']},confidence=1.)
   return dict(model=SNAPSHOT,provider='TypeSafe',answers=ans,usage=dict(cost=.000001,input_tokens=10,output_tokens=0))
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);rows=paired();actor=NativeActor(provider,L(),A(),lambda r:None,'test');s=execute(rows,actor,p);(p/'cases.json').write_text(json.dumps(rows));(p/'traces.json').write_text(json.dumps(actor.records));self.assertTrue(audit_saved(p)['verified']);self.assertEqual(s['optimal_count_difference'],0)
   rs=json.loads((p/'records.json').read_text());site=next(iter(rs[0]['decision']['map']));rs[0]['decision']['map'][site]='LAND';(p/'records.json').write_text(json.dumps(rs))
   with self.assertRaises(ValueError):audit_saved(p)

class PublicPlan(unittest.TestCase):
 def test_shared_registration_contract(self):
  sys.path.insert(0,str(B.parent.parent/'experiment-documentation'))
  from public_plan import validate
  url='https://github.com/dmarzzz/swarm-lab/blob/'+('a'*40)+'/researchers/vishesh/notes/phantom-coast/pc10/PLAN.md'
  receipt=validate({'id':'phantom-coast-pc10','url':url,'description':'TLDR: paired individual-control wording diagnostic'},(B/'PLAN.md').read_text(),'TLDR: sixteen paired calls; frozen objective diagnostic, not population poisoning evidence.')
  self.assertEqual(receipt['experiment'],'phantom-coast-pc10')
