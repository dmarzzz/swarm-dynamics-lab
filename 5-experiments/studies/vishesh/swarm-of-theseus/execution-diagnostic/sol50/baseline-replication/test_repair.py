import copy,io,json,unittest,urllib.error
import contract as c,q3_relay as relay

class RepairTests(unittest.TestCase):
 def test_all_phase_families_have_explicit_json_instruction(self):
  for family in ('release','failover','delegation'):
   for phase in ('learn','select','attest','decide','question','teach','commit'):
    self.assertTrue(c.validate_wire(c.wire(phase,family,{})))
 def test_legacy_missing_instruction_rejected_before_reserving(self):
  b=c.wire('learn','release',{});b['messages'][0]['content']=b['messages'][0]['content'].removeprefix('Return exactly one JSON object and no surrounding prose. ')
  with self.assertRaisesRegex(ValueError,'json_instruction_missing'):c.validate_wire(b)
  b['messages'][1]['content']='JSON in user input is insufficient'
  with self.assertRaisesRegex(ValueError,'json_instruction_missing'):c.validate_wire(b)
 def test_error_echoes_never_returned(self):
  marker='SYNTHETIC_PRIVATE_ACTOR_AND_CREDENTIAL_SENTINEL'
  raw=json.dumps({'error':{'code':'invalid_request_error','message':marker,'metadata':{'raw':marker}},'request':marker}).encode()
  error=urllib.error.HTTPError('https://example.invalid/'+marker,400,marker,{'Authorization':marker,'x-request-id':marker},io.BytesIO(raw))
  result=relay.safe_http_error(error)
  self.assertEqual(result['category'],'invalid_request_error');self.assertNotIn(marker,json.dumps(result));self.assertTrue(error.closed)
  self.assertEqual(set(result),{'http_status','category','body_prefix_sha256','body_truncated'})
 def test_untrusted_code_and_malformed_large_body(self):
  for raw in (b'not json',json.dumps({'error':{'code':'PRIVATE_SECRET'}}).encode(),b'X'*10000,json.dumps({'error':[]}).encode()):
   stream=io.BytesIO(raw);e=urllib.error.HTTPError('https://example.invalid',400,'private',{},stream);r=relay.safe_http_error(e)
   self.assertEqual(r['category'],'unclassified');self.assertNotIn('PRIVATE_SECRET',json.dumps(r));self.assertEqual(r['body_truncated'],len(raw)>8192)
 def test_body_read_failure_is_safe(self):
  class Bad(io.BytesIO):
   def read(self,n):raise RuntimeError('PRIVATE_SECRET')
  r=relay.safe_http_error(urllib.error.HTTPError('https://example.invalid',400,'private',{},Bad()))
  self.assertEqual(r['category'],'diagnostic_read_failed');self.assertNotIn('PRIVATE_SECRET',json.dumps(r))
if __name__=='__main__':unittest.main()
