"""Operator-only saved-data finalize hook. No allocation, model or reporting calls."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

STAGES=('peer-contract-q2',)


def command(checkout,results,stage,outcome,worker_stopped):
    root=Path(checkout).resolve();saved=Path(results).resolve()
    if not worker_stopped:raise ValueError('verified_worker_stop_required')
    if stage not in STAGES or outcome not in ('completed','failed','blocked','ambiguous'):
        raise ValueError('invalid_closeout_scope')
    relative=saved.relative_to(root/'data')
    if not saved.is_dir() or not (saved/'summary.json').is_file():raise ValueError('saved_evidence_required')
    if not (root/'scripts/experiment.py').is_file():raise ValueError('canonical_operations_checkout_required')
    return [sys.executable,str(root/'scripts/experiment.py'),'finalize','immune-response-v3',
            '--attempt',stage,'--results',str(Path('data')/relative),'--outcome',outcome,'--worker-stopped']


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--checkout',required=True);p.add_argument('--results',required=True)
    p.add_argument('--stage',choices=STAGES,required=True);p.add_argument('--outcome',choices=['completed','failed','blocked','ambiguous'],required=True)
    p.add_argument('--worker-stopped',action='store_true');a=p.parse_args()
    result=subprocess.run(command(a.checkout,a.results,a.stage,a.outcome,a.worker_stopped),cwd=a.checkout)
    if result.returncode:raise SystemExit(result.returncode)
    print(json.dumps({'operational_finalize':'completed','scientific_review':'still_required','next_stage_authorized':False}))
