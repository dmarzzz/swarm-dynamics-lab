import unittest,json,copy
from pathlib import Path
from cases import build
from baseline import solve
from contract import request,score,summarize,normalize,core
class Tests(unittest.TestCase):
 def test_oracle_and_pairs(self):
  rows=build('development4');records=[]
  for r in rows:
   a=solve(r['actor']);s=score(r,a);records.append({'case_id':r['id'],'valid':True,'parsed':a,'score':s})
  self.assertTrue(summarize(rows,records)['qualified']);self.assertEqual(len({json.dumps(request(r['actor'])['response_format'],sort_keys=True) for r in rows}),1)
  for root in {r['root'] for r in rows}:
   pair=[r for r in rows if r['root']==root];self.assertEqual(pair[0]['actor']['reports'],pair[1]['actor']['reports']);self.assertEqual(pair[0]['gold']['reports'],pair[1]['gold']['reports']);self.assertEqual(sum(r['gold']['decision']=='DEFER' for r in pair),1)
 def test_label_correct_but_wrong_fact_fails(self):
  r=next(r for r in build('development4') if not r['condition']['source_observed']);a=solve(r['actor']);a['reports'][0]['value']+=1;s=score(r,a)
  self.assertTrue(s['labels_correct']);self.assertTrue(s['quotes_valid']);self.assertFalse(s['grounded_quotes_valid']);self.assertEqual(s['report_facts_correct'],3)
 def test_prior_error_rejected(self):
  p=Path(__file__).resolve().parents[2]/'results/QM-PQ-03/misses.json';e=json.loads(p.read_text())[0];a=copy.deepcopy(e['receipt']['parsed'])
  for f in a['reports']:f.pop('status')
  with self.assertRaises(ValueError):score(e['case'],a)
 def test_identity_and_missingness(self):
  r=build('development4')[0]
  for action in [lambda a:a['reports'].pop(),lambda a:a['reports'].append(a['reports'][0]),lambda a:a['reports'][0].update(id='unknown')]:
   a=solve(r['actor']);action(a)
   with self.assertRaises(ValueError):score(r,a)
  self.assertFalse(summarize(build('development4'),[])['qualified'])
 def test_report_status_and_null_forbidden(self):
  r=build('development4')[0]
  for update in [{'status':'unknown'},{'value':None},{'value':True}]:
   a=solve(r['actor']);a['reports'][0].update(update)
   with self.assertRaises(ValueError):score(r,a)
 def test_wrong_source_abstention_detected(self):
  r=next(r for r in build('development4') if not r['condition']['source_observed']);a=solve(r['actor']);a['sources'][0].update(status='observed',value=1);s=score(r,a);self.assertFalse(s['decision_correct']);self.assertFalse(s['grounded_quotes_valid'])
