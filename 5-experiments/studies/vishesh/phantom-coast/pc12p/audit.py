"""Exact historical-readiness and640-assignment replay, without recollection."""
import json
from pathlib import Path
from instrument import *
from native import request,decode
from runner import readiness

def check(path):
 p=Path(path);load=lambda n:json.loads((p/n).read_text());ready,prior=readiness();assert load('readiness.json')==ready and load('historical-qualification.json')==prior
 records=load('records.json');ws=worlds();assert load('worlds.json')==ws;by={r['assignment']:r for r in records};assert len(by)==len(records)==640;main=[]
 for w in ws:
  for f,c in arms(w):
   base=f"{w['id']}/{'false' if f else 'true'}/{c}"
   for phase in ('before','after'):
    for a in range(10):
     r=by[f'{base}/{a}/{phase}'];previous=by[f'{base}/{a}/before'].get('decision') if phase=='after' else None;assert r['packet']==main_packet(w,f,c,a,phase,previous);main.append(r)
 for r in records:
  if r['status']=='unstarted':continue
  assert r['request']==request(r['packet']) and r['request_sha256']==digest(r['request']) and r['packet_sha256']==digest(r['packet'])
  if r['status']=='valid':
   v=r['response'];raw=dict(model=v['model'],provider=v['provider'],usage=v['usage'],choices=[dict(finish_reason=v['finish_reason'],message=dict(content=v['content']))]);d,cost,_=decode(raw,r['packet']);assert d==r['decision'] and cost==r['actual_nano']
 summary=analyze(ws,main);assert summary==load('diagnostic-summary.json')
 return dict(verified=True,assigned=640,started=sum(r['status']!='unstarted' for r in records),valid=sum(r['status']=='valid' for r in records),readiness=ready,diagnostic=summary,bridge_digest_check_required=True)
