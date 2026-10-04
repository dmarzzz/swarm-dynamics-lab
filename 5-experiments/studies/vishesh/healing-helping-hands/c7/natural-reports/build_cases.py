"""Frozen hand-audited values, independently checked by visible-prose baseline."""
from pathlib import Path
import json,hashlib
from baseline import reconcile,actor_input
ROOT=Path(__file__).resolve().parent
# Values were read from source prose before running baseline; no model output used.
INCIDENTS=[('bea-2024q1','BEA','2024-Q1','2024-05-30',1.3,1.6,['bea-q1']),('bea-2024q2','BEA','2024-Q2','2024-08-29',3.0,2.8,['bea-q2']),('bea-2024q3','BEA','2024-Q3','2024-12-19',3.1,2.8,['bea-q3']),('bls-2023dec','BLS','2023-12','2024-03-08',290000,333000,['bls-feb','bls-mar']),('bls-2024jan','BLS','2024-01','2024-04-05',256000,353000,['bls-feb','bls-mar','bls-apr']),('bls-2024feb','BLS','2024-02','2024-04-05',270000,275000,['bls-mar','bls-apr'])]
def build():
 sources=json.loads((ROOT/'sources.json').read_text());cases=[]
 for iid,pub,period,date,current,old,sids in INCIDENTS:
  metric='real_gdp_qoq_annualized_percent' if pub=='BEA' else 'nonfarm_payroll_monthly_change_jobs'
  for suffix,p,value,label in [('current',period,current,'SUPPORT'),('superseded',period,old,'REFUTE'),('future','2025-Q1' if pub=='BEA' else '2025-01',current,'UNCERTAIN')]:
   q={'publisher':pub,'metric':metric,'period':p,'geography':'US','cutoff':date,'value':value,'vintage':'latest supplied'}
   case={'id':iid+'-'+suffix,'incident_family':iid,'publisher_family':pub,'query':q,'source_ids':sids,'expected':label,'rationale':{'current':'Explicit current value matches.','superseded':'Explicit different revised value; old vintage remains historically true but is not latest.','future':'The supplied dated excerpts do not measure the queried future period; no claim about later actual value.'}[suffix]}
   observed=reconcile(q,[s for s in sources if s['id'] in sids]);assert observed['label']==label,(case,observed)
   case['label_evidence']=observed['evidence'];cases.append(case)
 (ROOT/'cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 payload=[actor_input(c,sources) for c in cases];(ROOT/'actor-inputs.json').write_text(json.dumps(payload,indent=2)+'\n')
 print(json.dumps({'cases':len(cases),'incident_roots':len(INCIDENTS),'publisher_series_families':2,'model_calls':0,'source_baseline_correct':len(cases)}))
if __name__=='__main__':build()
