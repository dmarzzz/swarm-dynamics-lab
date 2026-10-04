#!/usr/bin/env python3
"""Read-only task/hub screening of the ten PI guide projects. No model calls."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import urllib.request
import yaml

ROOT = Path(__file__).resolve().parents[4]
TOKENS = {
 'quorum': ('quorum-mirrors', 'quorum-of-mirrors'),
 'phantom': ('phantom',), 'dissenter': ('dissenter',),
 'sizing': ('sizing', 'swarm-size', 'optimal-size'),
 'heterogeneous': ('heterogeneous', 'poietic', 'salvage'),
 'theseus': ('theseus',), 'immune': ('immune',),
 'influence': ('influence',), 'healing': ('healing',), 'antsy': ('antsy', 'adaptive-quorum'),
}

def stamp(value):
    return datetime.fromtimestamp(value, timezone.utc).isoformat() if isinstance(value, (int, float)) else value


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--hub-state', type=Path, help='Optional saved public /api/state JSON; avoids client-specific HTTP filtering')
    args = ap.parse_args()
    guide_path = ROOT/'researchers/vishesh/notes/pi-review-guide-2026-10-04/review-guide.json'
    guide = json.loads(guide_path.read_text())
    tasks = []
    for path in sorted((ROOT/'tasks').glob('*.md')):
        match = re.match(r'^---\n(.*?)\n---', path.read_text(), re.S)
        if match:
            t = yaml.safe_load(match.group(1))
            tasks.append({k: t.get(k) for k in ('id', 'title', 'status', 'owner', 'for', 'updated')})
    url = 'https://swarm-live.pages.dev/api/state'
    if args.hub_state:
        state = json.loads(args.hub_state.read_text())
    else:
        with urllib.request.urlopen(url, timeout=30) as response:
            state = json.load(response)
    output = {'repository_commit': subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT,text=True).strip(),
              'source_guide': str(guide_path.relative_to(ROOT)),
              'guide_cutoff': '2026-10-04T02:30Z through 03:40Z; presentation excludes later results',
              'hub_url': url, 'hub_timestamp_utc': stamp(state.get('now')),
              'hub_status': 'HTTP 200',
              'coordination_tasks': [t for t in tasks if t['id'] == 'pi-cycle-2026-10-04'],
              'projects': []}
    for p in guide['projects']:
        terms = TOKENS[p['id']]
        def relevant(value):
            return any(token in value.lower() for token in terms)
        related = [t for t in tasks if relevant(t['id']) and not t['id'].startswith('scan-')]
        experiments = []
        for e in state['experiments']:
            if not relevant(e['id']):
                continue
            runs = e.get('runs', [])
            latest = sorted(runs, key=lambda r: r.get('updated') or 0, reverse=True)[:3]
            experiments.append({'id': e['id'], 'run_status_counts': dict(Counter(r['status'] for r in runs)),
                'latest_runs': [{'run': r['run'], 'status': r['status'], 'updated': stamp(r.get('updated')),
                                  'stale_by_600_second_rule': bool(r['status'] in ('running','assigned') and state.get('now', 0)-(r.get('updated') or 0)>600)}
                                 for r in latest]})
        output['projects'].append({'id': p['id'], 'name': p['name'], 'guide_evidence_status': p['assessments']['evidence']['status'],
             'recommended_options': [o for o in p['options'] if o.get('recommended')],
             'related_tasks': related, 'hub_experiments': experiments})
    target = Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(output, indent=2, default=str)+'\n')
    print('Hub timestamp:', output['hub_timestamp_utc'])
    for p in output['projects']:
        print(p['id'], 'guide:',p['guide_evidence_status'], 'claimed:',[(t['id'], t['owner']) for t in p['related_tasks'] if t['status']=='claimed'])
        print('hub:', [(e['id'], e['run_status_counts']) for e in p['hub_experiments']])

if __name__=='__main__':
    main()
