"""D2 only: canonical full decisions and single-option feasibility checks.

Seventy-two assigned calls: 24 fixed items (6 canonical decisions, 18 atomic
feasibility checks on open worlds 20001-20006) for each of three models. Claude
Opus 5.5 is the model under test; Sonnet 4.6 and Haiku 4.5 are the matched
comparison arms defined by D2-PLAN.md. No retries, no fallback, no successor.
One further Opus call, a compatibility probe on a synthetic request outside the
24 items, precedes the batch; it is recorded and never counted as a result.

Nothing here polls a queue, provisions a server or opens a holdout. The operator
controls credentials, the hub run, the claim and the service lifecycle. All files
this CLI writes are private run artifacts until sanitized.
"""
import argparse
import copy
from collections import Counter
from datetime import datetime, timezone, timedelta
import fcntl
import hashlib
from itertools import permutations
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

from tasks import digest, feasible, rng_for
from providers import Anthropic, ProviderFailure
from bench_v3.contracts import strict_json
from bench_v3.evidence import resolve
from bench_v3.failures import safe_failure, REASONS
from bench_v3.journal import Journal, read_events
from bench_v3.scoring import reference_winner
from bench_v3.worlds import make_case

ROOT = Path(__file__).resolve().parent
NOTES = ROOT.parent
REPO = ROOT.parents[4]
D2 = NOTES / 'benchmark-v3/d2'
FACTS = D2 / 'canonical-facts.json'
PLAN_DOC = D2 / 'PLAN.md'
SETUP_DOC = D2 / 'SETUP.md'
BASE_PLAN = NOTES / 'benchmark-v3/D2-PLAN.md'
PRE_DOC = NOTES / 'reviews/v3-d2-a1-pre.md'
Q0_RECEIPT = NOTES / 'benchmark-v3/results/v3-q0-a1/analysis.json'
Q0_SELECTION = NOTES / 'benchmark-v3/next-run-planning-evidence.json'

ATTEMPT = 'v3-d2-a1'
PARENT = 'v3-d1-a1'
EXPERIMENT = 'discussion-dose-v3'
VERSION = 'd2-canonical-atomic-v1'
ORDER_SEED = 'd2-order-v1'
SERVER = 'sim-dmarz-3'
CLAIM = 'dmarz-discussion-v3-d2'
WORLDS = tuple(range(20001, 20007))
OPTIONS = ('A', 'B', 'C')
BUDGET_CAP_USD = 5
ASSIGNED = 72
PER_MODEL = 24

OPUS = 'claude-opus-5-5'
SONNET = 'claude-sonnet-4-6'
HAIKU = 'claude-haiku-4-5-20251001'
# Report order: the model under test first, then the comparison arms.
MODELS = (OPUS, SONNET, HAIKU)
# Prices are USD per million tokens from the official pricing page, read
# 2026-10-04. Opus 5.5 rejects non-default sampling parameters and cannot turn
# thinking off, so its arm omits temperature, sets effort explicitly and has
# room for thinking inside max_tokens. See benchmark-v3/d2/PLAN.md.
SETTINGS = {
    OPUS: {'role': 'model_under_test', 'input_usd_per_million': 4, 'output_usd_per_million': 20,
           'max_output_tokens': 4000, 'temperature': None, 'effort': 'medium',
           'thinking': 'adaptive_always_on_field_omitted'},
    SONNET: {'role': 'comparison_arm', 'input_usd_per_million': 3, 'output_usd_per_million': 15,
             'max_output_tokens': 2000, 'temperature': 0, 'effort': None,
             'thinking': 'disabled_by_omission'},
    HAIKU: {'role': 'comparison_arm', 'input_usd_per_million': 1, 'output_usd_per_million': 5,
            'max_output_tokens': 2000, 'temperature': 0, 'effort': None,
            'thinking': 'disabled_by_omission'},
}
MAX_INPUT_BYTES = 60000
TIMEOUT = 120
DEADLINE_SECONDS = 3600
REFUSAL_CATEGORIES = frozenset(('cyber', 'bio', 'reasoning_extraction', 'frontier_llm', 'general_harms'))
# One synthetic request for the Opus compatibility probe. It is hand-written, is
# not generated from any world ID and is not one of the 24 experimental items.
PROBE_REQUEST = {'phase': 'd2_feasibility', 'context': {
    'task': {'family': 'capacity',
             'instructions': 'Select the only site with power >= 10 units AND access time <= 5 hours. '
                             'If multiple sites qualify, maximize power. Break objective ties alphabetically.',
             'rules': {'access_max': 5, 'power_min': 10}},
    'option': 'A', 'facts': {'A.access': 4, 'A.power': 12}}}

SYSTEM = '''You are an honest agent working on a fictional finite decision task. The facts in the request are the complete and correct facts for this task. There is no other evidence, no retrieval and no hidden answer. Apply the stated instructions and rules exactly as written.
d2_decision: the request gives the task instructions, the rules, the options A, B and C, and every fact for every option. Return {"vote": "A|B|C|ABSTAIN"}. Vote for the option that the instructions select. Use ABSTAIN only if the instructions select no option.
d2_feasibility: the request gives the same instructions and rules, and the facts for one option only. Return {"feasible": true or false}. Answer true if that option meets every requirement the instructions place on an option that may be selected, and false otherwise. Judge this option alone; the objective and the tie-break do not apply.
The output must match the JSON schema exactly.'''

FORBIDDEN = frozenset(('truth', 'truth_answer', 'expected', 'expected_supported', 'false_value', 'roles',
                       'target', 'target_key', 'stratum', 'allocation', 'attack_id', 'evidence_allowed_choices',
                       'gold', 'winner', 'feasible', 'correct', 'label', 'vote', 'answer', 'documents',
                       'catalog', 'domains', 'reports', 'claims'))


def read(path):
    return strict_json(Path(path).read_text(encoding='utf-8'))


def fingerprint(path):
    raw = Path(path).read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def sync_dir(path):
    fd = os.open(str(path), os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)


def write_new(path, data):
    """Exclusive, fsynced creation including the directory entry."""
    path = Path(path)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(data, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    sync_dir(path.parent)


# ---------------------------------------------------------------- worlds and items

def world_case(world):
    if world not in WORLDS: raise ValueError('D2 uses only open development worlds 20001-20006')
    return make_case(world, 'resolvable' if world <= 20003 else 'ambiguous')


def build_table():
    """Values only: no winner, feasibility label, attack target or model answer."""
    rows = []
    for world in WORLDS:
        case = world_case(world); task = case['task']
        rows.append({'world': world, 'family': task['family'], 'instructions': task['instructions'],
                     'rules': copy.deepcopy(task['rules']), 'options': list(task['options']),
                     'facts': {k: case['truth'][k] for k in sorted(case['truth'])}})
    return {'schema': 'd2-canonical-facts-v1', 'worlds': rows}


def canonical_table():
    table = read(FACTS)
    if table != build_table(): raise ValueError('committed canonical fact table differs from the world generator')
    reject_gold(table)
    return table


def check_q0(q0):
    """Compare every canonical value with the retained clean Q0 full-evidence requests."""
    q0 = Path(q0); receipt = read(Q0_RECEIPT)['verified_remote_files']
    for name in ('manifest.json', 'events.jsonl'):
        if fingerprint(q0 / name) != receipt[name]: raise ValueError('retained Q0 bytes differ from the published audit receipt')
    selected = {int(s['label'].split(':')[0]): s for s in read(Q0_SELECTION)['selected'] if s['group'] == 'diagnostic'}
    if sorted(selected) != list(WORLDS) or any(s['label'] != f'{w}:0:diagnostic' for w, s in selected.items()):
        raise ValueError('clean full-evidence selection mismatch')
    starts = {e['call_id']: e for e in read_events(q0 / 'events.jsonl') if e['kind'] == 'call_start'}
    checked = {}; values = 0
    for row in canonical_table()['worlds']:
        saved = selected[row['world']]; request = starts[saved['q0_call_id']]['request']
        if digest(request) != saved['request_sha256'] or request['phase'] != 'diagnostic':
            raise ValueError('retained clean request differs from the published selection')
        task = request['context']['task']
        if any(task[k] != row[k] for k in ('family', 'instructions', 'rules', 'options')):
            raise ValueError('retained public rule differs from the canonical table')
        if sorted(task['fact_keys']) != sorted(row['facts']): raise ValueError('retained fact keys differ')
        for key, value in row['facts'].items():
            supported = resolve(key, request['context']['documents'], task['policy'])
            if list(supported) != [value]: raise ValueError('canonical value differs from the retained clean record')
            values += 1
        checked[str(row['world'])] = saved['request_sha256']
    return {'q0_manifest': fingerprint(q0 / 'manifest.json'), 'q0_events': fingerprint(q0 / 'events.jsonl'),
            'clean_requests': checked, 'values_checked': values}


def reject_gold(value):
    if type(value) is dict:
        if FORBIDDEN.intersection(value): raise ValueError('evaluator or prior-output field in actor input')
        for child in value.values(): reject_gold(child)
    elif type(value) is list:
        for child in value: reject_gold(child)


def option_facts(facts, option):
    return {k: v for k, v in facts.items() if k.startswith(option + '.')}


def items():
    """Twenty-four actor requests. Evaluator labels never enter these objects."""
    rows = []
    for row in canonical_table()['worlds']:
        world = row['world']
        rule = {'family': row['family'], 'instructions': row['instructions'], 'rules': row['rules']}
        rows.append({'item': f'dec-{world}', 'probe': 'decision', 'world': world, 'option': None,
                     'request': {'phase': 'd2_decision',
                                 'context': {'task': {**rule, 'options': row['options']}, 'facts': row['facts']}}})
        for option in row['options']:
            rows.append({'item': f'atom-{world}-{option}', 'probe': 'feasibility', 'world': world, 'option': option,
                         'request': {'phase': 'd2_feasibility',
                                     'context': {'task': rule, 'option': option,
                                                 'facts': option_facts(row['facts'], option)}}})
    for row in rows:
        reject_gold(row['request'])
        if len(json.dumps(row['request'], sort_keys=True).encode()) > MAX_INPUT_BYTES: raise ValueError('input exceeds byte limit')
    if Counter(r['probe'] for r in rows) != {'decision': 6, 'feasibility': 18}: raise ValueError('item allocation mismatch')
    return rows


def text_predicate(instructions, values):
    """Independent check that reads thresholds from the public sentence, not from rules."""
    site = re.search(r'power >= (\d+) units AND access time <= (\d+) hours', instructions)
    ship = re.search(r'base \+ freight <= (\d+) units AND days <= (\d+)\.', instructions)
    station = re.search(r'direct >= (\d+) OR \(backup = 1 AND transfer <= (\d+)\)', instructions)
    if site:
        return not (values['power'] < int(site.group(1))) and not (values['access'] > int(site.group(2)))
    if ship:
        return int(ship.group(1)) - values['base'] - values['freight'] >= 0 and int(ship.group(2)) - values['days'] >= 0
    if station:
        return values['direct'] - int(station.group(1)) >= 0 or (values['backup'] == 1 and int(station.group(2)) - values['transfer'] >= 0)
    raise ValueError('unrecognized public rule sentence')


def raw_objective(family, values):
    """Lower wins. Defined for every option so a predicted-feasible set can be ranked."""
    if family == 'capacity': return -values['power']
    if family == 'total_cost': return values['base'] + values['freight']
    if family == 'dependency': return values['transfer']
    raise ValueError('unknown family')


def gold():
    """Evaluator-only labels, cross-checked by three separate implementations."""
    labels = {}
    for row in canonical_table()['worlds']:
        case = world_case(row['world']); task = case['task']
        option_labels = {}
        for option in OPTIONS:
            values = {k.split('.')[1]: v for k, v in option_facts(row['facts'], option).items()}
            label = feasible(row['family'], values, row['rules'])
            if label != text_predicate(row['instructions'], values): raise ValueError('predicate implementations disagree')
            option_labels[option] = bool(label)
        winner = reference_winner(task, case['truth'])
        if [o for o in OPTIONS if option_labels[o]] != [winner]: raise ValueError('each D2 world must have exactly one feasible option')
        labels[row['world']] = {'winner': winner, 'feasible': option_labels, 'family': row['family']}
    if sum(v for w in labels.values() for v in w['feasible'].values()) != 6: raise ValueError('expected six feasible options')
    return labels


# ---------------------------------------------------------------- response contract

def schema(phase, context=None):
    def obj(properties):
        return {'type': 'object', 'properties': properties, 'required': list(properties), 'additionalProperties': False}
    if phase == 'd2_decision': return obj({'vote': {'type': 'string', 'enum': ['A', 'B', 'C', 'ABSTAIN']}})
    if phase == 'd2_feasibility': return obj({'feasible': {'type': 'boolean'}})
    raise ValueError('unknown phase')


def validate(response, phase):
    """Syntax only. A wrong vote or boolean is a measured outcome, never an invalid one."""
    if phase == 'd2_decision':
        if type(response) is not dict or set(response) != {'vote'} or response['vote'] not in ('A', 'B', 'C', 'ABSTAIN'):
            raise ValueError('invalid decision response')
    elif phase == 'd2_feasibility':
        if type(response) is not dict or set(response) != {'feasible'} or type(response['feasible']) is not bool:
            raise ValueError('invalid feasibility response')
    else: raise ValueError('unknown phase')
    return response


# ---------------------------------------------------------------- provider boundary

def body(request, model):
    """Expected native serialization, written independently of the adapter classes."""
    s = SETTINGS[model]
    fmt = {'type': 'json_schema', 'schema': schema(request['phase'], request['context'])}
    payload = {'model': model, 'system': SYSTEM,
               'messages': [{'role': 'user', 'content': json.dumps(request, sort_keys=True)}],
               'max_tokens': s['max_output_tokens']}
    if model == OPUS:
        payload['output_config'] = {'effort': s['effort'], 'format': fmt}
    else:
        payload['temperature'] = 0
        payload['output_config'] = {'format': fmt}
    return payload


class OpusAdaptive(Anthropic):
    """Opus 5.5 arm: no sampling parameter, explicit effort, thinking always on.

    The response may begin with thinking blocks whose text is empty by default;
    exactly one text block must follow and only that block is parsed. A refusal
    stop reason is its own failure category. No fallback model and no retry.
    """
    effort = SETTINGS[OPUS]['effort']
    last_stop_reason = None
    last_refusal_category = None

    def request_body(self, request):
        return {'model': self.model, 'system': self.system_prompt,
                'messages': [{'role': 'user', 'content': json.dumps(request, sort_keys=True)}],
                'max_tokens': self.max_output_tokens,
                'output_config': {'effort': self.effort,
                                  'format': {'type': 'json_schema', 'schema': self.response_schema(request['phase'], request['context'])}}}

    def complete(self, request):
        self.last_usage = {}; self.last_response_text = None; self.last_model = None
        self.last_stop_reason = None; self.last_refusal_category = None
        if self.calls >= self.max_calls: raise ProviderFailure('call budget exhausted', 'provider_local_limit')
        content = json.dumps(request, sort_keys=True)
        if len(content.encode()) > self.max_input_bytes: raise ProviderFailure('input byte budget exceeded', 'provider_local_limit')
        encoded = json.dumps(self.request_body(request)).encode()
        reservation = ((len(encoded) + 512) * self.input_rate + self.max_output_tokens * self.output_rate) / 1_000_000
        if self.reserved_usd + reservation > self.max_cost_usd: raise ProviderFailure('dollar reservation exhausted', 'provider_local_limit')
        headers = {'Content-Type': 'application/json', 'x-api-key': self.key, 'anthropic-version': '2023-06-01'}
        if self.workspace: headers['anthropic-workspace-id'] = self.workspace
        req = urllib.request.Request(self.base + '/messages', data=encoded, headers=headers)
        self.reserved_usd += reservation; self.calls += 1; self.usage_missing_calls += 1
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r: raw = r.read(2_000_001)
            if len(raw) > 2_000_000: raise ProviderFailure('response too large')
            response = json.loads(raw); usage = response.get('usage', {})
            self.last_model = response.get('model')
            self.last_usage = {k: v for k, v in usage.items()
                               if k in ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens')
                               and type(v) is int and v >= 0}
            if all(k in self.last_usage for k in ('input_tokens', 'output_tokens')):
                if any(self.last_usage.get(k, 0) for k in ('cache_creation_input_tokens', 'cache_read_input_tokens')):
                    raise ProviderFailure('unexpected cached usage; accounting requires review', 'provider_accounting_error')
                # Thinking tokens are billed as output tokens and are already inside output_tokens.
                self.actual_cost_usd += (self.last_usage['input_tokens'] * self.input_rate + self.last_usage['output_tokens'] * self.output_rate) / 1_000_000
                self.input_tokens += self.last_usage['input_tokens']; self.output_tokens += self.last_usage['output_tokens']
                self.usage_missing_calls -= 1
            stop = response.get('stop_reason')
            self.last_stop_reason = stop if stop in ('end_turn', 'max_tokens', 'refusal', 'stop_sequence', 'tool_use', 'pause_turn') else 'other'
            if stop == 'refusal':
                details = response.get('stop_details'); category = details.get('category') if type(details) is dict else None
                self.last_refusal_category = category if category in REFUSAL_CATEGORIES else 'other'
                raise ProviderFailure('model refusal', 'provider_schema_refusal')
            if stop != 'end_turn': raise ProviderFailure('incomplete response', 'provider_incomplete')
            blocks = response['content']
            if type(blocks) is not list or any(type(b) is not dict for b in blocks): raise ProviderFailure('unexpected response blocks', 'provider_malformed_output')
            texts = [b for b in blocks if b.get('type') == 'text']
            if len(texts) != 1 or blocks[-1] is not texts[0] or any(b.get('type') not in ('thinking', 'redacted_thinking') for b in blocks[:-1]):
                raise ProviderFailure('unexpected response blocks', 'provider_malformed_output')
            if type(texts[0].get('text')) is not str or len(texts[0]['text']) > 4000: raise ProviderFailure('unexpected answer text', 'provider_malformed_output')
            self.last_response_text = texts[0]['text']
            return self.response_decoder(self.last_response_text)
        except urllib.error.HTTPError as e:
            reason = 'provider_http_' + str(e.code)
            try:
                error = json.loads(e.read(16384)).get('error', {})
                if e.code == 400 and 'credit balance is too low' in error.get('message', '').lower(): reason = 'provider_credit_balance_low'
            except Exception: pass
            raise ProviderFailure(f'provider HTTP {e.code}', public_reason=reason, http_status=e.code) from None
        except ProviderFailure: raise
        except Exception as e:
            raise ProviderFailure('provider failure', public_reason=safe_failure(e)['reason']) from None


def provider(model, max_cost_usd, max_calls=PER_MODEL):
    """Haiku and Sonnet use the unchanged D1 adapter; only Opus needs the subclass."""
    s = SETTINGS[model]
    cls = OpusAdaptive if model == OPUS else Anthropic
    return cls(system_prompt=SYSTEM, response_schema=schema, response_decoder=strict_json, model=model,
               max_calls=max_calls, max_output_tokens=s['max_output_tokens'], max_input_bytes=MAX_INPUT_BYTES,
               timeout=TIMEOUT, max_cost_usd=max_cost_usd, input_usd_per_million=s['input_usd_per_million'],
               output_usd_per_million=s['output_usd_per_million'])


class ScriptedD2:
    """Known-answer controls. They read the actor request only, never a label."""
    scientific = False
    BEHAVIORS = ('oracle', 'always_feasible', 'always_infeasible', 'wrong_vote', 'malformed')

    def __init__(self, behavior='oracle'):
        if behavior not in self.BEHAVIORS: raise ValueError('unknown scripted control')
        self.behavior = behavior; self.name = 'scripted-d2-' + behavior
        self.calls = 0; self.last_usage = {}; self.last_response_text = None; self.last_model = None

    def belief(self, task, facts, option):
        if self.behavior == 'always_feasible': return True
        if self.behavior == 'always_infeasible': return False
        values = {k.split('.')[1]: v for k, v in option_facts(facts, option).items()}
        return bool(feasible(task['family'], values, task['rules']))

    def complete(self, request):
        self.calls += 1
        if self.behavior == 'malformed': return {'vote': 'D', 'feasible': 'yes'}
        context = request['context']; task = context['task']
        if request['phase'] == 'd2_feasibility':
            return {'feasible': self.belief(task, context['facts'], context['option'])}
        believed = [o for o in task['options'] if self.belief(task, context['facts'], o)]
        choice = derived_choice(task['family'], context['facts'], believed)
        if self.behavior == 'wrong_vote': choice = next(o for o in task['options'] if o != choice)
        return {'vote': choice if choice in OPTIONS else 'ABSTAIN'}


def derived_choice(family, facts, believed):
    """Unchanged objective and alphabetical tie-break over a believed-feasible set."""
    if not believed: return None
    def key(option):
        values = {k.split('.')[1]: v for k, v in option_facts(facts, option).items()}
        return (raw_objective(family, values), option)
    return min(believed, key=key)


# ---------------------------------------------------------------- schedule and freeze

def schedule():
    """Each item is asked of all three models; the within-item model order is balanced.

    Six decision items take each of the six model orders once; eighteen atomic
    items take each order three times. Every model is therefore first, second
    and third eight times, and Haiku precedes Sonnet in exactly twelve items.
    """
    rows = items(); orders = [list(p) for p in permutations(MODELS)]
    decisions = [r for r in rows if r['probe'] == 'decision']; atoms = [r for r in rows if r['probe'] == 'feasibility']
    assigned = {}
    for name, group, repeats in (('decision', decisions, 1), ('feasibility', atoms, 3)):
        pool = [copy.deepcopy(o) for o in orders for _ in range(repeats)]
        rng_for(ORDER_SEED, 'model-order', name).shuffle(pool)
        for row, order in zip(group, pool): assigned[row['item']] = order
    sequence = list(rows); rng_for(ORDER_SEED, 'item-order').shuffle(sequence)
    result = []
    for position, row in enumerate(sequence):
        for model in assigned[row['item']]:
            payload = body(row['request'], model); s = SETTINGS[model]
            result.append({'call_id': f'd2-{len(result):03d}', 'item': row['item'], 'probe': row['probe'],
                           'world': row['world'], 'option': row['option'], 'item_position': position, 'model': model,
                           'request_sha256': digest(row['request']), 'provider_body_sha256': digest(payload),
                           'reservation_microusd': (len(json.dumps(payload).encode()) + 512) * s['input_usd_per_million']
                                                   + s['max_output_tokens'] * s['output_usd_per_million']})
    check_schedule(result)
    return result


def check_schedule(rows):
    if len(rows) != ASSIGNED or [r['call_id'] for r in rows] != [f'd2-{i:03d}' for i in range(ASSIGNED)]:
        raise ValueError('schedule must contain exactly 72 ordered assignments')
    by_item = {}
    for row in rows: by_item.setdefault(row['item'], []).append(row)
    if len(by_item) != PER_MODEL or any(sorted(r['model'] for r in group) != sorted(MODELS) for group in by_item.values()):
        raise ValueError('every item must be assigned once to each model')
    if any(len({r['request_sha256'] for r in group}) != 1 for group in by_item.values()): raise ValueError('paired inputs differ')
    for model in MODELS:
        own = Counter(r['probe'] for r in rows if r['model'] == model)
        if own != {'decision': 6, 'feasibility': 18}: raise ValueError('per-model allocation mismatch')
    for position in range(3):
        if Counter(group[position]['model'] for group in by_item.values()) != {m: 8 for m in MODELS}:
            raise ValueError('model order is not balanced')
    first = sum(next(r['model'] for r in group if r['model'] in (HAIKU, SONNET)) == HAIKU for group in by_item.values())
    if first != 12: raise ValueError('Haiku/Sonnet order is not 12/12')
    return True


def source_hashes():
    paths = list((ROOT / 'bench_v3').glob('*.py'))
    paths += [ROOT / n for n in ('tasks.py', 'providers.py', 'diagnostic_v3_d2.py')] + [FACTS]
    return {p.relative_to(NOTES).as_posix(): fingerprint(p)['sha256'] for p in sorted(paths)}


def planning_documents():
    return {p.relative_to(REPO).as_posix(): fingerprint(p) for p in (PLAN_DOC, SETUP_DOC, BASE_PLAN, PRE_DOC)}


def source_commit():
    """Every executable dependency and planning document must be committed at HEAD."""
    value = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    if not re.fullmatch('[0-9a-f]{40}', value): raise ValueError('source commit required')
    committed = {(NOTES / name).relative_to(REPO).as_posix(): sha for name, sha in source_hashes().items()}
    committed.update({rel: doc['sha256'] for rel, doc in planning_documents().items()})
    for rel, expected in committed.items():
        saved = subprocess.run(['git', 'show', f'{value}:{rel}'], cwd=ROOT, capture_output=True)
        if saved.returncode or hashlib.sha256(saved.stdout).hexdigest() != expected:
            raise ValueError('commit the D2 source, fact table, plan, setup record and pre-run assessment before freezing')
    return value


def freeze(q0, launch_owner):
    if not re.fullmatch('[a-z0-9-]+/[a-z0-9-]+', launch_owner): raise ValueError('nonsecret agent launch owner required')
    gold()  # refuses a table whose labels are not unique and cross-checked
    rows = schedule(); commit = source_commit()
    relative_plan = PLAN_DOC.relative_to(REPO).as_posix()
    per_model = {m: sum(r['reservation_microusd'] for r in rows if r['model'] == m) for m in MODELS}
    probe = probe_record()
    reservation = sum(per_model.values()) + probe['reservation_microusd']
    if reservation > BUDGET_CAP_USD * 1_000_000: raise ValueError('worst-case reservation exceeds the dollar cap')
    return {'schema': VERSION, 'attempt': ATTEMPT, 'parent_attempt': PARENT,
            'status': 'frozen-diagnostic-only-preflight-required', 'launch_owner': launch_owner,
            'source_commit': commit, 'source_hashes': source_hashes(), 'planning_documents': planning_documents(),
            'public_plan': {'url': f'https://github.com/dmarzzz/swarm-lab/blob/{commit}/{relative_plan}',
                            'raw_url': f'https://raw.githubusercontent.com/dmarzzz/swarm-lab/{commit}/{relative_plan}',
                            'sha256': fingerprint(PLAN_DOC)['sha256']},
            'canonical_facts': fingerprint(FACTS), 'q0_check': check_q0(q0), 'system_hash': digest(SYSTEM),
            'schemas': {p: digest(schema(p)) for p in ('d2_decision', 'd2_feasibility')},
            'models': list(MODELS), 'model_settings': copy.deepcopy(SETTINGS),
            'planned_calls': ASSIGNED, 'items': PER_MODEL, 'counts_per_model': {'decision': 6, 'feasibility': 18},
            'compatibility_probe': probe, 'max_physical_calls': ASSIGNED + 1,
            'order_seed': ORDER_SEED,
            'configuration': {'max_input_bytes': MAX_INPUT_BYTES, 'timeout': TIMEOUT, 'transport_retries': 0,
                              'output_repair_retries': 0, 'fallback_models': 0, 'worker_count': 1,
                              'deadline_seconds': DEADLINE_SECONDS},
            'worst_case_reservation_microusd': reservation, 'reservation_by_model_microusd': per_model,
            'budget_cap_usd': BUDGET_CAP_USD, 'schedule': rows,
            'holdout_opened': False, 'successor_dispatch_authorized': False}


def probe_record():
    """The single Opus compatibility call: synthetic input, outside every denominator."""
    reject_gold(PROBE_REQUEST)
    if digest(PROBE_REQUEST) in {digest(r['request']) for r in items()}: raise ValueError('probe must not be an experimental item')
    payload = body(PROBE_REQUEST, OPUS); s = SETTINGS[OPUS]
    return {'model': OPUS, 'calls': 1, 'request_sha256': digest(PROBE_REQUEST), 'provider_body_sha256': digest(payload),
            'reservation_microusd': (len(json.dumps(payload).encode()) + 512) * s['input_usd_per_million']
                                    + s['max_output_tokens'] * s['output_usd_per_million'],
            'counts_toward_results': False}


def prepare(q0, output, launch_owner):
    frozen = freeze(q0, launch_owner)
    write_new(output, frozen)
    return {'status': frozen['status'], 'manifest_sha256': fingerprint(output)['sha256'], 'calls': ASSIGNED,
            'reservation_usd': frozen['worst_case_reservation_microusd'] / 1e6, 'model_calls_dispatched': 0}


def verify_manifest(manifest, q0):
    """Rebuild every manifest field from committed source and the retained records."""
    frozen = read(manifest)
    if frozen.get('schema') != VERSION or frozen.get('attempt') != ATTEMPT: raise ValueError('manifest version mismatch')
    if frozen != freeze(q0, frozen['launch_owner']): raise ValueError('frozen manifest differs from the bounded D2 plan')
    return frozen, {r['item']: r for r in items()}


# ---------------------------------------------------------------- admission

def check_models():
    """Authenticated metadata GET only; never an inference compatibility probe."""
    key = os.environ.get('SWARM_MODEL_API_KEY', '')
    if not key: raise ValueError('secure model environment absent')
    headers = {'x-api-key': key, 'anthropic-version': '2023-06-01'}
    workspace = os.environ.get('SWARM_MODEL_WORKSPACE_ID')
    if workspace: headers['anthropic-workspace-id'] = workspace
    found = {}
    for model in MODELS:
        req = urllib.request.Request('https://api.anthropic.com/v1/models/' + model, headers=headers)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            row = strict_json(response.read(200000).decode())
        if row.get('id') != model: raise ValueError('exact model unavailable; no fallback')
        limit = row.get('max_tokens')
        if type(limit) is int and limit < SETTINGS[model]['max_output_tokens']: raise ValueError('model output limit below the frozen ceiling')
        found[model] = {'id': row['id'], 'max_tokens': limit if type(limit) is int else None}
    return found


def public_plan(frozen):
    """Unauthenticated immutable raw-content and rendered-page check before dispatch."""
    expected = frozen['public_plan']
    with urllib.request.urlopen(expected['raw_url'], timeout=TIMEOUT) as response: raw = response.read(1000000)
    if hashlib.sha256(raw).hexdigest() != expected['sha256']: raise ValueError('public immutable plan content mismatch')
    text = raw.decode('utf-8')
    for section in ('TLDR', 'Question and prediction', 'Setup', 'Protocol', 'Metrics'):
        if '\n## ' + section + '\n' not in text: raise ValueError('public plan section absent')
    with urllib.request.urlopen(expected['url'], timeout=TIMEOUT) as response: page = response.read(8000000).decode('utf-8')
    for marker in (ATTEMPT, OPUS, '72'):
        if marker not in page: raise ValueError('public plan page does not display the current design')
    return {'url': expected['url'], 'sha256': expected['sha256'], 'public_raw_hash_matches': True,
            'public_page_markers_verified': True, 'verified_utc': datetime.now(timezone.utc).isoformat()}


EVIDENCE_KEYS = {'schema', 'manifest_sha256', 'launch_owner', 'server', 'claim_id', 'claim_until', 'hub_run',
                 'rehearsal_summary_sha256', 'rehearsal_readback_verified', 'duplicate_refusal_verified',
                 'budget_cap_usd', 'reviewer', 'review_kind', 'go_recorded_utc'}


def operator_evidence(evidence, manifest_hash, now=None):
    """Operator attestation is explicit evidence; nothing is inferred from a hostname."""
    now = now or datetime.now(timezone.utc)
    if type(evidence) is not dict or set(evidence) != EVIDENCE_KEYS or evidence['schema'] != 'd2-operator-preflight-v1':
        raise ValueError('operator evidence schema mismatch')
    if evidence['manifest_sha256'] != manifest_hash: raise ValueError('preflight evidence is for another manifest')
    if evidence['server'] != SERVER or evidence['claim_id'] != CLAIM: raise ValueError('the claimed D2 server is required')
    until = datetime.fromisoformat(evidence['claim_until'].replace('Z', '+00:00'))
    if until.tzinfo is None or until - now < timedelta(minutes=90): raise ValueError('claim must cover the one-hour run plus audit and upload')
    if evidence['hub_run'] != f'{EXPERIMENT}/{ATTEMPT}': raise ValueError('fixed D2 hub run required')
    if not re.fullmatch('[0-9a-f]{64}', str(evidence['rehearsal_summary_sha256'])): raise ValueError('rehearsal evidence hash required')
    if evidence['rehearsal_readback_verified'] is not True or evidence['duplicate_refusal_verified'] is not True:
        raise ValueError('rehearsal readback and duplicate refusal must be verified')
    if evidence['budget_cap_usd'] != BUDGET_CAP_USD: raise ValueError('dollar cap mismatch')
    if evidence['review_kind'] != 'same-researcher-check-under-owner-waiver' or not re.fullmatch('[a-z0-9-]+/[a-z0-9-]+', str(evidence['reviewer'])):
        raise ValueError('record the reviewer and that this is a same-researcher check, not independent review')
    datetime.fromisoformat(evidence['go_recorded_utc'].replace('Z', '+00:00'))
    return evidence


def preflight(manifest, q0, evidence, output):
    frozen, inputs = verify_manifest(manifest, q0)
    proof = operator_evidence(read(evidence), fingerprint(manifest)['sha256'])
    if proof['launch_owner'] != frozen['launch_owner']: raise ValueError('single launch owner mismatch')
    adapters = {m: provider(m, BUDGET_CAP_USD) for m in MODELS}
    for row in frozen['schedule']:
        request = inputs[row['item']]['request']
        native = adapters[row['model']].request_body(request)
        if native != body(request, row['model']) or digest(native) != row['provider_body_sha256']:
            raise ValueError('native provider serialization changed')
    available = check_models()
    result = {'schema': 'd2-preflight-pass-v1', 'manifest_sha256': fingerprint(manifest)['sha256'],
              'operator_evidence': proof, 'checked_utc': datetime.now(timezone.utc).isoformat(),
              'available_models': available, 'serialized_requests_verified': ASSIGNED,
              'worst_case_reservation_usd': frozen['worst_case_reservation_microusd'] / 1e6,
              'budget_cap_usd': BUDGET_CAP_USD, 'model_calls_dispatched': 0,
              'public_plan_verification': public_plan(frozen)}
    write_new(output, result)
    return {'status': 'preflight-passed', 'model_calls_dispatched': 0, 'preflight_sha256': fingerprint(output)['sha256']}


def validate_preflight(frozen, manifest_path, preflight_path):
    proof = read(preflight_path)
    if set(proof) != {'schema', 'manifest_sha256', 'operator_evidence', 'checked_utc', 'available_models',
                      'serialized_requests_verified', 'worst_case_reservation_usd', 'budget_cap_usd',
                      'model_calls_dispatched', 'public_plan_verification'}:
        raise ValueError('preflight receipt schema mismatch')
    if (proof['schema'] != 'd2-preflight-pass-v1' or sorted(proof['available_models']) != sorted(MODELS)
            or proof['serialized_requests_verified'] != ASSIGNED or proof['model_calls_dispatched'] != 0):
        raise ValueError('passing exact-model zero-call preflight required')
    public = proof['public_plan_verification']
    if (public.get('url') != frozen['public_plan']['url'] or public.get('sha256') != frozen['public_plan']['sha256']
            or public.get('public_raw_hash_matches') is not True or public.get('public_page_markers_verified') is not True):
        raise ValueError('immutable public plan verification required')
    owner = operator_evidence(proof['operator_evidence'], fingerprint(manifest_path)['sha256'])
    elapsed = datetime.now(timezone.utc) - datetime.fromisoformat(proof['checked_utc'])
    if elapsed < timedelta(0) or elapsed > timedelta(minutes=30): raise ValueError('preflight expired; recheck without inference calls')
    if (owner['launch_owner'] != frozen['launch_owner'] or proof['manifest_sha256'] != fingerprint(manifest_path)['sha256']
            or proof['budget_cap_usd'] != BUDGET_CAP_USD
            or round(proof['worst_case_reservation_usd'] * 1e6) != frozen['worst_case_reservation_microusd']):
        raise ValueError('owner, manifest or budget mismatch')
    return proof


# ---------------------------------------------------------------- scoring and analysis

def score(assignment, response, labels=None):
    labels = labels or gold(); world = labels[assignment['world']]
    base = {'probe': assignment['probe'], 'world': assignment['world'], 'family': world['family'], 'option': assignment['option']}
    if assignment['probe'] == 'decision':
        ev = {'invalid': int(response is None), 'correct': None, 'wrong_nonabstain': None, 'abstain': None,
              'feasible_choice': None, 'constraint_violation': None}
        if response is not None:
            vote = response['vote']
            ev.update(correct=int(vote == world['winner']), abstain=int(vote == 'ABSTAIN'),
                      wrong_nonabstain=int(vote not in (world['winner'], 'ABSTAIN')),
                      feasible_choice=int(vote in OPTIONS and world['feasible'][vote]),
                      constraint_violation=int(vote in OPTIONS and not world['feasible'][vote]))
        return {**base, 'gold': world['winner'], 'evaluation': ev}
    truth = world['feasible'][assignment['option']]
    ev = {'invalid': int(response is None), 'correct': None, 'true_positive': None, 'true_negative': None,
          'false_positive': None, 'false_negative': None}
    if response is not None:
        said = response['feasible']
        ev.update(correct=int(said == truth), true_positive=int(said and truth), true_negative=int(not said and not truth),
                  false_positive=int(said and not truth), false_negative=int(not said and truth))
    return {**base, 'gold': truth, 'evaluation': ev}


def total(rows, name):
    return sum(r['score']['evaluation'][name] or 0 for r in rows)


def model_summary(model, frozen, starts, rows, labels):
    own = [r for r in rows if r['model'] == model]; s = SETTINGS[model]
    start_ids = {e['call_id'] for e in starts if e['model'] == model}; terminal = {r['call_id'] for r in own}
    valid_usage = [r for r in own if all(type(r['usage'].get(k)) is int and r['usage'][k] >= 0 for k in ('input_tokens', 'output_tokens'))]
    missing_usage = [r['call_id'] for r in own if r['dispatched'] and r not in valid_usage]
    tokens = {k: sum(r['usage'][k] for r in valid_usage) for k in ('input_tokens', 'output_tokens')}
    cost = tokens['input_tokens'] * s['input_usd_per_million'] + tokens['output_tokens'] * s['output_usd_per_million']
    table = canonical_table(); facts = {w['world']: w['facts'] for w in table['worlds']}
    decisions = {r['world']: r for r in own if r['probe'] == 'decision'}
    atoms = {(r['world'], r['option']): r for r in own if r['probe'] == 'feasibility'}
    worlds = []
    for world in WORLDS:
        label = labels[world]; decision = decisions.get(world)
        vote = decision['response']['vote'] if decision and decision['response'] is not None else None
        vector = {o: (atoms[(world, o)]['response']['feasible'] if (world, o) in atoms and atoms[(world, o)]['response'] is not None else None)
                  for o in OPTIONS}
        complete = all(v is not None for v in vector.values())
        believed = [o for o in OPTIONS if vector[o]] if complete else None
        derived = derived_choice(label['family'], facts[world], believed) if complete else None
        worlds.append({'world': world, 'family': label['family'], 'correct_option': label['winner'],
                       'canonical_vote': vote, 'canonical_correct': None if vote is None else int(vote == label['winner']),
                       'atomic_predictions': vector, 'atomic_gold': label['feasible'],
                       'atomic_correct': sum(vector[o] is not None and vector[o] == label['feasible'][o] for o in OPTIONS),
                       'composition': {'state': 'missing' if not complete else 'none_predicted_feasible' if not believed
                                                else 'multiple_predicted_feasible' if len(believed) > 1 else 'one_predicted_feasible',
                                       'derived_choice': derived,
                                       'derived_correct': None if not complete else int(derived == label['winner']),
                                       'agrees_with_canonical_vote': None if not complete or vote is None
                                                                     else int((derived or 'ABSTAIN') == vote)}})
    d_rows = list(decisions.values()); a_rows = list(atoms.values())
    families = {}
    for family in ('capacity', 'total_cost', 'dependency'):
        fd = [r for r in d_rows if r['score']['family'] == family]; fa = [r for r in a_rows if r['score']['family'] == family]
        families[family] = {'canonical_correct': total(fd, 'correct'), 'canonical_assigned': 2,
                            'atomic_correct': total(fa, 'correct'), 'atomic_assigned': 6}
    complete = (len(own) == len(start_ids) == PER_MODEL and all(r['status'] == 'valid' for r in own) and not missing_usage)
    canonical = total(d_rows, 'correct'); atomic = total(a_rows, 'correct')
    scientific = bool(frozen.get('scientific', True))
    if not complete: reading = 'incomplete_or_invalid_no_screen_reading'
    elif canonical == 6 and atomic == 18: reading = 'both_screens_pass_nominate_separate_contract_test'
    elif atomic == 18: reading = 'atomic_pass_canonical_fail_focus_on_decision_composition'
    elif canonical == 6: reading = 'canonical_pass_atomic_fail_inconsistent_not_repaired'
    else: reading = 'atomic_fail_inspect_predicate_task_interface_semantics'
    return {'model': model, 'role': s['role'], 'assigned_calls': PER_MODEL, 'started': len(start_ids), 'terminal': len(own),
            'valid': sum(r['status'] == 'valid' for r in own), 'physical_calls_observed': sum(r['dispatched'] for r in own),
            'unstarted': PER_MODEL - len(start_ids), 'unresolved': sorted(start_ids - terminal),
            'failures': dict(Counter(r['reason'] for r in own if r['status'] != 'valid')),
            'refusal_stop_reasons': sum(r.get('stop_reason') == 'refusal' for r in own),
            'output_ceiling_stops': sum(r.get('stop_reason') == 'max_tokens' for r in own),
            'returned_models': sorted({str(r['returned_model']) for r in own if r['dispatched']}),
            'usage_missing_calls': missing_usage, **tokens, 'observed_usage_cost_microusd': cost,
            'actual_cost_complete': not missing_usage and not (start_ids - terminal)
                                    and not any(r['reason'] == 'provider_accounting_error' for r in own),
            'latency_seconds': [r['latency_seconds'] for r in own],
            'canonical': {'assigned': 6, 'terminal': len(d_rows), 'invalid': total(d_rows, 'invalid'),
                          'correct': canonical, 'wrong_nonabstain': total(d_rows, 'wrong_nonabstain'),
                          'abstain': total(d_rows, 'abstain'), 'feasible_choice': total(d_rows, 'feasible_choice'),
                          'constraint_violation': total(d_rows, 'constraint_violation'), 'required': 6},
            'atomic': {'assigned': 18, 'terminal': len(a_rows), 'invalid': total(a_rows, 'invalid'), 'correct': atomic,
                       'true_positive': total(a_rows, 'true_positive'), 'feasible_assigned': 6,
                       'true_negative': total(a_rows, 'true_negative'), 'infeasible_assigned': 12,
                       'false_positive': total(a_rows, 'false_positive'), 'false_negative': total(a_rows, 'false_negative'),
                       'required': 18, 'always_infeasible_baseline_correct': 12, 'always_feasible_baseline_correct': 6,
                       'above_always_infeasible_baseline': atomic > 12},
            'composition': {'derived_correct': sum(w['composition']['derived_correct'] or 0 for w in worlds),
                            'missing': sum(w['composition']['state'] == 'missing' for w in worlds),
                            'none_predicted_feasible': sum(w['composition']['state'] == 'none_predicted_feasible' for w in worlds),
                            'multiple_predicted_feasible': sum(w['composition']['state'] == 'multiple_predicted_feasible' for w in worlds),
                            'disagrees_with_canonical_vote': sum(w['composition']['agrees_with_canonical_vote'] == 0 for w in worlds),
                            'assigned': 6},
            'families': families, 'worlds': worlds,
            'screen': {'canonical_pass': bool(scientific and complete and canonical == 6),
                       'atomic_pass': bool(scientific and complete and atomic == 18),
                       'complete_valid_usage': complete, 'reading': reading if scientific else 'scripted_rehearsal_not_model_evidence',
                       'model_qualified': False}}


def summarize(frozen, events, rows):
    starts = [e for e in events if e['kind'] == 'call_start']
    ids = [e['call_id'] for e in starts]; terminal = [r['call_id'] for r in rows]
    if len(ids) != len(set(ids)) or len(terminal) != len(set(terminal)) or set(terminal) - set(ids):
        raise ValueError('duplicate or unstarted records')
    labels = gold(); by_id = {r['call_id']: r for r in rows}
    models = {m: model_summary(m, frozen, starts, rows, labels) for m in MODELS}
    paired = []
    for item in sorted({a['item'] for a in frozen['schedule']}):
        assignments = {a['model']: a for a in frozen['schedule'] if a['item'] == item}
        correct = {}
        for model, assignment in assignments.items():
            row = by_id.get(assignment['call_id'])
            correct[model] = row['score']['evaluation']['correct'] if row else None
        def delta(a, b):
            return None if correct[a] is None or correct[b] is None else correct[a] - correct[b]
        first = next(iter(assignments.values()))
        paired.append({'item': item, 'probe': first['probe'], 'world': first['world'], 'option': first['option'],
                       'correct': correct, 'opus_minus_sonnet': delta(OPUS, SONNET), 'opus_minus_haiku': delta(OPUS, HAIKU),
                       'sonnet_minus_haiku': delta(SONNET, HAIKU)})
    return {'schema': VERSION, 'attempt': frozen['attempt'], 'scientific': bool(frozen.get('scientific', True)),
            'assigned_calls': ASSIGNED, 'started': len(starts), 'terminal': len(rows),
            'unresolved': sorted(set(ids) - set(terminal)), 'models': models, 'paired_items': paired,
            'observed_usage_cost_microusd': sum(m['observed_usage_cost_microusd'] for m in models.values()),
            'qualification': False, 'holdout_opened': False, 'successors_dispatched': False,
            'limitations': ['Six reused development world clusters; descriptive diagnostics only.',
                            'Evidence packaging and the response contract change together; D1 and D2 are not interchangeable trials.',
                            'The Opus arm differs from the comparison arms in model, always-on thinking, effort, sampling default and output ceiling.',
                            'Each world has exactly one feasible option; multiple-feasible tie-breaking is not tested.',
                            'One response per model and item; no repeats, so no within-model variability estimate.',
                            'Comparison-arm refusals and unexpected blocks share one failure reason; only the Opus adapter separates them.',
                            'Ambiguous dispatched calls are never retried; absent usage is unknown cost, not zero.']}


# ---------------------------------------------------------------- execution

class HubProgress:
    """Attach to the operator's already-started hub run; never enqueue or restart it.

    Reports counters only. Actor inputs, outputs and scores stay in private artifacts.
    """
    def __init__(self, hub_run, manifest_sha256, scientific):
        expected = f'{EXPERIMENT}/{ATTEMPT}' + ('' if scientific else '-rehearsal')
        if hub_run != expected: raise ValueError('wrong bounded hub run')
        import swarm_report as sr
        current = sr.get_run(hub_run)
        if current.get('status') != 'running' or current.get('params', {}).get('manifest_sha256') != manifest_sha256:
            raise ValueError('operator must start one manifest-bound hub run before attachment')
        self.reporter = sr.Run(hub_run, EXPERIMENT, current['params'])
        self.started = self.terminal = self.invalid = self.physical = self.cost_micro = self.missing_usage = 0
        self.scientific = scientific

    def metrics(self):
        return {'assigned_calls': ASSIGNED, 'started_calls': self.started, 'terminal_calls': self.terminal,
                'physical_model_calls': self.physical, 'invalid_calls': self.invalid,
                'observed_usage_cost_usd': self.cost_micro / 1e6, 'usage_missing_calls': self.missing_usage,
                'qualification_passed': 0}

    def label(self):
        return ('D2: 24 fixed items for each of Opus 5.5 (model under test), Sonnet 4.6 and Haiku 4.5; no retries.'
                if self.scientific else 'SCRIPTED REHEARSAL, NOT MODEL EVIDENCE: zero model calls, known-answer controls.')

    def __call__(self, event):
        if event['kind'] == 'call_start': self.started += 1
        if event['kind'] == 'call_terminal':
            row = event['record']; self.terminal += 1; s = SETTINGS[row['model']]
            self.invalid += row['status'] != 'valid'; self.physical += row['dispatched']
            self.missing_usage += row['dispatched'] and not all(k in row['usage'] for k in ('input_tokens', 'output_tokens'))
            self.cost_micro += (row['usage'].get('input_tokens', 0) * s['input_usd_per_million']
                                + row['usage'].get('output_tokens', 0) * s['output_usd_per_million'])
        if event['kind'] in ('call_start', 'call_terminal', 'dispatch_stopped', 'complete'):
            self.reporter.progress(self.terminal, ASSIGNED, message=self.label(), **self.metrics())

    def finish(self, output, checked):
        from bench_v3.hub_worker import publish
        write_new(Path(output) / 'audit.json', {k: v for k, v in checked.items() if k != 'summary'})
        publish(self.reporter, Path(output))
        if self.terminal == ASSIGNED and not self.invalid and not self.missing_usage:
            self.reporter.done(message=('D2 execution and audit complete; read the per-model screens in the published results. No model qualification, no successor.'
                                        if self.scientific else 'SCRIPTED REHEARSAL complete: 72 known-answer assignments, zero model calls. Not model evidence.'),
                               **self.metrics())
        else:
            self.reporter.fail(message='D2 bounded diagnostic retained failures or missing records; no retry, no successor.', **self.metrics())


def execute(frozen, inputs, output, ledger, providers, scientific, preflight_proof=None, observer=None, clock=time.monotonic):
    """A permanent attempt marker precedes dispatch; refusal survives another output path."""
    output = Path(output); ledger = Path(ledger)
    if output.exists(): raise ValueError('output exists; audit instead of restarting')
    if not ledger.is_dir(): raise ValueError('operator-created persistent dispatch ledger required')
    prefix = frozen['attempt'] if scientific else frozen['attempt'] + '-zero-model-rehearsal'
    lock = (ledger / (prefix + '.lock')).open('a')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        write_new(ledger / (prefix + '.started.json'), {'attempt': frozen['attempt'], 'manifest_hash': digest(frozen),
                                                      'scientific': scientific, 'automatic_restart_permitted': False})
        output.mkdir(parents=True, exist_ok=False); sync_dir(output.parent)
        run_manifest = {**frozen, 'scientific': scientific, 'preflight': preflight_proof}
        write_new(output / 'manifest.json', run_manifest)
        journal = Journal(output / 'events.jsonl', observer=observer)
        rows = []; begin = clock(); labels = gold()
        try:
            journal.emit('manifest', manifest_hash=digest(run_manifest))
            for assignment in frozen['schedule']:
                if clock() - begin >= DEADLINE_SECONDS or (ledger / (prefix + '.stop')).exists():
                    journal.emit('dispatch_stopped', reason='deadline_or_owner_stop'); break
                model = assignment['model']; adapter = providers[model]
                request = copy.deepcopy(inputs[assignment['item']]['request'])
                journal.emit('call_start', **assignment, request=request)
                start = time.monotonic(); before = adapter.calls
                status = 'valid'; reason = None; http_class = None; response = None
                try:
                    answer = adapter.complete(request)
                    if scientific and adapter.last_model != model:
                        raise ProviderFailure('returned model mismatch', 'provider_model_mismatch')
                    try: response = validate(answer, request['phase'])
                    except (ValueError, TypeError, KeyError):
                        status = 'invalid_output'; reason = 'provider_malformed_output'
                except Exception as exc:
                    failure = safe_failure(exc); status = 'provider_failure'
                    reason = failure['reason']; http_class = failure['http_status_class']
                usage = {k: v for k, v in copy.deepcopy(getattr(adapter, 'last_usage', {})).items()
                         if k in ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens')
                         and type(v) is int and v >= 0}
                dispatched = bool(scientific and adapter.calls > before)
                row = {**assignment, 'status': status, 'reason': reason, 'http_status_class': http_class,
                       'response': response, 'raw_text': getattr(adapter, 'last_response_text', None),
                       'returned_model': getattr(adapter, 'last_model', None),
                       'stop_reason': getattr(adapter, 'last_stop_reason', None),
                       'refusal_category': getattr(adapter, 'last_refusal_category', None),
                       'usage': usage, 'dispatched': dispatched,
                       'dispatch_state': 'outcome_unknown' if dispatched and reason in ('provider_timeout', 'provider_transport_error', 'provider_unknown') else 'terminal',
                       'latency_seconds': round(time.monotonic() - start, 6), 'score': score(assignment, response, labels)}
                rows.append(row); journal.emit('call_terminal', record=row)
                if reason in ('provider_model_mismatch', 'provider_accounting_error', 'provider_local_limit'):
                    journal.emit('dispatch_stopped', reason=reason); break
            journal.emit('complete', terminal=len(rows), assigned=ASSIGNED)
            write_new(output / 'outcomes.json', rows)
            write_new(output / 'summary.json', summarize(run_manifest, journal.events, rows))
            write_new(output / 'reporting.json', {'observer_failures': journal.observer_failures})
        finally: journal.close()
        return {'status': 'bounded-execution-ended', 'assigned': ASSIGNED, 'terminal': len(rows),
                'physical_calls': sum(r['dispatched'] for r in rows), 'qualification': False}
    finally: lock.close()


def probe(manifest, q0, preflight_path, ledger, output):
    """One Opus call on the synthetic request, so a rejected setting costs no assignment.

    The ledger marker is permanent: one probe per attempt. A failed probe blocks
    the batch and goes back to the reviewer; this command never retries.
    """
    frozen, _ = verify_manifest(manifest, q0)
    validate_preflight(frozen, manifest, preflight_path)
    ledger = Path(ledger)
    if not ledger.is_dir(): raise ValueError('operator-created persistent dispatch ledger required')
    if (ledger / (ATTEMPT + '.started.json')).exists(): raise ValueError('batch already started; no probe')
    record = frozen['compatibility_probe']
    adapter = provider(OPUS, record['reservation_microusd'] / 1e6 + 1e-6, max_calls=1)
    if digest(adapter.request_body(PROBE_REQUEST)) != record['provider_body_sha256']: raise ValueError('probe serialization changed')
    write_new(ledger / (ATTEMPT + '.opus-probe.started.json'),
              {'attempt': ATTEMPT, 'manifest_sha256': fingerprint(manifest)['sha256'], 'automatic_retry_permitted': False})
    status = 'valid'; reason = None; http_class = None; response = None; start = time.monotonic()
    try:
        answer = adapter.complete(copy.deepcopy(PROBE_REQUEST))
        if adapter.last_model != OPUS: raise ProviderFailure('returned model mismatch', 'provider_model_mismatch')
        try: response = validate(answer, PROBE_REQUEST['phase'])
        except (ValueError, TypeError, KeyError): status = 'invalid_output'; reason = 'provider_malformed_output'
    except Exception as exc:
        failure = safe_failure(exc); status = 'provider_failure'; reason = failure['reason']; http_class = failure['http_status_class']
    receipt = {'schema': 'd2-opus-probe-v1', 'attempt': ATTEMPT, 'manifest_sha256': fingerprint(manifest)['sha256'],
               'model': OPUS, 'request_sha256': record['request_sha256'], 'provider_body_sha256': record['provider_body_sha256'],
               'status': status, 'reason': reason, 'http_status_class': http_class, 'response': response,
               'stop_reason': adapter.last_stop_reason, 'refusal_category': adapter.last_refusal_category,
               'returned_model': adapter.last_model, 'usage': dict(adapter.last_usage), 'physical_calls': adapter.calls,
               'latency_seconds': round(time.monotonic() - start, 6), 'counts_toward_results': False,
               'checked_utc': datetime.now(timezone.utc).isoformat()}
    write_new(output, receipt)
    return {'status': 'probe-passed' if status == 'valid' else 'probe-failed-batch-blocked', 'reason': reason,
            'http_status_class': http_class, 'stop_reason': adapter.last_stop_reason, 'physical_calls': adapter.calls,
            'usage': dict(adapter.last_usage)}


def validate_probe(frozen, manifest_path, probe_path):
    receipt = read(probe_path); record = frozen['compatibility_probe']
    if (receipt.get('schema') != 'd2-opus-probe-v1' or receipt.get('manifest_sha256') != fingerprint(manifest_path)['sha256']
            or receipt.get('request_sha256') != record['request_sha256'] or receipt.get('provider_body_sha256') != record['provider_body_sha256']
            or receipt.get('status') != 'valid' or receipt.get('returned_model') != OPUS or receipt.get('physical_calls') != 1
            or receipt.get('counts_toward_results') is not False):
        raise ValueError('a passing Opus compatibility probe for this manifest is required before the batch')
    validate(receipt['response'], PROBE_REQUEST['phase'])
    return receipt


def run(manifest, q0, preflight_path, probe_path, output, ledger, hub_run):
    if hub_run is None: raise ValueError('paid run requires an operator-started manifest-bound hub run')
    frozen, inputs = verify_manifest(manifest, q0)
    proof = validate_preflight(frozen, manifest, preflight_path)
    proof = {**proof, 'compatibility_probe': validate_probe(frozen, manifest, probe_path)}
    # Each adapter is capped at its own frozen worst-case reservation; the sum is below the dollar cap.
    providers = {m: provider(m, frozen['reservation_by_model_microusd'][m] / 1e6 + 1e-6) for m in MODELS}
    observer = HubProgress(hub_run, fingerprint(manifest)['sha256'], True)
    result = execute(frozen, inputs, output, ledger, providers, True, proof, observer)
    observer.finish(output, audit(output, q0))
    return result


# Rehearsal controls: one known-answer policy per model slot, so the analysis
# path is exercised at 18/18, at the 12/18 trivial baseline and at 6/18.
REHEARSAL_CONTROLS = {OPUS: 'oracle', SONNET: 'always_infeasible', HAIKU: 'always_feasible'}


def rehearse(manifest, q0, output, ledger, hub_run=None, failure_call=None):
    frozen, inputs = verify_manifest(manifest, q0)
    observer = HubProgress(hub_run, fingerprint(manifest)['sha256'], False) if hub_run else None
    providers = {m: ScriptedD2(REHEARSAL_CONTROLS[m]) for m in MODELS}
    if failure_call is not None:
        if not 0 <= failure_call < ASSIGNED: raise ValueError('scripted failure index must be 0..71')
        target = frozen['schedule'][failure_call]
        ordinal = sum(a['model'] == target['model'] for a in frozen['schedule'][:failure_call])
        class FailureFixture(ScriptedD2):
            def complete(self, request):
                if self.calls == ordinal:
                    self.calls += 1; raise TimeoutError('scripted deliberate failure')
                return super().complete(request)
        providers[target['model']] = FailureFixture(REHEARSAL_CONTROLS[target['model']])
    result = execute(frozen, inputs, output, ledger, providers, False, observer=observer)
    if observer: observer.finish(output, audit(output, q0))
    return result


def audit(directory, q0, allow_interrupted=False):
    directory = Path(directory); frozen = read(directory / 'manifest.json')
    if frozen['source_hashes'] != source_hashes(): raise ValueError('audit with the exact D2 source')
    with tempfile.TemporaryDirectory() as folder:
        manifest = Path(folder) / 'manifest.json'
        write_new(manifest, {k: v for k, v in frozen.items() if k not in ('scientific', 'preflight')})
        protocol, inputs = verify_manifest(manifest, q0)
    events = read_events(directory / 'events.jsonl')
    if not events or events[0].get('manifest_hash') != digest(frozen): raise ValueError('journal manifest mismatch')
    complete = events[-1]['kind'] == 'complete'
    if not complete and not allow_interrupted: raise ValueError('interrupted run; use audit --allow-interrupted; never restart')
    starts = [e for e in events if e['kind'] == 'call_start']
    terminals = [e['record'] for e in events if e['kind'] == 'call_terminal']
    if len(starts) > ASSIGNED: raise ValueError('unassigned starts')
    envelope = ('seq', 'previous', 'kind', 'hash')
    for start, assignment in zip(starts, protocol['schedule']):
        request = inputs[assignment['item']]['request']
        if start != {**{k: start[k] for k in envelope}, **assignment, 'request': request}:
            raise ValueError('saved schedule or request mismatch')
    by_start = {e['call_id']: e for e in starts}; labels = gold()
    for row in terminals:
        if row['call_id'] not in by_start: raise ValueError('terminal without start')
        assignment = protocol['schedule'][int(row['call_id'][3:])]
        if any(row[k] != v for k, v in assignment.items()): raise ValueError('terminal assignment drift')
        phase = inputs[row['item']]['request']['phase']; response = row['response']
        if row['status'] == 'valid':
            validate(response, phase)
            if frozen['scientific'] and (strict_json(row['raw_text']) != response or row['returned_model'] != row['model'] or not row['dispatched']):
                raise ValueError('saved raw response or model mismatch')
        elif row['status'] not in ('invalid_output', 'provider_failure') or response is not None or row['reason'] not in REASONS:
            raise ValueError('invalid failure record')
        elif row['raw_text'] is not None and row['reason'] == 'provider_malformed_output':
            try: validate(strict_json(row['raw_text']), phase)
            except (ValueError, TypeError, KeyError): pass
            else: raise ValueError('valid raw response disguised as a malformed failure')
        if score(assignment, response, labels) != row['score']: raise ValueError('saved outcome score mismatch')
    summary = summarize(frozen, events, terminals)
    if complete:
        if read(directory / 'outcomes.json') != terminals or read(directory / 'summary.json') != summary:
            raise ValueError('saved outcomes or summary mismatch')
        if events[-1] != {**{k: events[-1][k] for k in envelope}, 'terminal': len(terminals), 'assigned': ASSIGNED}:
            raise ValueError('final accounting mismatch')
    return {'ok': True, 'complete_journal': complete, 'requests_verified': len(starts),
            'outcomes_recomputed': len(terminals), 'summary': summary}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('table').add_argument('--output', type=Path, required=True)
    for name in ('prepare', 'preflight', 'probe', 'run', 'rehearse', 'audit'):
        p = sub.add_parser(name)
        p.add_argument('--q0', type=Path, required=True, help='retained clean Q0 record directory')
        if name != 'audit': p.add_argument('--output', type=Path, required=True)
        if name in ('preflight', 'probe', 'run', 'rehearse'): p.add_argument('--manifest', type=Path, required=True)
        if name == 'prepare': p.add_argument('--launch-owner', required=True)
        if name == 'preflight': p.add_argument('--operator-evidence', type=Path, required=True)
        if name in ('probe', 'run'): p.add_argument('--preflight', type=Path, required=True)
        if name == 'run': p.add_argument('--probe', type=Path, required=True)
        if name in ('probe', 'run', 'rehearse'): p.add_argument('--dispatch-ledger', type=Path, required=True)
        if name in ('run', 'rehearse'):
            p.add_argument('--hub-run', required=name == 'run', help='operator-started manifest-bound run; never enqueued by this CLI')
        if name == 'rehearse': p.add_argument('--scripted-failure-call', type=int, help='0-based deliberate software failure; no model call')
        if name == 'audit':
            p.add_argument('--directory', type=Path, required=True)
            p.add_argument('--allow-interrupted', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.command == 'table':
            write_new(args.output, build_table()); result = {'worlds': 6, 'values': 48, 'model_calls_dispatched': 0}
        elif args.command == 'prepare': result = prepare(args.q0, args.output, args.launch_owner)
        elif args.command == 'preflight': result = preflight(args.manifest, args.q0, args.operator_evidence, args.output)
        elif args.command == 'probe': result = probe(args.manifest, args.q0, args.preflight, args.dispatch_ledger, args.output)
        elif args.command == 'run': result = run(args.manifest, args.q0, args.preflight, args.probe, args.output, args.dispatch_ledger, args.hub_run)
        elif args.command == 'rehearse':
            result = rehearse(args.manifest, args.q0, args.output, args.dispatch_ledger, args.hub_run, args.scripted_failure_call)
        else:
            result = {k: v for k, v in audit(args.directory, args.q0, args.allow_interrupted).items() if k != 'summary'}
        print(json.dumps(result, sort_keys=True)); return 0
    except Exception as exc:
        # No paths, credentials, provider bodies or arbitrary exception strings.
        detail = str(exc) if type(exc) is ValueError else 'See private setup and audit evidence; no automatic retry.'
        print(json.dumps({'status': 'stopped', **safe_failure(exc), 'detail': detail}, sort_keys=True))
        return 2


if __name__ == '__main__': raise SystemExit(main())
