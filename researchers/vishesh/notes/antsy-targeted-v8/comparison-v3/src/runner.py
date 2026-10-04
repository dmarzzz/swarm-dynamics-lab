"""Bounded native comparison controller. Offline tests inject a collector; no auto-retry."""
import argparse
import json
import os
from pathlib import Path
import sys
import time
from common import HERE,STUDY,REPO,digest,sha,write
from compare import evaluate,qualify
from receipts import Receipts,snapshot
from worker import settings
sys.path.insert(0,str(STUDY/'execution-repair-v1'))
from capture import run_once

STAGES={'qualification':('Q0-comparison',6,12),'evaluation':('E0-comparison',18,36)}
STAGE_SECONDS={'qualification':1200,'evaluation':2400}


def instrument():
    paths=list(HERE.glob('*.py'))+[HERE.parent/'PLAN.md',STUDY/'src/fields.py',STUDY/'src/adapter.py',
      STUDY/'trace-repair-v2/fields.py',STUDY/'execution-repair-v1/capture.py',STUDY/'execution-repair-v1/telemetry.py',
      STUDY/'execution-repair-v1/worker.py',STUDY.parent/'antsy-diversity-v7/src/core.py',
      STUDY.parent/'antsy-receipt-v6/src/contract.py',REPO/'scripts/experiment_ops/trace_receipts.py']
    return digest({str(p.relative_to(REPO)):sha(p) for p in sorted(paths)})


def admit(a,stage,freeze,runtime,now=None):
    now=time.time() if now is None else now
    attempt,n,cap=STAGES[stage]
    expected={'study':'antsy-targeted-v8','attempt':attempt,'instrument_sha256':instrument(),
      'freeze_sha256':digest(freeze),'runtime_sha256':digest(runtime),'max_calls':cap,'max_total_calls':48,
      'deadline_s':90,'eligibility_s':45,'new_charge_cap_usd':0,'automatic_retries':False}
    if not all(a.get(k)==v for k,v in expected.items()):raise ValueError('admission_contract_mismatch')
    flags=('owner_scope_approved','exclusive_claim_verified','approved_account_verified','runtime_pinned',
           'public_plan_registered','public_page_verified','prior_budget_reconciled','duplicate_dispatch_fenced')
    if not all(a.get(k) is True for k in flags):raise ValueError('admission_missing')
    if not isinstance(a.get('authority_reference_sha256'),str) or len(a['authority_reference_sha256'])!=64:raise ValueError('authority_reference_missing')
    if not (0<=now-a['verified_at']<900 and now+STAGE_SECONDS[stage]+60<a['claim_expires_at']):raise ValueError('admission_stale')
    if not (type(a.get('previous_calls')) is int and a['previous_calls']==(0 if stage=='qualification' else 12)):
        raise ValueError('call_reservation_mismatch')
    if stage=='evaluation':
        q=a.get('qualification',{})
        if q.get('passed') is not True or q.get('instrument_sha256')!=instrument() or q.get('freeze_sha256')!=digest(freeze):
            raise ValueError('qualification_missing')
    return True


def native_invoke(reader,image,directory,runtime):
    py=runtime['interpreters'][reader]
    command=[py,str(HERE/'worker.py'),'--engine',reader,'--image',str(image),'--models',runtime['models'],
             '--out','{out}','--phases','{phases}']
    return run_once(command,directory,image,sha(image),deadline_s=90,eligibility_s=45)


def collect(stage,case_root,out,freeze,runtime,invoke=native_invoke,clock=time.monotonic):
    """Caller must admit native use. No resume; a stopped attempt stays stopped."""
    attempt,count,cap=STAGES[stage]
    manifest=case_root/stage/'actor/manifest.json';truth=case_root/stage/'evaluator/gold.json'
    if sha(manifest)!=freeze['splits'][stage]['actor_sha256'] or sha(truth)!=freeze['splits'][stage]['gold_sha256']:
        raise ValueError('case_freeze_mismatch')
    cases=json.loads(manifest.read_text())['cases'];gold=json.loads(truth.read_text())['cases']
    if len(cases)!=count or [c['id'] for c in cases]!=[g['id'] for g in gold]:raise ValueError('case_roster_mismatch')
    for c in cases:
        image=case_root/stage/'actor'/c['image']
        if image.parent!=case_root/stage/'actor' or image.is_symlink() or sha(image)!=c['sha256']:raise ValueError('input_mismatch')
    out.mkdir(mode=0o700,exist_ok=False);(out/'private').mkdir(mode=0o700);(out/'private/calls').mkdir(mode=0o700)
    config={'stage':stage,'source':instrument(),'runtime':runtime,'freeze_sha256':digest(freeze),
            'engine_settings':{r:settings(r) for r in ('P','C')},'deadline_s':90,'eligibility_s':45}
    recorder=Receipts(out,attempt,cases,instrument(),config)
    write(out/'reservation.json',{'attempt':attempt,'reserved_calls':cap,'new_charge_usd':0,'no_new_allowance':True})
    records={};start=clock();stop='completed';index=0
    try:
        for case in cases:
            for reader in ('P','C'):
                if clock()-start+92>STAGE_SECONDS[stage]:stop='stage_deadline';break
                image=case_root/stage/'actor'/case['image'];directory=out/'private/calls'/f'{index+1:03d}'
                context={'configuration':config,'engine':reader,'input_sha256':case['sha256']}
                recorder.begin(index,image,context)
                try:
                    result=invoke(reader,image,directory,runtime)
                    effective=directory/'private/effective-context.json'
                    expected={'settings':settings(reader),'input_sha256':case['sha256'],'worker_source_sha256':sha(HERE/'worker.py')}
                    if result['status']=='valid' and (not effective.is_file() or json.loads(effective.read_text())!=expected):
                        result={**result,'status':'error','category':'effective_context_mismatch'}
                except Exception:
                    result={'status':'error','category':'supervisor_exception','wall_s':None}
                recorder.terminal(index,result,directory)
                row={k:result.get(k) for k in ('status','category','wall_s')}
                if result['status']=='valid':row['raw_words']=json.loads((directory/'private/output.json').read_text())['raw_words']
                records.setdefault(case['id'],{})[reader]=row
                snapshot(out/'private/records.json',records);index+=1
                if result['status']!='valid':stop=result['category'];break
                audit=recorder.audit()
                if audit['status']!='verified_declared_coverage':stop='trace_gap';break
            if stop!='completed':break
    except BaseException:
        stop='interrupted'
        raise
    finally:
        report=evaluate(gold,records);trace=recorder.audit()
        summary={'attempt':attempt,'assigned_calls':cap,'started_calls':trace.get('started_count',0),
                 'unresolved_started':trace.get('unresolved_started',0),
                 'unstarted_calls':sum(c['status']=='unstarted' for c in recorder.value['calls']),
                 'stop':stop,'instrument_sha256':instrument(),'freeze_sha256':digest(freeze),
                 'trace_status':trace['status'],'qualification_passed':stage=='qualification' and stop=='completed' and trace['status']=='verified_declared_coverage' and qualify(gold,records),
                 'new_charge_usd':0,'model_calls':0,'automatic_successor':False,**report}
        # Public data: values/counts/timings only. Raw OCR and runtime paths stay private.
        write(out/'summary.json',summary);write(out/'trace-audit.json',trace)
        from render import render
        render(summary,out/'final_frame.png')
    return summary


def main():
    p=argparse.ArgumentParser();p.add_argument('--stage',choices=STAGES,required=True);p.add_argument('--cases',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--admission',type=Path,required=True);p.add_argument('--runtime',type=Path,required=True);p.add_argument('--qualification',type=Path)
    a=p.parse_args();os.umask(0o077)
    freeze=json.loads((a.cases/'freeze.json').read_text());runtime=json.loads(a.runtime.read_text());admission=json.loads(a.admission.read_text())
    if a.stage=='evaluation':
        if a.qualification is None:raise ValueError('saved_qualification_required')
        q=json.loads(a.qualification.read_text())
        expected={'passed':q.get('qualification_passed'),'instrument_sha256':q.get('instrument_sha256'),
                  'freeze_sha256':q.get('freeze_sha256')}
        if admission.get('qualification')!=expected or admission.get('qualification_sha256')!=sha(a.qualification):
            raise ValueError('qualification_receipt_mismatch')
    admit(admission,a.stage,freeze,runtime)
    result=collect(a.stage,a.cases,a.out,freeze,runtime)
    print(json.dumps({k:result[k] for k in ('attempt','started_calls','unstarted_calls','stop','qualification_passed','trace_status')}))

if __name__=='__main__':
    try:main()
    except Exception:raise SystemExit('comparison_failed_see_retained_private_evidence') from None
