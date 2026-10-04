import unittest
from decimal import Decimal
from provider import microdollars
class Money(unittest.TestCase):
    def test_conservative_rounding(self):
        self.assertEqual(microdollars('0.0000001'),1)
        self.assertEqual(microdollars(Decimal('0.01')),10000)
        self.assertEqual(microdollars('0'),0)
        for invalid in ('NaN','Infinity','-1'):
            with self.assertRaises(ValueError):microdollars(invalid)
if __name__=='__main__':unittest.main()
