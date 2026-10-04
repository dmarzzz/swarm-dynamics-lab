#!/usr/bin/env python3
"""Native structured-output pool attempt; bounded 429 backoff, no paid fallback.
Does not alter or retry any earlier cohort's answers. Each new assignment has at
most three transport attempts; a 429 is saved before waiting, respecting Retry-After.
"""
import argparse
import hashlib
import json
import math
import os
import subprocess
import time
import urllib.error
import urllib.request
import factory as f
import structured as shaped

BASE_ANALYZE=f.analyze

def read_spec(name,frozen=True):
    p=f.ROOT/'specs'/(name if name.endswith('.json') else name+'.json')
    s=json.loads(p.read_text())
    assert s['route']=='anthropic-pool' and s['model']=='claude-sonnet-4-6'
    assert s['max_paid_usd']==0 and s['max_calls']==204 and s['concurrency']==2
    if frozen:
        assert subprocess.check_output(['git','show','HEAD:'+str(p.relative_to(f.REPO))],cwd=f.REPO)==p.read_bytes()
        for path,digest in s['source_sha256'].items():assert f.sha(f.REPO/path)==digest,'source drift '+path
    return s

def assignments(s):
    # Complete a paired root before starting the next one. Randomized root order,
    # then original shuffled within-root order; minimizes wasted incomplete pairs.
    aa=shaped.assignments(s);groups={}
    for a in aa:
        if a['stage']=='M':groups.setdefault((a['family'],a['task']),[]).append(a)
    keys=sorted(groups);__import__('random').Random(s['dispatch_seed']).shuffle(keys)
    return [a for a in aa if a['stage']=='Q']+[a for k in keys for a in groups[k]]

def call(s,a,key):
    f.enforce_launch_hold()
    study,sim,provider=f.load_parent()
    system=provider.SYSTEM+'\nReturn exactly {"values":{"0":integer_or_null,"1":integer_or_null,"2":integer_or_null,"3":integer_or_null,"4":integer_or_null,"5":integer_or_null}}.'
    body=dict(model=s['model'],max_tokens=500,temperature=0,system=system,
              output_config={'format':{'type':'json_schema','schema':provider.SCHEMA}},
              messages=[{'role':'user','content':json.dumps(a['packet'],sort_keys=True)}])
    row={k:v for k,v in a.items() if k!='packet'}
    row.update(started_at=f.now(),model=s['model'],route=s['route'],status='failed',paid_usd=0,
               request_hash=hashlib.sha256(json.dumps(body,sort_keys=True).encode()).hexdigest(),transport_attempts=[])
    t0=time.monotonic();data=None
    req=urllib.request.Request('http://127.0.0.1:18811/v1/messages',data=json.dumps(body).encode(),
         headers={'x-api-key':key,'anthropic-version':'2023-06-01','content-type':'application/json'})
    for attempt in range(3):
        if time.time()>=f.DEADLINE:row['error']='deadline';break
        event=dict(id=a['id'],attempt=attempt+1,time=f.now())
        try:
            with urllib.request.urlopen(req,timeout=90) as response:data=json.loads(response.read(200000))
            event['status']=200
        except urllib.error.HTTPError as e:
            event['status']=e.code;row['error']='http_'+str(e.code)
            value=e.headers.get('Retry-After','0') if e.headers else '0'
            try:retry=float(value)
            except ValueError:retry=0
            event['wait_seconds']=max(120*(attempt+1),retry if math.isfinite(retry) else 0)
        except Exception as e:
            event['status']=type(e).__name__;row['error']=type(e).__name__
        # Distinct files per assignment avoid concurrent append on one stream.
        trace=f.ROOT/'results'/s['id']/'transport'/f"{a['id']}.jsonl";trace.parent.mkdir(exist_ok=True)
        f.append(trace,event);row['transport_attempts'].append(event)
        if data is not None:break
        if event['status']!=429 or attempt==2:break
        wait=event['wait_seconds']
        if time.time()+wait>=f.DEADLINE:break
        time.sleep(wait)
    if data is not None:
        try:
            row.update(returned_model=data.get('model'),usage=data.get('usage'),stop_reason=data.get('stop_reason'),response_id=data.get('id'))
            texts=[b['text'] for b in data.get('content',[]) if b.get('type')=='text'];row['raw_text']='\n'.join(texts)
            assert data.get('model')==s['model'],'model_mismatch'
            assert isinstance(data.get('usage'),dict),'missing_usage'
            assert data.get('stop_reason')=='end_turn','stop_reason'
            assert len(texts)==1,'text_blocks'
            ans=f.parse_answer(texts[0]);row['answer']=ans
            row['metrics']=sim.grade(ans['values'],a['answers'],a['fabricated'])
            if a['stage']=='Q':row['exact']=ans['values']==a['expected']
            row['status']='completed';row.pop('error',None)
        except Exception as e:row['error']=type(e).__name__+(':'+str(e) if isinstance(e,AssertionError) else '')
    row.update(ended_at=f.now(),elapsed_seconds=round(time.monotonic()-t0,3))
    return row

def analyze(s,aa,rows,out):
    summary=BASE_ANALYZE(s,aa,rows,out)
    summary['transport_attempts']=sum(len(r.get('transport_attempts',[])) for r in rows)
    f.dump(out/'summary.json',summary)
    p=out/'FINDING.md';text=p.read_text().replace('No retries or outcome replacements.','Only HTTP429 transport refusals retried (maximum three attempts per assignment, all persisted); no answer retries or outcome replacements.')
    text=text.replace('an explicit JSON instruction instead of Opus effort-low schema-constrained output','native schema-constrained output instead of Opus effort-low schema-constrained output')
    text+='\n## Attempt lineage\n\nThis separate native-schema pool cohort follows failed pool transport, failed unstructured OpenRouter answers, and an OpenRouter quota interruption. No earlier answers are pooled or selected into this run. Fresh qualification roots are 5141 and 5146. See [native pool amendment](../../AMENDMENT-NATIVE.md).\n'
    p.write_text(text);return summary

def main():
    f.call=call;f.assignments=assignments;f.analyze=analyze
    p=argparse.ArgumentParser();p.add_argument('command',choices=['queue','analyze']);p.add_argument('--spec');args=p.parse_args()
    if args.command=='analyze':
        s=read_spec(args.spec);out=f.ROOT/'results'/s['id'];rows=[json.loads(l) for l in (out/'records.jsonl').read_text().splitlines()]
        print(json.dumps(analyze(s,f.assignments(s),rows,out),indent=2));return
    for name in json.loads((f.ROOT/'queue-native.json').read_text())['specs']:
        if time.time()>=f.DEADLINE:return
        if (f.ROOT/'results'/name/'terminal.json').exists():continue
        result=f.run(read_spec(name))
        if not result['qualification_passed']:
            print('Native queue stopped at qualification; no other provider/credential selected',flush=True);return
if __name__=='__main__':main()
