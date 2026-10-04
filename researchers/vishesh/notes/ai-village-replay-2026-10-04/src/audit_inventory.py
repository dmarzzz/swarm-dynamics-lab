"""Aggregate structural coverage of private prefixes; no behavioral labels or text output."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


def utc(value):
    # SCHEMA.md: PostgreSQL timezone-free export timestamps are UTC.
    d = datetime.fromisoformat(value.replace('Z', '+00:00'))
    return d.replace(tzinfo=timezone.utc) if d.tzinfo is None else d.astimezone(timezone.utc)


def audit(directory):
    tables = {name:[json.loads(line) for line in (directory/(name+'.development-prefix.jsonl')).open(encoding='utf-8')]
              for name in ('events','chat_messages','agent_memories','computer_use_sessions')}
    chats = {r['id'] for r in tables['chat_messages']}
    sessions = {r['id'] for r in tables['computer_use_sessions']}
    links = [r['data']['messageId'] for r in tables['events'] if r.get('data',{}).get('messageId')]
    consolidations = [r for r in tables['events'] if r.get('data',{}).get('actionType') == 'CONSOLIDATE']
    session_links = [r['data']['computerUseSessionId'] for r in consolidations if r['data'].get('computerUseSessionId')]
    result = {'scope':'structural audit of convenience development prefixes; absent joins mean NOT LOADED, not missing in source',
              'chat_event_links':len(links),'chat_event_links_loaded':sum(x in chats for x in links),
              'consolidation_events':len(consolidations),'consolidation_session_links':len(session_links),
              'consolidation_sessions_loaded':sum(x in sessions for x in session_links),
              'tables':{},'validated_episodes':0,'model_calls':0}
    for name,rows in tables.items():
        dates=[utc(r['created_at']) for r in rows]
        result['tables'][name]={'rows':len(rows),'duplicate_ids':len(rows)-len({r['id'] for r in rows}),
          'backward_timestamp_steps':sum(b<a for a,b in zip(dates,dates[1:])),
          'rows_modified_after_creation':sum(utc(r['updated_at'])>utc(r['created_at']) for r in rows if r.get('updated_at')),
          'prefix_projection_sha256':hashlib.sha256((directory/(name+'.development-prefix.jsonl')).read_bytes()).hexdigest()}
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('private_dir',type=Path)
    a=p.parse_args()
    try: print(json.dumps(audit(a.private_dir),indent=2))
    except Exception: raise SystemExit('Audit failed; raw source diagnostics suppressed.')
