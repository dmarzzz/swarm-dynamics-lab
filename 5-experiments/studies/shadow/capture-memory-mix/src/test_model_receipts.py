"""J010: mismatched model/provider responses are retained but never accepted."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch
import model


class ReceiptTest(unittest.TestCase):
    def test_mismatch_and_missing_receipts_invalid_without_erasing_response(self):
        cases = [{'model':'other/model', 'provider':'TestProvider'},
                 {'provider':'TestProvider'}, {'model':'test'},
                 {'model':'test', 'provider':'OtherProvider'}]
        for identity in cases:
            with self.subTest(identity=identity), tempfile.TemporaryDirectory() as temp:
                path = Path(temp)/'ledger.json'
                with patch.object(model.Path, 'read_text', return_value='synthetic-key'):
                    policy = model.HTTPPolicy('test', 1, concurrency=1, ledger=str(path),
                                              provider_order=['TestProvider'])
                self.addCleanup(policy.pool.shutdown)
                response = identity | {'choices':[{'message':{'content':'synthetic-key'}}], 'usage':{'cost':0}}
                policy._opener = MagicMock()
                policy._opener.open.return_value.__enter__.return_value.read.return_value = json.dumps(response).encode()
                with self.assertRaises(model.ModelFailure):
                    policy._request('test')
                text = (Path(temp)/'ledger-receipts.jsonl').read_text()
                self.assertNotIn('synthetic-key', text)
                receipt = json.loads(text)
                self.assertEqual(receipt['requested_model'], 'test')
                self.assertEqual(receipt['response'].get('model'), identity.get('model'))
                self.assertEqual(receipt['response']['choices'][0]['message']['content'], '[REDACTED]')
                self.assertEqual(json.loads(path.read_text())['calls'], 1)

    def test_matching_model_and_provider_are_accepted(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(model.Path, 'read_text', return_value='synthetic-key'):
                policy = model.HTTPPolicy('test', 1, concurrency=1, ledger=str(Path(temp)/'ledger.json'))
            self.addCleanup(policy.pool.shutdown)
            policy._opener = MagicMock()
            policy._opener.open.return_value.__enter__.return_value.read.return_value = b'{"model":"test","provider":"TestProvider","choices":[{}],"usage":{"cost":0}}'
            self.assertEqual(policy._request('test')['model'], 'test')
            self.assertTrue((Path(temp)/'ledger-receipts.jsonl').exists())


if __name__ == '__main__':
    unittest.main()
