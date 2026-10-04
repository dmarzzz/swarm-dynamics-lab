"""Replay exact planned assignment/packet/response/score lineage from saved data."""
import json
from pathlib import Path
from instrument import *
from native import request,decode

def check(path):
 p=Path(path);load=lambda n:json.loads((p/n).read_text());records=load('records.json');qs=qualification();ws=worlds();assert load('qualification-cases.json')==qs and load('worlds.json')==ws
 by={r['assignment']:r for r in records};assert len(by)==len(records);qr=[]
 for c in qs:
  r=by[c['id']];assert r['packet']==c['packet'];qr.append(r)
 q=qscore(qs,qr);assert q==load('qualification-summary.json');main=[]
 if q['qualification_passed']:
  for w in ws:
   for f,copies in arms(w):
    base=f"{w['id']}/{'false' if f else 'true'}/{copies}"
    for phase in ('before','after'):
     for a in range(10):
      id=f'{base}/{a}/{phase}';r=by[id];prior=by[f'{base}/{a}/before'].get('decision') if phase=='after' else None
      assert r['packet']==main_packet(w,f,copies,a,phase,prior);main.append(r)
 assert len(records)==len(qr)+len(main)
 for r in records:
  if r['status']=='unstarted':continue
  assert r['request']==request(r['packet']) and r['request_sha256']==digest(r['request']) and r['packet_sha256']==digest(r['packet'])
  if r['status']=='valid':
   s=r['response'];raw=dict(model=s['model'],provider=s['provider'],usage=s['usage'],choices=[dict(finish_reason=s['finish_reason'],message=dict(content=s['content']))]);d,cost,_=decode(raw,r['packet']);assert d==r['decision'] and cost==r['actual_nano']
 if main:assert analyze(ws,main)==load('diagnostic-summary.json')
 return dict(verified=True,assigned=len(records),started=sum(r['status']!='unstarted' for r in records),valid=sum(r['status']=='valid' for r in records),qualification=q,diagnostic=analyze(ws,main) if main else None,bridge_digest_check_required=True)
