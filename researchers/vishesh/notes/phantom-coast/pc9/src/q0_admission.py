"""Fail-closed private operator receipts; attestations are not independent audits."""
import datetime,hashlib,json,subprocess
from pathlib import Path
from contract import digest
from qualification import assignments
from native import SNAPSHOT
from q0_ledger import PRIOR_NANO,PREDECESSOR
BASE=Path(__file__).resolve().parents[1]
def utc():return datetime.datetime.now(datetime.timezone.utc)
def parse(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
def fingerprint():
 files=sorted((BASE/'src').glob('*.py'))+[BASE/'NATIVE-PLAN.md',BASE/'PLAN.md',BASE/'q0.py']
 return {str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}

def receipt(ref):
 if not isinstance(ref,dict) or set(ref)!={'path','sha256'}:raise ValueError('receipt_reference')
 p=Path(ref['path'])
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=ref['sha256']:raise ValueError('receipt_hash')
 r=json.loads(p.read_text())
 if r.get('scope')!='pc9-q0-a1' or r.get('verified') is not True:raise ValueError('receipt_scope')
 return r

class Admission:
 def __init__(self,c,public_check):
  self.c=c
  if c.get('scope')!='pc9-q0-a1' or c.get('stage')!='Q0' or c.get('model')!=SNAPSHOT:raise ValueError('scope_or_model')
  head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip()
  if c.get('source_commit')!=head or c.get('instrument')!=fingerprint() or c.get('assignments_sha256')!=digest(assignments()):raise ValueError('source_binding')
  if subprocess.check_output(['git','status','--porcelain','--',str(BASE)],cwd=BASE,text=True).strip():raise ValueError('dirty_source')
  for flag in ('owner_scope_approved','exclusive_approved_account_allocation','predecessor_fenced','single_ledger_authority','credential_consumer_authorized','rendered_public_page_verified'):
   if c.get(flag) is not True:raise ValueError(flag)
  proofs={k:receipt(c.get(k)) for k in ('scope_authority','allocation','runtime','public_page','budget_lineage')}
  if c.get('prior_exposure_nano')!=PRIOR_NANO or c.get('predecessor_sha256')!=PREDECESSOR:raise ValueError('lineage')
  if hashlib.sha256(Path(c['predecessor_path']).read_bytes()).hexdigest()!=PREDECESSOR:raise ValueError('predecessor_file')
  now=utc()
  if not datetime.timedelta(0)<=now-parse(c['checked_utc'])<datetime.timedelta(minutes=5):raise ValueError('stale_receipt')
  self.deadline=min(parse(c['claim_until']),parse(c['deadline']))
  if self.deadline<now+datetime.timedelta(minutes=15):raise ValueError('short_allocation')
  public=public_check('phantom-coast-pc9',c['run_tldr']);h=hashlib.sha256((BASE/'NATIVE-PLAN.md').read_bytes()).hexdigest()
  url=f"https://github.com/dmarzzz/swarm-lab/blob/{head}/researchers/vishesh/notes/phantom-coast/pc9/NATIVE-PLAN.md"
  if public.get('url')!=url or public.get('plan_sha256')!=h:raise ValueError('public_plan')
  self.public=public
 def current(self):return utc()<self.deadline
