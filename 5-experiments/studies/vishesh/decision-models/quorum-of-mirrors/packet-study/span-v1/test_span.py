import unittest,copy,json,sqlite3
from pathlib import Path
from cases import build,FAMILIES
from baseline import solve
from contract import score,decode,request,bound,summarize,digest
import budget
class Tests(unittest.TestCase):
 def test_stress_across_seeds(self):
  count=0
  for seed in range(10):
   for r in build('software-'+str(seed),10):
    s=score(r,solve(r['actor']));self.assertTrue(s['grounded_quotes_valid'] and s['labels_correct'] and s['decision_correct']);self.assertLessEqual(bound(request(r['actor'])),7000);count+=1
  self.assertEqual(count,1000)
 def test_balanced_qualification(self):
  rows=build('balance')
  for family in FAMILIES:
   ds=[r['gold']['decision'] for r in rows if r['family']==family and r['condition']['copies']==1]
   self.assertEqual(sorted(ds),['DEFER','DEFER','ONE','ZERO'])
 def test_wrong_old_clause_no_query_vote(self):
  r=next(r for r in build('old') if r['family']=='timelines' and r['condition']['source_observed']);a=solve(r['actor']);a['sources'][0]['quote']=r['actor']['sources'][0]['text'].splitlines()[0]
  s=score(r,a);self.assertFalse(s['grounded_quotes_valid']);self.assertEqual(s['decision'],'DEFER');self.assertEqual(s['source_selections_correct'],2)
 def test_wrong_entity_preserved_not_replaced(self):
  r=next(r for r in build('entity') if r['family']=='entities' and r['condition']['source_observed']);a=solve(r['actor']);a['sources'][0]['quote']=r['actor']['sources'][0]['text'].splitlines()[0]
  d=decode(r['actor'],a);self.assertTrue(d['sources'][0]['entity'].endswith('-other'));self.assertFalse(score(r,a)['grounded_quotes_valid'])
 def test_wrong_initial_not_corrected_by_decoder(self):
  r=next(r for r in build('initial') if r['family']=='corrections' and r['condition']['source_observed']);a=solve(r['actor']);a['sources'][0]['quote']=r['actor']['sources'][0]['text'].splitlines()[0]
  self.assertFalse(score(r,a)['grounded_quotes_valid'])
 def test_cropped_marker_and_negation(self):
  r=build('crop')[0];a=solve(r['actor']);i=next(i for i,f in enumerate(a['reports']) if f['quote'].startswith('Unconfirmed:'));a['reports'][i]['quote']=a['reports'][i]['quote'].removeprefix('Unconfirmed: ')
  with self.assertRaises(ValueError):decode(r['actor'],a)
  r=next(r for r in build('neg') if r['actor']['query']['property']=='running');a=solve(r['actor']);a['sources'][2]['quote']=a['sources'][2]['quote'].replace('not running','running')
  with self.assertRaises(ValueError):decode(r['actor'],a)
 def test_plan_as_source_not_silent_pass(self):
  r=next(r for r in build('plan') if not r['condition']['source_observed']);a=solve(r['actor']);a['sources'][0]['quote']=r['actor']['sources'][0]['text'];s=score(r,a)
  self.assertTrue(s['decision_correct']);self.assertFalse(s['grounded_quotes_valid']);self.assertEqual(s['source_selections_correct'],2)
 def test_false_null(self):
  r=next(r for r in build('null') if r['condition']['source_observed']);a=solve(r['actor']);a['sources'][0]['quote']=None;s=score(r,a);self.assertFalse(s['grounded_quotes_valid']);self.assertEqual(s['decision'],'DEFER')
 def test_shape_id_and_redundant_fields(self):
  r=build('shape')[0];a=solve(r['actor']);a['sources'][0]['value']=0
  with self.assertRaises(ValueError):decode(r['actor'],a)
  a=solve(r['actor']);a['reports'][1]['id']=a['reports'][0]['id']
  with self.assertRaises(ValueError):decode(r['actor'],a)
 def test_sorted_pairs_and_complete_gate(self):
  rows=build('summary');rr=[]
  for r in rows:
   a=solve(r['actor']);rr.append(dict(case_id=r['id'],valid=True,parsed=a,score=score(r,a)))
  self.assertTrue(summarize(rows,rr)['qualified']);self.assertEqual(summarize(rows,rr),summarize(list(reversed(rows)),rr));self.assertFalse(summarize(rows,rr[:-1])['qualified'])
 def test_schema_constant(self):self.assertEqual(len({digest(request(r['actor'])['response_format']) for r in build('schema')}),1)
 def test_budget_envelope_and_duplicate(self):
  with sqlite3.connect(':memory:') as db:
   db.executescript("create table calls(id text primary key,reserved real,status text,actual real);create table authority_extensions(id text primary key,amount real,evidence text);insert into authority_extensions values('PQ-02-owner-2026-10-04',2,'old');insert into authority_extensions values('R1-owner-2026-10-04',5,'new');")
   budget.reserve(db,'QM-SP-01-000',.048,'QM-SP-01',1,.048,'old','new')
   with self.assertRaises(AssertionError):budget.reserve(db,'QM-SP-01-001',.048,'QM-SP-01',1,.048,'old','new')
   with self.assertRaises(AssertionError):budget.reserve(db,'QM-SP-01-000',.048,'QM-SP-01',1,.048,'old','new')
  db.close()
if __name__=='__main__':unittest.main()
