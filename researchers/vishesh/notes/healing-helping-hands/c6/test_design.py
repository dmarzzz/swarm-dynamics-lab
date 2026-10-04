import copy,json,unittest
from design import *
from parser_reference import predict
class DesignTests(unittest.TestCase):
 def test_balanced_unique(self):
  for s,n in [('D0',12),('S0',60),('S1',432)]:
   rows=cases(s);self.assertEqual(len(rows),n);self.assertEqual(len({r['id'] for r in rows}),n)
   self.assertEqual([sum(r['expected']==l for r in rows) for l in LABELS],[n//3]*3)
   self.assertEqual(len({sha(visible(r)) for r in rows}),n)
 def test_actor_isolation(self):
  r=cases('S0')[0];altered={**r,'expected':'DO_NOT_SEND','family':'SECRET','id':'GOLD_ID'}
  self.assertEqual(haiku(r,0),haiku(altered,0));self.assertEqual(qwen(r,'original','schema'),qwen(altered,'original','schema'))
 def test_crossed_factors(self):
  r=cases('D0')[0]
  for prompt in ('original','simple'):
   a=qwen(r,prompt,'schema');b=qwen(r,prompt,'text');a.pop('format');self.assertEqual(a,b)
  a=qwen(r,'original','schema');b=qwen(r,'simple','schema');a.pop('messages');b.pop('messages');self.assertEqual(a,b)
 def test_baseline_all_cells(self):
  for stage in ('D0','S0','S1'):
   for r in cases(stage):self.assertEqual(predict(r['claim'],r['report']),r['expected'],r['id'])
 def test_baseline_no_evaluator(self):
  self.assertIsNone(predict('A claim','Novel unrelated prose.'))
  self.assertEqual(predict('M improves accuracy','M achieved 40% accuracy and the baseline achieved 60%.'),'REFUTE')
  self.assertEqual(predict('M improves accuracy','M achieved 70% accuracy and the baseline achieved 60%.'),'SUPPORT')
  self.assertEqual(predict('Renamed improves accuracy','Renamed achieved 70% accuracy and the baseline achieved 60%.'),'SUPPORT')
 def test_qualification_rejects_collapse(self):
  rows=cases('S0')
  for r in rows:r.update(status='completed',labels={a:r['expected'] for a in ('a','b','jev')})
  self.assertTrue(qualification(rows)['qualified'])
  for r in rows:r['labels']['a']='REFUTE'
  self.assertFalse(qualification(rows)['qualified'])
 def test_strict_schema_and_cohort(self):
  p=haiku(cases('S0')[0],0);self.assertTrue(p['response_format']['json_schema']['strict']);self.assertEqual(p['max_tokens'],64);self.assertEqual(COHORT,'C6R2')
 def test_complete_fence_normalization(self):
  self.assertEqual(parse_label('```json\n{"label":"SUPPORT"}\n```'),'SUPPORT')
 def test_parse_fail_closed(self):
  for text in ('SUPPORT','prose ```json\n{}\n```','{"label":"SUPPORT","extra":1}','{"label":"maybe"}'):
   with self.assertRaises(ValueError):parse_label(text)
 def test_haiku_only_option_order_changes(self):
  a=haiku(cases('S0')[0],0);b=haiku(cases('S0')[0],1)
  x=a.pop('messages')[0]['content'];y=b.pop('messages')[0]['content'];sa=a.pop('response_format');sb=b.pop('response_format');self.assertEqual(set(sa['json_schema']['schema']['properties']['label']['enum']),set(sb['json_schema']['schema']['properties']['label']['enum']));self.assertEqual(a,b)
  self.assertEqual(x.replace('SUPPORT, REFUTE, UNCERTAIN','LABELS'),y.replace('REFUTE, UNCERTAIN, SUPPORT','LABELS'))
 def test_same_wrong_agreement_is_not_rescued(self):
  rows=cases('S1')
  for r in rows:r.update(status='completed',labels={'a':'REFUTE','b':'REFUTE','jev':r['expected']})
  s=score(rows);self.assertFalse(s['useful_descriptive_result']);self.assertEqual(s['counterfactual_cascade_jev_calls'],0)
if __name__=='__main__':unittest.main()
