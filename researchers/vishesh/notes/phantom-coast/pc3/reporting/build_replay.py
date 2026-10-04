"""Build an offline interactive view from a completed native PC-3 cohort."""
import argparse,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();r=a.directory
s=json.loads((r/'summary.json').read_text());e=json.loads((r/'episodes.json').read_text())
assert s['stage']=='S1' and len(e)==96
payload=json.dumps({'summary':s,'episodes':e},separators=(',',':')).replace('</','<\\/')
t=Path(__file__).with_name('replay-template.html').read_text();out=r/'measured-replay.html';out.write_text(t.replace('__DATA__',payload));print(json.dumps({'output':str(out),'episodes':len(e),'source_sha256':{n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in ('summary.json','episodes.json')}}))
