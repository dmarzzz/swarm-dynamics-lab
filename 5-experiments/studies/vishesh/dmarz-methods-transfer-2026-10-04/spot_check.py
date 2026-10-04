"""Saved-data arithmetic audit. Standard library only; no providers or world generators."""
from pathlib import Path
from collections import Counter, defaultdict
from statistics import mean
import csv, gzip, hashlib, json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
D = ROOT / 'researchers/dmarz/notes'
INPUTS = []
def rows(rel):
    p = D / rel
    INPUTS.append(p)
    if p.suffix == '.gz':
        with gzip.open(p, 'rt') as f: return [json.loads(line) for line in f]
    with p.open() as f: return list(csv.DictReader(f))
def integrity(rs, n):
    assert len(rs) == n and len({r['id'] for r in rs}) == n
    assert all(r['status'] == 'completed' for r in rs)
def paired(rs, keys, select, value):
    groups = defaultdict(dict)
    for r in rs:
        if select(r):
            key = tuple(r[k] for k in keys)
            cell, val = value(r)
            assert cell not in groups[key]
            groups[key][cell] = val
    return groups

out = {'scope': 'Independent arithmetic on saved row evaluations and CSV outputs; not raw-trace regrading or an independent replication.', 'model_calls': 0}
m = rows('market-split-opus/report/s1-001/episode-results.csv')
assert len(m) == 36 and all(r['valid'] == 'True' for r in m)
assert len({(r['task_id'],r['world'],r['arm']) for r in m}) == 36
out['market_split'] = {'tasks': len({r['task_id'] for r in m}), 'episodes':len(m), 'calls':sum(int(r['model_calls']) for r in m), 'flexible_evasion':{w:sum(r['behavioral_evasion']=='True' for r in m if r['world']==w and r['arm']=='neutral_dynamic') for w in ['firm','owner','none']}}
mp = rows('market-split-opus/report/s1-001/paired-task-results.csv')
out['market_split']['firm_profit_difference'] = mean(float(r['dynamic_profit'])-float(r['locked_profit']) for r in mp if r['regulator']=='firm')
assert out['market_split']['flexible_evasion'] == {'firm':6,'owner':0,'none':0}

s = rows('sybil-split-opus/records/s1-episodes.jsonl.gz'); integrity(s,2688)
def split_effect(p):
    g=paired(s,['family','task'],lambda r:r['attacker_pass']==p and r['checks']==12 and r['arm'] in ['degree','coverage'] and r['k'] in [1,27],lambda r:((r['arm'],r['k']),r['evaluation']['rare_wrong']))
    assert len(g)==48 and all(len(v)==4 for v in g.values())
    return mean((v['degree',27]-v['degree',1])-(v['coverage',27]-v['coverage',1]) for v in g.values())
out['sybil_split']={'roots':len({(r['family'],r['task']) for r in s}), 'rows':len(s), 'distinct_packets':len({r['packet_hash'] for r in s}), 'strong_primary_pp':100*split_effect(.1),'weak_primary_pp':100*split_effect(.9)}
assert abs(split_effect(.1)-.4097222222222222)<1e-12

s = rows('sybil-scarcity-opus/records/s1-episodes.jsonl.gz'); integrity(s,1440)
g=paired(s,['task'],lambda r:r['arm']=='random' and r['attacker_pass']==.1 and r['checks']==108,lambda r:(r['carriers'],r['evaluation']['rare_accuracy']))
assert len(g)==24 and all(len(v)==5 for v in g.values())
invariants=defaultdict(list)
for r in s: invariants[r['task'],r['arm'],r['attacker_pass'],r['checks']].append(r)
violations=sum(len({tuple(r[k] for k in ['audit_hash','admitted_hash','order_hash']) for r in rs})!=1 for rs in invariants.values())
out['sybil_scarcity']={'roots':len(g),'rows':len(s),'primary_pp':100*mean(v[1]-v[81] for v in g.values()),'carrier_accuracy':{c:mean(v[c] for v in g.values()) for c in [1,3,9,27,81]},'matched_invariance_groups':len(invariants),'hash_invariance_violations':violations}
assert violations==0 and abs(out['sybil_scarcity']['primary_pp']+95.83333333333333)<1e-9

s=rows('trust-credit-qwen/records/s1-episodes.jsonl.gz'); integrity(s,504)
g=paired(s,['task'],lambda r:r['kind']=='pilot' and r['attacker_pass']==.1 and r['rule'] in ['direct','propagated'] and r['checks'] in [32,108],lambda r:((r['rule'],r['checks']),r['admission']['attacker_seats']))
assert len(g)==24 and all(len(v)==4 for v in g.values())
out['trust_credit']={'roots':len(g),'rows':len(s),'scripted_primary_seats':mean((v['propagated',108]-v['propagated',32])-(v['direct',108]-v['direct',32]) for v in g.values()),'direct_32':mean(v['direct',32] for v in g.values()),'propagated_32':mean(v['propagated',32] for v in g.values())}
assert out['trust_credit']['scripted_primary_seats']==20.75

s=rows('verify-cost-qwen/records/attempt-002/p0-episodes.jsonl.gz')+rows('verify-cost-qwen/records/attempt-002/q0-episodes.jsonl.gz'); integrity(s,24)
optimal=correct=swapped=near_swapped=follow=0
for r in s:
    # Re-derive loss from explicit action consequences, independently of saved evaluation.
    loss={'check':r['unknown_cost'],'explore':r['error']}
    action=r['evaluation']['action'] # label recovered from saved evaluator; no prompt regeneration
    optimal+=loss[action]==min(loss.values())
    w=r['evaluation']['work']; c,x=w['cost_check'],w['cost_explore']
    correct+=abs(c-loss['check'])<.005 and abs(x-loss['explore'])<.005
    is_swap=abs(c-loss['explore'])<.005 and abs(x-loss['check'])<.005
    swapped+=is_swap
    near_swapped+=not is_swap and ((abs(c-loss['explore'])<.005 and x==0 and loss['check']<loss['explore']) or (abs(x-loss['check'])<.005 and c==0 and loss['explore']<loss['check']))
    follow+=({'check':c,'explore':x}[action]==min(c,x))
out['verify_cost_repair']={'layouts':len({r['layout'] for r in s}),'valid_rows':len(s),'optimal':optimal,'both_costs_correct':correct,'exact_cost_swap':swapped,'swapped_with_zero':near_swapped,'chooses_smaller_written_cost':follow,'optimal_by_representation':dict(Counter(r['representation'] for r in s if r['evaluation']['optimal']))}
assert (optimal,correct,swapped,near_swapped,follow)==(10,8,11,4,23)
out['inputs']=[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in INPUTS]
print(json.dumps(out,indent=2,sort_keys=True))
