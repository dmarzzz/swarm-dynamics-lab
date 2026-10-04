"""J006: durable dollar admission shared by adapters, threads and processes."""
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch
import model


def reserve_from_process(path):
    try:
        model.Ledger(Path(path)).reserve('test', .25, 1)
        return 1
    except model.ModelFailure:
        return 0


class ReservationTest(unittest.TestCase):
    def test_processes_share_one_admission_cap(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'ledger.json'
            with ProcessPoolExecutor(max_workers=4) as pool:
                self.assertEqual(sum(pool.map(reserve_from_process, [str(path)] * 32)), 4)
            d = json.loads(path.read_text())
            self.assertEqual(d['spent_usd'], 1)
            self.assertEqual(d['calls'], 4)
            self.assertEqual(len(d['reservations']), 4)
            with self.assertRaises(model.ModelFailure):
                model.Ledger(path).reserve('restarted', .01, 1)

    def test_typed_settlement_releases_only_known_liability(self):
        with tempfile.TemporaryDirectory() as temp:
            ledger = model.Ledger(Path(temp)/'ledger.json')
            ident = ledger.reserve('test', 1, 1)
            ledger.settle(ident, .25)
            self.assertEqual(ledger.spent(), .25)
            with self.assertRaises(model.ModelFailure):
                ledger.settle(ident, 0)
            second = ledger.reserve('test', .75, 1)
            with self.assertRaises(model.ModelFailure):
                ledger.settle(second, -.5)
            self.assertEqual(ledger.spent(), 1)

    def test_reservation_breach_retains_actual_and_blocks_new_calls(self):
        with tempfile.TemporaryDirectory() as temp:
            ledger = model.Ledger(Path(temp)/'ledger.json')
            ident = ledger.reserve('test', .25, 1)
            with self.assertRaises(model.ModelFailure):
                ledger.settle(ident, .5)
            self.assertEqual(ledger.spent(), .5)
            with self.assertRaises(model.ModelFailure):
                model.Ledger(ledger.path).reserve('test', .1, 1)

    def test_two_adapters_cannot_both_dispatch_against_one_remaining_budget(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(model.Path, 'read_text', return_value='synthetic'), \
             patch.object(model.time, 'sleep'):
            path = str(Path(temp)/'ledger.json')
            policies = [model.HTTPPolicy('test', .0002, retries=1, concurrency=1, ledger=path) for _ in range(2)]
            for policy in policies:
                self.addCleanup(policy.pool.shutdown)
                policy._opener = MagicMock()
                policy._opener.open.side_effect = TimeoutError('synthetic')
            def attempt(policy):
                with self.assertRaises(model.ModelFailure):
                    policy._request('test')
            with ThreadPoolExecutor(max_workers=2) as pool:
                list(pool.map(attempt, policies))
            self.assertEqual(sum(p._opener.open.call_count for p in policies), 1)
            self.assertEqual(sum(p.calls for p in policies), 1)
            self.assertGreater(policies[0].ledger.spent(), 0)
            self.assertLessEqual(policies[0].ledger.spent(), .0002)


if __name__ == '__main__':
    unittest.main()
