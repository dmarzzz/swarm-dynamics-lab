"""Assignment manifest: per stage the count, every assignment id with its packet hash in dispatch
order, the number of distinct packets and a digest, for the scripted stage and for each model's
paid stages. Both qualification sets are listed. `python3 src/manifest.py` writes manifest.json; `--check` compares.
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
    """`stages`: the scripted stage and the first model's paid stages. `models`: per model its batches,
    its system message hash and, for a later ladder model, its own paid stages (its packet hashes use
    its own system message). The user messages are the same for every model."""
    ladder = study.model_ladder(); first = ladder[0]
    stages = {stage: stage_entry(study.assignments(stage, first)) for stage in study.STAGES}
    sets = {which: stage_entry(study.qualification_fixtures(which, first)) for which in ('a', 'b')}
    models = {}
    for name in ladder:
        m = study.spec(name)
        models[name] = {'provider': study.provider_name(name), 'answer_format': m['answer_format'], 'qualification_set': m['qualification_set'],
                        'batches': {stage: (study.design()['scripted_batch'] if stage == 'S0' else f'{stage.lower()}-{m["attempt"]}{m["tag"]}') for stage in study.STAGES},
                        'system_sha256': hashlib.sha256(study.system(name).encode()).hexdigest()}
        if name != first:
            models[name]['stages'] = {stage: stage_entry(study.assignments(stage, name)) for stage in ('P0', 'Q0', 'S1')}
    parts = {**{s: stages[s]['digest'] for s in study.STAGES}, **{'qualification_' + w: sets[w]['digest'] for w in sets},
             **{f'{name}:{s}': e['digest'] for name, m in models.items() for s, e in m.get('stages', {}).items()},
             **{f'{name}:system': m['system_sha256'] for name, m in models.items()}}
    digest = hashlib.sha256(json.dumps(parts, sort_keys=True).encode()).hexdigest()
    return {'study': study.EXPERIMENT, 'format': 'one "<assignment id> <sha256 of the system message and user message>" per line, dispatch order',
            'source_hash': study.source_hash(), 'digest': digest,
            'system_sha256': hashlib.sha256(study.system(first).encode()).hexdigest(),
            'model_ladder': ladder, 'stages': stages, 'qualification_sets': sets, 'models': models}


def entry(reference, stage, name=None):
    """The manifest entry of one stage for a model (default: this chain's model)."""
    name = name or study.model()
    if stage == 'S0' or name == reference['model_ladder'][0]:
        return reference['stages'][stage]
    return reference['models'][name]['stages'][stage]


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
