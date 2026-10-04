"""Package synthetic experimental records with hashes; preserve originals."""
import gzip,hashlib,json,re,shutil
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
SAFE=('manifest.json','public-plan-receipt.json','summary.json','episodes.jsonl','events.jsonl','comparison.json','diagnosis.json','citation-diagnosis.json','decision-diagnosis.json','visual-validation.json','image-validation.json','publication.json','image-publication.json','runtime-samples.jsonl','reconciliation.json','replay.html','final.svg','final.png','replay.gif')
def package():
 out=BASE/'evidence';out.mkdir(exist_ok=True);index=[]
 for stage in ('Q0','Q1','D0','Q2','S1'):
  src=BASE/'results'/stage
  if not (src/'summary.json').exists():continue
  dst=out/stage;dst.mkdir(exist_ok=True)
  for name in SAFE:
   p=src/name
   if not p.exists():continue
   data=p.read_bytes()
   if p.suffix not in ('.png','.gif'):
    if re.search(rb'\bsk-[A-Za-z0-9_-]{20,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----|Bearer [A-Za-z0-9._-]{20,}',data):raise ValueError('secret_pattern_blocked')
   if name=='events.jsonl':
    dest=dst/(name+'.gz');dest.write_bytes(gzip.compress(data,mtime=0))
   else:dest=dst/name;dest.write_bytes(data)
   index.append({'stage':stage,'path':str(dest.relative_to(BASE)),'source_bytes':len(data),'source_sha256':hashlib.sha256(data).hexdigest(),'stored_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'encoding':'gzip' if name=='events.jsonl' else 'identity'})
 (out/'index.json').write_text(json.dumps(index,indent=2)+'\n')
 print(json.dumps({'files':len(index),'stages':sorted({x['stage'] for x in index}),'synthetic_secret_scan':'passed'}))
if __name__=='__main__':package()
