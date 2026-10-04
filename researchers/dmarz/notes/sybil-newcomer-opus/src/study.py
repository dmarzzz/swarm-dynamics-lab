"""Frozen paired assignments; model receives only observable packets, never evaluator data."""
import gzip,hashlib,json,subprocess
from pathlib import Path
from collections import Counter
import yaml
import sim
ROOT=Path(__file__).resolve().parent.parent

def design():return yaml.safe_load((ROOT/'design.yaml').read_text())
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()
def source_hash():
    paths=[ROOT/'design.yaml',ROOT/'experiment.yaml',ROOT/'requirements.txt']+sorted((ROOT/'src').glob('*.py'))
    return digest([(p.name,hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths])
def params(stage):
    if stage not in ('S0','Q0','S1'):raise ValueError('Formal S2 disabled')
    return dict(stage=stage,backend='scripted' if stage=='S0' else 'anthropic',batch=f'{stage.lower()}-001',source_hash=source_hash(),code=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip())

def qualification_assignments():
    rows=[]
    for task in design()['qualification_worlds']:
        vals=sim.rng(task,'qualification').sample(range(-900,901),6)
        for shape in ('full','common_only','sparse'):
            for repeated in (False,True):
                skills=list(range(6)) if shape=='full' else list(range(3)) if shape=='common_only' else [1,3,5]
                reports=[{'message':f'q{i}-{s}','node':f'p{sim.rng(task,i,s).randrange(10000,99999)}','skill':s,'claim':vals[s],'join_round':1,'audit_now':'passed' if i==0 else 'unchecked','history':{'pass':int(i==0),'fail':0}} for i in range(2 if repeated else 1) for s in skills]
                sim.rng(task,shape,repeated).shuffle(reports)
                packet={'skills':list(range(6)),'round':4,'reports':reports,'audit_pass_probability':{'true_claim':.95,'false_claim':.05}}
                a=dict(task=task,identities=0,arm=shape,round=4,strategy='clean',kind='qualification',packet=packet,answers=vals,expected={str(s):vals[s] if s in skills else None for s in range(6)},graph_metrics={})
                a['id']=digest([task,shape,repeated])[:20];a['packet_hash']=digest(packet);rows.append(a)
    return rows

def assignments(stage,out=None,heartbeat=None):
    d=design();rows=qualification_assignments() if stage in ('S0','Q0') else []
    worlds_log=gzip.open(out/'worlds.jsonl.gz','wt') if out else None
    history_log=gzip.open(out/'history.jsonl.gz','wt') if out else None
    if stage in ('S0','S1'):
        for task in d['engineering_worlds'] if stage=='S0' else d['worlds']:
            for identities in d['identities']:
                if heartbeat:heartbeat(identities,task)
                for strategy in d['strategies']:
                    world=sim.make_world(task,identities,strategy,d['cfg'])
                    if worlds_log:worlds_log.write(json.dumps(world,sort_keys=True)+'\n')
                    for arm in d['arms']:
                        trace=sim.simulate(world,arm,d['cfg'])
                        for state in trace:
                            if history_log:history_log.write(json.dumps(dict(task=task,identities=identities,strategy=strategy,arm=arm,**state),sort_keys=True)+'\n')
                            if state['round'] not in d['observed_rounds']:continue
                            t=state['round'];packet=state['packet'];present={r['skill'] for r in packet['reports']}
                            a=dict(task=task,identities=identities,arm=arm,round=t,strategy=strategy,kind='pilot',packet=packet,answers=world['truths'][t],expected={str(s):world['truths'][t][s] if s in present else None for s in range(6)},graph_metrics=state['metrics'])
                            a['id']=digest([task,identities,arm,t,strategy])[:20];a['packet_hash']=digest(packet);rows.append(a)
    if worlds_log:worlds_log.close()
    if history_log:history_log.close()
    sim.rng('sybil-newcomer-api-v1',stage,'dispatch').shuffle(rows)
    assert len({r['id'] for r in rows})==len(rows)
    return rows

def scripted(packet):
    values={}
    for s in packet['skills']:
        # Baseline gives each message one vote, ties abstain. Not a claimed optimal policy.
        c=Counter(r['claim'] for r in packet['reports'] if r['skill']==s).most_common()
        values[str(s)]=c[0][0] if c and (len(c)==1 or c[0][1]>c[1][1]) else None
    return {'values':values}

def validate(answer):
    if not isinstance(answer,dict) or set(answer)!={'values'}:raise ValueError('answer_schema')
    values=answer['values']
    if not isinstance(values,dict) or set(values)!={str(s) for s in range(6)}:raise ValueError('answer_keys')
    if not all(v is None or type(v) is int for v in values.values()):raise ValueError('answer_type')
    return answer

def evaluate(a,answer):
    v=validate(answer)['values'];expected=a['expected'];correct=[v[str(s)]==a['answers'][s] for s in range(6)]
    missing=[s for s in range(6) if expected[str(s)] is None];metrics=dict(a['graph_metrics'])
    metrics.update(rare_accuracy=sum(correct[3:])/3,task_accuracy=sum(correct)/6,wrong_specialist=sum(v[str(s)] is not None and not correct[s] for s in (3,4,5))/3,
        qualification_accuracy=sum(v[k]==x for k,x in expected.items())/6,exact_packet=v==expected,missing_fields=len(missing),missing_correct=sum(v[str(s)] is None for s in missing))
    return metrics

def qualification(rows):
    cells=[]
    for shape in ('full','common_only','sparse'):
        rr=[r for r in rows if r['kind']=='qualification' and r['arm']==shape and r['status']=='completed'];expected=len(design()['qualification_worlds'])*2
        fields=sum(r['evaluation']['missing_fields'] for r in rr)
        c=dict(shape=shape,count=len(rr),expected=expected,fact_accuracy=sim.mean([r['evaluation']['qualification_accuracy'] for r in rr]),exact_packet_rate=sim.mean([r['evaluation']['exact_packet'] for r in rr]),missing_abstention=sum(r['evaluation']['missing_correct'] for r in rr)/fields if fields else 1)
        c['passed']=len(rr)==expected and all(c[k]>=design()['qualification'][k] for k in ('fact_accuracy','exact_packet_rate','missing_abstention'));cells.append(c)
    return {'cells':cells,'passed':all(c['passed'] for c in cells)}
