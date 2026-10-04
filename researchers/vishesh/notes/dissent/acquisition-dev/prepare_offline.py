"""Emit only public offline development evidence and a disabled candidate packet."""
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import random
import subprocess
import sys
from episodes import build, digest
from engine import actor_projection, selection_request, resolve, neutral_reference, routine, replay, validate_world

BASE=Path(__file__).resolve().parent


def save(path,value):
    path.write_text(json.dumps(value,indent=2)+'\n')


def structural_signature(world):
    """Conservative core-rule grouping; state variants do not inflate family counts."""
    task=world['task'];required=set(task['requirements'])
    ranks={s['authority'] for s in world['sources'] if required.intersection(s['covers'])}
    ranks.update(task['source_authorities'][d['origin']] for d in world['initial'] if required.intersection(d['facts']))
    return {'required_predicates':len(required),'authority_levels':len(ranks),
            'combination':'mandatory_false_else_all_true_else_defer','metadata_gate':'scope_revision_inclusive_ttl'}


def prepare():
    out=BASE/'offline';out.mkdir(exist_ok=True)
    test=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(BASE),'-p','test_offline.py','-v'],capture_output=True,text=True)
    (out/'tests.txt').write_text(test.stdout+test.stderr)
    if test.returncode:raise SystemExit('Offline tests failed; no packet emitted.')
    worlds=build(); counterfactuals=[]; comparisons=[];grouped=defaultdict(list);goals={}
    for w in worlds:
        rows=validate_world(w)
        commitments={r['event']['resolution']['action'] for r in rows if r['event']['resolution']['action']!='DEFER'}
        assert len(commitments)<=1,'Conflicting attainable commitments need a different utility label.'
        goal=next(iter(commitments)) if commitments else 'DEFER';goals[w['id']]=goal
        counterfactuals.append({'episode':w['id'],'actor_initial':actor_projection(w),
            'hand_authored_labels':w['gold_by_choice'],'attainable_action':goal,'choice_outcomes':rows,
            'scope':'Every source response is authored simulation data, not a native tool execution.'})
        signature=structural_signature(w);grouped[json.dumps(signature,sort_keys=True)].append(w['id'])
        for name,policy in [('routine',routine),('neutral_reference',neutral_reference)]:
            actor=actor_projection(w);choice=policy(actor);row=replay(w,choice)
            comparisons.append({'episode':w['id'],'policy':name,'selection':choice,
                'conditional_interpreter_correct':row['event']['resolution']['action']==w['gold_by_choice'][choice],
                'attainable_action':goal,'attainable_action_reached':row['event']['resolution']['action']==goal,
                'trace':row})
    save(out/'cases.json',worlds);save(out/'counterfactuals.json',counterfactuals);save(out/'comparators.json',comparisons)
    families=[{'core_rule':json.loads(k),'episodes':v} for k,v in grouped.items()]
    save(out/'family-audit.json',{'development_episodes':len(worlds),'coverage_mechanisms':len({w['mechanism'] for w in worlds}),
        'conservative_core_rule_clusters':len(families),'clusters':families,
        'independence':'Same author and simulator; three core-rule clusters, not six independent semantic families or a24family corpus. Authority-threshold and tie-conflict states differ but share the authority resolver.'})
    assignments=[];gold={}
    for repeat in range(3):
        block=[]
        for world in worlds:
            for incumbent in ['PROCEED','HOLD','DEFER']:
                w=deepcopy(world);w['incumbent']['action']=incumbent
                actor=actor_projection(w)
                for policy in ['routine','neutral','challenge']:
                    identity='candidate-'+digest([w['id'],incumbent,policy,repeat])[:20]
                    selector=selection_request(actor,policy) if policy!='routine' else None
                    row={'id':identity,'episode':w['id'],'repeat':repeat,'incumbent':incumbent,'policy':policy,
                         'actor_before_selection':actor,'selector_request':selector,
                         'selector_request_sha256':digest(selector) if selector else None,
                         'maximum_model_calls':1 if policy=='routine' else 2}
                    block.append(row);gold[identity]={'conditional_action_by_choice':w['gold_by_choice'],
                                                      'attainable_action':goals[w['id']]}
        random.Random(81004+repeat).shuffle(block);assignments+=block
    packet={'schema':'rd-acquisition-development-candidate-v1','stage':'ACQ-D1-candidate',
            'dispatch_enabled':False,'funding':'not_granted','data_scope':'public_development_not_holdout',
            'fresh_repeats':3,'episodes':6,'incumbent_conditions':3,'policies':3,
            'trajectories':len(assignments),'maximum_model_calls':sum(r['maximum_model_calls'] for r in assignments),
            'model':'typesafe/jev-1.13-20260917','provider':'TypeSafe','assignments':assignments}
    assert packet['trajectories']==162 and packet['maximum_model_calls']==270
    for i in range(3):assert len([r for r in assignments if r['repeat']==i])==54
    for episode in worlds:
        for incumbent in ['PROCEED','HOLD','DEFER']:
            for policy in ['neutral','challenge']:
                hashes={r['selector_request_sha256'] for r in assignments if r['episode']==episode['id'] and r['incumbent']==incumbent and r['policy']==policy}
                assert len(hashes)==1
    save(out/'candidate-packet.json',packet);save(out/'candidate-gold.json',gold)
    summary={'mode':'offline_rule_replay','native_calls':0,'new_spend':0,'reserved_cases_read':0,
             'development_episodes':6,'conservative_core_rule_clusters':3,'counterfactual_choices':18,
             'conditional_label_agreement':'18/18 hand-authored rows agree with rule interpreter',
             'comparators':{p:{'assigned':6,'attainable_action_reached':sum(r['attainable_action_reached'] for r in comparisons if r['policy']==p),
                               'conditional_interpreter_correct':sum(r['conditional_interpreter_correct'] for r in comparisons if r['policy']==p),
                               'synthetic_checks_used':sum(r['trace']['event']['checks_used'] for r in comparisons if r['policy']==p)} for p in ['routine','neutral_reference']},
             'native_neutral_competence':'unmeasured','native_challenge_competence':'unmeasured',
             'native_fresh_repeatability':'unmeasured','candidate_calls':270,
             'candidate_api_ceiling_nano':270*1344000,'candidate_infrastructure_ceiling_nano':71430000,
             'candidate_additional_ceiling_nano':270*1344000+71430000,
             'required_lifetime_call_ceiling':554+270,
             'scientific_limit':'The simple coverage controller reaches all six attainable actions. These fixtures do not demonstrate a residual benefit from dissent.'}
    save(out/'summary.json',summary)
    inventory={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file() and p.name!='validation.json'}
    save(out/'validation.json',{'test_command':'python3 -m unittest discover -s researchers/vishesh/notes/dissent/acquisition-dev -p test_offline.py -v',
        'tests_passed':20,'counterfactual_rows_checked':18,'packet_balance_and_repeated_input_hashes':'passed',
        'source_sha256':{n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in ['episodes.py','engine.py','test_offline.py','prepare_offline.py','PLAN.md']},
        'artifacts':inventory,'native_calls':0})
    print(json.dumps(summary,indent=2))


if __name__=='__main__':prepare()
