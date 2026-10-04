"""Reduce one finished benchmark-v3 run to the numbers and states the explainer film draws.

Reads the run's own records (manifest.json, episodes.json, summary.json, events.jsonl) and writes one JSON
file. Nothing is recomputed that the pinned analyser already reports: the primary and safety contrasts and the
qualification verdict are copied from summary.json. Evaluator truth (roles, true and planted values) comes from
bench_v3.worlds and is checked against the manifest's world hashes.

    PYTHONPATH=researchers/dmarz/notes/discussion-dose/src \
      python3 researchers/dmarz/notes/discussion-dose/src/film_v3/build_data.py \
      data/discussion-v3/v3-q0-a1 data/discussion-v3/v3-q0-a1/film-data.json
"""
import json
import sys
from pathlib import Path

from bench_v3 import worlds

ARMS = ('independent', 'reports', 'private', 'board')
WORKED = 20001          # the world the film walks through, chosen as the first qualification id
QUOTE = {'arm': 'board', 'turn': 1, 'agent': 0,
         'text': 'Primary authority ranks secondary; C.power=13 fails minimum.'}


def belief(ballot, key, true, false):
    """What one ballot says about the contested fact."""
    if ballot is None: return 'invalid'
    claim = ballot['claims'].get(key)
    if claim is None: return 'none'
    return 'true' if claim['value'] == true else 'false' if claim['value'] == false else 'other'


def vote(ballot):
    if ballot is None: return '?'
    return ballot['vote'] if ballot['vote'] in ('A', 'B', 'C') else '-'


def parent_outcome(e):
    if e['parent_invalid']: return 'invalid'
    if e['parent_abstain']: return 'abstain'
    if e['parent_groundtruth_wrong']: return 'wrong'
    if e['parent_correct']: return 'correct'
    raise ValueError('unclassified parent outcome')


def stage(ballots, key, true, false):
    return {'beliefs': [belief(b, key, true, false) for b in ballots], 'votes': [vote(b) for b in ballots]}


def main(run_dir, out_path):
    run = Path(run_dir)
    manifest = json.loads((run / 'manifest.json').read_text())
    rows = json.loads((run / 'episodes.json').read_text())
    summary = json.loads((run / 'summary.json').read_text())
    audit = json.loads((run / 'audit.json').read_text())
    events = [json.loads(line) for line in (run / 'events.jsonl').read_text().splitlines()]
    if not audit['ok'] or summary['reconciliation']['missing']:
        raise SystemExit('run is not complete and audited; the film only draws finished runs')

    by_id = {r['id']: r for r in rows}
    strata = {a['world']: a['stratum'] for a in manifest['assignments'] if a['kind'] == 'swarm'}
    cases = {}
    for world in manifest['worlds']:
        case = worlds.make_case(world, strata[world])
        if worlds.digest(case) != manifest['world_hashes'][str(world)]:
            raise SystemExit(f'world {world} does not match the hash the run recorded')
        cases[world] = case

    def cell(world, attack, arm):
        case = cases[world]; key = case['target_key']
        true, false = case['truth'][key], case['false_value']
        r = by_id[f'{world}:{int(attack)}:{arm}']; e = r['evaluation']
        target = [m for m in r['memory'] if m['key'] == key]
        return {'final': stage(r['ballots'], key, true, false), 'decision': r['decision'],
                'rounds': [stage(t['ballots'], key, true, false) for t in r['trajectory'] if t['turn'] >= 1],
                'memory': {'records': len(r['memory']),
                           'target': None if not target else belief({'claims': {key: target[0]}}, key, true, false),
                           'target_value': target[0]['value'] if target else None},
                'parent': {'value': r['parent']['value'], 'outcome': parent_outcome(e),
                           'inherited_error': e['parent_inherited_error']},
                'vote_correct': e['vote_correct'], 'vote_invalid': e['vote_invalid'],
                'post_report_false': e['post_report_false_endorsements']}

    grid = {arm: [cell(w, True, arm) for w in manifest['worlds']] for arm in ARMS}
    clean = {arm: [cell(w, False, arm) for w in manifest['worlds']] for arm in ARMS}

    # the worked world, stage by stage
    case = cases[WORKED]; key = case['target_key']; true, false = case['truth'][key], case['false_value']
    owner = {doc: agent for agent, docs in enumerate(case['allocation']) for doc in docs}
    facts = []
    for doc in case['documents'] if isinstance(case['documents'], list) else case['documents'].values():
        if doc['id'] not in owner: continue
        for k, v in doc['facts'].items():
            planted = doc['id'] == case['attack_id']    # make_case lists the clean corpus; the attack swaps this one value
            facts.append({'key': k, 'value': case['false_value'] if planted else v, 'authority': doc['authority'],
                          'agent': owner[doc['id']], 'planted': planted})
    checkpoints = {(e['label'], e['stage']): e for e in events if e['kind'] == 'checkpoint'}
    initial = checkpoints[f'{WORKED}:1:acquisition', 'private_initial']
    reports = checkpoints[f'{WORKED}:1:report_snapshot', 'reports']
    posts = [p for e in events if e['kind'] == 'delivery' and e['label'] == f'{WORKED}:1:{QUOTE["arm"]}'
             for p in e['posts'] if p['turn'] == QUOTE['turn'] and p['agent'] == QUOTE['agent']]
    if not posts or QUOTE['text'] not in posts[0]['message']:
        raise SystemExit('the quoted sentence is not in the recorded post')
    worked = {'world': WORKED, 'family': case['family'], 'instructions': case['task']['instructions'],
              'truth': case['truth'], 'facts': facts, 'roles': case['roles'], 'target': case['target'],
              'key': key, 'true': true, 'false': false, 'delta': case['delta'], 'truth_answer': true + case['delta'],
              'winner': by_id[f'{WORKED}:0:board']['decision'],
              'initial': stage(initial['ballots'], key, true, false),
              'reports': stage(reports['ballots'], key, true, false),
              'arms': {arm: cell(WORKED, True, arm) for arm in ARMS}, 'quote': QUOTE}

    def tally(cells, pick):
        return sum(1 for c in cells if pick(c))
    attacked = {arm: {o: tally(grid[arm], lambda c, o=o: c['parent']['outcome'] == o)
                      for o in ('wrong', 'correct', 'abstain', 'invalid')} for arm in ARMS}
    out = {
        'run': {'id': 'discussion-dose-v3/v3-q0-a1', 'model': manifest['model_config']['model'],
                'rounds': manifest['rounds'], 'created_utc': manifest['created_utc'],
                'calls': summary['reconciliation']['physical_model_calls'],
                'cases': summary['reconciliation']['terminal'],
                'input_tokens': summary['reconciliation']['input_tokens'],
                'output_tokens': summary['reconciliation']['output_tokens'],
                'cost_usd': round(sum(g['estimated_cost_usd'] for g in summary['resources'].values()), 2),
                'journal_events': audit['journal_events'], 'audit_ok': audit['ok']},
        'worlds': [{'id': w, 'family': cases[w]['family'], 'stratum': strata[w]} for w in manifest['worlds']],
        'worked': worked, 'grid': grid,
        'attacked': attacked,
        'clean': {arm: {'vote_correct': tally(clean[arm], lambda c: c['vote_correct']),
                        'parent_wrong': tally(clean[arm], lambda c: c['parent']['outcome'] == 'wrong')}
                  for arm in ARMS},
        'spread': {'majority_false_after_reports': tally(grid['reports'], lambda c: c['post_report_false'] >= 2),
                   'false_after_reports': [c['post_report_false'] for c in grid['reports']]},
        'final_false_ballots': {arm: sum(c['final']['beliefs'].count('false') for c in grid[arm]) for arm in ARMS},
        'invalid_ballots': sum(c['vote_invalid'] for arm in ARMS for c in grid[arm] + clean[arm]),
        'primary': {'mean': summary['primary']['mean'],
                    'per_world': [{'world': p['world'], 'contrast': p['contrast']} for p in summary['primary']['per_world']]},
        'safety': {'mean': summary['safety']['mean'],
                   'per_world': [{'world': p['world'], 'contrast': p['contrast']} for p in summary['safety']['per_world']]},
        'qualification': {k: summary['qualification'][k] for k in
                          ('clean_full_evidence_correct', 'clean_reports_correct', 'required_each', 'assigned_each',
                           'competence_screen_pass', 'model_qualified', 'execution_complete')},
    }
    Path(out_path).write_text(json.dumps(out, indent=1, sort_keys=True) + '\n')
    print(json.dumps({k: out[k] for k in ('attacked', 'clean', 'spread', 'final_false_ballots', 'primary', 'qualification')}))


if __name__ == '__main__':
    main(*sys.argv[1:3])
