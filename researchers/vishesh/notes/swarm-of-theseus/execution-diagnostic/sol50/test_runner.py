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
