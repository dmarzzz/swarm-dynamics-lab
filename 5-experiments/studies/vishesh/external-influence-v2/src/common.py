"""Reproducible fixture utilities; this module never reads credentials."""
import hashlib
import json
import random


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def rng(*parts):
    return random.Random(int(digest(parts)[:16], 16))


def mean(values):
    return sum(values) / len(values) if values else None


def bootstrap(values, seed=719, n=2000):
    if not values:
        return None
    r = random.Random(seed)
    samples = sorted(mean(r.choices(values, k=len(values))) for _ in range(n))
    return [samples[int(.025*n)], samples[int(.975*n)-1]]
