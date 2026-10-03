"""Deterministic compressed/chunked uploads below the fleet proxy's request limit."""
import gzip
import hashlib
import json
from pathlib import Path

MAX_PART=1_000_000

def prepare_artifacts(out,limit=MAX_PART):
    out=Path(out);upload=out/'upload';upload.mkdir(exist_ok=True)
    parts=[];index={'version':1,'files':[]}
    for name in ('manifest.json','episodes.jsonl','events.jsonl','summary.json'):
        path=out/name
        if not path.exists():continue
        raw=path.read_bytes();compressed=name.endswith('.jsonl') or len(raw)>limit
        payload=gzip.compress(raw,mtime=0) if compressed else raw
        base=name+('.gz' if compressed else '')
        names=[]
        for offset in range(0,max(1,len(payload)),limit):
            chunk=payload[offset:offset+limit]
            part_name=base if len(payload)<=limit else base+f'.part{offset//limit:04d}'
            p=upload/part_name;p.write_bytes(chunk);parts.append(p);names.append(part_name)
        index['files'].append({'original':name,'raw_bytes':len(raw),'raw_sha256':hashlib.sha256(raw).hexdigest(),
                               'encoding':'gzip' if compressed else 'identity','payload_sha256':hashlib.sha256(payload).hexdigest(),
                               'parts':names})
    idx=upload/'artifact-index.json';idx.write_text(json.dumps(index,indent=2));parts.append(idx)
    return parts

def publish_artifacts(run,out):
    for path in prepare_artifacts(out):run.artifact(path,path.name)
