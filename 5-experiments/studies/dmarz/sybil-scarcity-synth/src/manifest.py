"""Assignment manifest: per stage the count, every assignment id with its synthesizer
configuration and packet hash in dispatch order, and a digest; plus the pinned prompt hashes.
`python3 src/manifest.py` writes manifest.json; `--check` compares.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import provider
import study

PATH = study.ROOT / 'manifest.json'


def line(a):
    return f'{a["id"]} {a["prompt"]}-{a["effort"]} {a["packet_hash"]}'


def build():
    stages = {}
    for stage in study.STAGES:
        rows = study.assignments(stage)
        lines = [line(a) for a in rows]
        stages[stage] = {'count': len(lines), 'distinct_packets': len({a['packet_hash'] for a in rows}),
                         'digest': hashlib.sha256('\n'.join(lines).encode()).hexdigest(), 'assignments': lines}
    digest = hashlib.sha256(json.dumps({s: stages[s]['digest'] for s in study.STAGES}, sort_keys=True).encode()).hexdigest()
    return {'study': study.EXPERIMENT,
            'format': 'one "<assignment id> <prompt>-<effort> <packet sha256>" per line, dispatch order',
            'prompt_sha256': {name: hashlib.sha256(text.encode()).hexdigest() for name, text in provider.PROMPTS.items()},
            'source_hash': study.source_hash(), 'digest': digest, 'stages': stages}


def render(manifest):
    """Stable text: one assignment per line, so the file stays compact and diffs stay readable."""
    return json.dumps(manifest, indent=1, sort_keys=True) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true', help='exit 1 unless manifest.json equals the regenerated manifest')
    a = ap.parse_args()
    text = render(build())
    m = json.loads(text)
    counts = {s: m['stages'][s]['count'] for s in study.STAGES}
    if a.check:
        same = PATH.exists() and PATH.read_text() == text
        print(json.dumps({'manifest_matches': same, 'digest': m['digest'], 'source_hash': m['source_hash'], 'counts': counts}))
        return 0 if same else 1
    PATH.write_text(text)
    print(json.dumps({'written': str(PATH.name), 'bytes': len(text), 'digest': m['digest'], 'counts': counts}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
