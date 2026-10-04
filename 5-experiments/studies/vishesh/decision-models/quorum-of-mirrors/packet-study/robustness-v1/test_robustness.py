import unittest,copy,sqlite3
from cases import build,FAMILIES
from baseline import solve
from contract import score,request,bound,summarize,digest
import budget
class Cases(unittest.TestCase):
 def test_stress(self):
  rows=build('offline-stress',100)
  self.assertEqual(len(rows),1000)
  for row in rows:
   s=score(row,solve(row['actor']))
   self.assertTrue(s['grounded_quotes_valid'] and s['labels_correct'] and s['decision_correct'])
   self.assertLessEqual(bound(request(row['actor'])),7000)
 def test_pair_control(self):
  rows=build('controls')
  for root in {r['root'] for r in rows}:
   a,b=sorted([r for r in rows if r['root']==root],key=lambda r:r['condition']['copies'])
   self.assertEqual(a['actor']['sources'],b['actor']['sources']);self.assertEqual(a['actor']['query'],b['actor']['query'])
   self.assertEqual(len(a['actor']['reports']),6);self.assertEqual(len(b['actor']['reports']),8)
   self.assertEqual(a['gold']['decision'],b['gold']['decision'])
 def test_balance(self):
  rows=build('balance')
  for family in FAMILIES:
   rs=[r for r in rows if r['family']==family and r['condition']['copies']==1]
   self.assertEqual([r['gold']['decision'] for r in rs].count('DEFER'),2)
   self.assertEqual({r['gold']['decision'] for r in rs},{'ONE','ZERO','DEFER'})
 def test_mode_fault_does_not_hide(self):
  row=next(r for r in build('modes') if not r['condition']['source_observed']);a=solve(row['actor'])
  f=next(f for f in a['reports'] if f['mode']=='HEDGE');f['mode']='ASSERTION'
  s=score(row,a);self.assertTrue(s['labels_correct']);self.assertFalse(s['grounded_quotes_valid'])
 def test_value_fault_does_not_hide(self):
  row=next(r for r in build('values') if not r['condition']['source_observed']);a=solve(row['actor']);a['reports'][0]['value']+=1
  s=score(row,a);self.assertTrue(s['labels_correct']);self.assertFalse(s['grounded_quotes_valid'])
 def test_quote_marker_required(self):
  row=build('quote')[0];a=solve(row['actor']);f=next(f for f in a['reports'] if f['mode']=='HEDGE');f['quote']=f['quote'].removeprefix('Unconfirmed: ')
  self.assertFalse(score(row,a)['quotes_valid'])
 def test_schema_constant(self):
  self.assertEqual(len({digest(request(r['actor'])['response_format']) for r in build('schema')}),1)
 def test_stage_gate(self):
  rows=build('q',1,'qualification')+build('e');records=[]
  for r in rows[:10]:
   a=solve(r['actor']);records.append(dict(case_id=r['id'],valid=True,parsed=a,score=score(r,a)))
  s=summarize(rows,records);self.assertTrue(s['qualified']);self.assertFalse(s['evaluation_accepted']);self.assertEqual(s['stages']['evaluation']['unstarted'],40)
  records[0]['score']['grounded_quotes_valid']=False
  self.assertFalse(summarize(rows,records)['qualified'])
class Budget(unittest.TestCase):
 def setUp(self):
  self.db=sqlite3.connect(':memory:');self.db.executescript("create table calls(id text primary key,reserved real,status text,actual real);create table authority(id int,experiment text,cap real);insert into authority values(1,'quorum-of-mirrors',1);create table authority_extensions(id text primary key,amount real,evidence text);insert into authority_extensions values('PQ-02-owner-2026-10-04',2,'old');create table next_attempts(attempt text,status text);insert into calls values('old',.06,'complete',.01);insert into calls values('unknown',.06,'failed_or_uncertain',NULL);")
 def tearDown(self):self.db.close()
 def test_settlement_preserves_unknown_and_original(self):
  h=budget.prior_digest(self.db);self.assertAlmostEqual(budget.initialize(self.db,h,'old','new'),.07)
  self.assertEqual(budget.prior_digest(self.db),h)
  budget.initialize(self.db,h,'old','new');self.assertEqual(self.db.execute('select count(*) from authority_extensions').fetchone()[0],2)
  self.assertEqual(self.db.execute('select count(*) from settlements').fetchone()[0],1)
 def test_attempt_cap_and_duplicate(self):
  budget.initialize(self.db,budget.prior_digest(self.db),'old','new')
  budget.reserve(self.db,'run-0',.048,'run',1,.048,'old','new')
  with self.assertRaises(AssertionError):budget.reserve(self.db,'run-1',.048,'run',1,.048,'old','new')
 def test_overcharge_fail_closed(self):
  self.db.execute("update calls set actual=.07 where id='old'")
  with self.assertRaises(AssertionError):budget.exposure(self.db)
if __name__=='__main__':unittest.main()
