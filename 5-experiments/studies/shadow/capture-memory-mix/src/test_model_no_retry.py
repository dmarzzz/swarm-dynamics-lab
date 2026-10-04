"""J008: each logical request can dispatch once, even with legacy retries > 1."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch
import urllib.error
import model


class NoRetryTest(unittest.TestCase):
    def test_ambiguous_failures_are_not_retried(self):
        failures = [TimeoutError('synthetic'),
                    urllib.error.HTTPError('https://example.invalid', 503, 'unavailable', {}, io.BytesIO(b'')),
                    urllib.error.HTTPError('https://example.invalid', 429, 'limited', {}, io.BytesIO(b''))]
        for failure in failures:
            with self.subTest(failure=type(failure).__name__), tempfile.TemporaryDirectory() as temp, \
                 patch.object(model.Path, 'read_text', return_value='synthetic'), \
                 patch.object(model.time, 'sleep') as sleep:
                policy = model.HTTPPolicy('test', 1, retries=10, concurrency=1, ledger=str(Path(temp)/'ledger.json'))
                self.addCleanup(policy.pool.shutdown)
                policy._opener = MagicMock()
                policy._opener.open.side_effect = failure
                with self.assertRaises(model.ModelFailure):
                    policy._request('test')
                self.assertEqual(policy._opener.open.call_count, 1)
                self.assertEqual(policy.calls, 1)
                self.assertGreater(policy.ledger.spent(), 0)
                sleep.assert_not_called()
                with policy.ledger.path.open() as stream:
                    self.assertEqual(json.load(stream)['calls'], 1)


if __name__ == '__main__':
    unittest.main()
