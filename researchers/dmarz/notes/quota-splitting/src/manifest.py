"""Assignment manifest for multi-turn episodes. Later inputs of an episode depend on the model's
answers, so the manifest lists, per stage, every episode id with the first 16 hex digits of the
hash of its fixed inputs (system prompt, schema, world, rules, round-1 state, turn limit), the
largest number of calls the stage can make, and a digest over the ids and the full hashes.
`python3 src/manifest.py` writes manifest.json; `python3 src/manifest.py --check` exits non-zero
when the committed file differs."""
import argparse
import json
import sys

import study

PATH = study.ROOT / 'manifest.json'
KEYS = ('episodes', 'max_calls', 'digest', 'distinct_fixed_inputs', 'first_request_bytes')


def stage_entry(rows):
    pairs = sorted((a['id'], a['fixed_hash']) for a in rows)
    scripted = any(a['planner'] for a in rows)
    return {'episodes': len(pairs), 'max_calls': 0 if scripted else sum(a['max_turns'] for a in rows),
            'digest': study.digest(pairs), 'distinct_fixed_inputs': len({h for _, h in pairs}),
            'first_request_bytes': sum(len(study.system_prompt(a['condition'])) + len(study.user_text(a['first_state'])) for a in rows),
            'ids': [f'{i}:{h[:16]}' for i, h in pairs]}


def build():
    stages = {stage: stage_entry(study.assignments(stage)) for stage in study.STAGES}
    return {'experiment': study.EXPERIMENT, 'contract': 'ready-chain-v1',
            'digest': study.digest([(s, stages[s]['digest']) for s in study.STAGES]), 'stages': stages}


def text(manifest):
    """Compact and stable: one line per episode."""
    lines = ['{', f' "contract": {json.dumps(manifest["contract"])},', f' "digest": {json.dumps(manifest["digest"])},',
             f' "experiment": {json.dumps(manifest["experiment"])},', ' "stages": {']
    names = list(manifest['stages'])
    for n, stage in enumerate(names):
        e = manifest['stages'][stage]
        lines.append(f'  {json.dumps(stage)}: {{')
        for key in KEYS:
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
    counts = {s: {'episodes': e['episodes'], 'max_calls': e['max_calls']} for s, e in m['stages'].items()}
    if a.check:
        same = PATH.exists() and PATH.read_text() == fresh
        print(json.dumps({'manifest_current': same, 'digest': m['digest'], 'stages': counts}))
        sys.exit(0 if same else 1)
    PATH.write_text(fresh)
    print(json.dumps({'written': str(PATH), 'digest': m['digest'], 'bytes': len(fresh), 'stages': counts}))


if __name__ == '__main__':
    main()
