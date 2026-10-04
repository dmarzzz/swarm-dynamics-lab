"""Offline proposal: named observations, explicit legend, semantic teacher gate."""
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import instrument as i
SOURCES=('source_0','source_1','source_2')
PREDICATES={'release':'signal_and_fresh','incident':'signal','recovery':'not_signal_and_fresh'}
LEGEND='Every source contains its own signal and fresh values (0 or 1). Both values in a predicate always come from the same named governing source. Historical outcome=true means allow; outcome=false means hold. A case without outcome is unlabelled work, never historical evidence.'

def encode(record):
    result=copy.deepcopy(record);values=result.pop('readings')
    result['sources']={s:{'signal':v[0],'fresh':v[1]} for s,v in zip(SOURCES,values)}
    return result

def decode(record):
    result=copy.deepcopy(record);values=result.pop('sources')
    if set(values)!=set(SOURCES):raise ValueError('source_names')
    if any(set(v)!={'signal','fresh'} or any(type(x)is not int or x not in (0,1) for x in v.values()) for v in values.values()):raise ValueError('source_fields')
    result['readings']=[[values[s]['signal'],values[s]['fresh']] for s in SOURCES];return result

def teacher_gate(role,reply,visible):
    if not isinstance(reply,dict) or reply.get('governing_source') not in SOURCES or reply.get('predicate')!=PREDICATES[role]:return False
    try:
        evidence=[decode(r) for r in reply['evidence']];available={i.digest(r) for r in visible}
        source=SOURCES.index(reply['governing_source'])
        return bool(evidence) and all(i.digest(r) in available for r in evidence) and i.compatible(role,evidence)==[source]
    except (TypeError,KeyError,ValueError):return False

def development_world(seed,scenario):
    # Deterministic development construction: retain all worlds, extend histories
    # with fresh visible examples until both outcomes have been demonstrated.
    world=i.make_world(seed,scenario)
    for role,d in world['roles'].items():
        seen={h['outcome'] for h in d['history']}
        if len(seen)<2:
            from itertools import product
            used={i.digest(c['readings']) for key in ('history','founder_tests','tests') for c in d[key]}
            for bits in product((0,1),repeat=6):
                values=[list(bits[k:k+2]) for k in (0,2,4)];out=i.truth(role,values,d['source'])
                if out not in seen and i.digest(values) not in used:
                    d['history'].append(i.record(seed,role,0,len(d['history']),values,out));break
            else:raise ValueError('no_disjoint_training_witness')
    return world
