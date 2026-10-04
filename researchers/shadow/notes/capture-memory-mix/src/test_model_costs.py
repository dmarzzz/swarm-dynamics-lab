"""J013: reject malformed/negative accounting, never read a real credential."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch
import model


class CostTest(unittest.TestCase):
    def test_invalid_updates_do_not_change_ledger_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            ledger = model.Ledger(Path(temp) / 'ledger.json')
            ledger.add('test', .5, 1)
            before = ledger.path.read_bytes()
            for usd, calls in [(-1, 0), (float('nan'), 1), (float('inf'), 1), (True, 1),
                               (.1, -1), (.1, 1.5), (.1, True)]:
                with self.subTest(usd=usd, calls=calls), self.assertRaises(model.ModelFailure):
                    ledger.add('test', usd, calls)
                self.assertEqual(ledger.path.read_bytes(), before)

    def test_invalid_rates_and_cap_rejected_before_key_read(self):
        for field in ('input_usd_per_million', 'output_usd_per_million', 'max_cost_usd'):
            for bad in (-1, float('nan'), float('inf')):
                args = {'model':'test', 'max_cost_usd':1, field:bad}
                with self.subTest(field=field, bad=bad), patch.object(model.Path, 'read_text') as read:
                    with self.assertRaises(model.ModelFailure):
                        model.HTTPPolicy(**args)
                    read.assert_not_called()

    def test_invalid_provider_cost_retains_positive_estimate(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(model.Path, 'read_text', return_value='synthetic'):
            policy = model.HTTPPolicy('test', 1, concurrency=1, ledger=str(Path(temp)/'ledger.json'))
            self.addCleanup(policy.pool.shutdown)
            policy._opener = MagicMock()
            for bad in (-1, float('nan'), float('inf'), True, '0.1'):
                policy._opener.open.return_value.__enter__.return_value.read.return_value = json.dumps(
                    {'choices':[{}], 'usage':{'cost':bad}}).encode()
                before = policy.ledger.spent()
                with self.subTest(bad=bad), self.assertRaises(model.ModelFailure):
                    policy._request('test')
                self.assertGreater(policy.ledger.spent(), before)
            policy._opener.open.return_value.__enter__.return_value.read.return_value = b'{"choices":[{}],"usage":{"cost":0}}'
            before = policy.ledger.spent()
            self.assertEqual(policy._request('test')['_cost'], 0)
            self.assertEqual(policy.ledger.spent(), before)


if __name__ == '__main__':
    unittest.main()
