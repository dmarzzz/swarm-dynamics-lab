"""Offline fault fixtures only; mocked transport, no credentials or network."""
import io
import json
import unittest
from email.message import Message
from urllib.error import HTTPError
from unittest.mock import patch
from provider_diagnostics import BODY_LIMIT, http_failure, retry_seconds
from runner import invoke


def error(body, retry='12'):
    headers = Message()
    headers['Retry-After'] = retry
    headers['Authorization'] = 'DO_NOT_RETAIN'
    raw = body if isinstance(body, bytes) else json.dumps(body).encode()
    return HTTPError('https://fixture.invalid',429,'DO_NOT_RETAIN',headers,io.BytesIO(raw))


class DiagnosticsTests(unittest.TestCase):
    def make_error(self, *args, **kwargs):
        response = error(*args, **kwargs)
        self.addCleanup(response.close)
        return response

    def test_allowlist_and_usage_without_cost_claim(self):
        value = http_failure(self.make_error({'error':{'type':'rate_limit_error','message':'DO_NOT_RETAIN'},
                                   'usage':{'input_tokens':7,'output_tokens':0,'secret':'DO_NOT_RETAIN'}}),0)
        self.assertEqual(value['http_status'],429)
        self.assertEqual(value['provider_error_type'],'rate_limit_error')
        self.assertEqual(value['retry_after_seconds'],12)
        self.assertEqual(value['error_usage'],{'input_tokens':7,'output_tokens':0})
        self.assertNotIn('DO_NOT_RETAIN',json.dumps(value))

    def test_unknown_type_never_guesses_from_message(self):
        for kind in ('billing_DO_NOT_RETAIN',[],None):
            value=http_failure(self.make_error({'error':{'type':kind,'message':'billing quota exhausted DO_NOT_RETAIN'}}),0)
            self.assertEqual(value['provider_error_type'],'unknown')
            self.assertNotIn('DO_NOT_RETAIN',json.dumps(value))

    def test_invalid_usage(self):
        value=http_failure(self.make_error({'usage':{'input_tokens':True,'output_tokens':-1,
             'cache_creation_input_tokens':1.2,'cache_read_input_tokens':2**80}}),0)
        self.assertIsNone(value['error_usage'])

    def test_malformed_and_oversized(self):
        for body in (b'not json DO_NOT_RETAIN',b'[]',b'\xff'):
            self.assertEqual(http_failure(self.make_error(body),0)['error_metadata_state'],'malformed')
        self.assertEqual(http_failure(self.make_error(b'x'*(BODY_LIMIT+1)),0)['error_metadata_state'],'oversized')

    def test_bounded_read_and_failure(self):
        e=self.make_error(b'{}')
        with patch.object(e,'read',side_effect=OSError('DO_NOT_RETAIN')) as read:
            value=http_failure(e,0)
        read.assert_called_once_with(BODY_LIMIT+1)
        self.assertEqual(value['error_metadata_state'],'unavailable')
        self.assertNotIn('DO_NOT_RETAIN',json.dumps(value))

    def test_retry_numeric_date_and_poisoned(self):
        self.assertEqual(retry_seconds('Thu, 01 Jan 1970 00:00:20 GMT',10),10)
        self.assertEqual(retry_seconds('0',10),0)
        for value in ('-1','nan','Infinity','DO_NOT_RETAIN','9'*150,'604801',None):
            self.assertIsNone(retry_seconds(value,10))

    def test_invoke_single_dispatch_no_response_no_cost(self):
        e=self.make_error({'error':{'type':'rate_limit_error','message':'DO_NOT_RETAIN'},'usage':{'input_tokens':3}})
        with patch.dict('os.environ',{'SWARM_MODEL_WORKSPACE_ID':'fixture'}), patch('urllib.request.urlopen',side_effect=e) as request:
            value=invoke({},'DO_NOT_RETAIN',1)
        request.assert_called_once()
        self.assertEqual(value['error'],'http_429')
        self.assertEqual(value['error_usage'],{'input_tokens':3})
        for key in ('value','raw_text','usage','actual_usd'):self.assertIsNone(value[key])
        self.assertFalse(value['response_received'])
        self.assertNotIn('DO_NOT_RETAIN',json.dumps(value))

if __name__=='__main__':unittest.main()
