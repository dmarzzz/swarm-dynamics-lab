"""Retrospective saved-data analysis. No network, credentials or native calls."""
import json,hashlib,gzip,statistics,sys
from pathlib import Path
B=Path(__file__).resolve().parents[1];ROOT=B.parents[4];out=B/'results'
rows=json.loads((out/'pc5-decisions.json').read_text());ws=json.loads((out/'pc5-worlds.json').read_text());audit=json.loads((out/'PC5-REAUDIT.json').read_text())
for n in ('decisions.json','worlds.json'):assert hashlib.sha256((out/('pc5-'+n)).read_bytes()).hexdigest()==audit['hashes'][n]
assert len(rows)==128 and len({r['id'] for r in rows})==128 and all(r['status']=='valid' for r in rows)
sys.path.insert(0,str(B/'src'));from simple_policy import choose
paired=[];cells=[];strata=[]
for p in (.8,.2):
 pairs=[]
 for seed in sorted({r['seed'] for r in rows}):
  rs={r['objective']:r for r in rows if r['seed']==seed and r['reliability']==p};w=ws[str(seed)]
  def regret(cell):return (.25 if cell==w['report_cell'] else 1-p if cell==w['unknown_cell'] else .25+1-p)-min(.25,1-p)
  for r in rs.values():assert abs(regret(r['choice'])-r['expected_regret'])<1e-10
  pairs.append(dict(seed=seed,reliability=p,legacy=rs['legacy']['optimal'],explicit=rs['explicit']['optimal'],delta=rs['explicit']['expected_regret']-rs['legacy']['expected_regret'],report_first=w['legal_order'][0]==w['report_cell'],label=w['report_label']))
  assert abs(regret(choose(w['report_cell'],w['unknown_cell'],p)))<1e-10
 paired.extend(pairs)
 cells.append(dict(reliability=p,assigned_pairs=len(pairs),improved=sum(x['explicit'] and not x['legacy'] for x in pairs),regressed=sum(x['legacy'] and not x['explicit'] for x in pairs),both_correct=sum(x['legacy'] and x['explicit'] for x in pairs),both_wrong=sum(not x['legacy'] and not x['explicit'] for x in pairs),regret_delta=statistics.mean(x['delta'] for x in pairs)))
 for feature in ('report_first','label'):
  for v in sorted({x[feature] for x in pairs}):
   xs=[x for x in pairs if x[feature]==v];strata.append(dict(reliability=p,feature=feature,value=v,n=len(xs),legacy_optimal=sum(x['legacy'] for x in xs),explicit_optimal=sum(x['explicit'] for x in xs)))
policy=[]
for p in (.8,.2):
 for name in ('legacy','explicit','always_check','always_explore','analytic'):
  rs=[r for r in rows if r['reliability']==p and r['objective']==name]
  val=statistics.mean(r['expected_regret'] for r in rs) if rs else (.25-min(.25,1-p) if name=='always_check' else 1-p-min(.25,1-p) if name=='always_explore' else 0)
  policy.append(dict(reliability=p,policy=name,expected_regret=round(val,12),evidence='saved native choices' if rs else 'analytic counterfactual on declared contract'))
dmarz=ROOT/'researchers/dmarz/notes/verify-cost-qwen/records/attempt-002';files=[dmarz/(x+'-episodes.jsonl.gz') for x in ('p0','q0')]
drows=[json.loads(line) for f in files for line in gzip.open(f,'rt')];assert len(drows)==24
counts={'both_correct':0,'exact_swap':0,'swap_small_zero':0,'other':0,'chooses_own_minimum':0,'optimal':0,'misses_with_reversed_cost_order':0}
for r in drows:
 u,e=r['unknown_cost'],r['error'];c=r['evaluation']['work'];a,z=c['cost_check'],c['cost_explore'];eq=lambda a,b:abs(a-b)<=.005
 category='both_correct' if eq(a,u) and eq(z,e) else 'exact_swap' if eq(a,e) and eq(z,u) else 'swap_small_zero' if ((e>u and eq(a,e) and eq(z,0)) or (u>e and eq(a,0) and eq(z,u))) else 'other'
 counts[category]+=1;chosen=a if r['evaluation']['action']=='check' else z;counts['chooses_own_minimum']+=chosen<=min(a,z)+1e-9;counts['optimal']+=r['evaluation']['optimal'];counts['misses_with_reversed_cost_order']+=not r['evaluation']['optimal'] and (a-z)*(u-e)<0
result=dict(analysis='retrospective; no new native evidence',pc5_independent_layouts=32,pc5_dependent_choices=128,pc5_missing=0,paired_strata=cells,exploratory_feature_strata=strata,policies=policy,verify_cost_qwen_attempt002=dict(independent_layouts=len({r['layout'] for r in drows}),dependent_choices=len(drows),counts=counts,pooled_with_pc5=False,source_hashes={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}),known_api_usd=.845052138,conservative_api_exposure_usd=.857148138,new_native_calls=0,new_spend_usd=0)
(out/'prior-analysis.json').write_text(json.dumps(result,indent=2)+'\n');(out/'paired-layouts.json').write_text(json.dumps(paired,indent=2)+'\n');print(json.dumps({'pc5_pairs':cells,'qwen_counts':counts,'new_calls':0}))
