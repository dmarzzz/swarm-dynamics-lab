"""Fail-closed launch admission. Operator attestations remain explicitly attestations."""
import datetime
import hashlib
import json
import re
import subprocess
from pathlib import Path
from design import schedule,STAGES,qualified
from wire import digest,SNAPSHOT
BASE=Path(__file__).resolve().parents[1]

def fingerprint():
    files=sorted((BASE/'src').glob('*.py'))+[BASE/'src/replay-template.html']+[BASE/'PLAN.md',BASE/'reviews/RUNNER-PRE.md',BASE/'reviews/REVIEW-POLICY-AMENDMENT.md']
    return {str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}

def utc():return datetime.datetime.now(datetime.timezone.utc)
def date(x):return datetime.datetime.fromisoformat(x.replace('Z','+00:00'))

def receipt_file(entry):
    if not isinstance(entry,dict) or set(entry)!={'path','sha256'}:raise ValueError('evidence_reference')
    p=Path(entry['path'])
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:raise ValueError('evidence_hash')
    return p

class Admission:
    def __init__(self,c,stage,public_check,now=None):
        now=now or utc();self.stage=stage;self.c=c
        if stage not in STAGES or c.get('design')!='PC-6' or c.get('stage')!=stage or not re.fullmatch(r'[a-zA-Z0-9-]{3,80}',c.get('attempt','')):raise ValueError('configuration')
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip()
        if c.get('source_commit')!=head or c.get('instrument')!=fingerprint() or c.get('assignment_sha256')!=digest(schedule(stage)):raise ValueError('source_binding')
        for name in ('research_scope','pre_assessment','page_verification','allocation','budget_lineage','runtime'):
            receipt_file(c.get(name))
        # Scope is the operator's experiment/budget scope, not researcher approval.
        if c.get('research_scope_admitted') is not True:raise ValueError('research_scope_required')
        if c.get('authorization')!='phantom-coast-usd5-20261004' or c.get('prior_spend_nano')!=857148138 or c.get('api_cap_nano')!=4000000000 or c.get('max_calls')!=48:raise ValueError('budget_authority')
        for flag in ('predecessor_fenced','predecessor_reconciled','single_ledger_authority','exclusive_allocation','approved_mars_fleet','rendered_page_verified'):
            if c.get(flag) is not True:raise ValueError(flag)
        if not datetime.timedelta(0)<=now-date(c['checked_utc'])<datetime.timedelta(minutes=5):raise ValueError('stale_admission')
        self.deadline=min(date(c['claim_until']),date(c['deadline']))
        if self.deadline<now+datetime.timedelta(minutes=65):raise ValueError('insufficient_time')
        if c.get('model')!=SNAPSHOT or c.get('ledger_sha256') is None:raise ValueError('model_or_ledger')
        ledger=Path(c['ledger_path'])
        if not ledger.is_file() or hashlib.sha256(ledger.read_bytes()).hexdigest()!=c['ledger_sha256']:raise ValueError('ledger_binding')
        public=public_check('phantom-coast-pc6',c['run_tldr'])
        if public['url']!=c.get('plan_url') or public['plan_sha256']!=c.get('plan_sha256') or public['plan_sha256']!=hashlib.sha256((BASE/'PLAN.md').read_bytes()).hexdigest():raise ValueError('public_plan_binding')
        self.public=public
    def allows(self,seed):return type(seed) is int and seed in STAGES[self.stage] and self.current()
    def current(self):return utc()<self.deadline
