"""Native calls with transactional spend reservations and durable usage receipts.

Credentials only enter request headers. Receipts contain counts/status/hash, never
headers, credentials, arbitrary exception text, or raw provider responses.
"""
import hashlib,json,os,sqlite3,time,urllib.error,urllib.request,uuid
from pathlib import Path
from study import AnthropicPolicy as PreviousPolicy

class DurablePolicy(PreviousPolicy):
 def __init__(self):
  ledger=Path(os.environ['SWARM_BUDGET_LEDGER'])
  if not ledger.is_file():raise ValueError('existing_budget_ledger_required')
  self.run_id=os.environ['SWARM_ATTEMPT_ID']
  if not self.run_id:raise ValueError('attempt_id_required')
  self.usage_path=Path(os.environ['SWARM_USAGE_LOG'])
  super().__init__()
  with sqlite3.connect(self.ledger) as db:
   db.execute('CREATE TABLE IF NOT EXISTS immune_requests (request_id TEXT PRIMARY KEY, run_id TEXT, request_hash TEXT, state TEXT, reserved_usd REAL, input_tokens INTEGER, output_tokens INTEGER, actual_usd REAL, started REAL, ended REAL)')
   if db.execute('SELECT count(*) FROM immune_requests WHERE run_id=?',(self.run_id,)).fetchone()[0]:raise ValueError('attempt_already_dispatched')

 def reserve(self,encoded):
  cost=((len(encoded)+512)*self.input_rate+self.max_output*self.output_rate)/1e6
  request_id=uuid.uuid4().hex
  with sqlite3.connect(self.ledger,timeout=20) as db:
   db.execute('BEGIN IMMEDIATE')
   cap,used,calls=db.execute('SELECT cap,reserved,calls FROM budget').fetchone()
   count=db.execute('SELECT count(*) FROM immune_requests WHERE run_id=?',(self.run_id,)).fetchone()[0]
   if used+cost>cap or calls>=6500 or count>=120:raise ValueError('persistent_budget_or_attempt_limit')
   db.execute('UPDATE budget SET reserved=?,calls=? WHERE id=1',(used+cost,calls+1))
   db.execute('INSERT INTO immune_requests VALUES (?,?,?,?,?,?,?,?,?,?)',(request_id,self.run_id,hashlib.sha256(encoded).hexdigest(),'reserved_unresolved',cost,None,None,None,time.time(),None))
  self.calls+=1;self.usage_missing+=1
  self.export()
  return request_id

 def finish(self,request_id,state,usage=None):
  usage=usage or {};known=all(type(usage.get(k)) is int and usage[k]>=0 for k in ['input_tokens','output_tokens'])
  actual=(usage['input_tokens']*self.input_rate+usage['output_tokens']*self.output_rate)/1e6 if known else None
  with sqlite3.connect(self.ledger) as db:
   db.execute('UPDATE immune_requests SET state=?,input_tokens=?,output_tokens=?,actual_usd=?,ended=? WHERE request_id=?',(state,usage.get('input_tokens') if known else None,usage.get('output_tokens') if known else None,actual,time.time(),request_id))
  if known:self.actual_usd+=actual;self.usage_missing-=1
  self.export()

 def export(self):
  with sqlite3.connect(self.ledger) as db:
   db.row_factory=sqlite3.Row
   rows=[dict(x) for x in db.execute('SELECT * FROM immune_requests WHERE run_id=? ORDER BY started',(self.run_id,))]
  self.usage_path.parent.mkdir(parents=True,exist_ok=True)
  temp=self.usage_path.with_suffix('.tmp')
  with temp.open('w') as f:
   for row in rows:f.write(json.dumps(row)+'\n')
   f.flush();os.fsync(f.fileno())
  os.replace(temp,self.usage_path)

 def complete(self,request,fallback):
  body={'model':self.model,'system':request['instructions'],'temperature':0,'max_tokens':self.max_output,'messages':[{'role':'user','content':json.dumps(request['observation'],sort_keys=True)}],'output_config':{'format':{'type':'json_schema','schema':request['response_schema']}}}
  encoded=json.dumps(body).encode()
  if len(encoded)>self.max_input_bytes:raise ValueError('input_bound_exceeded')
  request_id=self.reserve(encoded)
  headers={'Content-Type':'application/json','x-api-key':self.key,'anthropic-version':'2023-06-01'}
  if self.workspace:headers['anthropic-workspace-id']=self.workspace
  req=urllib.request.Request('https://api.anthropic.com/v1/messages',data=encoded,headers=headers)
  try:
   with urllib.request.urlopen(req,timeout=self.timeout) as response:raw=response.read(1_000_001)
   if len(raw)>1_000_000:raise ValueError('response_bound_exceeded')
   result=json.loads(raw)
  except Exception as exc:
   state='http_'+str(exc.code) if isinstance(exc,urllib.error.HTTPError) else 'transport_or_decode_'+type(exc).__name__
   self.finish(request_id,state)
   raise ValueError(state) from None
  # Persist billing evidence before output validation, including malformed output.
  self.finish(request_id,'response_received',result.get('usage'))
  if result.get('stop_reason')!='end_turn':raise ValueError('incomplete_output')
  return json.loads(result['content'][0]['text'])
