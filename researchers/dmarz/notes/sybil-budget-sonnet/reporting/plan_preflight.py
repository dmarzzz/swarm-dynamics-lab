"""Fail-closed public-plan check before a stage, reusing the shared validator.

Validates experiment.yaml's immutable plan URL and TLDR against the plan fetched
from GitHub (works before hub registration). No credentials, no model calls.
Usage: python3 reporting/plan_preflight.py --run-tldr "..." --receipt reviews/<attempt>-plan-receipt.json
"""
import argparse,importlib.util,json,yaml
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('public_plan',ROOT.parents[2]/'vishesh/notes/experiment-documentation/public_plan.py')
pp=importlib.util.module_from_spec(spec);spec.loader.exec_module(pp)
ap=argparse.ArgumentParser();ap.add_argument('--run-tldr',required=True);ap.add_argument('--receipt',required=True);a=ap.parse_args()
exp=yaml.safe_load((ROOT/'experiment.yaml').read_text())
raw=(exp.get('url') or '').replace('https://github.com/','https://raw.githubusercontent.com/').replace('/blob/','/')
try:
    receipt=pp.validate(exp,pp.fetch(raw),a.run_tldr)
except Exception as e:
    raise SystemExit('Public plan preflight failed: '+(str(e) if isinstance(e,ValueError) else type(e).__name__))
with Path(a.receipt).open('x') as f:json.dump(receipt,f,indent=2)
print('Public plan preflight passed: '+json.dumps({k:receipt[k] for k in ('commit','plan_sha256','checked_utc')}))
