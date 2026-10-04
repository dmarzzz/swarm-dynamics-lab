import unittest
from decimal import Decimal
from provider import microdollars
class Money(unittest.TestCase):
    def test_conservative_rounding(self):
        self.assertEqual(microdollars('0.0000001'),1)
        self.assertEqual(microdollars(Decimal('0.01')),10000)
        self.assertEqual(microdollars('0'),0)
        for invalid in ('NaN','Infinity','-1'):
            with self.assertRaises(ValueError):microdollars(invalid)
if __name__=='__main__':unittest.main()

class ChildBoundary(unittest.TestCase):
    def test_http_timeout_and_missing_credential_are_safe(self):
        from unittest.mock import patch,Mock
        import urllib.error
        from provider import request_child
        for error,code in [(urllib.error.HTTPError('https://example.invalid',429,'private body',{},None),'http_429'),(TimeoutError('private timeout details'),'provider_deadline')]:
            connection=Mock()
            with patch('provider.os.environ.get',return_value='test-only-placeholder'),patch('provider.urllib.request.urlopen',side_effect=error):
                request_child(connection,{},1)
            self.assertEqual(connection.send.call_args.args[0],{'ok':False,'failure':code})
        connection=Mock()
        with patch('provider.os.environ.get',return_value=None):request_child(connection,{},1)
        self.assertEqual(connection.send.call_args.args[0],{'ok':False,'failure':'credential_unavailable'})
