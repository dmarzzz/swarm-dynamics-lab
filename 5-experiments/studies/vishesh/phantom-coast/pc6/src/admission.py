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
    files=sorted((BASE/'src').glob('*.py'))+[BASE/'src/PARKED.json']+[BASE/'PLAN.md',BASE/'reviews/RUNNER-PRE.md',BASE/'reviews/REVIEW-POLICY-AMENDMENT.md']
    return {str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}

def utc():return datetime.datetime.now(datetime.timezone.utc)
def date(x):return datetime.datetime.fromisoformat(x.replace('Z','+00:00'))

def receipt_file(entry):
    if not isinstance(entry,dict) or set(entry)!={'path','sha256'}:raise ValueError('evidence_reference')
    p=Path(entry['path'])
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:raise ValueError('evidence_hash')
    return p

class Admission:
    def __init__(self,*args,**kwargs):
        raise ValueError('pc6_parked_no_decision_value')
