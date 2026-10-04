#!/usr/bin/env python3
"""Single-author exploratory diagnostic. Only `run` performs model calls."""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import random
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
MODEL = 'openai/gpt-4o-mini'
ENDPOINT = 'https://openrouter.ai/api/v1/chat/completions'
CAP = 12.0
RESERVE = .05
MAX_CALLS = 156
DEADLINE = '2026-10-04T21:25:00+00:00'
NAMES = ('Cedar', 'Raven')
CONDITIONS = [(r, o) for r in ('raw', 'summary') for o in ('chronological', 'reversed', 'shuffled')]
SYSTEM = ('You are one of several agents playing a coordination game. In each round you are paired with another agent and '
          'you both say a name; you score a point when you say the same name as your partner. You will be shown the names '
          'your recent partners said. Reply with exactly one of the two allowed names and nothing else. '
          'Event indices encode chronology: larger indices are more recent. Display order may vary.')


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    if not isinstance(data, bytes):
        data = json.dumps(data, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(data).hexdigest()


def dump(path, obj):
    data = json.dumps(obj, indent=2, sort_keys=True) + '\n'
    with path.open('x') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def histories():
    out = []
    for i, name in enumerate(NAMES):
        out.append(dict(id=f'Q{i}', stage='S0', events=[name] * 16, majority=name, conflict=False))
    i = 0
    for n in (16, 64, 256):
        for name in NAMES:
            other = next(x for x in NAMES if x != name)
            for conflict in (False, True):
                for replicate in (0, 1):
                    last = other if conflict else name
                    events = [name] * (n * 5 // 8 - int(last == name)) + [other] * (n * 3 // 8 - int(last == other))
                    random.Random(913000 + i).shuffle(events)
                    events.append(last)
                    out.append(dict(id=f'H{i:02d}', stage='S1', events=events, majority=name,
                                    conflict=conflict, replicate=replicate))
                    i += 1
    return out


def representation(h, rep, order):
    events = list(enumerate(h['events'], 1))
    if order == 'reversed':
        events.reverse()
    elif order == 'shuffled':
        random.Random('display-' + h['id']).shuffle(events)
    payload = {'last_event': {'index': len(h['events']), 'name': h['events'][-1]}}
    if rep == 'raw':
        payload['events'] = [{'index': i, 'name': name} for i, name in events]
    else:
        groups = {}
        for i, name in events:
            groups.setdefault(name, []).append(i)
        payload['counts_and_positions'] = [{'name': name, 'count': len(indices), 'event_indices': indices} for name, indices in groups.items()]
    return payload


def reconstruct(payload):
    if 'events' in payload:
        pairs = [(x['index'], x['name']) for x in payload['events']]
    else:
        pairs = [(i, x['name']) for x in payload['counts_and_positions'] for i in x['event_indices']]
    assert len({i for i, _ in pairs}) == len(pairs)
    assert sorted(i for i, _ in pairs) == list(range(1, len(pairs) + 1))
    seq = [name for _, name in sorted(pairs)]
    assert payload['last_event'] == {'index': len(seq), 'name': seq[-1]}
    return seq


def body(h, rep, order):
    payload = representation(h, rep, order)
    # Identical neutral wording, allowed-name order and chronology key in every condition.
    user = ('Allowed names: Cedar, Raven.\nPartner-name history (indices encode chronology):\n'
            + json.dumps(payload, separators=(',', ':')) + '\nWhich name do you say now?')
    return {'model': MODEL, 'temperature': 0, 'max_tokens': 8, 'logprobs': True, 'top_logprobs': 20,
            'usage': {'include': True},
            'provider': {'require_parameters': True, 'max_price': {'prompt': 1, 'completion': 2}},
            'messages': [{'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': user}]}


def build_input():
    hs = histories()
    assignments = []
    for h in hs:
        for rep, order in CONDITIONS:
            b = body(h, rep, order)
            assignments.append({'id': f'{h["id"]}-{rep}-{order}', 'history': h['id'], 'stage': h['stage'],
                                'representation': rep, 'order': order, 'body': b, 'request_sha256': digest(b)})
    random.Random(20261004).shuffle(assignments)
    return {'model': MODEL, 'histories': hs, 'assignments': assignments, 'plan_sha256': digest((ROOT / 'PLAN.md').read_bytes())}


def freeze():
    payload = build_input()
    p = ROOT / 'input.json'
    if p.exists():
        assert json.loads(p.read_text()) == payload, 'frozen input differs; refuse overwrite'
    else:
        dump(p, payload)
    print('frozen', len(payload['histories']), 'histories;', len(payload['assignments']), 'assignments;', digest(p.read_bytes()))


def score(response):
    try:
        model = response['model']
        if model not in (MODEL, 'openai/gpt-4o-mini-2024-07-18', 'gpt-4o-mini', 'gpt-4o-mini-2024-07-18'):
            return {'valid': False, 'reason': 'model_mismatch'}
        ch = response['choices'][0]
        choice = ch['message']['content'].strip()
        if choice not in NAMES:
            return {'valid': False, 'reason': 'unparseable_choice'}
        tokens = ch['logprobs']['content'][0]['top_logprobs']
        mass = dict.fromkeys(NAMES, 0.0)
        for token in tokens:
            text = token['token'].strip().lower()
            if not text:
                continue
            for name in NAMES:
                if name.lower().startswith(text):
                    mass[name] += math.exp(float(token['logprob']))
        total = sum(mass.values())
        if not .8 <= total <= 1.00001:
            return {'valid': False, 'reason': 'low_or_invalid_allowed_mass', 'mass': total}
        return {'valid': True, 'choice': choice, 'mass': total, 'p': {k: v / total for k, v in mass.items()}}
    except (KeyError, IndexError, TypeError, ValueError, OverflowError):
        return {'valid': False, 'reason': 'missing_or_invalid_response_contract'}


def read_journal(path=None):
    p = path or ROOT / 'results' / 'journal.jsonl'
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []


def append(f, event):
    f.write(json.dumps({'time': now(), **event}, sort_keys=True) + '\n')
    f.flush()
    os.fsync(f.fileno())


def admission(journal, a, timestamp=None):
    starts = [r for r in journal if r['event'] == 'start']
    assert a['id'] not in {r['id'] for r in starts}, 'assignment already started'
    assert len(starts) < MAX_CALLS, 'call cap'
    assert sum(r['reservation_usd'] for r in starts) + RESERVE <= CAP + 1e-9, 'dollar cap'
    assert (timestamp or now()) < DEADLINE, 'deadline'
    b = a['body']
    assert b['model'] == MODEL and b['max_tokens'] == 8
    assert b['provider']['max_price'] == {'prompt': 1, 'completion': 2}
    assert len(json.dumps(b).encode()) <= 20000, 'request too large'
    assert digest(b) == a['request_sha256'], 'request hash mismatch'


def qualify(data, rows):
    hs = {h['id']: h for h in data['histories']}
    terminal = {r['id']: r for r in rows if r['event'] == 'terminal'}
    assignments = [a for a in data['assignments'] if a['stage'] == 'S0']
    valid = correct = 0
    for a in assignments:
        r = terminal.get(a['id'], {})
        s = score(r.get('response', {}))
        valid += s['valid']
        correct += s['valid'] and s['choice'] == hs[a['history']]['majority']
    return {'assigned': len(assignments), 'valid': valid, 'correct': correct,
            'pass': len(assignments) == 12 and valid == 12 and correct >= 11}


def preflight(revision, stage):
    assert len(revision) == 40 and all(x in '0123456789abcdef' for x in revision), 'full commit required'
    files = ('PLAN.md', 'input.json', 'reading_rule.py')
    for name in files:
        relative = str((ROOT / name).relative_to(REPO))
        committed = subprocess.check_output(['git', 'show', f'{revision}:{relative}'], cwd=REPO)
        assert committed == (ROOT / name).read_bytes(), f'uncommitted drift: {name}'
    relative = str((ROOT / 'PLAN.md').relative_to(REPO))
    url = f'https://raw.githubusercontent.com/dmarzzz/swarm-lab/{revision}/{relative}'
    with urllib.request.urlopen(url, timeout=30) as response:
        public = response.read(100000)
    assert public == (ROOT / 'PLAN.md').read_bytes(), 'public plan mismatch'
    data = json.loads((ROOT / 'input.json').read_text())
    assert data == build_input(), 'frozen instrument mismatch'
    receipt = {'stage': stage, 'revision': revision, 'public_plan_url': url, 'public_plan_sha256': digest(public),
               'source_sha256': digest((ROOT / 'reading_rule.py').read_bytes()), 'input_sha256': digest((ROOT / 'input.json').read_bytes()),
               'time': now(), 'model': MODEL, 'endpoint': ENDPOINT, 'cap_usd': CAP, 'python': sys.version,
               'assessment': 'diagnostic-only; same-author, scoped to PLAN.md', 'qualification': qualify(data, read_journal())}
    if stage == 'S1':
        assert receipt['qualification']['pass'], 'S0 did not qualify'
        assert (ROOT / 'S1-PRE.md').exists(), 'missing S1 stage assessment'
    # Hub registration is required before paid dispatch, including the exact immutable plan URL.
    import swarm_report as sr
    sr.register('capture-memory-reading-rule', title='Frozen-history reading-rule diagnostic (exploratory)',
                description='Same 24 indexed histories across raw/lossless summary and chronological/reversed/shuffled displays. '
                            'gpt-4o-mini via OpenRouter; history-level effects; no swarm recovery inference. Plan: ' + url,
                owner='shadow', url=url,
                params={'stage': {'type': 'str', 'description': 'S0 qualification or S1 frozen history diagnostic', 'role': 'stage'}},
                metrics=['assigned', 'valid', 'primary_effect', 'cost_usd'], primary_metric='primary_effect')
    receipt['hub_registered'] = True
    dump(ROOT / 'results' / f'admission-{stage}-{datetime.now(timezone.utc).strftime("%H%M%S%f")}.json', receipt)
    return data, receipt


def run(stage, revision):
    results = ROOT / 'results'
    results.mkdir(exist_ok=True)
    with (results / '.run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        data, receipt = preflight(revision, stage)
        key = (Path.home() / '.moltbot/secrets/openrouter.key').read_text().strip()
        assert key, 'missing credential'
        journal = read_journal()
        starts = {r['id'] for r in journal if r['event'] == 'start'}
        consecutive_errors = 0
        with (results / 'journal.jsonl').open('a') as log:
            for a in data['assignments']:
                if a['stage'] != stage or a['id'] in starts:
                    continue
                admission(journal, a)
                start = {'event': 'start', 'id': a['id'], 'stage': stage, 'request_sha256': a['request_sha256'],
                         'reservation_usd': RESERVE, 'revision': revision}
                append(log, start)
                journal.append(start)
                starts.add(a['id'])
                req = urllib.request.Request(ENDPOINT, data=json.dumps(a['body']).encode(), headers={
                    'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json', 'X-Title': 'swarm-lab-reading-rule'})
                event = {'event': 'terminal', 'id': a['id'], 'stage': stage}
                stop = False
                try:
                    with urllib.request.urlopen(req, timeout=45) as resp:
                        response = json.loads(resp.read(200000))
                    s = score(response)
                    event.update(response=response, score=s)
                    consecutive_errors = 0
                    cost = (response.get('usage') or {}).get('cost')
                    if cost is not None:
                        if not math.isfinite(float(cost)) or not 0 <= float(cost) <= RESERVE:
                            stop = True
                            event['budget_alert'] = 'cost_outside_reservation'
                    stop |= s.get('reason') == 'model_mismatch'
                except urllib.error.HTTPError as error:
                    event.update(error='http_error', http_status=error.code)
                    stop = error.code in (401, 402, 403, 429)
                    consecutive_errors += 1
                except Exception as error:
                    event.update(error=type(error).__name__)
                    consecutive_errors += 1
                append(log, event)
                journal.append(event)
                print(a['id'], event.get('score', {}).get('valid', False), flush=True)
                if stop or consecutive_errors >= 3:
                    break
        print(json.dumps({'stage': stage, 'qualification': qualify(data, journal), 'started_total': len(starts),
                          'retained_reservations_usd': round(len(starts) * RESERVE, 2)}))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('command', choices=('freeze', 'run'))
    ap.add_argument('stage', nargs='?', choices=('S0', 'S1'))
    ap.add_argument('--revision')
    args = ap.parse_args()
    if args.command == 'freeze':
        freeze()
    else:
        assert args.stage and args.revision
        run(args.stage, args.revision)

if __name__ == '__main__':
    main()
