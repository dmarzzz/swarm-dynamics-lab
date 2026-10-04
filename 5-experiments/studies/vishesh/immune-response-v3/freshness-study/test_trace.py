import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import freshness
from trace_provider import TracePolicy
class Reply:
 def __init__(self,obj):self.raw=json.dumps(obj).encode()
 def __enter__(self):return self
 def __exit__(self,*a):pass
 def read(self,n):return self.raw[:n]
class TraceTests(unittest.TestCase):
 def run_case(self,response):
  with tempfile.TemporaryDirectory() as td:
   p=TracePolicy.__new__(TracePolicy);p.usage_path=Path(td)/'usage.jsonl';p.model='fixture-model';p.max_output=512;p.max_input_bytes=16000;p.timeout=1;p.key='TEST-KEY-NEVER-LOG';p.workspace='TEST-ROUTING-NEVER-LOG';p.reserve=lambda encoded:'fixture-request';finished=[];p.finish=lambda *a:finished.append(a)
   request={'instructions':'Synthetic fixture only','observation':{'observed':True},'response_schema':{'type':'object'}}
   with patch('urllib.request.urlopen',return_value=Reply(response)):
    with self.assertRaises(ValueError):p.complete(request,None)
   raw=(Path(td)/'transport.jsonl').read_text();self.assertNotIn(p.key,raw);self.assertNotIn(p.workspace,raw);self.assertNotIn('headers',raw);rows=[json.loads(x) for x in raw.splitlines()];self.assertEqual([x['kind'] for x in rows],['request','response']);self.assertEqual(finished[0][1],'response_received');return rows
 def test_malformed_action_preserved_before_parse(self):
  rows=self.run_case({'stop_reason':'end_turn','usage':{'input_tokens':1,'output_tokens':2},'content':[{'type':'text','text':'not-json'}]});self.assertEqual(rows[1]['body']['content'][0]['text'],'not-json')
 def test_refusal_stop_reason_preserved(self):
  rows=self.run_case({'stop_reason':'refusal','usage':{'input_tokens':1,'output_tokens':2},'content':[]});self.assertEqual(rows[1]['body']['stop_reason'],'refusal')
class HttpDiagnosticTests(unittest.TestCase):
 def error(self,body,retry):
  import io,urllib.error
  return urllib.error.HTTPError('https://fixture.invalid',429,'failure',{'Retry-After':retry,'Authorization':'SECRET-HEADER'},io.BytesIO(body))
 def test_allowlist_excludes_messages_and_headers(self):
  from trace_provider import http_diagnostics
  result=http_diagnostics(self.error(json.dumps({'error':{'type':'rate_limit_error','message':'SECRET-BODY'}}).encode(),'12'))
  self.assertEqual(result,{'error_category':'rate_limit_error','retry_after_seconds':12});self.assertNotIn('SECRET',json.dumps(result))
 def test_untrusted_categories_and_retry_values_omitted(self):
  from trace_provider import http_diagnostics
  for raw in [b'not-json',b'x'*4097,json.dumps({'error':{'type':'SECRET-CATEGORY'}}).encode()]:
   self.assertEqual(http_diagnostics(self.error(raw,'SECRET-RETRY')), {})
if __name__=='__main__':unittest.main()
