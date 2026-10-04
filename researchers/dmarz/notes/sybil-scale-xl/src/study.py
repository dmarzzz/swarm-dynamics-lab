"""Frozen assignments, public packets and evaluator for an exploratory API study."""
import hashlib
import os
import importlib.util
import json
from pathlib import Path
import subprocess
import yaml

ROOT = Path(__file__).resolve().parent.parent
import sim


def design():
    return yaml.safe_load((ROOT / 'design.yaml').read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def source_hash():
    paths = [ROOT/'design.yaml', ROOT/'experiment.yaml', ROOT/'requirements.txt']
    paths += sorted((ROOT/'src').glob('*.py'))
    return digest([(p.name, hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths])


def params(stage):
    if stage not in ('S0', 'Q0', 'S1'):
        raise ValueError('Formal S2 disabled')
    return dict(stage=stage, backend='scripted' if stage == 'S0' else 'anthropic',
                batch=f'{stage.lower()}-001', source_hash=source_hash(),
                code=subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip())


def packet(world, admitted, passed, visibility, arm):
    reports = []
    for node in admitted:
        row = {'node':node, **world['public']['nodes'][node]}
        if visibility == 'visible':
            row['verification'] = ('trusted' if node in world['public']['trusted'] else
                                   'passed' if node in passed else 'unchecked')
        reports.append(row)
    # Same order across badge modes and verifier reliabilities; no rank/truth sorting.
    sim.rng(world['task'], 'packet-order', arm).shuffle(reports)
    return {'skills':list(range(6)), 'reports':reports}


def cfg_for(n):
    cfg=dict(design()['cfg']);cfg.update(core=n//2,community=n//4,admission_seats=n//2)
    return cfg


def prepare(job):
    n,task,rate,kind=job;cfg=cfg_for(n);d=design()
    if kind=='qualification':
        world=sim.make_world(task,n//36,rate,True,cfg);nodes=sorted(world['public']['nodes'])
        # Clean packets at the S1 packet size (n/2 reports): a uniform sample with every skill,
        # and the n/2 common-skill identities, so the missing-fact abstention test is kept.
        sample=sorted(sim.rng(task,n,'q0-sample').sample(nodes,n//2))
        common=[x for x in nodes if world['public']['nodes'][x]['skill']<3]
        return n,kind,world,[('sample',sample),('common_only',common)]
    world=sim.make_world(task,n//36,rate,False,cfg)
    return n,kind,world,sim.checkpoints(world,[4,n//9],d['arms'],cfg)


def assignments(stage, out=None, heartbeat=None):
    import gzip
    d=design(); rows=[]
    worlds_log=gzip.open(out/'worlds.jsonl.gz','wt') if out else None
    def remember(world,n,rate,kind):
        if heartbeat: heartbeat(n,world['task'])
        if worlds_log: worlds_log.write(json.dumps({'n':n,'rate':rate,'kind':kind,'world':world},sort_keys=True)+'\n')
    def add(world,n,arm,checks,visibility,kind,admitted,passed,checked,events):
        pack=packet(world,admitted,passed,visibility,arm)
        present={p['skill'] for p in pack['reports']}
        a={'task':world['task'],'n':n,'arm':arm,'checks':checks,'visibility':visibility,
           'attacker_pass':world['cell']['attacker_pass'] if kind=='pilot' else None,'kind':kind,
           'packet':pack,'answers':world['answers'],'expected':{str(s):world['answers'][s] if s in present else None for s in range(6)},
           'graph_metrics':sim.evaluate(world,admitted,sim.decide(world['public'],admitted),checked),
           'verification_events':events}
        a['id']=digest({k:a[k] for k in ('task','n','arm','checks','visibility','attacker_pass','kind')})[:20]
        a['packet_hash']=digest(pack); rows.append(a)
    jobs=[]
    for n in d['sizes']:
        if stage in ('S0','Q0'):
            jobs+=[(n,task,.1,'qualification') for task in d['qualification_worlds']]
        if stage in ('S0','S1'):
            jobs+=[(n,task,rate,'pilot') for task in (d['engineering_worlds'] if stage=='S0' else d['worlds'])
                   for rate in d['pilot']['attacker_pass']]
    # Worlds are independent and deterministic; workers only parallelize preparation.
    # imap preserves job order, so rows are identical to the serial loop before the shuffle.
    import multiprocessing
    # At most 4 processes: an N=8748 world plus its checkpoints holds several hundred MB per process.
    with multiprocessing.get_context('fork').Pool(max(1,min(len(jobs),os.cpu_count() or 1,4))) as pool:
        for n,kind,world,recs in pool.imap(prepare,jobs):
            remember(world,n,world['cell']['attacker_pass'],kind)
            if kind=='qualification':
                for arm,admitted in recs:
                    for visibility in d['visibility']:
                        add(world,n,arm,0,visibility,'qualification',admitted,[],[],[])
            else:
                for rec in recs:
                    for visibility in d['visibility']:
                        add(world,n,rec['arm'],rec['checks'],visibility,'pilot',rec['admitted'],rec['passed'],rec['checked'],rec['events'])
    if worlds_log: worlds_log.close()
    sim.rng('sybil-scale-xl-v1',stage,'dispatch').shuffle(rows)
    assert len({a['id'] for a in rows})==len(rows)
    assert all(a['task']<10000 for a in rows)
    return rows


def scripted(packet):
    from collections import Counter
    values = {}
    for skill in packet['skills']:
        counts = Counter(r['claim'] for r in packet['reports'] if r['skill'] == skill).most_common()
        values[str(skill)] = counts[0][0] if counts and (len(counts)==1 or counts[0][1]>counts[1][1]) else None
    return {'values':values}


def validate(answer):
    if not isinstance(answer, dict) or set(answer) != {'values'}:
        raise ValueError('answer_schema')
    vals = answer['values']
    if not isinstance(vals, dict) or set(vals) != {str(s) for s in range(6)}:
        raise ValueError('answer_keys')
    if not all(v is None or type(v) is int for v in vals.values()):
        raise ValueError('answer_type')
    return answer


def evaluate(a,answer):
    vals=validate(answer)['values'];expected=a['expected']
    correct=[vals[str(s)]==a['answers'][s] for s in range(6)]
    missing=[s for s in range(6) if expected[str(s)] is None]
    result=dict(a['graph_metrics'])
    result.update(rare_accuracy=sum(correct[3:])/3,task_accuracy=sum(correct)/6,
        correct_skills=sum(correct),qualification_accuracy=sum(vals[k]==v for k,v in expected.items())/6,
        exact_packet=vals==expected,missing_fields=len(missing),missing_correct=sum(vals[str(s)] is None for s in missing))
    return result


def qualification(rows):
    cells=[];d=design()
    for n in d['sizes']:
        good=[r for r in rows if r['kind']=='qualification' and r['n']==n and r['status']=='completed']
        expected=len(d['qualification_worlds'])*4
        fields=sum(r['evaluation']['missing_fields'] for r in good)
        m={'n':n,'count':len(good),'expected':expected,
           'fact_accuracy':sum(r['evaluation']['qualification_accuracy'] for r in good)/len(good) if good else 0,
           'exact_packet_rate':sum(r['evaluation']['exact_packet'] for r in good)/len(good) if good else 0,
           'missing_abstention':sum(r['evaluation']['missing_correct'] for r in good)/fields if fields else 0}
        m['passed']=len(good)==expected and all(m[k]>=d['qualification'][k] for k in ('fact_accuracy','exact_packet_rate','missing_abstention'))
        cells.append(m)
    return {'cells':cells,'passed':all(c['passed'] for c in cells)}
