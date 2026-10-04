"""Frozen design, the request in two equal-information representations, local answer validation,
assignments per stage, gates and instrument invariants for verify-cost-qwen.

The decision itself (layouts, consequence records, scorer) is sim.py, the parameterized copy of the
phantom-coast PC5 contract. PC5's design.py (schedule, qualified, grade, contrasts) became
`assignments`, `qualification`, `evaluate` here and `analyze.py`; its engine.py (reserve before any
wire effect, durable terminal record per assignment, grading from saved records) became worker.py
on top of the reference OpenRouter adapter and ledger in provider.py.
"""
import collections
import functools
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

import yaml

import sim

ROOT = Path(__file__).resolve().parent.parent
EXPERIMENT = 'verify-cost-qwen'
STAGES = ('S0', 'P0', 'Q0', 'S1')
REPRESENTATIONS = ('prose', 'table')
POLICIES = ('optimal', 'always_check', 'always_explore', 'always_first', 'always_second')
GRID_KINDS = ('main', 'engineering')
ROW_FIELDS = ('id', 'kind', 'set', 'layout', 'error', 'unknown_cost', 'representation', 'legal_cells', 'input_hash', 'content_bytes')
# Words that must never appear in what the model reads.
FORBIDDEN = ('truth', 'seed', 'optimal', 'regret', 'recommend', 'better', 'best', 'should', 'draw', 'margin',
             'dominan', 'qualif', 'engineering', 'layout', 'expected loss', 'expected cost of', 'comparator')
CHARS_PER_TOKEN_FLOOR = 2.5     # planning assumption for text with many numbers; P0 measures the real ratio


@functools.lru_cache(maxsize=1)
def design():
    """The frozen design. Cached: callers must not mutate the returned mapping."""
    return yaml.safe_load((ROOT / 'design.yaml').read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def source_hash():
    """Covers the frozen design, the hub registration, the pinned requirements and every source file.
    README, SETUP, preregistration, RUN, VISUALIZATION, READY.yaml, manifest.json and reviews are outside it."""
    paths = [ROOT / 'design.yaml', ROOT / 'experiment.yaml', ROOT / 'requirements.txt'] + sorted((ROOT / 'src').glob('*.py'))
    return digest([(p.name, hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths])


def code_revision():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return os.environ.get('STUDY_CODE_COMMIT', 'unknown')


def results_dir():
    """Run outputs never go into the committed tree: STUDY_RESULTS_DIR, else the git-ignored results/."""
    return Path(os.environ.get('STUDY_RESULTS_DIR') or ROOT / 'results')


def model():
    """The model of this chain: STUDY_MODEL, default the first entry of the frozen ladder."""
    ladder = design()['model_ladder']; chosen = os.environ.get('STUDY_MODEL') or ladder[0]
    if chosen not in ladder: raise ValueError('model_not_in_ladder')
    return chosen


def provider_name(name=None):
    return design()['providers'][name or model()]


def schema(name=None):
    """The answer schema of a model's chain: `cost_then_choice` (attempt 002) or `choice_only` (attempt 001's)."""
    return design()['models'][name or model()]['answer_schema']


@functools.lru_cache(maxsize=None)
def _budget(name):
    return dict(design()['budget'], **(design()['models'][name].get('budget') or {}))


def budget(name=None):
    """The budget of a model's chain: the common budget with the model's overrides. Cached: do not mutate."""
    return _budget(name or model())


def batch(stage, name=None):
    """`<stage>-<attempt>` for the first model of the ladder, `<stage>-<attempt>-<tag>` for any other model."""
    tag = design()['models'][name or model()]['tag']
    return f'{stage.lower()}-{design()["attempt"]}' + (f'-{tag}' if tag else '')


def params(stage):
    if stage not in STAGES: raise ValueError('unknown_stage')
    return {'stage': stage, 'backend': 'scripted' if stage == 'S0' else provider_name(), 'model': model(), 'batch': batch(stage),
            'source_hash': source_hash(), 'code': code_revision()}


def provider_config(name=None):
    """What the model's reference adapter needs, taken from the frozen design and nowhere else."""
    d = design(); name = name or model()
    if provider_name(name) == 'openrouter':
        return {'model': d['model'], 'canonical_model': d['canonical_model'], 'provider': d['provider'],
                'request_template': d['request_template'], 'budget': budget(name)}
    return {'model': name, 'request_template': d['models'][name]['request_template'], 'budget': budget(name)}


# ------------------------------------------------------------------ the request

SYSTEM_CHOICE_ONLY = ('You decide which one cell of a map to inspect. Read the map, the evidence, the objective and the '
                      'consequences of each allowed action, then choose. Answer with one JSON object and nothing else, in '
                      'exactly this shape: {"inspect": "<row>,<column>"}. The value must be one of the two allowed cells, '
                      'written exactly as listed. Do not add other keys and do not write anything outside the JSON object.')
SYSTEM = ('You decide which one cell of a map to inspect. Read the map, the evidence, the objective and the '
          'consequences of each allowed action. Before choosing, write the expected total cost of the final map for '
          'each of the two allowed actions, then choose. Answer with one JSON object and nothing else, in '
          'exactly this shape: {"cost_if_inspect": {"<first allowed cell>": <number>, "<second allowed cell>": <number>}, '
          '"inspect": "<row>,<column>"}. The value of "inspect" must be one of the two allowed cells, '
          'written exactly as listed. Do not add other keys and do not write anything outside the JSON object.')

RESULT = {'measured': 'correct direct measurement', 'unknown': 'returned as UNKNOWN', 'kept': 'direct measurement kept'}
TABLE_HEADER = 'action | cell | result | probability | cost'
NUMBER = re.compile(r'\d+\.\d\d')


def fmt(x):
    return f'{x:.2f}'


def shown(records):
    """Consequence records with probabilities and costs as the two-decimal strings both renderings print."""
    return [dict(r, probability=fmt(r['probability']), cost=fmt(r['cost'])) for r in records]


def render_prose(records):
    """One sentence per action and one for the untouched cells. `records` come from `shown`."""
    lines, by_action = [], collections.OrderedDict()
    for r in records: by_action.setdefault(r['action'], []).append(r)
    for action, rs in by_action.items():
        if action == 'either':
            (r,) = rs
            lines.append(f'Whichever cell you inspect: each of the other {r["count"]} cells keeps its direct measurement '
                         f'with probability {r["probability"]}, at cost {r["cost"]}.')
            continue
        own = rs[0]
        text = (f'If you inspect {action}: cell {own["cell"]} gets a correct direct measurement with probability '
                f'{own["probability"]}, at cost {own["cost"]}; ')
        if rs[1]['outcome'] == 'unknown':
            u = rs[1]
            text += f'cell {u["cell"]} is returned as UNKNOWN with probability {u["probability"]}, at cost {u["cost"]}.'
        else:
            right, wrong = rs[1], rs[2]
            text += (f'cell {right["cell"]} keeps the report label {right["label"]}, which is right with probability '
                     f'{right["probability"]}, at cost {right["cost"]}, and wrong with probability {wrong["probability"]}, '
                     f'at cost {wrong["cost"]}.')
        lines.append(text)
    return '\n'.join(lines)


def render_table(records):
    """One row per record."""
    lines = [TABLE_HEADER]
    for r in records:
        if r['action'] == 'either':
            lines.append(f'either | each of the other {r["count"]} cells | {RESULT["kept"]} | {r["probability"]} | {r["cost"]}')
        elif r['outcome'] in ('report_right', 'report_wrong'):
            word = r['outcome'].split('_')[1]
            lines.append(f'inspect {r["action"]} | {r["cell"]} | report label {r["label"]} kept and {word} | {r["probability"]} | {r["cost"]}')
        else:
            lines.append(f'inspect {r["action"]} | {r["cell"]} | {RESULT[r["outcome"]]} | {r["probability"]} | {r["cost"]}')
    return '\n'.join(lines)


_CELL, _NUM, _LABEL = r'(\d,\d)', r'(\d+\.\d\d)', r'(LAND|WATER)'
_PROSE_OWN = (r'If you inspect ' + _CELL + r': cell ' + _CELL + r' gets a correct direct measurement with probability '
              + _NUM + r', at cost ' + _NUM + r'; ')
_PROSE_UNKNOWN = re.compile(_PROSE_OWN + r'cell ' + _CELL + r' is returned as UNKNOWN with probability ' + _NUM + r', at cost ' + _NUM + r'\.')
_PROSE_REPORT = re.compile(_PROSE_OWN + r'cell ' + _CELL + r' keeps the report label ' + _LABEL + r', which is right with probability '
                           + _NUM + r', at cost ' + _NUM + r', and wrong with probability ' + _NUM + r', at cost ' + _NUM + r'\.')
_PROSE_OTHERS = re.compile(r'Whichever cell you inspect: each of the other (\d+) cells keeps its direct measurement with probability '
                           + _NUM + r', at cost ' + _NUM + r'\.')
_TABLE_ROW = re.compile(r'inspect ' + _CELL + r' \| ' + _CELL + r' \| (.+) \| ' + _NUM + r' \| ' + _NUM)
_TABLE_OTHERS = re.compile(r'either \| each of the other (\d+) cells \| direct measurement kept \| ' + _NUM + r' \| ' + _NUM)
_TABLE_REPORT = re.compile(r'report label ' + _LABEL + r' kept and (right|wrong)')


def parse_prose(text):
    """The records a prose block states. Raises ValueError on any line that is not one of the three sentences."""
    out = []
    for line in text.split('\n'):
        m = _PROSE_UNKNOWN.fullmatch(line)
        if m:
            a, own, p, c, other, p2, c2 = m.groups()
            out += [{'action': a, 'cell': own, 'outcome': 'measured', 'probability': p, 'cost': c},
                    {'action': a, 'cell': other, 'outcome': 'unknown', 'probability': p2, 'cost': c2}]
            continue
        m = _PROSE_REPORT.fullmatch(line)
        if m:
            a, own, p, c, other, label, p2, c2, p3, c3 = m.groups()
            out += [{'action': a, 'cell': own, 'outcome': 'measured', 'probability': p, 'cost': c},
                    {'action': a, 'cell': other, 'outcome': 'report_right', 'label': label, 'probability': p2, 'cost': c2},
                    {'action': a, 'cell': other, 'outcome': 'report_wrong', 'label': label, 'probability': p3, 'cost': c3}]
            continue
        m = _PROSE_OTHERS.fullmatch(line)
        if m:
            out.append({'action': 'either', 'cell': 'others', 'count': int(m.group(1)), 'outcome': 'kept',
                        'probability': m.group(2), 'cost': m.group(3)})
            continue
        raise ValueError('unparsed_prose_line')
    return out


def parse_table(text):
    """The records a table block states. Raises ValueError on a wrong header or any row that is not a record."""
    lines = text.split('\n')
    if lines[0] != TABLE_HEADER: raise ValueError('table_header')
    out = []
    for line in lines[1:]:
        m = _TABLE_OTHERS.fullmatch(line)
        if m:
            out.append({'action': 'either', 'cell': 'others', 'count': int(m.group(1)), 'outcome': 'kept',
                        'probability': m.group(2), 'cost': m.group(3)})
            continue
        m = _TABLE_ROW.fullmatch(line)
        if not m: raise ValueError('unparsed_table_row')
        a, cell, result, p, c = m.groups()
        r = {'action': a, 'cell': cell, 'probability': p, 'cost': c}
        report = _TABLE_REPORT.fullmatch(result)
        if report:
            r.update(outcome='report_' + report.group(2), label=report.group(1))
        elif result in (RESULT['measured'], RESULT['unknown']):
            r['outcome'] = 'measured' if result == RESULT['measured'] else 'unknown'
        else:
            raise ValueError('unparsed_table_result')
        out.append(r)
    return out


RENDER = {'prose': render_prose, 'table': render_table}
PARSE = {'prose': parse_prose, 'table': parse_table}
BLOCK_START, BLOCK_END = '\n\nCONSEQUENCES\n', '\n\nANSWER\n'


def consequence_block(w, error, unknown_cost, representation):
    return RENDER[representation](shown(sim.consequences(w, error, unknown_cost)))


def system(kind=None):
    """The system message of an answer schema: attempt 002's for `cost_then_choice`, attempt 001's for `choice_only`."""
    return {'cost_then_choice': SYSTEM, 'choice_only': SYSTEM_CHOICE_ONLY}[kind or schema()]


def user_text(w, error, unknown_cost, representation, kind=None):
    """The whole user message. Everything outside the CONSEQUENCES block is the same for both representations;
    everything before the ANSWER block is the same for both answer schemas."""
    f = sim.facts(w, error, unknown_cost); a, b = f['legal_cells']; rep = f['report']
    measurements = '; '.join(f'{c} {label}' for c, label in f['measurements'])
    return ('MAP\n'
            'A 6 by 6 grid. Cells are named row,column. Every cell is LAND or WATER.\n\n'
            'EVIDENCE\n'
            f'Direct measurements, current and noiseless ({len(f["measurements"])} cells): {measurements}\n'
            f'Report, older (1 cell): cell {rep["cell"]} is {rep["label"]}. The report is wrong with probability {fmt(rep["error_probability"])}.\n'
            f'No evidence (1 cell): {f["unknown_cell"]}.\n\n'
            'DECISION\n'
            f'You have one inspection. Allowed cells, in this order: {a}; {b}.\n'
            'After the inspection the final map is filled in by the fixed rule under CONSEQUENCES and every cell is scored.\n'
            'Objective: minimize the expected total cost of the final map.'
            + BLOCK_START + consequence_block(w, error, unknown_cost, representation) + BLOCK_END + answer_block(a, b, kind))


def answer_block(a, b, kind=None):
    """The only part of the user message that differs between the answer schemas."""
    if (kind or schema()) == 'choice_only':       # attempt 001's line, byte for byte
        return f'Reply with exactly one of these JSON objects: {{"inspect": "{a}"}} or {{"inspect": "{b}"}}'
    return ('First write the expected total cost of the final map for each allowed action, then your choice. '
            f'Reply with one JSON object of exactly this form: {{"cost_if_inspect": {{"{a}": <number>, "{b}": <number>}}, "inspect": "<cell>"}} '
            f'where <cell> is {a} or {b}.')


def split_block(text):
    """(text before the consequence block, the block, text after it)."""
    head, rest = text.split(BLOCK_START, 1); block, tail = rest.split(BLOCK_END, 1)
    return head, block, tail


def squeeze(text):
    """A cell name with surrounding whitespace and spaces around the comma removed."""
    return re.sub(r'\s*,\s*', ',', text.strip())


def number(value):
    """A written cost as a float, or None. Numbers and numeric strings count; booleans, nulls and words do not."""
    if isinstance(value, bool): return None
    if isinstance(value, (int, float)): out = float(value)
    elif isinstance(value, str):
        try: out = float(value.strip())
        except ValueError: return None
    else: return None
    return out if out == out and abs(out) != float('inf') else None


def validate(obj, legal_cells, kind=None):
    """The local schema, by answer schema. For `choice_only` see the end of this function. For attempt 002, decided in advance (preregistration, "Attempt 002").
    Valid: one JSON object whose `inspect` is a string naming one of the two legal cells after trimming
    whitespace and removing spaces around the comma. Everything about `cost_if_inspect` and any extra key is
    tolerated and recorded in `work`. (The adapter has already rejected text that is not JSON, and any
    object that repeats a key.) Returns the choice, what was noted, and the object as returned, kept as JSON
    text so that its key order survives storage."""
    if type(obj) is not dict or 'inspect' not in obj: raise ValueError('answer_object_or_inspect_missing')
    value = obj['inspect']
    if type(value) is not str or squeeze(value) not in legal_cells: raise ValueError('answer_value')
    if (kind or schema()) == 'choice_only':
        # The original answer {"inspect": "<cell>"}: same validity rule; extra keys tolerated and recorded; no working field.
        work = {'extra_keys': [str(k)[:40] for k in obj if k != 'inspect'][:8], 'inspect_respaced': squeeze(value) != value}
        return {'inspect': squeeze(value), 'work': work, 'raw': json.dumps(obj)}
    key = design()['answer']['work_key']; written = obj.get(key); keys = list(obj)
    costs = {cell: None for cell in legal_cells}; spaced = strings = False; other = []
    if isinstance(written, dict):
        for k, v in written.items():
            cell = squeeze(k) if isinstance(k, str) else None
            if cell in costs and costs[cell] is None and number(v) is not None:
                costs[cell] = number(v); spaced = spaced or cell != k; strings = strings or isinstance(v, str)
            elif cell not in costs: other.append(str(k)[:40])
    work = {'costs': costs, 'work_malformed': any(v is None for v in costs.values()),
            'costs_as_strings': strings, 'cost_keys_respaced': spaced, 'cost_extra_keys': other[:8],
            'extra_keys': [str(k)[:40] for k in keys if k not in ('inspect', key)][:8],
            'cost_before_inspect': (keys.index(key) < keys.index('inspect')) if key in keys else None,
            'inspect_respaced': squeeze(value) != value}
    return {'inspect': squeeze(value), 'work': work, 'raw': json.dumps(obj)}


def scripted_answer(name, a):
    """The answer object a scripted policy returns: the analytic expected cost of each action, then its choice
    (only the choice in the `choice_only` schema)."""
    w = layout(a['layout'])
    if schema() == 'choice_only': return {'inspect': policy(name, a)}
    costs = {cell: sim.expected_loss(a['error'], a['unknown_cost'], sim.action_of(w, cell)) for cell in a['legal_cells']}
    return {design()['answer']['work_key']: costs, 'inspect': policy(name, a)}


def work_check(a, answer):
    """The written costs against the analytic expected cost of each action (U for inspecting the reported cell,
    e for the cell without evidence), and whether the choice contradicts the model's own two numbers. Reported,
    never gated."""
    w = layout(a['layout']); costs = answer['work']['costs']; tol = design()['answer']['work_tolerance']; out = {}
    for action in sim.ACTIONS:
        written = costs.get(sim.cell_of(w, action)); truth = sim.expected_loss(a['error'], a['unknown_cost'], action)
        out[f'cost_{action}'] = written
        out[f'abs_error_{action}'] = None if written is None else round(abs(written - truth), 12)
    both = all(out[f'cost_{x}'] is not None for x in sim.ACTIONS); chosen = sim.action_of(w, answer['inspect'])
    favour = None if not both else 'tie' if out['cost_check'] == out['cost_explore'] else min(sim.ACTIONS, key=lambda x: out[f'cost_{x}'])
    out.update(both_written=both, both_correct=both and all(out[f'abs_error_{x}'] <= tol for x in sim.ACTIONS),
               own_numbers_favour=favour, contradicts_own_numbers=bool(both and favour != 'tie' and favour != chosen))
    return out


# ------------------------------------------------------------------ assignments

@functools.lru_cache(maxsize=None)
def layout(seed):
    """Cached: callers must not mutate the returned mapping."""
    return sim.layout(seed)


def cases():
    d = design()
    return [(e, u) for e in d['error_probabilities'] for u in d['unknown_costs']]


def assignment(kind, seed, error, unknown_cost, representation, group=None):
    """One assignment in the answer schema of the chain's model."""
    w = layout(seed); user = user_text(w, error, unknown_cost, representation)
    prefix = {'engineering': 'g', 'main': 'm', 'qualification': 'q' + str(group)}[kind]
    return {'id': f'{prefix}-{seed}-e{round(error * 100):02d}-u{round(unknown_cost * 100):02d}-{representation}',
            'kind': kind, 'set': group, 'layout': seed, 'error': error, 'unknown_cost': unknown_cost,
            'representation': representation, 'legal_cells': list(w['legal_order']),
            'input_hash': digest([system(), user]), 'content_bytes': len(system().encode()) + len(user.encode())}


def user_for(a):
    return user_text(layout(a['layout']), a['error'], a['unknown_cost'], a['representation'])


def grid(kind):
    """Every case and both representations on every layout of the kind; the 24 requests of a layout in a seeded order."""
    out = []
    for seed in design()['layouts'][kind]:
        cells = [(e, u, rep) for e, u in cases() for rep in REPRESENTATIONS]
        sim.rng(seed, 'dispatch-order').shuffle(cells)
        out += [assignment(kind, seed, e, u, rep) for e, u, rep in cells]
    return out


def fixtures(group):
    """The 24 qualification fixtures of a set, in their frozen order: fixture i on layout i, both representations,
    the leading representation alternating. The first one is the interface probe (P0)."""
    q = design()['qualification']; seeds = design()['layouts'][f'qualification_{group}']; out = []
    for i, (seed, (e, u)) in enumerate(zip(seeds, q[f'fixtures_{group}'])):
        for rep in (REPRESENTATIONS if i % 2 == 0 else REPRESENTATIONS[::-1]):
            out.append(assignment('qualification', seed, float(e), float(u), rep, group))
    return out


def active_set():
    """The qualification set of the chain's model: the model's own `qualification_set`, else `qualification.set`."""
    return design()['models'][model()].get('qualification_set') or design()['qualification']['set']


@functools.lru_cache(maxsize=None)
def _build(stage, kind, group):
    assert kind == schema() and group == active_set()
    if stage == 'S0': return grid('engineering') + fixtures('a') + fixtures('b')
    if stage == 'P0': return fixtures(active_set())[:1]
    if stage == 'Q0': return fixtures(active_set())[1:]
    if stage == 'S1': return grid('main')
    raise ValueError('unknown_stage')


def _assignments(stage):
    """The stage's assignments for the chain's model (cached per answer schema)."""
    return _build(stage, schema(), active_set())


_assignments.cache_clear = _build.cache_clear


def assignments(stage):
    return [dict(a) for a in _assignments(stage)]


def policy(name, a):
    """Scripted reference policies. `optimal` is the analytic minimum-loss action; the others are offline comparators."""
    w = layout(a['layout'])
    if name == 'optimal': return sim.cell_of(w, sim.optimal_action(a['error'], a['unknown_cost']))
    if name == 'always_check': return w['report_cell']
    if name == 'always_explore': return w['unknown_cell']
    if name == 'always_first': return w['legal_order'][0]
    if name == 'always_second': return w['legal_order'][1]
    raise ValueError('unknown_policy')


def evaluate(a, choice, answer=None):
    """The grade of the choice (only `inspect` is graded) and, when the validated answer is given, the report on
    the written costs."""
    out = sim.score(layout(a['layout']), a['error'], a['unknown_cost'], choice)
    if answer is not None and 'costs' in answer['work']: out['work'] = work_check(a, answer)
    return out


def combine(rows):
    """One terminal row per unit from an original run followed by its continuations, in run order. A later
    row replaces an earlier one only when the earlier one was left not started; a completed or failed
    unit is never replaced."""
    final = {}
    for r in rows:
        if r['id'] not in final or final[r['id']]['status'] == 'not_started': final[r['id']] = r
    return list(final.values())


# ------------------------------------------------------------------ gates

def qualification(rows):
    """The program's gate over one set's 24 fixtures: valid structure throughout and at least 11 of 12
    optimal in each representation. `rows` must be exactly the 24 rows of one set."""
    q = design()['qualification']; out = {'assigned': len(rows), 'valid': sum(r['status'] == 'completed' for r in rows),
                                          'sets': sorted({str(r.get('set')) for r in rows}), 'misses': []}
    ok = len(rows) == q['valid_required'] and out['valid'] == q['valid_required'] and len({r['id'] for r in rows}) == len(rows) \
        and all(r['kind'] == 'qualification' for r in rows) and len(out['sets']) == 1
    for rep in REPRESENTATIONS:
        mine = [r for r in rows if r['representation'] == rep]
        optimal = sum(r['status'] == 'completed' and r['evaluation']['optimal'] for r in mine)
        out[rep] = {'assigned': len(mine), 'valid': sum(r['status'] == 'completed' for r in mine), 'optimal': optimal}
        out['misses'] += [r['id'] for r in mine if not (r['status'] == 'completed' and r['evaluation']['optimal'])]
        ok = ok and len(mine) == 12 and optimal >= q['optimal_required_per_format']
    out['passed'] = bool(ok)
    return out


def scripted_qualification(rows):
    """S0: the analytic policy must pass the gate on both frozen sets."""
    return {g: qualification([r for r in rows if r['kind'] == 'qualification' and r['set'] == g]) for g in ('a', 'b')}


PROBE_METADATA = ('response_model', 'response_provider', 'response_id', 'finish_reason', 'reasoning_tokens', 'latency_seconds',
                  'provider_reported_usd', 'computed_usd', 'actual_usd', 'reserved_usd', 'input_tokens', 'output_tokens', 'request_bytes', 'attempts',
                  'visible_output_tokens', 'cost_source', 'input_pricing', 'cached_tokens', 'system_fingerprint', 'rate_limits')


def probe_gate(rows):
    """P0 checks the interface. A completed row means the adapter accepted the response: it parsed, the model
    id matched, usage was reported, the finish reason was `stop`, and the answer passed local validation (on
    OpenRouter also: no reasoning tokens were billed and the response names the pinned provider, which this
    gate checks again; OpenAI has no provider routing, so there is nothing to check there). Whether the
    choice is optimal counts in Q0's gate. The raw response metadata of the one call is returned for the summary."""
    out = {'passed': False}
    if len(rows) != 1 or rows[0]['id'] != _assignments('P0')[0]['id']: return out
    acc = rows[0].get('accounting') or {}
    out.update({k: acc.get(k) for k in PROBE_METADATA}, content_bytes=rows[0]['content_bytes'])
    served = acc.get('response_provider')
    out['provider_is_pinned'] = (isinstance(served, str) and design()['provider'] in served.lower()) if provider_name() == 'openrouter' else None
    if acc.get('input_tokens'): out['tokens_per_byte'] = acc['input_tokens'] / rows[0]['content_bytes']
    out['passed'] = bool(rows[0]['status'] == 'completed' and out['provider_is_pinned'] is not False)
    return out


def qualification_rows(rows, probe_rows):
    """Q0's 23 rows plus P0's saved row, or None when P0's row is not the expected one at this source hash."""
    probe = list(probe_rows or [])
    if len(probe) != 1 or probe[0].get('id') != _assignments('P0')[0]['id'] or probe[0].get('source_hash') != source_hash():
        return None
    return probe + list(rows)


def gate(stage, rows, violations=(), probe_rows=None):
    """True or False for S0, P0 and Q0; None for S1, which has no gate of its own."""
    if stage == 'S1': return None
    if violations: return False
    if stage == 'S0':
        return all(q['passed'] for q in scripted_qualification(rows).values())
    if stage == 'P0':
        return probe_gate(rows)['passed']
    both = qualification_rows(rows, probe_rows)
    return bool(both) and qualification(both)['passed']


# ------------------------------------------------------------------ invariants

def numbers(text):
    return NUMBER.findall(text)


def largest_request_bytes(stage='S1'):
    """Bytes of the largest encoded request body of a stage (template plus both messages)."""
    t = provider_config()['request_template']; biggest = max(_assignments(stage), key=lambda a: a['content_bytes'])
    body = dict(t, messages=[{'role': 'system', 'content': system()}, {'role': 'user', 'content': user_for(biggest)}])
    return len(json.dumps(body).encode())


def check_request(a):
    """Violations of one assignment's request: legality, leaks, equal information, size."""
    out = []; w = layout(a['layout']); text = user_for(a); tag = a['id']
    rc, uc = w['report_cell'], w['unknown_cell']
    if sorted(a['legal_cells']) != sorted([rc, uc]) or rc == uc: out.append(f'{tag}:both_actions_must_be_legal')
    a1, a2 = a['legal_cells']
    if f'Allowed cells, in this order: {a1}; {a2}.' not in text or not text.endswith(answer_block(a1, a2)) \
            or (schema() == 'cost_then_choice' and f'{{"{a1}": <number>, "{a2}": <number>}}' not in text) \
            or (schema() == 'choice_only' and ('cost_if_inspect' in system() + text or not text.endswith(f'{{"inspect": "{a1}"}} or {{"inspect": "{a2}"}}'))):
        out.append(f'{tag}:legal_cells_not_listed_in_order')
    low = (system() + '\n' + text).lower()
    if any(word in low for word in FORBIDDEN) or str(a['layout']) in text: out.append(f'{tag}:forbidden_text')
    f = sim.facts(w, a['error'], a['unknown_cost'])
    if len(f['measurements']) != 34 or any(c in (rc, uc) for c, _ in f['measurements']): out.append(f'{tag}:measurements')
    if digest([system(), text]) != a['input_hash']: out.append(f'{tag}:input_hash')
    # equal information: the block states exactly the records, and so does the other representation's block
    want = shown(sim.consequences(w, a['error'], a['unknown_cost']))
    head, block, tail = split_block(text)
    try:
        if PARSE[a['representation']](block) != want or RENDER[a['representation']](want) != block: out.append(f'{tag}:block_is_not_exactly_the_records')
    except ValueError:
        out.append(f'{tag}:block_does_not_parse')
    other = next(r for r in REPRESENTATIONS if r != a['representation'])
    head2, block2, tail2 = split_block(user_text(w, a['error'], a['unknown_cost'], other))
    try:
        if PARSE[other](block2) != PARSE[a['representation']](block): out.append(f'{tag}:representations_state_different_facts')
    except ValueError:
        out.append(f'{tag}:other_block_does_not_parse')
    if (head, tail) != (head2, tail2): out.append(f'{tag}:text_outside_the_block_differs')
    if sorted(numbers(block)) != sorted(numbers(block2)): out.append(f'{tag}:numbers_differ_between_representations')
    cells = lambda s: set(re.findall(r'\d,\d', s))
    if cells(block) != cells(block2) or set(re.findall(r'LAND|WATER', block)) != set(re.findall(r'LAND|WATER', block2)):
        out.append(f'{tag}:cells_or_labels_differ_between_representations')
    if any(word in block.lower() + block2.lower() for word in ('expected', 'total', 'sum', 'average', 'prefer')):
        out.append(f'{tag}:block_states_more_than_consequences')
    return out


def check_layout(seed, pairs):
    """Within a layout only e, 1 - e, U and the representation change: with every two-decimal number masked the
    request is identical across cases, and the numbers differ only at the positions that hold e, 1 - e or U."""
    out = []; w = layout(seed); probe = (0.07, 0.31)        # no number of the probe equals another or a constant
    for rep in REPRESENTATIONS:
        text = user_text(w, probe[0], probe[1], rep)
        role = {'0.07': 'e', '0.93': 'r', '0.31': 'u'}
        roles = [role.get(n) for n in numbers(text)]; constants = numbers(text); skeleton = NUMBER.sub('#', text)
        if sorted(r for r in roles if r) != ['e', 'e', 'r', 'u']: out.append(f'{seed}:{rep}:case_number_positions')
        for e, u in pairs:
            actual = user_text(w, e, u, rep); value = {'e': fmt(e), 'r': fmt(1 - e), 'u': fmt(u)}
            if NUMBER.sub('#', actual) != skeleton: out.append(f'{seed}:{rep}:{e}:{u}:text_changes_beyond_the_numbers')
            if numbers(actual) != [value[r] if r else c for r, c in zip(roles, constants)]:
                out.append(f'{seed}:{rep}:{e}:{u}:numbers_change_beyond_e_and_u')
    return out


def policy_rows(rows, name):
    """The rows a scripted policy would produce (evaluator-side, no call)."""
    out = []
    for a in rows:
        answer = validate(scripted_answer(name, a), a['legal_cells'])
        out.append(dict(a, status='completed', answer=answer, evaluation=evaluate(a, answer['inspect'], answer)))
    return out


def check_design():
    """Structural facts of the frozen design that make the study informative. Returns violations."""
    out = []; d = design(); q = d['qualification']; main = cases(); L = d['layouts']; b = budget()
    best = [sim.optimal_action(e, u) for e, u in main]
    if len(main) != 12 or best.count('check') != 6 or best.count('explore') != 6: out.append('optimum_must_change_across_the_twelve_cases')
    seeds = [s for k in ('engineering', 'qualification_a', 'qualification_b', 'main') for s in L[k]]
    if len(set(seeds)) != len(seeds) or max(seeds) >= 10000 or len(L['main']) != 24: out.append('layout_seeds')
    combos = collections.Counter((layout(s)['legal_order'][0] == layout(s)['report_cell'], layout(s)['report_label']) for s in L['main'])
    if sorted(combos.values()) != [6, 6, 6, 6]: out.append('order_and_label_not_balanced_over_main_layouts')
    pairs = {g: [(float(e), float(u)) for e, u in q[f'fixtures_{g}']] for g in ('a', 'b')}
    if set(pairs['a']) & set(pairs['b']) or (set(pairs['a']) | set(pairs['b'])) & set(main): out.append('qualification_pairs_not_disjoint')
    for g in ('a', 'b'):
        if len(pairs[g]) != 12 or len(set(pairs[g])) != 12 or len(L[f'qualification_{g}']) != 12: out.append(f'qualification_{g}:count')
        if any(round(abs(e - u), 12) < q['min_margin'] for e, u in pairs[g]): out.append(f'qualification_{g}:margin_below_stated_minimum')
        if [sim.optimal_action(e, u) for e, u in pairs[g]] != ['check'] * 6 + ['explore'] * 6: out.append(f'qualification_{g}:six_check_then_six_explore')
        fx = fixtures(g)
        for half in (fx[:12], fx[12:]):
            first = sum(layout(a['layout'])['legal_order'][0] == layout(a['layout'])['report_cell'] for a in half)
            if first != 6: out.append(f'qualification_{g}:listing_order_not_balanced')
        if not qualification(policy_rows(fx, 'optimal'))['passed']: out.append(f'qualification_{g}:analytic_policy_fails')
        for name in POLICIES[1:]:
            result = qualification(policy_rows(fx, name))
            if result['passed'] or result['prose']['optimal'] != 6 or result['table']['optimal'] != 6:
                out.append(f'qualification_{g}:{name}_must_score_6_of_12_and_fail')
    for stage in STAGES:
        rows = _assignments(stage)
        if len(rows) != d['stages'][stage]['assignments'] or len({a['id'] for a in rows}) != len(rows): out.append(f'{stage}:assignment_count')
        if stage != 'S0' and len(rows) != b['max_calls'][stage]: out.append(f'{stage}:call_cap_differs_from_assignments')
    repair = q['repairs_allowed'] * q['valid_required']       # the repair attempt's P0 and Q0 calls, in the same ledger
    if sum(b['max_calls'].values()) + repair != b['max_attempted_calls']: out.append('study_call_cap')
    ladder = d['model_ladder']; tags = [d['models'][m]['tag'] for m in ladder] if set(d['models']) == set(ladder) else None
    if ladder[0] != d['model'] or set(d['providers']) != set(ladder) or tags is None or tags[0] != '' or len(set(tags)) != len(tags) \
            or d['providers'][ladder[0]] != 'openrouter' or any(d['models'][m]['answer_schema'] not in ('cost_then_choice', 'choice_only') for m in ladder):
        out.append('model_ladder')
    if 'json' not in (system() + user_for(_assignments('P0')[0])).lower(): out.append('json_mode_needs_the_word_json')
    if {a['id'] for a in _assignments('P0') + _assignments('Q0')} & {a['id'] for a in _assignments('S1')}: out.append('qualification_inside_main')
    biggest = max(largest_request_bytes(s) for s in ('P0', 'Q0', 'S1'))
    if biggest > b['max_input_bytes']: out.append('request_larger_than_max_input_bytes')
    if biggest / CHARS_PER_TOKEN_FLOOR > b['max_input_tokens']: out.append('request_may_exceed_the_input_ceiling')
    if b['max_failed'] != max(3, -(-len(_assignments('S1')) // 100)): out.append('max_failed_rule')
    return out


def check_invariants(stage):
    """Violations for a stage. S0 checks the design and every request of every stage; a paid stage re-checks
    its own requests before any call is made."""
    if stage == 'S0':
        out = check_design()
        for s in STAGES:
            for a in _assignments(s): out += check_request(a)
        d = design(); q = d['qualification']
        for seed in d['layouts']['engineering'] + d['layouts']['main']: out += check_layout(seed, cases())
        for g in ('a', 'b'):
            for seed, pair in zip(d['layouts'][f'qualification_{g}'], q[f'fixtures_{g}']):
                out += check_layout(seed, [(float(pair[0]), float(pair[1]))])
        return out
    return [v for a in _assignments(stage) for v in check_request(a)]
