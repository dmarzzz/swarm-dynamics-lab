"""Prospective native adapter for the shared receipt contract, not a second format."""
import json
import os
from pathlib import Path
import sys
from common import REPO,digest,sha
sys.path.insert(0,str(REPO/'scripts'))
from experiment_ops.trace_receipts import KINDS,retain,audit


def snapshot(path,value):
    temp=path.with_suffix('.pending')
    with temp.open('w') as f:json.dump(value,f,indent=2);f.flush();os.fsync(f.fileno())
    os.replace(temp,path)
    fd=os.open(path.parent,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)


class Receipts:
    def __init__(self,out,attempt,cases,source_hash,config):
        self.out=out;self.path=out/'trace-manifest.json'
        assignments=[{'id':f"{c['id']}-{r}",'unit':c['id'],'arm':r} for c in cases for r in ('P','C')]
        self.value={'schema_version':1,'study':'antsy-targeted-v8','attempt':attempt,'source_sha256':source_hash,
                    'config_sha256':digest(config),'assignments':assignments,
                    'calls':[{'assignment':a['id'],'call_id':None,'status':'unstarted','artifacts':{}} for a in assignments]}
        self.config=config
        snapshot(self.path,self.value)
    def store(self,content):
        ref=retain(self.out/'private'/'blobs',content);ref['path']='private/blobs/'+ref['path'];return ref
    def begin(self,index,image,context):
        row=self.value['calls'][index]
        if row['status']!='unstarted':raise ValueError('duplicate_dispatch')
        artifacts={k:{'absent':'not_reached'} for k in KINDS}
        artifacts['input']=self.store(image.read_bytes())
        artifacts['context']=self.store(json.dumps(context,sort_keys=True).encode())
        artifacts['transition']={'absent':'not_applicable'};artifacts['usage']={'absent':'not_applicable'}
        row.update(call_id=f'call-{index+1:03d}',status='started',artifacts=artifacts)
        snapshot(self.path,self.value)
    def terminal(self,index,result,directory):
        row=self.value['calls'][index];row['status']='valid' if result['status']=='valid' else 'failed'
        for kind,name in [('response','output.json'),('phases','phases.jsonl'),('stdout','stdout.bin'),('stderr','stderr.bin')]:
            path=directory/'private'/name
            row['artifacts'][kind]=self.store(path.read_bytes()) if path.is_file() else {'absent':'not_collected'}
        row['artifacts']['grade']=self.store(json.dumps(result,sort_keys=True).encode())
        output=directory/'private/output.json'
        if result['status']=='valid':
            row['artifacts']['parsed']=self.store(json.dumps(json.loads(output.read_text())['candidate'],sort_keys=True).encode())
        effective=directory/'private/effective-context.json'
        if effective.is_file():
            # Keep both parent-declared envelope and actual worker declaration.
            row['artifacts']['context']=self.store(json.dumps({'declared':self.config,'worker':json.loads(effective.read_text())},sort_keys=True).encode())
        else:
            row['artifacts']['context']={'absent':'not_collected'}
        snapshot(self.path,self.value)
    def audit(self):return audit(self.out,'antsy-targeted-v8',self.value['attempt'])
