"""Fail-closed Q3 packet/source/funding evidence checks. Receipts confer no authority themselves."""
from pathlib import Path
import hashlib,json,time,urllib.request
ROOT=Path(__file__).resolve().parent
ATTEMPT='R3-Q3-A1';EXPERIMENT='swarm-of-theseus-r3-q3'
PRIOR='1.1637270437';MODEL_CAP='2.4462';ALL_IN='3.4462'

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def source_hash():
 paths=list(ROOT.glob('*.py'))+[ROOT.parent/'instrument.py',ROOT.parent/'native.py']
 return digest({str(p.relative_to(ROOT.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)})
def plan_url(revision):return 'https://github.com/dmarzzz/swarm-lab/blob/'+revision+'/researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/sol50/baseline-replication/Q3-PLAN.md'

def validate_packet(p):
 from development import dev_world
 if p.get('attempt')!=ATTEMPT or p.get('stage')!='Q3' or p.get('max_calls')!=108:raise ValueError('packet_scope')
 assignments=p.get('assignments',[])
 if [a.get('family') for a in assignments]!=['release','failover','delegation']:raise ValueError('family_assignments')
 seeds=[]
 for a in assignments:
  w=a.get('world',{});seed=w.get('seed')
  if type(seed) is not int or seed<2**40 or w!=dev_world(seed):raise ValueError('fresh_world_contract')
  seeds.append(seed)
 if len(set(seeds))!=3:raise ValueError('duplicate_world')
 return True

def validate(receipt,grant,packet,revision,now=None):
 now=time.time() if now is None else now;validate_packet(packet)
 expected={'attempt':ATTEMPT,'stage':'Q3','source_commit':revision,'source_sha256':source_hash(),'packet_sha256':digest(packet),'model':'openai/gpt-6-sol','provider':'OpenAI','reasoning_effort':'none','max_calls':108,'max_input_bytes':6500,'max_output_tokens':512,'model_cap_usd':MODEL_CAP,'all_in_cap_usd':ALL_IN,'prior_exposure_usd':PRIOR,'study_cap_usd':'60','portfolio_cap_usd':'200','retry_count':0}
 for key,value in expected.items():
  if receipt.get(key)!=value:raise ValueError('admission_'+key)
 for key in ('approved_account_verified','exclusive_allocation_verified','worker_idle_verified','host_key_verified','ledger_reconciled','public_page_verified','runtime_verified','provider_capacity_verified','aggregate_publication_authorized'):
  if receipt.get(key) is not True:raise ValueError('missing_'+key)
 if not 0<=now-receipt.get('verified_epoch',0)<=900:raise ValueError('stale_admission')
 if receipt.get('claim_until_epoch',0)<now+1800:raise ValueError('claim_expiry')
 for key in ('host','claim_evidence_sha256','account_evidence_sha256','historical_ledger_sha256'):
  if not receipt.get(key):raise ValueError('missing_'+key)
 if receipt.get('plan_url')!=plan_url(revision) or receipt.get('plan_sha256')!=hashlib.sha256((ROOT/'Q3-PLAN.md').read_bytes()).hexdigest():raise ValueError('immutable_plan')
 if grant.get('funding_status')!='funded' or grant.get('reservation_status')!='reserved':raise ValueError('unfunded')
 for key in ('attempt','stage','packet_sha256','source_sha256','model_cap_usd','all_in_cap_usd','prior_exposure_usd','study_cap_usd','portfolio_cap_usd'):
  if grant.get(key)!=expected[key]:raise ValueError('grant_'+key)
 if grant.get('infrastructure_cap_usd')!='1' or grant.get('reservation_amount_usd')!=ALL_IN:raise ValueError('grant_envelope')
 for key in ('pi_decision_evidence','portfolio_reservation_id'):
  if not grant.get(key):raise ValueError('grant_evidence_'+key)
 if not now<grant.get('expires_epoch',0):raise ValueError('grant_expired')
 if grant.get('portfolio_reservation_id')!='PI-FUND-20261004-06':raise ValueError('named_pi_decision')
 if receipt.get('grant_sha256')!=digest(grant):raise ValueError('grant_binding')
 return True

def public_check(receipt):
 def fetch(url):
  req=urllib.request.Request(url,headers={'User-Agent':'Theseus-R3','Cache-Control':'no-cache'})
  with urllib.request.urlopen(req,timeout=30) as r:data=r.read(10000001)
  if len(data)>10000000:raise ValueError('public_response_bound')
  return data
 state=json.loads(fetch('https://swarm-live.pages.dev/api/state'));exp=next((e for e in state['experiments'] if e.get('id')==EXPERIMENT),{})
 if exp.get('url')!=receipt['plan_url'] or not exp.get('description','').startswith('TLDR: '):raise ValueError('public_registration')
 url=receipt['plan_url'].replace('https://github.com/','https://raw.githubusercontent.com/').replace('/blob/','/')
 if hashlib.sha256(fetch(url)).hexdigest()!=receipt['plan_sha256']:raise ValueError('public_plan_hash')
 return {'verified_epoch':time.time(),'plan_url':receipt['plan_url']}
