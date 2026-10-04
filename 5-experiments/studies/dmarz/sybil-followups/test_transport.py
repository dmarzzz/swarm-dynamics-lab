"""Run with PYTHONPATH set to either study's src; never sends network traffic."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import provider
import study


class Response:
    def __init__(self, data): self.data = data
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self): return json.dumps(self.data).encode()


class TransportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.env = patch.dict(os.environ, {
            'SWARM_MODEL_API_KEY': 'test-placeholder',
            'SWARM_MODEL_WORKSPACE_ID': 'test-placeholder',
            'SYBIL_FOLLOWUPS_LEDGER': str(self.root / 'shared'),
        })
        self.env.start()
        self.ledger = provider.Ledger(self.root / 'study')
        self.packet = {'skills': list(range(6)), 'reports': []}

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def response(self, text=None):
        return {'model': study.design()['model'], 'stop_reason': 'end_turn',
                'usage': {'input_tokens': 100, 'output_tokens': 40},
                'content': [{'type': 'text', 'text': text if text is not None else json.dumps({'values': {str(i): None for i in range(6)}})}]}

    def test_known_response_settles_once(self):
        api = provider.Anthropic(self.ledger, opener=lambda *a, **k: Response(self.response()))
        answer, accounting = api.call(self.packet, 'one')
        self.assertEqual(accounting['actual_usd'], .0003)
        self.assertEqual(api.shared.transact()['held_usd'], 0)
        self.assertEqual(api.shared.transact()['actual_usd'], .0003)
        with self.assertRaises(provider.CallFailure): api.call(self.packet, 'one')
        self.assertEqual(self.ledger.transact()['attempted_calls'], 1)

    def test_transport_failure_retains_full_reservation(self):
        def failed(*a, **k): raise urllib.error.HTTPError('redacted', 429, 'rate', None, None)
        api = provider.Anthropic(self.ledger, opener=failed)
        with self.assertRaises(provider.CallFailure) as error: api.call(self.packet, 'bad')
        self.assertEqual(error.exception.category, 'http_429')
        self.assertTrue(error.exception.accounting['attempted'])
        self.assertGreater(api.shared.transact()['held_usd'], 0)
        self.assertEqual(api.shared.transact()['settled'], 0)

    def test_malformed_billed_response_is_charged(self):
        api = provider.Anthropic(self.ledger, opener=lambda *a, **k: Response(self.response('{')))
        with self.assertRaises(provider.CallFailure) as error: api.call(self.packet, 'malformed')
        self.assertEqual(error.exception.category, 'invalid_structured_answer')
        self.assertEqual(error.exception.accounting['actual_usd'], .0003)
        self.assertEqual(api.shared.transact()['actual_usd'], .0003)

    def test_local_refusal_does_not_charge_shared_guard(self):
        self.ledger.transact({'type': 'reserve', 'call_id': 'already-local', 'micro_usd': 1})
        api = provider.Anthropic(self.ledger, opener=lambda *a, **k: self.fail('network called'))
        with self.assertRaises(provider.CallFailure): api.call(self.packet, 'already-local')
        self.assertEqual(api.shared.transact()['committed_usd'], 0)


if __name__ == '__main__': unittest.main()
