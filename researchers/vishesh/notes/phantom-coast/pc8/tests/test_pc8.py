import sys,json,tempfile,unittest,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from contract import *
from wire import request,validate,reservation
from design import schedule,qualified,grade
from ledger import Ledger
from engine import Engine

def fake(req):
 labels=parser(req['state']);return dict(model='typesafe/jev-1.13-20260917',provider='TypeSafe',answers={k:dict(type='choice',choice=v,probabilities={x:float(x==v) for x in LABELS},confidence=1,debug='SYNTHETIC_SECRET') for k,v in labels.items()},usage=dict(cost=.0000042,input_tokens=100,output_tokens=24),headers={'Authorization':'SYNTHETIC_SECRET'})
class Tests(unittest.TestCase):
 def test_gold_counts_and_parser_development(self):
  for s in range(4000,4008):
   w=development_world(s);gold=ledger_labels(w['records']);self.assertEqual(sum(v!='EXCLUDE' for v in gold.values()),3)
   for rep in ('structured','prose'):self.assertEqual(parser(packet(w,rep)),gold)
 def test_correction_and_provenance(self):
  w=development_world(4001);rs=w['records'];old=next(r for r in rs if r['replaces']);g=ledger_labels(rs);self.assertEqual(g[old['replaces']],'EXCLUDE');self.assertNotEqual(g[old['id']],'EXCLUDE')
  for s in (4000,4002,4003):
   w=development_world(s);gold=ledger_labels(w['records']);self.assertEqual(sum(v=='EXCLUDE' for v in gold.values()),3)
 def test_packets_no_gold(self):
  for s in range(4000,4008):
   w=development_world(s)
   for rep in ('structured','prose'):
    p=packet(w,rep);self.assertEqual(set(p),{'task','cutoff_day','records'});self.assertEqual(len(p['records']),6);self.assertFalse(any(x in p for x in ('seed','family','gold','check_cost','posterior')))
   self.assertEqual([r['id'] for r in packet(w,'structured')['records']],[r['id'] for r in packet(w,'prose')['records']])
 def test_scores_and_controls(self):
  for s in range(4000,4008):
   w=development_world(s);g=ledger_labels(w['records']);o=outcome(w,g);self.assertEqual(o['field_errors'],0);self.assertAlmostEqual(o['first_action_regret'],0);self.assertEqual(o['admitted'],3);self.assertEqual(outcome(w,None)['field_errors'],6)
 def test_assignment_partitions(self):
  self.assertEqual(len(schedule('Q0')),16);self.assertEqual(len(schedule('S1')),48)
  for s in (4100,4200):
   with self.assertRaises(ValueError):development_world(s)
 def test_safe_raw_and_reservation(self):
  req=request(packet(development_world(4000),'prose'));out=validate(fake(req),req);self.assertNotIn('SYNTHETIC_SECRET',str(out));self.assertEqual(len(out['safe_raw_answers']),6);self.assertEqual(reservation(req),8064000)
 def test_qualification_requires_incremental_value(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);l=Ledger(d/'l','a'*64);r=Engine('Q0','test',d/'out',l,fake,{s:development_world(s) for s in range(4000,4008)}).run();self.assertTrue(r['semantic_passed']);self.assertFalse(r['qualification_passed']);self.assertEqual(r['assigned'],16);l.db.close()
 def test_failures_preserve_denominator(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);l=Ledger(d/'l','a'*64)
   def fail(req):raise TimeoutError()
   r=Engine('Q0','test',d/'out',l,fail,{s:development_world(s) for s in range(4000,4008)}).run();self.assertEqual(r['started'],5);self.assertEqual(r['assigned'],16);self.assertFalse(r['qualification_passed']);self.assertEqual(sum(x['native_correct'] for x in r['cells']),0);l.db.close()
 def test_budget_and_duplicates(self):
  with tempfile.TemporaryDirectory() as d:
   l=Ledger(Path(d)/'l','a'*64);l.claim('Q0','a')
   with self.assertRaises(Exception):l.claim('Q0','b')
   for i in range(64):l.reserve(str(i),8064000)
   with self.assertRaises(ValueError):l.reserve('extra',8064000)
   self.assertAlmostEqual(l.summary()['cumulative_exposure_usd'],1.373244138);l.db.close()
 def test_admission_rejects_missing_source(self):
  from admission import Admission
  with self.assertRaises(ValueError):Admission({'design':'PC-8','stage':'Q0','attempt':'q0-a1'},'Q0',lambda *a:None)
if __name__=='__main__':unittest.main()
