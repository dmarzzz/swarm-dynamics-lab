#!/usr/bin/env python3
"""R2 operational wrapper. Frozen requests and behavioral scoring are imported unchanged."""
import argparse
from datetime import datetime, timezone
import fcntl
import json
import math
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.request
import reading_rule as r

ROOT = r.ROOT
RESULTS = ROOT / 'results-r2'
CAP = 8.0
MAX_CALLS = 157
FROZEN_INPUT = 'c9d24c92ff32abbdd3c961bb4446f07edf60ba9aff330417b5436b4cc71f2639'
HISTORICAL_JOURNAL = '78f7f3c1be4beed6fba65428ae1003ef006664e0db7f7f2d8c134619378b67ae'


def read_journal():
    return r.read_journal(RESULTS / 'journal.jsonl')


def historical():
    path = ROOT / 'results/journal.jsonl'
    assert r.digest(path.read_bytes()) == HISTORICAL_JOURNAL
    rows = r.read_journal(path)
    assert len([x for x in rows if x['event'] == 'start']) == 1
    return [dict(x, id='v1/' + x['id']) for x in rows]


def score(response):
    s = r.score(response)
    if s['valid'] and not isinstance(response.get('provider'), str):
        return {'valid': False, 'reason': 'missing_provider_identity'}
    if s['valid'] and not response['provider'].strip():
        return {'valid': False, 'reason': 'missing_provider_identity'}
    return s


def qualify(data, rows):
    hs = {h['id']: h for h in data['histories']}
    terminal = {x['id']: x for x in rows if x['event'] == 'terminal'}
    assignments = [a for a in data['assignments'] if a['stage'] == 'S0']
    valid = correct = 0
    for a in assignments:
        s = score(terminal.get(a['id'], {}).get('response', {}))
        valid += s['valid']
        correct += s['valid'] and s['choice'] == hs[a['history']]['majority']
    return {'assigned': len(assignments), 'valid': valid, 'correct': correct,
            'pass': len(assignments) == 12 and valid == 12 and correct >= 11}


def admission(rows, assignment, timestamp=None):
    assert not any(x.get('halt') for x in rows), 'durable stop latch'
    r.admission(rows, assignment, timestamp)
    starts = [x for x in historical() + rows if x['event'] == 'start']
    assert len(starts) < MAX_CALLS, 'cumulative call cap'
    assert sum(x['reservation_usd'] for x in starts) + r.RESERVE <= CAP + 1e-9, 'cumulative USD8 cap'


def preflight(revision, stage):
    assert len(revision) == 40 and all(x in '0123456789abcdef' for x in revision)
    files = ['PLAN.md', 'AMENDMENT-R2.md', 'input.json', 'reading_rule.py', 'successor_run.py', 'test_successor.py']
    if stage == 'S1':
        files += ['S1-R2-PRE.md']
    hashes = {}
    for name in files:
        path = ROOT / name
        relative = str(path.relative_to(r.REPO))
        committed = subprocess.check_output(['git', 'show', f'{revision}:{relative}'], cwd=r.REPO)
        assert committed == path.read_bytes(), 'uncommitted drift: ' + name
        hashes[name] = r.digest(committed)
    assert hashes['input.json'] == FROZEN_INPUT
    data = json.loads((ROOT / 'input.json').read_text())
    assert data == r.build_input()
    public_receipts = []
    for name in ['PLAN.md', 'AMENDMENT-R2.md']:
        relative = str((ROOT / name).relative_to(r.REPO))
        url = f'https://raw.githubusercontent.com/dmarzzz/swarm-lab/{revision}/{relative}'
        with urllib.request.urlopen(url, timeout=30) as response:
            public = response.read(100000)
        assert public == (ROOT / name).read_bytes(), 'public document mismatch'
        public_receipts.append({'url': url, 'sha256': r.digest(public)})
    rows = read_journal()
    assert not any(x.get('halt') for x in rows), 'durable stop latch'
    q = qualify(data, rows)
    if stage == 'S1':
        assert q['pass'], 'S0 did not qualify'
        receipts = [json.loads(p.read_text()) for p in RESULTS.glob('admission-S0-*.json')]
        assert receipts, 'missing S0 admission'
        for name in ['PLAN.md', 'AMENDMENT-R2.md', 'input.json', 'reading_rule.py', 'successor_run.py']:
            assert all(x['hashes'][name] == hashes[name] for x in receipts), 'qualified source drift'
    import swarm_report as sr
    sr.register('capture-memory-reading-rule', title='Frozen-history reading-rule diagnostic (exploratory R2)',
                description='Unchanged 24 synthetic histories, six lossless presentations. Fresh access-restored qualification; cumulative USD8 including v1. Plan: ' + url,
                owner='shadow', url=url,
                params={'stage': {'type': 'str', 'description': 'R2 S0 or qualified S1', 'role': 'stage'}},
                metrics=['assigned', 'valid', 'primary_effect', 'cost_usd'], primary_metric='primary_effect')
    receipt = {'stage': stage, 'attempt': 'R2', 'revision': revision, 'time': r.now(), 'public_documents': public_receipts,
               'hashes': hashes, 'cap_usd': CAP, 'reserve_usd': r.RESERVE, 'historical_reserved_usd': .05,
               'historical_journal_sha256': HISTORICAL_JOURNAL, 'qualification': q, 'hub_registered': True,
               'model': r.MODEL, 'endpoint': r.ENDPOINT, 'python': sys.version,
               'assessment': 'diagnostic-only; same-author; AMENDMENT-R2.md'}
    r.dump(RESULTS / f'admission-{stage}-{datetime.now(timezone.utc).strftime("%H%M%S%f")}.json', receipt)
    return data


def run(stage, revision):
    RESULTS.mkdir(exist_ok=True)
    # Same lock as v1: neither entry point may dispatch concurrently.
    with (ROOT / 'results/.run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        data = preflight(revision, stage)
        key = (Path.home() / '.moltbot/secrets/openrouter.key').read_text().strip()
        assert key
        rows = read_journal()
        started = {x['id'] for x in rows if x['event'] == 'start'}
        consecutive_errors = 0
        with (RESULTS / 'journal.jsonl').open('a') as log:
            for a in data['assignments']:
                if a['stage'] != stage or a['id'] in started:
                    continue
                admission(rows, a)
                start = {'event': 'start', 'attempt': 'R2', 'id': a['id'], 'stage': stage,
                         'request_sha256': a['request_sha256'], 'reservation_usd': r.RESERVE, 'revision': revision}
                r.append(log, start)
                rows.append(start)
                started.add(a['id'])
                req = urllib.request.Request(r.ENDPOINT, data=json.dumps(a['body']).encode(), headers={
                    'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json', 'X-Title': 'swarm-lab-reading-rule'})
                event = {'event': 'terminal', 'attempt': 'R2', 'id': a['id'], 'stage': stage}
                try:
                    with urllib.request.urlopen(req, timeout=45) as response:
                        body = json.loads(response.read(200000))
                    s = score(body)
                    event.update(response=body, score=s)
                    consecutive_errors = 0
                    cost = (body.get('usage') or {}).get('cost')
                    if cost is not None and (not math.isfinite(float(cost)) or not 0 <= float(cost) <= r.RESERVE):
                        event['halt'] = 'cost_outside_reservation'
                    if s.get('reason') in ('model_mismatch', 'missing_provider_identity'):
                        event['halt'] = s['reason']
                except urllib.error.HTTPError as error:
                    event.update(error='http_error', http_status=error.code)
                    consecutive_errors += 1
                    if error.code in (400, 401, 402, 403, 429):
                        event['halt'] = 'http_' + str(error.code)
                    if error.code == 429:
                        event['retry_after'] = error.headers.get('Retry-After')
                except Exception as error:
                    event['error'] = type(error).__name__
                    consecutive_errors += 1
                if consecutive_errors >= 3:
                    event['halt'] = 'three_consecutive_transport_failures'
                r.append(log, event)
                rows.append(event)
                print(a['id'], event.get('score', {}).get('valid', False), event.get('halt', ''), flush=True)
                if event.get('halt'):
                    break
        print(json.dumps({'stage': stage, 'qualification': qualify(data, rows), 'r2_started': len(started),
                          'all_attempts_started': len(started) + 1, 'retained_reservations_usd': round((len(started) + 1) * r.RESERVE, 2)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['S0', 'S1'])
    parser.add_argument('--revision', required=True)
    args = parser.parse_args()
    run(args.stage, args.revision)
