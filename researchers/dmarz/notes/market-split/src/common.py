from __future__ import annotations
import hashlib
import json
import re
import subprocess
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parent.parent
EXP = 'market-split'


def load(name):
    return yaml.safe_load((ROOT/name).read_text())


def git(*args):
    return subprocess.run(['git',*args],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()


def source_hash():
    h=hashlib.sha256()
    for p in sorted((ROOT/'src').glob('*')):
        if p.is_file(): h.update(p.name.encode());h.update(p.read_bytes())
    return h.hexdigest()


def design_hash():
    return hashlib.sha256((ROOT/'design.yaml').read_bytes()).hexdigest()


def assert_frozen(attempt):
    if not re.fullmatch('[a-z0-9-]{3,70}',attempt): raise ValueError('invalid attempt ID')
    review=ROOT/'reviews'/f'{attempt}-pre.md'
    if not review.exists() or 'Status: ready' not in review.read_text():
        raise ValueError('complete and commit a ready pre-run assessment for this attempt')
    paths=['src','design.yaml','preregistration.md',str(review.relative_to(ROOT))]
    if git('status','--porcelain','--',*paths): raise ValueError('commit protocol, source and assessment before execution')
    git('ls-files','--error-unmatch',str(review.relative_to(ROOT)))
    if load('design.yaml').get('api_budget_usd') != 0: raise ValueError('this worker only supports zero-cost scripted qualification')
    return git('rev-parse','HEAD')


def plans(stage,attempt):
    d=load('design.yaml')
    if stage not in ('S0','S1'): raise ValueError('S2 blocked: prior-art and cross-researcher hypothesis gates are unmet')
    st=d['stages'][stage]
    return [{'stage':stage,'backend':'scripted','regulator':reg,'threshold':threshold,
             'registration_fee':fee,'tasks':st['tasks'],'seeds':st['seeds'],'arms':d['arms'],
             'cfg':{**d['cfg'],'rounds':st['rounds'],'registration_fee':fee},'attempt_id':attempt,
             'code':git('rev-parse','HEAD'),'engine_sha256':source_hash(),'design_sha256':design_hash()}
            for reg in d['regulators'] for threshold in st['thresholds'] for fee in st['fees']]


def dump(path,value):
    Path(path).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
