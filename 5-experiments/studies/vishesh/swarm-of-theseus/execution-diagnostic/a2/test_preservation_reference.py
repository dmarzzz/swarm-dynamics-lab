import copy, unittest
from preservation_reference import decide, fixtures
from design import label

class PreservationFixtures(unittest.TestCase):
    def test_stable_and_irrelevant_variants(self):
        old, records, _, _ = fixtures()
        changed=copy.deepcopy(records)
        for h in changed: h['case']['queue']='irrelevant';h['case']['summary']='irrelevant'
        for cls in 'AB':
            practice={'class':cls,'source':old[cls]}
            self.assertEqual(decide(practice,records,'release',1)['state'],'retain')
            self.assertEqual(decide(practice,records,'release',1),decide(practice,changed,'release',1))
    def test_selective_revision_and_counterexample(self):
        old, _, records, _ = fixtures()
        self.assertEqual(decide({'class':'A','source':old['A']},records,'release',1)['state'],'revise')
        self.assertEqual(decide({'class':'B','source':old['B']},records,'release',1)['state'],'retain')
        self.assertTrue(any(h['case']['class']=='A' and label(h['case'],old['A'],'release')!=h['outcome'] for h in records))
    def test_conflict_quarantine_and_no_evidence_provisional(self):
        old, _, _, records = fixtures();cls=records[-1]['case']['class']
        self.assertEqual(decide({'class':cls,'source':old[cls]},records,'release',1)['state'],'quarantine')
        self.assertEqual(decide({'class':cls,'source':old[cls]},records,'release',2)['state'],'provisional')
if __name__=='__main__':unittest.main()
