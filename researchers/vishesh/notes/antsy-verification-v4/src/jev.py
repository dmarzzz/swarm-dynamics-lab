"""Pinned Jev adapter and finite probe/actor payload allowlist. No credential handling here."""
import hashlib,itertools,json,math,time,urllib.request
from pathlib import Path
from policies import MODES,ROLES,calibrate,initial,purchase,actor_input
MODEL='typesafe/jev-1.13';SNAPSHOT='typesafe/jev-1.13-20260917';PROVIDER='TypeSafe';RATE=.000000042;RESERVE=32000*RATE

def digest(state,q):return hashlib.sha256(json.dumps([state,q],sort_keys=True).encode()).hexdigest()
def probes():
    options={m:m for m in ('A','B','C','STOP')};items=[]
    for x in options:items.append({'state':'The required response is '+x+'.','question':{'type':'choice','instructions':'Select exactly the required response.','criteria':options},'target':x,'kind':'option'})
    for j,order in enumerate(itertools.permutations('ABC')):
        scores=dict(zip(order,[.9,.5,.1]));items.append({'state':'Current estimated qualities: '+json.dumps(scores),'question':{'type':'choice','instructions':'Select the configuration with the highest current estimated quality.','criteria':{m:m for m in MODES}},'target':order[0],'kind':'reading'})
        items.append({'state':f'Old estimated qualities: {order[0]}=0.9, {order[1]}=0.5, {order[2]}=0.1. After a paid check the current estimates are {order[0]}=0.2, {order[1]}=0.5, {order[2]}=0.1.','question':{'type':'choice','instructions':'Use the CURRENT estimates after the check. Select the configuration with the highest current quality.','criteria':{m:m for m in MODES}},'target':order[1],'kind':'update'})
    return items

def validate_response(data,criteria):
    if data.get('model')!=SNAPSHOT or data.get('provider')!=PROVIDER:raise ValueError('route_changed')
    u=data['usage'];cost=u['cost'];nt=u['input_tokens']
    if not isinstance(nt,int) or not 0<nt<=32000 or not math.isfinite(cost) or not 0<=cost<=RESERVE+1e-10:raise ValueError('usage_invalid')
    ans=data['answers']['decision'];p=ans['probabilities'];c=ans['choice']
    if set(p)!=set(criteria) or c not in criteria or any(not math.isfinite(v) or not 0<=v<=1 for v in p.values()) or abs(sum(p.values())-1)>.001 or p[c]<max(p.values())-1e-5:raise ValueError('choice_invalid')
    return {'model':data['model'],'provider':data['provider'],'usage':{k:u[k] for k in ('cost','input_tokens','output_tokens')},'answers':{'decision':{'choice':c,'probabilities':p}}}

class Runtime:
    def __init__(self,relay):
        assert relay.startswith('http://127.0.0.1:')
        self.relay=relay;self.receipts=[];self.metadata={'model':MODEL,'checkpoint':SNAPSHOT,'provider':PROVIDER,'endpoint':'OpenRouter Decisions API','route_fallbacks':False,'input_usd_per_token':RATE,'device':'hosted; worker on exclusive fleet allocation'}
    def choose(self,state,instructions,criteria,context):
        q={'type':'choice','instructions':instructions,'criteria':criteria};h=digest(state,q);rid=hashlib.sha256(json.dumps([context,h],sort_keys=True).encode()).hexdigest()
        receipt={'context':context,'state':state,'question':q,'input_hash':h,'valid':False,'encoded_tokens':0};self.receipts.append(receipt);start=time.monotonic()
        try:
            payload=json.dumps({'id':rid,'state':state,'question':q}).encode()
            request=urllib.request.Request(self.relay,payload,{'Content-Type':'application/json'})
            with urllib.request.urlopen(request,timeout=35) as response:data=json.load(response)
            if 'error' in data:raise RuntimeError('relay_rejected_or_provider_failed')
            data=validate_response(data,criteria);answer=data['answers']['decision']
            receipt.update(valid=True,choice=answer['choice'],probabilities=answer['probabilities'],usage=data['usage'],encoded_tokens=data['usage']['input_tokens'],served_model=data['model'],provider=data['provider'])
            return answer['choice']
        except Exception as exc:receipt['error']=type(exc).__name__;raise
        finally:receipt['wall_s']=time.monotonic()-start

def allowlist(records):
    allowed={digest(p['state'],p['question']) for p in probes()};cal=calibrate(records[:20])
    for record in records[20:]:
        boards=[initial(record,cal)]
        for m in MODES:
            b=initial(record,cal);purchase(b,record,m);boards.append(b)
        for b in boards:
            for role,shared in [(4,True)]+[(r,False) for r in range(5)]:
                state=actor_input(b,role,shared)
                q={'type':'choice','instructions':f'You are the {ROLES[role]}. Select the most useful next check for choosing high-quality OCR. Stop if another check is unlikely to change the choice. Consider uncertainty and the two-check limit.','criteria':{m:f'Check configuration {m}' for m in MODES}|{'STOP':'Stop checking and commit'}}
                allowed.add(digest(state,q))
    return sorted(allowed)
