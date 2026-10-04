"""Keyed seed streams (plan section 4, design.json "seeds").

derive(): SHA-256 of the canonical JSON array of the key parts; first 8 bytes, big-endian.
Stream: a portable SHA-256 counter generator, so draws are identical on every Python version.
Each stream is addressed by its full key; no mutable generator is shared across treatments.
"""
import hashlib
import json

STREAMS = ('world', 'allocation', 'labels', 'order', 'initial', 'policy', 'analysis')


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def derive(root, stream, *keys):
    if stream not in STREAMS:
        raise ValueError('unknown seed stream: %r' % (stream,))
    digest = hashlib.sha256(canonical([root, stream, *keys]).encode()).digest()
    return int.from_bytes(digest[:8], 'big')


class Stream:
    def __init__(self, seed):
        self.seed = int(seed)
        self.counter = 0

    def _word(self):
        block = hashlib.sha256(('%d:%d' % (self.seed, self.counter)).encode()).digest()
        self.counter += 1
        return int.from_bytes(block[:8], 'big')

    def randbelow(self, n):
        if n <= 0:
            raise ValueError('n must be positive')
        limit = (1 << 64) - ((1 << 64) % n)  # rejection sampling: no modulo bias
        while True:
            word = self._word()
            if word < limit:
                return word % n

    def randint(self, low, high):
        return low + self.randbelow(high - low + 1)

    def choice(self, items):
        return items[self.randbelow(len(items))]

    def shuffled(self, items):
        out = list(items)
        for i in range(len(out) - 1, 0, -1):
            j = self.randbelow(i + 1)
            out[i], out[j] = out[j], out[i]
        return out
