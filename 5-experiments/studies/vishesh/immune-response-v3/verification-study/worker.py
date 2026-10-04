"""Admitted native collection and saved-data publication; no automatic successor."""
import argparse,hashlib,importlib.util,json,os,sys
from pathlib import Path
import native_run
BASE=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--admission',required=True);a=p.parse_args();out=Path(a.out)
    receipt=native_run.verify_admission(a.admission);assert not out.exists()
    fd=os.open(str(out)+'.dispatch',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.close(fd)
    sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
    job=sr.start('immune-response-v3',params={'stage':'verification-v1','runtime_commit':receipt['commit'],'max_calls':192,'episodes':48},message='Fresh confirmation versus contradiction; explicit guard versus unguarded Opus;6authored roots in3families,2fresh repeats. Protected outcomes separate from model competence.')
    print(json.dumps({'run':job.id}),flush=True)
    def publish():
        if (out/'episodes.json').exists():
            spec=importlib.util.spec_from_file_location('verification_render',BASE/'render.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r);r.render(out/'episodes.json',out/'replay.html','native')
        index=[]
        # Explicit allowlist excludes private admission/account/ledger metadata.
        for name in ('episodes.json','episodes.jsonl','events.jsonl','summary.json','usage.jsonl','transport.jsonl','replay.html'):
            file=out/name
            if file.exists():
                import gzip
                raw=file.read_bytes();compressed=out/(name+'.gz');compressed.write_bytes(gzip.compress(raw,mtime=0));job.artifact(compressed,compressed.name)
                index.append({'file':name,'sha256':hashlib.sha256(raw).hexdigest(),'encoding':'gzip','parts':[compressed.name]})
        (out/'artifact-index.json').write_text(json.dumps(index,indent=2));job.artifact(out/'artifact-index.json','artifact-index.json')
    try:
        s=native_run.execute(out,a.admission);publish();job.done(message='Collection complete; authored scientific review pending; no successor admitted.',episodes=s['completed'],api_calls=s['api_calls'],actual_usd=s['actual_usd'],scientific_review_complete=0)
    except Exception as e:
        try:publish()
        except Exception:pass
        job.fail('Stopped; retain partial evidence: '+type(e).__name__);raise
if __name__=='__main__':
    try:main()
    except Exception as e:print(json.dumps({'stopped':type(e).__name__}));raise SystemExit(1)
