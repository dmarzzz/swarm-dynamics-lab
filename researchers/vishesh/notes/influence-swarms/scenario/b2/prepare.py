"""Freeze the OFFLINE candidate packet. Never dispatches requests or reserves funds."""
import json,subprocess,sys
from pathlib import Path
import cases as c,instrument as i
from test_b1 import cell
H=Path(__file__).resolve().parent

def main():
 cases=json.loads((H/'dossiers.json').read_text());manifest=json.loads((H/'case-manifest.json').read_text())
 assert c.digest(cases)==manifest['dossiers_sha256']
 assert {x['id']:c.digest(x) for x in cases}==manifest['case_hashes']
 gold=json.loads((c.ROOT/'data/influence-b2/gold.json').read_text());assert c.digest(gold)==manifest['gold_sha256']
 run=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(H),'-p','test_b1.py'],capture_output=True,text=True)
 if run.returncode:raise SystemExit(run.stdout+run.stderr)
 maximum=0;fixture_calls=0;recordsets={};treatment=[]
 for split in ('development','evaluation'):
  records=[];lookup={x['id']:x for x in cases}
  for row in i.schedule(cases,split):
   rec,width=cell(lookup[row['case_id']],row['condition'],row['arm'],row['repetition'],maximal=True);maximum=max(maximum,width);fixture_calls+=len(rec['answers']);records.append(rec)
  recordsets[split]=records
 assert i.qualification(cases,recordsets['development'])['qualified']
 assert i.analyze(cases,recordsets['evaluation'])['overall_mean']==0
 for x in cases:treatment.append({'case_id':x['id'],**i.treatment_check(x)})
 dev=i.schedule(cases,'development');evaluation=i.schedule(cases,'evaluation')
 packet={'schema_version':1,'scope':'B2-D0_then_conditional_B2-E0','launch_enabled':False,'approval':'not_funded','study_original_cap_usd':8,'prior_reserved_usd':9.129056,'proposed_incremental_max_usd':11.48,'model_max_usd':9.805824,'hosting_max_usd':.5,'hosting_max_hours':6,'hosting_hourly_all_in_ceiling_usd':.5/6,'historical_hosting_usd':None,'model':i.MODEL,'provider':'openai','fallbacks':False,'max_request_bytes':i.MAX_WIRE,'max_output_tokens':i.MAX_OUTPUT,'per_request_reservation_usd':i.RESERVATION,'max_transport_attempts':2016,'automatic_retries':0,'conditions':list(i.CONDITIONS),'arms':list(i.ARMS),'case_manifest_sha256':c.digest(manifest),'development':{'name':'B2-D0','assignments':dev,'maximum_requests':96,'maximum_model_usd':.466944},'evaluation':{'name':'B2-E0','assignments':evaluation,'maximum_requests':1920,'maximum_model_usd':9.33888,'requires':'B2-D0 complete and neutral-only qualification passes'},'source_hashes':{name:__import__('hashlib').sha256((H/name).read_bytes()).hexdigest() for name in ('cases.py','instrument.py','prepare.py','test_b1.py','dossiers.json','SOURCE-FIT.md','PLAN.md','CASE-CLARITY-REVIEW.md')}}
 for name,data in [('packet.json',packet),('offline-validation.json',{'status':'offline_pass','native_calls':0,'test_count':13,'scripted_calls_rehearsed':fixture_calls,'maximum_rehearsed_wire_bytes':maximum,'wire_ceiling':i.MAX_WIRE,'packet_sha256':c.digest(packet),'source_hashes':packet['source_hashes'],'treatments':treatment,'qualification_fixture':'passes_neutral_gates; advocacy_harm_selection_test_passes','analysis_fixture':'zero scripted contrast; missing-cell aggregate suppression passes','gold_validation':'hand-specified family/status/acceptable structure plus exact arithmetic/schedule fixtures and mutations; not independent external validation','budget_arithmetic':{'development':96*i.RESERVATION,'evaluation':1920*i.RESERVATION,'total_models':2016*i.RESERVATION,'max_incremental_with_hosting':11.48},'remaining_admission':['PI funded named-scope decision','historical hosting reconciliation and original-ledger ceiling amendment','fresh route/rate availability','exact approved-account exclusive allocation and hosting quote','registered immutable condition plans/public-page verification','source/runtime verification and admitted acquisition adapter']})]:
  path=H/name;raw=json.dumps(data,indent=2)+'\n'
  if path.exists() and path.read_text()!=raw:raise SystemExit('Frozen offline artifact differs: create/review a new version rather than silently overwrite '+name)
  path.write_text(raw)
 print(json.dumps({'native_calls':0,'fixture_calls':fixture_calls,'max_wire_bytes':maximum,'packet_sha256':c.digest(packet),'incremental_proposal_usd':11.48}))
if __name__=='__main__':main()
