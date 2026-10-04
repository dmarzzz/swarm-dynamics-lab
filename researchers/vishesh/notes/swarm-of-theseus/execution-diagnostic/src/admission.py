"""Fail-closed D1 admission. Operator receipt is evidence binding, not spending authority."""
import hashlib,json,re,time,urllib.request
from instrument import ROOT,MODEL,source_hash,digest
class GateError(ValueError):
 """Only fixed, non-secret rejection reasons may use this class."""

EXPERIMENT='swarm-of-theseus-execution-d1'
PREFIX='https://github.com/dmarzzz/swarm-lab/blob/'
REL='researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/'
def fetch(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'Cache-Control':'no-cache','User-Agent':'Theseus-D1'}),timeout=25) as r:data=r.read(2_000_001)
 if len(data)>2_000_000:raise GateError('public_document_too_large')
 return data.decode()
def raw(url):return url.replace('https://github.com/','https://raw.githubusercontent.com/').replace('/blob/','/')
def validate(receipt,revision,assignments,now=None):
 now=time.time() if now is None else now
 required={'experiment':EXPERIMENT,'source_commit':revision,'instrument_sha256':source_hash(),'assignments_sha256':digest(assignments),'model':MODEL,'max_calls':144,'cap_usd':5,'max_seconds':7200,'workers':1,'retries':0,'input_rate':1,'output_rate':5,'exclusive_claim_verified':True,'public_page_verified':True,'dependencies_verified':True,'research_review_status':'not-required-owner-direction'}
 for k,v in required.items():
  if receipt.get(k)!=v:raise GateError('admission_mismatch_'+k)
 for k in ('authority_allocation_id','owner_authorization_ref','claim_id','host','review_policy_ref','operator','allocation_verification_ref'):
  if not receipt.get(k):raise GateError('admission_missing_'+k)
 for k,age in [('verified_epoch',900),('public_page_verified_epoch',900),('pricing_verified_epoch',86400)]:
  if not 0<=now-receipt.get(k,0)<=age:raise GateError('stale_'+k)
 if receipt.get('claim_until_epoch',0)<now+7200:raise GateError('claim_too_short')
 expected=PREFIX+revision+'/'+REL+'PLAN.md'
 if receipt.get('plan_url')!=expected:raise GateError('wrong_plan_revision')
 if receipt.get('plan_sha256')!=hashlib.sha256((ROOT/'PLAN.md').read_bytes()).hexdigest():raise GateError('wrong_plan_hash')
 review=receipt.get('assessment_url','')
 if not re.fullmatch(re.escape(PREFIX)+r'[0-9a-f]{40}/'+re.escape(REL)+r'(?:reviews/)?[A-Za-z0-9_-]+\.md',review):raise GateError('immutable_assessment_required')
 if not re.fullmatch('[0-9a-f]{64}',receipt.get('assessment_sha256','')):raise GateError('assessment_hash_required')
 if len(assignments)!=144 or sum(len(a['cases']) for a in assignments)!=480:raise GateError('assignment_count_mismatch')
 return receipt

def public_check(receipt,read=fetch):
 state=json.loads(read('https://swarm-live.pages.dev/api/state'))
 exp=next((x for x in state['experiments'] if x['id']==EXPERIMENT),{})
 if exp.get('url')!=receipt['plan_url'] or not exp.get('description','').startswith('TLDR: '):raise GateError('registration_mismatch')
 plan=read(raw(receipt['plan_url']))
 if hashlib.sha256(plan.encode()).hexdigest()!=receipt['plan_sha256']:raise GateError('public_plan_hash_mismatch')
 for section in ('TLDR','Question and prediction','Setup','Protocol','Metrics','Launch gates'):
  if '\n## '+section+'\n' not in plan:raise GateError('missing_plan_section')
 review=read(raw(receipt['assessment_url']))
 if hashlib.sha256(review.encode()).hexdigest()!=receipt['assessment_sha256']:raise GateError('review_hash_mismatch')
 if not any(line.strip()=='Status: diagnostic-only' for line in review.splitlines()):raise GateError('review_not_admitted')
 return {'checked_epoch':time.time(),'plan_url':receipt['plan_url'],'plan_sha256':receipt['plan_sha256'],'assessment_sha256':receipt['assessment_sha256']}
