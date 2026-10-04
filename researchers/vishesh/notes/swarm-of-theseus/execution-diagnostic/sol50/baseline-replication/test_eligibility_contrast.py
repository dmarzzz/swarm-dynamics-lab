import unittest
import eligibility_contrast as e
class EligibilityContrastTests(unittest.TestCase):
 def test_public_boundaries_and_wrong_pairs(self):
  self.assertEqual(e.boundary_fixture(),{'current':'allow','lower-bound':'allow','future':'defer','stale':'defer','missing':'defer','wrong-pair-missing':'defer','wrong-pair-present':'hold'})
if __name__=='__main__':unittest.main()
