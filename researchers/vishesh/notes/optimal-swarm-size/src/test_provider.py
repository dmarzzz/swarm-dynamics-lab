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

class Anthropic(unittest.TestCase):
    def test_request_transform_and_usage_accounting(self):
        from provider import native_payload,usage_charge
        from failures import SafeFailure
        cfg={'model':'claude-haiku-4-5-20251001','max_output_tokens':4096,'input_usd_per_token':0.000001,'output_usd_per_token':0.000005}
        body=native_payload([{'role':'system','content':'JSON only'},{'role':'user','content':'task'}],cfg)
        self.assertEqual(body['system'],'JSON only');self.assertEqual(body['messages'],[{'role':'user','content':'task'}])
        self.assertEqual(body['service_tier'],'standard_only');self.assertNotIn('tools',body)
        self.assertEqual(usage_charge({'input_tokens':100,'output_tokens':20},cfg),200)
        for usage in ({},{'input_tokens':True,'output_tokens':1},{'input_tokens':1,'output_tokens':-1}):
            with self.assertRaisesRegex(SafeFailure,'usage_missing'):usage_charge(usage,cfg)
        with self.assertRaisesRegex(SafeFailure,'unexpected_cache_usage'):
            usage_charge({'input_tokens':1,'output_tokens':1,'cache_creation_input_tokens':2},cfg)
