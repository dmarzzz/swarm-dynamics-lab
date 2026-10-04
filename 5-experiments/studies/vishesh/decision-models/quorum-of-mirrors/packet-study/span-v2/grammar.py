"""Same-input grammar baseline: no construction labels or condition metadata."""
import re
from decimal import Decimal
PATTERN=re.compile(r'((?:(Unconfirmed|Plan): )?At (\d\d:\d\d), ([\w-]+) (?:(?:was|will be) (running|operating|stopped|not running)|(?:measured|will measure) (\d+(?:\.\d+)?) (grams|kilograms))\.)')
def parse(text,query,source=False):
 candidates=[]
 for m in PATTERN.finditer(text):
  quote,marker,time,entity,state,num,unit=m.groups();mode={'Plan':'PLAN','Unconfirmed':'HEDGE',None:'ASSERTION'}[marker]
  prop='running' if state else 'mass_g';value=int(state in ['running','operating']) if state else int(Decimal(num)*(1000 if unit=='kilograms' else 1))
  f=dict(entity=entity,time=time,property=prop,value=value,status='observed',quote=quote)
  if not source:f['mode']=mode
  matching=all(f[k]==query[k] for k in ['entity','time','property'])
  if not source or (matching and mode=='ASSERTION'):candidates.append((matching,f))
 matches=[f for match,f in candidates if match]
 if matches:return matches[-1]
 if not source and len(candidates)==1:return candidates[0][1]
 if source:return {k:query[k] for k in ['entity','time','property']}|dict(value=None,status='unknown',quote=text)
 raise ValueError('ambiguous_report')
def solve(actor):
 return {kind:[dict(id=r['id'],**{k:v for k,v in parse(r['text'],actor['query'],kind=='sources').items() if kind=='sources' or k!='status'}) for r in actor[kind]] for kind in ['sources','reports']}
