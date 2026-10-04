"""Instrument of memory-handoff-qwen: root worlds, the source store, six memory states, four
handoff policies, the reference actor and the scorer. No network access, no study configuration
read at import time; every function takes the frozen `instrument` mapping of design.yaml.

Copied from discussion-dose bench_v3 (swarm-lab commit ce2c87fe), behaviour unchanged:
  digest, rng_for     discussion-dose/src/tasks.py
  resolve             discussion-dose/src/bench_v3/evidence.py   (function text identical)
  strict_json         discussion-dose/src/bench_v3/contracts.py  (function text identical)
  score               discussion-dose/src/bench_v3/scoring.py parent_score, same labels, with the
                      origin map taken from the visible records instead of a catalog, plus the
                      outcome classes of this study
  reference           bench_v3/evidence.py supported_parent over this study's packet
New here: the world generator, the source store, the states, the handoff policies and the rule
that turns a packet into resolver records (`visible_records`).

Truth separation: `handoff` builds what the successor reads from the predecessor's notes and the
source store only. The evaluator's truth is in `world` and `evaluator`; it is never copied into
a packet. A false original stays false when it is retrieved.
"""
import copy
import hashlib
import json
import random
import time

FAMILIES = ('capacity', 'total_cost', 'dependency')
FIELDS = {'capacity': ('power', 'access'), 'total_cost': ('base', 'freight', 'days'),
          'dependency': ('direct', 'backup', 'transfer')}
STATES = ('clean', 'misquote', 'stale', 'copies', 'contradiction', 'false_original')
POLICIES = ('raw', 'metadata', 'content', 'reset')
RANKS = {'primary': 2, 'secondary': 1}
PACKET_KEYS = ('task', 'inherited_memory', 'source_registry', 'retrieved_records')
QUESTION = 'Report the value of the exact fact key plus delta, or null if the fact is unresolved.'


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def rng_for(*parts):
    return random.Random(int(digest(parts)[:16], 16))


def resolve(key, records, policy):
    """Return supported alternatives after PUBLIC precedence, not a hidden truth test.

    Multiple copies of one origin never create independent support. A newer version
    supersedes only the same origin, then declared authority ranks apply across origins.
    Equal-rank contradictions are retained. Empty means missing/insufficient evidence.
    """
    relevant = [r for r in records if key in r['facts']]
    latest = {}
    for r in relevant:
        latest[r['origin']] = max(latest.get(r['origin'], -1), r['version'])
    relevant = [r for r in relevant if r['version'] == latest[r['origin']]]
    if not relevant:
        return {}
    rank = max(policy['ranks'][r['authority']] for r in relevant)
    relevant = [r for r in relevant if policy['ranks'][r['authority']] == rank]
    alternatives = {}
    for r in relevant:
        v = r['facts'][key]
        item = alternatives.setdefault(v, {'sources': set(), 'origins': set()})
        item['sources'].add(r['id'])
        item['origins'].add(r['origin'])
    return {v: {'sources': sorted(s['sources']), 'origins': sorted(s['origins'])}
            for v, s in sorted(alternatives.items())
            if len(s['origins']) >= policy.get('min_origins', 1)}


def strict_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key')
            result[key] = value
        return result
    def constant(_):
        raise ValueError('nonfinite JSON number')
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


# ------------------------------------------------------------------ worlds (evaluator side)

def letters(*parts, n=8):
    """A letters-only token: record and origin IDs carry no digits, so every number in a packet is a value."""
    v = int(digest(list(parts))[:20], 16); out = ''
    for _ in range(n):
        out += chr(97 + v % 26); v //= 26
    return out


def world(root, cfg):
    """The hidden world of one root: family, requested fact, truth T, false value F, delta and three
    other facts. Every number that can appear in a packet of this root is distinct from T, F,
    T + delta and F + delta, so an answer's class is never a coincidence of values."""
    if type(root) is not int or not 0 <= root < 10000:
        raise ValueError('root ids are integers below 10000')
    version = cfg['world_version']; family = FAMILIES[root % 3]; r = rng_for(version, root)
    option = r.choice(['A', 'B', 'C'])
    key = f'{option}.{cfg["target_field"][family]}'
    others = [f'{o}.{f}' for o in ('A', 'B', 'C') for f in FIELDS[family] if f'{o}.{f}' != key]
    while True:
        truth = r.randint(*cfg['truth_range'])
        false = truth + r.randint(*cfg['false_offset']) * r.choice((-1, 1))
        delta = r.randint(*cfg['delta_range'])
        keys = sorted(r.sample(others, cfg['distractor_notes']))
        values = [r.randint(*cfg['distractor_range']) for _ in keys]
        numbers = [truth, false, truth + delta, false + delta] + values + [v + delta for v in values]
        if len(set(numbers)) == len(numbers) and min(numbers) >= 10:
            break
    ident = lambda kind, slot: ('rec-' if kind == 'record' else 'org-') + letters(version, root, kind, slot)
    slots = ['a', 'a2', 'b', 'c2', 'c3'] + [f'd{i}' for i in range(len(keys))]
    w = {'root': root, 'family': family, 'key': key, 'truth': truth, 'false': false, 'delta': delta,
         'distractors': [{'key': k, 'value': v} for k, v in zip(keys, values)],
         'ids': {s: ident('record', s) for s in slots}, 'origins': {s: ident('origin', s) for s in ['a', 'b'] + slots[5:]},
         'target_position': r.randrange(len(keys) + 1), 'truth_first': bool(r.randrange(2)), 'version': version}
    if len(set(w['ids'].values()) | set(w['origins'].values())) != len(w['ids']) + len(w['origins']):
        raise ValueError('identifier collision')
    return w


def record(ident, origin, version, key, value):
    return {'id': ident, 'origin': origin, 'authority': 'primary', 'version': version, 'facts': {key: value}}


def note(key, value, sources):
    return {'key': key, 'value': value, 'sources': list(sources)}


def state_world(w, state, cfg):
    """One memory state of a root: (source store records, the predecessor's notes, min_origins).

    The three other notes and their records are identical in every state. Only the target note(s)
    and what the cited records really are differ."""
    if state not in STATES:
        raise ValueError('unknown memory state')
    ids, org, key, T, F = w['ids'], w['origins'], w['key'], w['truth'], w['false']
    A = lambda value: record(ids['a'], org['a'], 1, key, value)
    minimum = cfg['min_origins']['default']
    if state == 'clean':
        target, notes = [A(T)], [note(key, T, [ids['a']])]
    elif state == 'misquote':        # a genuine source that says T, quoted as F
        target, notes = [A(T)], [note(key, F, [ids['a']])]
    elif state == 'stale':           # version 1 said F and was current; version 2 of the same origin says T
        target, notes = [A(F), record(ids['a2'], org['a'], 2, key, T)], [note(key, F, [ids['a']])]
    elif state == 'copies':          # one origin, three records, cited as three reports
        assert cfg['copies'] == 3
        target = [A(F), record(ids['c2'], org['a'], 1, key, F), record(ids['c3'], org['a'], 1, key, F)]
        notes = [note(key, F, [ids['a'], ids['c2'], ids['c3']])]
        minimum = cfg['min_origins']['copies']
    elif state == 'contradiction':   # two primary origins, equal authority, different values
        target = [A(T), record(ids['b'], org['b'], 1, key, F)]
        notes = [note(key, T, [ids['a']]), note(key, F, [ids['b']])]
        if not w['truth_first']:
            notes.reverse()
    else:                            # false_original: the authoritative source itself says F
        target, notes = [A(F)], [note(key, F, [ids['a']])]
    others = [record(ids[f'd{i}'], org[f'd{i}'], 1, d['key'], d['value']) for i, d in enumerate(w['distractors'])]
    other_notes = [note(d['key'], d['value'], [ids[f'd{i}']]) for i, d in enumerate(w['distractors'])]
    p = w['target_position']
    return target + others, other_notes[:p] + notes + other_notes[p:], minimum


class SourceStore:
    """The records that exist in a state of a root. The handoff protocol reads it; the successor does not."""

    def __init__(self, records):
        self.records = {r['id']: r for r in records}
        if len(self.records) != len(records):
            raise ValueError('duplicate record id')

    def current_version(self, origin):
        return max(r['version'] for r in self.records.values() if r['origin'] == origin)

    def registry(self, ident):
        r = self.records[ident]
        return {'id': r['id'], 'origin': r['origin'], 'authority': r['authority'], 'version': r['version'],
                'current_version': self.current_version(r['origin'])}

    def fetch(self, ident):
        return copy.deepcopy(self.records[ident])

    def current(self, origin):
        """The record(s) of an origin at its current version."""
        version = self.current_version(origin)
        return [copy.deepcopy(r) for r in self.records.values() if r['origin'] == origin and r['version'] == version]


# ------------------------------------------------------------------ handoff policies

def handoff(w, state, policy, cfg):
    """What the successor reads, and the protocol's retrieval log.

    raw       the notes as the predecessor left them
    metadata  the notes plus the registry entry of every cited record (origin, authority, version,
              the origin's current version); no content
    content   as metadata, plus every cited record in full and, when a cited record is superseded,
              the current version of its origin. Whatever the store holds is returned as it is.
    reset     nothing inherited and nothing looked up; no replacement fact is supplied
    Returns (packet, log). The log's `seconds` is measured and is not part of any hash."""
    if policy not in POLICIES:
        raise ValueError('unknown handoff policy')
    records, notes, minimum = state_world(w, state, cfg)
    store = SourceStore(records)
    memory = [] if policy == 'reset' else copy.deepcopy(notes)
    registry, retrieved = [], []
    started = time.perf_counter()
    if policy in ('metadata', 'content'):
        for n in memory:
            for ident in n['sources']:
                if all(e['id'] != ident for e in registry):
                    registry.append(store.registry(ident))
    if policy == 'content':
        for n in memory:
            for ident in n['sources']:
                found = [store.fetch(ident)]
                if found[0]['version'] < store.current_version(found[0]['origin']):
                    found += store.current(found[0]['origin'])
                for r in found:
                    if all(x['id'] != r['id'] for x in retrieved):
                        retrieved.append(r)
    seconds = time.perf_counter() - started
    packet = {'task': {'key': w['key'], 'delta': w['delta'], 'min_origins': minimum, 'question': QUESTION},
              'inherited_memory': memory, 'source_registry': registry, 'retrieved_records': retrieved}
    log = {'registry_lookups': len(registry), 'records_retrieved': len(retrieved),
           'bytes': (len(lines(registry).encode()) if registry else 0) + (len(lines(retrieved).encode()) if retrieved else 0),
           'seconds': seconds}
    return packet, log


def lines(items):
    return '[\n' + ',\n'.join(json.dumps(x) for x in items) + '\n]' if items else '[]'


def render(packet):
    """The user message: one JSON object, one note, registry entry or record per line."""
    assert tuple(packet) == PACKET_KEYS
    return ('{\n"task": ' + json.dumps(packet['task']) + ',\n"inherited_memory": ' + lines(packet['inherited_memory'])
            + ',\n"source_registry": ' + lines(packet['source_registry'])
            + ',\n"retrieved_records": ' + lines(packet['retrieved_records']) + '\n}')


def visible_ids(packet):
    ids = [s for n in packet['inherited_memory'] for s in n['sources']]
    ids += [e['id'] for e in packet['source_registry']] + [r['id'] for r in packet['retrieved_records']]
    return sorted(set(ids))


def numbers(value):
    """Every integer in a packet (keys excluded). Used by the leak checks."""
    if isinstance(value, bool):
        return []
    if isinstance(value, int):
        return [value]
    if isinstance(value, dict):
        return [n for v in value.values() for n in numbers(v)]
    if isinstance(value, list):
        return [n for v in value for n in numbers(v)]
    return []


# ------------------------------------------------------------------ reference actor (visible evidence only)

def visible_records(packet, use_versions=True):
    """The successor's evidence as resolver records, by the public source policy:

    1. a cited record whose text is retrieved says what its text states, whatever the note claims;
       otherwise the note's claimed value stands for what the record says;
    2. origin, authority and version come from the registry entry or the record text; a record below
       its origin's current version is superseded and does not count;
    3. a cited ID with neither registry entry nor text is taken as presented: its own origin,
       primary and current.
    `use_versions=False` skips the current-version rule (a scripted control actor, never the reference)."""
    registry = {e['id']: e for e in packet['source_registry']}
    retrieved = {r['id']: r for r in packet['retrieved_records']}
    current = {}
    for e in registry.values():
        current[e['origin']] = max(current.get(e['origin'], 0), e['current_version'])
    records = []
    for n in packet['inherited_memory']:
        for ident in n['sources']:
            if ident in retrieved:
                continue
            meta = registry.get(ident) or {'origin': ident, 'authority': 'primary', 'version': 1}
            records.append({'id': ident, 'origin': meta['origin'], 'authority': meta['authority'],
                            'version': meta['version'], 'facts': {n['key']: n['value']}})
    for r in retrieved.values():
        records.append({k: copy.deepcopy(r[k]) for k in ('id', 'origin', 'authority', 'version', 'facts')})
    if use_versions:
        records = [r for r in records if r['version'] >= current.get(r['origin'], r['version'])]
    return records


def resolver_policy(packet):
    return {'ranks': RANKS, 'min_origins': packet['task']['min_origins']}


def reference(packet, use_versions=True):
    """The actor-evidence reference: bench_v3's supported_parent over this packet."""
    values = resolve(packet['task']['key'], visible_records(packet, use_versions), resolver_policy(packet))
    if len(values) != 1:
        return {'value': None, 'sources': []}
    value, support = next(iter(values.items()))
    return {'value': value + packet['task']['delta'], 'sources': support['sources']}


def control(packet, behavior):
    """Scripted actors with known behaviour. They validate the instrument; they are not model evidence."""
    key, delta = packet['task']['key'], packet['task']['delta']
    if behavior == 'reference':
        return reference(packet)
    if behavior == 'abstain':
        return {'value': None, 'sources': []}
    if behavior == 'version_blind':          # follows the policy except that it never checks versions
        return reference(packet, use_versions=False)
    if behavior == 'trust_memory':           # repeats the first note about the requested fact, whatever else is supplied
        n = next((n for n in packet['inherited_memory'] if n['key'] == key), None)
        return {'value': n['value'] + delta, 'sources': list(n['sources'])} if n else {'value': None, 'sources': []}
    if behavior == 'wrong_entity':           # answers with a note about another fact
        n = next((n for n in packet['inherited_memory'] if n['key'] != key), None)
        return {'value': n['value'] + delta, 'sources': list(n['sources'])} if n else {'value': None, 'sources': []}
    raise ValueError('unknown scripted control')


CONTROLS = ('reference', 'trust_memory', 'version_blind', 'abstain', 'wrong_entity')


# ------------------------------------------------------------------ answer format and scoring

def validate(obj, max_sources=16):
    """Structure only. A wrong, unsupported or badly cited answer with valid structure is a measured
    outcome, never a failed call."""
    if type(obj) is not dict or set(obj) != {'value', 'sources'}:
        raise ValueError('invalid response fields')
    value, sources = obj['value'], obj['sources']
    if value is not None and (type(value) is not int or abs(value) > 10000):
        raise ValueError('invalid integer')
    if type(sources) is not list or len(sources) > max_sources or any(type(s) is not str or not 0 < len(s) <= 64 for s in sources):
        raise ValueError('invalid sources')
    if len(sources) != len(set(sources)):
        raise ValueError('duplicate source')
    return {'value': value, 'sources': list(sources)}


def evaluator(w, state, policy, cfg):
    """Evaluator-only labels of one assignment. Never part of an actor input."""
    code = cfg['expected'][state][policy]
    hand = {'T': w['truth'] + w['delta'], 'F': w['false'] + w['delta'], 'N': None}[code]
    return {'truth_answer': w['truth'] + w['delta'],
            'false_answer': None if state == 'clean' else w['false'] + w['delta'],
            'expected_code': code, 'expected_value': hand}


def score(packet, answer, truth_answer, false_answer):
    """bench_v3 parent_score over this packet, plus this study's outcome class.

    `answer` None is an invalid or missing response: its harm is unidentified, not zero.
    supported        the value equals the reference and the citations are valid
    inherited_error  the value equals the false inherited value plus delta (the primary outcome)
    outcome          correct | abstain | inherited_error | other_wrong"""
    expected = reference(packet)
    records = visible_records(packet)
    policy = resolver_policy(packet)
    possibilities = resolve(packet['task']['key'], records, policy)
    if answer is None:
        return {'invalid': 1, 'outcome': None, 'correct': None, 'abstain': None, 'inherited_error': None, 'other_wrong': None,
                'supported': None, 'supported_wrong': None, 'unsupported_correct': None, 'unsupported_wrong': None,
                'correct_abstain': None, 'unnecessary_abstain': None, 'citation_valid': None,
                'answerable': int(expected['value'] is not None)}
    value = answer['value']; justified = value == expected['value']
    support_ids = set(expected['sources'])
    cited = set(answer['sources'])
    origins = {r['id']: r['origin'] for r in records}
    citation_valid = (not cited if value is None else bool(cited) and cited <= support_ids and
                      len({origins[s] for s in cited}) >= policy['min_origins'])
    correct = value is not None and value == truth_answer
    inherited = value is not None and false_answer is not None and value == false_answer
    outcome = 'abstain' if value is None else 'correct' if correct else 'inherited_error' if inherited else 'other_wrong'
    supported = justified and citation_valid
    return {'invalid': 0, 'outcome': outcome, 'correct': int(correct), 'abstain': int(value is None),
            'inherited_error': int(inherited), 'other_wrong': int(outcome == 'other_wrong'),
            'supported': int(supported),
            'supported_wrong': int(value is not None and supported and not correct),
            'unsupported_correct': int(value is not None and not supported and correct),
            'unsupported_wrong': int(value is not None and not supported and not correct),
            'correct_abstain': int(value is None and len(possibilities) != 1),
            'unnecessary_abstain': int(value is None and len(possibilities) == 1),
            'citation_valid': int(citation_valid), 'answerable': int(len(possibilities) == 1)}
