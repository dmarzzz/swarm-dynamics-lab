import copy
import unittest
from audit import exact_trusted_rule,verify_rule,audit

class AuditTests(unittest.TestCase):
    def setUp(self):self.reports=[{'visible_root':str(i),'value':v,'q':.65} for i,v in enumerate((1,0,0))]
    def test_all_finite_configurations(self):self.assertEqual(verify_rule()['configurations'],5488)
    def test_copies_cannot_flip_answer(self):
        self.assertEqual(exact_trusted_rule(self.reports), 'ZERO')
        self.assertEqual(exact_trusted_rule([self.reports[0]]*20+self.reports[1:]),'ZERO')
    def test_unknown_lineage_refused(self):
        for root in (None,'',1):
            bad=copy.deepcopy(self.reports);bad[0]['visible_root']=root
            with self.assertRaises(ValueError):exact_trusted_rule(bad)
    def test_contradictory_copy_refused(self):
        with self.assertRaises(ValueError):exact_trusted_rule(self.reports+[dict(self.reports[0],value=0)])
    def test_unequal_reliability_refused(self):
        with self.assertRaises(ValueError):exact_trusted_rule([dict(self.reports[0],q=.8)]+self.reports[1:])
    def test_bad_reliability_refused(self):
        for q in (.5,1,0,float('nan'),True,'0.65'):
            with self.assertRaises(ValueError):exact_trusted_rule([dict(r,q=q) for r in self.reports])
    def test_nonbinary_refused(self):
        for value in (True,2,'0',None):
            with self.assertRaises(ValueError):exact_trusted_rule([dict(self.reports[0],value=value)]+self.reports[1:])
    def test_other_grammar_refused(self):
        for reports in ([],self.reports[:2],self.reports+[dict(self.reports[0],visible_root='4')]):
            with self.assertRaises(ValueError):exact_trusted_rule(reports)
    def test_saved_receipts_and_billing_reconcile(self):
        r=audit();self.assertEqual((r['assigned'],r['valid'],r['graded'],r['correct'],r['confounded_cases']),(16,16,8,0,8))
        self.assertEqual(r['known_attempt_actual_usd'],.00068544)
        self.assertEqual(sum(row['context']=='peer' for row in r['rows']),4)
        self.assertFalse(r['mechanism_identified'])

if __name__=='__main__':unittest.main()
