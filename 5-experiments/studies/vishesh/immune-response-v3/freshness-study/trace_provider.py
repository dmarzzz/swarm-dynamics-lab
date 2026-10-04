"""Credential-free experimental transport records; never log headers or env."""
import hashlib,json,time,urllib.error,urllib.request,os
from durable_provider import DurablePolicy

def http_diagnostics(exc):
 """Allowlisted error metadata only; never retain provider messages/headers."""
 out={}
 try:
  retry=exc.headers.get('Retry-After','')
  if retry.isascii() and retry.isdigit() and len(retry)<=5 and int(retry)<=86400:out['retry_after_seconds']=int(retry)
 except Exception:pass
 try:
  raw=exc.read(4097)
  if len(raw)<=4096:
   category=json.loads(raw).get('error',{}).get('type')
   if category in {'invalid_request_error','authentication_error','permission_error','not_found_error','request_too_large','rate_limit_error','api_error','overloaded_error'}:out['error_category']=category
 except Exception:pass
 return out

class TracePolicy(DurablePolicy):
 def record(self,row):
  path=self.usage_path.parent/'transport.jsonl';path.parent.mkdir(parents=True,exist_ok=True)
  with path.open('a') as f:f.write(json.dumps(row)+'\n');f.flush();os.fsync(f.fileno())
 def complete(self,request,fallback):
  body={'model':self.model,'system':request['instructions'],'temperature':0,'max_tokens':self.max_output,'messages':[{'role':'user','content':json.dumps(request['observation'],sort_keys=True)}],'output_config':{'format':{'type':'json_schema','schema':request['response_schema']}}}
  encoded=json.dumps(body).encode()
  if len(encoded)>self.max_input_bytes:raise ValueError('input_bound_exceeded')
  request_id=self.reserve(encoded)
  self.record({'kind':'request','request_id':request_id,'request_hash':hashlib.sha256(encoded).hexdigest(),'body':body,'at':time.time()})
  headers={'Content-Type':'application/json','x-api-key':self.key,'anthropic-version':'2023-06-01'}
  if self.workspace:headers['anthropic-workspace-id']=self.workspace
  req=urllib.request.Request('https://api.anthropic.com/v1/messages',data=encoded,headers=headers)
  try:
   with urllib.request.urlopen(req,timeout=self.timeout) as r:raw=r.read(1_000_001)
   if len(raw)>1_000_000:raise ValueError('response_bound_exceeded')
   result=json.loads(raw)
  except Exception as exc:
   state='http_'+str(exc.code) if isinstance(exc,urllib.error.HTTPError) else 'transport_or_decode_'+type(exc).__name__
   self.finish(request_id,state);diagnostics=http_diagnostics(exc) if isinstance(exc,urllib.error.HTTPError) else {};self.record({'kind':'transport_error','request_id':request_id,'state':state,'at':time.time(),**diagnostics});raise ValueError(state) from None
  self.finish(request_id,'response_received',result.get('usage'))
  self.record({'kind':'response','request_id':request_id,'body':{k:result[k] for k in ['id','model','stop_reason','usage','content'] if k in result},'at':time.time()})
  if result.get('stop_reason')!='end_turn':raise ValueError('incomplete_output')
  return json.loads(result['content'][0]['text'])
