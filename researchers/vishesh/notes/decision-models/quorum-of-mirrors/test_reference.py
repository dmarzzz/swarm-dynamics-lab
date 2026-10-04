"""Hand-authored software fixtures only; no experiment assignments or model calls."""
import unittest
from dataclasses import replace
from reference import Report, actor_packet, oracle_posterior, evidence_score, committee, summarize, valid_response


def fixture(counts=(3, 3, 3), hide=False):
    return [Report(f'report-{i}-{j}', f'root-{i}', None if hide and i in (0, 1) else f'root-{i}',
                   (1, 0, 0)[i], .8)
            for i, count in enumerate(counts) for j in range(count)]


def vote(choice, probability=.5):
    return dict(choice=choice, p_one=probability)


class EvidenceContracts(unittest.TestCase):
    def test_hand_derived_posterior(self):
        # Prior odds 1, likelihood odds 4*(1/4)*(1/4)=1/4; posterior 1/5.
        self.assertAlmostEqual(oracle_posterior(fixture()), .2)

    def test_repetition_does_not_change_root_posterior(self):
        for counts in ((3,3,3), (7,1,1), (1,7,1), (1,1,7)):
            self.assertAlmostEqual(oracle_posterior(fixture(counts)), .2)

    def test_naive_amplifies_copy_count(self):
        self.assertAlmostEqual(evidence_score(actor_packet(fixture()), 'naive'), 1/65)
        self.assertAlmostEqual(evidence_score(actor_packet(fixture((7,1,1))), 'naive'), 1024/1025)

    def test_full_lineage_dedup_matches_oracle(self):
        for counts in ((3,3,3), (7,1,1), (1,7,1), (1,1,7)):
            for policy in ('visible', 'capped'):
                self.assertAlmostEqual(evidence_score(actor_packet(fixture(counts)), policy), .2)

    def test_opaque_cap_and_visible_failure_are_distinguished(self):
        packet = actor_packet(fixture((7,1,1), hide=True))
        self.assertAlmostEqual(evidence_score(packet, 'visible'), 1024/1025)
        self.assertAlmostEqual(evidence_score(packet, 'capped'), .5)
        # This selected fixture is not evidence that capping is generally optimal.

    def test_hidden_ancestry_nonidentifiability(self):
        reports = fixture((7,1,1), hide=True)
        alternative = [replace(r, true_root=r.report_id) if r.visible_root is None else r for r in reports]
        self.assertEqual(actor_packet(reports), actor_packet(alternative))
        self.assertNotAlmostEqual(oracle_posterior(reports), oracle_posterior(alternative))
        # Alternative has a different root count: information-limit fixture, outside QM-2 generator.

    def test_capping_can_discard_useful_independent_evidence(self):
        reports = [replace(r, bit=1 if r.true_root in ('root-0', 'root-1') else 0)
                   for r in fixture(hide=True)]
        self.assertAlmostEqual(oracle_posterior(reports), .8)
        self.assertAlmostEqual(evidence_score(actor_packet(reports), 'capped'), .5)

    def test_truth_and_hidden_root_do_not_enter_packet(self):
        packet = actor_packet(fixture(hide=True))
        self.assertEqual(set(packet[0]), {'report_id','visible_root','bit','q'})
        changed = [replace(r, true_root='renamed-' + r.true_root) if r.visible_root is None else r
                   for r in fixture(hide=True)]
        self.assertEqual(packet, actor_packet(changed))
        packet[0]['truth'] = 1
        with self.assertRaises(ValueError):
            evidence_score(packet, 'visible')

    def test_invalid_ancestry_fails_closed(self):
        reports = fixture()
        for corrupt in (replace(reports[1], bit=0), replace(reports[1], q=.7),
                        replace(reports[1], visible_root=None), replace(reports[1], report_id=reports[0].report_id)):
            with self.subTest(corrupt=corrupt):
                with self.assertRaises(ValueError):
                    actor_packet([reports[0], corrupt, *reports[2:]])

    def test_permutation_and_label_symmetry(self):
        reports = fixture((7,1,1), hide=True)
        flipped = [replace(r, bit=1-r.bit) for r in reports]
        for policy in ('naive', 'visible', 'capped'):
            p = evidence_score(actor_packet(reports), policy)
            self.assertAlmostEqual(p, evidence_score(actor_packet(list(reversed(reports))), policy))
            self.assertAlmostEqual(1-p, evidence_score(actor_packet(flipped), policy))

    def test_quorum_does_not_shrink_on_failures(self):
        self.assertEqual(committee([vote('ONE')]*2 + [None]*3), 'DEFER')
        self.assertEqual(committee([vote('ONE')]*3 + [None]*2), 'ONE')
        self.assertEqual(committee([vote('DEFER')]*5), 'DEFER')
        with self.assertRaises(ValueError):
            committee([vote('ONE')]*3)

    def test_response_contract(self):
        for bad in (None, {}, vote('BAD'), vote('ONE', float('nan')), vote('ONE', True),
                    vote('ONE', 1.1), dict(choice='ONE', p_one=.9, truth=1)):
            self.assertFalse(valid_response(bad))

    def test_all_assigned_denominator_and_unanimity(self):
        outcomes = {'a': (1, [vote('ONE', .9)]*5),
                    'b': (1, [vote('ZERO', .1)]*5),
                    'c': (1, [vote('ONE')]*2+[None]*3)}
        s = summarize(['a','b','c','d'], outcomes)
        self.assertEqual((s['correct'],s['wrong'],s['defer'],s['unstarted']), (1,1,1,1))
        self.assertEqual(s['accuracy_all_assigned'], .25)
        self.assertEqual(s['wrong_unanimous'], 1)
        self.assertEqual(s['invalid_slots'], 3)
        self.assertEqual(s['valid_probabilities'], 12)
        self.assertAlmostEqual(s['brier_valid'], (5*.01+5*.81+2*.25)/12)
        with self.assertRaises(ValueError):
            summarize(['a'], outcomes)

    def test_missing_probabilities_are_not_zero(self):
        self.assertIsNone(summarize(['a'], {})['brier_valid'])
        with self.assertRaises(ValueError):
            summarize(['a','a'], {})
        with self.assertRaises(ValueError):
            summarize([], {})


if __name__ == '__main__':
    unittest.main()
