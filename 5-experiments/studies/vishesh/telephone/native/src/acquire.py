"""Full-table bounded private projections; stdout never includes corpus or errors."""
import hashlib,json,os,sys,zlib,urllib.request
from pathlib import Path
SHARED=Path(__file__).resolve().parents[3]/'ai-village-replay-2026-10-04/src'
sys.path.insert(0,str(SHARED))
from inventory import SafeRedirect,project,REVISION

def collect(table,token,out):
    path=out/(table+'.jsonl');dec=zlib.decompressobj(16+zlib.MAX_WBITS)
    compressed=decoded=count=0;buf=b'';h=hashlib.sha256()
    req=urllib.request.Request(f'https://huggingface.co/datasets/aidigestorg/ai-village/resolve/{REVISION}/{table}.jsonl.gz',headers={'Authorization':'Bearer '+token})
    with urllib.request.build_opener(SafeRedirect()).open(req,timeout=60) as response,path.open('x') as f:
        while True:
            chunk=response.read(65536)
            if not chunk:break
            compressed+=len(chunk)
            if compressed>(512 if table=='events' else 128)*1024**2:raise ValueError('compressed_limit')
            expanded=dec.decompress(chunk,(4 if table=='events' else 1)*1024**3-decoded+1);decoded+=len(expanded)
            if decoded>(4 if table=='events' else 1)*1024**3:raise ValueError('decoded_limit')
            buf+=expanded
            lines=buf.split(b'\n');buf=lines.pop()
            for line in lines:
                if not line:continue
                row=json.loads(line);h.update(line+b'\n');count+=1
                f.write(json.dumps(project(table,row),ensure_ascii=False)+'\n')
        if buf:
            row=json.loads(buf);h.update(buf);count+=1;f.write(json.dumps(project(table,row),ensure_ascii=False)+'\n')
    if not dec.eof or dec.unused_data:raise ValueError('incomplete_or_extra_gzip')
    return {'table':table,'rows':count,'compressed_bytes':compressed,'decoded_bytes':decoded,'source_sha256':h.hexdigest(),'projection_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'complete':True}
if __name__=='__main__':
    os.umask(0o077)
    try:
        out=Path(sys.argv[1]);out.mkdir(mode=0o700,exist_ok=False)
        token=Path('/Users/ultron/.cache/huggingface/token').read_text().strip()
        receipt={'revision':REVISION,'tables':[],'model_calls':0}
        for table in ('chat_messages','events'):
            receipt['tables'].append(collect(table,token,out))
            (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
            print(json.dumps(receipt['tables'][-1]),flush=True)
    except Exception: print('Acquisition stopped; diagnostics suppressed.');raise SystemExit(1)
