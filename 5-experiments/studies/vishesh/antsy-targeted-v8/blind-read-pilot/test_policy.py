import unittest
from policy import normalized,policies,outcome,direct,admission
class Tests(unittest.TestCase):
 def test_locale(self):
  self.assertEqual(normalized('14.300','ID'),'14300.00');self.assertEqual(normalized('14.30','MY'),'14.30');self.assertIsNone(normalized('14,30','MY'))
 def test_invalid(self):
  for s in ['1,23,456','12.345,678','-2','NaN','1e3','12 000']:self.assertIsNone(normalized(s,'ID'))
 def test_direct_not_repaired(self):self.assertIsNone(direct({'decision':'accept','amount':'29.998'}))
 def test_contradiction(self):
  a={'decision':'accept','token':'1,096,0409'};b={'decision':'accept','token':'1,096,040'}
  self.assertIsNone(policies({}, {},a,b,{'verified':True,'token':b['token']},'ID')['conditioned'])
 def test_shared_wrong_survives(self):
  a={'decision':'accept','token':'29,900'};r=policies({}, {},a,a,{'verified':True,'token':'29,900'},'ID')
  self.assertEqual(outcome(r['blind'],'29999.00'),'wrong_accept');self.assertEqual(r['blind'],r['conditioned'])
 def test_exact_token(self):
  a={'decision':'accept','token':'32,000'};b={'decision':'accept','token':'32.000'}
  self.assertIsNone(policies({}, {},a,b,{'verified':False,'token':'32,000'},'ID')['blind'])
 def test_unknown(self):self.assertEqual(outcome('10.00',None),'unsupported_accept');self.assertEqual(outcome(None,None),'refer')
 def test_manifest_fail_closed(self):
  with self.assertRaises(AssertionError):admission([])
 def test_referral_not_correct(self):self.assertEqual(outcome(None,'10.00'),'refer')
if __name__=='__main__':unittest.main()
