"""Pinned Jev adapter and finite probe/actor payload allowlist. No credential handling here."""
import copy,hashlib,itertools,json,math,os,time,urllib.request
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
    if set(p)!=set(criteria) or c not in criteria or any(not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v) or not 0<=v<=1 for v in p.values()):raise ValueError('choice_invalid')
    # Preserve the returned numbers. Two-decimal serialization can sum to 0.99/1.01.
    on_grid=all(abs(v*100-round(v*100))<1e-8 for v in p.values())
    tolerance=.005*len(p)+1e-9 if on_grid else .001
    if abs(sum(p.values())-1)>tolerance or p[c]<max(p.values())-1e-5:raise ValueError('choice_invalid')
    return {'model':data['model'],'provider':data['provider'],'usage':{k:u[k] for k in ('cost','input_tokens','output_tokens')},'answers':{'decision':{'choice':c,'probabilities':p}}}

def safe_diagnostic(data,criteria):
    def number(v):return v if isinstance(v,(int,float)) and math.isfinite(v) else None
    u=data.get('usage',{});a=data.get('answers',{}).get('decision',{});p=a.get('probabilities',{})
    vals={k:number(p.get(k)) for k in criteria};c=a.get('choice')
    return {'model_matches':data.get('model')==SNAPSHOT,'provider_matches':data.get('provider')==PROVIDER,'selected':c if c in criteria else 'unexpected','labels_match':set(p)==set(criteria),'probabilities':vals,'probability_sum':sum(vals.values()) if all(v is not None for v in vals.values()) else None,'usage':{k:number(u.get(k)) for k in ['cost','input_tokens','output_tokens']}}

class Runtime:
    def __init__(self,relay,attempt=1,previous=(),journal=None):
        assert relay.startswith('http://127.0.0.1:')
        self.relay=relay;self.attempt=attempt;self.receipts=[];self.journal=journal;self.cache={}
        for path in previous:
            data=json.loads(Path(path).read_text());rows=data if isinstance(data,list) else [data['response']]
            for old in rows:
                r=copy.deepcopy(old)
                diag=r.get('diagnostic')
                if not r['valid'] and r.get('reason')=='choice_invalid' and diag and diag['model_matches'] and diag['provider_matches'] and diag['labels_match']:
                    data={'model':SNAPSHOT,'provider':PROVIDER,'usage':diag['usage'],'answers':{'decision':{'choice':diag['selected'],'probabilities':diag['probabilities']}}}
                    checked=validate_response(data,r['question']['criteria'])
                    r.update(valid=True,choice=diag['selected'],probabilities=diag['probabilities'],usage=diag['usage'],encoded_tokens=diag['usage']['input_tokens'],served_model=SNAPSHOT,provider=PROVIDER,schema_recovered='two-decimal probability sum; original action unchanged')
                if r['valid']:self.cache.setdefault(json.dumps([r['context'],r['input_hash']],sort_keys=True),(r,Path(path).parent.name))
        self.metadata={'model':MODEL,'checkpoint':SNAPSHOT,'provider':PROVIDER,'endpoint':'OpenRouter Decisions API','route_fallbacks':False,'probability_sum_rule':'half a 0.01 rounding unit per component when all values lie on that grid; otherwise 0.001; no normalization','input_usd_per_token':RATE,'device':'hosted; worker on exclusive fleet allocation'}
    def choose(self,state,instructions,criteria,context):
        q={'type':'choice','instructions':instructions,'criteria':criteria};h=digest(state,q);rid=hashlib.sha256(json.dumps([context,h,self.attempt],sort_keys=True).encode()).hexdigest()
        key=json.dumps([context,h],sort_keys=True)
        if key in self.cache:
            old,source=self.cache[key];receipt=copy.deepcopy(old);receipt['reused_from']=source;self.receipts.append(receipt);self.persist(receipt);return receipt['choice']
        receipt={'context':context,'state':state,'question':q,'input_hash':h,'valid':False,'encoded_tokens':0};self.receipts.append(receipt);start=time.monotonic()
        try:
            payload=json.dumps({'id':rid,'state':state,'question':q}).encode()
            request=urllib.request.Request(self.relay,payload,{'Content-Type':'application/json'})
            with urllib.request.urlopen(request,timeout=35) as response:data=json.load(response)
            if 'error' in data:
                receipt['diagnostic']=data.get('diagnostic');receipt['reason']=data.get('reason');raise RuntimeError('relay_rejected_or_provider_failed')
            data=validate_response(data,criteria);answer=data['answers']['decision']
            receipt.update(valid=True,choice=answer['choice'],probabilities=answer['probabilities'],usage=data['usage'],encoded_tokens=data['usage']['input_tokens'],served_model=data['model'],provider=data['provider'])
            return answer['choice']
        except Exception as exc:receipt['error']=type(exc).__name__;raise
        finally:
            receipt['wall_s']=time.monotonic()-start;self.persist(receipt)
    def persist(self,receipt):
        if self.journal:
            with Path(self.journal).open('a') as f:f.write(json.dumps(receipt)+'\n');f.flush();os.fsync(f.fileno())

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
