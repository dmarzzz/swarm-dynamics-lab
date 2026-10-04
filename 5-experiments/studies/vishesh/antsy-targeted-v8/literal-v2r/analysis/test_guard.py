import unittest
from exact_quote_guard import verified_quote
class Tests(unittest.TestCase):
 def test_exact_not_prefix(self):
  r={'verified':True,'evidence':'DU 1,096,040 visible as final payable total'}
  self.assertFalse(verified_quote({'token':'1,096,0409'},r));self.assertTrue(verified_quote({'token':'1,096,040'},r))
 def test_false_and_missing_stay_false(self):
  self.assertFalse(verified_quote({'token':'14.300'},{'verified':False,'evidence':'Total 14.300'}));self.assertFalse(verified_quote({'token':'14.300'},{'verified':True,'evidence':'yes'}))
 def test_common_misreading_still_passes(self):
  self.assertTrue(verified_quote({'token':'29,900'},{'verified':True,'evidence':'Total 29,900'}))
if __name__=='__main__':unittest.main()
