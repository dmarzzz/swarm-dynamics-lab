"""Prospective per-call receipts built from the fsynced authoritative journal."""
import hashlib,json,sys
from pathlib import Path

def write_manifest(root,rows,revision,repo):
    sys.path.insert(0,str(repo/'scripts'))
    from experiment_ops.trace_receipts import retain,KINDS
    root=Path(root).resolve();calls=[];assignments=[]
    def save(value):
        raw=json.dumps(value,sort_keys=True).encode();receipt=retain(root/'receipts',raw)
        # retain returns a path relative to its own directory.
        return dict(path='receipts/'+hashlib.sha256(raw).hexdigest(),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
    for row in rows:
        target=root/str(row['index']).zfill(2);f=target/'trace.jsonl'
        events=[json.loads(l) for l in f.read_text().splitlines()] if f.exists() else []
        for turn in range(10):
            aid=f"case{row['index']}-turn{turn}";assignments.append(dict(id=aid,unit=f"case{row['index']}",arm='n1'))
            cid=f"{row['id']}/{turn}/0";req=next((e for e in events if e.get('kind')=='request_context' and e.get('call')==cid),None)
            if req is None:calls.append(dict(assignment=aid,call_id=None,status='unstarted',artifacts={}));continue
            response=next((e for e in events if e.get('kind')=='model_response' and e.get('call')==cid),None)
            parsed=next((e for e in events if e.get('kind')=='parsed' and e.get('turn')==turn),None)
            transition=next((e for e in events if e.get('kind')=='transition' and e.get('turn')==turn),None)
            grade=next((e for e in events if e.get('kind')=='grade'),None)
            artifacts={k:{'absent':'not_reached'} for k in KINDS}
            artifacts.update(input=save(req),context=save(req),phases=save({'turn':turn,'request_journaled':True,'response_retained':response is not None,'parsed':parsed is not None,'transitioned':transition is not None}),stdout={'absent':'not_applicable'},stderr={'absent':'not_applicable'})
            for kind,value in [('response',response),('parsed',parsed),('transition',transition),('grade',grade),('usage',response.get('usage') if response else None)]:
                if value is not None:artifacts[kind]=save(value)
            status='valid' if response and parsed and transition else 'failed' if grade else 'started'
            calls.append(dict(assignment=aid,call_id=f"iq1-c{row['index']}-t{turn}",status=status,artifacts=artifacts))
    manifest=dict(schema_version=1,study='optimal-swarm-size',attempt='incident-q1',source_sha256=hashlib.sha256(revision.encode()).hexdigest(),config_sha256=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),assignments=assignments,calls=calls)
    temporary=root/'trace-manifest.tmp';temporary.write_text(json.dumps(manifest,indent=2));temporary.replace(root/'trace-manifest.json')
