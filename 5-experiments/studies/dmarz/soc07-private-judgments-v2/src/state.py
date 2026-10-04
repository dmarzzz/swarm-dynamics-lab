"""Private first-answer vault and immutable public board snapshots.

Vault: write-once per agent. Readable by the controller, the evaluator and the owning agent's
own context only; any other reader is refused. Peer visibility is an explicit allowlist of
fields, applied by the controller when it publishes to the board (PUBLIC: choice, confidence).

Board: publish() freezes content as canonical JSON and returns a snapshot with its SHA-256.
A snapshot cannot be changed; reading it returns a fresh copy.

These are in-process boundaries for a study with no tools. They are not a defence against
arbitrary code; the model only ever receives text from contexts.py.
"""
import hashlib
import json

PUBLIC_INITIAL_FIELDS = ('choice', 'confidence')


class AccessDenied(Exception):
    pass


class Vault:
    def __init__(self):
        self._entries = {}
        self.reads = []

    def put(self, agent, record, raw):
        if agent in self._entries:
            raise AccessDenied('vault entry is write-once')
        self._entries[agent] = json.dumps({'record': record, 'raw': raw}, sort_keys=True)

    def clone(self):
        """An isolated copy for one arm's continuation: same first-pass entries, separate store."""
        other = Vault()
        other._entries = dict(self._entries)
        return other

    def has(self, agent):
        return agent in self._entries

    def read(self, agent, reader):
        """reader: 'controller', 'evaluator' or ('agent', n). Only agent n may read entry n."""
        allowed = reader in ('controller', 'evaluator') or reader == ('agent', agent)
        self.reads.append({'entry': agent, 'reader': reader if isinstance(reader, str) else 'agent:%d' % reader[1],
                           'allowed': allowed})
        if not allowed:
            raise AccessDenied('reader may not read this vault entry')
        if agent not in self._entries:
            return None
        return json.loads(self._entries[agent])

    def public_fields(self, agent):
        """The allowlisted fields a PUBLIC board may show, or the unavailable placeholder."""
        entry = self.read(agent, 'controller')
        if entry is None or entry['record'] is None:
            return {'agent': agent, 'unavailable': True}
        return dict({'agent': agent}, **{k: entry['record'][k] for k in PUBLIC_INITIAL_FIELDS})


class Snapshot:
    __slots__ = ('kind', '_frozen', 'sha256')

    def __init__(self, kind, content):
        object.__setattr__(self, 'kind', kind)
        object.__setattr__(self, '_frozen', json.dumps(content, sort_keys=True, separators=(',', ':')))
        object.__setattr__(self, 'sha256', hashlib.sha256((kind + '\n' + self._frozen).encode()).hexdigest())

    def __setattr__(self, name, value):
        raise AttributeError('board snapshots are immutable')

    def content(self):
        return json.loads(self._frozen)


class Board:
    def __init__(self):
        self._snapshots = []

    def publish(self, kind, content):
        if any(s.kind == kind for s in self._snapshots):
            raise AccessDenied('board snapshot kind already published: ' + kind)
        snapshot = Snapshot(kind, content)
        self._snapshots.append(snapshot)
        return snapshot

    def get(self, kind):
        for snapshot in self._snapshots:
            if snapshot.kind == kind:
                return snapshot
        return None

    def hashes(self):
        return {s.kind: s.sha256 for s in self._snapshots}
