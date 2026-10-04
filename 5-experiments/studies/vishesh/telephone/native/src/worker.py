"""Bounded engine injected with admitted transport; no credential discovery."""
import json,time
from pathlib import Path
from contract import assignments,request,response,sha,validate_count,envelope

def write(path,data):
 with path.open('x') as f:
  json.dump(data,f,indent=2);f.flush()
  import os;os.fsync(f.fileno())

def execute(packet,out,ledger,count_tokens,generate,deadline,report=lambda x:None):
 if out.exists():raise ValueError('attempt_exists')
 expected=assignments([x['id'] for x in packet['cases']])
 if packet['assignments']!=expected or len(expected)>72 or packet['stage'] not in ('A0','A1','V0'):raise ValueError('packet_scope')
 out.mkdir(mode=0o700,parents=True);write(out/'packet.json',packet)
 byid={x['id']:x for x in packet['cases']};parents={};rows=[];stopped=False
 for a in expected:
  row={**a,'status':'unstarted'};rows.append(row)
  if stopped:continue
  try:
   if time.time()+60>=deadline:raise ValueError('deadline')
   chain=(a['component'],a['arm']);previous=parents.get(chain)
   req=request(a['arm'],a['hop'],byid[a['component']]['records'],previous)
   cid=packet['stage']+':'+a['call_id'];write(out/(a['call_id']+'.request.json'),req)
   validate_count(count_tokens(req))
   ledger.reserve(cid,packet['stage'],'model',envelope(1)['per_call_reserve_nano'],sha(req))
   row['status']='started';start=time.monotonic()
   try:
    raw=generate(req)
    write(out/(a['call_id']+'.response.json'),raw)
    # Settle only usage verified by full contract; invalid/ambiguous answers retain reserve.
    parsed=response(raw,a['arm']);ledger.settle(cid,parsed['token_cost_nano'])
    row.update(status='valid',latency_seconds=time.monotonic()-start,**{k:v for k,v in parsed.items() if k!='text'})
    parents[chain]=parsed['text']
   except Exception:
    ledger.settle(cid,None);raise
  except Exception as exc:
   row['status']='failed';row['failure_type']=type(exc).__name__;stopped=True
   if type(getattr(exc,'code',None)) is int:row['http_status']=exc.code
  write(out/(a['call_id']+'.receipt.json'),row)
  report({'assigned':len(expected),'valid':sum(x['status']=='valid' for x in rows),'stopped':stopped})
 summary={'scope':packet['scope']+'; semantic review pending','stage':packet['stage'],'assigned':len(expected),'valid':sum(x['status']=='valid' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'unstarted':sum(x['status']=='unstarted' for x in rows),'scored':0,'stopped':stopped,'budget':ledger.summary(),'assignments':rows}
 write(out/'summary.json',summary);return summary
