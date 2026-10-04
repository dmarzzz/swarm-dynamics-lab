import unittest
from unittest.mock import patch
import instrument as i
import runner as r
import test_coordinator
class RunnerTests(unittest.TestCase):
 def test_qualification_has_27_calls_and_native_handover(self):
  w=i.world(111,5);oracle=test_coordinator.SchedulingTests().oracle(w);calls=[]
  def call(phase,p):calls.append(phase);return oracle(phase,p)
  result=r.qualify(w,call);self.assertTrue(result['passed']);self.assertEqual(len(calls),27)
 def test_missing_admission_fails_closed(self):
  with self.assertRaises(ValueError):r.validate({},'x')
 def test_qualification_failure_does_not_enter_joint_round(self):
  calls=[]
  def fail(phase,p):calls.append(phase);return {}
  result=r.qualify(i.world(222,5),fail);self.assertFalse(result['passed']);self.assertEqual(calls,['learn']*5)
if __name__=='__main__':unittest.main()

class ReplayRepairTests(unittest.TestCase):
 def test_saved_founders_never_invoke_live_callback(self):
  import tempfile,json
  from pathlib import Path
  import native as n
  w=i.world(333,5);oracle=test_coordinator.SchedulingTests().oracle(w);seen=[]
  class Live:
   def set_condition(self,c):pass
   def __call__(self,phase,p):seen.append(phase);return oracle(phase,p)
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);(root/'terminal.json').write_text(json.dumps({'started_calls':5,'status':'complete'}))
   for k,p in enumerate(w['members']):
    packet,_=n.founder_packet(w,p);value=oracle('learn',packet)
    (root/(str(k)+'-request.json')).write_text(json.dumps({'phase':'learn','request':n.request('learn',packet)}))
    (root/(str(k)+'-response.json')).write_text(json.dumps({'error':None,'response':{'model':'openai/gpt-6-sol','choices':[{'finish_reason':'stop','message':{'content':json.dumps(value)}}]}}))
   wrapped=r.ReplayFounders(root,Live());result=r.qualify(w,wrapped)
   self.assertTrue(result['passed']);self.assertEqual(len(seen),22);self.assertNotIn('learn',seen)
