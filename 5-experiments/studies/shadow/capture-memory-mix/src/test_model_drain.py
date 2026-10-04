"""J031: no terminal episode while submitted work can still mutate context."""
from concurrent.futures import ThreadPoolExecutor
import threading
import unittest
from unittest.mock import patch
import model


class DrainTest(unittest.TestCase):
    def policy(self, workers=2):
        policy = object.__new__(model.HTTPPolicy)
        policy.pool = ThreadPoolExecutor(max_workers=workers)
        self.addCleanup(policy.pool.shutdown)
        policy._lock = threading.Lock()
        policy.calls = 0
        return policy

    def test_early_failure_drains_other_running_future(self):
        policy = self.policy()
        slow_started, failed, release, slow_finished = [threading.Event() for _ in range(4)]
        ctx = {'task': {'words': {}}, 'calls': 5}
        def one(agent, words, context, flip):
            with policy._lock:
                policy.calls += 1
            if agent == 'fail':
                self.assertTrue(slow_started.wait(2))
                failed.set()
                raise model.ModelFailure('synthetic')
            slow_started.set()
            self.assertTrue(release.wait(2))
            context['cost_usd'] = 1.25
            slow_finished.set()
            return .5
        policy.one = one
        with ThreadPoolExecutor(max_workers=1) as caller:
            outcome = caller.submit(policy, ['fail', 'slow'], {}, ctx)
            try:
                self.assertTrue(failed.wait(2))
                self.assertFalse(outcome.done())
            finally:
                release.set()
            with self.assertRaises(model.ModelFailure):
                outcome.result(timeout=2)
        self.assertTrue(slow_finished.is_set())
        self.assertEqual(ctx['cost_usd'], 1.25)
        self.assertEqual(ctx['calls'], 7)
        self.assertEqual(ctx['round_failures'], [{'index':0, 'type':'ModelFailure'}])

    def test_success_preserves_input_order(self):
        policy = self.policy()
        def one(agent, *args):
            with policy._lock:
                policy.calls += 1
            return agent / 10
        policy.one = one
        ctx = {'task': {'words': {}}}
        self.assertEqual(policy([3, 1, 2], {}, ctx), [.3, .1, .2])
        self.assertEqual(ctx['calls'], 3)

    def test_empty_batch_has_no_side_effects(self):
        policy = self.policy()
        ctx = {'task': {'words': {}}}
        self.assertEqual(policy([], {}, ctx), [])
        self.assertNotIn('calls', ctx)


if __name__ == '__main__':
    unittest.main()
