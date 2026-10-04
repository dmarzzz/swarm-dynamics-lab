"""Per-physical-call prospective receipts; original fsynced journals stay authoritative."""
import hashlib,json,sys
from pathlib import Path


def write_manifest(root,rows,revision,repo,attempt='causal-v3'):
    sys.path.insert(0,str(repo/'scripts'));from experiment_ops.trace_receipts import retain,KINDS
    root=Path(root).resolve();calls=[];assignments=[]
    def save(value):
        raw=json.dumps(value,sort_keys=True).encode();retain(root/'receipts',raw)
        return {'path':'receipts/'+hashlib.sha256(raw).hexdigest(),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
    for row in rows:
        f=root/f"{row['index']:02d}"/'trace.jsonl';events=[json.loads(x) for x in f.read_text().splitlines()] if f.exists() else []
        for turn in range(row['round_limit']):
            for actor in range(row['n']):
                aid=f"case{row['index']}-turn{turn}-actor{actor}";assignments.append({'id':aid,'unit':row['root'],'arm':f"n{row['n']}"})
                cid=f"{row['id']}/{turn}/{actor}";req=next((e for e in events if e.get('kind')=='request_context' and e.get('call')==cid),None)
                if req is None:calls.append({'assignment':aid,'call_id':None,'status':'unstarted','artifacts':{}});continue
                response=next((e for e in events if e.get('kind')=='model_response' and e.get('call')==cid),None)
                parsed=next((e for e in events if e.get('kind')=='parsed' and e.get('turn')==turn and e.get('actor')==actor),None)
                transition=next((e for e in events if e.get('kind')=='transition' and e.get('turn')==turn),None)
                grade=next((e for e in events if e.get('kind')=='grade'),None)
                artifacts={k:{'absent':'not_reached'} for k in KINDS}
                artifacts.update(input=save(req),context=save(req),phases=save({'request_journaled':True,'reply':response is not None,'parsed':parsed is not None,'transition':transition is not None,'turn':turn,'actor':actor}),stdout={'absent':'not_applicable'},stderr={'absent':'not_applicable'})
                for k,v in [('response',response),('parsed',parsed),('transition',transition),('grade',grade),('usage',response.get('usage') if response else None)]:
                    if v is not None:artifacts[k]=save(v)
                calls.append({'assignment':aid,'call_id':f'v3-{aid}','status':'valid' if response and parsed and transition else 'failed' if grade else 'started','artifacts':artifacts})
    manifest={'schema_version':1,'study':'optimal-swarm-size','attempt':attempt,'source_sha256':hashlib.sha256(revision.encode()).hexdigest(),'config_sha256':hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),'assignments':assignments,'calls':calls}
    p=root/'trace-manifest.tmp';p.write_text(json.dumps(manifest,indent=2));p.replace(root/'trace-manifest.json')
