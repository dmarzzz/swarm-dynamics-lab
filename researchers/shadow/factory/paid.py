#!/usr/bin/env python3
"""Prospective paid-route amendment after all pool attempts returned HTTP429.
Original runner/specs remain unchanged. Explicit new -or specs, no fallback within a run.
"""
import fcntl
import json
import math
import os
from pathlib import Path
import subprocess
import threading
import time
import urllib.error
import urllib.request
import factory as f

class BudgetStop(RuntimeError): pass

class Ledger:
    """One process/thread-safe append-only reservation ledger for the entire factory.
    An unsettled/unknown call keeps its full conservative reservation forever.
    """
    def __init__(self,path):
        self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
        self.lock=threading.Lock()
    def event(self,kind,ident,call,usd=0,cap=4):
        with self.lock,self.path.open('a+') as h:
            fcntl.flock(h,fcntl.LOCK_EX); h.seek(0)
            es=[json.loads(l) for l in h if l.strip()]
            reserves={}; settled={}
            for e in es:
                key=(e['spec'],e['call'])
                if e['kind']=='reserve': reserves[key]=e['usd']
                else: settled[key]=e['usd']
            key=(ident,call)
            spent=sum(settled.get(k,v) for k,v in reserves.items())
            spec_spent=sum(settled.get(k,v) for k,v in reserves.items() if k[0]==ident)
            f.require(math.isfinite(usd) and usd>=0, 'validation failed')
            if kind=='reserve':
                if key in reserves: raise BudgetStop('duplicate_reservation')
                if spent+usd>20+1e-10 or spec_spent+usd>min(cap,4)+1e-10: raise BudgetStop('cap_reached')
            else:
                if key not in reserves or key in settled: raise BudgetStop('invalid_settlement')
            e=dict(kind=kind,spec=ident,call=call,usd=usd,time=f.now())
            h.seek(0,2); h.write(json.dumps(e,sort_keys=True)+'\n');h.flush();os.fsync(h.fileno())
            if kind=='settle' and usd>reserves[key]+1e-9: raise BudgetStop('reservation_breached')
            return e
    def accounted(self,ident):
        if not self.path.exists():return 0
        with self.lock,self.path.open() as h:
            fcntl.flock(h,fcntl.LOCK_SH)
            reserves={};settled={}
            for line in h:
                e=json.loads(line)
                if e['spec']!=ident:continue
                (reserves if e['kind']=='reserve' else settled)[e['call']]=e['usd']
            return sum(settled.get(k,v) for k,v in reserves.items())

LEDGER=Ledger(f.ROOT/'results'/'paid-ledger.jsonl')

def read_spec(name,frozen=True):
    p=f.ROOT/'specs'/(name if name.endswith('.json') else name+'.json')
    s=json.loads(p.read_text())
    f.require(s['route']=='openrouter' and s['model']=='anthropic/claude-sonnet-4.6', 'validation failed')
    f.require(s['max_paid_usd']==4 and s['max_calls']==204 and s['concurrency']==2, 'validation failed')
    if frozen:
        f.require(subprocess.check_output(['git','show','HEAD:'+str(p.relative_to(f.REPO))],cwd=f.REPO)==p.read_bytes(), 'uncommitted spec')
        for path,digest in s['source_sha256'].items(): f.require(f.sha(f.REPO/path)==digest, 'source drift '+path)
    return s

def key():
    return (Path.home()/'.moltbot/secrets/openrouter.key').read_text().strip()

def call(s,a,key):
    study,sim,provider=f.load_parent()
    system=provider.SYSTEM+'\nReturn exactly {"values":{"0":integer_or_null,"1":integer_or_null,"2":integer_or_null,"3":integer_or_null,"4":integer_or_null,"5":integer_or_null}}.'
    body=dict(model=s['model'],max_tokens=500,temperature=0,reasoning={'enabled':False},
        provider={'order':['Anthropic'],'allow_fallbacks':False,'require_parameters':True,'max_price':{'prompt':3,'completion':15}},
        messages=[{'role':'system','content':system},{'role':'user','content':json.dumps(a['packet'],sort_keys=True)}])
    raw=json.dumps(body).encode()
    row={k:v for k,v in a.items() if k!='packet'}
    row.update(started_at=f.now(),model=s['model'],route=s['route'],status='failed',paid_usd=0,
        request_hash=__import__('hashlib').sha256(json.dumps(body,sort_keys=True).encode()).hexdigest())
    # Every request byte treated as one token, plus 2048 envelope tokens; reserve
    # at twice the published input rate to cover cache-write variation. All 500
    # possible output tokens reserved. Tools, search and automatic caching off.
    reservation=((len(raw)+2048)*6+500*15)/1e6
    t0=time.monotonic()
    try:
        if time.time()>=f.DEADLINE: raise BudgetStop('deadline')
        LEDGER.event('reserve',s['id'],a['id'],reservation,s['max_paid_usd'])
        row['reserved_paid_usd']=reservation
        req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=raw,
            headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','X-Title':'swarm-lab Shadow factory'})
        with urllib.request.urlopen(req,timeout=90) as resp: data=json.loads(resp.read(200000))
        usage=data.get('usage') or {}
        cost=usage.get('cost')
        if isinstance(cost,(int,float)) and math.isfinite(cost) and cost>=0:
            LEDGER.event('settle',s['id'],a['id'],cost,s['max_paid_usd'])
            row['paid_usd']=cost
        else: row['paid_usd']=reservation; row['cost_unknown']=True
        row.update(returned_model=data.get('model'),provider=data.get('provider'),response_id=data.get('id'),
                   usage={'input_tokens':usage.get('prompt_tokens',0),'output_tokens':usage.get('completion_tokens',0),'cost':cost},raw_usage=usage)
        ch=data['choices'][0];row['stop_reason']=ch.get('finish_reason');row['raw_text']=ch['message'].get('content') or ''
        f.require(data.get('model')==s['model'], 'model_mismatch')
        f.require(data.get('provider')=='Anthropic', 'provider_mismatch')
        f.require(ch.get('finish_reason')=='stop', 'stop_reason')
        f.require(usage.get('prompt_tokens') is not None and usage.get('completion_tokens') is not None, 'missing_usage')
        f.require(not (usage.get('completion_tokens_details') or {}).get('reasoning_tokens',0), 'unexpected_reasoning')
        ans=f.parse_answer(row['raw_text']);row['answer']=ans
        row['metrics']=sim.grade(ans['values'],a['answers'],a['fabricated'])
        if a['stage']=='Q':row['exact']=ans['values']==a['expected']
        row['status']='completed'
    except urllib.error.HTTPError as e:
        row['error']='http_'+str(e.code)
        # Provider-rejected errors retain full reservation; no free-call assumption.
        row['paid_usd']=row.get('reserved_paid_usd',0);row['cost_unknown']=True
    except Exception as e:
        row['error']=type(e).__name__+(':'+str(e) if isinstance(e,(AssertionError,BudgetStop)) else '')
        if row.get('reserved_paid_usd') and not row.get('usage'):
            row['paid_usd']=row['reserved_paid_usd'];row['cost_unknown']=True
    row.update(ended_at=f.now(),elapsed_seconds=round(time.monotonic()-t0,3))
    return row

BASE_ANALYZE=f.analyze

def analyze(s,aa,rows,out):
    summary=BASE_ANALYZE(s,aa,rows,out)
    summary['paid_usd']=LEDGER.accounted(s['id'])
    summary['cost_unknown_calls']=sum(bool(r.get('cost_unknown')) for r in rows)
    f.dump(out/'summary.json',summary)
    p=out/'FINDING.md';text=p.read_text()
    text=text.replace('local Anthropic pool, no paid fallback','OpenRouter, Anthropic-only provider, reasoning disabled; separately preregistered paid attempt')
    text=text.replace('External paid spend $0;',f"External paid spend/accounted reservations ${summary['paid_usd']:.6f} ({summary['cost_unknown_calls']} unknown-cost calls conservatively reserved);")
    text += '\n## Attempt lineage\n\nThe original pool attempt returned four HTTP429 errors at qualification and made no comparison calls. It remains in its own result directory. This dated, separately preregistered OpenRouter attempt uses a different route and repeats the entire fixed screen. No parent attempt outcomes are selected into this cohort. See [paid-route amendment](../../AMENDMENT-PAID.md).\n'
    p.write_text(text)
    return summary

def main():
    f.read_spec=read_spec;f.call=call;f.pool_key=key;f.analyze=analyze
    # Separate queue: never reinterpret a completed pool spec as a paid run.
    import argparse
    p=argparse.ArgumentParser();p.add_argument('command',choices=['queue','run','analyze']);p.add_argument('--spec');p.add_argument('--watch',action='store_true');args=p.parse_args()
    if args.command=='queue':
        while time.time()<f.DEADLINE:
            for name in json.loads((f.ROOT/'queue-paid.json').read_text())['specs']:
                if time.time()>=f.DEADLINE:return
                if not (f.ROOT/'results'/name/'terminal.json').exists():f.run(read_spec(name))
            if not args.watch:return
            time.sleep(min(60,max(0,f.DEADLINE-time.time())))
    elif args.command=='run':f.run(read_spec(args.spec))
    else:
        s=read_spec(args.spec);out=f.ROOT/'results'/s['id'];rows=[json.loads(l) for l in (out/'records.jsonl').read_text().splitlines()]
        print(json.dumps(analyze(s,f.assignments(s),rows,out),indent=2))
if __name__=='__main__':main()
