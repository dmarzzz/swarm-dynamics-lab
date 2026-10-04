"""Draft normalized private records. Unknown visibility/redaction prevents actor admission."""
import argparse
import json
import os
from pathlib import Path
from audit_inventory import utc
from replay import REVISION, digest

TABLES = {'chat_messages': ('chat','content'), 'agent_memories': ('memory','content'),
          'computer_use_sessions': ('session_intent','session_goal')}


def normalize(table, row):
    kind, text_key = TABLES[table]
    return {'id': table + ':' + row['id'], 'revision': REVISION, 'kind': kind,
            'created_at': utc(row['created_at']).isoformat(),
            'updated_at': utc(row['updated_at']).isoformat(),
            'available_at': utc(row['created_at']).isoformat(),
            'availability_status':'unreviewed; created_at is only a candidate availability time',
            'visible_to': [], 'redacted': None, 'content': row.get(text_key) or '',
            'source_sha256':digest(row), 'source_digest_scope':'retained allowlisted projection, not original complete row'}

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('private_dir',type=Path);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    try:
        os.umask(0o077)
        count=0
        with args.out.open('x',encoding='utf-8') as output:
            for table in TABLES:
                with (args.private_dir/(table+'.development-prefix.jsonl')).open(encoding='utf-8') as source:
                    for line in source:
                        output.write(json.dumps(normalize(table,json.loads(line)),ensure_ascii=False)+'\n')
                        count+=1
        print(json.dumps({'draft_records':count,'admitted_records':0,'visibility':'requires review'}))
    except Exception:
        raise SystemExit('Normalization refused; raw source diagnostics suppressed.')
