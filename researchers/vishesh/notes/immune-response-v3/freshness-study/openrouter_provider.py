"""A5 credential-free remote client; local relay owns OpenRouter authentication."""
import json,os,sqlite3,urllib.request,urllib.error,math
from pathlib import Path
from trace_provider import TracePolicy
from provider import HTTPPolicy
MODEL='anthropic/claude-haiku-4.5'
PROVIDER={'only':['anthropic'],'allow_fallbacks':False,'require_parameters':True}
def wire(request):
 return {'model':MODEL,'provider':{'only':['anthropic'],'allow_fallbacks':False,'require_parameters':True},'temperature':0,'max_tokens':512,'reasoning':{'enabled':False},'stream':False,'messages':[{'role':'system','content':request['instructions']},{'role':'user','content':json.dumps(request['observation'],sort_keys=True)}],'response_format':{'type':'json_schema','json_schema':{'name':'immune_action','strict':True,'schema':request['response_schema']}}}
def validate_wire(body):
 assert set(body)=={'model','provider','temperature','max_tokens','reasoning','stream','messages','response_format'}
 assert body['model']==MODEL and body['provider']==PROVIDER and body['temperature']==0 and body['max_tokens']==512 and body['reasoning']=={'enabled':False} and body['stream'] is False
 assert len(body['messages'])==2 and [x['role'] for x in body['messages']]==['system','user'] and all(set(x)=={'role','content'} and isinstance(x['content'],str) for x in body['messages'])
 f=body['response_format'];assert f['type']=='json_schema' and f['json_schema']['strict'] is True and f['json_schema']['name']=='immune_action'
 assert len(json.dumps(body).encode())<=16000
class OpenRouterPolicy(TracePolicy):
 def __init__(self):
  assert Path(os.environ['SWARM_BUDGET_LEDGER']).is_file()
  HTTPPolicy.__init__(self);assert self.base=='http://127.0.0.1:18765' and not self.key
  self.run_id=os.environ['SWARM_ATTEMPT_ID'];assert self.run_id=='freshness-a6'
  self.usage_path=Path(os.environ['SWARM_USAGE_LOG']);self.actual_usd=0.;self.usage_missing=0
  with sqlite3.connect(self.ledger) as db:assert not db.execute('select count(*) from immune_requests where run_id=?',(self.run_id,)).fetchone()[0]
 def reserve(self,encoded):
  if self.calls>=18:raise ValueError('attempt_limit')
  return super().reserve(encoded)
 def complete(self,request,fallback):
  body=wire(request);validate_wire(body);encoded=json.dumps(body).encode();rid=self.reserve(encoded)
  import hashlib,time
  self.record({'kind':'request','request_id':rid,'request_hash':hashlib.sha256(encoded).hexdigest(),'body':body,'at':time.time()})
  try:
   req=urllib.request.Request(self.base+'/invoke',json.dumps({'request_id':rid,'body':body}).encode(),{'Content-Type':'application/json'})
   with urllib.request.urlopen(req,timeout=60) as r:raw=r.read(1_000_001)
   assert len(raw)<=1_000_000;result=json.loads(raw)
  except Exception as e:
   state='http_'+str(e.code) if isinstance(e,urllib.error.HTTPError) else 'transport_'+type(e).__name__;self.finish(rid,state);self.record({'kind':'transport_error','request_id':rid,'state':state});raise ValueError(state) from None
  self.record({'kind':'response','request_id':rid,'body':result,'at':time.time()})
  u=result.get('usage') or {};normalized={'input_tokens':u.get('prompt_tokens'),'output_tokens':u.get('completion_tokens')};cost=u.get('cost')
  known=all(type(normalized[k]) is int and normalized[k]>=0 for k in normalized) and type(cost) in (int,float) and math.isfinite(cost) and cost>=0
  self.finish(rid,'response_received',normalized if known else None)
  if not known:raise ValueError('missing_usage_or_cost')
  with sqlite3.connect(self.ledger) as db:
   old,reserved=db.execute('select actual_usd,reserved_usd from immune_requests where request_id=?',(rid,)).fetchone();db.execute('update immune_requests set actual_usd=? where request_id=?',(cost,rid))
   if cost>reserved:db.execute('update budget set reserved=reserved+? where id=1',(cost-reserved,))
  self.actual_usd+=cost-old;self.export()
  if cost>reserved:raise ValueError('reservation_exceeded')
  if result.get('model') not in (MODEL,'anthropic/claude-4.5-haiku-20251001') or result.get('provider','').lower()!='anthropic':raise ValueError('served_route_mismatch')
  choice=result['choices'][0]
  if choice['finish_reason']!='stop':raise ValueError('incomplete_output')
  return json.loads(choice['message']['content'])
