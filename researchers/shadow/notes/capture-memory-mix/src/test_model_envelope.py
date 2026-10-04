"""J009: provider price ceilings and conservative byte-based reservation."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch
import model


class EnvelopeTest(unittest.TestCase):
    def test_dispatch_binds_prices_and_retains_byte_envelope(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(model.Path, 'read_text', return_value='synthetic'):
            policy = model.HTTPPolicy('test', 1, retries=1, concurrency=1, input_usd_per_million=3,
                                      output_usd_per_million=15, ledger=str(Path(temp)/'ledger.json'))
            self.addCleanup(policy.pool.shutdown)
            policy._opener = MagicMock()
            policy._opener.open.side_effect = TimeoutError('synthetic')
            with self.assertRaises(model.ModelFailure):
                policy._request('unicode: ' + '\u2600' * 100)
            req = policy._opener.open.call_args.args[0]
            payload = json.loads(req.data)
            self.assertEqual(payload['provider']['max_price'], {'prompt':3, 'completion':15})
            self.assertEqual(payload['max_tokens'], 6)
            expected = ((len(req.data) + 2048) * 2 * 3 + 8 * 15) / 1e6
            self.assertAlmostEqual(policy.ledger.spent(), expected, places=8)
            self.assertGreater(policy.ledger.spent(), len(req.data) * 3 / 1e6)

    def test_envelope_exceeding_remaining_cap_does_not_dispatch(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(model.Path, 'read_text', return_value='synthetic'):
            policy = model.HTTPPolicy('test', .00001, retries=1, concurrency=1, ledger=str(Path(temp)/'ledger.json'))
            self.addCleanup(policy.pool.shutdown)
            policy._opener = MagicMock()
            with self.assertRaises(model.ModelFailure):
                policy._request('test')
            policy._opener.open.assert_not_called()
            self.assertEqual(policy.calls, 0)


if __name__ == '__main__':
    unittest.main()
