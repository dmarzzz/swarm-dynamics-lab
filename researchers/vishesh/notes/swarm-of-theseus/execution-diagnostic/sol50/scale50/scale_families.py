"""Lossless sparse lessons; no gold routes are sent in actor packets."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'baseline-replication'))
from families import *
import families as base

def history(w,family,owner,changed=False):
 peers=[p for p in w['members'] if p!=owner]
 required=w['changed_routes' if changed else 'routes'][owner]
 rows=[]
 for j,veto in enumerate([None]+peers):
  t=target(family,owner,ident(w['seed'],owner,'history',j,changed))
  records=[record(t,p,p!=veto) for p in peers]
  rows.append({'veto_source':veto,'outcome':decide(required,records,t)})
 return {'encoding':'one eligible true record from each other roster position; veto_source, when non-null, has value false instead. All metadata matches this owner and each distinct episode; observed_at=now. No missing or conflicting records.', 'episodes':rows}

def infer(owner,peers,episodes):
 if not isinstance(episodes,dict):return base.infer(owner,peers,episodes)
 rows=episodes['episodes'];candidates=[]
 for pair in itertools.combinations(peers,2):
  if all(('hold' if x['veto_source'] in pair else 'allow')==x['outcome'] for x in rows):candidates.append(list(pair))
 if len(candidates)!=1:raise ValueError('nonidentifiable_history')
 return candidates[0]

def expanded(w,family,owner,compact,changed=False):
 peers=[p for p in w['members'] if p!=owner];out=[]
 for j,e in enumerate(compact['episodes']):
  t=target(family,owner,ident(w['seed'],owner,'history',j,changed))
  out.append({'target':t,'records':[{'source':p,'value':p!=e['veto_source']} for p in peers],'outcome':e['outcome']})
 return out
