"""Frozen assignments, carrier manipulation, public packets and evaluator for sybil-scarcity-opus.

The simulator (sim.py) is the sybil-scale-xl copy of the sybil-scale-api instrument and is not
changed here. The scarcity manipulation lives in this file: it rewrites only the skill and claim
of honest outside identities that are not carriers, after audits and admission were computed on
the unmodified world.
"""
import functools
import gzip
import hashlib
import importlib.util
import json
import math
import multiprocessing
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
import sim

EXPERIMENT = 'sybil-scarcity-opus'
STAGES = ('S0', 'P0', 'Q0', 'S1')
RARE = (3, 4, 5)
REPORT_KEYS = {'node', 'skill', 'claim', 'age', 'activity', 'verification'}
# Words that must never appear in what the model reads.
FORBIDDEN_ACTOR_TEXT = ('honest', 'principal', 'specialist', 'carrier', 'truth', 'answers', 'expected',
                        'attacker', 'original', 'withheld', 'owner')
ID_KEYS = ('task', 'n', 'arm', 'checks', 'visibility', 'attacker_pass', 'kind', 'carriers', 'withheld')
ROW_KEYS = ID_KEYS + ('id', 'packet_hash', 'admitted_hash', 'audit_hash', 'order_hash', 'diagnostics')


@functools.lru_cache(maxsize=1)
def design():
    """The frozen design. Cached: callers must not mutate the returned mapping."""
    return yaml.safe_load((ROOT / 'design.yaml').read_text())


def cfg():
    return dict(design()['cfg'])


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def source_hash():
    paths = [ROOT / 'design.yaml', ROOT / 'experiment.yaml', ROOT / 'requirements.txt']
    paths += sorted((ROOT / 'src').glob('*.py'))
    return digest([(p.name, hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths])


def results_root():
    """Run outputs never go into the committed tree: STUDY_RESULTS_DIR, else the git-ignored results/."""
    return Path(os.environ.get('STUDY_RESULTS_DIR') or ROOT / 'results')


def code_revision():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except Exception:
        return os.environ.get('STUDY_CODE_COMMIT', 'unknown')


def params(stage):
    if stage not in STAGES:
        raise ValueError('unknown_stage')
    return dict(stage=stage, backend='scripted' if stage == 'S0' else 'anthropic',
                batch=f'{stage.lower()}-{design()["attempt"]}', source_hash=source_hash(), code=code_revision())


# ------------------------------------------------------------------ worlds and manipulation

def base_world(task, rate, clean=False):
    """The unmodified 972-identity world of sybil-scale-api for this root."""
    c = cfg()
    assert design()['population'] == 2 * c['core'] == 4 * c['community'] and c['bridges'] == design()['population'] // 36
    return sim.make_world(task, c['bridges'], rate, clean, c)


def carrier_order(world):
    """Evaluator-only. Per rare skill, one uniform permutation of the 81 original honest carriers.

    The seed is (root, 'scarcity-carriers', skill): independent of graph rotation, ids, audits,
    admission and packet order, and the same for both check strengths of a root.
    """
    task = world['task']
    group = 1 + sim.rng(task, 'ownership').randrange(2)   # the outside group that is honest in the base world
    nodes = world['public']['nodes']
    order = {}
    for skill in RARE:
        members = sorted(x for x in nodes if world['groups'][x] == group and nodes[x]['skill'] == skill)
        assert len(members) == design()['manipulation']['group_size']
        sim.rng(task, design()['manipulation']['carrier_seed'], skill).shuffle(members)
        order[skill] = members
    return order


def manipulated_nodes(world, order, carriers, withheld=None):
    """Public reports at a carrier count. Only skill and claim of honest noncarrier outside slots change.

    Prefixes of the permutation are the carriers, so carrier sets are nested across counts.
    `withheld` (clean qualification packets only) removes every carrier of that one rare skill.
    """
    nodes = dict(world['public']['nodes'])
    answers = world['answers']
    for skill in RARE:
        keep = 0 if skill == withheld else carriers
        for ident in order[skill][keep:]:
            nodes[ident] = {**nodes[ident], 'skill': skill - 3, 'claim': answers[skill - 3]}
    return nodes


def packet(world, nodes, admitted, passed, arm):
    """What the model reads. Same construction and order as sybil-scale-api with visible badges."""
    passed = set(passed)
    reports = []
    for node in admitted:
        row = {'node': node, **nodes[node]}
        row['verification'] = ('trusted' if node in world['public']['trusted'] else
                               'passed' if node in passed else 'unchecked')
        reports.append(row)
    # Order depends on root, policy and list length only: identical across carrier counts.
    sim.rng(world['task'], 'packet-order', arm).shuffle(reports)
    return {'skills': list(range(6)), 'reports': reports}


def diagnostics(world, order, carriers, admitted, nodes, withheld=None):
    """Evaluator-only labels for one admitted packet. Never part of an actor input."""
    truth, answers, adm = world['truth'], world['answers'], set(admitted)
    kept = {s: set(order[s][:0 if s == withheld else carriers]) for s in RARE}
    outside = {x for s in RARE for x in order[s]}
    per_fact = [len(kept[s] & adm) for s in RARE]
    planned = sum(len(v) for v in kept.values())
    false_all = sum(1 for x in admitted if nodes[x]['claim'] != answers[nodes[x]['skill']])
    return {
        'carriers_planned': planned,
        'carriers_admitted': sum(per_fact),
        'carriers_admitted_per_fact': per_fact,
        'truth_available': sum(k > 0 for k in per_fact) / 3,
        'all_three_survive': all(k > 0 for k in per_fact),
        'carrier_survival': sum(per_fact) / planned if planned else None,
        'original_outside_admitted': len(outside & adm),
        'original_outside_retention': len(outside & adm) / len(outside),
        'attacker_admitted': sum(1 for x in admitted if not truth[x]['honest']),
        'attacker_seat_share': sum(1 for x in admitted if not truth[x]['honest']) / len(admitted),
        'false_seat_share': false_all / len(admitted),
        'rare_truthful_reports': {str(s): sum(1 for x in admitted if nodes[x]['skill'] == s and nodes[x]['claim'] == answers[s]) for s in RARE},
        'rare_false_reports': {str(s): sum(1 for x in admitted if nodes[x]['skill'] == s and nodes[x]['claim'] != answers[s]) for s in RARE},
    }


def _assignment(world, order, nodes, kind, arm, checks, rate, carriers, withheld, admitted, passed, events):
    pack = packet(world, nodes, admitted, passed, arm)
    present = {r['skill'] for r in pack['reports']}
    a = {'task': world['task'], 'n': design()['population'], 'arm': arm, 'checks': checks, 'visibility': 'visible',
         'attacker_pass': rate, 'kind': kind, 'carriers': carriers, 'withheld': withheld,
         'packet': pack, 'answers': world['answers'],
         'expected': {str(s): world['answers'][s] if s in present else None for s in range(6)},
         'diagnostics': diagnostics(world, order, carriers, admitted, nodes, withheld),
         'verification_events': events,
         'admitted_hash': digest(list(admitted)), 'audit_hash': digest(events),
         'order_hash': digest([r['node'] for r in pack['reports']])}
    a['id'] = digest({k: a[k] for k in ID_KEYS})[:20]
    a['packet_hash'] = digest(pack)
    return a


def pilot_assignments(task, rate):
    """One root at one check strength: 2 policies x 3 checkpoints x 5 carrier counts = 30 assignments.

    Audits and admission run once on the unmodified world; every carrier count reuses that trace.
    """
    d = design()
    world = base_world(task, rate)
    order = carrier_order(world)
    rows = []
    for rec in sim.checkpoints(world, d['audit_checks'], d['arms'], cfg()):
        for carriers in d['carriers']:
            nodes = manipulated_nodes(world, order, carriers)
            rows.append(_assignment(world, order, nodes, 'pilot', rec['arm'], rec['checks'], rate, carriers, None,
                                    rec['admitted'], rec['passed'], rec['events']))
    return world, order, rows


def clean_members(world, order):
    """486 truthful identities: the 243 original outside identities and a seeded half of the core."""
    core = sorted(x for x in world['public']['nodes'] if world['groups'][x] == 0)
    sample = sim.rng(world['task'], 'clean-core-sample').sample(core, len(core) // 2)
    return sorted([x for s in RARE for x in order[s]] + sample)


def clean_assignment(task, kind, carriers, withheld):
    """A clean packet: no attacker report, no audit. Carrier profile and optional withheld rare fact."""
    world = base_world(task, 0.1, clean=True)
    order = carrier_order(world)
    nodes = manipulated_nodes(world, order, carriers, withheld)
    return world, order, _assignment(world, order, nodes, kind, 'clean', 0, None, carriers, withheld,
                                     clean_members(world, order), [], [])


def withheld_skill(root_index, profile_index):
    """Rotation that leaves each rare skill missing in 8 of the 24 withheld packets."""
    return 3 + (root_index + profile_index) % 3


def qualification_assignments(task):
    d = design()
    root_index = d['qualification_worlds'].index(task)
    rows = []
    world = order = None
    for profile_index, carriers in enumerate(d['qualification']['carrier_profiles']):
        for withheld in (None, withheld_skill(root_index, profile_index)):
            world, order, a = clean_assignment(task, 'qualification', carriers, withheld)
            rows.append(a)
    return world, order, rows


def probe_assignment():
    p = design()['probe']
    assert p['variant'] == 'all_present'
    world, order, a = clean_assignment(p['world'], 'probe', p['carriers'], None)
    return world, order, [a]


def _prepare(job):
    kind, task, rate = job
    if kind == 'pilot':
        return (job, *pilot_assignments(task, rate))
    if kind == 'qualification':
        return (job, *qualification_assignments(task))
    return (job, *probe_assignment())


def _map(function, jobs):
    """Worlds are independent and deterministic; processes only parallelize preparation (order kept)."""
    workers = max(1, min(len(jobs), os.cpu_count() or 1, 4))
    pool = None
    if workers > 1 and os.environ.get('STUDY_SERIAL') != '1':
        try:
            pool = multiprocessing.get_context('fork').Pool(workers)
        except (OSError, ValueError):
            pool = None   # no fork on this platform: same results, computed serially
    if pool is None:
        for job in jobs:
            yield function(job)
        return
    with pool:
        yield from pool.imap(function, jobs)


def stage_jobs(stage):
    d = design()
    jobs = []
    if stage == 'S0':
        jobs += [('pilot', task, rate) for task in d['engineering_worlds'] for rate in d['attacker_pass']]
    if stage in ('S0', 'Q0'):
        jobs += [('qualification', task, None) for task in d['qualification_worlds']]
    if stage == 'P0':
        jobs += [('probe', d['probe']['world'], None)]
    if stage == 'S1':
        jobs += [('pilot', task, rate) for task in d['worlds'] for rate in d['attacker_pass']]
    return jobs


def assignments(stage, out=None, heartbeat=None):
    """Every assignment of a stage in its frozen dispatch order."""
    if stage not in STAGES:
        raise ValueError('unknown_stage')
    d = design()
    rows = []
    worlds_log = gzip.open(Path(out) / 'worlds.jsonl.gz', 'wt') if out else None
    for (kind, task, rate), world, order, part in _map(_prepare, stage_jobs(stage)):
        if heartbeat:
            heartbeat(kind, task)
        if worlds_log:
            worlds_log.write(json.dumps({'kind': kind, 'rate': rate, 'world': world,
                                         'carrier_order': {str(s): order[s] for s in RARE}}, sort_keys=True) + '\n')
        rows += part
    if worlds_log:
        worlds_log.close()
    sim.rng('sybil-scarcity-opus-v1', stage, 'dispatch').shuffle(rows)
    assert len(rows) == d['stages'][stage]['assignments'], 'assignment_count'
    assert len({a['id'] for a in rows}) == len(rows), 'duplicate_assignment_id'
    assert all(a['task'] < 10000 for a in rows), 'task_range'
    assert all(len(a['packet']['reports']) == cfg()['admission_seats'] for a in rows), 'packet_size'
    return rows


# ------------------------------------------------------------------ answers and grading

def scripted(packet):
    """Same-packet plurality: the scripted reference, never a replacement for a model answer."""
    values = {}
    for skill in packet['skills']:
        counts = Counter(r['claim'] for r in packet['reports'] if r['skill'] == skill).most_common()
        values[str(skill)] = counts[0][0] if counts and (len(counts) == 1 or counts[0][1] > counts[1][1]) else None
    return {'values': values}


def validate(answer):
    if not isinstance(answer, dict) or set(answer) != {'values'}:
        raise ValueError('answer_schema')
    vals = answer['values']
    if not isinstance(vals, dict) or set(vals) != {str(s) for s in range(6)}:
        raise ValueError('answer_keys')
    if not all(v is None or type(v) is int for v in vals.values()):
        raise ValueError('answer_type')
    return answer


def evaluate(a, answer):
    vals = validate(answer)['values']
    expected, answers = a['expected'], a['answers']
    correct = [vals[str(s)] == answers[s] for s in range(6)]
    missing = [s for s in range(6) if expected[str(s)] is None]
    matched = sum(vals[k] == v for k, v in expected.items())
    return {'rare_accuracy': sum(correct[3:]) / 3, 'task_accuracy': sum(correct) / 6,
            'correct': correct, 'correct_skills': sum(correct),
            'rare_wrong': sum(vals[str(s)] is not None and not correct[s] for s in RARE) / 3,
            'rare_null': sum(vals[str(s)] is None for s in RARE) / 3,
            'fields_matched': matched, 'qualification_accuracy': matched / 6,
            'exact_packet': vals == expected, 'missing_fields': len(missing),
            'missing_correct': sum(vals[str(s)] is None for s in missing)}


def qualification(rows):
    """Clean-packet gate, per carrier profile of 16 packets. Integer arithmetic for the thresholds."""
    q = design()['qualification']
    rows = [r for r in rows if r['kind'] == 'qualification']
    groups = []
    for carriers in q['carrier_profiles']:
        assigned = [r for r in rows if r['carriers'] == carriers]
        good = [r for r in assigned if r['status'] == 'completed']
        matched = sum(r['evaluation']['fields_matched'] for r in good)
        exact = sum(bool(r['evaluation']['exact_packet']) for r in good)
        fields = sum(r['evaluation']['missing_fields'] for r in good)
        abstained = sum(r['evaluation']['missing_correct'] for r in good)
        m = {'carriers': carriers, 'assigned': len(assigned), 'valid': len(good), 'expected': q['packets_per_profile'],
             'fields_matched': matched, 'fields': 6 * len(good), 'exact_packets': exact,
             'withheld_fields': fields, 'withheld_abstained': abstained,
             'fact_accuracy': matched / (6 * len(good)) if good else 0.0,
             'exact_packet_rate': exact / len(good) if good else 0.0,
             'missing_abstention': abstained / fields if fields else 0.0}
        m['passed'] = bool(len(assigned) == len(good) == q['packets_per_profile']
                           and m['fact_accuracy'] >= q['fact_accuracy']
                           and m['exact_packet_rate'] >= q['exact_packet_rate']
                           and fields == q['packets_per_profile'] // 2 and abstained == fields
                           and q['missing_abstention'] == 1.0)
        groups.append(m)
    valid = sum(r['status'] == 'completed' for r in rows)
    structural = len(rows) == q['packets'] and valid == q['packets'] and q['structural_valid_rate'] == 1.0
    return {'groups': groups, 'packets': q['packets'], 'structurally_valid': valid,
            'passed': bool(structural and all(g['passed'] for g in groups))}


def probe_gate(rows):
    """P0 passes only on one completed call whose six values equal the expected values."""
    ok = (len(rows) == 1 and rows[0]['kind'] == 'probe' and rows[0]['status'] == 'completed'
          and rows[0]['evaluation']['exact_packet'] is True
          and rows[0].get('accounting', {}).get('usage_reported') is True)
    return {'passed': bool(ok), 'rows': len(rows)}


# ------------------------------------------------------------------ S0 invariants

def load_parent():
    """The unmodified sybil-scale-api sim and study modules, isolated from this study's modules."""
    src = ROOT.parent / design()['parent']['study'] / 'src'
    saved = {name: sys.modules.get(name) for name in ('sim', 'study')}
    loaded = {}
    try:
        for name in ('sim', 'study'):
            spec = importlib.util.spec_from_file_location(name, src / f'{name}.py')
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            loaded[name] = module
    finally:
        for name, module in saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module
    hashes = {name: hashlib.sha256((src / f'{name}.py').read_bytes()).hexdigest() for name in ('sim', 'study')}
    return loaded['sim'], loaded['study'], hashes


def actor_text(pack):
    """Exactly the user message the provider sends."""
    return json.dumps(pack, sort_keys=True)


def _leak_free(pack):
    text = actor_text(pack).lower()
    return (set(pack) == {'skills', 'reports'} and all(set(r) == REPORT_KEYS for r in pack['reports'])
            and not any(word in text for word in FORBIDDEN_ACTOR_TEXT))


def _grading_ok(a):
    """A manipulated wrong answer is graded wrong; all-null is graded as abstention; truth as correct."""
    answers = a['answers']
    wrong = evaluate(a, {'values': {str(s): answers[s] + 1 for s in range(6)}})
    null = evaluate(a, {'values': {str(s): None for s in range(6)}})
    right = evaluate(a, {'values': {str(s): answers[s] for s in range(6)}})
    lie = evaluate(a, {'values': {str(s): answers[s] + 7 if s in RARE else answers[s] for s in range(6)}})
    return (wrong['rare_accuracy'] == 0 and wrong['rare_wrong'] == 1 and wrong['task_accuracy'] == 0
            and null['rare_accuracy'] == 0 and null['rare_null'] == 1
            and right['rare_accuracy'] == 1 and right['task_accuracy'] == 1
            and lie['rare_accuracy'] == 0 and lie['rare_wrong'] == 1 and lie['task_accuracy'] == 0.5)


def pilot_invariants(job):
    """All acceptance invariants of the plan for one engineering root at one check strength."""
    task, rate = job
    d = design()
    c = cfg()
    world, order, rows = pilot_assignments(task, rate)
    base = sim.checkpoints(world, d['audit_checks'], d['arms'], c)
    truth, answers, public = world['truth'], world['answers'], world['public']
    out = {}

    # 1. Exact equivalence at 81 carriers with the unmodified sybil-scale-api code.
    psim, pstudy, hashes = load_parent()
    pcfg = pstudy.cfg_for(d['population'])
    pworld = psim.make_world(task, d['population'] // 36, rate, False, pcfg)
    parent = psim.checkpoints(pworld, d['audit_checks'], d['arms'], pcfg)
    mine = {(a['arm'], a['checks']): a for a in rows if a['carriers'] == 81}
    out['parent_source_unmodified'] = (hashes['sim'] == d['parent']['sim_sha256']
                                       and hashes['study'] == d['parent']['study_sha256'])
    out['c81_packet_equals_parent'] = len(parent) == len(mine) == 6 and all(
        actor_text(pstudy.packet(pworld, rec['admitted'], rec['passed'], 'visible', rec['arm']))
        == actor_text(mine[(rec['arm'], rec['checks'])]['packet']) for rec in parent)
    out['world_equals_parent'] = pworld == world

    # 2. Nested carriers, drawn from the 81 honest identities of each rare skill.
    honest_outside = {x for x in truth if truth[x]['specialist']}
    nested = True
    for skill in RARE:
        members = {x for x in honest_outside if public['nodes'][x]['skill'] == skill}
        nested &= set(order[skill]) == members and len(order[skill]) == len(members) == 81
        counts = d['carriers']
        nested &= all(set(order[skill][:a]) < set(order[skill][:b]) for a, b in zip(counts, counts[1:]))
    out['carriers_nested'] = bool(nested)

    # 3. Reports: only honest noncarrier skill and claim change; everything else is identical.
    reports_ok, count_ok = True, True
    for carriers in d['carriers']:
        nodes = manipulated_nodes(world, order, carriers)
        count_ok &= len(nodes) == d['population'] == len(public['nodes'])
        kept = {x for s in RARE for x in order[s][:carriers]}
        for ident, original in public['nodes'].items():
            now = nodes[ident]
            if ident in honest_outside and ident not in kept:
                reports_ok &= (now == {**original, 'skill': original['skill'] - 3, 'claim': answers[original['skill'] - 3]}
                               and list(now) == list(original))
            else:
                reports_ok &= now == original
        rare_truthful = sum(1 for x in nodes if nodes[x]['skill'] in RARE and nodes[x]['claim'] == answers[nodes[x]['skill']])
        rare_false = sum(1 for x in nodes if nodes[x]['skill'] in RARE and nodes[x]['claim'] != answers[nodes[x]['skill']])
        reports_ok &= rare_truthful == 3 * carriers and rare_false == c['community']
        # 4. Audit and admission recomputed on the manipulated world must equal the base trace.
        recomputed = sim.checkpoints({**world, 'public': {**public, 'nodes': nodes}}, d['audit_checks'], d['arms'], c)
        same = len(recomputed) == len(base) and all(
            all(x[k] == y[k] for k in ('arm', 'checks', 'admitted', 'passed', 'checked', 'events'))
            for x, y in zip(recomputed, base))
        out.setdefault('audit_admission_identical_across_c', True)
        out['audit_admission_identical_across_c'] &= bool(same)
    out['only_noncarrier_content_changes'] = bool(reports_ok)
    out['world_has_972_reports'] = bool(count_ok)

    # 5. Packets: constant size, identical order, badges and metadata across carrier counts.
    cells = {}
    for a in rows:
        cells.setdefault((a['arm'], a['checks']), []).append(a)
    packets_ok, labels_ok, leak_ok, grade_ok = True, True, True, True
    for (arm, checks), group in cells.items():
        rec = next(r for r in base if r['arm'] == arm and r['checks'] == checks)
        packets_ok &= len(group) == len(d['carriers'])
        packets_ok &= len({(a['admitted_hash'], a['audit_hash'], a['order_hash']) for a in group}) == 1
        packets_ok &= group[0]['admitted_hash'] == digest(rec['admitted']) and group[0]['audit_hash'] == digest(rec['events'])
        reference = group[0]['packet']['reports']
        for a in group:
            reports = a['packet']['reports']
            packets_ok &= len(reports) == c['admission_seats'] == len({r['node'] for r in reports})
            packets_ok &= {r['node'] for r in reports} == set(rec['admitted'])
            for r, ref in zip(reports, reference):
                packets_ok &= all(r[k] == ref[k] for k in ('node', 'age', 'activity', 'verification'))
                if not truth[r['node']]['honest'] or not truth[r['node']]['specialist']:
                    packets_ok &= r == ref
                packets_ok &= r['verification'] == ('trusted' if r['node'] in public['trusted'] else
                                                    'passed' if r['node'] in rec['passed'] else 'unchecked')
            # 6. Evaluator labels recounted from the packet and the hidden truth.
            g = a['diagnostics']
            truthful = [sum(1 for r in reports if r['skill'] == s and r['claim'] == answers[s]) for s in RARE]
            false = sum(1 for r in reports if r['claim'] != answers[r['skill']])
            attackers = sum(1 for r in reports if not truth[r['node']]['honest'])
            outside = sum(1 for r in reports if truth[r['node']]['specialist'])
            labels_ok &= (g['carriers_planned'] == 3 * a['carriers'] and g['carriers_admitted_per_fact'] == truthful
                          and g['carriers_admitted'] == sum(truthful)
                          and g['truth_available'] == sum(k > 0 for k in truthful) / 3
                          and g['attacker_admitted'] == attackers == false
                          and g['attacker_seat_share'] == g['false_seat_share'] == attackers / len(reports)
                          and g['original_outside_admitted'] == outside
                          and g['original_outside_retention'] == outside / c['community']
                          and [g['rare_truthful_reports'][str(s)] for s in RARE] == truthful
                          and sum(g['rare_false_reports'].values()) == attackers)
            labels_ok &= a['expected'] == {str(s): answers[s] if any(r['skill'] == s for r in reports) else None for s in range(6)}
            # 7. No truth, ownership or carrier role in the actor input.
            leak_ok &= _leak_free(a['packet'])
            # 8. Grading.
            grade_ok &= _grading_ok(a)
        # Invariant diagnostics across carrier counts.
        labels_ok &= len({(a['diagnostics']['original_outside_admitted'], a['diagnostics']['attacker_admitted']) for a in group}) == 1
    out['packets_constant_and_ordered'] = bool(packets_ok)
    out['evaluator_labels_correct'] = bool(labels_ok)
    out['actor_inputs_leak_free'] = bool(leak_ok)
    out['wrong_answer_graded_wrong'] = bool(grade_ok)
    out['thirty_assignments'] = len(rows) == 30
    return {k: bool(v) for k, v in out.items()}


def fixture_invariants(_=None):
    """Clean qualification packets and the probe packet."""
    d = design()
    q = d['qualification']
    out = {'clean_packets_truthful': True, 'clean_profiles_exact': True, 'clean_order_shared_within_root': True,
           'clean_actor_inputs_leak_free': True, 'clean_absent_fact_scoring': True}
    withheld_count = Counter()
    total = 0
    for task in d['qualification_worlds']:
        _, _, rows = qualification_assignments(task)
        total += len(rows)
        out['clean_order_shared_within_root'] &= len({a['order_hash'] for a in rows}) == 1
        for a in rows:
            answers, reports = a['answers'], a['packet']['reports']
            out['clean_packets_truthful'] &= (len(reports) == q['reports_per_packet']
                                              and all(r['claim'] == answers[r['skill']] for r in reports)
                                              and a['diagnostics']['attacker_admitted'] == 0)
            per_skill = Counter(r['skill'] for r in reports)
            for skill in RARE:
                want = 0 if skill == a['withheld'] else a['carriers']
                out['clean_profiles_exact'] &= per_skill.get(skill, 0) == want
            out['clean_profiles_exact'] &= all(per_skill.get(s, 0) > 0 for s in range(3))
            out['clean_actor_inputs_leak_free'] &= _leak_free(a['packet'])
            script = evaluate(a, scripted(a['packet']))
            out['clean_absent_fact_scoring'] &= script['exact_packet'] is True
            if a['withheld'] is not None:
                withheld_count[a['withheld']] += 1
                invented = dict(scripted(a['packet'])['values'])
                invented[str(a['withheld'])] = answers[a['withheld']]
                graded = evaluate(a, {'values': invented})
                out['clean_absent_fact_scoring'] &= (a['expected'][str(a['withheld'])] is None
                                                     and script['missing_fields'] == 1 == script['missing_correct']
                                                     and graded['exact_packet'] is False and graded['missing_correct'] == 0)
            else:
                out['clean_absent_fact_scoring'] &= script['missing_fields'] == 0
    out['clean_withheld_rotation_balanced'] = dict(withheld_count) == {3: 8, 4: 8, 5: 8} and total == q['packets']
    _, _, probe = probe_assignment()
    a = probe[0]
    out['probe_packet_ready'] = (a['task'] == d['probe']['world'] and a['task'] not in d['worlds']
                                 and a['task'] not in d['qualification_worlds']
                                 and evaluate(a, scripted(a['packet']))['exact_packet'] is True
                                 and all(v is not None for v in a['expected'].values()) and _leak_free(a['packet']))
    return {k: bool(v) for k, v in out.items()}


def _invariant_job(job):
    return fixture_invariants() if job == 'fixtures' else pilot_invariants(job)


def check_invariants():
    """Run every S0 invariant on the engineering roots and the clean fixtures."""
    d = design()
    jobs = [(task, rate) for task in d['engineering_worlds'] for rate in d['attacker_pass']] + ['fixtures']
    checks = {}
    for job, result in zip(jobs, _map(_invariant_job, jobs)):
        for name, ok in result.items():
            checks[name] = checks.get(name, True) and ok
    splits = [set(d[k]) for k in ('worlds', 'qualification_worlds', 'engineering_worlds')]
    checks['splits_disjoint_below_10000'] = (all(not a & b for i, a in enumerate(splits) for b in splits[i + 1:])
                                              and max(set.union(*splits)) < 10000)
    return {'checks': checks, 'passed': all(checks.values()), 'jobs': len(jobs)}


def mean(values):
    """Exactly rounded mean, so results do not depend on the Python version's sum()."""
    values = list(values)
    return math.fsum(values) / len(values) if values else None
