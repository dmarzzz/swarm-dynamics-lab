"""Per-agent context builder: the only code that writes text a model will read.

It receives the deadline, the display mapping, public records and already-published board
snapshots. It never receives the truth, the world's regime metadata or another agent's vault
entry. Every context lists the sources it used; build() refuses a source outside the allowlist
for that arm and phase. An agent is one conversation: earlier turns are replayed verbatim.
"""
import json
import prompts
import parse

# Sources a context may draw on, by phase and arm (plan sections 2 and 3).
ACCESS = {
    'initial': {arm: {'task', 'own_records'} for arm in ('shared', 'prepare')},
    'discussion': {
        'private': {'task', 'own_records', 'own_initial', 'facts_packet'},
        'never': {'task', 'own_records', 'own_initial', 'facts_packet'},
        'prepare': {'task', 'own_records', 'own_initial', 'facts_packet'},
        'public': {'task', 'own_records', 'own_initial', 'facts_packet', 'initial_votes'},
        'vote': {'task', 'own_records', 'own_initial'},
    },
}
ACCESS['final'] = {arm: set(sources) | {'own_discussion', 'discussion_board'}
                   for arm, sources in ACCESS['discussion'].items() if arm != 'vote'}
ACCESS['final']['vote'] = set(ACCESS['discussion']['vote']) | {'own_discussion'}
ACCESS['qualification'] = {'single': {'task', 'all_records'}}

UNITS = {'cost': 'units', 'delivery': 'days'}


class AccessError(Exception):
    pass


def one_line(text):
    return ' '.join(str(text).split())


class Renderer:
    def __init__(self, deadline, label_of, evidence_id):
        self.deadline, self.label_of, self.evidence_id = deadline, dict(label_of), dict(evidence_id)

    def record_lines(self, records):
        rows = sorted(records, key=lambda r: self.evidence_id[r['key']])
        return '\n'.join(prompts.RECORD_LINE.format(
            id=self.evidence_id[r['key']], day=r['day'], source=r['source'], label=self.label_of[r['supplier']],
            field=r['field'], value=r['value'], unit=UNITS[r['field']]) for r in rows)

    def task_block(self, records):
        return (prompts.DEADLINE.format(deadline=self.deadline) + '\n\n' + prompts.OWN_RECORDS + '\n'
                + self.record_lines(records))


def _you(agent, me):
    return ' (you)' if agent == me else ''


def votes_block(votes, me):
    lines = []
    for vote in votes:
        if vote.get('unavailable'):
            lines.append(prompts.VOTE_UNAVAILABLE.format(n=vote['agent'] + 1, you=_you(vote['agent'], me)))
        else:
            lines.append(prompts.VOTE_LINE.format(n=vote['agent'] + 1, you=_you(vote['agent'], me),
                                                  choice=vote['choice'], confidence=json.dumps(vote['confidence'])))
    return '\n'.join(lines)


def board_block(messages, me):
    lines = [prompts.BOARD_HEADER]
    for m in messages:
        if m.get('unavailable'):
            lines.append(prompts.BOARD_UNAVAILABLE.format(n=m['agent'] + 1, you=_you(m['agent'], me)))
        else:
            lines.append(prompts.BOARD_LINE.format(
                n=m['agent'] + 1, you=_you(m['agent'], me), recommendation=m['recommendation'],
                cites=', '.join(m['evidence_ids']) or 'none', message=one_line(m['message'])))
    return '\n'.join(lines)


def build(phase, arm, agent, renderer, own_records, own_initial=None, own_discussion=None,
          facts=None, initial_votes=None, discussion=None, final_kind=None, replay=False):
    """Return {'system', 'messages', 'schema', 'sources'} for one call.

    phase: initial | discussion | final. arm for the shared first pass is 'shared'.
    own_initial / own_discussion: the agent's own earlier raw outputs (strings).
    facts / initial_votes / discussion: published board snapshot contents, or None.
    """
    sources = {'task', 'own_records'}
    if phase == 'initial':
        ask, fields, schema = ((prompts.PREPARE_ASK, prompts.FIELDS_PREPARE, 'prepare') if arm == 'prepare'
                               else (prompts.INITIAL_ASK, prompts.FIELDS_INITIAL, 'initial'))
        first = renderer.task_block(own_records) + '\n\n' + ask + '\n' + fields
        messages = [{'role': 'user', 'content': first}]
    else:
        if own_initial is None:
            raise AccessError('a later phase needs the agent\'s own first-pass output')
        sources.add('own_initial')
        first_arm = 'prepare' if arm == 'prepare' else 'shared'
        first = build('initial', first_arm, agent, renderer, own_records)['messages'][0]
        messages = [first, {'role': 'assistant', 'content': own_initial}]
        if arm == 'vote':
            if facts is not None or initial_votes is not None or discussion is not None:
                raise AccessError('VOTE receives no peer facts, votes or messages')
            second = '\n\n'.join([prompts.VOTE_NO_DISCUSSION,
                                  prompts.VOTE_RECORDS + '\n' + renderer.record_lines(own_records),
                                  prompts.REVISION['vote'],
                                  prompts.VOTE_REVIEW_ASK + '\n' + prompts.FIELDS_DISCUSSION])
        else:
            if facts is None:
                raise AccessError('communicating arms discuss after the factual release')
            sources.add('facts_packet')
            visibility = (prompts.VISIBILITY_REPLAY if replay else prompts.VISIBILITY)[arm]
            if arm == 'public':
                if initial_votes is None:
                    raise AccessError('PUBLIC needs the published first choices')
                sources.add('initial_votes')
                visibility += '\n' + votes_block(initial_votes, agent)
            elif initial_votes is not None:
                raise AccessError('only PUBLIC may see first choices before discussion')
            second = '\n\n'.join([prompts.PACKET_HEADER + '\n' + renderer.record_lines(facts), visibility,
                                  prompts.REVISION[arm], prompts.DISCUSSION_ASK + '\n' + prompts.FIELDS_DISCUSSION])
        messages.append({'role': 'user', 'content': second})
        schema = 'discussion'
        if phase == 'final':
            if own_discussion is None:
                raise AccessError('a final answer needs the agent\'s own discussion output')
            sources.add('own_discussion')
            messages.append({'role': 'assistant', 'content': own_discussion})
            if arm == 'vote':
                if discussion is not None:
                    raise AccessError('VOTE receives no peer messages')
                board = prompts.VOTE_NO_MESSAGES
            else:
                if discussion is None:
                    raise AccessError('communicating arms answer after the frozen discussion board')
                sources.add('discussion_board')
                board = board_block(discussion, agent)
            ask = {'public': prompts.FINAL_PUBLIC, 'private': prompts.FINAL_PRIVATE}[final_kind]
            messages.append({'role': 'user', 'content': board + '\n\n' + ask + '\n' + prompts.FIELDS_FINAL})
            schema = 'final'
        elif phase != 'discussion':
            raise ValueError('unknown phase: %r' % (phase,))
    allowed = ACCESS[phase][arm]
    if not sources <= allowed:
        raise AccessError('context uses sources outside the allowlist: %s' % sorted(sources - allowed))
    return {'system': prompts.SYSTEM, 'messages': messages, 'schema': schema, 'sources': sorted(sources)}


def build_qualification(renderer, records):
    text = (prompts.DEADLINE.format(deadline=renderer.deadline) + '\n\nRecords:\n' + renderer.record_lines(records)
            + '\n\n' + prompts.QUALIFICATION_ASK + '\n' + prompts.FIELDS_QUALIFICATION)
    return {'system': prompts.SYSTEM_SINGLE, 'messages': [{'role': 'user', 'content': text}],
            'schema': 'qualification', 'sources': ['all_records', 'task']}


def request_bytes(context):
    """Bytes of everything the provider will read: system, messages and the output schema."""
    body = {'system': context['system'], 'messages': context['messages'],
            'schema': parse.SCHEMAS[context['schema']]}
    return len(json.dumps(body, sort_keys=True).encode())


def text_of(context):
    return context['system'] + '\n' + '\n'.join(m['content'] for m in context['messages'])
