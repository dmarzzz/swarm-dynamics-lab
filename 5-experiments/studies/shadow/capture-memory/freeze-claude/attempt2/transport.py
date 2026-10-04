#!/usr/bin/env python3
"""Attempt2 OpenRouter transport. Scientific functions imported without edits."""
import concurrent.futures as cf
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import threading
import time
import urllib.error
import urllib.request

OUT=Path(__file__).resolve().parent
BASE=OUT.parent
sys.path.insert(0,str(BASE))
import run as frozen
MODELS={'sonnet':'anthropic/claude-sonnet-5.5','opus':'anthropic/claude-opus-5.5'}
DEADLINE=datetime(2026,10,4,23,30,tzinfo=timezone.utc).timestamp()
CAP=Decimal('10')
RESERVE=Decimal('0.25') # deliberately conservative exposure per <=20KB, <=32-token request

def lines(name):
    p=OUT/name
    return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []

def setup():
    manifest=json.loads((OUT/'source-hashes.json').read_text())
    for name,digest in manifest.items():
        assert frozen.sha(BASE/name)==digest, ('frozen source mismatch',name)
    frozen.ROOT=OUT
    frozen.DEADLINE=DEADLINE
    return json.loads((BASE/'inputs.json').read_text())

class Router:
    def __init__(self,key=None):
        self.key=key if key is not None else Path('/home/shad0w/.moltbot/secrets/openrouter.key').read_text().strip()
        self.lock=threading.Lock()
        self.count=len(lines('requests.jsonl'))
        self.qcount=sum(r['meta']['stage']=='qualification' for r in lines('requests.jsonl'))
        self.cost=sum((Decimal(str(r['response']['usage']['cost'])) for r in lines('responses.jsonl')
                       if isinstance(r.get('response'),dict) and r['response'].get('usage',{}).get('cost') is not None),Decimal('0'))
        self.reserved=Decimal('0')
        self.unknown=Decimal('0')
        self.cooldown=0
        self.errors=0
        self.halted=False
        # A process restart after any ambiguous dispatch is not an automatic retry.
        if self.count: raise frozen.Stop('attempt already started; no automatic restart')
    def append(self,name,obj):
        with (OUT/name).open('a') as f:
            f.write(json.dumps(obj,sort_keys=True)+'\n'); f.flush(); os.fsync(f.fileno())
    def ledger(self):
        frozen.save('budget.json',dict(cost_usd=str(self.cost),reserved_usd=str(self.reserved),
            unresolved_exposure_usd=str(self.unknown),cap_usd=str(CAP),requests=self.count,
            prior_attempt_requests=8,qualification_attempts=self.qcount,halted=self.halted,time=frozen.now()))
    def call(self,model,words,history,meta):
        payload=dict(model=MODELS[model],max_tokens=32,
            messages=[dict(role='system',content=frozen.SYSTEM),dict(role='user',content=frozen.user_prompt(words,history))],
            provider={'allow_fallbacks':False},usage={'include':True})
        data=json.dumps(payload).encode()
        if len(data)>20000: raise frozen.Stop('outside conservative request exposure envelope')
        for attempt in range(2):
            while True:
                with self.lock:
                    if self.halted: raise frozen.Stop('route halted')
                    delay=self.cooldown-time.time()
                if delay<=0: break
                time.sleep(min(delay,1))
            with self.lock:
                if self.halted: raise frozen.Stop('route halted')
                if time.time()>=DEADLINE: raise frozen.Stop('23:30Z dispatch deadline')
                if self.count+8>=1500: raise frozen.Stop('1500 lineage attempt cap')
                if meta['stage']=='qualification' and self.qcount>=12:
                    self.halted=True; raise frozen.Stop('12 qualification attempt cap')
                if self.cost+self.reserved+self.unknown+RESERVE>CAP:
                    self.halted=True; raise frozen.Stop('dollar exposure cap')
                self.reserved+=RESERVE
                self.count+=1; reqid=self.count
                if meta['stage']=='qualification': self.qcount+=1
                self.append('requests.jsonl',dict(request_id=reqid,started=frozen.now(),attempt=attempt,meta=meta,payload=payload))
                self.ledger()
            req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=data,
                    headers={'Content-Type':'application/json','Authorization':'Bearer '+self.key})
            status=0; response=None; error=None; retry_after=30
            started=time.monotonic()
            try:
                with urllib.request.urlopen(req,timeout=120) as res:
                    status=res.status
                    response=json.loads(res.read().decode().replace(self.key,'[REDACTED]'))
            except urllib.error.HTTPError as e:
                status=e.code; raw=e.read().decode(errors='replace').replace(self.key,'[REDACTED]')
                try: response=json.loads(raw)
                except Exception: response={'raw_error':raw}
                try: retry_after=max(30,float(e.headers.get('Retry-After','30')))
                except ValueError: pass
            except Exception as e: error=type(e).__name__
            text=''
            if status==200 and response:
                choices=response.get('choices',[])
                if choices: text=choices[0].get('message',{}).get('content') or ''
            cleaned=text.strip().strip(' .\n\t\"\'`*').lower()
            choice=next((int(k) for k,v in words.items() if cleaned==v.lower()),None)
            receipt=(response or {}).get('usage',{}).get('cost')
            served=(response or {}).get('model')
            fatal=None
            with self.lock:
                self.reserved-=RESERVE
                if receipt is not None:
                    amount=Decimal(str(receipt))
                    if not amount.is_finite() or amount<0:
                        fatal='invalid cost receipt'; self.unknown+=RESERVE
                    else:
                        self.cost+=amount
                        if amount>RESERVE: fatal='cost exceeds conservative reservation'
                elif status==200:
                    self.unknown+=RESERVE; fatal='missing actual cost receipt'
                else:
                    # Do not invent zero charges for unreceipted errors.
                    self.unknown+=RESERVE
                if status==200 and served!=MODELS[model]: fatal='unexpected returned model ID'
                if status in (400,401,402,403,404): fatal='route unavailable or authorization failure'
                if status==429 or status>=500:
                    self.errors+=1
                    self.cooldown=max(self.cooldown,time.time()+retry_after)
                    if self.errors>=3: fatal='repeated throttling/server errors'
                if status==0: fatal='ambiguous transport failure; no retry'
                if self.cost+self.unknown>=CAP: fatal='dollar cap'
                if fatal: self.halted=True
                self.append('responses.jsonl',dict(request_id=reqid,finished=frozen.now(),elapsed_s=time.monotonic()-started,
                    status=status,response=response,error=error,text=text,choice=choice,meta=meta,
                    returned_model=served,provider=(response or {}).get('provider'),transport_stop=fatal))
                self.ledger()
            if fatal: raise frozen.Stop(fatal)
            if status==200:
                if choice is None: raise frozen.Stop('unparseable response')
                return dict(choice=choice,request_id=reqid)
            if attempt==0 and (status==429 or status>=500): continue
            raise frozen.Stop(f'transport status={status} error={error}')
        raise frozen.Stop('retry exhausted')

def main():
    plan=setup()
    pool=Router()
    if not frozen.qualify(pool,plan):
        frozen.save('STOP.json',dict(reason='qualification gate failed or unavailable',time=frozen.now(),requests=pool.count))
        return
    frozen.save('S1-ADMISSION.json',dict(status='qualified diagnostic only',time=frozen.now(),
        source_hashes=json.loads((OUT/'source-hashes.json').read_text()),budget=json.loads((OUT/'budget.json').read_text()),
        scope='Frozen 16 Sonnet repair, then4 attack, optional2 Opus. Same scientific functions and plan.'))
    for stage in ['repair','attack','opus']:
        assignments=[a for a in plan['assignments'] if a['stage']==stage]
        for a in assignments:
            if time.time()>=DEADLINE or pool.halted or pool.count+8>=1500:
                frozen.save('STOP.json',dict(reason='deadline/cap/route stop',time=frozen.now(),requests=pool.count)); return
            if stage=='opus' and (pool.count+8+sum(x['calls'] for x in assignments)>1500 or
                                 time.time()+300>DEADLINE or pool.cost+Decimal('1')>CAP):
                frozen.save('OPUS-SKIP.json',dict(reason='remaining time/budget/request envelope',time=frozen.now())); return
            frozen.episode(pool,plan,a)
    frozen.save('completion.json',dict(time=frozen.now(),requests=pool.count))

if __name__=='__main__': main()
