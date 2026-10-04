import copy
import unittest
from collections import Counter
from build import cases,predict,evaluate

class ClaimCaseTests(unittest.TestCase):
    def test_units_labels_and_unique_ids(self):
        rows=cases();self.assertEqual(len(rows),32);self.assertEqual(len({r['id'] for r in rows}),32)
        self.assertEqual(Counter(r['scenario_id'] for r in rows),{f'CF-{i:02}':4 for i in range(8)})
        self.assertEqual(Counter(r['gold']['relation'] for r in rows),{'SUPPORTED':16,'CONTRADICTED':8,'NOT_ESTABLISHED':8})
    def test_gold_absent_from_actor_and_evidence_spans_present(self):
        for r in cases():
            a=r['actor'];self.assertEqual(set(a),{'contract','receipt','reports'})
            self.assertEqual(a['reports'][0]['receipt_id'],a['receipt']['id'])
            self.assertTrue(r['gold']['rationale'])
            for span in r['gold']['evidence_spans']:self.assertIn(span,a['receipt']['source_sentences'])
    def test_source_fixed_across_each_four_claims(self):
        rows=cases()
        for i in range(0,32,4):
            group=rows[i:i+4]
            for r in group:self.assertEqual(r['actor']['receipt'],group[0]['actor']['receipt'])
            self.assertEqual(len({r['actor']['reports'][0]['claim'] for r in group}),4)
    def test_repeated_copies_and_order_do_not_add_evidence(self):
        for r in cases():
            for policy in ('abstain_all','literal_clause','overlap_diagnostic'):
                original=predict(r['actor'],policy);a=copy.deepcopy(r['actor'])
                a['reports']*=9;a['receipt']['source_sentences'].reverse()
                self.assertEqual(predict(a,policy),original)
    def test_literal_positive_controls(self):
        for r in cases()[::4]:self.assertEqual(predict(r['actor'],'literal_clause'),'SUPPORTED')
    def test_same_accuracy_can_hide_false_support(self):
        s=evaluate(cases())['summary'];self.assertEqual(s['literal_clause']['correct'],s['overlap_diagnostic']['correct'])
        self.assertEqual(s['literal_clause']['false_support'],0);self.assertEqual(s['overlap_diagnostic']['false_support'],7)
    def test_missing_time_and_completion_not_negative_truth(self):
        rows={r['id']:r for r in cases()}
        for name in ('CF-00-3','CF-01-3','CF-05-3','CF-07-3'):
            self.assertEqual(rows[name]['gold']['relation'],'NOT_ESTABLISHED')
    def test_all_assignments_retained_for_each_policy(self):
        d=evaluate(cases());self.assertEqual(len(d['outcomes']),96)
        for policy in d['summary']:
            self.assertEqual({x['id'] for x in d['outcomes'] if x['policy']==policy},{r['id'] for r in cases()})
if __name__=='__main__':unittest.main()
