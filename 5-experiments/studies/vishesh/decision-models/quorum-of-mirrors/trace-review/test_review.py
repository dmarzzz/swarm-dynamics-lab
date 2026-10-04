import copy
import unittest
from audit_traces import audit
from development import bundles,evaluate,resolve,new_group

class TraceReviewTests(unittest.TestCase):
    def test_all_attempts_and_missingness(self):
        d=audit();self.assertEqual((d['assigned_total'],d['started_total'],d['retained_valid_answers'],d['unstarted_total']),(96,49,48,47))
        self.assertEqual(len(d['cells']),96)
        lost=[c for c in d['cells'] if c['grade']=='failed_response_missing'];self.assertEqual(len(lost),1);self.assertIsNone(lost[0]['response'])
    def test_successes_misses_and_partial_not_excluded(self):
        d=audit();self.assertEqual(len(d['graded_misses']),11)
        self.assertEqual(sum(c['grade']=='correct' for c in d['cells']),29)
        self.assertEqual(sum(c['grade']=='ungraded_partial' for c in d['cells']),8)
    def test_repeat_disagreement_retained(self):
        self.assertEqual(audit()['s0_repeats']['choice_agreement'],14)
    def test_bundle_counts_and_label_separation(self):
        rows=bundles();self.assertEqual(len(rows),24)
        self.assertEqual(len({r['id'] for r in rows}),24)
        for row in rows:
            self.assertNotIn('expected_receipt',row['actor']);self.assertNotIn('family',row['actor'])
        self.assertEqual(sum(r['expected_receipt'] is not None for r in rows),15)
    def test_hybrid_solves_development_but_not_generalization(self):
        r=evaluate(bundles())['summary']['hybrid']
        self.assertEqual((r['correct'],r['resolved_correct'],r['incorrect_admissions'],r['false_new_groups']),(24,15,0,0))
    def test_identical_wording_does_not_prove_same_acquisition(self):
        ambiguous=[r for r in bundles() if r['family']=='identical_independent' and r['expected_receipt'] is None]
        self.assertEqual(len(ambiguous),3)
        for row in ambiguous:self.assertIsNone(resolve(row['actor'],'hybrid'))
    def test_missing_receipt_not_inferred_from_similar_text(self):
        for row in bundles():
            if row['family']=='missing':self.assertIsNone(resolve(row['actor'],'hybrid'))
    def test_common_cause_blocks_new_group_despite_correct_mapping(self):
        for row in bundles():
            if row['family']=='common_cause':
                got=resolve(row['actor'],'hybrid');self.assertEqual(got,row['expected_receipt']);self.assertFalse(new_group(row['actor'],got))
    def test_order_invariance_and_unknown_ref(self):
        for row in bundles():
            actor=copy.deepcopy(row['actor']);expected=resolve(actor,'hybrid');actor['receipts'].reverse();self.assertEqual(resolve(actor,'hybrid'),expected)
        actor=copy.deepcopy(bundles()[0]['actor']);actor['report']['receipt_ref']='unknown';self.assertIsNone(resolve(actor,'hybrid'))

if __name__=='__main__':unittest.main()
