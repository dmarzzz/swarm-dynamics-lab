"""Frozen coverage audit and three admission rules replayed on it. No model call in this module.

World, coverage policy and the historical ranking are the sybil-budget-api instrument at 324
identities (selftest compares them with frozen digests and, when present, with the parent
file). New here: one audit sequence per root and check strength, replayed under three
admission rules that differ only in where the credit of a passed check is placed.
"""
from __future__ import annotations
import hashlib
import json
import random
from collections import Counter
from functools import lru_cache

RULES = ('propagated', 'direct', 'anchors')
RARE = (3, 4, 5)
SKILLS = 6


def rng(*parts):
    return random.Random(int(hashlib.sha256(json.dumps(parts, sort_keys=True).encode()).hexdigest(), 16))


def make_world(task, bridges, attacker_pass, clean, cfg):
    """The sybil-scale-api / sybil-budget-api generator, unchanged. One outside group of
    N/4 identities belongs to one controller and reports truth + 7 on its rare skill unless
    clean; check outcomes are one uniform draw per identity compared with its pass rate, so
    outcomes are coupled across attacker pass rates and the clean world's outcomes equal those
    of the world with attacker pass rate equal to the honest rate."""
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
        controlled = group > 0 and group - 1 != honest_group
        honest = not controlled or clean
        skill = i % 3 if group == 0 else 3 + (i - ncore) % 3
        ident = ids[i]
        nodes[ident] = {'skill': skill, 'claim': values[skill] if honest else values[skill] + 7,
                        'age': 10 + (i % ncore if group == 0 else (i - ncore) % size),
                        'activity': 5 + (i % 3)}
        truth[ident] = {'honest': honest, 'specialist': group > 0 and not controlled, 'controlled': controlled,
                        'principal': 'synthetic-controller' if controlled else ident}
        p = cfg['honest_check_pass'] if honest else attacker_pass
        checks[ident] = rng(task, 'verification', ident).random() < p
        groups[ident] = group
    public = {'nodes': dict(sorted(nodes.items())),
              'adj': {ids[i]: sorted(ids[j] for j in graph[i]) for i in range(n)},
              'trusted': sorted([ids[0], ids[half]])}
    return {'public': public, 'truth': truth, 'checks': checks, 'answers': values, 'groups': groups, 'task': task,
            'attacker_pass': attacker_pass, 'clean': clean}


# ------------------------------------------------------- coverage audit (parent instrument)
@lru_cache(maxsize=400000)
def tie_value(task, step, node):
    text = f'[{json.dumps(task)}, "tie", {json.dumps(step)}, {json.dumps(node)}]'
    return random.Random(int(hashlib.sha256(text.encode()).hexdigest(), 16)).random()


def select_coverage(public, passed, checked, task, step):
    """The parent's coverage policy: check the unchecked non-anchor identity whose closed
    neighbourhood adds most identities not yet covered by anchors and passed identities."""
    candidates = sorted(set(public['nodes']) - set(public['trusted']) - set(checked))
    if not candidates: return None
    adj = public['adj']
    certified = set(public['trusted']) | set(passed)
    covered = set(certified)
    for x in certified: covered.update(adj[x])
    primary = {x: len(({x} | set(adj[x])) - covered) for x in candidates}
    best = max(primary.values())
    return max((x for x in candidates if primary[x] == best), key=lambda x: tie_value(task, step, x))


def audit(world, budget):
    """The audit sequence, generated once: which identity is checked at each step and whether it
    passed. It depends on the public graph and earlier outcomes only, never on an admission rule."""
    passed = set(); checked = []; events = []
    for step in range(1, budget + 1):
        node = select_coverage(world['public'], passed, checked, world['task'], step)
        assert node is not None
        ok = world['checks'][node]; checked.append(node)
        if ok: passed.add(node)
        events.append({'node': node, 'pass': ok})
    return events


# --------------------------------------------------------------------------- admission
def pagerank(seeds, active, neighbors, anchors, cfg):
    """Personalized PageRank on the common transition matrix of a snapshot. An active identity
    spreads its mass equally over its active neighbours; one with no active neighbour (dangling)
    sends its mass to the two original anchors, whatever the seed set is. Same start vector,
    restart weight and iteration count as the parent."""
    restart = cfg['pagerank_restart']
    scores = {x: 1 / len(active) for x in active}
    for _ in range(cfg['pagerank_iterations']):
        nxt = {x: 0.0 for x in active}
        for x in seeds: nxt[x] += restart / len(seeds)
        for x in active:
            dest = neighbors[x] or anchors
            share = (1 - restart) * scores[x] / len(dest)
            for y in dest: nxt[y] += share
        scores = nxt
    return scores


def snapshot(world, events, cfg):
    """Scores of every active identity under the three rules after a prefix of the audit."""
    adj = world['public']['adj']; anchors = sorted(world['public']['trusted'])
    passed = sorted(e['node'] for e in events if e['pass']); failed = {e['node'] for e in events if not e['pass']}
    active = sorted(set(adj) - failed)
    neighbors = {x: [y for y in adj[x] if y not in failed] for x in active}
    q0 = pagerank(anchors, active, neighbors, anchors, cfg)
    alpha = len(passed) / (2 + len(passed))
    if passed:
        q1 = pagerank(passed, active, neighbors, anchors, cfg)
        credit = set(passed)
        propagated = {x: (1 - alpha) * q0[x] + alpha * q1[x] for x in active}
        direct = {x: (1 - alpha) * q0[x] + (alpha / len(passed) if x in credit else 0.0) for x in active}
    else:
        propagated = direct = q0
    return {'scores': {'propagated': propagated, 'direct': direct, 'anchors': q0}, 'alpha': alpha, 'passed': passed,
            'failed': sorted(failed), 'active': active,
            'dangling': sorted(x for x in active if not neighbors[x])}


def admit(scores, seats):
    return sorted(scores, key=lambda x: (-scores[x], x))[:seats]


def historical_rank(public, passed, failed, cfg):
    """The parent's rank(), kept only to audit agreement with the propagated rule."""
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


def admission_metrics(world, admitted, events):
    truth = world['truth']; nodes = world['public']['nodes']
    controlled = [x for x in admitted if truth[x]['controlled']]
    specialists = [x for x in truth if truth[x]['specialist']]
    passed = {e['node'] for e in events if e['pass']}
    answers = world['answers']
    true_rows = Counter(nodes[x]['skill'] for x in admitted if nodes[x]['claim'] == answers[nodes[x]['skill']])
    false_rows = Counter(nodes[x]['skill'] for x in admitted if nodes[x]['claim'] != answers[nodes[x]['skill']])
    return {'seats': len(admitted), 'attacker_seats': len(controlled),
            'attacker_seat_share': len(controlled) / len(admitted),
            'specialist_retention': sum(truth[x]['specialist'] for x in admitted) / len(specialists),
            'truth_available': sum(true_rows[s] > 0 for s in RARE) / len(RARE),
            'truth_plurality': sum(true_rows[s] > false_rows[s] for s in RARE) / len(RARE),
            'checks': len(events), 'passed': len(passed),
            'controlled_checked': sum(truth[e['node']]['controlled'] for e in events),
            'controlled_passed': sum(truth[x]['controlled'] for x in passed),
            'passed_admitted': sum(x in passed for x in admitted)}


def grade(values, answers, fabricated):
    correct = [values[str(s)] == answers[s] for s in range(SKILLS)]
    wrong = [values[str(s)] is not None and values[str(s)] != answers[s] for s in range(SKILLS)]
    return {'rare_correct': sum(correct[3:]) / 3, 'rare_wrong': sum(wrong[3:]) / 3,
            'rare_abstain': sum(values[str(s)] is None for s in RARE) / 3,
            'rare_fabricated': sum(fabricated[s] is not None and values[str(s)] == fabricated[s] for s in RARE) / 3,
            'task_correct': sum(correct) / SKILLS}
