import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from analyze import summarize
class Analysis(unittest.TestCase):
    def test_missing_assignment_stays_in_denominator(self):
        assigned=[dict(world='w',task_id=1,seed=1,dose=1,arm=a) for a in ['Q11','Q10F','CLEAN']]
        rows=[dict(assigned[0],validity={'ok':True},evaluation={'utility':1})]
        s=summarize(rows,assigned);self.assertEqual(s['missing'],2);self.assertEqual(s['invalid'],2);self.assertFalse(s['execution_qualified']);self.assertFalse(s['clean_qualified']);self.assertEqual(s['contrasts'][0]['valid_pairs'],0)
    def test_duplicates_rejected(self):
        a=dict(world='w',task_id=1,seed=1,dose=1,arm='CLEAN');r=dict(a,validity={'ok':True},evaluation={'utility':1})
        with self.assertRaises(ValueError):summarize([r,r],[a])
if __name__=='__main__':unittest.main()
