import statistics,math
from contract import rng,FAMILIES,packet,parser,outcome
STAGES={'Q0':range(4100,4108),'S1':range(4200,4224)}
def family(seed):return FAMILIES[seed%4]
def schedule(stage,seeds=None):
 rows=[]
 for seed in STAGES[stage] if seeds is None else seeds:
  reps=['structured','prose'];rng(seed,'condition_order').shuffle(reps)
  rows.extend(dict(id=f'{seed}-{r}',seed=seed,representation=r,family=family(seed)) for r in reps)
 return rows
def grade(records,worlds):
 rows=[]
 for r in records:
  w=worlds[r['seed']];labels=r.get('checked',{}).get('result',{}).get('labels') if r['status']=='valid' else None
  rows.append(dict(id=r['id'],seed=r['seed'],representation=r['representation'],family=r['family'],status=r['status'],native=outcome(w,labels),parser=outcome(w,parser(packet(w,r['representation'])))))
 return rows
def contrasts(rows):
 cells=[]
 for rep in ('structured','prose'):
  xs=[r for r in rows if r['representation']==rep]
  cells.append(dict(representation=rep,assigned=len(xs),valid=sum(r['status']=='valid' for r in xs),native_correct=sum(6-r['native']['field_errors'] for r in xs),parser_correct=sum(6-r['parser']['field_errors'] for r in xs),fields=6*len(xs),native_exact=sum(r['native']['exact'] for r in xs),native_protected_errors=sum(r['native']['protected_errors'] for r in xs),protected_denominator=sum(r['native']['protected_denominator'] for r in xs),native_regret=statistics.mean(r['native']['first_action_regret'] for r in xs),parser_regret=statistics.mean(r['parser']['first_action_regret'] for r in xs)))
 ps=[r for r in rows if r['representation']=='prose'];xs=[(r['native']['field_errors']-r['parser']['field_errors'])/6 for r in ps];mu=statistics.mean(xs);se=statistics.stdev(xs)/math.sqrt(len(xs)) if len(xs)>1 else None
 return dict(cells=cells,overall=dict(roots=len(ps),prose_native_minus_parser_error=mu,paired_se=se,descriptive_t23_interval=[mu-2.068658*se,mu+2.068658*se] if len(ps)==24 else None,practical_improvement=mu<=-1/6,root_values=[dict(seed=r['seed'],delta=x) for r,x in zip(ps,xs)]))
def qualified(records,worlds):
 expected=schedule('Q0',sorted(worlds));assert len(records)==len(expected) and {r['id'] for r in records}=={r['id'] for r in expected}
 out=contrasts(grade(records,worlds));c={r['representation']:r for r in out['cells']};allvalid=len(records)==16 and all(r['status']=='valid' for r in records)
 out['semantic_passed']=allvalid and c['structured']['native_correct']>=46 and c['prose']['native_correct']>=40 and sum(r['native_protected_errors'] for r in c.values())==0
 out['incremental_value_passed']=c['prose']['native_correct']>c['prose']['parser_correct']
 out['qualification_passed']=out['semantic_passed'] and out['incremental_value_passed'];return out
