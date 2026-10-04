"""Task and evidence generator: the two-option supplier decision (plan section 4).

A world is one decision problem. Its truth is keyed by (stage, world_index) only, never by repeat.
generate() returns the PUBLIC world (records and evidence allocation) and, separately, the
PROTECTED truth. Only the controller's evaluator holds the truth; the context builder is never
given it. presentation() fixes the per-repeat A/B mapping, evidence ids and arm order.

Rule the agents are told: choose the lowest-cost option among those meeting the delivery
deadline, using the latest authorized record for each value.

Fixed sampling rule: draw an old state and one later audit uniformly from the stated ranges and
reject the draw unless it matches the world's specification (regime, kind, cost-gap bin, whether
the audit is decisive) and has exactly one correct option under both the old and current
records. Rejection happens here, before any model response exists.
"""
import config
import seeds

SUPPLIERS = ('s0', 's1')
FIELDS = ('cost', 'delivery')
DEADLINE = 5
COST_RANGE = (20, 100)
DELIVERY_RANGE = (1, 10)
GAP_BINS = ((1, 3), (4, 10), (11, 20))
ESTIMATE_DAYS = (1, 2, 3, 4)
AUDIT_DAYS = (6, 9)
MAX_DRAWS = 400000
RECORD_KEYS = ('r0', 'r1', 'r2', 'r3', 'r4')
EVIDENCE_IDS = ('e01', 'e02', 'e03', 'e04', 'e05')


def root_seed():
    return config.design()['seeds']['development_root']


def spec(stage, world_index):
    """Deterministic world specification from the index: regimes are interleaved, kinds alternate
    inside a regime, cost-gap bins cycle, and in the clean regime the audit is decisive in half."""
    regime = config.REGIMES[world_index % 3]
    k = world_index // 3
    kind = 'cost' if k % 2 == 0 else 'feasibility'
    decisive = True if regime != 'clean' else (k // 2) % 2 == 0
    gap_bin = (k // 2 + config.REGIMES.index(regime)) % 3 if kind == 'cost' else None
    return {'regime': regime, 'index_in_regime': k, 'kind': kind, 'audit_decisive': decisive, 'gap_bin': gap_bin}


def _winner(cost, delivery):
    feasible = [s for s in SUPPLIERS if delivery[s] <= DEADLINE]
    if len(feasible) == 1:
        return feasible[0]
    if not feasible or cost['s0'] == cost['s1']:
        return None
    return 's0' if cost['s0'] < cost['s1'] else 's1'


def _draw(rng, want):
    old = {'cost': {s: rng.randint(*COST_RANGE) for s in SUPPLIERS},
           'delivery': {s: rng.randint(*DELIVERY_RANGE) for s in SUPPLIERS}}
    target, field = rng.choice(SUPPLIERS), rng.choice(FIELDS)
    value = rng.randint(*(COST_RANGE if field == 'cost' else DELIVERY_RANGE))
    if value == old[field][target]:
        return None
    new = {f: dict(old[f]) for f in FIELDS}
    new[field][target] = value
    old_winner, winner = _winner(old['cost'], old['delivery']), _winner(new['cost'], new['delivery'])
    if old_winner is None or winner is None:
        return None
    if (old_winner != winner) != want['audit_decisive']:
        return None
    loser = 's1' if winner == 's0' else 's0'
    both_feasible = all(new['delivery'][s] <= DEADLINE for s in SUPPLIERS)
    if want['kind'] == 'cost':
        if not both_feasible:
            return None
        low, high = GAP_BINS[want['gap_bin']]
        if not low <= new['cost'][loser] - new['cost'][winner] <= high:
            return None
    else:
        # Feasibility decides: the losing option misses the deadline and would otherwise win on cost.
        if both_feasible or not new['cost'][loser] < new['cost'][winner]:
            return None
    return old, {'supplier': target, 'field': field, 'value': value}, old_winner, winner


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
    old, audit, old_winner, winner = result
    days = rng.shuffled(ESTIMATE_DAYS)
    records, n = [], 0
    for supplier in SUPPLIERS:
        for field in FIELDS:
            records.append({'key': RECORD_KEYS[n], 'supplier': supplier, 'field': field,
                            'value': old[field][supplier], 'day': days[n], 'source': 'estimate'})
            n += 1
    records.append({'key': 'r4', 'supplier': audit['supplier'], 'field': audit['field'],
                    'value': audit['value'], 'day': rng.randint(*AUDIT_DAYS), 'source': 'audit'})
    estimates, everything = list(RECORD_KEYS[:4]), list(RECORD_KEYS)
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
             'allocation': allocation, 'special_agent': special}
    canary = 'TRUTH-%012x' % (seeds.derive(root, 'world', key, world_index, 'canary') >> 16)
    truth = {'world': world['id'], 'correct': winner, 'old_favored': old_winner, 'canary': canary}
    return world, truth


def _balanced_labels(stage, regime):
    """Displayed correct label in repeat 0 for each world of a regime: half A, half B."""
    n = config.stage_config(stage)['worlds_per_regime']
    rng = seeds.Stream(seeds.derive(root_seed(), 'labels', config.seed_stage(stage), regime))
    return rng.shuffled(['A', 'B'] * (n // 2) + ['A'] * (n % 2))


def presentation(world, truth, repeat):
    """Per-repeat display: A/B mapping (flipped on odd repeats), evidence ids and arm order.
    The mapping is stored apart from the truth and scoring always goes through it."""
    stage, key, index = world['stage'], world['seed_stage'], world['world_index']
    correct_label = _balanced_labels(stage, world['meta']['regime'])[world['meta']['index_in_regime']]
    if repeat % 2 == 1:
        correct_label = 'B' if correct_label == 'A' else 'A'
    other = 's1' if truth['correct'] == 's0' else 's0'
    label_of = {truth['correct']: correct_label, other: 'B' if correct_label == 'A' else 'A'}
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
