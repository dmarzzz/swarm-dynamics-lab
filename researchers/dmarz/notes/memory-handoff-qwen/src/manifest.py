"""Assignment manifest: per stage the count, every assignment id with its packet hash in dispatch
order, the number of distinct packets and a digest. Both qualification sets are listed (set a was
used by attempt 001, set b is used by attempt 002). `python3 src/manifest.py` writes manifest.json; `--check` compares.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import study  # noqa: E402

PATH = study.ROOT / 'manifest.json'


def stage_entry(rows):
    lines = [f'{a["id"]} {a["packet_hash"]}' for a in rows]
    return {'count': len(lines), 'distinct_packets': len({a['packet_hash'] for a in rows}),
            'max_request_bytes': max(a['request_bytes'] for a in rows),
            'digest': hashlib.sha256('\n'.join(lines).encode()).hexdigest(), 'assignments': lines}


def build():
    stages = {stage: stage_entry(study.assignments(stage)) for stage in study.STAGES}
    sets = {which: stage_entry(study.qualification_fixtures(which)) for which in ('a', 'b')}
    digest = hashlib.sha256(json.dumps({**{s: stages[s]['digest'] for s in study.STAGES}, **{'qualification_' + w: sets[w]['digest'] for w in sets},
                                        'system': hashlib.sha256(study.SYSTEM.encode()).hexdigest()}, sort_keys=True).encode()).hexdigest()
    return {'study': study.EXPERIMENT, 'format': 'one "<assignment id> <sha256 of the system message and user message>" per line, dispatch order',
            'source_hash': study.source_hash(), 'digest': digest,
            'system_sha256': hashlib.sha256(study.SYSTEM.encode()).hexdigest(),
            'qualification_set': study.design()['qualification']['set'],
            'attempt': study.design()['attempt'], 'stages': stages, 'qualification_sets': sets}


def render(manifest):
    """Stable text: one assignment per line, so the file stays compact and diffs stay readable."""
    return json.dumps(manifest, indent=1, sort_keys=True) + '\n'


def load():
    return json.loads(PATH.read_text())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true', help='exit 1 unless manifest.json equals the regenerated manifest')
    a = ap.parse_args()
    text = render(build()); m = json.loads(text)
    counts = {s: m['stages'][s]['count'] for s in study.STAGES}
    if a.check:
        same = PATH.exists() and PATH.read_text() == text
        print(json.dumps({'manifest_matches': same, 'digest': m['digest'], 'source_hash': m['source_hash'], 'counts': counts}))
        return 0 if same else 1
    PATH.write_text(text)
    print(json.dumps({'written': PATH.name, 'bytes': len(text), 'digest': m['digest'], 'counts': counts,
                      'distinct_packets': {s: m['stages'][s]['distinct_packets'] for s in study.STAGES}}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
