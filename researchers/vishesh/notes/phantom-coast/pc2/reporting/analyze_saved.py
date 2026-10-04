"""Post-run descriptive analysis; reads saved native files, makes no model calls."""
import argparse,collections,hashlib,json,statistics
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=a.directory
read=lambda n:json.loads((r/n).read_text())
s=read('summary.json');es=read('episodes.json');rows=read('records.json');manifest=read('manifest.json')
assert len(rows)==len(manifest['assignments'])==1792
assert {x['id'] for x in rows}=={x['id'] for x in manifest['assignments']}
assert len({x['id'] for x in rows})==len(rows)
assert len(es)==96 and {x['seed'] for x in es}==set(range(500,508))
for e in es:
 assert len(e['events'])<=12
 for v in e['events']:
  if v['target'] is not None:assert v['observation']['label']==e['truth'][v['target']]
 groups=collections.Counter(x['status'] for x in rows)
assert sum(groups.values())==1792
conditions=[]
for policy in ('team','single','uniform'):
 for report in ('misleading','benign'):
  for audit in (False,True):
   items=[e for e in es if (e['policy'],e['report'],e['audit'])==(policy,report,audit)]
   def mean(k):return statistics.mean(e['endpoint']['metrics'][k] for e in items)
   whole=[e['endpoint']['metrics']['whole'] for e in items]
   conditions.append(dict(policy=policy,report=report,audit=audit,roots=len(items),complete=sum(e['status']=='complete' for e in items),wrong=sum(x['wrong'] for x in whole),missing=sum(x['missing'] for x in whole),denominator=36*len(items),lower=statistics.mean(x['lower'] for x in whole),upper=statistics.mean(x['upper'] for x in whole),unique_cells=mean('unique_cells'),report_cells_visited=mean('report_cells_visited')))
paired=[]
for policy in ('team','single','uniform'):
 for audit in (False,True):
  pairs=[]
  for seed in range(500,508):
   d={e['report']:e for e in es if (e['seed'],e['policy'],e['audit'])==(seed,policy,audit)}
   m=d['misleading']['endpoint']['metrics'];b=d['benign']['endpoint']['metrics']
   pairs.append(dict(seed=seed,report_visits=m['report_cells_visited']-b['report_cells_visited'],unique_cells=m['unique_cells']-b['unique_cells'],upper_error=m['whole']['upper']-b['whole']['upper']))
  paired.append(dict(policy=policy,audit=audit,worlds=pairs,means={k:statistics.mean(v[k] for v in pairs) for k in ('report_visits','unique_cells','upper_error')}))
result=dict(stage=s['stage'],independent_roots=8,structural_families=2,dependent_episodes=96,assignment_status=dict(groups),conditions=conditions,misleading_minus_benign=paired,primary=s['overall'],by_family=s['by_family'],per_root_contrasts=s['worlds'],budget=s['budget'],usage_by_policy=s['usage_by_policy'],limitations='Eight synthetic roots from two structural families, one model snapshot, unequal inference compute. Missing labels are identification bounds, not confidence intervals. Descriptive exploratory contrasts; no independent replication.',source_sha256={n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in ('summary.json','episodes.json','records.json','manifest.json','worlds.json')})
a.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'assignment_status':dict(groups),'primary':s['overall'],'conditions':conditions,'paired_means':[{'policy':x['policy'],'audit':x['audit'],**x['means']} for x in paired]}))
