"""J011 endpoint admission tests, no credentials read and no model calls."""
import unittest
from unittest.mock import patch
import model


class EndpointTest(unittest.TestCase):
    def test_unapproved_endpoints_fail_before_key_read_or_pool(self):
        for base in ['https://example.org/api/v1', 'http://openrouter.ai/api/v1',
                     'https://openrouter.ai.example.org/api/v1',
                     'https://openrouter.ai@evil.invalid/api/v1',
                     'https://openrouter.ai/api/v1?destination=evil',
                     'https://openrouter.ai/api/v1#fragment',
                     'https://openrouter.ai/other', 'https://openrouter.ai:444/api/v1']:
            with self.subTest(base=base), patch.object(model.Path, 'read_text') as read, \
                 patch.object(model, 'ThreadPoolExecutor') as pool:
                with self.assertRaises(model.ModelFailure):
                    model.HTTPPolicy('test/model', 1, base_url=base)
                read.assert_not_called()
                pool.assert_not_called()

    def test_expected_endpoint_reaches_key_admission(self):
        for base in ['https://openrouter.ai/api/v1', 'https://openrouter.ai/api/v1/']:
            with patch.object(model.Path, 'read_text', return_value='') as read:
                with self.assertRaisesRegex(model.ModelFailure, 'empty key'):
                    model.HTTPPolicy('test/model', 1, base_url=base)
                read.assert_called_once()

    def test_redirects_never_create_forwarded_requests(self):
        handler = model.NoCredentialRedirect()
        for code in [301, 302, 303, 307, 308]:
            with self.subTest(code=code), self.assertRaises(model.ModelFailure):
                handler.redirect_request(None, None, code, 'redirect', {}, 'https://evil.invalid/')


if __name__ == '__main__':
    unittest.main()
