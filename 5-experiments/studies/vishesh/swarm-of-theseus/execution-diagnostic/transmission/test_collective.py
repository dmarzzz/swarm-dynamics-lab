import unittest
import collective
class CollectiveTests(unittest.TestCase):
    def test_receipts_and_counterfactual_edges(self):
        self.assertEqual(collective.validate()['distinct_cases'],8)
    def test_every_required_peer_changes_the_decision(self):
        receipts=collective.fixtures()[0][2]
        for peer in ('b','e'):
            self.assertEqual(collective.decide(('b','e'),[r for r in receipts if r['who']!=peer],1),'defer')
    def test_no_evidence_cannot_authorize(self):
        self.assertEqual(collective.decide(('b','e'),[],1),'defer')
