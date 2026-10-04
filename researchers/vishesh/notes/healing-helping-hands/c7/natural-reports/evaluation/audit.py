"""Rebuild evaluation queries from manually reviewed sources; never tunes baseline."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT.parent))
from baseline import reconcile,actor_input,extract
# Hand-read source targets, independent of regex output; tuple(current, previous).
GOLD={'2022-Q3':(2.9,2.6),'2022-Q4':(2.7,2.9),'2023-Q1':(1.3,1.1),'2023-Q2':(2.1,2.4),'2023-Q3':(5.2,4.9),'2023-Q4':(3.2,3.3),'2024-03':(315000,303000),'2024-04':(165000,175000),'2024-05':(218000,272000),'2024-06':(179000,206000),'2024-07':(89000,114000),'2024-08':(159000,142000)}
def run():
 freeze=json.loads((ROOT/'selection-freeze.json').read_text());assert hashlib.sha256((ROOT.parent/'baseline.py').read_bytes()).hexdigest()==freeze['baseline_sha256']
 sources=json.loads((ROOT/'bea-sources.json').read_text())+json.loads((ROOT/'bls-sources.json').read_text());cases=[];results=[];dev=json.loads((ROOT.parent/'sources.json').read_text())
 assert len(sources)==12 and not ({s['url'] for s in sources}&{s['url'] for s in dev})
 for s in sources:
  assert hashlib.sha256(s['excerpt'].encode()).hexdigest()==s['excerpt_sha256']
  current,old=GOLD[s['target_period']];metric='real_gdp_qoq_annualized_percent' if s['publisher']=='BEA' else 'nonfarm_payroll_monthly_change_jobs'
  for kind,period,value,expected in [('current',s['target_period'],current,'SUPPORT'),('previous',s['target_period'],old,'SUPPORT' if current==old else 'REFUTE'),('missing','2025-Q1' if s['publisher']=='BEA' else '2025-01',current,'UNCERTAIN')]:
   c={'id':s['id']+'-'+kind,'incident_family':s['id'],'source_ids':[s['id']],'query':{'publisher':s['publisher'],'metric':metric,'period':period,'geography':'US','cutoff':s['published'],'value':value,'vintage':'latest supplied'},'expected':expected};cases.append(c);out=reconcile(c['query'],[s]);results.append({'id':c['id'],'expected':expected,'observed':out['label'],'correct':out['label']==expected,'evidence':out['evidence']})
   assert reconcile(c['query'],[s,s])['label']==out['label']
   assert actor_input(c,[s])==actor_input({**c,'expected':'changed','rationale':'private'},[s])
 (ROOT/'cases.json').write_text(json.dumps(cases,indent=2)+'\n');(ROOT/'actor-inputs.json').write_text(json.dumps([actor_input(c,sources) for c in cases],indent=2)+'\n')
 report={'status':'offline_frozen_baseline_evaluation','baseline_sha256':freeze['baseline_sha256'],'source_documents':12,'incident_roots':12,'publisher_series_families':2,'established_independent_population_samples':0,'queries':36,'baseline_correct':sum(x['correct'] for x in results),'source_overlap_with_development':0,'all_source_values_manually_read':True,'native_model_calls':0,'baseline_tuned_after_selection':False,'results':results,'limitations':['same known agency styles','operator-read source labels, not blind adjudication','no fresh model runs','all selected target statements remain regex-readable','six BLS headline variants not covered by frozen extractor; target revision clauses are covered'],'cases_sha256':hashlib.sha256((ROOT/'cases.json').read_bytes()).hexdigest()}
 (ROOT/'RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'}))
if __name__=='__main__':run()
