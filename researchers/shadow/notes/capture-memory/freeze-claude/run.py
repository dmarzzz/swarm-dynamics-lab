#!/usr/bin/env python3
"""Frozen Claude-pool instrument. prepare is offline; run requires explicit stage."""
from __future__ import annotations
import concurrent.futures as cf
import copy
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import random
import sys
import threading
import time
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'src'))
import sim
SYSTEM = ('You are one agent in a group agreeing on a name. Choose a name to coordinate with a randomly '
          'encountered group member. There is no objectively correct name. You will see only the names '
          'your previous partners used. Reply with exactly one of the two allowed names and nothing else.')
MODELS = {'sonnet': 'claude-sonnet-5-5', 'opus': 'claude-opus-5-5'}
CFG = dict(n_agents=12, beta=2.5, h_inside=0.1, h_outside=0.5, entrench_rounds=20,
           takeover_max_rounds=400, clean_takeover_rounds=20, capture_frac=0.75,
           capture_streak=3, recovery_rounds=20, eval_round=20, recover_frac=0.75, recover_streak=10)
ARMS = [('full','removal'), ('1','removal'), ('full','wipe'), ('1','wipe')]
DEADLINE = datetime(2026,10,4,22,45,tzinfo=timezone.utc).timestamp()

def now():
    return datetime.now(timezone.utc).isoformat()

def save(path, x):
    (ROOT/path).write_text(json.dumps(x, indent=2, sort_keys=True)+'\n')

def jread(path):
    return json.loads((ROOT/path).read_text())

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def user_prompt(words, history):
    allowed = sorted(words.values())
    return (f'Allowed names: {allowed[0]}, {allowed[1]}.\n'
            f'Partner names, oldest first: {", ".join(words[str(x)] for x in history) or "(none)"}.\n'
            'Which name do you use now?')

def serialize(agents):
    return {str(i): {'word':a.word,'mem': list(a.mem) if not a.committed else [],
                    'committed':a.committed} for i,a in agents.items()}

def frac(agents):
    honest = [a for a in agents.values() if not a['committed']]
    return sum(a['word']==1 for a in honest)/len(honest)

def repair_agents(root, memory, arm):
    agents = {i:copy.deepcopy(a) for i,a in root['agents'].items() if not a['committed']}
    for a in agents.values():
        if memory == '1': a['mem'] = a['mem'][-1:]
        if arm == 'wipe': a['mem'] = []
    return agents

def heard_at(agents, pairs):
    heard = {}
    for a,b in pairs:
        a,b = str(a),str(b)
        if a in agents and b in agents:
            if not agents[a]['committed']: heard[a] = agents[b]['word']
            if not agents[b]['committed']: heard[b] = agents[a]['word']
    return heard

def qualification():
    # Six conflict histories and two unanimous controls for Sonnet; Opus has two of each.
    histories = [[1]*8,[-1]*8,[1]*7+[-1],[-1]*7+[1],
                 [1,1,1,-1,1,1,1,-1],[-1,-1,-1,1,-1,-1,-1,1],
                 [1]*15+[-1],[-1]*15+[1]]
    out=[]
    words={'1':'cedar','-1':'raven'}
    for model, ids in [('sonnet', range(8)),('opus',[0,1,2,3])]:
        for i in ids:
            h=histories[i]
            out.append(dict(id=f'q-{model}-{i}',model=model,words=words,history=h,
                            unanimous=len(set(h))==1,
                            tanh_p_original=(math.tanh(2.5*(sum(h)/len(h)+0.1))+1)/2))
    return out

def prepare():
    if (ROOT/'requests.jsonl').exists():
        raise SystemExit('prepare refuses after any requests')
    roots=[]
    for task_id in range(160,164):
        t=sim.task(task_id)
        pre=sim.simulate_prefix(t,1,'W1_INSIDE',0.54,'full',CFG,sim.scripted_policy,{'task':t})
        schedules=[sim.round_draws(task_id,1,pre['rnd']+r,12)[0] for r in range(20)]
        roots.append(dict(task_id=task_id, seed=1,words={str(k):v for k,v in t['words'].items()},
                          agents=serialize(pre['agents']), captured=pre['capture_round'] is not None,
                          capture_round=pre['capture_round'],removal_round=pre['rnd'],
                          prefix_series=pre['series'],baseline=sim.frac_original(pre['agents']),
                          schedules=schedules))
    assignments=[]
    for ri,root in enumerate(roots):
        arms=ARMS[ri:]+ARMS[:ri]
        for memory,arm in arms:
            a=repair_agents(root,memory,arm)
            decisions=sum(len(heard_at(a,p)) for p in root['schedules'])
            assignments.append(dict(id=f'repair-sonnet-{root["task_id"]}-{memory}-{arm}',
                                    stage='repair',model='sonnet',task_id=root['task_id'],
                                    memory=memory,arm=arm,rounds=20,calls=decisions))
    attacks=[]
    for task_id in [170,171]:
        t=sim.task(task_id)
        for memory,dose in [('1',0.42),('full',0.54)]:
            removed=sim.replaced(task_id,1,12,round(12*dose))
            a={str(i):dict(word=(-1 if i in removed else 1),committed=i in removed,
                          mem=[] if i in removed else ([1] if memory=='1' else [1]*21)) for i in range(12)}
            schedules=[sim.round_draws(task_id,1,20+r,12)[0] for r in range(8)]
            attacks.append(dict(task_id=task_id,memory=memory,dose=dose,words={str(k):v for k,v in t['words'].items()},
                                agents=a,schedules=schedules))
            assignments.append(dict(id=f'attack-sonnet-{task_id}-{memory}',stage='attack',model='sonnet',
                                    task_id=task_id,memory=memory,arm='attack',rounds=8,
                                    calls=8*(12-round(dose*12))))
    optional=[]
    for root in roots[:2]:
        a=repair_agents(root,'full','removal')
        optional.append(dict(id=f'repair-opus-{root["task_id"]}-full-removal',stage='opus',model='opus',
                             task_id=root['task_id'],memory='full',arm='removal',rounds=20,
                             calls=sum(len(heard_at(a,p)) for p in root['schedules'])))
    nominal=12+sum(a['calls'] for a in assignments+optional)
    if nominal<=1450:
        assignments+=optional
    else:
        nominal=12+sum(a['calls'] for a in assignments)
    assert nominal<=1450, ('allocation amendment needed',nominal)
    plan=dict(version=1,created=now(),config=CFG,roots=roots,attacks=attacks,qualification=qualification(),
              assignments=assignments,nominal_calls=nominal,hard_cap=1500,
              source_hashes={p.name:sha(p) for p in [ROOT/'run.py',ROOT/'PREREG.md',ROOT.parent/'src/sim.py']})
    save('inputs.json',plan)
    scripted=[]
    for a in assignments:
        if a['stage']!='repair': continue
        root=next(x for x in roots if x['task_id']==a['task_id'])
        agents=repair_agents(root,a['memory'],a['arm'])
        trace=[frac(agents)]
        switches=[]
        for r,pairs in enumerate(root['schedules']):
            heard=heard_at(agents,pairs)
            draws=sim.round_draws(root['task_id'],1,root['removal_round']+r,12)[1]
            changes=0
            for i,w in heard.items():
                ag=agents[i]; ag['mem'].append(w)
                if a['memory']=='1': ag['mem']=ag['mem'][-1:]
                m=sum(ag['mem'])/len(ag['mem'])
                new=sim.scripted_policy(m,CFG,draws[int(i)],{'h':0.1})
                changes+=int(new!=ag['word']); ag['word']=new
            trace.append(frac(agents)); switches.append(dict(switched=changes,decisions=len(heard)))
        scripted.append(dict(assignment=a,trace=trace,switches=switches,delta=trace[-1]-trace[0]))
    save('scripted-reference.json',scripted)
    print(json.dumps(dict(nominal_calls=nominal,assignments=len(assignments),
                         roots=[{k:r[k] for k in ['task_id','baseline','captured','removal_round']} for r in roots]),indent=2))

class Stop(Exception): pass

class Pool:
    def __init__(self):
        # Brief named ocplatform.json, absent on this host. Same authorized provider in actual config.
        cfg=json.loads(Path('/home/shad0w/.openclaw/openclaw.json').read_text())
        self.key=cfg['models']['providers']['anthropic-proxy']['apiKey']
        self.lock=threading.Lock()
        self.count=sum(1 for _ in (ROOT/'requests.jsonl').open()) if (ROOT/'requests.jsonl').exists() else 0
        self.cooldown=0
        self.throttles=0
        self.halted=False
    def append(self,file,obj):
        # Caller holds lock. Flush and fsync every durable record.
        import os
        with (ROOT/file).open('a') as f:
            f.write(json.dumps(obj,sort_keys=True)+'\n'); f.flush(); os.fsync(f.fileno())
    def call(self, model, words, history, meta):
        payload=dict(model=MODELS[model],max_tokens=32,system=SYSTEM,
                     messages=[dict(role='user',content=user_prompt(words,history))])
        data=json.dumps(payload).encode()
        for attempt in range(2):
            while True:
                with self.lock:
                    delay=self.cooldown-time.time()
                    if self.halted: raise Stop('pool stopped after repeated error')
                if delay<=0: break
                time.sleep(min(delay,5))
            with self.lock:
                if time.time()>=DEADLINE: raise Stop('18:45 EDT deadline')
                if self.count>=1500: raise Stop('request cap')
                self.count+=1
                reqid=self.count
                self.append('requests.jsonl',dict(request_id=reqid,started=now(),attempt=attempt,
                                               meta=meta,payload=payload))
            request=urllib.request.Request('http://127.0.0.1:18811/v1/messages',data=data,
                        headers={'Content-Type':'application/json','x-api-key':self.key,
                                 'anthropic-version':'2023-06-01'})
            status=0; response=None; error=None; retry_after=30
            started=time.monotonic()
            try:
                with urllib.request.urlopen(request,timeout=120) as res:
                    status=res.status
                    response=json.loads(res.read())
            except urllib.error.HTTPError as e:
                status=e.code
                raw=e.read().decode(errors='replace')
                # Never record request headers; sanitize against accidental credential echoes.
                raw=raw.replace(self.key,'[REDACTED]')
                try: response=json.loads(raw)
                except Exception: response={'raw_error':raw}
                try: retry_after=max(30,float(e.headers.get('Retry-After','30')))
                except ValueError: retry_after=30
            except Exception as e:
                error=type(e).__name__
            text=''
            if status==200 and response:
                text=''.join(x.get('text','') for x in response.get('content',[]) if x.get('type')=='text')
            cleaned=text.strip().strip(' .\n\t\"\'`*').lower()
            choice=next((int(k) for k,v in words.items() if cleaned==v.lower()),None)
            record=dict(request_id=reqid,finished=now(),elapsed_s=time.monotonic()-started,status=status,
                        response=response,error=error,text=text,choice=choice,meta=meta)
            with self.lock:
                self.append('responses.jsonl',record)
                if status in (429,529):
                    self.throttles+=1
                    if self.throttles>=3: self.halted=True
                if status in (401,403) or status==400: self.halted=True
                if status==429 or status>=500:
                    self.cooldown=max(self.cooldown,time.time()+retry_after)
            if status==200:
                if choice is None: raise Stop('unparseable response')
                return dict(choice=choice,request_id=reqid)
            if attempt==0 and (status==429 or status>=500): continue
            raise Stop(f'transport status={status} error={error}')
        raise Stop('retry exhausted')

def qualify(pool,plan):
    path=ROOT/'qualification.json'
    if path.exists(): return json.loads(path.read_text())['passed']
    results=[]
    # Sequential qualification avoids wasting calls if route is structurally broken.
    for q in plan['qualification']:
        try:
            r=pool.call(q['model'],q['words'],q['history'],dict(stage='qualification',id=q['id']))
            results.append(dict(**q,**r,valid=True))
        except Stop as e:
            results.append(dict(**q,valid=False,error=str(e)))
            if pool.halted: break
    sonnet=[q for q in results if q['model']=='sonnet']
    valid=sum(q['valid'] for q in results)
    controls=[q for q in results if q['unanimous']]
    noncopy=[q for q in sonnet if q['valid'] and not q['unanimous'] and q['choice']!=q['history'][-1]]
    passed=(len(results)==12 and valid/12>=0.9 and all(q['valid'] and q['choice']==q['history'][0] for q in controls)
            and len(noncopy)>0)
    save('qualification.json',dict(passed=passed,valid=valid,assigned=12,noncopy_sonnet_conflicts=len(noncopy),results=results))
    print('qualification',passed,'valid',valid,'noncopy',len(noncopy),flush=True)
    return passed

def episode(pool,plan,a):
    destination=ROOT/'episodes'/f'{a["id"]}.json'
    if destination.exists():
        print('already terminal',a['id'],flush=True); return
    destination.parent.mkdir(exist_ok=True)
    if a['stage']=='attack':
        root=next(x for x in plan['attacks'] if x['task_id']==a['task_id'] and x['memory']==a['memory'])
        agents=copy.deepcopy(root['agents'])
    else:
        root=next(x for x in plan['roots'] if x['task_id']==a['task_id'])
        agents=repair_agents(root,a['memory'],a['arm'])
    result=dict(assignment=a,started=now(),trace=[frac(agents)],rounds=[],status='started')
    save(str(destination.relative_to(ROOT)),result)
    try:
        for rnd,pairs in enumerate(root['schedules'],1):
            heard=heard_at(agents,pairs)
            for i,w in heard.items():
                agents[i]['mem'].append(w)
                if a['memory']=='1': agents[i]['mem']=agents[i]['mem'][-1:]
            new={}; failures=[]
            with cf.ThreadPoolExecutor(max_workers=6) as ex:
                futures={i:ex.submit(pool.call,a['model'],root['words'],list(agents[i]['mem']),
                                    dict(stage=a['stage'],id=a['id'],round=rnd,agent=int(i))) for i in sorted(heard)}
                for i,fut in futures.items():
                    try: new[i]=fut.result()
                    except Stop as e: failures.append(str(e))
            rr=dict(round=rnd,pairs=pairs,heard=heard,decisions=new,
                    before={i:ag['word'] for i,ag in agents.items()})
            if failures:
                rr['errors']=failures; result['rounds'].append(rr)
                raise Stop('; '.join(failures))
            rr['switched']=sum(new[i]['choice']!=agents[i]['word'] for i in new)
            for i,r in new.items(): agents[i]['word']=r['choice']
            rr['after']={i:ag['word'] for i,ag in agents.items()}
            result['rounds'].append(rr); result['trace'].append(frac(agents))
            save(str(destination.relative_to(ROOT)),result)
        result['status']='complete'
    except Stop as e:
        result['status']='failed'; result['error']=str(e)
    result['finished']=now()
    result['final_agents']=agents
    save(str(destination.relative_to(ROOT)),result)
    print(a['id'],result['status'],'trace',result['trace'],'calls',pool.count,flush=True)

def run(stage):
    plan=jread('inputs.json')
    assert plan['source_hashes']['run.py']==sha(ROOT/'run.py'),'runner changed after prepare'
    pool=Pool()
    if not qualify(pool,plan):
        save('STOP.json',dict(reason='qualification failed',time=now(),requests=pool.count)); return
    if stage=='qualification': return
    stages=['repair','attack','opus'] if stage=='all' else [stage]
    for st in stages:
        assignments=[a for a in plan['assignments'] if a['stage']==st]
        if st=='opus' and pool.count+sum(a['calls'] for a in assignments)>1500:
            save('OPUS-SKIP.json',dict(reason='remaining cap insufficient',requests=pool.count)); continue
        for a in assignments:
            if time.time()>=DEADLINE or pool.halted or pool.count>=1500:
                save('STOP.json',dict(reason='deadline/cap/pool stop',time=now(),requests=pool.count)); return
            episode(pool,plan,a)
    save('completion.json',dict(time=now(),requests=pool.count,stage=stage))

if __name__=='__main__':
    if len(sys.argv)<2: raise SystemExit('prepare | qualification | repair | attack | opus | all')
    if sys.argv[1]=='prepare': prepare()
    else: run(sys.argv[1])
