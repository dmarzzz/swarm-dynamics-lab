#!/usr/bin/env python3
"""List one attempt's hub runs with their recorded artifact hashes, for archive.py. No model calls."""
import json
import sys
import swarm_report as sr

study, attempt = sys.argv[1:3]
rows = []
for r in sr.runs(study, limit=500):
    if r['params'].get('attempt_id') != attempt or r['params'].get('kind') == 'analysis':
        continue
    full = sr.get_run(r['run'])
    rows.append({'run': full['run'], 'status': full['status'], 'params': full['params'],
                 'metrics': full.get('metrics', {}),
                 'artifacts': [{'name': a['name'], 'sha256': a['sha256']} for a in full.get('artifacts', [])]})
print(json.dumps(sorted(rows, key=lambda v: v['run']), indent=2))
