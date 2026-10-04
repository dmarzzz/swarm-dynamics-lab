"""Durable append-only journal and strict, network-free response playback."""
import copy
import json
import os
from tasks import digest
from .contracts import strict_json


class Journal:
    def __init__(self, path=None):
        self.events = []
        self.handle = open(path, 'x', encoding='utf-8') if path is not None else None

    def emit(self, kind, **data):
        event = {'seq': len(self.events), 'previous': self.events[-1]['hash'] if self.events else '0' * 64,
                 'kind': kind, **copy.deepcopy(data)}
        event['hash'] = digest(event)
        if self.handle:
            self.handle.write(json.dumps(event, sort_keys=True) + '\n')
            self.handle.flush(); os.fsync(self.handle.fileno())
        self.events.append(event)
        return event

    def close(self):
        if self.handle: self.handle.close()


def read_events(path):
    events = []; previous = '0' * 64
    with open(path, encoding='utf-8') as stream:
        for line in stream:
            event = strict_json(line)
            if event.get('seq') != len(events) or event.get('previous') != previous:
                raise ValueError('journal sequence mismatch')
            if digest({k: v for k, v in event.items() if k != 'hash'}) != event.get('hash'):
                raise ValueError('journal hash mismatch')
            events.append(event); previous = event['hash']
    return events


class RecordedFailure(Exception):
    pass


class Replay:
    scientific = False
    def __init__(self, events):
        starts = [e for e in events if e['kind'] == 'call_start']
        outcomes = [e for e in events if e['kind'] in ('call_response', 'provider_failure')]
        terminal = {e['call_id']: e for e in outcomes}
        if (len(terminal) != len(outcomes) or len(terminal) != len(starts) or
            len({e['call_id'] for e in starts}) != len(starts) or any(e['call_id'] not in terminal for e in starts)):
            raise ValueError('incomplete or duplicate call ledger')
        self.rows = [(e, terminal[e['call_id']]) for e in starts]
        self.index = 0; self.calls = 0; self.last_usage = {}; self.last_response_text = None
        self.name = 'saved-response-replay'

    def complete(self, request):
        if self.index >= len(self.rows): raise AssertionError('replay exhausted')
        start, outcome = self.rows[self.index]
        if request != start['request']:
            raise AssertionError('replay request mismatch')
        self.index += 1; self.calls += 1
        self.last_usage = outcome.get('usage', {})
        self.last_response_text = outcome.get('raw_text')
        if outcome['kind'] == 'provider_failure': raise RecordedFailure()
        return copy.deepcopy(outcome['response'])

    def finish(self):
        if self.index != len(self.rows): raise AssertionError('unused saved responses')
