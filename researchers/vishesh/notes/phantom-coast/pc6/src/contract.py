"""PC6 synthetic environment; evaluator truth is excluded from native packets."""
import collections
import copy
import hashlib
import random

CELLS=tuple(f'{r},{c}' for r in range(6) for c in range(6))
LABELS={'LAND','WATER','UNKNOWN'}
POLICIES={'team','single','uniform'}


def rng(seed,stream):
    return random.Random(int.from_bytes(hashlib.sha256(f'{seed}/{stream}'.encode()).digest(),'big'))


def valid_map(m):
    return isinstance(m,dict) and set(m)==set(CELLS) and all(type(v) is str and v in LABELS for v in m.values())


def majority(maps):
    if len(maps)!=3:raise ValueError('three assigned maps required')
    maps=[m if valid_map(m) else {} for m in maps]
    return {c:next((v for v in ('LAND','WATER') if sum(m.get(c)==v for m in maps)>=2),'UNKNOWN') for c in CELLS}


def error(m,truth,cells=CELLS):
    m=m if valid_map(m) else {};cells=list(cells)
    wrong=sum(m.get(c,'UNKNOWN') not in ('UNKNOWN',truth[c]) for c in cells)
    missing=sum(m.get(c,'UNKNOWN')=='UNKNOWN' for c in cells);n=len(cells)
    return dict(wrong=wrong,missing=missing,denominator=n,lower=wrong/n if n else None,upper=(wrong+missing)/n if n else None)



def development_world(seed,family='layout'):
    if type(seed) is not int or seed not in range(2000,2008):raise ValueError('development_seed')
    return _world(seed,family)
def _world(seed,family='layout'):
    order=list(CELLS);rng(seed,'roles').shuffle(order)
    truth={c:rng(seed,'terrain/'+c).choice(('LAND','WATER')) for c in CELLS}
    legal=order[:2]
    if (seed//2)%2:legal.reverse()
    return dict(seed=seed,family='layout',report_cell=order[0],unknown_cell=order[1],report_label='LAND' if seed%2==0 else 'WATER',truth=truth,truth_draw=rng(seed,'report-calibration').random(),legal_order=legal)
def packet(w,reliability,objective,actor=0,qualification=False):
    if reliability not in (.8,.2) or objective not in ('prose','table'):raise ValueError('condition')
    rc,uc=w['report_cell'],w['unknown_cell'];observations=[dict(id='r0',acquisition_id='r0',cell=rc,label=w['report_label'],epoch=0,source='report',reliability=reliability)]
    observations += [dict(id=f's{i}',acquisition_id=f's{i}',cell=c,label=w['truth'][c],epoch=2,source='sensor',reliability=1.0) for i,c in enumerate(CELLS) if c not in (rc,uc)]
    task='Choose one cell to inspect to minimize final whole-map error within one sensing slot. Reports may be wrong. Direct measurements are noiseless. Report reliability is its calibrated probability of correctness.'
    if objective in ('prose','table'):task+=' After this action, retain the label of any uninspected report; return UNKNOWN for any uninspected cell without evidence. The selected cell receives a correct direct measurement. Each wrong label costs 1, UNKNOWN costs 0.25, and a correct label costs 0. Minimize expected total loss under this rule.'
    legal=w['legal_order']
    result=dict(task=task,actor=f'observer-{actor}',cells=list(CELLS),legal_cells=legal,remaining_slots=1,evidence=dict(observations=observations,withdrawn=[]))
    if objective=='table':
        result['action_consequences']=[dict(inspect_cell=c,remaining_uncertainty='uninspected unknown cell' if c==rc else 'uninspected report',expected_total_loss=.25 if c==rc else round(1-reliability,12)) for c in legal]
    return result
def score(w,reliability,choice):
    risk=round(1-reliability,12);rc,uc=w['report_cell'],w['unknown_cell'];optimal=uc if risk<.25 else rc
    expected=.25 if choice==rc else risk if choice==uc else risk+.25
    false=w['truth_draw']>=reliability
    realized=.25 if choice==rc else float(false) if choice==uc else float(false)+.25
    return dict(choice_role='report' if choice==rc else 'unknown' if choice==uc else 'no_inspection',optimal_cell=optimal,optimal=choice==optimal,expected_loss=expected,expected_regret=round(expected-min(.25,risk),12),realized_scripted_loss=realized,report_actually_false=false)
