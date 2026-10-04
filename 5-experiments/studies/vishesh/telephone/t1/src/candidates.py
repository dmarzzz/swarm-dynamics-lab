"""Index existing private projections. Candidates are joins, never validated episodes."""
import argparse
import hashlib
import json
import os
from pathlib import Path

TABLES=('events','chat_messages','agent_memories','computer_use_sessions')


def build(source, destination):
    os.umask(0o077)
    destination.mkdir(mode=0o700,parents=True,exist_ok=False)
    tables={}
    hashes={}
    for table in TABLES:
        path=source/(table+'.development-prefix.jsonl')
        hashes[table]=hashlib.sha256(path.read_bytes()).hexdigest()
        with path.open(encoding='utf-8') as handle:
            rows=[json.loads(line) for line in handle]
        if len({r['id'] for r in rows})!=len(rows):
            raise ValueError('duplicate source ids')
        tables[table]=rows
    chat={r['id']:r for r in tables['chat_messages']}
    sessions={r['id']:r for r in tables['computer_use_sessions']}
    candidates=[]
    counts={'chat_references':0,'chat_loaded':0,'consolidation_references':0,'consolidation_loaded':0}
    for event in tables['events']:
        data=event.get('data') or {}
        match=None
        if data.get('messageId'):
            counts['chat_references']+=1
            if data['messageId'] in chat:
                counts['chat_loaded']+=1
                match=('chat',chat[data['messageId']])
        elif data.get('actionType')=='CONSOLIDATE' and data.get('computerUseSessionId'):
            counts['consolidation_references']+=1
            if data['computerUseSessionId'] in sessions:
                counts['consolidation_loaded']+=1
                match=('consolidation',sessions[data['computerUseSessionId']])
        if match:
            kind,row=match
            cid=hashlib.sha256((kind+':'+event['id']).encode()).hexdigest()[:20]
            candidates.append({'candidate_id':cid,'kind':kind,'event':event,'linked_row':row,
                'status':'unreviewed_join_only','complete_task':False,'historical_visibility':'unresolved',
                'semantic_gold':None,'split':'development','required_next':['complete task/window and dependent records','source receipt if operational claim','visibility and privacy review','semantic annotation and simple baseline']})
    path=destination/'candidates.json'
    path.write_text(json.dumps(candidates,ensure_ascii=False,indent=2)+'\n')
    summary={'scope':'metadata joins over retained development prefixes; no corpus text in report',
             'input_rows':{k:len(v) for k,v in tables.items()},'source_projection_hashes':hashes,
             'joins':counts,'candidate_join_bundles':len(candidates),'independent_tasks_established':0,
             'validated_cases':0,'model_calls':0,'private_bundle_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('destination',type=Path)
    a=p.parse_args()
    try:print(json.dumps(build(a.source,a.destination),indent=2))
    except Exception:raise SystemExit('Candidate preparation failed; source text and raw diagnostics suppressed.')
