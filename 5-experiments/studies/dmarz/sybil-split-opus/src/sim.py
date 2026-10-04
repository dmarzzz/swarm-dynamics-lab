"""Identity splitting at fixed attacker resources: worlds, admission policies, evaluator.

Two honest-world generators (the ring construction of sybil-scale-api and a separately
implemented community graph), one attacker overlay that partitions 27 fixed resource units
into k identities, the public-observation check policies and ranking of the parent
instrument, and the evaluator. Nothing in this module calls a model.
"""
from __future__ import annotations
import hashlib
import json
import random
from collections import Counter
from functools import lru_cache

ARMS = ('no_verification', 'degree', 'random', 'coverage')
FAMILIES = ('ring', 'community')
RARE = (3, 4, 5)
SKILLS = 6


def rng(*parts):
    return random.Random(int(hashlib.sha256(json.dumps(parts, sort_keys=True).encode()).hexdigest(), 16))


# --------------------------------------------------------------------------- ring family
def parent_make_world(task, bridges, attacker_pass, clean, cfg):
    """The sybil-scale-api generator, unchanged (selftest compares it with the parent file
    and with frozen digests). This study only uses it with clean=True: every identity honest."""
    ncore, size = cfg['core'], cfg['community']
    assert ncore == 2 * size and size >= 9 and size % 9 == 0
    half = ncore // 2
    n = ncore + 2 * size
    graph = {i: set() for i in range(n)}
    def add(a, b): graph[a].add(b); graph[b].add(a)
    def remove(a, b): graph[a].remove(b); graph[b].remove(a)
    for group in range(2):
        for i in range(half):
            for j in (1, 2, 3): add(group * half + i, group * half + (i + j) % half)
    for i in range(half): add(i, i + half)
    for offset in (ncore, ncore + size):
        for i in range(size):
            for j in (1, 2): add(offset + i, offset + (i + j) % size)
    shift = rng(task, 'rotation').randrange(half)
    for k in range(bridges):
        a = (shift + 2 * k) % half; b = (a + 1) % half
        for group in range(2):
            c, d = a + group * half, b + group * half
            u, v = ncore + group * size + a, ncore + group * size + b
            remove(c, d); remove(u, v); add(c, u); add(d, v)
    labels = list(range(n)); rng(task, 'ids').shuffle(labels)
    ids = {i: f'n{labels[i]:02d}' for i in range(n)}
    honest_group = rng(task, 'ownership').randrange(2)
    values = [rng(task, 'truth', s).randint(10, 89) for s in range(6)]
    nodes = {}; truth = {}; checks = {}; groups = {}
    for i in range(n):
        group = 0 if i < ncore else 1 + (i - ncore) // size
        honest = i < ncore or clean or group - 1 == honest_group
        skill = i % 3 if group == 0 else 3 + (i - ncore) % 3
        ident = ids[i]
        nodes[ident] = {'skill': skill, 'claim': values[skill] if honest else values[skill] + 7,
                        'age': 10 + (i % ncore if group == 0 else (i - ncore) % size),
                        'activity': 5 + (i % 3)}
        truth[ident] = {'honest': honest, 'specialist': group > 0 and honest,
                        'principal': ident if honest else 'synthetic-attacker'}
        p = cfg['honest_check_pass'] if honest else attacker_pass
        checks[ident] = rng(task, 'verification', ident).random() < p
        groups[ident] = group
    public = {'nodes': dict(sorted(nodes.items())),
              'adj': {ids[i]: sorted(ids[j] for j in graph[i]) for i in range(n)},
              'trusted': sorted([ids[0], ids[half]])}
    return {'public': public, 'truth': truth, 'checks': checks, 'answers': values, 'groups': groups, 'task': task}


# ---------------------------------------------------------------------- community family
def connected(adj):
    start = next(iter(adj)); seen = {start}; todo = [start]
    while todo:
        for v in adj[todo.pop()]:
            if v not in seen: seen.add(v); todo.append(v)
    return len(seen) == len(adj)


def random_regular(n, half_degree, r):
    """A connected simple graph on 0..n-1 in which every vertex has degree 2*half_degree.
    Starts from the circulant lattice and applies 20 switch attempts per edge; a switch
    replaces edges a-b and c-d by a-d and c-b and is skipped when it would create a loop
    or a repeated edge, so every degree is preserved. Redrawn until connected."""
    while True:
        adj = {i: set() for i in range(n)}
        for i in range(n):
            for j in range(1, half_degree + 1):
                adj[i].add((i + j) % n); adj[(i + j) % n].add(i)
        edges = sorted((a, b) for a in adj for b in adj[a] if a < b)
        for _ in range(20 * len(edges)):
            i, j = r.randrange(len(edges)), r.randrange(len(edges))
            (a, b), (c, d) = edges[i], edges[j]
            if r.random() < 0.5: c, d = d, c
            if len({a, b, c, d}) < 4 or d in adj[a] or b in adj[c]: continue
            adj[a].remove(b); adj[b].remove(a); adj[c].remove(d); adj[d].remove(c)
            adj[a].add(d); adj[d].add(a); adj[c].add(b); adj[b].add(c)
            edges[i] = (min(a, d), max(a, d)); edges[j] = (min(c, b), max(c, b))
        if connected(adj): return adj


def community_make_world(task, cfg):
    """Degree-matched planted partition, written for this study (no code shared with the ring
    generator beyond rng). Four blocks: two core blocks of 27 (random 6-regular inside, one
    matching edge to the twin vertex of the other core block) and two outside blocks of 27
    (random 4-regular). Each outside block is tied to one core block by size/9 swaps that
    replace one core edge and one outside edge by two core-outside edges, so every degree
    equals the ring family's (7 core, 4 outside) and each outside block has 2*size/9 bridge
    edges. Both core blocks use one drawn graph and both outside blocks another, with swaps at
    the same positions, so exchanging the two halves is a graph automorphism and the two
    outside groups have identical observable profiles."""
    ncore, size = cfg['core'], cfg['community']
    assert ncore == 2 * size and size % 9 == 0
    half = ncore // 2; n = ncore + 2 * size
    r = rng('community', task, 'graph')
    core_block = random_regular(half, 3, r)
    out_block = random_regular(size, 2, r)
    core_edges = sorted((a, b) for a in core_block for b in core_block[a] if a < b)
    out_edges = sorted((a, b) for a in out_block for b in out_block[a] if a < b)
    r.shuffle(core_edges); r.shuffle(out_edges)
    swaps = []; used_core = set(); used_out = set()
    for (c, d), (u, v) in zip(core_edges, out_edges):
        if len(swaps) == size // 9: break
        if {c, d} & used_core or {u, v} & used_out: continue
        used_core |= {c, d}; used_out |= {u, v}; swaps.append((c, d, u, v))
    assert len(swaps) == size // 9
    graph = {i: set() for i in range(n)}
    def add(a, b): graph[a].add(b); graph[b].add(a)
    def remove(a, b): graph[a].remove(b); graph[b].remove(a)
    for g in range(2):
        core0, out0 = g * half, ncore + g * size
        for a, b in core_edges: add(core0 + a, core0 + b)
        for a, b in out_edges: add(out0 + a, out0 + b)
        for c, d, u, v in swaps:
            remove(core0 + c, core0 + d); remove(out0 + u, out0 + v)
            add(core0 + c, out0 + u); add(core0 + d, out0 + v)
    for i in range(half): add(i, i + half)
    values = [rng('community', task, 'truth', s).randint(10, 89) for s in range(6)]
    nodes = {}; truth = {}; checks = {}; groups = {}
    for i in range(n):
        group = 0 if i < ncore else 1 + (i - ncore) // size
        ident = f'c{i:03d}'
        skill = i % 3 if group == 0 else 3 + (i - ncore) % 3
        nodes[ident] = {'skill': skill, 'claim': values[skill],
                        'age': 10 + (i % ncore if group == 0 else (i - ncore) % size),
                        'activity': 5 + (i % 3)}
        truth[ident] = {'honest': True, 'specialist': group > 0, 'principal': ident}
        checks[ident] = rng('community', task, 'verification', ident).random() < cfg['honest_check_pass']
        groups[ident] = group
    public = {'nodes': nodes, 'adj': {f'c{i:03d}': sorted(f'c{j:03d}' for j in graph[i]) for i in range(n)},
              'trusted': sorted(['c000', f'c{half:03d}'])}
    return {'public': public, 'truth': truth, 'checks': checks, 'answers': values, 'groups': groups, 'task': task}


@lru_cache(maxsize=256)
def _honest_world(family, task, cfg_items):
    cfg = dict(cfg_items)
    if family == 'ring':
        return parent_make_world(task, cfg['community'] // 9, 0.0, True, cfg)
    if family == 'community':
        return community_make_world(task, cfg)
    raise ValueError('unknown graph family')


def honest_world(family, task, cfg):
    """The honest world of a root. It does not depend on k, policy, budget or check strength;
    callers must not modify the returned object (make_world copies what it changes)."""
    return _honest_world(family, task, tuple(sorted(cfg.items())))


# ---------------------------------------------------------------------- attacker overlay
def order_key(task, kind, ident):
    return hashlib.sha256(json.dumps([task, 'row-order', kind, ident]).encode()).hexdigest()


def make_world(family, task, k, attacker_pass, cfg, attacker, truthful=False):
    """Honest world plus one attacker whose 27 resource units are held by k identities.

    Unit r (0..26) is one report row, one attachment edge and one verification attempt:
      row r        skill RARE[r % 3], the root's fabricated value for that skill;
      edge r       to honest identity targets[r] (one ordered draw per root, trusted anchors excluded);
      attempt r    one pre-drawn uniform number; a check passes when it is below attacker_pass.
    Identity j of k holds the contiguous units j*27/k .. (j+1)*27/k - 1. Its name, age and
    activity are those drawn for its first unit, and a check of it consumes its first attempt
    unit, so nothing about an identity depends on k except how many units it holds.
    Identities of the one attacker are linked to each other at no cost by the frozen rule
    `internal_links` ('ring2': to the two nearest identities on each side in unit order,
    the degree-4 ring of the honest outside groups; 'none': no such links).
    k=0 gives the honest world alone. truthful=True replaces the fabricated value by the
    true value (qualification fixtures only: an identity that carries many rows and is right)."""
    units = attacker['units']
    assert k == 0 or (units % k == 0 and units % len(RARE) == 0)
    base = honest_world(family, task, cfg); pub = base['public']
    honest = sorted(pub['nodes']); nh = len(honest)
    labels = list(range(nh + units)); rng(task, 'labels').shuffle(labels)
    name = {x: f'u{labels[i]:03d}' for i, x in enumerate(honest)}
    adj = {name[x]: {name[y] for y in pub['adj'][x]} for x in honest}
    profiles = {name[x]: {'age': pub['nodes'][x]['age'], 'activity': pub['nodes'][x]['activity']} for x in honest}
    rows = {name[x]: [{'skill': pub['nodes'][x]['skill'], 'claim': pub['nodes'][x]['claim'],
                       'order': order_key(task, 'honest', name[x])}] for x in honest}
    truth = {name[x]: {'honest': True, 'specialist': base['groups'][x] > 0, 'principal': name[x]} for x in honest}
    checks = {name[x]: base['checks'][x] for x in honest}
    groups = {name[x]: base['groups'][x] for x in honest}
    trusted = sorted(name[x] for x in pub['trusted'])
    values = base['answers']
    offset = attacker['fabrication_offset'] * (1 if rng(task, 'fabrication').random() < 0.5 else -1)
    fabricated = {s: values[s] + offset for s in RARE}
    candidates = sorted(set(name.values()) - set(trusted))
    rng(task, 'attach').shuffle(candidates)
    targets = candidates[:units]
    outside = sorted((v['age'], v['activity']) for x, v in profiles.items() if groups[x] > 0)
    draws = [rng(task, 'attacker-attempt', r).random() for r in range(units)]
    identities = []; holdings = {}
    for j in range(k):
        first = j * units // k; held = list(range(first, (j + 1) * units // k))
        ident = f'u{labels[nh + first]:03d}'
        age, activity = outside[rng(task, 'profile', first).randrange(len(outside))]
        identities.append(ident); holdings[ident] = held
        profiles[ident] = {'age': age, 'activity': activity}
        rows[ident] = [{'skill': RARE[r % 3], 'claim': values[RARE[r % 3]] if truthful else fabricated[RARE[r % 3]],
                        'order': order_key(task, 'unit', r)} for r in held]
        adj[ident] = set()
        truth[ident] = {'honest': truthful, 'specialist': False,
                        'principal': 'synthetic-heavy-reporter' if truthful else 'synthetic-attacker'}
        groups[ident] = 3
        for r in held:
            assert targets[r] not in adj[ident]
            adj[ident].add(targets[r]); adj[targets[r]].add(ident)
    internal = 0
    if attacker['internal_links'] == 'ring2':
        for j in range(k):
            for step in (1, 2):
                a, b = identities[j], identities[(j + step) % k]
                if a != b and b not in adj[a]:
                    adj[a].add(b); adj[b].add(a); internal += 1
    elif attacker['internal_links'] != 'none':
        raise ValueError('unknown internal link rule')
    public = {'nodes': dict(sorted(profiles.items())), 'adj': {x: sorted(adj[x]) for x in sorted(adj)}, 'trusted': trusted}
    return {'family': family, 'task': task, 'k': k, 'attacker_pass': attacker_pass, 'truthful': truthful,
            'public': public, 'rows': rows, 'truth': truth, 'checks': checks,
            'attempts': {x: draws[holdings[x][0]] < attacker_pass for x in identities},
            'groups': groups, 'answers': values, 'fabricated': [fabricated.get(s) for s in range(SKILLS)],
            'identities': identities,
            'resources': {'units': units, 'holdings': holdings, 'targets': targets, 'draws': draws,
                          'internal_links': internal}}


# ------------------------------------------------- policies and ranking (parent instrument)
def rank(public, passed, failed, cfg):
    adj = public['adj']; active = sorted(set(adj) - set(failed))
    seeds = set(public['trusted']) | set(passed)
    seeds &= set(active)
    restart = cfg['pagerank_restart']
    scores = {x: 1 / len(active) for x in active}
    neighbors = {x: [y for y in adj[x] if y not in failed] for x in active}
    for _ in range(cfg['pagerank_iterations']):
        nxt = {x: restart / len(seeds) if x in seeds else 0.0 for x in active}
        for x in active:
            dest = neighbors[x] or sorted(seeds)
            for y in dest: nxt[y] += (1 - restart) * scores[x] / len(dest)
        scores = nxt
    return sorted(active, key=lambda x: (-scores[x], x)), scores


@lru_cache(maxsize=200000)
def tie_value(task, step, node):
    text = f'[{json.dumps(task)}, "tie", {json.dumps(step)}, {json.dumps(node)}]'
    return random.Random(int(hashlib.sha256(text.encode()).hexdigest(), 16)).random()


def select_check(public, arm, passed, failed, checked, task, step):
    """Which identity to check next. Uses the public graph and earlier check outcomes only."""
    candidates = sorted(set(public['nodes']) - set(public['trusted']) - set(checked))
    if not candidates: return None
    adj = public['adj']
    if arm == 'random':
        return max(candidates, key=lambda x: tie_value(task, step, x))
    if arm == 'degree': primary = {x: len(adj[x]) for x in candidates}
    elif arm == 'coverage':
        certified = set(public['trusted']) | set(passed)
        covered = set(certified)
        for x in certified: covered.update(adj[x])
        primary = {x: len(({x} | set(adj[x])) - covered) for x in candidates}
    else: raise ValueError('Unknown verification policy')
    best = max(primary.values())
    return max((x for x in candidates if primary[x] == best), key=lambda x: tie_value(task, step, x))


def plurality(world, admitted, by_identity=False):
    """Same-packet deterministic rule: the most reported value per skill, null on a tie or no
    report. by_identity counts each identity once per value instead of once per row."""
    out = {}
    for s in range(SKILLS):
        if by_identity:
            votes = [c for x in admitted for c in sorted({r['claim'] for r in world['rows'][x] if r['skill'] == s})]
        else:
            votes = [r['claim'] for x in admitted for r in world['rows'][x] if r['skill'] == s]
        best = Counter(votes).most_common()
        out[str(s)] = best[0][0] if best and (len(best) == 1 or best[0][1] > best[1][1]) else None
    return out


def admission_metrics(world, admitted, checked, passed):
    truth = world['truth']; rows = world['rows']
    bad = [x for x in admitted if not truth[x]['honest']]
    specialists = [x for x in truth if truth[x]['specialist']]
    packet_rows = sum(len(rows[x]) for x in admitted)
    bad_rows = sum(len(rows[x]) for x in bad)
    return {'admitted_count': len(admitted), 'packet_rows': packet_rows,
            'attacker_identities_admitted': len(bad), 'attacker_rows_admitted': bad_rows,
            'attacker_seat_share': len(bad) / len(admitted) if admitted else 0.0,
            'attacker_row_share': bad_rows / packet_rows if packet_rows else 0.0,
            'specialist_retention': sum(x in admitted for x in specialists) / len(specialists),
            'honest_rare_rows': sum(truth[x]['specialist'] for x in admitted),
            'checks': len(checked),
            'attacker_checked': sum(not truth[x]['honest'] for x in checked),
            'attacker_passed': sum(not truth[x]['honest'] for x in passed),
            'honest_failed': sum(truth[x]['honest'] and x not in passed for x in checked)}


def grade(values, answers, fabricated):
    """Evaluator: values is {'0'..'5': int or None}. A non-null value different from the truth is wrong."""
    correct = [values[str(s)] == answers[s] for s in range(SKILLS)]
    wrong = [values[str(s)] is not None and values[str(s)] != answers[s] for s in range(SKILLS)]
    return {'rare_accuracy': sum(correct[3:]) / 3, 'rare_wrong': sum(wrong[3:]) / 3,
            'rare_abstain': sum(values[str(s)] is None for s in RARE) / 3,
            'rare_fabricated': sum(fabricated[s] is not None and values[str(s)] == fabricated[s] for s in RARE) / 3,
            'task_accuracy': sum(correct) / SKILLS, 'correct_skills': sum(correct)}


def checkpoints(world, budgets, arms, cfg):
    """Run each policy to its largest budget; record the admitted set at each budget."""
    records = []; truth = world['truth']; units = world['resources']['units']
    for arm in arms:
        passed = set(); failed = set(); checked = []; events = []; attempts_used = 0
        targets = [0] if arm == 'no_verification' else sorted(set(budgets))
        for step in range(max(targets) + 1):
            if step:
                node = select_check(world['public'], arm, passed, failed, checked, world['task'], step)
                assert node is not None
                if truth[node]['honest']: ok = world['checks'][node]
                else:
                    # One verification attempt per checked attacker identity, out of 27; an identity
                    # is checked at most once and holds 27/k attempts, so the budget cannot run out.
                    attempts_used += 1; assert attempts_used <= units
                    ok = world['attempts'][node]
                checked.append(node); (passed if ok else failed).add(node)
                events.append({'node': node, 'pass': ok})
            if step in targets:
                ordering, _ = rank(world['public'], passed, failed, cfg)
                admitted = ordering[:cfg['admission_seats']]
                records.append({'arm': arm, 'checks': step, 'admitted': admitted, 'passed': sorted(passed),
                                'checked': list(checked), 'events': list(events),
                                'admission': admission_metrics(world, admitted, checked, passed)})
    return records
