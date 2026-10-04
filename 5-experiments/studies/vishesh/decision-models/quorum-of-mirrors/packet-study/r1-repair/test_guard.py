import unittest,json
from pathlib import Path
from guard import check
from baseline import solve
from cases import build
class Tests(unittest.TestCase):
 def test_saved_cohort(self):
  audit=json.loads((Path(__file__).resolve().parents[2]/'results/QM-R1-01/audit.json').read_text())
  rejected=[];seen=0
  for e in audit:
   if e['receipt']:
    seen+=1
    if not check(e['case']['actor'],e['receipt']['parsed'])['accepted']:rejected.append(e['assignment']['id'])
  self.assertEqual(seen,35);self.assertEqual(rejected,['QM-R1-01-032','QM-R1-01-034'])
 def test_value_fault(self):
  r=build('guard')[0];a=solve(r['actor']);self.assertTrue(check(r['actor'],a)['accepted']);a['sources'][1]['value']=0;self.assertFalse(check(r['actor'],a)['accepted'])
 def test_unknown_value(self):
  r=next(r for r in build('guard') if not r['condition']['source_observed']);a=solve(r['actor']);a['sources'][0]['value']=0;self.assertFalse(check(r['actor'],a)['accepted'])
if __name__=='__main__':unittest.main()
