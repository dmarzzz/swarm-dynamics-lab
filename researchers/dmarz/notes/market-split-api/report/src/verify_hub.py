#!/usr/bin/env python3
"""Read back immutable run artifacts; emit hashes and sizes without private hub metadata."""
import concurrent.futures
import hashlib
import json
import sys
import urllib.parse
import urllib.request
import swarm_report as sr

study, attempt = sys.argv[1:3]
config = sr._config()
base = config['SWARM_HUB_URL'].rstrip('/')
headers = {'Authorization': 'Bearer ' + config['SWARM_HUB_TOKEN']}
runs = [sr.get_run(r['run']) for r in sr.runs(study, limit=500)
        if r['params'].get('attempt_id') == attempt]
assert runs and all(r['status'] == 'done' for r in runs)
items = [(r['run'], a) for r in runs for a in r['artifacts']]
assert items

def verify(item):
    run, artifact = item
    path = '/a/' + urllib.parse.quote(run, safe='/') + '/' + urllib.parse.quote(artifact['name'], safe='/')
    try:
        with urllib.request.urlopen(urllib.request.Request(base + path, headers=headers), timeout=30) as response:
            payload = response.read()
    except Exception as exc:
        raise RuntimeError('artifact_readback_failed:' + type(exc).__name__) from None
    digest = hashlib.sha256(payload).hexdigest()
    assert digest == artifact['sha256'], 'artifact_hash_mismatch'
    return {'run': run, 'name': artifact['name'], 'sha256': digest, 'bytes': len(payload)}

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    receipts = list(pool.map(verify, items))
print(json.dumps({'study': study, 'attempt': attempt, 'runs': len(runs),
                  'verified_artifacts': len(receipts), 'receipts': receipts}, indent=2))
