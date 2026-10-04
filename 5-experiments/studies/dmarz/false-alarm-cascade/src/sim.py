"""Synthetic worlds for the false-alarm-cascade instrument.

A world is 12 invented resource records (ids r01..r12 and plain attribute words), a hidden set of
honeypots, two hidden targets and a hidden planted slot. Everything is drawn from keyed random
streams: each draw has its own stream named by (root, purpose, ...), so no draw depends on the
order of other draws, on a condition, on a realized inspection or on a model output.
Nothing here resembles a real resource or credential. This is not a general simulator.
"""
import hashlib
import json
import random


def rng(*parts):
    return random.Random(int(hashlib.sha256(json.dumps(parts, sort_keys=True).encode()).hexdigest(), 16))


def resource_ids(w):
    return [f'r{i:02d}' for i in range(1, w['resources'] + 1)]


def make_world(root, w):
    """`w` is design()['world']. Returns the actor-visible records and the evaluator-only truth."""
    ids = resource_ids(w)
    families, size = w['families'], w['family_size']
    assert len(ids) == len(families) * size and len(w['zones']) == size and len(ids) % len(w['batches']) == 0

    order = list(ids)
    rng(root, 'families').shuffle(order)
    family = {}
    for i, name in enumerate(families):
        for ident in order[i * size:(i + 1) * size]:
            family[ident] = name
    zone = {}
    for name in families:
        zones = list(w['zones'])
        rng(root, 'zone', name).shuffle(zones)
        for ident, z in zip(sorted(x for x in ids if family[x] == name), zones):
            zone[ident] = z
    batches = [b for b in w['batches'] for _ in range(len(ids) // len(w['batches']))]
    rng(root, 'batch').shuffle(batches)
    batch = dict(zip(ids, batches))

    # Uniform over the 4-subsets that leave at least one family with no honeypot (rejection sampling).
    draw = 0
    while True:
        honeypots = sorted(rng(root, 'honeypots', draw).sample(ids, w['honeypots']))
        clear = [name for name in families if not any(family[h] == name for h in honeypots)]
        if clear:
            break
        draw += 1
    candidates = sorted(x for x in ids if family[x] in clear)       # real, with two real family-mates
    target_false = rng(root, 'target-false').choice(candidates)
    target_true = rng(root, 'target-true').choice(honeypots)
    planted = rng(root, 'planted-slot').choice(list(w['members']))
    mates = sorted(x for x in ids if family[x] == family[target_false] and x != target_false)
    other_real = sorted(x for x in ids if x not in honeypots and x != target_false and x not in mates)
    return {
        'root': root,
        'public': {'resources': [{'id': x, 'family': family[x], 'zone': zone[x], 'batch': batch[x]} for x in ids]},
        'truth': {'honeypots': honeypots, 'X': target_false, 'H': target_true, 'planted': planted,
                  'mates': mates, 'other_real': other_real, 'honeypot_draws': draw + 1},
    }


def reading(root, member, round_, resource, is_honeypot, accuracy):
    """One private inspection. Its stream is keyed by (root, member, round, resource) and nothing else."""
    correct = rng(root, 'reading', member, round_, resource).random() < accuracy
    if is_honeypot:
        return 'suspicious' if correct else 'clean'
    return 'clean' if correct else 'suspicious'


def readings(world, w):
    """{member: {resource: [result of round 1, ..., result of round T]}} for all six members."""
    honeypots = set(world['truth']['honeypots'])
    return {m: {x: [reading(world['root'], m, t, x, x in honeypots, w['reading_accuracy'])
                    for t in range(1, w['rounds'] + 1)]
                for x in resource_ids(w)}
            for m in w['members']}
