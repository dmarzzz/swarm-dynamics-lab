"""Package only synthetic experiment evidence, with deterministic content hashes."""
import gzip,hashlib,io,json,re,sys,tarfile
from pathlib import Path

def package(root,out):
    root=Path(root);out=Path(out);files=[]
    allowed={'manifest.json','summary.json','audit.json','outcome.json','events.jsonl','history.json','public-plan-receipt.json','rows.json','S0-a1-setup.json'}
    for p in sorted(root.rglob('*')):
        if not p.is_file() or p.name not in allowed:continue
        data=p.read_bytes()
        if re.search(rb'(?:sk-ant-|github_pat_|ghp_)[A-Za-z0-9_-]{20,}',data):raise ValueError('credential_pattern_detected')
        files.append((str(p.relative_to(root)),data))
    index={'format':'theseus-evidence-v1','scope':'Synthetic actor inputs/outputs, metrics, manifests and public-plan receipts; no provider headers or credentials.',
           'files':[{'path':n,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()} for n,d in files]}
    files.append(('bundle-index.json',json.dumps(index,indent=2).encode()))
    buf=io.BytesIO()
    with tarfile.open(fileobj=buf,mode='w') as tar:
        for name,data in files:
            info=tarfile.TarInfo(name);info.size=len(data);info.mtime=0;info.mode=0o644
            tar.addfile(info,io.BytesIO(data))
    out.write_bytes(gzip.compress(buf.getvalue(),mtime=0))
    return {'files':len(files),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
if __name__=='__main__':print(json.dumps(package(sys.argv[1],sys.argv[2])))
