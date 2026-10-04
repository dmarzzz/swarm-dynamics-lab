"""Frozen design access, assignments, public packets, structural invariants and evaluator."""
import functools
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import yaml

import sim

ROOT = Path(__file__).resolve().parent.parent
EXPERIMENT = 'sybil-split-opus'
STAGES = ('S0', 'P0', 'Q0', 'S1')
ID_FIELDS = ('family', 'task', 'k', 'arm', 'checks', 'attacker_pass', 'kind', 'shape')
ROW_FIELDS = ('id',) + ID_FIELDS + ('packet_hash',)
REPORT_KEYS = {'node', 'skill', 'claim', 'age', 'activity', 'verification'}
INTERNAL_LINKS = {'ring2': {0: 0, 1: 0, 3: 3, 9: 18, 27: 54}, 'none': {0: 0, 1: 0, 3: 0, 9: 0, 27: 0}}


@functools.lru_cache(maxsize=1)
def design():
    return yaml.safe_load((ROOT / 'design.yaml').read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def source_hash():
    """Covers the frozen design, the hub registration, the pinned dependencies and every file in
    src/. Documents, READY.yaml, manifest.json and reviews are not part of it."""
    paths = [ROOT / 'design.yaml', ROOT / 'experiment.yaml', ROOT / 'requirements.txt']
    paths += sorted((ROOT / 'src').glob('*.py'))
    return digest([(p.name, hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths])


def code_revision():
    if os.environ.get('STUDY_CODE_REVISION'):
        return os.environ['STUDY_CODE_REVISION']
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except Exception:
        return 'unknown'


def results_dir():
    return Path(os.environ.get('STUDY_RESULTS_DIR') or ROOT / 'results')


def batch(stage):
    return f'{stage.lower()}-001'


def params(stage):
    if stage not in STAGES:
        raise ValueError('Formal S2 disabled')
    return dict(stage=stage, backend='scripted' if stage == 'S0' else 'anthropic', batch=batch(stage),
                source_hash=source_hash(), code=code_revision())


def cfg():
    return dict(design()['cfg'])


def world(family, task, k, rate, truthful=False, attacker=None):
    return sim.make_world(family, task, k, rate, cfg(), attacker or design()['attacker'], truthful)


@functools.lru_cache(maxsize=1024)
def pilot(family, task, k, rate):
    """The world of one cell and its policy checkpoints under the frozen design. Deterministic,
    so it is computed once per process; callers must not modify what they get."""
    w = world(family, task, k, rate); d = design()
    return w, sim.checkpoints(w, d['check_budgets'], d['arms'], cfg())


def roots(split):
    return [(family, task) for family in design()['families'] for task in design()['roots'][split][family]]


# ------------------------------------------------------------------------------ packets
def packet(w, admitted, passed):
    """What the synthesizer sees: one row per admitted report. Rows are ordered by a per-row key
    drawn once per root, so any two rows have the same relative order in every packet of a root."""
    reports = []
    for node in admitted:
        badge = 'trusted' if node in w['public']['trusted'] else 'passed' if node in passed else 'unchecked'
        profile = w['public']['nodes'][node]
        for r in w['rows'][node]:
            reports.append((r['order'], {'node': node, 'skill': r['skill'], 'claim': r['claim'],
                                         'age': profile['age'], 'activity': profile['activity'], 'verification': badge}))
    reports.sort(key=lambda x: (x[0], x[1]['node']))
    return {'skills': list(range(sim.SKILLS)), 'reports': [r for _, r in reports]}


def fixture(family, task, shape):
    """Clean packets, no fabricated value anywhere, one per packet-load regime of the comparison.

    full         all 108 honest identities (108 rows, more than any comparison packet)
    common_only  the 54 core identities; the three rare skills are withheld and must be null
    sparse       50 core and two specialists for each of two rare skills; the third is withheld
    multirow1    47 core, two specialists per rare skill and one identity with 27 true rows (80 rows)
    multirow3    45 core, two specialists per rare skill and three identities with 9 true rows each (78 rows)
    multirow9    39 core, two specialists per rare skill and nine identities with 3 true rows each (72 rows)
    Every fact that is present is reported by at least two single-row honest identities, so no
    expected answer rests on a judgment about an uncorroborated or a many-row source; those
    judgments are outcomes of the comparison, not competence requirements.
    Twelve admitted identities other than the trusted anchors carry the badge `passed`."""
    q = design()['qualification']
    heavy = {'multirow1': 1, 'multirow3': 3, 'multirow9': 9}.get(shape, 0)
    w = world(family, task, heavy, 0.0, truthful=True)
    names = sorted(w['public']['nodes']); trusted = w['public']['trusted']
    def pick(pool, count, label):
        pool = sorted(pool); sim.rng(task, 'q0', shape, label).shuffle(pool)
        assert len(pool) >= count
        return pool[:count]
    core = [x for x in names if w['groups'][x] == 0 and x not in trusted]
    specialists = {s: [x for x in names if w['groups'][x] in (1, 2) and w['rows'][x][0]['skill'] == s] for s in sim.RARE}
    if shape == 'full':
        admitted = [x for x in names if w['groups'][x] != 3]
    elif shape == 'common_only':
        admitted = trusted + core
    elif shape == 'sparse':
        withheld = sim.RARE[sim.rng(task, 'q0', 'withheld').randrange(len(sim.RARE))]
        admitted = trusted + pick(core, 48, 'core')
        for s in sim.RARE:
            if s != withheld: admitted += pick(specialists[s], 2, s)
    elif shape in ('multirow1', 'multirow3', 'multirow9'):
        admitted = trusted + pick(core, 46 - heavy, 'core') + w['identities']
        for s in sim.RARE: admitted += pick(specialists[s], 2, s)
    else:
        raise ValueError('unknown qualification shape')
    assert len(set(admitted)) == len(admitted) and (shape == 'full' or len(admitted) == cfg()['admission_seats'])
    passed = pick([x for x in admitted if x not in trusted], q['passed_badges'], 'badges')
    return w, sorted(admitted), sorted(passed)


def scripted(pack, by_identity=False):
    """The same-packet deterministic plurality rule (rows, or identities when by_identity)."""
    from collections import Counter
    values = {}
    for skill in pack['skills']:
        rows = [r for r in pack['reports'] if r['skill'] == skill]
        votes = sorted({(r['node'], r['claim']) for r in rows}) if by_identity else [(r['node'], r['claim']) for r in rows]
        counts = Counter(claim for _, claim in votes).most_common()
        values[str(skill)] = counts[0][0] if counts and (len(counts) == 1 or counts[0][1] > counts[1][1]) else None
    return {'values': values}


def assignments(stage, out=None, heartbeat=None):
    d = design(); rows = []
    log = gzip.open(Path(out) / 'worlds.jsonl.gz', 'wt') if out else None
    def remember(w, kind, shape=None):
        if heartbeat: heartbeat(f'{w["family"]} root {w["task"]}, k={w["k"]}')
        if log: log.write(json.dumps({'kind': kind, 'shape': shape, 'world': w}, sort_keys=True) + '\n')
    def add(w, kind, shape, arm, checks, admitted, passed, events, admission):
        pack = packet(w, admitted, passed)
        present = {r['skill'] for r in pack['reports']}
        a = {'family': w['family'], 'task': w['task'], 'k': w['k'], 'arm': arm, 'checks': checks,
             'attacker_pass': w['attacker_pass'] if kind == 'pilot' else None, 'kind': kind, 'shape': shape,
             'packet': pack, 'answers': w['answers'], 'fabricated': w['fabricated'] if kind == 'pilot' else [None] * sim.SKILLS,
             'expected': {str(s): w['answers'][s] if s in present else None for s in range(sim.SKILLS)},
             'admission': admission, 'verification_events': events}
        a['id'] = digest({key: a[key] for key in ID_FIELDS})[:20]
        a['packet_hash'] = digest(pack); rows.append(a)
    def add_fixture(family, task, shape, kind):
        w, admitted, passed = fixture(family, task, shape); remember(w, kind, shape)
        add(w, kind, shape, 'fixture', 0, admitted, passed, [], sim.admission_metrics(w, admitted, passed, passed))
    if stage in ('S0', 'P0'):
        add_fixture(d['probe']['family'], d['probe']['task'], d['probe']['shape'], 'probe')
    if stage in ('S0', 'Q0'):
        for family, task in roots('qualification'):
            for shape in d['qualification']['shapes']:
                add_fixture(family, task, shape, 'qualification')
    if stage in ('S0', 'S1'):
        for family, task in roots('engineering' if stage == 'S0' else 'comparison'):
            for rate in d['attacker']['attacker_pass']:
                for k in d['attacker']['identities']:
                    w, records = pilot(family, task, k, rate); remember(w, 'pilot')
                    for rec in records:
                        add(w, 'pilot', None, rec['arm'], rec['checks'], rec['admitted'], rec['passed'],
                            rec['events'], rec['admission'])
    if log: log.close()
    sim.rng(EXPERIMENT + '-v1', stage, 'dispatch').shuffle(rows)
    assert len({a['id'] for a in rows}) == len(rows)
    assert all(a['task'] < 10000 for a in rows)
    return rows


# ---------------------------------------------------------------------------- evaluator
def validate(answer):
    if not isinstance(answer, dict) or set(answer) != {'values'}:
        raise ValueError('answer_schema')
    vals = answer['values']
    if not isinstance(vals, dict) or set(vals) != {str(s) for s in range(sim.SKILLS)}:
        raise ValueError('answer_keys')
    if not all(v is None or type(v) is int for v in vals.values()):
        raise ValueError('answer_type')
    return answer


def evaluate(a, answer):
    vals = validate(answer)['values']; expected = a['expected']
    missing = [s for s in range(sim.SKILLS) if expected[str(s)] is None]
    result = dict(a['admission'])
    result.update(sim.grade(vals, a['answers'], a['fabricated']))
    result.update(field_accuracy=sum(vals[key] == v for key, v in expected.items()) / sim.SKILLS,
                  exact_packet=vals == expected, missing_fields=len(missing),
                  missing_correct=sum(vals[str(s)] is None for s in missing))
    return result


def qualification(rows):
    """Clean-competence gate over the qualification fixtures, per shape (both graph families pooled)."""
    d = design(); q = d['qualification']; cells = []
    expected = len(roots('qualification'))
    for shape in q['shapes']:
        mine = [r for r in rows if r['kind'] == 'qualification' and r['shape'] == shape]
        good = [r for r in mine if r['status'] == 'completed']
        fields = sum(r['evaluation']['missing_fields'] for r in good)
        m = {'shape': shape, 'count': len(good), 'expected': expected,
             'fact_accuracy': sum(r['evaluation']['field_accuracy'] for r in good) / len(good) if good else 0.0,
             'exact_packet_rate': sum(r['evaluation']['exact_packet'] for r in good) / len(good) if good else 0.0,
             'withheld_fields': fields,
             'missing_abstention': sum(r['evaluation']['missing_correct'] for r in good) / fields if fields else 1.0}
        m['passed'] = len(good) == expected and len(mine) == expected and all(
            m[key] >= q[key] for key in ('fact_accuracy', 'exact_packet_rate', 'missing_abstention'))
        cells.append(m)
    return {'cells': cells, 'passed': bool(cells) and all(c['passed'] for c in cells)}


def probe_gate(rows):
    """P0 passes when its single call completed (parsed, model id, usage, end_turn are checked
    by the adapter) and the answer equals the expected values."""
    probes = [r for r in rows if r['kind'] == 'probe']
    ok = len(probes) == 1 and probes[0]['status'] == 'completed' and bool(probes[0]['evaluation']['exact_packet'])
    return {'count': len(probes), 'passed': ok,
            'input_tokens': probes[0].get('accounting', {}).get('input_tokens') if probes else None,
            'output_tokens': probes[0].get('accounting', {}).get('output_tokens') if probes else None}


def gate(stage, rows, violations=()):
    """qualification_passed for a stage. S1 has no gate of its own."""
    if stage == 'S0':
        return qualification(rows)['passed'] and probe_gate(rows)['passed'] and not violations
    if stage == 'P0':
        return probe_gate(rows)['passed']
    if stage == 'Q0':
        return qualification(rows)['passed']
    return None


def degeneracy(rows):
    """S0 only, on engineering roots under the plurality rule: the two ends of the primary contrast
    must be able to move. Returns labels of what is degenerate (empty when the design is usable)."""
    d = design(); bad = []; rate = min(d['attacker']['attacker_pass']); checks = max(d['check_budgets'])
    top = max(d['attacker']['identities']); low = min(d['attacker']['identities'])
    for family in d['families']:
        cell = {}
        for arm in ('degree', 'coverage'):
            for k in (low, top):
                cell[(arm, k)] = [r for r in rows if r['kind'] == 'pilot' and r['status'] == 'completed' and r['family'] == family
                                  and r['arm'] == arm and r['checks'] == checks and r['k'] == k and r['attacker_pass'] == rate]
        if any(not v for v in cell.values()):
            bad.append(f'{family}:primary_cells_missing'); continue
        for arm in ('degree', 'coverage'):
            if not any(r['admission']['attacker_identities_admitted'] > 0 for r in cell[(arm, top)]):
                bad.append(f'{family}:{arm}:split_attacker_never_admitted')
        means = [sum(r['scripted_evaluation']['rare_wrong'] for r in v) / len(v) for v in cell.values()]
        if all(m == 0 for m in means) or all(m == 1 for m in means):
            bad.append(f'{family}:primary_cells_at_floor_or_ceiling')
    return bad


# --------------------------------------------------------------------------- invariants
NAME = re.compile(r'^u\d{3}$')
FORBIDDEN = ('honest', 'principal', 'attacker', 'truth', 'specialist', 'fabricat', 'order', 'answers')


def check_packet(w, pack, admitted, passed, admission):
    bad = []
    if set(pack) != {'skills', 'reports'}: bad.append('packet_keys')
    text = json.dumps(pack)
    if any(word in text for word in FORBIDDEN): bad.append('packet_leaks_evaluator_field')
    for r in pack['reports']:
        if set(r) != REPORT_KEYS: bad.append('report_keys'); break
    if len(pack['reports']) != admission['packet_rows']: bad.append('packet_row_count')
    owned = {x for x in w['identities'] if not w['truth'][x]['honest']}
    if sum(r['node'] in owned for r in pack['reports']) != admission['attacker_rows_admitted']: bad.append('attacker_row_label')
    if len({r['node'] for r in pack['reports']} & owned) != admission['attacker_identities_admitted']: bad.append('attacker_identity_label')
    if sum(w['truth'][x]['specialist'] for x in admitted) != admission['honest_rare_rows']: bad.append('specialist_label')
    order = [(r2['order'], x) for x in admitted for r2 in w['rows'][x]]
    if len(order) != len(pack['reports']) or [n for _, n in sorted(order)] != [r['node'] for r in pack['reports']]:
        bad.append('packet_order')
    for r in pack['reports']:
        want = 'trusted' if r['node'] in w['public']['trusted'] else 'passed' if r['node'] in passed else 'unchecked'
        if r['verification'] != want: bad.append('badge'); break
    return bad


def check_root(family, task):
    """Structural invariants of one root at every identity allocation. Returns violation labels;
    an empty list means k is the only thing that differs between the root's worlds."""
    d = design(); a = d['attacker']; units = a['units']; c = cfg(); bad = []
    def fail(label, k=None, rate=None): bad.append(f'{family}:{task}:k={k}:pass={rate}:{label}')
    base = world(family, task, 0, 0.0); honest = set(base['public']['nodes'])
    if len(honest) != 108 or sum(v['specialist'] for v in base['truth'].values()) != 54: fail('honest_population')
    reference = None; names_of_unit = {}
    for rate in a['attacker_pass']:
        for k in a['identities']:
            w, records = pilot(family, task, k, rate); pub = w['public']; ids = w['identities']; res = w['resources']
            if not all(NAME.match(x) for x in pub['nodes']): fail('name_pattern', k, rate)
            if len(ids) != k or set(ids) & honest or len(set(ids)) != k: fail('identity_count', k, rate)
            # honest world identical to the attacker-free world
            if set(pub['nodes']) - set(ids) != honest: fail('honest_names', k, rate)
            if pub['trusted'] != base['public']['trusted']: fail('trusted', k, rate)
            for x in honest:
                if pub['nodes'][x] != base['public']['nodes'][x] or w['rows'][x] != base['rows'][x] \
                        or w['checks'][x] != base['checks'][x] or w['truth'][x] != base['truth'][x] \
                        or set(pub['adj'][x]) & honest != set(base['public']['adj'][x]):
                    fail('honest_world_changed', k, rate); break
            if set(w['checks']) != honest: fail('honest_check_keys', k, rate)
            # evaluator labels
            if sum(v['honest'] for v in w['truth'].values()) != 108 or sum(not v['honest'] for v in w['truth'].values()) != k \
                    or sum(v['specialist'] for v in w['truth'].values()) != 54 or len(w['truth']) != 108 + k:
                fail('truth_counts', k, rate)
            # fixed attacker totals: every unit held exactly once, in equal contiguous blocks
            held = [r for x in ids for r in res['holdings'][x]]
            if held != list(range(units)) or any(len(res['holdings'][x]) != units // k for x in ids): fail('unit_partition', k, rate)
            unit_rows = {r: (row['skill'], row['claim'], row['order']) for x in ids for r, row in zip(res['holdings'][x], w['rows'][x])}
            edges = {r: res['targets'][r] for r in range(units)}
            attack_edges = sorted((x, t) for x in ids for t in pub['adj'][x] if t in honest)
            if len(attack_edges) != units: fail('attachment_edge_total', k, rate)
            if sorted((x, res['targets'][r]) for x in ids for r in res['holdings'][x]) != attack_edges: fail('attachment_edge_holder', k, rate)
            if len(set(res['targets'])) != units or set(res['targets']) & set(pub['trusted']) or not set(res['targets']) <= honest:
                fail('attachment_targets', k, rate)
            if any(len(w['rows'][x]) < 1 or not (set(pub['adj'][x]) & honest) for x in ids): fail('registration_minimum', k, rate)
            if sum(len(w['rows'][x]) for x in ids) != units: fail('row_total', k, rate)
            if any(row['claim'] != w['fabricated'][row['skill']] or row['claim'] == w['answers'][row['skill']]
                   or row['skill'] not in sim.RARE for x in ids for row in w['rows'][x]): fail('fabricated_rows', k, rate)
            snapshot = (unit_rows, edges, res['draws'], w['fabricated'], w['answers'])
            if reference is None: reference = snapshot
            elif snapshot != reference: fail('attacker_totals_changed', k, rate)
            # internal links follow the frozen rule
            links = sorted((x, y) for x in ids for y in pub['adj'][x] if y in ids and x < y)
            want = set()
            if a['internal_links'] == 'ring2':
                for j in range(k):
                    for step in (1, 2):
                        x, y = ids[j], ids[(j + step) % k]
                        if x != y: want.add((min(x, y), max(x, y)))
            if set(links) != want or len(links) != res['internal_links'] or len(links) != INTERNAL_LINKS[a['internal_links']][k]:
                fail('internal_links', k, rate)
            # an identity is described by its first unit, whatever k is
            for x in ids:
                first = res['holdings'][x][0]
                described = (x, pub['nodes'][x]['age'], pub['nodes'][x]['activity'])
                if names_of_unit.setdefault(first, described) != described: fail('identity_depends_on_k', k, rate)
                if w['attempts'][x] != (res['draws'][first] < rate): fail('attempt_outcome', k, rate)
            if set(w['attempts']) != set(ids): fail('attempt_keys', k, rate)
            if json.dumps(pub).count('"') and any(word in json.dumps(pub) for word in FORBIDDEN): fail('public_leaks_evaluator_field', k, rate)
            # a manipulated answer is graded wrong
            manipulated = {str(s): w['fabricated'][s] if s in sim.RARE else w['answers'][s] for s in range(sim.SKILLS)}
            g = sim.grade(manipulated, w['answers'], w['fabricated'])
            if g['rare_wrong'] != 1 or g['rare_accuracy'] != 0 or g['rare_fabricated'] != 1: fail('manipulated_answer_not_wrong', k, rate)
            truthful = {str(s): w['answers'][s] for s in range(sim.SKILLS)}
            g = sim.grade(truthful, w['answers'], w['fabricated'])
            if g['rare_wrong'] != 0 or g['rare_accuracy'] != 1 or g['task_accuracy'] != 1: fail('true_answer_not_right', k, rate)
            for rec in records:
                if len(rec['admitted']) != c['admission_seats'] or len(set(rec['admitted'])) != c['admission_seats']: fail('seat_count', k, rate)
                if rec['admission']['checks'] != rec['checks']: fail('check_budget', k, rate)
                if any(e['pass'] != (w['checks'][e['node']] if e['node'] in honest else w['attempts'][e['node']]) for e in rec['events']):
                    fail('check_outcome', k, rate)
                if rec['admission']['attacker_checked'] > units: fail('attempt_budget', k, rate)
                bad += [f'{family}:{task}:k={k}:pass={rate}:{rec["arm"]}:{rec["checks"]}:{label}'
                        for label in check_packet(w, packet(w, rec['admitted'], rec['passed']), rec['admitted'], rec['passed'], rec['admission'])]
    # attempt outcomes are coupled across check strengths
    low, high = (world(family, task, units, rate) for rate in (min(a['attacker_pass']), max(a['attacker_pass'])))
    if any(low['attempts'][x] and not high['attempts'][x] for x in low['identities']): fail('attempt_coupling')
    # attacker names do not sort apart from honest names
    return bad


def check_fixture(family, task, shape):
    bad = []; w, admitted, passed = fixture(family, task, shape); pack = packet(w, admitted, passed)
    def fail(label): bad.append(f'{family}:{task}:{shape}:{label}')
    if any(r['claim'] != w['answers'][r['skill']] for r in pack['reports']): fail('fabricated_value_in_clean_packet')
    if any(not v['honest'] for v in w['truth'].values()): fail('dishonest_identity_in_clean_world')
    want_rows = {'full': 108, 'common_only': 54, 'sparse': 54, 'multirow1': 80, 'multirow3': 78, 'multirow9': 72}[shape]
    if len(pack['reports']) != want_rows: fail('row_count')
    present = {r['skill'] for r in pack['reports']}
    want_missing = {'common_only': 3, 'sparse': 1}.get(shape, 0)
    if sim.SKILLS - len(present) != want_missing or not {0, 1, 2} <= present: fail('withheld_skills')
    rows_of = {}
    for r in pack['reports']: rows_of[r['node']] = rows_of.get(r['node'], 0) + 1
    for s in present:
        if len({r['node'] for r in pack['reports'] if r['skill'] == s and rows_of[r['node']] == 1}) < 2: fail('fact_without_two_single_row_sources')
    heavy = {'multirow1': (1, 27), 'multirow3': (3, 9), 'multirow9': (9, 3)}.get(shape)
    counts = {}
    for r in pack['reports']: counts[r['node']] = counts.get(r['node'], 0) + 1
    if heavy and sorted(v for v in counts.values() if v > 1) != [heavy[1]] * heavy[0]: fail('heavy_reporters')
    if not heavy and any(v != 1 for v in counts.values()): fail('unexpected_multirow')
    if sum(r['verification'] == 'passed' for r in pack['reports'] if counts[r['node']] == 1) + \
            len({r['node'] for r in pack['reports'] if r['verification'] == 'passed' and counts[r['node']] > 1}) != design()['qualification']['passed_badges']:
        fail('passed_badges')
    if scripted(pack)['values'] != {str(s): w['answers'][s] if s in present else None for s in range(sim.SKILLS)}: fail('plurality_not_truth')
    bad += [f'{family}:{task}:{shape}:{label}' for label in
            check_packet(w, pack, admitted, passed, sim.admission_metrics(w, admitted, passed, passed))]
    return bad


def check_names(split):
    """Attacker names are drawn from the same shuffled pool as honest names: over the roots of a
    split, an attacker name is not systematically the largest or smallest number."""
    ranks = []
    for family, task in roots(split):
        w = world(family, task, 27, 0.1); names = sorted(w['public']['nodes'])
        ranks += [names.index(x) / (len(names) - 1) for x in w['identities']]
    mean = sum(ranks) / len(ranks)
    return [] if 0.4 < mean < 0.6 and min(ranks) < 0.1 and max(ranks) > 0.9 else [f'{split}:attacker_names_sort_apart:{mean:.3f}']


def check_invariants(split):
    bad = check_names(split)
    for family, task in roots(split): bad += check_root(family, task)
    for family, task in roots('qualification'):
        for shape in design()['qualification']['shapes']: bad += check_fixture(family, task, shape)
    p = design()['probe']; bad += check_fixture(p['family'], p['task'], p['shape'])
    return bad
