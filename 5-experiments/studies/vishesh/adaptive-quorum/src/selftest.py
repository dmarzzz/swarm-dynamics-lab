import unittest
import sim


class Tests(unittest.TestCase):
    def test_truth_seed_independent_and_blind(self):
        t = sim.task(7000)
        for seed in (1, 9):
            tape = sim.draw_reports(t, seed, 'clean')
            self.assertNotIn('a_star', str(tape))
            self.assertEqual({r['recommendation'] for step in tape for r in step}, {t['a_star']})

    def test_pairing_and_clean(self):
        rows = sim.run_episode(7000, 1, 'clean', 3, sim.ARMS, {})
        self.assertEqual(len({r['reports_hash'] for r in rows}), 1)
        self.assertTrue(all(r['evaluation']['correct'] for r in rows))
        reversed_rows = sim.run_episode(7000, 1, 'clean', 3, sim.ARMS[::-1], {})
        self.assertEqual([r['decision'] for r in rows], [r['decision'] for r in reversed_rows[::-1]])

    def test_threshold_boundary(self):
        reports = [{'root': str(i % 2)} for i in range(5)]
        votes = ['A'] * 5
        self.assertIsNone(sim.stop(votes, reports, 'fixed', 3, 3))
        self.assertIsNone(sim.stop(votes, reports, 'adaptive', 2, 3))
        self.assertEqual(sim.stop(votes, reports, 'adaptive', 3, 3), 'A')
        reports = [{'root': 'same'}] * 5
        self.assertIsNone(sim.stop(votes, reports, 'adaptive', 3, 3))

    def test_duplicate_invariance(self):
        r = {'root': 'x', 'recommendation': 'A'}
        self.assertEqual(sim.visible([r]), sim.visible([r] * 100))

    def test_failure_recorded(self):
        rows = sim.run_episode(7000, 1, 'clean', 3, sim.ARMS, {'decide': lambda _: 'INVALID'})
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(not r['validity']['ok'] and r['evaluation']['loss'] == 1 for r in rows))

    def test_adversarial_fixture(self):
        rows = sim.run_episode(7000, 1, 'late-correction', 6, sim.ARMS, {})
        self.assertTrue(rows[0]['evaluation']['false_commit'])
        self.assertTrue(rows[1]['evaluation']['correct'])


if __name__ == '__main__':
    unittest.main()
