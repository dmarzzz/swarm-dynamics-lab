import copy,json,sys,tempfile,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis'))
import candidate_checks as c
class Checks(unittest.TestCase):
 def setUp(self):
  spec=json.loads((BASE/'diagnostic-v4.json').read_text())['cases'][0];self.case=c.build(spec['family'],0,spec['world'],seed=109,dossier_spec=spec)
  self.original={'instructions':c.CHAIR,'observation':{'phase':'chair','brief':self.case['brief'],'candidates':self.case['candidates'],'documents':self.case['documents'],'reports':[],'checks':[]}}
  self.obs=c.review_request(self.original,True)['observation'];self.matrix={'choice':'DEFER','confidence':.5,'request':{'candidate':self.case['candidates'][0],'kind':'scope'},'candidate_checks':{n:{**v,'citations':[self.obs['documents'][0]['id']],'note':'fixture'} for n,v in c.source_checks(self.case).items()}}
 def test_coverage_and_not_truth(self):
  c.validate_matrix(self.matrix,self.obs);del self.matrix['candidate_checks'][self.case['candidates'][0]]
  with self.assertRaises(ValueError):c.validate_matrix(self.matrix,self.obs)
 def test_wrong_pass_valid_but_semantically_wrong(self):
  n=self.case['candidates'][0];self.matrix['candidate_checks'][n]['deployment_scope']='PASS';c.validate_matrix(self.matrix,self.obs);self.assertNotEqual(self.matrix['candidate_checks'][n]['deployment_scope'],c.source_checks(self.case)[n]['deployment_scope'])
 def test_gate_has_no_gold(self):
  n=self.case['candidates'][0];self.assertEqual(c.execution_gate(n,self.matrix),'DEFER')
  self.matrix['candidate_checks'][n].update({f:'PASS' for f in c.FIELDS});self.assertEqual(c.execution_gate(n,self.matrix),n);self.assertEqual(c.execution_gate(n,{}),'DEFER')
 def test_matched_observations(self):
  before=copy.deepcopy(self.original);a=c.review_request(before,False);b=c.review_request(before,True);self.assertEqual(a['observation'],b['observation']);x=c.chair_request(before,self.matrix);y=c.chair_request(before,self.matrix,True);self.assertEqual(x['observation'],y['observation']);self.assertNotEqual(x['instructions'],y['instructions']);self.assertEqual(before,self.original)
 def test_transfer_gate(self):
  with self.assertRaises(ValueError):c.transfer_gate({'stage':'D2','repair_screen_passed':True},'x')
  s={'stage':'D3','source_signature':'x','repair_screen_passed':True,'valid':18,'terminal':18,'matrix_correct':90,'usage_missing':0,'by_arm':{'matrix_consistent':{'acceptable':6}}};c.transfer_gate(s,'x')
  s['matrix_correct']=89
  with self.assertRaises(ValueError):c.transfer_gate(s,'x')
 def test_source_audit_all_cases(self):
  spec=json.loads((BASE/'diagnostic-v4.json').read_text());choices=set()
  for i,s in enumerate(spec['cases']):
   case=c.build(s['family'],i,s['world'],seed=109,dossier_spec=s);rows,acceptable=c.source_score(case);checks=c.source_checks(case);choices.update(acceptable)
   for n,r in rows.items():self.assertEqual(r['feasible'],all(x=='PASS' for x in checks[n].values()))
   answer=c.scripted({'phase':'chair','brief':case['brief'],'documents':case['documents'],'candidates':case['candidates']});self.assertTrue(c.evaluate(case,answer)['acceptable_decision'])
  self.assertIn('DEFER',choices);self.assertEqual(len(choices),4)
 def test_schema_requires_every_field(self):
  s=c.matrix_schema(self.obs)['properties']['candidate_checks'];self.assertEqual(set(s['required']),set(self.case['candidates']))
  for n in self.case['candidates']:self.assertTrue(set(c.FIELDS)<=set(s['properties'][n]['required']))
if __name__=='__main__':unittest.main()
