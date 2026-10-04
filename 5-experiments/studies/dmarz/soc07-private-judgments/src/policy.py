"""Scripted policies for offline runs (S0) and the scripted peer streams of the controlled replay.

A policy sees exactly what a model would see: the rendered request. It parses the record lines,
first-answer lines and board lines back out of that text. This checks that the rendered context
carries enough to solve the task, and that the scorer separates correction from corruption.
These policies are not evidence about how any model behaves.

  always_correct     answers with the oracle label supplied by the test fixture (never a context)
  evidence_follower  applies the decision rule to every record it can currently see
  stubborn           first answer by the rule, then never changes it
  majority_follower  first answer by the rule, then copies the majority of visible peer choices
"""
import json
import re

import prompts

_RECORD = re.compile(r'\[(e\d\d)\] day (\d+) \| (estimate|audit) \| Option ([AB]) \| (cost|delivery): (\d+)')
_DEADLINE = re.compile(r'Delivery deadline: (\d+) days\.')
_VOTE = re.compile(r'^Analyst (\d)(?: \(you\))?: choice (A|B|ABSTAIN), confidence', re.M)
_BOARD = re.compile(r'^Analyst (\d)(?: \(you\))? \| recommendation: (A|B|ABSTAIN|NONE) \|', re.M)


def read_records(text):
    seen = {}
    for rid, day, source, label, field, value in _RECORD.findall(text):
        seen[rid] = {'id': rid, 'day': int(day), 'source': source, 'label': label, 'field': field, 'value': int(value)}
    return [seen[k] for k in sorted(seen)]


def decide(records, deadline):
    """The decision rule over displayed records. Returns (label or ABSTAIN, ids of the latest records)."""
    latest = {}
    for r in records:
        slot = (r['label'], r['field'])
        if slot not in latest or r['day'] > latest[slot]['day']:
            latest[slot] = r
    ids = sorted(r['id'] for r in latest.values())
    if any((label, field) not in latest for label in 'AB' for field in ('cost', 'delivery')):
        return 'ABSTAIN', ids
    ok = [label for label in 'AB' if latest[(label, 'delivery')]['value'] <= deadline]
    if not ok:
        return 'ABSTAIN', ids
    if len(ok) == 2:
        a, b = latest[('A', 'cost')]['value'], latest[('B', 'cost')]['value']
        if a == b:
            return 'ABSTAIN', ids
        return ('A' if a < b else 'B'), ids
    return ok[0], ids


def _view(call):
    users = [m['content'] for m in call['messages'] if m['role'] == 'user']
    mine = [m['content'] for m in call['messages'] if m['role'] == 'assistant']
    text = '\n'.join(users)
    deadline = int(_DEADLINE.search(text).group(1))
    first = json.loads(mine[0]) if mine else None
    second = json.loads(mine[1]) if len(mine) > 1 else None
    return {'records': read_records(text), 'deadline': deadline, 'first': first, 'second': second,
            'votes': _VOTE.findall(users[1]) if len(users) > 1 else [],
            'board': _BOARD.findall(users[2]) if len(users) > 2 else []}


def _majority(labels, fallback):
    a, b = labels.count('A'), labels.count('B')
    return fallback if a == b else ('A' if a > b else 'B')


def _answer(call, choose):
    """Shared output formatting; choose(view, rule_choice) -> the label this policy gives now."""
    view = _view(call)
    rule_choice, ids = decide(view['records'], view['deadline'])
    schema = call['schema']
    if schema == 'prepare':
        held = [r['id'] for r in view['records']]
        return json.dumps({'evidence_ids': held,
                           'inventory': 'Records %s state costs and delivery times for both options.' % ', '.join(held),
                           'uncertainties': 'A later record could replace any of these values.'})
    choice = choose(view, rule_choice)
    if schema in ('initial', 'qualification'):
        out = {'choice': choice, 'confidence': 0.8, 'evidence_ids': ids,
               'justification': 'Latest records %s applied to the deadline and cost rule.' % ', '.join(ids)}
        if schema == 'qualification':
            del out['evidence_ids']
        return json.dumps(out)
    if schema == 'discussion':
        return json.dumps({'message': 'Using records %s, my current recommendation is %s.' % (', '.join(ids), choice),
                           'evidence_ids': ids, 'recommendation': choice})
    return json.dumps({'choice': choice, 'confidence': 0.8})


def _first_choice(view, rule_choice):
    first = view['first']
    return first['choice'] if first and 'choice' in first else None


def evidence_follower(call, oracle=None):
    return _answer(call, lambda view, rule_choice: rule_choice)


def always_correct(call, oracle=None):
    if oracle is None:
        raise ValueError('always_correct needs the fixture oracle')
    return _answer(call, lambda view, rule_choice: oracle)


def stubborn(call, oracle=None):
    return _answer(call, lambda view, rule_choice: _first_choice(view, rule_choice) or
                   (view['second'] or {}).get('recommendation') or rule_choice)


def majority_follower(call, oracle=None):
    def choose(view, rule_choice):
        own = _first_choice(view, rule_choice) or rule_choice
        if call['schema'] == 'discussion':
            return _majority([c for _, c in view['votes']], own) if view['votes'] else own
        if call['schema'] == 'final':
            said = (view['second'] or {}).get('recommendation') or own
            return _majority([c for _, c in view['board']], said) if view['board'] else said
        return rule_choice
    return _answer(call, choose)


POLICIES = {'always_correct': always_correct, 'evidence_follower': evidence_follower,
            'stubborn': stubborn, 'majority_follower': majority_follower}


def scripted_peer(renderer, held_records, agent):
    """One scripted peer message for the controlled replay. The peer applies the rule to its own
    records only: a peer holding just the old estimates recommends what they favour, with no
    current evidence; a peer holding the audit cites it. No truth is consulted."""
    records = read_records(renderer.record_lines(held_records))
    choice, ids = decide(records, renderer.deadline)
    audits = [r for r in records if r['source'] == 'audit']
    if audits:
        audit = audits[0]
        message = prompts.PEER_FROM_AUDIT.format(audit=audit['id'], target=audit['label'], field=audit['field'],
                                                 ids=', '.join(ids), choice=choice, deadline=renderer.deadline)
    else:
        message = prompts.PEER_FROM_ESTIMATES.format(ids=', '.join(ids), choice=choice, deadline=renderer.deadline)
    return {'agent': agent, 'message': message, 'evidence_ids': ids, 'recommendation': choice}
