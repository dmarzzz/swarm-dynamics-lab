"""Assigned-denominator R40 analysis. No imputation, p-values or call-level N."""
import statistics
import cases as c,instrument as i
ARMS=('large','small','generalist');WORLDS=('truthful','misleading')
def analyze(cases,records):
 cases={x['id']:x for x in cases if x['split']=='evaluation'};records={(r['case_id'],r['repetition']):r for r in records};outcomes=[];lookup={};groups={}
 for cid,case in cases.items():
  for rep in (0,1):
   record=records.get((cid,rep),{});nodes={x['id']:x for x in record.get('nodes',[])};graph={n['id']:n for n in i.make_graph(case,rep,WORLDS)}
   for world in WORLDS:
    for arm in ARMS:
     nid=world+'/'+arm+'-final';item=nodes.get(nid);score=i.score(case,graph[nid],item['answer']) if item and item['state']=='valid' else None;row={'case_id':cid,'family':case['family'],'repetition':rep,'world':world,'arm':arm,'state':item['state'] if item else 'unstarted','score':score};outcomes.append(row);lookup[cid,rep,world,arm]=score
     g=groups.setdefault(world+'/'+arm,{'assigned':0,'observed':0,'acceptable':0,'violation':0,'unsafe_purchase':0,'unsupported_clearance':0,'unnecessary_deferral':0,'target_adopted':0});g['assigned']+=1
     if score:
      g['observed']+=1
      for k in ('acceptable','violation','unsafe_purchase','unsupported_clearance','unnecessary_deferral','target_adopted'):g[k]+=score[k]
 for g in groups.values():g['violation_bounds']=[g['violation']/g['assigned'],(g['violation']+g['assigned']-g['observed'])/g['assigned']]
 contrasts={}
 for name,left,right in (('primary_large_vs_generalist','large','generalist'),('secondary_small_vs_generalist','small','generalist'),('secondary_large_vs_small','large','small')):
  roots=[];all_lower=[];all_upper=[]
  for cid,case in cases.items():
   repeats=[]
   for rep in (0,1):
    low=high=0;complete=True
    for world,arm,sign in (('misleading',left,1),('truthful',left,-1),('misleading',right,-1),('truthful',right,1)):
     z=lookup[cid,rep,world,arm];a=b=int(z['violation']) if z else None
     if z is None:a,b=0,1;complete=False
     low+=sign*(a if sign==1 else b);high+=sign*(b if sign==1 else a)
    repeats.append({'repetition':rep,'point':low if complete else None,'bounds':[low,high]})
   lower=statistics.mean(r['bounds'][0] for r in repeats);upper=statistics.mean(r['bounds'][1] for r in repeats);roots.append({'case_id':cid,'family':case['family'],'point':lower if all(r['point']is not None for r in repeats) else None,'bounds':[lower,upper],'repetitions':repeats});all_lower.append(lower);all_upper.append(upper)
  contrasts[name]={'point':statistics.mean(r['point'] for r in roots) if all(r['point']is not None for r in roots) else None,'bounds':[statistics.mean(all_lower),statistics.mean(all_upper)],'roots':roots,'leave_one_family_out_bounds':{r['family']:[statistics.mean(x['bounds'][0] for x in roots if x is not r),statistics.mean(x['bounds'][1] for x in roots if x is not r)] for r in roots}}
 disagreements=[]
 for cid in cases:
  for world in WORLDS:
   for arm in ARMS:
    a=lookup[cid,0,world,arm];b=lookup[cid,1,world,arm];disagreements.append({'case_id':cid,'world':world,'arm':arm,'decision_disagreement':(a['raw_action'],a['raw_choice'])!=(b['raw_action'],b['raw_choice']) if a and b else None})
 return {'assigned_final_decisions':108,'observed_final_decisions':sum(x['score']is not None for x in outcomes),'independent_configurations':9,'authored_families':9,'fresh_repetitions':2,'groups':groups,'contrasts':contrasts,'outcomes':outcomes,'repeat_disagreement':disagreements,'limitation':'Authored configurations, one per family. Shared prefixes, agents and calls are dependent. Bounds address missingness, not sampling confidence; no population CI or neutral-page effect.'}
