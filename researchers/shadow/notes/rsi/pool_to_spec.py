#!/usr/bin/env python3
"""Explicitly scoped, local-only pool adapter. Never copies content to public output.

Requires a LOCAL selection array [{row: <pool-record>, receipt: <local-receipt>}]
and a LOCAL approved OpenClaw session. The entire approved subagent task must
occur in a structured USER message in each selected request. This establishes
content-based task scope, not transport/session identity or a live timestamp.
Selections, nonce receipts, source paths and plain content hashes stay local.
"""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import secrets
import sys
import protocol as p

MODELS = {'claude-fable-5-1', 'claude-opus-5-5', 'gpt-6-astra'}

def strings(value):
    if isinstance(value, str): yield value
    elif isinstance(value, list):
        for v in value: yield from strings(v)
    elif isinstance(value, dict):
        for v in value.values(): yield from strings(v)


def approved_task(path):
    for line in Path(path).read_text().splitlines():
        row = p.loads(line); m = row.get('message', {})
        if m.get('role') != 'user': continue
        text = '\n'.join(c.get('text', '') for c in m.get('content', []) if isinstance(c, dict) and c.get('type') == 'text')
        if '[Subagent Task]:' in text:
            task = text.split('[Subagent Task]:', 1)[1].strip()
            if len(task) >= 100: return task
    raise ValueError('no full approved task')


def positive_integer(value):
    return type(value) is int and 0 <= value <= 9007199254740991


def convert(row, task, index, stream_id, previous_hash):
    if not isinstance(row.get('request'), str): raise ValueError('request is not intact JSON text')
    request = p.loads(row['request'])
    matched = any(task in text for m in request.get('messages', []) if isinstance(m, dict) and m.get('role') == 'user' for text in strings(m.get('content')))
    if not matched: raise ValueError('source does not match approved research task')
    if row.get('model') not in MODELS or row.get('provider') != 'anthropic': raise ValueError('unapproved provider/model')
    event_id = 'event-' + secrets.token_hex(12)
    attrs = {'gen_ai.operation.name': 'chat', 'gen_ai.provider.name': 'anthropic', 'gen_ai.request.model': row['model']}
    if type(row.get('stream')) is bool: attrs['gen_ai.request.stream'] = row['stream']
    u = row.get('usage') or {}
    # Anthropic raw input_tokens excludes cache reads/writes. OTel total includes them.
    keys = ('input_tokens', 'cache_read_input_tokens', 'cache_creation_input_tokens')
    if all(positive_integer(u.get(k)) for k in keys): attrs['gen_ai.usage.input_tokens'] = sum(u[k] for k in keys)
    for src, dest in [('output_tokens', 'gen_ai.usage.output_tokens'), ('cache_read_input_tokens', 'gen_ai.usage.cache_read.input_tokens'), ('cache_creation_input_tokens', 'gen_ai.usage.cache_write.input_tokens')]:
        if positive_integer(u.get(src)): attrs[dest] = u[src]
    status = row.get('status')
    if not (type(status) is int and 100 <= status <= 599): status = None
    state = 'unknown' if status is None else 'ok' if 200 <= status < 300 else 'error'
    if state == 'error': attrs['error.type'] = 'rate_limit' if status == 429 else '_OTHER'
    timing = dt.datetime.fromisoformat(row['ts'].replace('Z', '+00:00')).astimezone(dt.timezone.utc).replace(second=0, microsecond=0)
    commitments, local = {}, {'event_id': event_id}
    for slot, key, representation in [('prompt', 'request', 'pool-request-utf8'), ('response', 'response', 'pool-collected-response-utf8')]:
        text = row.get(key)
        if not isinstance(text, str): commitments[slot] = None; continue
        blob = text.encode('utf-8'); nonce = secrets.token_bytes(32)
        commitments[slot] = {'commitment': p.commitment(slot, blob, nonce), 'algorithm': 'sha256-domain-nonce-v1', 'representation': representation,
                             'completeness': 'clipped' if re.search(r'\[clipped \d+\]$', text) else 'stored-snapshot' if slot == 'prompt' else 'unknown', 'tier': 'sealed'}
        local[slot] = {'nonce_hex': nonce.hex(), 'plain_sha256': p.sha(blob)}
    rec = {'schema_version': p.VERSION, 'record_type': 'event', 'event_id': event_id,
        'stream_id': stream_id, 'stream_seq': index, 'trace_id': secrets.token_hex(16), 'span_id': secrets.token_hex(8), 'parent_span_id': None,
        'span_kind': 'CLIENT', 'step_id': None, 'parent_step_id': None, 'links': [], 'event_type': 'span_snapshot',
        'producer_id': 'shadow/pool-adapter', 'agent_id': None, 'owner_id': 'shadow', 'run_id': None, 'task_id': None, 'attempt_id': None,
        'source': {'adapter': 'pool-meter', 'mode': 'historical-import', 'attribution': 'approved-task-text-match', 'identity_quality': 'import-generated'},
        'timing': {'observed_at': timing.isoformat().replace('+00:00', 'Z'), 'precision_ms': 60000,
                   'duration_ms': row.get('latency_ms') if positive_integer(row.get('latency_ms')) else None,
                   'ttfb_ms': row.get('ttfb_ms') if positive_integer(row.get('ttfb_ms')) else None, 'start_time': None, 'end_time': None},
        'otel_semconv_revision': p.REVISION, 'attributes': attrs,
        'transport': {'http_status': status, 'state': state, 'stream_terminal_observed': None}, 'tool_calls': None,
        'cost': {'currency': 'USD', 'estimated_microusd': None, 'billed_microusd': None, 'receipt_hash': None, 'coverage': 'unknown'},
        'outcome': {'state': 'ungraded', 'score': None}, 'content': commitments,
        'disclosure': {'envelope_tier': 'public', 'content_tier': 'sealed', 'policy_id': 'shadow-research-envelope-v1',
                      'hints': ['operation', 'model', 'usage', 'latency', 'transport-status', 'commitments'], 'permitted_builders': ['builder-offline-demo'],
                      'release_state': 'sealed', 'reveal_not_before': None},
        'market': {'eligible': False, 'opportunity_id': None, 'source_rebate_floor_bps': 2000, 'permit_hash': None},
        'integrity': {'record_hash': '0' * 64, 'previous_event_hash': previous_hash, 'signature': None}}
    p.seal_record(rec); p.validate(rec)
    content = {'schema_version': p.VERSION, 'record_type': 'content_public', 'event_id': event_id, 'projection': 'omitted-by-policy',
               'prompt': '[SEALED]', 'response': '[SEALED]', 'tool_arguments': '[OMITTED]', 'tool_results': '[OMITTED]'}
    p.validate(content)
    return rec, content, local


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--selection', required=True); ap.add_argument('--approved-session', required=True)
    ap.add_argument('--private-receipts', required=True); ap.add_argument('--output', required=True)
    a = ap.parse_args()
    private, output = Path(a.private_receipts).resolve(), Path(a.output).resolve()
    repo = Path(__file__).resolve().parents[4]
    if private.is_relative_to(repo) or private.is_relative_to(output): raise ValueError('private receipts must be outside repository and public output')
    task = approved_task(a.approved_session)
    selected = p.loads(Path(a.selection).read_text())
    if not 1 <= len(selected) <= 10: raise ValueError('explicit bounded cohort required')
    records, content, receipts = [], [], []
    prev = None; stream_id = 'import-' + secrets.token_hex(12)
    for i, entry in enumerate(selected):
        record, projection, local = convert(entry['row'], task, i, stream_id, prev)
        prev = record['integrity']['record_hash']
        records.append(record); content.append(projection)
        local['source_receipt'] = entry['receipt']; receipts.append(local)
    private.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
    fd = os.open(private, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as f: json.dump(receipts, f, indent=2)
    output.mkdir(parents=True, exist_ok=True)
    for name, rows in [('pool-events.jsonl', records), ('pool-content-public.jsonl', content)]:
        with (output / name).open('x') as f:
            for row in rows: f.write(p.canonical(row).decode('ascii') + '\n')
    print(json.dumps({'converted': len(records), 'raw_content_exported': False, 'source': 'real-scoped-pool-records', 'live_market_eligible': False}))


if __name__ == '__main__':
    try: main()
    except (ValueError, KeyError, OSError, TypeError):
        print('Conversion refused: invalid scope, source shape, destination or existing files.', file=sys.stderr)
        sys.exit(2)
