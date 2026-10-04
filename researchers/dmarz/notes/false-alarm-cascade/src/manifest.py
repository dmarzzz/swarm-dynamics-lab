"""Assignment manifest. Per stage: the planned call rows, every unit in dispatch order and a digest.

A fixture (P0, Q0) is one call whose packet is fixed in advance: its line is "<id> <packet sha256>".
An episode is 30 calls whose later packets depend on earlier answers, so its line is
"<id> <sha256 of the episode's fixed inputs>": resources, every member's inspections for all
rounds, the planted slot and posts, the model slots, the system prompt and the schema.
`python3 src/manifest.py` writes manifest.json; `--check` compares.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import study

PATH = study.ROOT / 'manifest.json'


def line(unit):
    return f'{unit["id"]} {unit["fixed_hash"] if unit["type"] == "episode" else unit["packet_hash"]}'


def build():
    stages = {}
    for stage in study.STAGES:
        plan = study.plan(stage)
        lines = [line(u) for u in plan['units']]
        stages[stage] = {'rows': plan['rows'],
                         'episodes': sum(u['type'] == 'episode' for u in plan['units']),
                         'fixtures': sum(u['type'] == 'fixture' for u in plan['units']),
                         'digest': hashlib.sha256('\n'.join(lines).encode()).hexdigest(), 'units': lines}
    digest = hashlib.sha256(json.dumps({s: stages[s]['digest'] for s in study.STAGES}, sort_keys=True).encode()).hexdigest()
    return {'study': study.EXPERIMENT,
            'format': 'one "<unit id> <sha256>" per line in dispatch order: packet hash for a fixture, fixed-inputs hash for an episode',
            'source_hash': study.source_hash(), 'digest': digest, 'stages': stages}


def render(manifest):
    """Stable text: one unit per line, so the file stays compact and diffs stay readable."""
    return json.dumps(manifest, indent=1, sort_keys=True) + '\n'


def counts(m):
    return {s: {k: m['stages'][s][k] for k in ('rows', 'episodes', 'fixtures')} for s in study.STAGES}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true', help='exit 1 unless manifest.json equals the regenerated manifest')
    a = ap.parse_args()
    text = render(build())
    m = json.loads(text)
    if a.check:
        same = PATH.exists() and PATH.read_text() == text
        print(json.dumps({'manifest_matches': same, 'digest': m['digest'], 'source_hash': m['source_hash'], 'counts': counts(m)}))
        return 0 if same else 1
    PATH.write_text(text)
    print(json.dumps({'written': str(PATH.name), 'bytes': len(text), 'digest': m['digest'], 'counts': counts(m)}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
