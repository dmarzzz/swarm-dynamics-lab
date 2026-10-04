#!/usr/bin/env python3
"""Only this frozen pilot. No CLI model/budget override, no retries, no scaling."""
import argparse
from datetime import datetime
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.error
import urllib.request

import durable as d
import instrument as ins

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[4]
RESULTS=ROOT/'results'
SPEC_ID='shadow-factory-provenance-attempt2'
DEADLINE=datetime.fromisoformat('2026-10-04T23:00:00+00:00').timestamp()
PAID=d.PaidLedger(ROOT.parents[1]/'results/paid-ledger.jsonl')
SOURCES=['SPEC.md','PRE-RUN.md','instrument.py','durable.py','run.py','analyze.py','recompute.py','test_pilot.py','requirements.txt','HISTORICAL-REVIEW.md']


class AdmissionError(RuntimeError):pass


def require(ok,why):
    if not ok:raise AdmissionError(why)


def git(*args):return subprocess.check_output(['git',*args],cwd=REPO,text=True).strip()


def source_hashes():return {p:d.sha(ROOT/p) for p in SOURCES}


def hub_client():
    sys.path.insert(0,os.environ.get('SWARM_REPORT_PATH',str(Path.home()/'projects/swarm-labs-agentops/hub')))
    import swarm_report
    return swarm_report


def prepare():
    """Publication verification only. No provider request or credential loading."""
    require(not (RESULTS/'admission.json').exists(),'already_prepared')
    s=ins.spec();require(s['id']==SPEC_ID and s['max_http_attempts']==149,'scope_drift')
    require(s['max_paid_usd']==9 and s['factory_max_paid_usd']==10.851345,'budget_drift')
    for name in SOURCES:
        rel=str((ROOT/name).relative_to(REPO))
        committed=subprocess.check_output(['git','show','HEAD:'+rel],cwd=REPO)
        require(committed==(ROOT/name).read_bytes(),'uncommitted_source:'+name)
    revision=git('rev-parse','HEAD');rel=str((ROOT/'SPEC.md').relative_to(REPO))
    url=f'https://github.com/dmarzzz/swarm-lab/blob/{revision}/{rel}'
    raw=f'https://raw.githubusercontent.com/dmarzzz/swarm-lab/{revision}/{rel}'
    with urllib.request.urlopen(raw,timeout=30) as r:published=r.read(100000)
    require(published==(ROOT/'SPEC.md').read_bytes(),'public_plan_mismatch')
    with urllib.request.urlopen(url,timeout=30) as r:page=r.read(2500000)
    require(b'Provenance / duplication invariance' in page,'rendered_plan_missing')
    sr=hub_client()
    sr.register(SPEC_ID,title='Shadow: provenance / duplication invariance',owner='shadow',url=url,
        description='Bounded 12-root exploratory diagnostic. Fixed evidence, copies1/4/16; raw, supplied ancestry, exact dedup and irrelevant padding. Six clean cases before comparisons. Synthetic rule accuracy, false confidence, decision flips; not native Quorum or real-world provenance.',
        params={'route':{'type':'str','role':'condition'},'cohort':{'type':'str','role':'condition'}},
        metrics=['valid','failed','unstarted','complete_roots','paid_liability'],primary_metric='complete_roots')
    registered=next((e for e in sr._call('GET','/api/v1/experiments') if e['id']==SPEC_ID),None)
    require(registered is not None and registered.get('url')==url,'hub_registration_not_verified')
    versions={p:importlib.metadata.version(p) for p in ('tiktoken','PyYAML')}
    require(versions=={'tiktoken':'0.12.0','PyYAML':'6.0.2'},'dependency_version_drift')
    assignments={route:ins.assignments(route) for route in ('openrouter',)}
    manifest={'study':SPEC_ID,'source_revision':revision,'source_sha256':source_hashes(),
              'assignment_digest':{k:ins.digest(v) for k,v in assignments.items()},
              'public_plan_url':url,'spec_sha256':d.sha(ROOT/'SPEC.md'),'created':d.now(),
              'max_http_attempts':149,'max_paid_usd':9,'factory_max_paid_usd':10.851345,'prior_http_attempts':2,
              'deadline':DEADLINE,'prior_factory_paid_liability':PAID.liability(),
              'registration_readback':{'id':registered['id'],'url':registered['url']},
              'rendered_page_sha256':hashlib.sha256(page).hexdigest(),
              'dependency_versions':versions,'python':sys.version,
              'tokenizer':'tiktoken 0.12.0 cl100k_base','memory':'fresh stateless call; no inherited operator context',
              'qualified':False,'scope':'Q then conditional M, exact fixed assignment list',
              'routes':['openrouter']}
    d.immutable(RESULTS/'assignments.json',assignments)
    manifest['assignment_file_sha256']=d.sha(RESULTS/'assignments.json')
    d.immutable(RESULTS/'admission.json',manifest)
    print(json.dumps({'prepared':SPEC_ID,'source_revision':revision,'assigned_per_route':len(assignments['openrouter']),
                      'prior_factory_liability':manifest['prior_factory_paid_liability']}))


def admitted(route,assignment):
    m=d.read(RESULTS/'admission.json')
    require(m['study']==SPEC_ID and m['max_http_attempts']==149,'admission_scope')
    require(m['source_sha256']==source_hashes(),'runtime_source_drift')
    require(m['dependency_versions']=={p:importlib.metadata.version(p) for p in ('tiktoken','PyYAML')},'dependency_drift')
    require(m['assignment_file_sha256']==d.sha(RESULTS/'assignments.json'),'assigned_file_drift')
    require(m['registration_readback']=={'id':SPEC_ID,'url':m['public_plan_url']},'registration_binding')
    require(time.time()<min(m['deadline'],DEADLINE),'deadline')
    require(route in ('openrouter',),'route')
    all_assignments=d.read(RESULTS/'assignments.json')
    aa=all_assignments[route]
    require(ins.digest(aa)==m['assignment_digest'][route],'assignment_manifest_drift')
    require(any(a==assignment for a in aa),'assignment_not_admitted')
    if assignment['stage']=='M':
        outcomes=[d.read(RESULTS/route/'outcomes'/f'{a["id"]}.json') for a in aa if a['stage']=='Q']
        require(len(outcomes)==6 and all(r['status']=='completed' and r['metrics']['accuracy']==1 for r in outcomes),'qualification_required')
        body=body_for(route,assignment)
        expected=ins.digest({k:v for k,v in body.items() if k!='messages'})
        for a,r in zip(aa[:6],outcomes):
            ip=RESULTS/route/'init'/f'{a["id"]}.json';init=d.read(ip)
            require(r['init_sha256']==d.sha(ip),'qualification_init_drift')
            require(r['metrics']==ins.score(ins.validate_answer(r['answer']),a),'qualification_score_drift')
            require(r['served_model']==body['model'],'qualification_model_drift')
            require(init['effective_config_sha256']==expected,'qualified_configuration_drift')
    return m


def key_for(route):
    if route=='pool':
        obj=d.read(Path.home()/'.moltbot/secrets/pool-keys.json')
        return next(k['key'] for k in obj['keys'] if k.get('enabled') and k.get('label')=='default')
    return (Path.home()/'.moltbot/secrets/openrouter.key').read_text().strip()


def body_for(route,a):
    model='claude-sonnet-4-6' if route=='pool' else 'anthropic/claude-sonnet-4.6'
    b={'model':model,'max_tokens':128,'temperature':0}
    if route=='pool':
        b.update(system=ins.SYSTEM,messages=[{'role':'user','content':a['prompt']}],
                 output_config={'format':{'type':'json_schema','schema':ins.SCHEMA}})
    else:
        b.update(messages=[{'role':'system','content':ins.SYSTEM},{'role':'user','content':a['prompt']}],
                 reasoning={'enabled':False},response_format={'type':'json_schema','json_schema':{'name':'decision','strict':True,'schema':ins.SCHEMA}},
                 provider={'order':['Anthropic'],'allow_fallbacks':False,'require_parameters':True,'max_price':{'prompt':3,'completion':15}})
    return b


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise AdmissionError('provider_redirect_rejected')


def dispatch(route,a):
    """Unavoidable shared boundary. Caller cannot inject body, model, key or cap."""
    with d.locked(RESULTS/'request.lock'):
        m=admitted(route,a)
        out=RESULTS/route;name=a['id'];unique=route+'/'+name
        require(not (out/'terminal.json').exists(),'terminal_cohort')
        require(not (out/'init'/f'{name}.json').exists(),'duplicate_assignment')
        body=body_for(route,a);ins.validate_wire_schema(ins.SCHEMA);raw=ins.canonical(body)
        require(len(raw)<=16000,'request_byte_budget')
        config={k:v for k,v in body.items() if k!='messages'}
        init={'study':SPEC_ID,'cohort':route,'assignment':name,'created':d.now(),
              'source_revision':m['source_revision'],'admission_sha256':d.sha(RESULTS/'admission.json'),
              'assignment_sha256':ins.digest(a),'resolved_requested_model':body['model'],
              'effective_config_sha256':ins.digest(config),'request_sha256':hashlib.sha256(raw).hexdigest(),
              'context_sha256':a['context_hash'],'request_body':body,'proxy_input_tokens':a['proxy_input_tokens'],
              'memory':{'reset':True,'namespace':unique,'inherited_context':False,'tools':[]},
              'served_model':None,'served_model_status':'not_observed_until_response'}
        d.immutable(out/'init'/f'{name}.json',init)
        row={'study':SPEC_ID,'cohort':route,'id':name,'stage':a['stage'],'arm':a['arm'],'copies':a['copies'],
             'root':a['world']['root'],'started':d.now(),'status':'failed','network_attempted':False,
             'init_sha256':d.sha(out/'init'/f'{name}.json'),'served_model':None,'paid_usd':0,'cost_unknown':False}
        t0=time.monotonic()
        try:
            with d.locked(RESULTS/'calls.jsonl') as h:
                h.seek(0);events=[json.loads(x) for x in h if x.strip()]
                require(len(events)<149,'http_attempt_cap')
                require(unique not in {e['call'] for e in events},'duplicate_http_reservation')
                d.append_locked(h,{'call':unique,'created':d.now(),'init_sha256':row['init_sha256']})
            if route=='openrouter':
                # byte-based conservative upper input bound, doubled input price
                # for possible caching differences, full possible output charge.
                reservation=((len(raw)+2048)*6+128*15)/1e6
                PAID.reserve(SPEC_ID,unique,reservation)
                row.update(paid_usd=reservation,cost_unknown=True,reserved_paid_usd=reservation)
            require(time.time()<DEADLINE,'deadline_before_network')
            key=key_for(route)
            if route=='pool':
                url='http://127.0.0.1:18811/v1/messages'
                headers={'x-api-key':key,'anthropic-version':'2023-06-01','Content-Type':'application/json'}
            else:
                url='https://openrouter.ai/api/v1/chat/completions'
                headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'}
            request=urllib.request.Request(url,data=raw,headers=headers)
            timeout=min(90,DEADLINE-time.time());require(timeout>0,'deadline_before_network')
            row['network_attempted']=True
            with urllib.request.build_opener(NoRedirect()).open(request,timeout=timeout) as response:
                data=json.loads(response.read(200000))
            # Retain only response fields, never request headers or exceptions.
            response_fields=('id','model','usage','stop_reason','content','provider','choices')
            row.update(response={k:data[k] for k in response_fields if k in data},
                       served_model=data.get('model'),usage=data.get('usage',{}))
            if route=='openrouter':
                cost=row['usage'].get('cost')
                if type(cost) in (int,float) and math.isfinite(cost) and cost>=0:
                    row.update(paid_usd=cost,cost_unknown=False)
                    PAID.settle(SPEC_ID,unique,cost)
                else:raise AdmissionError('missing_actual_cost')
            require(data.get('model')==body['model'],'served_model_mismatch')
            require(isinstance(data.get('usage'),dict),'missing_usage')
            if route=='pool':
                require(data.get('stop_reason')=='end_turn','truncated_response')
                texts=[x['text'] for x in data.get('content',[]) if x.get('type')=='text']
                require(len(texts)==1,'response_blocks');text=texts[0]
            else:
                require(data.get('provider')=='Anthropic','provider_mismatch')
                require(len(data.get('choices',[]))==1,'response_choices')
                require(data['choices'][0]['finish_reason']=='stop','truncated_response')
                text=data['choices'][0]['message']['content']
            answer=ins.validate_answer(json.loads(text));row.update(answer=answer,metrics=ins.score(answer,a),status='completed')
        except urllib.error.HTTPError as e:
            row['error']='http_'+str(e.code)
            row['error_class']='request_contract' if e.code==400 else 'availability' if e.code in (429,502,503,504) else 'provider_refusal'
            # Store bounded provider numeric/code diagnostics, not headers or text.
            try:
                error=json.loads(e.read(8192)).get('error',{})
                if isinstance(error,dict):
                    code=error.get('code',error.get('type'))
                    if type(code) is int or (isinstance(code,str) and len(code)<=80 and all(c.isalnum() or c in '_-' for c in code)):
                        row['provider_error_code']=code
            except Exception:pass
        except Exception as e:
            row['error']=type(e).__name__+(':'+str(e) if isinstance(e,(AdmissionError,d.BudgetStop)) else '')
        row.update(ended=d.now(),elapsed_seconds=round(time.monotonic()-t0,6))
        d.immutable(out/'outcomes'/f'{name}.json',row)
        return row


def close_cohort(route,reason):
    """Close every assignment before terminal summary or publication."""
    out=RESULTS/route
    if (out/'terminal.json').exists():return d.read(out/'terminal.json')
    aa=d.read(RESULTS/'assignments.json')[route]
    for a in aa:
        path=out/'outcomes'/f'{a["id"]}.json'
        if path.exists():continue
        init=out/'init'/f'{a["id"]}.json'
        row={'study':SPEC_ID,'cohort':route,'id':a['id'],'stage':a['stage'],'arm':a['arm'],
             'copies':a['copies'],'root':a['world']['root'],'status':'interrupted_unknown' if init.exists() else 'not_run',
             'reason':reason,'served_model':None,'ended':d.now(),'network_attempted':None if init.exists() else False}
        if init.exists():row['init_sha256']=d.sha(init)
        d.immutable(path,row)
    rows=[d.read(out/'outcomes'/f'{a["id"]}.json') for a in aa]
    terminal={'cohort':route,'reason':reason,'ended':d.now(),'assigned':len(aa),
        'completed':sum(r['status']=='completed' for r in rows),
        'failed':sum(r['status'] in ('failed','interrupted_unknown') for r in rows),
        'not_run':sum(r['status']=='not_run' for r in rows),
        'qualification_passed':all(r['status']=='completed' and r['metrics']['accuracy']==1 for r in rows[:6]),
        'outcome_sha256':{r['id']:d.sha(out/'outcomes'/f'{r["id"]}.json') for r in rows}}
    d.immutable(out/'terminal.json',terminal)
    return terminal


def execute_cohort(route):
    out=RESULTS/route
    if out.exists():
        # Existing unknown state is closed, never interpreted as restart permission.
        return close_cohort(route,'existing_cohort_closeout_only')
    reason='completed'
    try:
        for a in d.read(RESULTS/'assignments.json')[route]:
            if (RESULTS/'calls.jsonl').exists() and len((RESULTS/'calls.jsonl').read_text().splitlines())>=149:
                reason='remaining_cumulative_http_cap';break
            r=dispatch(route,a)
            print(json.dumps({'cohort':route,'id':a['id'],'status':r['status'],'error':r.get('error'),
                              'accuracy':r.get('metrics',{}).get('accuracy')}),flush=True)
            if r['status']!='completed':reason=r.get('error','failed');break
            if a['stage']=='Q' and r['metrics']['accuracy']!=1:reason='clean_competence_failure';break
    except Exception as e:reason=type(e).__name__
    return close_cohort(route,reason)


def run():
    with d.locked(RESULTS/'pilot.lock'):
        require((RESULTS/'admission.json').exists(),'no_admission')
        require(d.read(RESULTS/'admission.json')['source_sha256']==source_hashes(),'source_drift')
        execute_cohort('openrouter')


def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','run','closeout']);a=p.parse_args()
    if a.action=='prepare':prepare()
    elif a.action=='run':run()
    else:
        with d.locked(RESULTS/'pilot.lock'):
            for route in ('openrouter',):close_cohort(route,'operator_closeout_no_retry')

if __name__=='__main__':main()
