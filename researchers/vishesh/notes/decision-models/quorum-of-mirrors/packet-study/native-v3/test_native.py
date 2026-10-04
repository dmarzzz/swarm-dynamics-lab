import unittest,json,copy
from cases import build
from baseline import solve
from contract import request,score,summarize,normalize,bound
class Tests(unittest.TestCase):
 def test_constant_schema_and_semantics(self):
  schemas=set();records=[]
  for row in build('development-PQ3'):
   req=request(row['actor']);schemas.add(json.dumps(req['response_format'],sort_keys=True));self.assertLessEqual(bound(req),10000)
   s=score(row,solve(row['actor']));self.assertTrue(s['labels_correct'] and s['quotes_valid'] and s['decision_correct']);self.assertEqual(s['source_facts_correct'],3);self.assertEqual(s['report_facts_correct'],len(row['actor']['reports']));records.append({'valid':True,'score':s})
  self.assertEqual(len(schemas),1);self.assertTrue(summarize(build('development-PQ3'),records)['qualified'])
 def test_missing_duplicate_extra_ids_rejected(self):
  row=build('development-PQ3')[0]
  for mutate in [lambda a:a['reports'].pop(),lambda a:a['reports'].append(a['reports'][0]),lambda a:a['reports'][0].update(id='unknown')]:
   a=solve(row['actor']);mutate(a)
   with self.assertRaises(ValueError):score(row,a)
 def test_invalid_facts_and_quotes(self):
  row=build('development-PQ3')[0];a=solve(row['actor']);a['sources'][0]['value']=True
  with self.assertRaises(ValueError):score(row,a)
  a=solve(row['actor']);a['sources'][0]['quote']='At';self.assertFalse(score(row,a)['quotes_valid'])
 def test_no_actor_gold(self):
  for r in build('development-PQ3'):self.assertEqual(json.loads(request(r['actor'])['messages'][1]['content']),r['actor'])
 def test_missingness(self):self.assertFalse(summarize(build('development-PQ3'),[])['qualified'])
