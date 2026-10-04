"""Event-sourced actor continuity. No networking; policies are injected by gated runner."""
import copy
from domain import (ARMS, commands, digest, history, instructions, oracle, rules,
                    score, tickets, validate_output)


def member(seed, scenario, slot, generation, parent=None):
    return {'id': f'{scenario}:{seed}:slot{slot}:g{generation}', 'slot': slot,
            'generation': generation, 'notebook': '', 'feedback': [],
            'onboarding': parent, 'note_hash': digest('')}


def archive(crew, step):
    entries = [{'member': m['id'], 'generation': m['generation'],
                'note_hash': m['note_hash'], 'notebook': m['notebook']} for m in crew]
    # Cap the actual text, retaining full ancestry independently in the event log.
    text = '\n'.join(m['id'] + ': ' + m['notebook'] for m in crew)[:2400]
    return {'id': digest({'step': step, 'entries': entries, 'text': text}),
            'step': step, 'entries': entries, 'text': text}


def initial(seed, scenario):
    crew = [member(seed, scenario, slot, 0) for slot in range(3)]
    return {'seed': seed, 'scenario': scenario, 'crew': crew, 'archive': None, 'founder_archive': None}


def advance(state, step, arm, policy, split='pilot'):
    assert arm in ARMS
    seed, scenario = state['seed'], state['scenario']
    replaced = None
    if 2 <= step <= 7:
        slot = (step - 2) % 3
        generation = 1 if step <= 4 else 2
        parent = state['founder_archive'] if arm == 'frozen' else state['archive']
        if arm == 'none': parent = None
        replaced = state['crew'][slot]['id']
        state['crew'][slot] = member(seed, scenario, slot, generation, copy.deepcopy(parent))
    cases = tickets(seed, scenario, step, split)
    docs = commands(scenario, step)
    before = copy.deepcopy(state['crew'])
    calls = []; member_votes = []
    for actor in state['crew']:
        observation = {'step': step, 'role': actor['slot'], 'cases': cases, 'commands': docs,
                       'private_notebook': actor['notebook'], 'feedback': actor['feedback']}
        if step == 0:
            observation['history'] = history(seed, scenario)
        if actor['onboarding'] is not None:
            observation['inherited_record'] = actor['onboarding']['text']
        request = {'instructions': instructions(scenario, arm if step >= 2 else 'rolling'),
                   'observation': observation}
        result = policy.complete(request)
        value = result.get('value')
        votes, errors = validate_output(value, cases, docs)
        member_votes.append(votes)
        calls.append({'member': actor['id'], 'request': request, 'request_hash': digest(request),
                      'result': result, 'validation_errors': errors, 'parsed_votes': votes})
        if isinstance(value, dict) and isinstance(value.get('notebook'), str) and len(value['notebook']) <= 700:
            actor['notebook'] = value['notebook']
        actor['note_hash'] = digest(actor['notebook'])
        actor['feedback'] = [{'observation': c, 'action': votes.get(c['id']),
                              'accepted_action': oracle(c, scenario, rules(seed, scenario, step))} for c in cases]
        actor['onboarding'] = None
    state['archive'] = archive(state['crew'], step)
    if step == 1: state['founder_archive'] = copy.deepcopy(state['archive'])
    event = {'kind': 'trajectory_step', 'scenario': scenario, 'seed': seed, 'arm': arm,
             'step': step, 'replaced': replaced, 'crew_before': before,
             'crew_after': copy.deepcopy(state['crew']), 'archive': copy.deepcopy(state['archive']),
             'calls': calls, 'cases': cases, 'commands': docs,
             'evaluator': {'rule': rules(seed, scenario, step), 'stale_rule': rules(seed, scenario, 0)},
             'scores': score(cases, scenario, rules(seed, scenario, step), rules(seed, scenario, 0), member_votes)}
    return event


def acquire(seed, scenario, policy, emit):
    state = initial(seed, scenario)
    for step in (0, 1): emit(advance(state, step, 'rolling', policy))
    return state


def continuation(checkpoint, arm, policy, emit):
    state = copy.deepcopy(checkpoint)
    for step in range(2, 10): emit(advance(state, step, arm, policy))
    return state
