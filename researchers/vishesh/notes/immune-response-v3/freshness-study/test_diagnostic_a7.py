import freshness
import unittest,json,io,itertools,copy
from pathlib import Path
import jsonschema
from diagnostic_errors import safe_error
from openrouter_provider import validate_wire
class Diagnostics(unittest.TestCase):
 def test_equivalent_language_and_wire_bounds(self):
  packet=json.loads(Path(__file__).with_name('diagnostic-a7-packet.json').read_text());schemas=[x['body']['response_format']['json_schema']['schema'] for x in packet]
  for x in packet:validate_wire(x['body'])
  for s in schemas:jsonschema.Draft202012Validator.check_schema(s)
  validators=[jsonschema.Draft202012Validator(s) for s in schemas];admitted=0
  for kind,service,version in itertools.product(['deploy','inspect','refresh','wait','bogus'],['gateway-1','worker-1','store-1','none','bogus'],[-1,0,1,2,3,4,True]):
   a={'action':kind,'service':service,'version':version,'reason':'diagnostic'};v=[s.is_valid(a) for s in validators];self.assertEqual(v[0],v[1]);admitted+=v[0]
   if v[0]:self.assertTrue(v[2])
  self.assertEqual(admitted,10)
  x=copy.deepcopy(packet[0]['body']);y=copy.deepcopy(packet[1]['body']);x.pop('response_format');y.pop('response_format');self.assertEqual(x,y)
 def test_error_redaction_outer_and_nested(self):
  for b in [{'error':{'message':'Invalid schema: additionalProperties must be false SECRET'}},{'error':{'message':'Provider error','metadata':{'raw':json.dumps({'error':{'message':'Invalid schema anyOf type required SECRET'}})}}}]:
   r=safe_error(io.BytesIO(json.dumps(b).encode()));self.assertEqual(r['reported_reason'],'schema_invalid_or_unsupported');self.assertNotIn('SECRET',json.dumps(r));self.assertEqual(r['body_status'],'parsed')
 def test_unknown_and_bounded(self):
  self.assertEqual(safe_error(io.BytesIO(b'x'*8193))['body_status'],'oversized')
  self.assertEqual(safe_error(io.BytesIO(b'not json SECRET'))['body_status'],'malformed')
  self.assertEqual(safe_error(io.BytesIO(b'{"error":{"message":"unknown SECRET"}}'))['reported_reason'],'unknown')
 def test_relay_envelope_only_fixed_values(self):
  b={'error':'provider_http','body_status':'parsed','reported_reason':'schema_invalid_or_unsupported','keywords':['anyOf','SECRET'],'extra':'SECRET'}
  r=safe_error(io.BytesIO(json.dumps(b).encode()));self.assertEqual(r['keywords'],['anyOf']);self.assertNotIn('SECRET',json.dumps(r))
if __name__=='__main__':unittest.main()

class StopRules(unittest.TestCase):
 def test_only_expected_400_continues(self):
  import tempfile
  from unittest.mock import patch
  import diagnostic_a7
  for failure,expected in [('http_400',3),('http_429',1)]:
   class Fake:
    calls=0;actual_usd=0.;usage_missing=0
    def complete(self,request,fallback):
     self.calls+=1;self.usage_missing+=1;raise ValueError(failure)
   with tempfile.TemporaryDirectory() as td,patch.object(diagnostic_a7,'DiagnosticPolicy',Fake),patch.dict('os.environ',{},clear=False):
    out=Path(td)/'out'
    if failure=='http_400':diagnostic_a7.execute(out)
    else:
     with self.assertRaises(ValueError):diagnostic_a7.execute(out)
    self.assertEqual(json.loads((out/'summary.json').read_text())['api_calls'],expected)
