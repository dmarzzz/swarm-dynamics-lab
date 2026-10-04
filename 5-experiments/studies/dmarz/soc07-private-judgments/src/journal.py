"""Append-only event journal with a hash chain. One file per stage attempt; fsync on every event."""
import hashlib
import json
import os
import threading
import time

GENESIS = '0' * 64


class Journal:
    def __init__(self, path, header, durable=True):
        self.path = path
        self.durable = durable
        self._lock = threading.Lock()
        self._seq = 0
        self._prev = GENESIS
        self._file = open(path, 'x', encoding='utf-8')
        self.append('journal_open', **header)

    def append(self, kind, **fields):
        with self._lock:
            event = {'seq': self._seq, 'kind': kind, 'time': time.time(), 'prev': self._prev}
            event.update(fields)
            body = json.dumps(event, sort_keys=True, separators=(',', ':'))
            event_hash = hashlib.sha256(body.encode()).hexdigest()
            self._file.write(json.dumps({'event': event, 'hash': event_hash}, sort_keys=True) + '\n')
            self._file.flush()
            if self.durable:
                os.fsync(self._file.fileno())
            self._seq += 1
            self._prev = event_hash
            return event

    def close(self):
        with self._lock:
            self._file.close()


def read(path):
    """Yield events after verifying order and the hash chain; raises on any break."""
    prev, seq = GENESIS, 0
    with open(path, encoding='utf-8') as f:
        for line in f:
            row = json.loads(line)
            event = row['event']
            body = json.dumps(event, sort_keys=True, separators=(',', ':'))
            if event['seq'] != seq or event['prev'] != prev or hashlib.sha256(body.encode()).hexdigest() != row['hash']:
                raise ValueError('journal chain broken at seq %d' % seq)
            prev, seq = row['hash'], seq + 1
            yield event
