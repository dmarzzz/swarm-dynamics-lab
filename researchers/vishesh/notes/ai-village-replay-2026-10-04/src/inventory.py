"""Bounded private source inventory. Never prints corpus text or exception bodies."""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import urllib.request
import zlib

REVISION = '838b4150303ca8228e8edb432d8b8ccae353d258'
TABLES = ('chat_messages', 'events', 'agent_memories', 'computer_use_sessions')
FIELDS = {
    'chat_messages': ('id', 'created_at', 'updated_at', 'agent_speaker_id', 'speaker_type', 'room_id', 'content'),
    'agent_memories': ('id', 'created_at', 'updated_at', 'agent_id', 'content'),
    'computer_use_sessions': ('id', 'created_at', 'updated_at', 'agent_id', 'session_goal'),
    'events': ('id', 'created_at', 'updated_at', 'event_index'),
}

class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        from urllib.parse import urlparse
        if urlparse(newurl).scheme != 'https':
            raise ValueError('non-TLS redirect')
        out = super().redirect_request(req, fp, code, msg, headers, newurl)
        if urlparse(req.full_url).netloc != urlparse(newurl).netloc:
            out.remove_header('Authorization')
        return out

def project(table, row):
    out = {k: row.get(k) for k in FIELDS[table]}
    if table == 'events':
        data = row.get('data') or {}
        out['data'] = {k: data[k] for k in ('actionType', 'agentId', 'speakerId', 'roomId', 'messageId', 'computerUseSessionId') if k in data}
    return out

def collect(table, token, destination, limit=2000):
    url = f'https://huggingface.co/datasets/aidigestorg/ai-village/resolve/{REVISION}/{table}.jsonl.gz'
    request = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + token})
    opener = urllib.request.build_opener(SafeRedirect())
    count, compressed, decoded = 0, 0, 0
    timestamps, agents, types = [], set(), collections.Counter()
    h = hashlib.sha256()
    buffer = b''
    dec = zlib.decompressobj(16 + zlib.MAX_WBITS)
    # Parent and file are private; projected text is NEVER returned to stdout.
    path = destination / (table + '.development-prefix.jsonl')
    with opener.open(request, timeout=45) as response, path.open('x', encoding='utf-8') as f:
        os.chmod(path, 0o600)
        while count < limit:
            chunk = response.read(65536)
            if not chunk:
                break
            compressed += len(chunk)
            if compressed > 32 * 1024 * 1024:
                break
            expanded = dec.decompress(chunk, 128 * 1024 * 1024 - decoded + 1)
            decoded += len(expanded)
            if decoded > 128 * 1024 * 1024:
                raise ValueError('decoded cap')
            buffer += expanded
            while b'\n' in buffer and count < limit:
                line, buffer = buffer.split(b'\n', 1)
                row = json.loads(line)
                h.update(line + b'\n')
                projected = project(table, row)
                f.write(json.dumps(projected, ensure_ascii=False) + '\n')
                count += 1
                if row.get('created_at'):
                    timestamps.append(row['created_at'])
                agent = row.get('agent_id') or row.get('agent_speaker_id')
                if agent:
                    agents.add(agent)
                if table == 'events':
                    # Only documented action types, no arbitrary source values in public report.
                    action = (row.get('data') or {}).get('actionType')
                    types[action if action in {'AGENT_TALK','USER_TALK','CONSOLIDATE','START_USING_COMPUTER','STOP_USING_COMPUTER','WAIT','PAUSE','SEARCH_HISTORY','ENTER_ROOM'} else 'OTHER'] += 1
    return {'rows': count, 'compressed_bytes_read': compressed, 'decoded_bytes_read': decoded,
            'consumed_line_prefix_sha256': h.hexdigest(), 'unique_agent_ids': len(agents),
            'earliest_created_at': min(timestamps, default=None), 'latest_created_at': max(timestamps, default=None),
            'action_type_counts': dict(types), 'complete_table': bool(dec.eof and count < limit)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--token-file', type=Path, required=True)
    parser.add_argument('--private-dir', type=Path, required=True)
    args = parser.parse_args()
    os.umask(0o077)
    args.private_dir.mkdir(mode=0o700, parents=True, exist_ok=False)
    summary = {'revision': REVISION, 'scope': 'first 2000 file-order rows per table; convenience development inventory, not a sample of independent tasks', 'tables': {}, 'model_calls': 0, 'evaluated_episodes': 0}
    try:
        token = args.token_file.read_text().strip()
        for table in TABLES:
            try:
                summary['tables'][table] = collect(table, token, args.private_dir)
            except Exception:
                summary['tables'][table] = {'status': 'failed; raw diagnostic suppressed'}
        (args.private_dir / 'inventory-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
        print(json.dumps(summary, indent=2))
    except Exception:
        print('Inventory failed; source text and authentication diagnostics suppressed.')
        raise SystemExit(1)

if __name__ == '__main__':
    main()
