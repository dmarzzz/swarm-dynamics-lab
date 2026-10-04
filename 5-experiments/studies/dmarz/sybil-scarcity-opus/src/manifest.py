"""Assignment manifest: per stage the count, every assignment id with its packet hash in dispatch
order, and a digest. `python3 src/manifest.py` writes manifest.json; `--check` compares.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import study

PATH = study.ROOT / 'manifest.json'


def build():
    stages = {}
    for stage in study.STAGES:
        rows = study.assignments(stage)
        lines = [f'{a["id"]} {a["packet_hash"]}' for a in rows]
        stages[stage] = {'count': len(lines), 'distinct_packets': len({a['packet_hash'] for a in rows}),
                         'digest': hashlib.sha256('\n'.join(lines).encode()).hexdigest(), 'assignments': lines}
    digest = hashlib.sha256(json.dumps({s: stages[s]['digest'] for s in study.STAGES}, sort_keys=True).encode()).hexdigest()
    return {'study': study.EXPERIMENT, 'format': 'one "<assignment id> <packet sha256>" per line, dispatch order',
            'source_hash': study.source_hash(), 'digest': digest, 'stages': stages}


def render(manifest):
    """Stable text: one assignment per line, so the file stays compact and diffs stay readable."""
    return json.dumps(manifest, indent=1, sort_keys=True) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true', help='exit 1 unless manifest.json equals the regenerated manifest')
    a = ap.parse_args()
    text = render(build())
    if a.check:
        same = PATH.exists() and PATH.read_text() == text
        m = json.loads(text)
        print(json.dumps({'manifest_matches': same, 'digest': m['digest'], 'source_hash': m['source_hash'],
                          'counts': {s: m['stages'][s]['count'] for s in study.STAGES}}))
        return 0 if same else 1
    PATH.write_text(text)
    m = json.loads(text)
    print(json.dumps({'written': str(PATH.name), 'bytes': len(text), 'digest': m['digest'],
                      'counts': {s: m['stages'][s]['count'] for s in study.STAGES}}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
