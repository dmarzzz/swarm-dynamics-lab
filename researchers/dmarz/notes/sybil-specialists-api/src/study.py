"""Frozen assignments, public packets and evaluator for an exploratory API study."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import yaml

ROOT = Path(__file__).resolve().parent.parent
PARENT = ROOT.parent / 'sybil-specialists/src/sim.py'
spec = importlib.util.spec_from_file_location('sybil_environment', PARENT)
sim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sim)


def design():
    return yaml.safe_load((ROOT / 'design.yaml').read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def source_hash():
    paths = [ROOT/'design.yaml', ROOT/'experiment.yaml', ROOT/'requirements.txt', PARENT]
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


def assignments(stage):
    d = design(); cfg = d['cfg']; rows = []
    if stage in ('S0', 'Q0'):
        for task in d['stages']['Q0']['tasks']:
            world = sim.make_world(task, 1, .1, True, cfg)
            for arm in ('full', 'common_only'):
                admitted = [n for n,v in world['public']['nodes'].items()
                            if arm == 'full' or v['skill'] < 3]
                for visibility in d['visibility']:
                    rows.append({'task':task, 'arm':arm, 'visibility':visibility,
                                 'attacker_pass':None, 'kind':'qualification', 'world':world,
                                 'admitted':admitted, 'checked':[],
                                 'packet':packet(world, admitted, [], visibility, arm)})
    if stage in ('S0', 'S1'):
        for task in d['stages']['S1']['tasks']:
            for rate in d['pilot']['attacker_pass']:
                world = sim.make_world(task, d['pilot']['bridges'], rate, False, cfg)
                for result in sim.run_episode(world, d['pilot']['verification_budget'], d['arms'], cfg):
                    final = result['trace'][-1]
                    for visibility in d['visibility']:
                        rows.append({'task':task, 'arm':result['arm'], 'visibility':visibility,
                                     'attacker_pass':rate, 'kind':'pilot', 'world':world,
                                     'admitted':final['admitted'],
                                     'checked':[t['event']['node'] for t in result['trace'] if t['event']],
                                     'packet':packet(world, final['admitted'], final['passed'], visibility, result['arm'])})
    for r in rows:
        r['id'] = digest({k:r[k] for k in ('task','arm','visibility','attacker_pass','kind')})[:20]
        r['packet_hash'] = digest(r['packet'])
    sim.rng('sybil-specialists-api-v1', stage, 'dispatch').shuffle(rows)
    assert len({r['id'] for r in rows}) == len(rows)
    assert all(r['task'] < 10000 for r in rows)
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


def evaluate(a, answer):
    vals = validate(answer)['values']
    result = sim.evaluate(a['world'], a['admitted'], vals, a['checked'])
    present = {r['skill'] for r in a['packet']['reports']}
    expected = {str(s): a['world']['answers'][s] if s in present else None for s in range(6)}
    missing = [s for s in range(6) if s not in present]
    result.update(qualification_accuracy=sum(vals[k]==v for k,v in expected.items())/6,
                  exact_packet=vals==expected, missing_fields=len(missing),
                  missing_correct=sum(vals[str(s)] is None for s in missing))
    return result


def qualification(rows):
    good = [r for r in rows if r['status']=='completed' and r['kind']=='qualification']
    expected = len(design()['stages']['Q0']['tasks'])*4
    fields = sum(r['evaluation']['missing_fields'] for r in good)
    metrics = {'count':len(good),
               'fact_accuracy':sum(r['evaluation']['qualification_accuracy'] for r in good)/len(good) if good else 0,
               'exact_packet_rate':sum(r['evaluation']['exact_packet'] for r in good)/len(good) if good else 0,
               'missing_abstention':sum(r['evaluation']['missing_correct'] for r in good)/fields if fields else 0}
    q = design()['qualification']
    metrics['passed'] = len(good)==expected and all(metrics[k]>=q[k] for k in ('fact_accuracy','exact_packet_rate','missing_abstention'))
    return metrics
