"""Reduce vishesh's Swarm of Theseus pilot (attempt S1-a1) to what the narrated film draws.

Reads the study's committed per-step rows and summary, and the filed evidence archive for the two runs the film goes
inside. Nothing is estimated: every value is copied from a saved record, or is a mean the study's own results table
also reports. This script only reads the study's files; it writes one small JSON file under data/.

    python3 researchers/dmarz/notes/theseus-film/film_data.py \
      --results researchers/vishesh/notes/swarm-of-theseus/results/S1-a1 \
      --evidence artifacts/theseus-pilot-evidence/theseus-pilot-evidence-v1.gz \
      --out data/theseus-film/film-data.json
"""
import argparse
import json
import tarfile
from pathlib import Path

ARMS = ['neither', 'notes', 'mentor', 'both', 'founders', 'verbatim']      # the wall's rows, top to bottom
SCENARIOS = ['seed-bank', 'observatory', 'repair-dock']                    # the wall's column groups
WORKED = ('seed-bank', 200)                                                # first scenario, first seed: chosen before reading any run
INSIDE = ['both', 'neither']                                               # the run the film enters, and its neighbour


def events(tar, attempt, scenario, arm, seed):
    raw = tar.extractfile(f'{attempt}/{scenario}-{arm}-{seed}/events.jsonl').read().decode()
    return [json.loads(line) for line in raw.splitlines() if line.strip()]


def inside(ev):
    """One run, step by step: who is in the crew, what each member was given and returned, and each handover."""
    steps = {}
    for e in ev:
        s = steps.setdefault(e['step'], {'members': {}, 'handover': None})
        if e['kind'] == 'frame':
            s.update({k: e[k] for k in ('accuracy', 'convention', 'collective', 'expected', 'rule_changed')}); s['roster'] = e['members']
            continue
        op, actor = e['operation'], e['actor']
        if op == 'solve':
            m = s['members'].setdefault(actor, {})
            if e['kind'] == 'request':
                o = e['request']['observation']
                m.update({'notebook_in': o['private_notebook'], 'onboarding': o['onboarding'], 'cases': o['cases']})
            else:
                out = e['output']
                m.update({'labels': [w['label'] for w in out['work']], 'case_ids': [w['case_id'] for w in out['work']],
                          'convention': out['convention'], 'notebook_out': out['notebook']})
        else:                                                               # the newcomer's question, the departing member's answer
            h = s['handover'] or {}
            if e['kind'] == 'response': h[op] = {'actor': actor, 'message': e['output']['message']}
            elif op == 'answer': h['answer_notebook'] = e['request']['observation']['private_notebook']
            s['handover'] = h
    out = []
    for k in sorted(steps):
        s = steps[k]; s['step'] = k; s['members'] = [dict(s['members'][name], id=name) for name in s['roster']]; del s['roster']
        out.append(s)
    return out


def main():
    ap = argparse.ArgumentParser()
    for a in ('results', 'evidence', 'out'): ap.add_argument('--' + a, required=True)
    args = ap.parse_args()
    res = Path(args.results)
    rows, summary, manifest = (json.loads((res / f).read_text()) for f in ('rows.json', 'summary.json', 'manifest.json'))
    if summary['assigned'] != summary['completed'] or summary['failed'] or any(r['status'] != 'completed' for r in rows):
        raise SystemExit('the pilot is not complete')

    wall = []
    for r in rows:
        steps = [{'founder': [m.startswith('founder') for m in h['members']], 'right': [c == x for c, x in zip(h['collective'], h['expected'])],
                  'receipt': h['convention'], 'changed': h['rule_changed']} for h in r['history']]
        wall.append({'scenario': r['scenario'], 'seed': r['seed'], 'arm': r['arm'], 'steps': steps})

    by = summary['by_scenario']
    after = {arm: sum(by[sc][arm]['accuracy'] for sc in SCENARIOS) / len(SCENARIOS) for arm in ARMS}      # steps 4 and 5, equal weight per scenario
    with tarfile.open(args.evidence) as tar:
        runs = {arm: inside(events(tar, manifest['attempt'], WORKED[0], arm, WORKED[1])) for arm in INSIDE}
        calls = sum(1 for r in rows for e in events(tar, manifest['attempt'], r['scenario'], r['arm'], r['seed']) if e['kind'] == 'request')
        instructions = events(tar, manifest['attempt'], WORKED[0], 'both', WORKED[1])[0]['request']['instructions']

    data = {'run': {'attempt': manifest['attempt'], 'source': manifest['source'], 'runs': len(rows), 'calls': calls,
                    'calls_reported': summary['cost']['calls'], 'cost_usd': summary['cost']['actual_usd']},
            'arms': ARMS, 'scenarios': SCENARIOS, 'seeds': sorted({r['seed'] for r in rows}), 'worked': {'scenario': WORKED[0], 'seed': WORKED[1]},
            'wall': wall, 'after': after, 'by_scenario': {sc: {arm: by[sc][arm] for arm in ARMS} for sc in SCENARIOS},
            'primary': summary['primary'], 'inside': runs, 'instructions': instructions}
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(data, sort_keys=True))
    print(f'wrote {out}: {len(wall)} runs, {calls} calls, after turnover ' + ', '.join(f'{a} {after[a]:.1%}' for a in ARMS))


if __name__ == '__main__':
    main()
