"""Saved-data-only trace/score reconciliation; no paid calls."""
import json
from pathlib import Path
from contract import digest
from native import request,decode
from cases import grade,summarize
from engine import audit
from analysis import contrast

def check(path):
 p=Path(path);load=lambda n:json.loads((p/n).read_text());ts=load('traces.json');cs=load('cases.json');rs=load('qualification.json')
 assert len({t['id'] for t in ts})==len(ts)
 for t in ts:
  assert t['packet_sha256']==digest(t['packet']) and t['request']==request(t['packet']) and t['request_sha256']==digest(t['request'])
  if t['status']=='valid':
   r=t['response'];raw=dict(model=r['model'],provider=r['provider'],usage=r['usage'],choices=[dict(finish_reason=r['finish_reason'],message=dict(content=r['content']))]);d,c,_=decode(raw,t['packet']);assert d==t['decision']
 for c,r in zip(cs,rs):
  assert c['id']==r['id']
  if r['status']=='valid':assert r['grade']==grade(c,r['decision'])
 assert summarize(rs)==load('qualification-summary.json')
 es=load('episodes.json') if (p/'episodes.json').exists() else []
 for e in es:audit(e)
 if len(es)==4:assert contrast(es)==load('pilot-summary.json')
 entries=[x for e in es for t in e['turns'] for x in t['entries']]
 matched=ts[len(cs):len(cs)+len(entries)]
 assert all(t['packet']==e['packet'] and t.get('decision')==e.get('decision') for t,e in zip(matched,entries)) and len(matched)==len(entries)
 return dict(verified=True,calls=len(ts),valid=sum(t['status']=='valid' for t in ts),complete_arms=len(es),qualification=summarize(rs),bridge_digest_check_required=True)
