#!/usr/bin/env python3
"""Materialize our evidence rows and report registered experiments/results to hub.
Never edits another owner's registry rows. Run after results are snapshotted/terminal.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import factory as f

BASE='https://github.com/dmarzzz/swarm-lab/tree/main/researchers/shadow/factory'

def update_evidence():
    path=f.REPO/'experiments/evidence-metadata.json';reg=json.loads(path.read_text())
    own=[]
    for file in sorted((f.ROOT/'results').glob('*/summary.json')):
        out=file.parent;s=json.loads(file.read_text());spec=json.loads((f.ROOT/'specs'/f"{s['spec']}.json").read_text())
        if not (out/'terminal.json').exists():continue
        ident='shadow-factory-'+s['spec'];prefix=str(out.relative_to(f.REPO))
        n=s['main_valid'];complete=n==192 and s['qualification_passed']
        claim=(f"{spec['model']}, {spec['internal_links']} internal links, pass={spec['attacker_pass']}, checks={spec['checks']}: "
               +(f"paired splitting difference-in-differences {s['primary']:+.4f}; exploratory same-family sensitivity, not a general defense claim." if s['primary'] is not None else 'No interpretable treatment contrast; qualification/transport stopped before complete paired outcomes.'))
        own.append(dict(id=ident,title=spec['title']+' ('+spec['route']+')',documents=[prefix+'/FINDING.md'],
            experiment_ids=[ident],registration_paths=[],assessor='shadow/sol-factory',assessed_at='2026-10-04',
            source_commit=json.loads((out/'provenance.json').read_text())['commit'],
            evidence_confidence=dict(score=2 if complete else (1 if n else 0),claim=claim,
                rationale='Source-reported exploratory comparison; 48 reused synthetic roots in two graph families, reduced clean qualification, no independent review, model/configuration change and five unadjusted dependent contrasts.' if n else 'Transport or clean-screen failure prevents treatment inference. All failed and unstarted outcomes are retained.'),
            sample_size_summary=f"Observed: {s['paired_roots']}/48 complete paired synthetic roots; main {n}/192 valid; all stages {s['valid']}/{s['planned']} valid, {s['failed']} failed, {s['unstarted']} unstarted. Qualification planned 12. Parent roots reused; no independent-real-world sample.",
            sources=[prefix+'/summary.json',prefix+'/records.jsonl',prefix+'/provenance.json',str((f.ROOT/'specs'/f"{s['spec']}.json").relative_to(f.REPO))],
            status_at_assessment=s['status']))
    ids={r['id'] for r in own}
    reg['studies']=[r for r in reg['studies'] if r['id'] not in ids]+own
    f.dump(path,reg)
    subprocess.run([sys.executable,'scripts/experiment_evidence.py','--write'],cwd=f.REPO,check=True)
    print('evidence rows:',len(own))

def hub(register_only=False):
    sys.path.insert(0,os.environ.get('SWARM_REPORT_PATH',str(Path.home()/'projects/swarm-labs-agentops/hub')))
    import swarm_report as sr
    os.environ['SWARM_SOURCE']='shadow/sol-factory'
    for file in sorted((f.ROOT/'specs').glob('*.json')):
        spec=json.loads(file.read_text());name=spec['id'];ident='shadow-factory-'+name
        out=f.ROOT/'results'/name
        # Locally persisted registration receipts avoid repeated API writes.
        receipt=f.ROOT/'hub'/f'{name}.json'
        if not receipt.exists():
            sr.register(ident,title=spec['title']+' ('+spec['route']+')',owner='shadow',
                description='Prospective exploratory factory sensitivity. Parent Dmarz sybil-split-opus; Sonnet configuration, same 48 synthetic roots; independently unreviewed.',
                params={'model':{'type':'str','role':'fixed'},'route':{'type':'str','role':'fixed'},'spec':{'type':'str','role':'condition'}},
                metrics=['primary','paired_roots','valid','failed','unstarted','paid_usd'],primary_metric='primary',url=BASE+'/specs/'+file.name)
            f.dump(receipt,dict(experiment=ident,registered_at=f.now()))
            time.sleep(.25)
        if register_only or not (out/'terminal.json').exists():continue
        done=f.ROOT/'hub'/f'{name}-closed.json'
        if done.exists():continue
        s=json.loads((out/'summary.json').read_text())
        run=sr.start(ident,run=ident+'/cohort-001',params={'model':spec['model'],'route':spec['route'],'spec':name},message='Saved terminal factory cohort, no automatic launch')
        for filename in ('FINDING.md','summary.json','cells.csv','records.jsonl','provenance.json','dispatch.jsonl'):
            run.artifact(out/filename,filename)
        metrics={k:s[k] for k in ('primary','paired_roots','valid','failed','unstarted','paid_usd') if s[k] is not None}
        msg=f"{s['status']}; {s['valid']}/{s['planned']} valid, {s['failed']} failed, {s['unstarted']} unstarted; exploratory"
        if s['main_valid']==192 and s['qualification_passed']:run.done(message=msg,**metrics)
        else:run.fail(message=msg,**metrics)
        # Verify server state rather than equating a local/spooled done event with delivery.
        state=sr.get_run(ident+'/cohort-001')
        expected='done' if s['main_valid']==192 and s['qualification_passed'] else 'failed'
        assert state.get('status')==expected, 'hub terminal readback mismatch'
        f.dump(done,dict(experiment=ident,run=ident+'/cohort-001',closed_at=f.now(),status=state.get('status'),metrics=state.get('metrics')))
        print('hub:',ident,s['status'])
        time.sleep(.25)

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['evidence','hub','register']);args=p.parse_args()
    if args.action=='evidence':update_evidence()
    else:hub(args.action=='register')
if __name__=='__main__':main()
