import unittest,sys,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from corpus import generate
from contract import request,bound,score,summarize
class NativeTests(unittest.TestCase):
 def test_input_envelope_and_isolation(self):
  for r in generate('qualification',1):
   req=request(r['actor']);self.assertLessEqual(bound(req),6000);self.assertNotIn('gold',req['messages'][1]['content']);self.assertFalse(req['provider']['allow_fallbacks'])
 def answer(self,r):
  return {'decision':r['gold']['decision'],'source_votes':r['gold']['source_votes'],'source_quotes':{x['id']:x['text'].splitlines()[-1] for x in r['actor']['receipts']},'distorted_report_ids':[i for i,v in r['gold']['report_fidelity'].items() if not v]}
 def test_perfect_and_constant_answer_gate(self):
  rows=generate('qualification',2);records=[{'valid':True,'score':score(r,self.answer(r))} for r in rows];self.assertTrue(summarize(rows,records)['qualified'])
  for r in records:r['score']['decision_correct']=r['score']['decision']=='ZERO'
  self.assertFalse(summarize(rows,records)['qualified'])
 def test_bad_fields_and_quotes(self):
  r=generate('qualification',3)[0];a=self.answer(r);a['extra']='forbidden'
  with self.assertRaises(ValueError):score(r,a)
  a=self.answer(r);a['source_quotes']={i:'fabricated' for i in a['source_quotes']};self.assertFalse(score(r,a)['quotes_valid'])
 def test_missingness_never_passes(self):
  rows=generate('qualification',2);self.assertFalse(summarize(rows,[])['qualified']);self.assertEqual(summarize(rows,[{'valid':False}])['unstarted'],23)
if __name__=='__main__':unittest.main()
