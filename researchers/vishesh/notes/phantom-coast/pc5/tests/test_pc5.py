import unittest,tempfile,json,sys,copy,sqlite3
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from contract import development_world,packet,score
from design import schedule,qualified,grade,contrasts
from wire import request,reservation,validate
from engine import Engine
from ledger import Ledger

def raw(req):
 q=req['questions']['target'];choice=next(iter(q['criteria']));return dict(model='typesafe/jev-1.13-20260917',provider='TypeSafe',answers={'target':dict(type='choice',choice=choice,confidence=1,probabilities={c:float(c==choice) for c in q['criteria']})},usage=dict(input_tokens=100,output_tokens=0,cost=.0000042))
class Tests(unittest.TestCase):
 def test_scoring_and_missing(self):
  w=development_world(1600)
  for p,optimal,wrong,regret in [(.8,w['unknown_cell'],w['report_cell'],.05),(.2,w['report_cell'],w['unknown_cell'],.55)]:
   self.assertTrue(score(w,p,optimal)['optimal']);self.assertEqual(score(w,p,optimal)['expected_regret'],0);self.assertEqual(score(w,p,wrong)['expected_regret'],regret);self.assertGreater(score(w,p,None)['expected_loss'],score(w,p,wrong)['expected_loss'])
 def test_disclosure_only(self):
  for seed in range(1600,1608):
   w=development_world(seed)
   for p in (.8,.2):
    a=packet(w,p,'legacy');b=packet(w,p,'explicit');a.pop('task');b.pop('task');self.assertEqual(a,b);self.assertEqual(len(a['evidence']['observations']),35);self.assertEqual(len(set(a['legal_cells'])),2)
    self.assertFalse(any(x in json.dumps(a) for x in ('truth_draw','optimal','seed','expected_regret')))
 def test_calibration_coupling(self):
  w=development_world(1600)
  for draw,expected in [(0.1,(False,False)),(.5,(False,True)),(.9,(True,True))]:
   w['truth_draw']=draw;self.assertEqual(tuple(score(w,p,None)['report_actually_false'] for p in (.8,.2)),expected)
 def test_assignment_counts(self):
  self.assertEqual(len(schedule('Q0')),12);self.assertEqual(len(schedule('S1')),128);self.assertEqual(len({x['id'] for x in schedule('S1')}),128)
 def test_choice_wire_and_reservation(self):
  req=request(packet(development_world(1600),.8,'explicit'),'choice');self.assertEqual(reservation(req),1344000);self.assertIn(validate(raw(req),req)['result']['choice'],req['questions']['target']['criteria'])
 def test_qualification_engine(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);l=Ledger(d/'l','a'*64);e=Engine('Q0','test',d/'out',l,raw,{s:development_world(s) for s in range(1600,1604)});s=e.run();self.assertTrue(s['qualification_passed']);self.assertEqual(s['correct_targets'],12);l.db.close()
 def test_main_engine_and_failed_denominators(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);l=Ledger(d/'l','a'*64);e=Engine('S1','test',d/'out',l,raw,{1600:development_world(1600),1601:development_world(1601)});s=e.run();self.assertEqual(s['assigned'],8);self.assertEqual(s['valid'],8);rows=json.loads((d/'out/decisions.json').read_text());self.assertEqual(sum(x['assigned'] for x in s['cells']),8);l.db.close()
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);l=Ledger(d/'l','a'*64)
   def fail(req):raise TimeoutError()
   e=Engine('S1','test',d/'out',l,fail,{1600:development_world(1600),1601:development_world(1601)});s=e.run();self.assertEqual(s['started'],5);self.assertEqual(s['assigned'],8);self.assertEqual(sum(x['no_inspection'] for x in s['cells']),8);self.assertFalse(s['overall']['practical_success']);l.db.close()
 def test_budget_and_duplicates(self):
  with tempfile.TemporaryDirectory() as d:
   l=Ledger(Path(d)/'l','a'*64);self.assertEqual(l.summary()['prior_usd'],.83914929)
   for i in range(140):l.reserve(str(i),1344000);l.finish(str(i))
   self.assertAlmostEqual(l.summary()['cumulative_exposure_usd'],1.02730929)
   with self.assertRaises(ValueError):l.reserve('extra',1344000)
   l.db.close()
 def test_dev_partition(self):
  for seed in (1000,1400,1800,1900):
   with self.assertRaises(ValueError):development_world(seed)
if __name__=='__main__':unittest.main()
