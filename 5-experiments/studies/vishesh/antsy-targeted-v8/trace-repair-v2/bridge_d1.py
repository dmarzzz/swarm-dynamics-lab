"""Retrospective D1 receipt manifest, private retained bytes, no native execution."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[5]/'scripts'))
from experiment_ops.trace_receipts import KINDS, audit, retain

p=argparse.ArgumentParser();p.add_argument('--q0',type=Path,required=True);p.add_argument('--d1',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
a.out.mkdir(mode=0o700,parents=False,exist_ok=False)
def store(content):
    ref=retain(a.out/'private',content);ref['path']='private/'+ref['path'];return ref
native=(a.d1/'manifest.json').read_bytes();config=hashlib.sha256(native).hexdigest()
source=hashlib.sha256(json.loads(native)['source'].encode()).hexdigest()
assignments=[];calls=[]
for seq,i in enumerate((60,61,62,60,61,62),1):
    assignments.append({'id':f'assignment-{seq}','unit':f'receipt-{i}','arm':'checker'})
    row={'assignment':f'assignment-{seq}','call_id':None,'status':'unstarted','artifacts':{}}
    if seq<=3:
        private=a.d1/f'private/calls/{seq:02d}/private'
        result=json.loads((a.d1/f'private/calls/{seq:02d}/result.json').read_text())
        row.update(call_id=f'D1-call-{seq}',status=result['status'])
        art={k:{'absent':'not_applicable'} for k in KINDS}
        art['input']=store((a.q0/f'private/train-{i}.png').read_bytes())
        art['context']={'absent':'legacy_missing'} # no complete effective worker configuration receipt
        art['grade']=store((a.d1/f'private/calls/{seq:02d}/result.json').read_bytes())
        for kind,name in [('response','output.json'),('phases','phases.jsonl'),('stdout','stdout.bin'),('stderr','stderr.bin')]:
            art[kind]=store((private/name).read_bytes())
        data=json.loads((private/'output.json').read_text())
        art['parsed']=store(json.dumps(data['candidate'],sort_keys=True).encode())
        row['artifacts']=art
    calls.append(row)
manifest={'schema_version':1,'study':'antsy-targeted-v8','attempt':'D1-latency-attempt-1',
          'source_sha256':source,'config_sha256':config,'assignments':assignments,'calls':calls}
(a.out/'trace-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
result=audit(a.out,'antsy-targeted-v8','D1-latency-attempt-1')
(a.out/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
