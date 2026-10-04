"""Task and evidence generator, design v2: the three-option supplier decision.

A world is one decision problem. Its truth is keyed by (stage, world_index) only, never by repeat.
generate() returns the PUBLIC world (records and evidence allocation) and, separately, the
PROTECTED truth. Only the controller's evaluator holds the truth; the context builder is never
given it. presentation() fixes the per-repeat A/B/C mapping, evidence ids and arm order.

Rule the agents are told: choose the lowest-cost option among those meeting the delivery deadline
(delivery at or before the deadline meets it), using the latest authorized record for each value.

What is harder than v1 (README, "Why v2"):
- three options instead of two;
- eleven records instead of five: per option a cost and a delivery estimate, plus one earlier
  estimate of one of its values that a later estimate supersedes, and two audits;
- two audits. Pattern 'conflict': the second audit revises the same value as the first, so the
  first audit is itself superseded and, read alone, points to a wrong answer. Pattern
  'independent': the audits touch different values and only one of them changes the answer;
- smaller cost margins between the winner and the next-cheapest on-time option (1-2, 3-5, 6-9);
- deadline-boundary worlds, where the winning option's latest delivery equals the deadline.

Fixed sampling rule: draw estimates and audits uniformly from the stated ranges and reject the
draw unless it matches the world's specification and has exactly one correct option under both
the estimates alone and the current records. Rejection happens here, before any model response.
"""
import config
import seeds

SUPPLIERS = ('s0', 's1', 's2')
LABELS = ('A', 'B', 'C')
FIELDS = ('cost', 'delivery')
DEADLINE = 5
COST_RANGE = (20, 100)
DELIVERY_RANGE = (1, 10)
GAP_BINS = ((1, 2), (3, 5), (6, 9))
EARLY_DAYS = (1, 2, 3)
ESTIMATE_DAYS = (4, 5, 6, 7)
AUDIT1_DAYS = (8, 9)
AUDIT2_DAYS = (10, 12)
PATTERNS = ('conflict', 'independent')
MAX_DRAWS = 2000000
N_EARLY = len(SUPPLIERS)
N_ESTIMATES = N_EARLY + len(SUPPLIERS) * len(FIELDS)
RECORD_KEYS = tuple('r%02d' % i for i in range(N_ESTIMATES + 2))
ESTIMATE_KEYS = RECORD_KEYS[:N_ESTIMATES]
AUDIT_KEYS = RECORD_KEYS[N_ESTIMATES:]
EVIDENCE_IDS = tuple('e%02d' % (i + 1) for i in range(len(RECORD_KEYS)))


def root_seed():
    return config.design()['seeds']['development_root']


def spec(stage, world_index):
    """Deterministic world specification from the index: regimes are interleaved, kinds alternate
    inside a regime, cost-gap bins cycle, audit patterns alternate, every third world of a regime
    is a deadline-boundary world, and in the clean regime the audits are decisive in half."""
    regime = config.REGIMES[world_index % 3]
    k = world_index // 3
    kind = 'cost' if k % 2 == 0 else 'feasibility'
    decisive = True if regime != 'clean' else (k // 2) % 2 == 0
    gap_bin = (k // 2 + config.REGIMES.index(regime)) % 3 if kind == 'cost' else None
    pattern = PATTERNS[(k // 2) % 2] if decisive else PATTERNS[k % 2]
    boundary = k % 3 == 2
    return {'regime': regime, 'index_in_regime': k, 'kind': kind, 'audit_decisive': decisive, 'gap_bin': gap_bin,
            'audit_pattern': pattern, 'boundary': boundary}


def winner(cost, delivery):
    """Unique lowest-cost option among those whose delivery is at or before the deadline, else None."""
    on_time = [s for s in SUPPLIERS if delivery[s] <= DEADLINE]
    if not on_time:
        return None
    ranked = sorted(on_time, key=lambda s: cost[s])
    if len(ranked) > 1 and cost[ranked[0]] == cost[ranked[1]]:
        return None
    return ranked[0]


def _apply(state, updates):
    new = {f: dict(state[f]) for f in FIELDS}
    for supplier, field, value in updates:
        new[field][supplier] = value
    return new


def _value(rng, field):
    return rng.randint(*(COST_RANGE if field == 'cost' else DELIVERY_RANGE))


def _draw(rng, want):
    old = {'cost': {s: _value(rng, 'cost') for s in SUPPLIERS},
           'delivery': {s: _value(rng, 'delivery') for s in SUPPLIERS}}
    slots = [(s, f) for s in SUPPLIERS for f in FIELDS]
    slot1 = rng.choice(slots)
    a1 = (slot1[0], slot1[1], _value(rng, slot1[1]))
    if want['audit_pattern'] == 'conflict':
        slot2 = slot1
    else:
        slot2 = rng.choice([s for s in slots if s != slot1])
    a2 = (slot2[0], slot2[1], _value(rng, slot2[1]))
    if a1[2] == old[a1[1]][a1[0]] or a2[2] == old[a2[1]][a2[0]] or (slot2 == slot1 and a2[2] == a1[2]):
        return None
    current = _apply(old, [a1, a2])
    old_winner, win = winner(old['cost'], old['delivery']), winner(current['cost'], current['delivery'])
    if old_winner is None or win is None:
        return None
    if (old_winner != win) != want['audit_decisive']:
        return None
    first_only = winner(*(lambda s: (s['cost'], s['delivery']))(_apply(old, [a1])))
    second_only = winner(*(lambda s: (s['cost'], s['delivery']))(_apply(old, [a2])))
    if want['audit_pattern'] == 'conflict':
        # The superseded first audit, read without the second, must not give the current answer.
        if first_only is None or first_only == win:
            return None
    elif want['audit_decisive']:
        # Exactly one of the two audits is decisive on its own; the other leaves the old answer.
        if sorted([first_only == win, second_only == win]) != [False, True]:
            return None
        if (second_only if first_only == win else first_only) != old_winner:
            return None
    on_time = [s for s in SUPPLIERS if current['delivery'][s] <= DEADLINE]
    others = sorted((s for s in on_time if s != win), key=lambda s: current['cost'][s])
    cheaper_late = [s for s in SUPPLIERS if s not in on_time and current['cost'][s] < current['cost'][win]]
    if want['kind'] == 'cost':
        if not others or cheaper_late:
            return None
        low, high = GAP_BINS[want['gap_bin']]
        if not low <= current['cost'][others[0]] - current['cost'][win] <= high:
            return None
    else:
        # Feasibility decides: some option that misses the deadline would otherwise win on cost.
        if not cheaper_late:
            return None
    if want['boundary'] != (current['delivery'][win] == DEADLINE):
        return None
    early = []
    for s in SUPPLIERS:
        f = rng.choice(FIELDS)
        v = _value(rng, f)
        if v == old[f][s]:
            return None
        early.append((s, f, v))
    return old, early, a1, a2, old_winner, win


def generate(stage, world_index):
    """Return (public_world, truth)."""
    cfg = config.stage_config(stage)
    if not 0 <= world_index < cfg['worlds']:
        raise ValueError('world index outside the stage allocation')
    want = spec(stage, world_index)
    root = root_seed()
    key = config.seed_stage(stage)
    rng = seeds.Stream(seeds.derive(root, 'world', key, world_index))
    for draws in range(1, MAX_DRAWS + 1):
        result = _draw(rng, want)
        if result:
            break
    else:
        raise RuntimeError('generator could not satisfy the specification')
    old, early, a1, a2, old_winner, win = result
    keys = iter(RECORD_KEYS)
    records = []
    for supplier, field, value in early:
        records.append({'key': next(keys), 'supplier': supplier, 'field': field, 'value': value,
                        'day': rng.choice(EARLY_DAYS), 'source': 'estimate'})
    days = rng.shuffled(ESTIMATE_DAYS * 2)[:len(SUPPLIERS) * len(FIELDS)]
    n = 0
    for supplier in SUPPLIERS:
        for field in FIELDS:
            records.append({'key': next(keys), 'supplier': supplier, 'field': field, 'value': old[field][supplier],
                            'day': days[n], 'source': 'estimate'})
            n += 1
    records.append({'key': next(keys), 'supplier': a1[0], 'field': a1[1], 'value': a1[2],
                    'day': rng.choice(AUDIT1_DAYS), 'source': 'audit'})
    records.append({'key': next(keys), 'supplier': a2[0], 'field': a2[1], 'value': a2[2],
                    'day': rng.randint(*AUDIT2_DAYS), 'source': 'audit'})
    estimates, everything = list(ESTIMATE_KEYS), list(RECORD_KEYS)
    offset = seeds.Stream(seeds.derive(root, 'allocation', key)).randbelow(config.AGENTS)
    special = None if want['regime'] == 'clean' else (offset + want['index_in_regime']) % config.AGENTS
    allocation = {}
    for agent in range(config.AGENTS):
        if want['regime'] == 'clean':
            allocation[agent] = everything
        elif want['regime'] == 'informed_minority':
            allocation[agent] = everything if agent == special else estimates
        else:
            allocation[agent] = estimates if agent == special else everything
    world = {'id': '%s-w%04d' % (key, world_index), 'stage': stage, 'seed_stage': key, 'world_index': world_index,
             'meta': dict(want, generator_draws=draws), 'deadline': DEADLINE, 'records': records,
             'allocation': allocation, 'special_agent': special, 'audit_keys': list(AUDIT_KEYS)}
    canary = 'TRUTH-%012x' % (seeds.derive(root, 'world', key, world_index, 'canary') >> 16)
    truth = {'world': world['id'], 'correct': win, 'old_favored': old_winner, 'canary': canary}
    return world, truth


def _balanced_labels(stage, regime):
    """Displayed correct label in repeat 0 for each world of a regime: as even as possible over A, B, C."""
    n = config.stage_config(stage)['worlds_per_regime']
    rng = seeds.Stream(seeds.derive(root_seed(), 'labels', config.seed_stage(stage), regime))
    pool = list(LABELS) * (n // len(LABELS)) + list(LABELS[:n % len(LABELS)])
    return rng.shuffled(pool)


def presentation(world, truth, repeat):
    """Per-repeat display: A/B/C mapping (rotated on odd repeats), evidence ids and arm order.
    The mapping is stored apart from the truth and scoring always goes through it."""
    stage, key, index = world['stage'], world['seed_stage'], world['world_index']
    correct_label = _balanced_labels(stage, world['meta']['regime'])[world['meta']['index_in_regime']]
    rest = [s for s in SUPPLIERS if s != truth['correct']]
    rest = seeds.Stream(seeds.derive(root_seed(), 'labels', key, index, 'others')).shuffled(rest)
    others = [label for label in LABELS if label != correct_label]
    label_of = {truth['correct']: correct_label, rest[0]: others[0], rest[1]: others[1]}
    if repeat % 2 == 1:
        rotate = {LABELS[i]: LABELS[(i + 1) % len(LABELS)] for i in range(len(LABELS))}
        label_of = {s: rotate[label] for s, label in label_of.items()}
    order = seeds.Stream(seeds.derive(root_seed(), 'order', key, index, repeat))
    evidence_id = dict(zip(RECORD_KEYS, order.shuffled(EVIDENCE_IDS)))
    stage_arms = config.stage_config(stage)['arms']
    arms = seeds.Stream(seeds.derive(root_seed(), 'order', key, index, repeat, 'arms')).shuffled(stage_arms)
    return {'world': world['id'], 'repeat': repeat, 'label_of': label_of, 'evidence_id': evidence_id,
            'arm_order': arms}


def replay_focal(world):
    """Controlled replay: the focal model agent is never the special-role agent, so its four
    scripted peers are three agents of its own role plus the special one (plan section 5)."""
    k = world['meta']['index_in_regime']
    if world['special_agent'] is None:
        return k % config.AGENTS
    return (world['special_agent'] + 1 + k % (config.AGENTS - 1)) % config.AGENTS
