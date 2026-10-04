import json,gzip,hashlib,sys
from pathlib import Path
B=Path(__file__).resolve().parents[1];sys.path.insert(0,str(B.parent/'pc5/src'));from wire import digest
p=B/'results/native-traces.json.gz';a=json.loads((B/'results/trace-audit.json').read_text());assert hashlib.sha256(p.read_bytes()).hexdigest()==a['bundle_sha256'];rs=json.loads(gzip.decompress(p.read_bytes()));assert len(rs)==140 and len({(r['stage'],r['id']) for r in rs})==140
for r in rs:
 assert digest(r['request'])==r['request_sha256']==r['checked_response']['request_sha256']
 assert r['checked_response']['result']['choice'] in r['request']['questions']['target']['criteria']
 assert set(r['request'])=={'model','provider','state','questions'} and r['native_tool_calls']==0
assert sum(r['stage']=='Q0' for r in rs)==12 and sum(r['stage']=='S1' and not r['semantic_optimal'] for r in rs)==50
print('Portable trace readback verified:140 request/checked-output pairs;50 S1 suboptimal;raw-body gap preserved.')
