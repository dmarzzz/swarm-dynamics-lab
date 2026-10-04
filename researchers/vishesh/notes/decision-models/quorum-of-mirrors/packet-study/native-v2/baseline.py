"""Same-input exact grammar parser, separate from construction labels."""
import re
PATTERN=re.compile(r'([Aa]t (\d\d:\d\d), ([\w-]+) (?:was (running|operating|stopped|not running)|measured (\d+) (grams|kilograms))\.)')
def parse(text,query=None):
 observations=[]
 for line in text.splitlines():
  if line.startswith('Plan:'):continue
  for m in PATTERN.finditer(line):
   quote,time,entity,state,num,unit=m.groups();prop='running' if state else 'mass_g';value=(1 if state in ['running','operating'] else 0) if state else int(num)*(1000 if unit=='kilograms' else 1)
   if query and any(v!=query[k] for k,v in [('entity',entity),('time',time),('property',prop)]):continue
   observations.append(dict(entity=entity,time=time,property=prop,value=value,status='observed',quote=quote))
 if observations:return observations[-1]
 if query:return {k:query[k] for k in ['entity','time','property']}|{'value':None,'status':'unknown','quote':text}
 raise ValueError('not_in_grammar')
def solve(actor):return {'sources':{r['id']:parse(r['text'],actor['query']) for r in actor['sources']},'reports':{r['id']:parse(r['text']) for r in actor['reports']}}
