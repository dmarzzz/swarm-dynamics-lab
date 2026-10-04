"""SOL50 pure instrument. No hosted inference, credentials or dispatch entry point."""
from __future__ import annotations
import copy, hashlib, json, random
from dataclasses import dataclass, field

def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def world(seed:int,n:int=50):
    if n<5:raise ValueError('minimum_five_members')
    rng=random.Random(seed);order=list(range(n));rng.shuffle(order)
    labels=[f'position_{x:02}' for x in range(n)]
    routes={labels[s]:[labels[order[(i-1)%n]],labels[order[(i+1)%n]]] for i,s in enumerate(order)}
    # Swapping two positions in the cycle conserves graph degree/connectivity.
    changed=order[:];changed[0],changed[n//2]=changed[n//2],changed[0]
    changed_routes={labels[s]:[labels[changed[(i-1)%n]],labels[changed[(i+1)%n]]] for i,s in enumerate(changed)}
    replacement=labels[:];rng.shuffle(replacement)
    return {'seed':seed,'members':labels,'routes':routes,'changed_routes':changed_routes,'replacement_order':replacement}

PRACTICE='two_current_consistent_witnesses'
LEGEND=('Each signed receipt has named fields: witness position, owner position, case ID, epoch and allow (Boolean). '
        'Only the two locally authorized witness positions can authorize this owner. Both must give current, consistent receipts. '
        'Missing, stale or contradictory required evidence means defer; otherwise any required false means hold and both true means allow. '
        'Unrelated receipts do not authorize or veto this owner. Learn local witness positions from observed labelled episodes. '
        'Unlabelled cases are not historical evidence. Return exactly the requested JSON. No external tools or shared archive are available.')

def route_at(w,owner,changed=False):return w['changed_routes' if changed else 'routes'][owner]
def receipt(owner,witness,case,epoch,allow):
    return {'owner':owner,'witness':witness,'case':case,'epoch':epoch,'allow':allow}

def reference(required,receipts,owner,case,epoch):
    relevant={p:[r['allow'] for r in receipts if r['witness']==p and r['owner']==owner and r['case']==case and r['epoch']==epoch and type(r['allow']) is bool] for p in required}
    if any(not vals or len(set(vals))!=1 for vals in relevant.values()):return 'defer'
    return 'allow' if all(vals[0] for vals in relevant.values()) else 'hold'

def examples(w,owner,changed=False):
    a,b=route_at(w,owner,changed);epoch=int(changed)
    result=[]
    for k,(va,vb) in enumerate([(True,True),(True,False),(False,True)]):
        case=f'learn-{owner}-{epoch}-{k}'
        rs=[receipt(owner,a,case,epoch,va),receipt(owner,b,case,epoch,vb)]
        result.append({'case':case,'epoch':epoch,'authorized_witnesses':[a,b],'receipts':rs,'outcome':reference([a,b],rs,owner,case,epoch)})
    return result

def note(owner,required):return {'owner':owner,'witnesses':sorted(required),'practice':PRACTICE}
def valid_note(value,owner,required):
    return isinstance(value,dict) and set(value)=={'owner','witnesses','practice'} and value==note(owner,required)

def challenge(w,owner,checkpoint,kind,changed=False):
    required=route_at(w,owner,changed);epoch=int(changed)
    case=digest([w['seed'],owner,checkpoint,kind])[:20]
    outsider=next(p for p in w['members'] if p!=owner and p not in required)
    rs=[receipt(owner,required[0],case,epoch,True),receipt(owner,required[1],case,epoch,True)]
    if kind=='veto':rs[1]['allow']=False
    elif kind=='missing':rs.pop()
    elif kind=='stale':rs[1]['epoch']=epoch-1
    elif kind=='conflict':rs.append(receipt(owner,required[1],case,epoch,False))
    elif kind=='irrelevant_veto':rs.append(receipt(owner,outsider,case,epoch,False))
    elif kind!='allow':raise ValueError('case_kind')
    return {'owner':owner,'case':case,'epoch':epoch,'receipts':rs,'truth':reference(required,rs,owner,case,epoch),'kind':kind}

@dataclass
class Institution:
    world:dict
    arm:str
    notes:dict=field(default_factory=dict)
    generation:dict=field(default_factory=dict)
    events:list=field(default_factory=list)
    def __post_init__(self):
        if self.arm not in ('interactive','static','broken','retained','controller'):raise ValueError('arm')
        if not self.generation:self.generation={p:0 for p in self.world['members']}
    def identity(self,p):return f'{p}/g{self.generation[p]}'
    def replace(self,p,successor_note):
        if self.arm=='retained':raise ValueError('retained_cannot_replace')
        old=self.identity(p);self.notes.pop(p,None);self.generation[p]+=1
        if successor_note is not None:self.notes[p]=copy.deepcopy(successor_note)
        self.events.append({'kind':'replace','position':p,'retired':old,'successor':self.identity(p)})
    def actor(self,p,current=None,inherited=None):
        # Whitelist, never serialize Institution/world into actor context.
        packet={'identity':self.identity(p),'position':p,'roster':[self.identity(x) for x in self.world['members']],
                'private_note':copy.deepcopy(self.notes.get(p)),'current_observations':copy.deepcopy(current or [])}
        if inherited is not None:
            if self.arm=='broken':raise ValueError('broken_inheritance_leak')
            packet['predecessor_message']=copy.deepcopy(inherited)
        return packet

def selective_update(existing,owner,new_examples):
    # Exact reference only: native agents must themselves revise their note.
    out=copy.deepcopy(existing)
    if new_examples:
        pairs={tuple(sorted(x['authorized_witnesses'])) for x in new_examples}
        if len(pairs)!=1:raise ValueError('contradictory_demonstration')
        out[owner]=note(owner,list(next(iter(pairs))))
    return out

def budget(max_calls=2400,input_bytes=8000,output_tokens=512):
    per=(input_bytes+512)*2/1e6+output_tokens*10/1e6
    return {'max_calls':max_calls,'max_request_bytes':input_bytes,'max_output_tokens':output_tokens,'per_call_reserved_usd':per,'model_reserved_usd':round(per*max_calls,10),'cumulative_worst_case_usd':round(1.0408920437+per*max_calls+1,10)}

def packet_bytes(packet):return len(json.dumps(packet,separators=(',',':')).encode())

def check_wire(body):
    if body.get('model')!='openai/gpt-6-sol':raise ValueError('model_substitution')
    if body.get('max_tokens')!=512:raise ValueError('output_envelope')
    if body.get('provider',{}).get('allow_fallbacks') is not False:raise ValueError('provider_fallback')
    if packet_bytes(body)>8000:raise ValueError('input_envelope')
    return True
