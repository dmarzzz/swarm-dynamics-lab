import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from continuation import partition,combine
from rd4_design import assignments

class ContinuationTests(unittest.TestCase):
 def setUp(self):
  self.items=assignments('S4')
  for x in self.items:x['status']='planned'
  self.items[0]['status']='terminal';x=self.items[0]
  self.rows=[dict(case_id=x['case_id'],arm=x['arm'],epoch=i,status='failed') for i in range(4)]
 def test_terminal_failures_are_excluded_from_resume(self):
  p=partition({'assignments':self.items},self.rows);self.assertEqual(len(p),143);self.assertNotEqual((p[0]['case_id'],p[0]['arm']),(self.items[0]['case_id'],self.items[0]['arm']))
 def test_changed_parent_assignment_rejected(self):
  self.items.reverse()
  with self.assertRaises(ValueError):partition({'assignments':self.items},self.rows)
 def test_ambiguous_started_assignment_rejected(self):
  self.items[1]['status']='started'
  with self.assertRaises(ValueError):partition({'assignments':self.items},self.rows)
 def test_duplicate_result_rejected(self):
  with self.assertRaises(ValueError):combine(self.rows,self.rows)
 def test_original_order_and_prefix_preserved(self):
  x=self.items[1];added=[dict(case_id=x['case_id'],arm=x['arm'],epoch=i) for i in reversed(range(4))]
  c=combine(self.rows,added);self.assertEqual(c[:4],self.rows);self.assertEqual([x['epoch'] for x in c[4:]],list(range(4)))
 def test_missing_parent_epoch_rejected(self):
  with self.assertRaises(ValueError):partition({'assignments':self.items},self.rows[:3])
if __name__=='__main__':unittest.main()
