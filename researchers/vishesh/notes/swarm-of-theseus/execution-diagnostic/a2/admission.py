"""Fail-closed D1 admission. Operator receipt is evidence binding, not spending authority."""
import hashlib,json,re,time,urllib.request
from design import ROOT,MODEL,source_hash,digest
class GateError(ValueError):
 """Only fixed, non-secret rejection reasons may use this class."""

EXPERIMENT='swarm-of-theseus-acquisition-a2'
PREFIX='https://github.com/dmarzzz/swarm-lab/blob/'
REL='researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/'
def fetch(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'Cache-Control':'no-cache','User-Agent':'Theseus-D1'}),timeout=25) as r:data=r.read(2_000_001)
 if len(data)>2_000_000:raise GateError('public_document_too_large')
 return data.decode()
def raw(url):return url.replace('https://github.com/','https://raw.githubusercontent.com/').replace('/blob/','/')
def validate(receipt,revision,assignments,now=None):
 now=time.time() if now is None else now
 required={'authority_allocation_id':'theseus-a2-7300-7305-v1','experiment':EXPERIMENT,'source_commit':revision,'instrument_sha256':source_hash(),'assignments_sha256':digest(assignments),'model':MODEL,'max_calls':204,'cap_usd':2.5,'max_seconds':7200,'workers':1,'retries':0,'input_rate':1,'output_rate':5,'exclusive_claim_verified':True,'public_page_verified':True,'dependencies_verified':True,'research_review_status':'not-required-owner-direction','prior_unresolved_usd':0.010452,'attempt':'A2'}
 for k,v in required.items():
  if receipt.get(k)!=v:raise GateError('admission_mismatch_'+k)
 for k in ('authority_allocation_id','owner_authorization_ref','claim_id','host','review_policy_ref','operator','allocation_verification_ref'):
  if not receipt.get(k):raise GateError('admission_missing_'+k)
 for k,age in [('verified_epoch',900),('public_page_verified_epoch',900),('pricing_verified_epoch',86400)]:
  if not 0<=now-receipt.get(k,0)<=age:raise GateError('stale_'+k)
 if receipt.get('claim_until_epoch',0)<now+7200:raise GateError('claim_too_short')
 expected=PREFIX+revision+'/'+REL+'A2-PLAN.md'
 if receipt.get('plan_url')!=expected:raise GateError('wrong_plan_revision')
 if receipt.get('plan_sha256')!=hashlib.sha256((ROOT/'A2-PLAN.md').read_bytes()).hexdigest():raise GateError('wrong_plan_hash')
 review=receipt.get('assessment_url','')
 if not re.fullmatch(re.escape(PREFIX)+r'[0-9a-f]{40}/'+re.escape(REL)+r'(?:reviews/)?[A-Za-z0-9_-]+\.md',review):raise GateError('immutable_assessment_required')
 if not re.fullmatch('[0-9a-f]{64}',receipt.get('assessment_sha256','')):raise GateError('assessment_hash_required')
 if len(assignments)!=204 or sum(a['kind']=='learn' for a in assignments)!=12:raise GateError('assignment_count_mismatch')
 if receipt.get('prior_spend_usd')!=0.8226830437 or receipt.get('total_authority_usd')!=5 or receipt.get('infrastructure_hold_usd')!=.1:raise GateError('budget_carryforward_mismatch')
 if receipt.get('update_approval_sha256')!=hashlib.sha256((ROOT/'A2-PLAN.md').read_bytes()).hexdigest():raise GateError('update_scope_mismatch')
 origin=receipt.get('dispatch_origin')
 if origin=='owner-direct-a2':
  authority=receipt.get('direct_dispatch_authorization',{})
  exact={'attempt':'A2','max_attempts':1,'max_calls':204,'original_cap_usd':5,'assignments_sha256':digest(assignments),'plan_sha256':receipt['plan_sha256'],'no_central_dispatch':True}
  if not isinstance(authority,dict) or any(authority.get(k)!=v for k,v in exact.items()):raise GateError('direct_authority_scope_mismatch')
  if not authority.get('decision_ref') or not authority.get('decision_record_sha256'):raise GateError('direct_authority_missing')
  if receipt.get('queue_closed_verified') is not True or receipt.get('central_dispatch_absent') is not True or not receipt.get('queue_fence_ref'):raise GateError('queue_fence_missing')
 else:raise GateError('unsupported_dispatch_origin')
 for k in ('approved_account_verified','original_ledger_reconciled','exclusive_workload_verified','credential_policy_verified','host_key_verified'):
  if receipt.get(k) is not True:raise GateError('missing_'+k)
 for k in ('queue_issue','original_ledger_ref','budget_retirement_ref','credential_policy_ref','runtime_sha256'):
  if not receipt.get(k):raise GateError('missing_'+k)
 if receipt.get('allocation_reserved_usd')!=2.6:raise GateError('allocation_envelope_mismatch')
 health=receipt.get('provider_health',{})
 if not isinstance(health,dict) or health.get('model')!=MODEL or health.get('route_verified') is not True or health.get('restriction_resolved') is not True:raise GateError('provider_health_unverified')
 if health.get('evidence_kind') not in ('successful_inference','authorized_account_resolution') or not health.get('evidence_ref'):raise GateError('provider_health_evidence_missing')
 if not 0<=now-health.get('verified_epoch',0)<=900 or health.get('verified_epoch',0)<=health.get('last_rejection_epoch',now):raise GateError('provider_health_stale')
 return receipt

def public_check(receipt,read=fetch):
 state=json.loads(read('https://swarm-live.pages.dev/api/state'))
 if not isinstance(state,dict) or not isinstance(state.get('experiments'),list):raise GateError('registration_unavailable')
 exp=next((x for x in state['experiments'] if isinstance(x,dict) and x.get('id')==EXPERIMENT),{})
 if exp.get('url')!=receipt['plan_url'] or not exp.get('description','').startswith('TLDR: '):raise GateError('registration_mismatch')
 plan=read(raw(receipt['plan_url']))
 if hashlib.sha256(plan.encode()).hexdigest()!=receipt['plan_sha256']:raise GateError('public_plan_hash_mismatch')
 for section in ('TLDR','Question and prediction','Setup','Protocol','Metrics','Budget and launch gates'):
  if '\n## '+section+'\n' not in plan:raise GateError('missing_plan_section')
 review=read(raw(receipt['assessment_url']))
 if hashlib.sha256(review.encode()).hexdigest()!=receipt['assessment_sha256']:raise GateError('review_hash_mismatch')
 if not any(line.strip()=='Status: diagnostic-only' for line in review.splitlines()):raise GateError('review_not_admitted')
 return {'checked_epoch':time.time(),'plan_url':receipt['plan_url'],'plan_sha256':receipt['plan_sha256'],'assessment_sha256':receipt['assessment_sha256']}
