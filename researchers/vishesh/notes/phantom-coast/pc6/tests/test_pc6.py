import unittest,sys,json,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from contract import development_world,packet,score
from design import schedule,qualified,grade
from ledger import Ledger
from engine import Engine
from wire import request,validate,reservation
class Tests(unittest.TestCase):
 def test_pairing_and_leakage(self):
  for seed in range(2000,2008):
   w=development_world(seed)
   for p in (.8,.2):
    prose=packet(w,p,'prose');table=packet(w,p,'table');rows=table.pop('action_consequences');self.assertEqual(prose,table);self.assertEqual([x['inspect_cell'] for x in rows],prose['legal_cells']);self.assertEqual(len(prose['evidence']['observations']),35)
    for row in rows:self.assertAlmostEqual(row['expected_total_loss'],score(w,p,row['inspect_cell'])['expected_loss'])
    self.assertFalse(any(x in json.dumps(prose) for x in ('truth_draw','optimal','seed','expected_regret')))
 def test_controls(self):
  w=development_world(2000)
  for role,expected in [('report_cell',.025),('unknown_cell',.275)]:self.assertAlmostEqual(sum(score(w,p,w[role])['expected_regret'] for p in (.8,.2))/2,expected)
  self.assertAlmostEqual(sum(max(score(w,p,w[c])['expected_regret'] for c in ('report_cell','unknown_cell')) for p in (.8,.2))/2,.30)
 def test_partition_and_balance(self):
  self.assertEqual(len(schedule('Q0')),48)
  with self.assertRaises(ValueError):development_world(2100)
  with self.assertRaises(ValueError):schedule('S1')
  ws=[development_world(s) for s in range(2000,2008)];self.assertEqual(sum(w['legal_order'][0]==w['report_cell'] for w in ws),4)
 def test_gate_rejects_stratum_regression_and_invalid(self):
  ws={s:development_world(2000+s%8) for s in range(12)};rs=[]
  for a in schedule('Q0',ws):
   w=ws[a['seed']];c=w['unknown_cell'] if a['reliability']==.8 else w['report_cell'];rs.append(dict(a,status='valid',checked={'result':{'choice':c}}))
  self.assertTrue(qualified(rs,ws)['qualification_passed'])
  r=next(r for r in rs if r['objective']=='table' and r['reliability']==.8);r['checked']['result']['choice']=ws[r['seed']]['report_cell'];self.assertFalse(qualified(rs,ws)['qualification_passed']);r['status']='invalid';self.assertFalse(qualified(rs,ws)['qualification_passed'])
 def test_budget_duplicate_and_prior(self):
  with tempfile.TemporaryDirectory() as d:
   l=Ledger(Path(d)/'l','a'*64);self.assertEqual(l.summary()['prior_usd'],.857148138);l.claim('Q0','a')
   with self.assertRaises(Exception):l.claim('Q0','b')
   for i in range(48):l.reserve(str(i),1344000)
   with self.assertRaises(ValueError):l.reserve('49',1344000)
   self.assertAlmostEqual(l.summary()['cumulative_exposure_usd'],.921660138);l.db.close()
 def test_failure_stop_keeps_denominators(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);l=Ledger(d/'l','a'*64)
   def fail(req):raise TimeoutError()
   result=Engine('Q0','fixture',d/'out',l,fail,{s:development_world(s) for s in range(2000,2008)}).run();self.assertEqual(result['assigned'],32);self.assertEqual(result['started'],5);self.assertFalse(result['qualification_passed']);self.assertEqual(sum(x['no_inspection'] for x in result['cells']),32);l.db.close()
 def test_wire_preserves_table(self):
  p=packet(development_world(2000),.8,'table');r=request(p,'choice');self.assertIn('action_consequences',json.dumps(r));self.assertEqual(reservation(r),1344000)
 def test_admission_is_fail_closed(self):
  from admission import Admission
  for c in ({},{'design':'PC-6','stage':'S1','attempt':'q0-a1'},{'design':'PC-6','stage':'Q0','attempt':'q0-a1','source_commit':'0'*40}):
   with self.assertRaises(ValueError):Admission(c,c.get('stage','Q0'),lambda *a: (_ for _ in ()).throw(AssertionError('public check reached before source gate')))
if __name__=='__main__':unittest.main()
