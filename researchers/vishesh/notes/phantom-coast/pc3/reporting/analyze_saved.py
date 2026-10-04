"""Post-run descriptive analysis; reads saved native files, makes no model calls."""
import argparse,collections,hashlib,json,statistics
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=a.directory
read=lambda n:json.loads((r/n).read_text())
s=read('summary.json');es=read('episodes.json');rows=read('records.json');manifest=read('manifest.json')
assert len(rows)==len(manifest['assignments'])==1792
assert {x['id'] for x in rows}=={x['id'] for x in manifest['assignments']}
assert len({x['id'] for x in rows})==len(rows)
assert len(es)==96 and {x['seed'] for x in es}==set(range(800,808))
for e in es:
 assert len(e['events'])<=12
 labels=e['endpoint']['map'] or {}
 wrong=sum(labels.get(c,'UNKNOWN') not in ('UNKNOWN',truth) for c,truth in e['truth'].items())
 missing=sum(labels.get(c,'UNKNOWN')=='UNKNOWN' for c in e['truth'])
 m=e['endpoint']['metrics']['whole']
 assert (wrong,missing,36)==(m['wrong'],m['missing'],m['denominator'])
 assert abs(m['lower']-wrong/36)<1e-12 and abs(m['upper']-(wrong+missing)/36)<1e-12
 for v in e['events']:
  if v['target'] is not None:assert v['observation']['label']==e['truth'][v['target']]
 groups=collections.Counter(x['status'] for x in rows)
assert sum(groups.values())==1792
conditions=[]
for policy in ('team','single','uniform'):
 for report in ('misleading','benign'):
  for guard in (False,True):
   items=[e for e in es if (e['policy'],e['report'],e['guard'])==(policy,report,guard)]
   def mean(k):return statistics.mean(e['endpoint']['metrics'][k] for e in items)
   whole=[e['endpoint']['metrics']['whole'] for e in items]
   conditions.append(dict(policy=policy,report=report,guard=guard,roots=len(items),complete=sum(e['status']=='complete' for e in items),wrong=sum(x['wrong'] for x in whole),missing=sum(x['missing'] for x in whole),denominator=36*len(items),loss=statistics.mean((x['wrong']+.25*x['missing'])/36 for x in whole),lower=statistics.mean(x['lower'] for x in whole),upper=statistics.mean(x['upper'] for x in whole),unique_cells=mean('unique_cells'),report_cells_visited=mean('report_cells_visited'),repeated_slots=mean('repeated_slots'),failed_slots=mean('failed_slots'),deterministic_upper=statistics.mean(e['endpoint']['deterministic']['upper'] for e in items),yoked_upper=statistics.mean(e['endpoint']['yoked']['upper'] for e in items) if policy=='team' else None))
for condition in conditions:
 items=[e for e in es if (e['policy'],e['report'],e['guard'])==(condition['policy'],condition['report'],condition['guard'])]
 condition['stratified_errors']={}
 for stratum in ('observed','unobserved','land','water'):
  cells=[e['endpoint']['metrics'][stratum] for e in items]
  totals={k:sum(x[k] for x in cells) for k in ('wrong','missing','denominator')}
  totals.update(lower=totals['wrong']/totals['denominator'] if totals['denominator'] else None,upper=(totals['wrong']+totals['missing'])/totals['denominator'] if totals['denominator'] else None)
  condition['stratified_errors'][stratum]=totals
 condition['first_report_visit']=[dict(seed=e['seed'],slot=e['endpoint']['metrics']['first_report_visit'],censored=e['endpoint']['metrics']['first_visit_censored']) for e in items]
 condition['stratum_weighting']='Pooled cell counts within condition; cells are dependent, not independent samples.'
paired=[]
for policy in ('team','single','uniform'):
 for guard in (False,True):
  pairs=[]
  for seed in range(800,808):
   d={e['report']:e for e in es if (e['seed'],e['policy'],e['guard'])==(seed,policy,guard)}
   m=d['misleading']['endpoint']['metrics'];b=d['benign']['endpoint']['metrics']
   pairs.append(dict(seed=seed,report_visits=m['report_cells_visited']-b['report_cells_visited'],unique_cells=m['unique_cells']-b['unique_cells'],upper_error=m['whole']['upper']-b['whole']['upper']))
  paired.append(dict(policy=policy,guard=guard,worlds=pairs,means={k:statistics.mean(v[k] for v in pairs) for k in ('report_visits','unique_cells','upper_error')}))
risk={(x['policy'],x['report'],x['guard']):x['loss'] for x in conditions}
independent_primary=risk['team','misleading',True]-risk['team','misleading',False]
assert abs(independent_primary-s['overall']['primary_loss_difference'])<1e-12
guard_differences=[]
for policy in ('team','single','uniform'):
 for report in ('misleading','benign'):
  on=next(x for x in conditions if (x['policy'],x['report'],x['guard'])==(policy,report,True))
  off=next(x for x in conditions if (x['policy'],x['report'],x['guard'])==(policy,report,False))
  guard_differences.append(dict(policy=policy,report=report,loss=on['loss']-off['loss'],upper_error=on['upper']-off['upper'],wrong=on['wrong']-off['wrong'],missing=on['missing']-off['missing'],report_cells_visited=on['report_cells_visited']-off['report_cells_visited'],unique_cells=on['unique_cells']-off['unique_cells'],meets_practical_threshold=on['loss']-off['loss']<=-2/36+1e-12))
sensitivity={'label':'Prespecified descriptive leave-one-root-out check; primary still uses all eight roots','leave_one_out':[{'omitted_root':x['seed'],'loss_difference':statistics.mean(y['primary_loss_difference'] for y in s['worlds'] if y['seed']!=x['seed'])} for x in s['worlds']]}
result=dict(primary_sensitivity=sensitivity,guard_on_minus_off=guard_differences,stage=s['stage'],independent_roots=8,structural_families=2,dependent_episodes=96,assignment_status=dict(groups),conditions=conditions,misleading_minus_benign=paired,primary=s['overall'],by_family=s['by_family'],per_root_contrasts=s['worlds'],budget=s['budget'],usage_by_policy=s['usage_by_policy'],limitations='Eight synthetic roots from two structural families, one model snapshot, unequal inference compute. Missing labels are identification bounds, not confidence intervals. Descriptive exploratory contrasts; no independent replication.',source_sha256={n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in ('summary.json','episodes.json','records.json','manifest.json','worlds.json')})
a.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'assignment_status':dict(groups),'primary':s['overall'],'conditions':conditions,'paired_means':[{'policy':x['policy'],'guard':x['guard'],**x['means']} for x in paired]}))
