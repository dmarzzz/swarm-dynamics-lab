import json,time,unittest
from unittest.mock import patch
import run_local as r
class LocalTests(unittest.TestCase):
 def test_qualification_gate(self):
  rows=[r.run_arm({k:v for k,v in c.items() if k!='arm'},c['arm'],r.ScriptedPolicy()) for c in r.assignments('Q0')]
  self.assertTrue(r.competence(rows))
  rows[0]['validity']['ok']=False;self.assertFalse(r.competence(rows))
 def test_assignments_disjoint_and_historical(self):
  self.assertEqual(len(r.assignments('S1')),50)
  self.assertEqual(len(r.assignments('D0')),4)
  self.assertNotEqual(r.assignments('Q0')[0]['task_id'],r.assignments('Q1')[0]['task_id'])
 def test_no_answer_values_in_schema(self):
  seen=[]
  def mock(path,body,timeout):
   seen.append(body)
   return {'done_reason':'stop','message':{'content':'{"choice":"candidate-y","confidence":0.5}'},'prompt_eval_count':50,'eval_count':12}
  with patch.object(r,'http',mock):
   p=r.LocalPolicy('test',time.monotonic()+10,lambda x:None)
   a=p.complete({'instructions':'choose','observation':{}},lambda o:{'choice':'private-template-value','confidence':.812345})
  self.assertEqual(a['choice'],'candidate-y')
  self.assertNotIn('private-template-value',json.dumps(seen));self.assertNotIn('.812345',json.dumps(seen))
  self.assertFalse(seen[0]['think']);self.assertEqual(p.output_tokens,12)
 def test_truncation_fails_without_fallback(self):
  with patch.object(r,'http',return_value={'done_reason':'length','message':{'content':'{}'}}):
   p=r.LocalPolicy('test',time.monotonic()+10,lambda x:None)
   with self.assertRaises(r.PolicyError):p.complete({'instructions':'x','observation':{}},lambda o:{})
   self.assertEqual(p.calls,1)
 def test_deadline_stops_before_dispatch(self):
  with patch.object(r,'http') as mock:
   p=r.LocalPolicy('test',time.monotonic()-1,lambda x:None)
   with self.assertRaises(r.PolicyError):p.complete({},lambda o:{})
   mock.assert_not_called()
 def test_replay_failure_and_final_count(self):
  import tempfile
  from pathlib import Path
  with tempfile.TemporaryDirectory() as td:
   row=dict(assignment=0,domain='test',world='clean',arm='private_review',validity={'ok':False},evaluation={'correct':0},call_slots=1)
   r.build_view(Path(td),[row],[dict(assignment=0,kind='failure'),dict(assignment=0,kind='terminal')],'test')
   self.assertTrue(json.loads((Path(td)/'visual-validation.json').read_text())['final_states_match'])
   self.assertIn('INVALID',(Path(td)/'final.svg').read_text())
if __name__=='__main__':unittest.main()
