import copy,json,sys,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis'));sys.path.insert(0,str(BASE/'src'))
from approval_review import review_request,chair_request
from dossier import build,evaluate
from study import reference_decision,cost_worksheet

class ApprovalReviewTests(unittest.TestCase):
 def test_only_review_instructions_differ(self):
  q={'instructions':'chair','observation':{'phase':'chair','reports':[{'choice':'Aster'}],'documents':[]}}
  a,b=review_request(q,'approval_review'),review_request(q,'general_review')
  self.assertEqual(a['observation'],b['observation']);self.assertNotEqual(a['instructions'],b['instructions']);self.assertEqual(q['observation']['phase'],'chair')
  before=copy.deepcopy(q);r={'choice':'DEFER'};c=chair_request(q,r)
  self.assertEqual(q,before);self.assertEqual(c['instructions'],q['instructions']);self.assertEqual(c['observation']['reports'],q['observation']['reports']+[r])
 def test_fresh_case_labels_and_document_oracle(self):
  specs=json.loads((BASE/'diagnostic-v3.json').read_text())['cases'];old=json.loads((BASE/'qualification-v2.json').read_text())['cases'];choices=[]
  self.assertTrue({s['id'] for s in specs}.isdisjoint(s['id'] for s in old))
  for i,s in enumerate(specs):
   c=build(s['family'],i,s['world'],seed=83,dossier_spec=s)
   obs={'phase':'chair','documents':c['documents'],'brief':c['brief'],'candidates':c['candidates']}
   answer=reference_decision(obs);self.assertEqual(evaluate(c,answer)['acceptable_decision'],1);choices.append(answer['choice'])
   self.assertNotIn('evaluator',obs);self.assertNotIn('acceptable',json.dumps(obs))
   self.assertEqual(len(cost_worksheet(obs)),3)
  self.assertEqual(choices[:2],['DEFER','DEFER']);self.assertNotIn('DEFER',choices[2:]);self.assertGreaterEqual(len(set(choices)),3)
 def test_wrong_action_and_blanket_deferral_rejected(self):
  specs=json.loads((BASE/'diagnostic-v3.json').read_text())['cases']
  for i,s in enumerate(specs):
   c=build(s['family'],i,s['world'],seed=83,dossier_spec=s)
   choice=c['candidates'][0] if i<2 else 'DEFER'
   self.assertEqual(evaluate(c,{'choice':choice,'confidence':.8,'annual_total_usd':None})['acceptable_decision'],0)
if __name__=='__main__':unittest.main()
