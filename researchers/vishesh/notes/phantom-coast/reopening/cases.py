"""Inspected development fixtures only. No model, network or policy experiment."""
import copy,json,hashlib
from pathlib import Path
SITES=['A','B','C','D']
TASK='Map each location LAND, WATER or UNKNOWN from current evidence. Direct current measurements are authoritative in this sandbox. Reports may be mistaken; authentic identity is not proof of correctness. Copies share their originating observation. Older observations before day 10 do not establish current state. All locations remain inspectable. The separate exploration objective and uncertainty loss are not yet frozen for native use.'
def rec(id,site,label,kind='report',day=10,origin=None):
 return dict(id=id,site=site,label=label,kind=kind,observed_day=day,origin=origin or id)
def reference(actor):
 out={}
 for site in SITES:
  rs=[r for r in actor['records'] if r['site']==site and r['kind']=='direct' and r['observed_day']>=actor['cutoff_day']]
  if not rs:out[site]='UNKNOWN';continue
  latest=max(r['observed_day'] for r in rs);labels={r['label'] for r in rs if r['observed_day']==latest}
  out[site]=next(iter(labels)) if len(labels)==1 else 'UNKNOWN'
 return out
DEFINITIONS=[
 ('legitimate-correction','LAND',[rec('old','A','WATER'),rec('survey','A','LAND','direct',12)],'Accept corrective evidence while retaining unrelated correct knowledge.'),
 ('copied-rumor','LAND',[rec('survey','A','LAND','direct',12),rec('rumor','A','WATER'),rec('copy-1','A','WATER',origin='rumor'),rec('copy-2','A','WATER',origin='rumor')],'Three repetitions of one rumor must not count as three independent observations.'),
 ('stale-authentic','LAND',[rec('old-survey','A','WATER','direct',2),rec('new-survey','A','LAND','direct',12)],'Source authenticity must not erase observation time; pre-episode truth can differ.'),
 ('false-negative-discovery','LAND',[rec('rumor','A','WATER')],'Unvisited real land remains discoverable. A false report must not remove the legal inspection action.'),
 ('false-positive-diversion','WATER',[rec('rumor','A','LAND')],'Mirror harm: false land may waste scarce inspection capacity rather than suppress visits.'),
 ('insufficient-evidence','LAND',[rec('report-1','A','WATER'),rec('report-2','A','LAND')],'Contradictory unsupported reports do not make evaluator-only truth knowable.')]
def build():
 cases=[]
 for name,truth,rs,purpose in DEFINITIONS:
  world=dict(A=truth,B='WATER',C='LAND',D='WATER')
  actor=dict(task=TASK,cutoff_day=10,sites=SITES,legal_inspections=SITES,records=rs+[rec('anchor-'+s,s,world[s],'direct',10) for s in SITES[1:]])
  resolved=copy.deepcopy(actor);resolved['records'].append(rec('resolution','A',truth,'direct',20))
  opposite=copy.deepcopy(resolved);other='WATER' if truth=='LAND' else 'LAND'
  for r in opposite['records']:
   if r['site']=='A' and r['kind']=='direct' and r['observed_day']>=10:r['label']=other
  missing=copy.deepcopy(actor);missing['records']=[r for r in missing['records'] if not(r['site']=='A' and r['kind']=='direct' and r['observed_day']>=10)]
  reorder=copy.deepcopy(actor);reorder['records'].reverse()
  for variant,a,w in [('base',actor,world),('resolved',resolved,world),('truth-flip',opposite,dict(world,A=other)),('reordered',reorder,world),('missing-current-evidence',missing,world)]:
   cases.append(dict(id=name+'/'+variant,development_root=name,variant=variant,purpose=purpose,actor=a,evaluator=dict(world=w,expected=reference(a)),actor_sha256=hashlib.sha256(json.dumps(a,sort_keys=True).encode()).hexdigest()))
 return cases
if __name__=='__main__':
 (Path(__file__).parent/'development-cases.json').write_text(json.dumps(build(),indent=2)+'\n')
