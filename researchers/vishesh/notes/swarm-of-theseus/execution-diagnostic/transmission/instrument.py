"""Offline institutional-transmission instrument. No provider imports or network dispatch.

Evaluator World objects never enter ActorPacket. Scripted reference actors are not
native evidence. A later native adapter must enforce the same packet boundaries.
"""
from dataclasses import dataclass, field
from itertools import product, combinations
import copy, hashlib, json, random

ROLES = ('release', 'incident', 'recovery')
SCENARIOS = ('stable_exception', 'changed_practice', 'unreliable_evidence')
NOTE_LIMIT = 1200
REQUEST_BYTES = 16000

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def truth(role, values, source):
    signal, fresh = values[source]
    if role == 'release': return bool(signal and fresh)
    if role == 'incident': return bool(signal)
    if role == 'recovery': return bool(not signal and fresh)
    raise ValueError('unknown_role')

def compatible(role, records):
    """Separate truth-table expression, using only supplied visible records."""
    def predict(values, source):
        bit, age = values[source]
        table = {'release': {(1, 1)}, 'incident': {(1, 0), (1, 1)}, 'recovery': {(0, 1)}}
        return (bit, age) in table[role]
    return [s for s in range(3) if all(predict(r['readings'], s) == r['outcome'] for r in records)]

def record(seed, role, phase, i, values, outcome=None):
    r = {'id': digest([seed, role, phase, i])[:16], 'readings': values}
    if outcome is not None: r.update(outcome=outcome, epoch=phase)
    return r

def make_world(seed, scenario):
    if scenario not in SCENARIOS: raise ValueError('unknown_scenario')
    rng = random.Random(seed); sources = rng.sample(range(3), 3); roles = {}
    universe = [[list(bits[i:i+2]) for i in (0, 2, 4)] for bits in product((0, 1), repeat=6)]
    for role, source in zip(ROLES, sources):
        pool = copy.deepcopy(universe); rng.shuffle(pool)
        # Deterministic case selection; no native outputs enter construction.
        train_values = []
        for values in pool:
            train_values.append(values)
            hist = [record(seed, role, 0, i, v, truth(role, v, source)) for i, v in enumerate(train_values)]
            if len(hist) >= 8 and compatible(role, hist) == [source]: break
        rest = [v for v in pool if v not in train_values]
        for _ in range(1000):
            tests = rng.sample(rest, 8)
            positives = sum(truth(role, v, source) for v in tests)
            if 2 <= positives <= 6 and all(any(truth(role,v,other)!=truth(role,v,source) for v in tests) for other in range(3) if other!=source): break
        else: raise ValueError('test_panel_construction_failed')
        remaining = [v for v in rest if v not in tests]
        for _ in range(1000):
            founder_tests = rng.sample(remaining, 8)
            positives = sum(truth(role, v, source) for v in founder_tests)
            if 2 <= positives <= 6 and all(any(truth(role,v,other)!=truth(role,v,source) for v in founder_tests) for other in range(3) if other!=source): break
        else: raise ValueError('founder_panel_construction_failed')
        roles[role] = {'source': source, 'history': hist,
                       'founder_tests': [record(seed, role, 'founder-test', i, v) for i, v in enumerate(founder_tests)],
                       'tests': [record(seed, role, 'test', i, v) for i, v in enumerate(tests)]}
    # Current-epoch observations are the declared intervention, not hidden truth.
    events = {role: [] for role in ROLES}
    if scenario == 'changed_practice':
        role = ROLES[0]; changed = (roles[role]['source'] + 1) % 3
        events[role] = [record(seed, role, 1, i, h['readings'], truth(role, h['readings'], changed))
                        for i, h in enumerate(roles[role]['history'])]
        assert compatible(role, events[role]) == [changed]
    elif scenario == 'unreliable_evidence':
        role = ROLES[1]; readings = roles[role]['history'][0]['readings']
        events[role] = [record(seed, role, 1, i, readings, bool(i)) for i in range(2)]
        role = ROLES[2]; events[role] = [record(seed, role, 1, 0, [[0, 0]]*3, False)]
    return {'seed': seed, 'scenario': scenario, 'roles': roles, 'events': events}

def minimal_support(role, history):
    options = compatible(role, history)
    for size in range(1, len(history)+1):
        for part in combinations(history, size):
            if compatible(role, part) == options: return list(part)
    return []

def evidence_decision(role, previous, history):
    options = compatible(role, history)
    if len(options) == 1:
        source = options[0]
        state = 'retain' if source == previous else 'revise'
    else:
        source = None
        state = 'provisional' if options and (previous is None or previous in options) else 'quarantine'
    return {'state': state, 'source': source, 'compatible': options}

def robust_action(role, case, options):
    outcomes = {truth(role, case['readings'], s) for s in options}
    return ('allow' if next(iter(outcomes)) else 'hold') if len(outcomes) == 1 else 'defer'

def make_note(role, previous, history):
    decision = evidence_decision(role, previous, history)
    note = dict(role=role, **decision, evidence=minimal_support(role, history))
    serialized = json.dumps(note, separators=(',', ':'))
    if len(serialized) > NOTE_LIMIT: raise ValueError('note_overflow')
    return serialized

def read_note(role, text):
    if not isinstance(text, str) or len(text) > NOTE_LIMIT: raise ValueError('note_overflow')
    obj = json.loads(text)
    if obj['role'] != role: raise ValueError('role_mismatch')
    if set(obj) != {'role','state','source','compatible','evidence'}: raise ValueError('note_schema')
    if obj['state'] not in ('retain','revise','quarantine','provisional'): raise ValueError('note_state')
    if obj['source'] is not None and (type(obj['source']) is not int or obj['source'] not in range(3)): raise ValueError('note_source')
    if not isinstance(obj['evidence'],list) or not isinstance(obj['compatible'],list): raise ValueError('note_schema')
    for r in obj['evidence']:
        if set(r) != {'id','readings','outcome','epoch'}: raise ValueError('note_evidence_schema')
    return obj

@dataclass
class Member:
    identity: str
    role: str
    note: str
    private_history: list = field(repr=False)
    parent: str | None = None
    active: bool = True

class Institution:
    """Context-access and ancestry model; no direct actor access to registry/log."""
    def __init__(self, world):
        self.world = copy.deepcopy(world); self.members = {}; self.current = {}; self.events = []
        for role in ROLES:
            data = world['roles'][role]; ident = f'founder-{role}'
            # Scripted reference initialization only, never native founder qualification.
            note = make_note(role, data['source'], data['history'])
            self.members[ident] = Member(ident, role, note, copy.deepcopy(data['history']))
            self.current[role] = ident
    def active(self, ident):
        if ident not in self.members or not self.members[ident].active: raise ValueError('retired_or_unknown_actor')
        return self.members[ident]
    def packet(self, role, phase, question='', answer='', arm='interactive', cases=None, current_evidence=None):
        member = self.active(self.current[role])
        if arm not in ('interactive', 'static', 'broken'): raise ValueError('unknown_arm')
        if phase not in ('founder', 'question', 'answer', 'commit'): raise ValueError('unknown_phase')
        if len(question) > 400 or len(answer) > 1200: raise ValueError('message_overflow')
        for case in cases or []:
            if set(case) != {'id','readings'}: raise ValueError('case_field_leak')
        for event in current_evidence or []:
            if set(event) != {'id','readings','outcome','epoch'}: raise ValueError('evidence_field_leak')
        p = {'role': role, 'phase': phase, 'rules': 'release: signal AND fresh; incident: signal; recovery: NOT signal AND fresh. One unknown governing source per role.',
             'note': member.note if arm != 'broken' and phase != 'founder' else '', 'current_evidence': copy.deepcopy(current_evidence or []),
             'question': question, 'answer': answer if arm == 'interactive' else '',
             'cases': copy.deepcopy(cases or [])}
        # Only a founder/active predecessor may read its private context. A novice
        # sees transmitted evidence inside the note, never this history field.
        if phase in ('founder', 'answer') and arm == 'interactive': p['private_history'] = copy.deepcopy(member.private_history)
        if len(json.dumps(p).encode()) > REQUEST_BYTES: raise ValueError('packet_overflow')
        return p
    def replace(self, role, new_note):
        old = self.active(self.current[role]); read_note(role, new_note)
        ident = f'member-{len(self.events)+1}-{role}'
        note = read_note(role, new_note)
        new = Member(ident, role, new_note, copy.deepcopy(note['evidence']), old.identity)
        old.active = False; self.members[ident] = new; self.current[role] = ident
        self.events.append({'retired': old.identity, 'successor': ident, 'role': role,
                            'before_note_sha256': digest(old.note), 'after_note_sha256': digest(new_note),
                            'active_roster': dict(self.current)})
        return ident

def reference_round(inst, events=None):
    rows=[]
    for role in ROLES:
        member=inst.active(inst.current[role]); note=read_note(role,member.note)
        evidence=copy.deepcopy((events or {}).get(role) or note['evidence'])
        decision=evidence_decision(role,note['source'],evidence)
        rows.append({'role':role,**decision,'actions':[robust_action(role,c,decision['compatible']) for c in inst.world['roles'][role]['tests']]})
        inst.replace(role,make_note(role,note['source'],evidence))
    return rows

def score_response(role, cases, reference_evidence, previous_source, response, transmitted_evidence):
    """Evaluator only: retains model response; never supplies repaired policy to actors.

    transmitted_evidence is the exact union the actor could read in the current
    packet/teacher reply, not the evaluator's ancestral database.
    """
    result={'valid':False,'policy_correct':False,'note_supported':False,'actions_correct':0,
            'assigned_actions':len(cases),'qualified':False}
    if not isinstance(response,dict) or set(response)!={'note','actions'}:return result
    try:
        note=read_note(role,response['note']);actions=response['actions']
        if not isinstance(actions,list) or len(actions)!=len(cases):return result
        if any(not isinstance(a,dict) or set(a)!={'id','action'} or a['action'] not in ('allow','hold','defer') for a in actions):return result
        by_id={a['id']:a['action'] for a in actions}
        if len(by_id)!=len(actions) or set(by_id)!={c['id'] for c in cases}:return result
        result['valid']=True
        expected=evidence_decision(role,previous_source,reference_evidence)
        result['policy_correct']=all(note[k]==expected[k] for k in ('state','source','compatible'))
        visible={digest(r) for r in transmitted_evidence}
        result['note_supported']=bool(note['evidence']) and all(digest(r) in visible for r in note['evidence']) and compatible(role,note['evidence'])==note['compatible']
        result['actions_correct']=sum(by_id[c['id']]==robust_action(role,c,expected['compatible']) for c in cases)
        result['qualified']=result['policy_correct'] and result['note_supported'] and result['actions_correct']==len(cases)
    except (ValueError,TypeError,KeyError,json.JSONDecodeError):pass
    return result

def qualification_manifest():
    # Seeds are intentionally not generated/exposed in preparation.
    rows=[]
    for root in range(6):
        for role in ROLES:
            parent=f'T1-Q0-r{root}-{role}-founder'
            rows.append({'id':parent,'root':root,'role':role,'phase':'founder','depends_on':[]})
            previous=parent
            for phase in ('question','answer','commit'):
                ident=f'T1-Q0-r{root}-{role}-{phase}'
                rows.append({'id':ident,'root':root,'role':role,'phase':phase,'depends_on':[previous]}); previous=ident
    return {'stage':'T1-Q0','status':'offline_prepared_not_admitted','native_dispatch_enabled':False,
            'max_calls':72,'max_input_tokens':16000,'max_output_tokens':1024,'model_cap_usd':1.70,
            'infrastructure_cap_usd':.10,'total_cap_usd':1.80,'prior_exposure_usd':.9793100437,
            'original_cap_usd':5,'max_retries':0,'assignments':rows}

def reconcile(manifest, outcomes):
    ids={x['id'] for x in manifest['assignments']}
    if not set(outcomes)<=ids: raise ValueError('unknown_assignment')
    return {i:outcomes.get(i,'unstarted') for i in sorted(ids)}

def validate():
    stats={'evidence_type':'scripted_development_only','native_calls':0,'roots':18,'roles':54,
           'scenario_counts':{},'exact_founder_policies':0,'two_cycle_rosters_verified':0,'max_packet_bytes':0,
           'states':{},'actions':{},'actor_history_leaks':0}
    for stratum, scenario in enumerate(SCENARIOS):
        stats['scenario_counts'][scenario]=6
        for seed in range(11000+100*stratum,11006+100*stratum):
            world=make_world(seed,scenario);inst=Institution(world)
            for role in ROLES:
                data=world['roles'][role];assert compatible(role,data['history'])==[data['source']]
                stats['exact_founder_policies']+=1
                packet=inst.packet(role,'commit',cases=data['tests'])
                assert 'private_history' not in packet and 'source' not in packet and 'world' not in packet
                stats['max_packet_bytes']=max(stats['max_packet_bytes'],len(json.dumps(packet).encode()))
            reference_round(inst)
            assert not any(i.startswith('founder') for i in inst.current.values())
            first=set(inst.current.values());rows=reference_round(inst,world['events'])
            assert first.isdisjoint(inst.current.values());stats['two_cycle_rosters_verified']+=1
            for row in rows:
                stats['states'][row['state']]=stats['states'].get(row['state'],0)+1
                for a in row['actions']:stats['actions'][a]=stats['actions'].get(a,0)+1
    return stats

if __name__=='__main__':
    import argparse
    from pathlib import Path
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args()
    result=validate()
    if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
