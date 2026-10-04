import unittest
from normalization_guard import check,quoted_amounts
class GuardTests(unittest.TestCase):
 def test_grouping(self):self.assertEqual(quoted_amounts('Total 14.300'),{'14300.00'})
 def test_comma_grouping(self):self.assertEqual(quoted_amounts('Total 32,000'),{'32000.00'})
 def test_fraction(self):self.assertEqual(quoted_amounts('Total 14.300,50'),{'14300.50'})
 def test_scale_mismatch_refers(self):self.assertEqual(check({'decision':'accept','amount':'14.30','evidence':'Total 14.300'}),'refer')
 def test_no_quote_or_multiple_values_refers(self):
  for s in ('Total','subtotal 13.000 total 14.300'):
   self.assertEqual(check({'decision':'accept','amount':'14300.00','evidence':s}),'refer')
 def test_agreement_is_not_truth(self):self.assertEqual(check({'decision':'accept','amount':'14300.00','evidence':'Total 14.300'}),'consistent_not_verified')
if __name__=='__main__':unittest.main()
