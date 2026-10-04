"""Assignment manifest. Every input is fixed in advance, so the manifest lists, per stage, every
assignment id with the first 16 hex digits of the hash of its request (system prompt and user message),
the number of calls, the request sizes and a digest over the ids and the full hashes.
`python3 src/manifest.py` writes manifest.json; `python3 src/manifest.py --check` exits non-zero when the
committed file differs."""
import argparse
import json
import os
import sys

import study

PATH = study.ROOT / 'manifest.json'
KEYS = ('assignments', 'max_calls', 'digest', 'distinct_inputs', 'content_bytes_total', 'content_bytes_max')


def stage_entry(rows, scripted=False):
    pairs = sorted((a['id'], a['input_hash']) for a in rows)
    return {'assignments': len(pairs), 'max_calls': 0 if scripted else len(pairs), 'digest': study.digest(pairs),
            'distinct_inputs': len({h for _, h in pairs}), 'content_bytes_total': sum(a['content_bytes'] for a in rows),
            'content_bytes_max': max(a['content_bytes'] for a in rows), 'ids': [f'{i}:{h[:16]}' for i, h in pairs]}


def model_entry(name):
    """The manifest of one model's chain: its batches, system prompt hash, digest and stages."""
    before = os.environ.get('STUDY_MODEL'); os.environ['STUDY_MODEL'] = name
    try:
        stages = {stage: stage_entry(study.assignments(stage), stage == 'S0') for stage in study.STAGES}
        return {'answer_schema': study.schema(), 'batches': [study.batch(s) for s in study.STAGES], 'provider': study.provider_name(),
                'system_prompt_sha256': study.digest(study.system()),
                'digest': study.digest([(s, stages[s]['digest']) for s in study.STAGES]), 'stages': stages}
    finally:
        if before is None: os.environ.pop('STUDY_MODEL', None)
        else: os.environ['STUDY_MODEL'] = before


def build():
    """The first model of the ladder at the top level (the same keys and digest as before the ladder existed) and
    every later model under `ladder`."""
    ladder = study.design()['model_ladder']; first = model_entry(ladder[0])
    return {'experiment': study.EXPERIMENT, 'contract': 'ready-chain-v1', 'attempt': study.design()['attempt'],
            'qualification_set': study.active_set(), 'model': ladder[0], 'system_prompt_sha256': first['system_prompt_sha256'],
            'digest': first['digest'], 'stages': first['stages'],
            'ladder': {name: model_entry(name) for name in ladder[1:]}}


def stage_lines(stages, pad):
    lines = [pad + '"stages": {']; names = list(stages)
    for n, stage in enumerate(names):
        e = stages[stage]
        lines.append(f'{pad} {json.dumps(stage)}: {{')
        for key in KEYS: lines.append(f'{pad}  {json.dumps(key)}: {json.dumps(e[key])},')
        lines.append(pad + '  "ids": [')
        lines += [f'{pad}   {json.dumps(x)}' + (',' if i < len(e['ids']) - 1 else '') for i, x in enumerate(e['ids'])]
        lines.append(pad + '  ]'); lines.append(pad + ' }' + (',' if n < len(names) - 1 else ''))
    lines.append(pad + '}')
    return lines


def text(manifest):
    """Compact and stable: one line per assignment."""
    lines = ['{']
    for key in ('attempt', 'contract', 'digest', 'experiment', 'model', 'qualification_set', 'system_prompt_sha256'):
        lines.append(f' {json.dumps(key)}: {json.dumps(manifest[key])},')
    lines += stage_lines(manifest['stages'], ' '); lines[-1] += ','
    lines.append(' "ladder": {'); names = list(manifest['ladder'])
    for n, name in enumerate(names):
        e = manifest['ladder'][name]
        lines.append(f'  {json.dumps(name)}: {{')
        for key in ('answer_schema', 'batches', 'digest', 'provider', 'system_prompt_sha256'):
            lines.append(f'   {json.dumps(key)}: {json.dumps(e[key])},')
        lines += stage_lines(e['stages'], '   ')
        lines.append('  }' + (',' if n < len(names) - 1 else ''))
    lines += [' }', '}']
    return '\n'.join(lines) + '\n'


def load():
    return json.loads(PATH.read_text())


def reference():
    """The committed manifest of the chain's model: its digest and stages."""
    m = load()
    return m if study.model() == m['model'] else m['ladder'][study.model()]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); a = ap.parse_args()
    fresh = text(build()); m = json.loads(fresh)
    counts = {s: {'assignments': e['assignments'], 'max_calls': e['max_calls']} for s, e in m['stages'].items()}
    counts['ladder'] = {name: e['digest'] for name, e in m['ladder'].items()}
    if a.check:
        same = PATH.exists() and PATH.read_text() == fresh
        print(json.dumps({'manifest_current': same, 'digest': m['digest'], 'stages': counts}))
        sys.exit(0 if same else 1)
    PATH.write_text(fresh)
    print(json.dumps({'written': str(PATH), 'digest': m['digest'], 'bytes': len(fresh), 'stages': counts}))


if __name__ == '__main__':
    main()
