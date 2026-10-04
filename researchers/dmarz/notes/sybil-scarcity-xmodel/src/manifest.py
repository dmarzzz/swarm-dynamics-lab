"""Assignment manifest: for every stage the number of assignments, each assignment id with the
first 16 hex digits of its packet hash, the largest and total request bytes, and a digest over
the ids and the full packet hashes. The same for every model of the ladder. `python3 src/manifest.py` writes manifest.json; `--check` exits non-zero when the
committed file differs."""
import argparse
import json
import sys

import study

PATH = study.ROOT / 'manifest.json'
ENTRIES = study.STAGES


def stage_entry(rows):
    pairs = sorted((a['id'], a['packet_hash']) for a in rows)
    return {'assignments': len(pairs), 'digest': study.digest(pairs),
            'request_bytes': sum(a['request_bytes'] for a in rows),
            'max_request_bytes': max(a['request_bytes'] for a in rows),
            'distinct_packets': len({h for _, h in pairs}),
            'ids': [f'{i}:{h[:16]}' for i, h in pairs]}


def build():
    entries = {stage: stage_entry(study.assignments(stage)) for stage in study.STAGES}
    return {'experiment': study.EXPERIMENT, 'contract': 'ready-chain-v1', 'attempt': study.design()['attempt'],
            'digest': study.digest([(s, entries[s]['digest']) for s in ENTRIES]), 'stages': entries}


def text(manifest):
    """Compact and stable: one line per assignment."""
    lines = ['{', f' "attempt": {json.dumps(manifest["attempt"])},', f' "contract": {json.dumps(manifest["contract"])},',
             f' "digest": {json.dumps(manifest["digest"])},', f' "experiment": {json.dumps(manifest["experiment"])},', ' "stages": {']
    names = list(manifest['stages'])
    for n, stage in enumerate(names):
        e = manifest['stages'][stage]
        lines.append(f'  {json.dumps(stage)}: {{')
        for key in ('assignments', 'digest', 'distinct_packets', 'max_request_bytes', 'request_bytes'):
            lines.append(f'   {json.dumps(key)}: {json.dumps(e[key])},')
        lines.append('   "ids": [')
        lines += [f'    {json.dumps(x)}' + (',' if i < len(e['ids']) - 1 else '') for i, x in enumerate(e['ids'])]
        lines.append('   ]'); lines.append('  }' + (',' if n < len(names) - 1 else ''))
    lines += [' }', '}']
    return '\n'.join(lines) + '\n'


def load():
    return json.loads(PATH.read_text())


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); a = ap.parse_args()
    fresh = text(build()); m = json.loads(fresh)
    counts = {s: e['assignments'] for s, e in m['stages'].items()}
    if a.check:
        same = PATH.exists() and PATH.read_text() == fresh
        print(json.dumps({'manifest_current': same, 'digest': m['digest'], 'assignments': counts})); sys.exit(0 if same else 1)
    PATH.write_text(fresh)
    print(json.dumps({'written': str(PATH), 'digest': m['digest'], 'bytes': len(fresh), 'assignments': counts}))


if __name__ == '__main__':
    main()
