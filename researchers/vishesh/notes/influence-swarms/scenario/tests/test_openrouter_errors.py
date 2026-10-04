import io,json,sys,unittest,urllib.error
from pathlib import Path
from unittest.mock import Mock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
from openrouter_errors import safe_openrouter_error
class OpenRouterErrorTests(unittest.TestCase):
 def error(self,body):return urllib.error.HTTPError('https://private.invalid',400,'private',{},io.BytesIO(json.dumps(body).encode()))
 def test_nested_schema_reason_without_raw(self):
  body={'error':{'message':'Provider returned error','metadata':{'raw':json.dumps({'error':{'message':'Schema is too complex for compilation. PRIVATE_SENTINEL'}}),'secret':'PRIVATE_SENTINEL'}}}
  out=safe_openrouter_error(self.error(body));self.assertEqual(out['reported_reason'],'schema_complexity');self.assertNotIn('PRIVATE_SENTINEL',json.dumps(out));self.assertFalse(out['retry_permitted'])
 def test_plain_unknown_and_ambiguous(self):
  for message,label in [('Invalid schema property','schema_invalid_or_unsupported'),('Insufficient credits','insufficient_credits'),('Rate limit exceeded','rate_limit'),('Invalid request PRIVATE_SENTINEL','unknown'),('rate limit; insufficient credits','ambiguous')]:
   out=safe_openrouter_error(self.error({'error':{'message':message}}));self.assertEqual(out['reported_reason'],label);self.assertNotIn('PRIVATE_SENTINEL',json.dumps(out))
 def test_bounded_malformed_and_failed_read(self):
  for raw,label in [(b'x'*8193,'oversized'),(b'bad','malformed'),(b'[]','unknown_envelope')]:
   error=self.error({});error.read=Mock(return_value=raw);out=safe_openrouter_error(error);self.assertEqual(out['error_body_status'],label);error.read.assert_called_once_with(8193)
  error=self.error({});error.read=Mock(side_effect=OSError('PRIVATE_SENTINEL'));self.assertEqual(safe_openrouter_error(error)['error_body_status'],'unreadable')
