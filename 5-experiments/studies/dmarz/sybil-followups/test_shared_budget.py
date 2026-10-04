import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import unittest
from shared_budget import SharedBudget, SharedBudgetError


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'budget.jsonl'
        self.a = SharedBudget(self.path, 'sybil-budget-api')
        self.b = SharedBudget(self.path, 'sybil-newcomer-api')

    def tearDown(self):
        self.tmp.cleanup()

    def test_parallel_cap_is_shared(self):
        def request(i):
            try:
                (self.a if i % 2 else self.b).reserve(str(i), 1_000_000)
                return True
            except SharedBudgetError:
                return False
        with ThreadPoolExecutor(max_workers=8) as pool:
            self.assertEqual(sum(pool.map(request, range(64))), 60)
        self.assertEqual(self.b.transact()['committed_usd'], 60)

    def test_settled_actual_releases_only_known_unused_charge(self):
        self.a.reserve('known', 40_000_000)
        self.b.reserve('unknown', 20_000_000)
        self.a.settle('known', 1_000_000)
        self.assertEqual(self.b.transact()['committed_usd'], 21)
        self.b.reserve('new', 39_000_000)
        with self.assertRaises(SharedBudgetError):
            self.a.reserve('overflow', 1)
        self.assertEqual(self.a.transact()['held_usd'], 59)

    def test_duplicate_and_unreserved_settlement_fail(self):
        self.a.reserve('one', 10)
        with self.assertRaises(SharedBudgetError):
            self.a.reserve('one', 10)
        with self.assertRaises(SharedBudgetError):
            self.b.settle('one', 1)
        self.a.settle('one', 5)
        with self.assertRaises(SharedBudgetError):
            self.a.settle('one', 5)

    def test_unknown_and_partial_write_fail_closed(self):
        self.a.reserve('unknown', 60_000_000)
        reconstructed = SharedBudget(self.path, 'sybil-newcomer-api')
        with self.assertRaises(SharedBudgetError):
            reconstructed.reserve('more', 1)
        with self.path.open('a') as stream:
            stream.write('{')
        with self.assertRaises(json.JSONDecodeError):
            reconstructed.transact()


if __name__ == '__main__':
    unittest.main()
