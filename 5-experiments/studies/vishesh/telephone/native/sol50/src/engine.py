"""Offline-testable Sol50 collection core; launch admission and transport are external.

This module never reads credentials, acquires a host or automatically retries.
"""
import json,time,hashlib
from decimal import Decimal,ROUND_CEILING
from pathlib import Path
from contract import request,parse,canonical,envelope,MODEL,MAX_OUTPUT,MAX_INPUT,assignments

def digest(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def write(p,obj):
 with p.open('x') as f:
  json.dump(obj,f,indent=2);f.flush()
  import os;os.fsync(f.fileno())
def normalize(raw,bound):
 if raw.get('model')!=MODEL or raw.get('provider')!='OpenAI' or raw.get('error'):raise ValueError('model_or_provider')
 choices=raw.get('choices');u=raw.get('usage',{})
 if not isinstance(choices,list) or len(choices)!=1:raise ValueError('choices')
 c=choices[0];m=c.get('message',{})
 if c.get('finish_reason')!='stop' or m.get('role')!='assistant' or m.get('tool_calls') or m.get('reasoning') or m.get('reasoning_details') or m.get('refusal'):raise ValueError('completion')
 inp,out=u.get('prompt_tokens'),u.get('completion_tokens')
 if type(inp) is not int or not 0<inp<=bound<=MAX_INPUT or type(out) is not int or not 0<out<=MAX_OUTPUT or u.get('total_tokens')!=inp+out:raise ValueError('usage')
 details=u.get('completion_tokens_details') or {}
 if details.get('reasoning_tokens',0)!=0:raise ValueError('reasoning_mode')
 cached=(u.get('prompt_tokens_details') or {}).get('cached_tokens',0)
 if type(cached) is not int or not 0<=cached<=inp or u.get('is_byok',False):raise ValueError('billing_route')
 if isinstance(u.get('cost'),bool) or u.get('cost') is None:raise ValueError('cost')
 cost=Decimal(str(u['cost']))
 if not cost.is_finite() or cost<0:raise ValueError('cost')
 nano=int((cost*1000000000).to_integral_value(rounding=ROUND_CEILING))
 if nano>inp*2000+out*10000+1:raise ValueError('price')
 return parse(m.get('content')),{'input_tokens':inp,'output_tokens':out,'cached_input_tokens':cached,'cost_nano':nano}

def execute_chain(packet,out,ledger,generate,deadline,qualification):
 if qualification.get('passed') is not True or qualification.get('model')!=MODEL or qualification.get('packet_sha256')!=digest(packet):raise ValueError('qualification_required')
 if out.exists():raise ValueError('attempt_exists')
 out.mkdir(parents=True,mode=0o700);write(out/'packet.json',packet);planned=assignments();previous=None;rows=[];stopped=False
 for a in planned:
  row={**a,'status':'unstarted'};rows.append(row)
  if stopped:continue
  try:
   if time.time()+60>=deadline:raise ValueError('deadline')
   req=request(packet if previous is None else None,previous);bound=len(canonical(req).encode())+1024
   cid='Sol50:'+a['agent_id'];write(out/(a['agent_id']+'.request.json'),req)
   ledger.reserve(cid,'Sol50','model',envelope()['per_call_reserve_nano'],digest(req),stage_call_cap=50)
   row['status']='started';start=time.monotonic()
   try:
    raw=generate(req);write(out/(a['agent_id']+'.response.json'),raw)
    obj,usage=normalize(raw,bound);ledger.settle(cid,usage['cost_nano']);previous=obj
    row.update(status='valid',latency_seconds=time.monotonic()-start,**usage,decision=obj['decision'],request_sha256=digest(req),response_sha256=digest(raw))
   except Exception:ledger.settle(cid,None);raise
  except Exception as exc:
   row.update(status='failed',failure_type=type(exc).__name__);stopped=True
  write(out/(a['agent_id']+'.receipt.json'),row)
 summary={'assigned':50,'valid':sum(r['status']=='valid' for r in rows),'unstarted':sum(r['status']=='unstarted' for r in rows),'failed':sum(r['status']=='failed' for r in rows),'stopped':stopped,'semantic_review_complete':False,'assignments':rows,'budget':ledger.summary()}
 write(out/'summary.json',summary);return summary
