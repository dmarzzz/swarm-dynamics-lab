#!/usr/bin/env python3
"""Offline packaging and publication from terminal records. Never provider calls."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile
import durable as d
import run as r

ROOT=Path(__file__).resolve().parent
BASE=ROOT/'results'


def package():
    target=BASE/'numeric-evidence.zip';outer=BASE/'archive-checksum.json'
    if target.exists():
        if d.read(outer)['sha256']!=d.sha(target):raise RuntimeError('existing_archive_mismatch')
        return target
    paths=[BASE/'admission.json',BASE/'assignments.json',BASE/'calls.jsonl']
    paths += [p for route in ('pool','openrouter') for p in sorted((BASE/route).rglob('*.json'))]
    inner={'source_revision':d.read(BASE/'admission.json')['source_revision'],
           'files':{str(p.relative_to(BASE)):d.sha(p) for p in paths}}
    # Inner manifest hashes payload only. Outer checksum is never inside the ZIP.
    d.immutable(BASE/'numeric-inventory.json',inner)
    with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for p in paths+[BASE/'numeric-inventory.json']:z.write(p,str(p.relative_to(BASE)))
    d.immutable(outer,{'file':target.name,'sha256':d.sha(target),'bytes':target.stat().st_size})
    with zipfile.ZipFile(target) as z:
        if z.testzip() is not None:raise RuntimeError('archive_crc')
        for name,digest in inner['files'].items():
            if hashlib.sha256(z.read(name)).hexdigest()!=digest:raise RuntimeError('archive_payload_mismatch')
    return target


def hub():
    archive=package();sr=r.hub_client();summary=d.read(BASE/'summary.json')
    existing={x['run']:x for x in sr.runs(experiment=r.SPEC_ID,limit=50)}
    for cohort in summary['cohorts']:
        name=cohort['cohort'];receipt=BASE/f'hub-{name}.json'
        if receipt.exists():continue
        run_id=r.SPEC_ID+'/'+name+'-001'
        params={'route':name,'cohort':name+'-001','admission_sha256':d.sha(BASE/'admission.json')}
        if run_id in existing:
            if existing[run_id].get('params')!=params:raise RuntimeError('hub_id_collision')
            if existing[run_id]['status'] in ('done','failed'):
                d.immutable(receipt,{'run':run_id,'status':existing[run_id]['status'],'readback':True,'params':params})
                continue
        run=sr.start(r.SPEC_ID,run=run_id,params=params,message='Closed qualification diagnostic; no valid model answers, not a treatment finding')
        for path in [archive,BASE/'archive-checksum.json',BASE/'summary.json',BASE/'recomputation.json',BASE/'FINDING.md',ROOT/'POSTMORTEM.md']:
            run.artifact(path,path.name if path!=archive else 'numeric-evidence-'+d.sha(archive)[:16]+'.zip')
        run.fail(message=f'{name}: first clean request refused; no main observations; independent check pending',
                 valid=cohort['terminal']['completed'],failed=cohort['terminal']['failed'],
                 unstarted=cohort['terminal']['not_run'],complete_roots=cohort['complete_roots'],
                 paid_liability=cohort['reported_paid_usd'])
        actual=sr.get_run(run_id)
        if actual.get('status')!='failed':raise RuntimeError('hub_terminal_readback')
        d.immutable(receipt,{'run':run_id,'status':actual['status'],'readback':True,'params':params,
                            'metrics':actual.get('metrics'),'created':d.now()})
        print('hub terminal verified:',run_id)


def evidence():
    path=r.REPO/'experiments/evidence-metadata.json';reg=d.read(path)
    prefix=str(ROOT.relative_to(r.REPO));ident=r.SPEC_ID
    row={'id':ident,'title':'Provenance / duplication invariance, blocked clean-screen diagnostic',
         'documents':[prefix+'/results/FINDING.md',prefix+'/POSTMORTEM.md'],
         'experiment_ids':[ident],'registration_paths':[],
         'assessor':'shadow/sol-factory','assessed_at':'2026-10-04',
         'source_commit':d.read(BASE/'admission.json')['source_revision'],
         'evidence_confidence':{'score':0,'claim':'No model answer or treatment contrast observed; two qualification requests refused.',
             'rationale':'Pool HTTP400 with unsupported wire-schema bounds identified; paid fallback HTTP403. All main cells unstarted. Same-author recomputation does not establish model competence or independent review.'},
         'sample_size_summary':'Observed:2 HTTP attempts,0 valid answers,0 complete paired roots. Planned:12 synthetic numeric roots with12 main calls/root; six qualification calls/route.300 potential conditional assignments are fully enumerated; max151 actual HTTP requests across routes. Calls/copies are not independent worlds.',
         'sources':[prefix+'/SPEC.md',prefix+'/results/admission.json',prefix+'/results/summary.json',prefix+'/results/recomputation.json',prefix+'/results/numeric-inventory.json'],
         'status_at_assessment':'blocked-unqualified'}
    reg['studies']=[x for x in reg['studies'] if x['id']!=ident]+[row]
    path.write_text(json.dumps(reg,indent=2)+'\n')
    subprocess.run([sys.executable,'scripts/experiment_evidence.py','--write'],cwd=r.REPO,check=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['package','hub','evidence']);a=p.parse_args()
    if a.action=='package':print(package())
    elif a.action=='hub':hub()
    else:evidence()
