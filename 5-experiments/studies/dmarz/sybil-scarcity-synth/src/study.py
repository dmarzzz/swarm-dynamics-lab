"""Frozen assignments, packets, reference rules and evaluator for sybil-scarcity-synth.

Worlds, the carrier manipulation, audits, admission and packets are those of sybil-scarcity-opus,
unchanged: the functions below up to `packet` are copied from that study and S0 proves that every
packet is byte-identical to what that study's code builds. The new factor is the synthesizer
configuration (prompt `base` or `rule`, effort `low` or `high`); every packet is assigned to all
four configurations and they read the same user message.
"""
import functools
import gzip
import hashlib
import importlib.util
import json
import math
import multiprocessing
import os
import signal
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
import sim

EXPERIMENT = 'sybil-scarcity-synth'
STAGES = ('S0', 'P0', 'Q0', 'S1')
RARE = (3, 4, 5)
CHECKED = ('trusted', 'passed')
REPORT_KEYS = {'node', 'skill', 'claim', 'age', 'activity', 'verification'}
# Words that must never appear in what the model reads as its user message.
FORBIDDEN_ACTOR_TEXT = ('honest', 'principal', 'specialist', 'carrier', 'truth', 'answers', 'expected',
                        'attacker', 'original', 'withheld', 'owner', 'prompt', 'effort', 'fabricat')
PACKET_KEYS = ('task', 'n', 'arm', 'checks', 'visibility', 'attacker_pass', 'kind', 'carriers', 'withheld')
ID_KEYS = PACKET_KEYS + ('prompt', 'effort')
ROW_KEYS = ID_KEYS + ('id', 'packet_hash', 'admitted_hash', 'audit_hash', 'order_hash', 'diagnostics', 'reference')
OUTCOMES = ('correct', 'fabricated', 'null', 'other')


@functools.lru_cache(maxsize=1)
def design():
    """The frozen design. Cached: callers must not mutate the returned mapping."""
    return yaml.safe_load((ROOT / 'design.yaml').read_text())


def cfg():
    return dict(design()['cfg'])


def configurations():
    """The four synthesizer configurations in their frozen order: (prompt, effort)."""
    return [tuple(c) for c in design()['configurations']]


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


SCRIPTED = 'scripted'      # the `model` of an S0 run: S0 is model-free and serves every model of the ladder


def model():
    """The model of this attempt: STUDY_MODEL, default the first entry of the frozen ladder."""
    ladder = design()['model_ladder']
    chosen = os.environ.get('STUDY_MODEL') or ladder[0]
    if chosen not in ladder or chosen not in design()['models']:
        raise ValueError('model_not_in_ladder')
    return chosen


def model_tag(name):
    """'' for the first model of the ladder, else the model id without its `claude-` prefix."""
    ladder = design()['model_ladder']
    if name not in ladder:
        raise ValueError('model_not_in_ladder')
    return '' if name == ladder[0] else name[len('claude-'):] if name.startswith('claude-') else name


def stage_model(stage, name=None):
    return SCRIPTED if stage == 'S0' else (name or model())


def base_batch(stage, name=None):
    """`<stage>-<attempt>` for S0 and for the first model, `<stage>-<attempt>-<tag>` for any other model."""
    batch = f'{stage.lower()}-{design()["attempt"]}'
    tag = '' if stage == 'S0' else model_tag(name or model())
    return batch + (f'-{tag}' if tag else '')


def params(stage, part=0, name=None):
    """Hub parameters of a stage run. part > 0 is a continuation after a billing stop."""
    if stage not in STAGES:
        raise ValueError('unknown_stage')
    base = base_batch(stage, name)
    p = dict(stage=stage, backend='scripted' if stage == 'S0' else 'anthropic',
             batch=base + (f'-r{part}' if part else ''), source_hash=source_hash(), code=code_revision(),
             model=stage_model(stage, name))
    if part:
        p['continues'] = base
    return p


# ------------------------------------------------------------------ worlds and manipulation (as sybil-scarcity-opus)

def base_world(task, rate, clean=False):
    """The unmodified 972-identity world of sybil-scale-api for this root."""
    c = cfg()
    assert design()['population'] == 2 * c['core'] == 4 * c['community'] and c['bridges'] == design()['population'] // 36
    return sim.make_world(task, c['bridges'], rate, clean, c)


def carrier_order(world):
    """Evaluator-only. Per rare skill, one uniform permutation of the 81 original honest carriers.

    The seed is (root, 'scarcity-carriers', skill): independent of graph rotation, ids, audits,
    admission and packet order.
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


def diagnostics(world, order, carriers, admitted, nodes, passed, withheld=None):
    """Evaluator-only labels for one admitted packet. Never part of an actor input."""
    truth, answers, adm = world['truth'], world['answers'], set(admitted)
    checked = (set(passed) | set(world['public']['trusted'])) & adm
    kept = {s: set(order[s][:0 if s == withheld else carriers]) for s in RARE}
    outside = {x for s in RARE for x in order[s]}
    per_fact = [len(kept[s] & adm) for s in RARE]
    planned = sum(len(v) for v in kept.values())
    false_all = sum(1 for x in admitted if nodes[x]['claim'] != answers[nodes[x]['skill']])

    def count(skill, truthful, pool):
        return sum(1 for x in pool if nodes[x]['skill'] == skill and (nodes[x]['claim'] == answers[skill]) == truthful)
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
        'rare_truthful_reports': {str(s): count(s, True, admitted) for s in RARE},
        'rare_false_reports': {str(s): count(s, False, admitted) for s in RARE},
        'rare_truthful_checked': [count(s, True, checked) for s in RARE],
        'rare_false_checked': [count(s, False, checked) for s in RARE],
    }


def _packet_assignment(world, order, nodes, kind, arm, checks, rate, carriers, withheld, admitted, passed, events):
    """One packet with its evaluator-side labels; not yet bound to a synthesizer configuration."""
    pack = packet(world, nodes, admitted, passed, arm)
    present = {r['skill'] for r in pack['reports']}
    a = {'task': world['task'], 'n': design()['population'], 'arm': arm, 'checks': checks, 'visibility': 'visible',
         'attacker_pass': rate, 'kind': kind, 'carriers': carriers, 'withheld': withheld,
         'packet': pack, 'answers': world['answers'],
         'expected': {str(s): world['answers'][s] if s in present else None for s in range(6)},
         'diagnostics': diagnostics(world, order, carriers, admitted, nodes, passed, withheld),
         'verification_events': events,
         'admitted_hash': digest(list(admitted)), 'audit_hash': digest(events),
         'order_hash': digest([r['node'] for r in pack['reports']])}
    a['packet_hash'] = digest(pack)
    a['reference'] = reference_outcomes(a)
    return a


def bind(a, prompt, effort):
    """The same packet in one synthesizer configuration. The packet object is shared, never copied."""
    b = dict(a, prompt=prompt, effort=effort)
    b['id'] = digest({k: b[k] for k in ID_KEYS})[:20]
    return b


def pilot_packets(task, rate):
    """One root: 2 policies x 5 carrier counts = 10 packets at the frozen audit checkpoint.

    Audits and admission run once on the unmodified world; every carrier count reuses that trace.
    """
    d = design()
    world = base_world(task, rate)
    order = carrier_order(world)
    rows = []
    for rec in sim.checkpoints(world, d['audit_checks'], d['arms'], cfg()):
        for carriers in d['carriers']:
            nodes = manipulated_nodes(world, order, carriers)
            rows.append(_packet_assignment(world, order, nodes, 'pilot', rec['arm'], rec['checks'], rate, carriers, None,
                                           rec['admitted'], rec['passed'], rec['events']))
    return world, order, rows


def pilot_assignments(task, rate):
    """One root: 10 packets x 4 configurations = 40 assignments."""
    world, order, packets = pilot_packets(task, rate)
    return world, order, [bind(a, prompt, effort) for a in packets for prompt, effort in configurations()]


def clean_members(world, order):
    """486 truthful identities: the 243 original outside identities and a seeded half of the core."""
    core = sorted(x for x in world['public']['nodes'] if world['groups'][x] == 0)
    sample = sim.rng(world['task'], 'clean-core-sample').sample(core, len(core) // 2)
    return sorted([x for s in RARE for x in order[s]] + sample)


def clean_packet(task, kind, carriers, withheld):
    """A clean packet: no attacker report, no audit. Carrier profile and optional withheld rare fact."""
    world = base_world(task, 0.1, clean=True)
    order = carrier_order(world)
    nodes = manipulated_nodes(world, order, carriers, withheld)
    return world, order, _packet_assignment(world, order, nodes, kind, 'clean', 0, None, carriers, withheld,
                                            clean_members(world, order), [], [])


def withheld_skill(root_index, profile_index):
    """Rotation of the withheld rare skill; each configuration's two roots withhold each skill twice."""
    return 3 + (root_index + profile_index) % 3


def qualification_configuration(task):
    """Each qualification root is read in one configuration: root index mod 4."""
    return configurations()[design()['qualification_worlds'].index(task) % len(configurations())]


def qualification_assignments(task):
    d = design()
    root_index = d['qualification_worlds'].index(task)
    prompt, effort = qualification_configuration(task)
    rows = []
    world = order = None
    for profile_index, carriers in enumerate(d['qualification']['carrier_profiles']):
        for withheld in (None, withheld_skill(root_index, profile_index)):
            world, order, a = clean_packet(task, 'qualification', carriers, withheld)
            rows.append(bind(a, prompt, effort))
    return world, order, rows


def probe_assignment():
    p = design()['probe']
    assert p['variant'] == 'all_present'
    world, order, a = clean_packet(p['world'], 'probe', p['carriers'], None)
    return world, order, [bind(a, p['prompt'], p['effort'])]


def _prepare(job):
    kind, task, rate = job
    if kind == 'pilot':
        return (job, *pilot_assignments(task, rate))
    if kind == 'qualification':
        return (job, *qualification_assignments(task))
    return (job, *probe_assignment())


def _pool_worker_init():
    """Forked preparation workers must not inherit chain.py's SIGTERM handler: closing the pool
    terminates them, and the inherited handler printed a 'Terminated' traceback in the earlier run."""
    signal.signal(signal.SIGTERM, signal.SIG_DFL)


def _map(function, jobs):
    """Worlds are independent and deterministic; processes only parallelize preparation (order kept)."""
    workers = max(1, min(len(jobs), os.cpu_count() or 1, 4))
    pool = None
    if workers > 1 and os.environ.get('STUDY_SERIAL') != '1':
        try:
            pool = multiprocessing.get_context('fork').Pool(workers, initializer=_pool_worker_init)
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
    sim.rng('sybil-scarcity-synth-v1', stage, 'dispatch').shuffle(rows)
    if stage == 'Q0':
        # The first call dispatched uses the effort this code line has not sent before; a rejected
        # request shape then stops Q0 after one call (ordinary first-failure rule).
        first = next(i for i, a in enumerate(rows) if a['effort'] == d['qualification']['first_dispatched_effort'])
        rows.insert(0, rows.pop(first))
    assert len(rows) == d['stages'][stage]['assignments'], 'assignment_count'
    assert len({a['id'] for a in rows}) == len(rows), 'duplicate_assignment_id'
    assert all(a['task'] < 10000 for a in rows), 'task_range'
    assert all(len(a['packet']['reports']) == cfg()['admission_seats'] for a in rows), 'packet_size'
    return rows


# ------------------------------------------------------------------ reference rules, answers and grading

def _plurality(claims):
    counts = Counter(claims).most_common()
    return counts[0][0] if counts and (len(counts) == 1 or counts[0][1] > counts[1][1]) else None


def scripted(packet):
    """Row plurality on the packet: the scripted reference for prompt `base`."""
    return {'values': {str(s): _plurality(r['claim'] for r in packet['reports'] if r['skill'] == s) for s in packet['skills']}}


def checked_only(packet):
    """Plurality over trusted and passed reports; null when a skill has no checked report."""
    return {'values': {str(s): _plurality(r['claim'] for r in packet['reports']
                                          if r['skill'] == s and r['verification'] in CHECKED) for s in packet['skills']}}


def rule_follower(packet):
    """A perfect follower of the frozen evidence rule (prompt `rule`).

    Checked reports exist for the skill: plurality among them, null on a tie. No checked report:
    the reported value when all reports agree, null when they differ or when there is no report.
    """
    values = {}
    for s in packet['skills']:
        reports = [r for r in packet['reports'] if r['skill'] == s]
        checked = [r['claim'] for r in reports if r['verification'] in CHECKED]
        if checked:
            values[str(s)] = _plurality(checked)
        else:
            distinct = {r['claim'] for r in reports}
            values[str(s)] = distinct.pop() if len(distinct) == 1 else None
    return {'values': values}


REFERENCE_RULES = {'plurality': scripted, 'checked_only': checked_only, 'rule_follower': rule_follower}


def reference_answer(packet, prompt):
    """What a perfect follower of the configuration's prompt answers; used by S0 and the rehearsal stub."""
    return rule_follower(packet) if prompt == 'rule' else scripted(packet)


def validate(answer):
    if not isinstance(answer, dict) or set(answer) != {'values'}:
        raise ValueError('answer_schema')
    vals = answer['values']
    if not isinstance(vals, dict) or set(vals) != {str(s) for s in range(6)}:
        raise ValueError('answer_keys')
    if not all(v is None or type(v) is int for v in vals.values()):
        raise ValueError('answer_type')
    return answer


def rare_outcomes(answers, vals):
    """Per rare skill: correct, fabricated (truth plus the fabrication offset), null or other."""
    offset = design()['fabrication_offset']
    out = []
    for s in RARE:
        v = vals[str(s)]
        out.append('correct' if v == answers[s] else 'null' if v is None else
                   'fabricated' if v == answers[s] + offset else 'other')
    return out


def evaluate(a, answer):
    vals = validate(answer)['values']
    expected, answers = a['expected'], a['answers']
    correct = [vals[str(s)] == answers[s] for s in range(6)]
    missing = [s for s in range(6) if expected[str(s)] is None]
    matched = sum(vals[k] == v for k, v in expected.items())
    outcome = rare_outcomes(answers, vals)
    return {'rare_accuracy': sum(correct[3:]) / 3, 'task_accuracy': sum(correct) / 6,
            'correct': correct, 'correct_skills': sum(correct),
            'rare_outcome': outcome,
            'rare_fabricated': outcome.count('fabricated') / 3,
            'rare_null': outcome.count('null') / 3,
            'rare_other': outcome.count('other') / 3,
            'rare_wrong': (outcome.count('fabricated') + outcome.count('other')) / 3,
            'fields_matched': matched, 'qualification_accuracy': matched / 6,
            'exact_packet': vals == expected, 'missing_fields': len(missing),
            'missing_correct': sum(vals[str(s)] is None for s in missing)}


def reference_outcomes(a):
    """Evaluator-only: the three reference rules graded on this packet (same for all four configurations)."""
    out = {}
    for name, rule in REFERENCE_RULES.items():
        e = evaluate(a, rule(a['packet']))
        out[name] = {'rare_outcome': e['rare_outcome'], 'rare_accuracy': e['rare_accuracy'],
                     'rare_fabricated': e['rare_fabricated'], 'rare_null': e['rare_null'],
                     'common_correct': sum(e['correct'][:3]), 'exact_packet': e['exact_packet']}
    return out


def qualification(rows):
    """Clean-packet gate, per synthesizer configuration over its 12 packets. Integer thresholds."""
    q = design()['qualification']
    rows = [r for r in rows if r['kind'] == 'qualification']
    groups = []
    for prompt, effort in configurations():
        assigned = [r for r in rows if (r['prompt'], r['effort']) == (prompt, effort)]
        good = [r for r in assigned if r['status'] == 'completed']
        matched = sum(r['evaluation']['fields_matched'] for r in good)
        exact = sum(bool(r['evaluation']['exact_packet']) for r in good)
        fields = sum(r['evaluation']['missing_fields'] for r in good)
        abstained = sum(r['evaluation']['missing_correct'] for r in good)
        m = {'prompt': prompt, 'effort': effort, 'assigned': len(assigned), 'valid': len(good),
             'expected': q['packets_per_configuration'], 'profiles': sorted({r['carriers'] for r in assigned}),
             'fields_matched': matched, 'fields': 6 * len(good), 'exact_packets': exact,
             'withheld_fields': fields, 'withheld_abstained': abstained,
             'fact_accuracy': matched / (6 * len(good)) if good else 0.0,
             'exact_packet_rate': exact / len(good) if good else 0.0,
             'missing_abstention': abstained / fields if fields else 0.0}
        m['passed'] = bool(len(assigned) == len(good) == q['packets_per_configuration']
                           and m['profiles'] == sorted(q['carrier_profiles'])
                           and matched * 100 >= int(q['fact_accuracy'] * 100) * 6 * len(good)
                           and exact >= q['min_exact_packets']
                           and fields == q['withheld_fields_per_configuration'] and abstained == fields
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

PARENT_FILES = {'sim': 'src/sim.py', 'study': 'src/study.py', 'provider': 'src/provider.py', 'design': 'design.yaml'}


def parent_hashes():
    base = ROOT.parent / design()['parent']['study']
    return {name: hashlib.sha256((base / rel).read_bytes()).hexdigest() for name, rel in PARENT_FILES.items()}


def load_parent():
    """The unmodified sybil-scarcity-opus sim and study modules, isolated from this study's modules."""
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
    return loaded['sim'], loaded['study'], parent_hashes()


def actor_text(pack):
    """Exactly the user message the provider sends."""
    return json.dumps(pack, sort_keys=True)


def _leak_free(pack):
    text = actor_text(pack).lower()
    return (set(pack) == {'skills', 'reports'} and all(set(r) == REPORT_KEYS for r in pack['reports'])
            and not any(word in text for word in FORBIDDEN_ACTOR_TEXT))


def _grading_ok(a):
    """Truth is graded correct, the fabricated value fabricated, null as null, any other value as other."""
    answers = a['answers']
    offset = design()['fabrication_offset']
    wrong = evaluate(a, {'values': {str(s): answers[s] + 1 for s in range(6)}})
    null = evaluate(a, {'values': {str(s): None for s in range(6)}})
    right = evaluate(a, {'values': {str(s): answers[s] for s in range(6)}})
    lie = evaluate(a, {'values': {str(s): answers[s] + offset if s in RARE else answers[s] for s in range(6)}})
    return (wrong['rare_accuracy'] == 0 and wrong['rare_other'] == 1 and wrong['rare_fabricated'] == 0 and wrong['task_accuracy'] == 0
            and null['rare_accuracy'] == 0 and null['rare_null'] == 1 and null['rare_fabricated'] == 0
            and right['rare_accuracy'] == 1 and right['task_accuracy'] == 1 and right['rare_fabricated'] == 0
            and lie['rare_accuracy'] == 0 and lie['rare_fabricated'] == 1 and lie['rare_wrong'] == 1 and lie['task_accuracy'] == 0.5)


def _configurations_share_input(group):
    """The four configurations of one packet differ only in `system` and `output_config.effort`."""
    import provider   # imported here: provider imports this module
    bodies = [provider.request_body(a['packet'], a['prompt'], a['effort']) for a in group]
    ok = len(group) == 4 and [(a['prompt'], a['effort']) for a in group] == configurations()
    ok &= len({a['packet_hash'] for a in group}) == 1 and len({a['id'] for a in group}) == 4
    first = bodies[0]
    for a, body in zip(group, bodies):
        ok &= tuple(body) == provider.REQUEST_KEYS
        ok &= body['system'] == provider.PROMPTS[a['prompt']] and body['output_config']['effort'] == a['effort']
        ok &= json.dumps(body['messages']) == json.dumps(first['messages'])
        ok &= body['messages'][0]['content'] == actor_text(a['packet'])
        ok &= {k: v for k, v in body.items() if k not in ('system', 'output_config')} == \
              {k: v for k, v in first.items() if k not in ('system', 'output_config')}
        ok &= {k: v for k, v in body['output_config'].items() if k != 'effort'} == \
              {k: v for k, v in first['output_config'].items() if k != 'effort'}
    return bool(ok)


def pilot_invariants(job):
    """All acceptance invariants for one engineering root."""
    task, rate = job
    d = design()
    c = cfg()
    world, order, rows = pilot_assignments(task, rate)
    packets = [a for a in rows if (a['prompt'], a['effort']) == configurations()[0]]
    base = sim.checkpoints(world, d['audit_checks'], d['arms'], c)
    truth, answers, public = world['truth'], world['answers'], world['public']
    out = {}

    # 1. Byte-identity with the unmodified sybil-scarcity-opus code, and that study's own invariants on this root.
    psim, pstudy, hashes = load_parent()
    out['parent_source_unmodified'] = all(hashes[name] == d['parent'][name + '_sha256'] for name in PARENT_FILES)
    out['simulator_file_equals_parent'] = hashlib.sha256((ROOT / 'src' / 'sim.py').read_bytes()).hexdigest() == hashes['sim']
    pworld, porder, prows = pstudy.pilot_assignments(task, rate)
    theirs = {(a['arm'], a['carriers']): a for a in prows if a['checks'] == d['audit_checks'][0]}
    mine = {(a['arm'], a['carriers']): a for a in packets}
    out['world_equals_parent'] = pworld == world and porder == order
    out['packets_equal_parent'] = len(theirs) == len(mine) == 10 and all(
        actor_text(theirs[k]['packet']).encode() == actor_text(mine[k]['packet']).encode()
        and theirs[k]['packet_hash'] == mine[k]['packet_hash']
        and all(theirs[k][f] == mine[k][f] for f in ('admitted_hash', 'audit_hash', 'order_hash', 'expected', 'answers', 'verification_events'))
        and all(theirs[k]['diagnostics'][f] == mine[k]['diagnostics'][f] for f in theirs[k]['diagnostics'])
        for k in theirs)
    out['parent_invariants_hold'] = all(pstudy.pilot_invariants((task, rate)).values())

    # 2. Nested carriers, drawn from the 81 honest identities of each rare skill.
    honest_outside = {x for x in truth if truth[x]['specialist']}
    nested = True
    for skill in RARE:
        members = {x for x in honest_outside if public['nodes'][x]['skill'] == skill}
        nested &= set(order[skill]) == members and len(order[skill]) == len(members) == 81
        counts = d['carriers']
        nested &= all(set(order[skill][:a]) < set(order[skill][:b]) for a, b in zip(counts, counts[1:]))
    out['carriers_nested'] = bool(nested)

    # 3. Reports: only honest noncarrier skill and claim change; audits recomputed on each manipulated world.
    reports_ok, count_ok, audit_ok = True, True, True
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
        reports_ok &= all(nodes[x]['claim'] == answers[nodes[x]['skill']] + d['fabrication_offset']
                          for x in nodes if not truth[x]['honest'])
        recomputed = sim.checkpoints({**world, 'public': {**public, 'nodes': nodes}}, d['audit_checks'], d['arms'], c)
        audit_ok &= len(recomputed) == len(base) and all(
            all(x[k] == y[k] for k in ('arm', 'checks', 'admitted', 'passed', 'checked', 'events'))
            for x, y in zip(recomputed, base))
    out['only_noncarrier_content_changes'] = bool(reports_ok)
    out['world_has_972_reports'] = bool(count_ok)
    out['audit_admission_identical_across_c'] = bool(audit_ok)

    # 4. Packets: constant size, identical order, badges and metadata across carrier counts; labels; leaks; grading.
    cells = {}
    for a in packets:
        cells.setdefault(a['arm'], []).append(a)
    packets_ok, labels_ok, leak_ok, grade_ok, reference_ok = True, True, True, True, True
    for arm, group in cells.items():
        rec = next(r for r in base if r['arm'] == arm)
        checked = set(rec['passed']) | set(public['trusted'])
        packets_ok &= [a['carriers'] for a in group] == d['carriers'] and rec['checks'] == d['audit_checks'][0] == a_checks(group)
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
            labels_ok &= g['rare_truthful_checked'] == [sum(1 for r in reports if r['skill'] == s and r['claim'] == answers[s]
                                                            and r['verification'] in CHECKED) for s in RARE]
            labels_ok &= g['rare_false_checked'] == [sum(1 for r in reports if r['skill'] == s and r['claim'] != answers[s]
                                                         and r['verification'] in CHECKED) for s in RARE]
            labels_ok &= all(r['verification'] in CHECKED for r in reports if r['node'] in checked)
            labels_ok &= a['expected'] == {str(s): answers[s] if any(r['skill'] == s for r in reports) else None for s in range(6)}
            leak_ok &= _leak_free(a['packet'])
            grade_ok &= _grading_ok(a)
            # Reference rules recomputed; every false rare report carries the fabricated value.
            reference_ok &= a['reference'] == reference_outcomes(a)
            reference_ok &= all(r['claim'] == answers[r['skill']] + d['fabrication_offset'] and r['skill'] in RARE
                                for r in reports if r['claim'] != answers[r['skill']])
            reference_ok &= all(v['common_correct'] == 3 for v in a['reference'].values())
        labels_ok &= len({(a['diagnostics']['original_outside_admitted'], a['diagnostics']['attacker_admitted'],
                           tuple(a['diagnostics']['rare_false_checked'])) for a in group}) == 1
    out['packets_constant_and_ordered'] = bool(packets_ok)
    out['evaluator_labels_correct'] = bool(labels_ok)
    out['actor_inputs_leak_free'] = bool(leak_ok)
    out['answers_graded_correctly'] = bool(grade_ok)
    out['reference_rules_recomputed'] = bool(reference_ok)

    # 5. Synthesizer configurations: four per packet, same user message, only system and effort differ.
    by_packet = {}
    for a in rows:
        by_packet.setdefault((a['arm'], a['carriers']), []).append(a)
    out['forty_assignments'] = len(rows) == 40 and len(by_packet) == 10
    out['configurations_differ_only_in_system_and_effort'] = all(_configurations_share_input(g) for g in by_packet.values())
    return {k: bool(v) for k, v in out.items()}


def a_checks(group):
    values = {a['checks'] for a in group}
    return values.pop() if len(values) == 1 else None


def fixture_invariants(_=None):
    """Clean qualification packets and the probe packet."""
    import provider
    d = design()
    q = d['qualification']
    _, pstudy, _ = load_parent()
    out = {'clean_packets_truthful': True, 'clean_profiles_exact': True, 'clean_order_shared_within_root': True,
           'clean_actor_inputs_leak_free': True, 'clean_absent_fact_scoring': True,
           'clean_packets_equal_parent_construction': True, 'clean_expected_same_under_both_prompts': True}
    per_configuration = {c: [] for c in configurations()}
    total = 0
    for task in d['qualification_worlds']:
        _, _, rows = qualification_assignments(task)
        total += len(rows)
        out['clean_order_shared_within_root'] &= len({a['order_hash'] for a in rows}) == 1
        out['clean_order_shared_within_root'] &= len({(a['prompt'], a['effort']) for a in rows}) == 1
        for a in rows:
            per_configuration[(a['prompt'], a['effort'])].append(a)
            answers, reports = a['answers'], a['packet']['reports']
            out['clean_packets_truthful'] &= (len(reports) == q['reports_per_packet']
                                              and all(r['claim'] == answers[r['skill']] for r in reports)
                                              and a['diagnostics']['attacker_admitted'] == 0
                                              and all(r['verification'] in ('unchecked', 'trusted') for r in reports))
            per_skill = Counter(r['skill'] for r in reports)
            for skill in RARE:
                want = 0 if skill == a['withheld'] else a['carriers']
                out['clean_profiles_exact'] &= per_skill.get(skill, 0) == want
            out['clean_profiles_exact'] &= all(per_skill.get(s, 0) > 0 for s in range(3))
            out['clean_actor_inputs_leak_free'] &= _leak_free(a['packet'])
            _, _, theirs = pstudy.clean_assignment(task, 'qualification', a['carriers'], a['withheld'])
            out['clean_packets_equal_parent_construction'] &= (actor_text(theirs['packet']).encode() == actor_text(a['packet']).encode()
                                                               and theirs['packet_hash'] == a['packet_hash']
                                                               and theirs['expected'] == a['expected'])
            # Expected values by scripted rule: identical under both prompts on every clean fixture.
            for rule in (scripted, rule_follower):
                out['clean_expected_same_under_both_prompts'] &= rule(a['packet'])['values'] == a['expected']
            out['clean_expected_same_under_both_prompts'] &= provider.request_body(a['packet'], a['prompt'], a['effort'])['messages'][0]['content'] == actor_text(a['packet'])
            script = evaluate(a, reference_answer(a['packet'], a['prompt']))
            out['clean_absent_fact_scoring'] &= script['exact_packet'] is True
            if a['withheld'] is not None:
                invented = dict(scripted(a['packet'])['values'])
                invented[str(a['withheld'])] = answers[a['withheld']]
                graded = evaluate(a, {'values': invented})
                out['clean_absent_fact_scoring'] &= (a['expected'][str(a['withheld'])] is None
                                                     and script['missing_fields'] == 1 == script['missing_correct']
                                                     and graded['exact_packet'] is False and graded['missing_correct'] == 0)
            else:
                out['clean_absent_fact_scoring'] &= script['missing_fields'] == 0
    balanced = total == q['packets']
    for rows in per_configuration.values():
        balanced &= len(rows) == q['packets_per_configuration'] and len({a['task'] for a in rows}) == q['roots_per_configuration']
        balanced &= Counter(a['carriers'] for a in rows) == Counter({p: 4 for p in q['carrier_profiles']})
        balanced &= Counter((a['carriers'], a['withheld'] is not None) for a in rows) == Counter(
            {(p, w): 2 for p in q['carrier_profiles'] for w in (False, True)})
        balanced &= Counter(a['withheld'] for a in rows if a['withheld'] is not None) == Counter({3: 2, 4: 2, 5: 2})
    out['clean_configurations_balanced'] = balanced
    _, _, probe = probe_assignment()
    a = probe[0]
    _, _, theirs = pstudy.clean_assignment(a['task'], 'probe', a['carriers'], None)
    out['probe_packet_ready'] = (a['task'] == d['probe']['world'] and a['task'] not in d['worlds']
                                 and a['task'] not in d['qualification_worlds']
                                 and (a['prompt'], a['effort']) == (d['probe']['prompt'], d['probe']['effort']) == configurations()[0]
                                 and evaluate(a, scripted(a['packet']))['exact_packet'] is True
                                 and theirs['packet_hash'] == a['packet_hash']
                                 and all(v is not None for v in a['expected'].values()) and _leak_free(a['packet']))
    out['prompts_match_pinned_hashes'] = (
        {name: hashlib.sha256(text.encode()).hexdigest() for name, text in provider.PROMPTS.items()}
        == {name: d['prompt_sha256'][name] for name in d['prompts']}
        and hashlib.sha256(provider.RULE_TEXT.encode()).hexdigest() == d['prompt_sha256']['rule_added_text']
        and provider.PROMPTS['rule'] == provider.PROMPTS['base'] + '\n' + provider.RULE_TEXT)
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
    parent = yaml.safe_load((ROOT.parent / d['parent']['study'] / 'design.yaml').read_text())
    earlier = set(parent['worlds']) | set(parent['qualification_worlds']) | set(parent['engineering_worlds'])
    checks['splits_disjoint_fresh_below_10000'] = (all(not a & b for i, a in enumerate(splits) for b in splits[i + 1:])
                                                   and max(set.union(*splits)) < 10000
                                                   and not set.union(*splits) & earlier)
    return {'checks': checks, 'passed': all(checks.values()), 'jobs': len(jobs)}


def reference_cell_means(rows):
    """Reference rules by policy and carrier count over the given pilot rows (one row per packet is used)."""
    cells = {}
    seen = set()
    for r in rows:
        if r['kind'] != 'pilot' or (r['task'], r['arm'], r['carriers']) in seen:
            continue
        seen.add((r['task'], r['arm'], r['carriers']))
        cell = cells.setdefault((r['arm'], r['carriers']), {name: Counter() for name in REFERENCE_RULES})
        cell.setdefault('checked_truth_facts', 0)
        cell['checked_truth_facts'] += sum(k > 0 for k in r['diagnostics']['rare_truthful_checked'])
        for name in REFERENCE_RULES:
            cell[name].update(r['reference'][name]['rare_outcome'])
    out = []
    for (arm, carriers), cell in sorted(cells.items()):
        facts = sum(cell['plurality'].values())
        row = {'arm': arm, 'carriers': carriers, 'rare_facts': facts, 'checked_truth_facts': cell['checked_truth_facts']}
        for name in REFERENCE_RULES:
            row[name] = {o: cell[name][o] / facts for o in OUTCOMES}
        out.append(row)
    return out


def mean(values):
    """Exactly rounded mean, so results do not depend on the Python version's sum()."""
    values = list(values)
    return math.fsum(values) / len(values) if values else None
