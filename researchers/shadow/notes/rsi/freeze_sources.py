#!/usr/bin/env python3
"""Freeze public historical inputs and typed metadata. No private input support.
Pool envelopes must already have passed the separate owner-local cohort adapter.
"""
import argparse
import gzip
import json
import subprocess
from pathlib import Path
import protocol as p

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CM = 'researchers/shadow/notes/capture-memory-mix/results'
DM = 'researchers/dmarz/notes/compositional-safety/records/q0-011/trace.jsonl.gz'
IMPORT_TIME = '2026-10-04T14:00:00Z'  # Coarse import batch label, not event execution time.


def digest(x):
    return p.sha(p.canonical(x))


def read_rows(path):
    text = gzip.decompress(path.read_bytes()).decode() if path.suffix == '.gz' else path.read_text()
    return [(n, p.loads(line), p.sha(line.encode())) for n, line in enumerate(text.splitlines(), 1) if line.strip()]


def inventory():
    paths = [(x, 'episode') for x in sorted((ROOT / CM / 'pilot-mp3').glob('MP_*.jsonl'))]
    paths += [(x, 'policy-call') for x in sorted((ROOT / CM / 'pilot-mp2').glob('calls-*.jsonl'))]
    paths += [(ROOT / DM, 'public-workflow-step')]
    if len(paths) != 11:
        raise ValueError('expected five MP3 cells, five MP2 call files and one public trace')
    return paths


def source_receipt(path, role):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': p.sha(path.read_bytes()),
            'role': role, 'rows': len(read_rows(path))}


def event(source, line, row, role, seq, previous):
    token = digest({'source': source['sha256'], 'line': line})
    model = None
    if role == 'episode':
        backend = row['backend']
        if backend.startswith('http:'):
            model = backend[5:]
    attrs = {'gen_ai.operation.name': 'chat' if role == 'policy-call' else 'invoke_workflow'}
    if model:
        attrs['gen_ai.request.model'] = model
    e = {'schema_version': p.VERSION, 'record_type': 'event', 'event_id': 'event-r1-' + token[:24],
         'stream_id': 'import-r1-public', 'stream_seq': seq, 'trace_id': token[:32], 'span_id': token[32:48],
         'parent_span_id': None, 'span_kind': 'CLIENT' if role == 'policy-call' else 'INTERNAL',
         'step_id': None, 'parent_step_id': None, 'links': [], 'event_type': 'span_snapshot',
         'producer_id': 'shadow/r1-public-adapter', 'agent_id': None,
         'owner_id': 'dmarz' if role == 'public-workflow-step' else 'shadow',
         'run_id': None, 'task_id': None, 'attempt_id': None,
         'source': {'adapter': 'experiment', 'mode': 'historical-import', 'attribution': 'owner-approved', 'identity_quality': 'import-generated'},
         'timing': {'observed_at': IMPORT_TIME, 'precision_ms': 3600000, 'duration_ms': None, 'ttfb_ms': None, 'start_time': None, 'end_time': None},
         'otel_semconv_revision': p.REVISION, 'attributes': attrs,
         'transport': {'http_status': None, 'state': 'unknown', 'stream_terminal_observed': None},
         'tool_calls': None, 'cost': {'currency': 'USD', 'estimated_microusd': None, 'billed_microusd': None, 'receipt_hash': None, 'coverage': 'unknown'},
         'outcome': {'state': 'ungraded', 'score': None}, 'content': {'prompt': None, 'response': None},
         'disclosure': {'envelope_tier': 'public', 'content_tier': 'sealed', 'policy_id': 'r1-public-metadata-only',
                       'hints': ['operation', 'model', 'task-class'], 'permitted_builders': ['builder-offline-demo'],
                       'release_state': 'owner-authorized-public', 'reveal_not_before': None},
         'market': {'eligible': False, 'opportunity_id': None, 'source_rebate_floor_bps': 2000, 'permit_hash': None},
         'integrity': {'record_hash': '0' * 64, 'previous_event_hash': previous, 'signature': None}}
    return p.seal_record(e)


def project(source, line, row, row_sha, ev, role):
    # Every value is explicitly selected. Never copy a source dict or free text.
    item = {'event_id': ev['event_id'], 'source_path': source['path'], 'source_line': line,
            'source_row_sha256': row_sha, 'role': role}
    if role == 'episode':
        if type(row['validity']['ok']) is not bool:
            raise ValueError('non-boolean validity')
        valid = row['validity']['ok']
        captured = row['evaluation']['captured'] if valid else None
        if valid and type(captured) is not bool:
            raise ValueError('non-boolean capture')
        item.update(cell=Path(source['path']).stem, task=row['task_id'], seed=row['seed'], arm=row['arm'],
                    valid=valid, captured=captured, eval_round=row['cfg']['eval_round'], native_attempt_id_known=row['attempt'] is not None)
        if item['arm'] not in ('A0_no_purge', 'A1_purge', 'A2_purge_wipe'):
            raise ValueError('unknown arm')
        if any(type(item[k]) is not int for k in ('task', 'seed', 'eval_round')):
            raise ValueError('non-integer episode identifier')
    elif role == 'policy-call':
        for key in ('task', 'round', 'n', 'n_orig'):
            if type(row[key]) is not int:
                raise ValueError('non-integer policy hint')
            item[key] = row[key]
        item['memory_kind'] = row['kind'] if row['kind'] in ('short', 'long') else 'unknown'
    else:
        item['step'] = row['step'] if type(row.get('step')) is int else row.get('observation', {}).get('step')
        if type(item['step']) is not int:
            raise ValueError('unknown public workflow step')
        item['actor'] = row['actor'] if type(row['actor']) is int else None
        operation = (row.get('event') or {}).get('operation')
        item['operation'] = operation if operation in ('read', 'message', 'wait', 'inspect', 'package', 'export', 'authorize', 'fulfill', 'buy') else 'other'
        item['episode_alias'] = 'public-episode-' + p.sha(row['episode_id'].encode())[:16]
    p.canonical(item)
    return item


def build(manifest):
    events, projections = [], []
    previous = None
    for source in manifest['sources']:
        path = ROOT / source['path']
        if p.sha(path.read_bytes()) != source['sha256']:
            raise ValueError('frozen source changed: ' + source['path'])
        rows = read_rows(path)
        if len(rows) != source['rows']:
            raise ValueError('source row count changed')
        if source['role'] == 'policy-call':
            rows = rows[:16]
        for line, row, row_sha in rows:
            ev = event(source, line, row, source['role'], len(events), previous)
            previous = ev['integrity']['record_hash']
            events.append(ev)
            projections.append(project(source, line, row, row_sha, ev, source['role']))
    return events, projections


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def freeze(output):
    output.mkdir(exist_ok=True)
    if (output / 'manifest.json').exists():
        raise ValueError('frozen input already exists; do not replace historical inputs')
    pool = output / 'pool-events.jsonl'
    if not pool.is_file():
        raise ValueError('scope-verified pool envelopes required')
    pool_events = [p.loads(x) for x in pool.read_text().splitlines()]
    for ev in pool_events:
        p.validate(ev)
    manifest = {'version': 'r1-input/1', 'source_revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                'plan_sha256': p.sha((HERE / 'REPLAY-PLAN-v2.md').read_bytes()),
                'sources': [source_receipt(path, role) for path, role in inventory()],
                'policy_call_sampling': 'first-16-records-per-file-not-random',
                'pool': {'path': 'pool-events.jsonl', 'sha256': p.sha(pool.read_bytes()), 'rows': len(pool_events),
                         'scope': 'full-approved-capture-memory-task-in-structured-user-message', 'game_call_join': 'unavailable'},
                'time_semantics': 'coarse-import-batch-not-source-execution', 'private_raw_exported': False}
    events, projections = build(manifest)
    for ev in events:
        p.validate(ev)
    text = ''.join(p.canonical(e).decode() + '\n' for e in events)
    (output / 'public-events.jsonl').write_text(text)
    write_json(output / 'projections.json', projections)
    manifest['derived'] = {name: p.sha((output / name).read_bytes()) for name in ('public-events.jsonl', 'projections.json')}
    write_json(output / 'manifest.json', manifest)
    print(json.dumps({'public_events': len(events), 'pool_events': len(pool_events), 'projections': len(projections), 'raw_pool_exported': False}))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, default=HERE / 'r1-input')
    freeze(ap.parse_args().output)
