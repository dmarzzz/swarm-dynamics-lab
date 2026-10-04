"""Offline hashes plus public amendment readback; no model request."""
from pathlib import Path
import hashlib,json,urllib.request,datetime
p=Path(__file__).resolve().parent.parent
names=['PREREG.md','AMENDMENT-0.md','AMENDMENT-1.md','run.py','inputs.json','analyze.py','scripted-reference.json','../src/sim.py','attempt2/transport.py']
(p/'attempt2/source-hashes.json').write_text(json.dumps({n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in names},indent=2)+'\n')
u='https://raw.githubusercontent.com/dmarzzz/swarm-lab/34aa78f7/researchers/shadow/notes/capture-memory/freeze-claude/AMENDMENT-1.md'
s=urllib.request.urlopen(u,timeout=30).read(); assert s==(p/'AMENDMENT-1.md').read_bytes()
(p/'attempt2/PUBLIC-PLAN.json').write_text(json.dumps(dict(url=u,sha256=hashlib.sha256(s).hexdigest(),verified=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n')
