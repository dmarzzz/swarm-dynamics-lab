#!/usr/bin/env python3
"""Owner audit: replay saved actions, including terminal failures, without model calls."""
import argparse
import json
from pathlib import Path
import sys


def audit(root, base, attempt):
    sys.path.insert(0, str(Path(root) / 'src'))
    import common
    import sim
    from provider import CallFailure
    totals = {'attempt': attempt, 'bundles': 0, 'episodes': 0, 'valid_episodes': 0,
              'invalid_episodes': 0, 'matched_calls': 0, 'recorded_rounds': 0, 'failure_causes': []}
    for folder in sorted(Path(base).iterdir()):
        if not (folder / 'summary.json').is_file():
            continue
        summary = json.loads((folder / 'summary.json').read_text())
        if summary['params']['attempt_id'] != attempt:
            continue
        for key, value in common.hashes().items():
            assert summary['params'][key] == value, 'frozen_source_mismatch'
        rows = [json.loads(line) for line in (folder / 'calls.jsonl').read_text().splitlines()]
        records = [json.loads(line) for line in (folder / 'episodes.jsonl').read_text().splitlines()]
        for record in records:
            calls = {c['round']: c for c in rows if c['arm'] == record['arm']}
            assert len(calls) == record['model_calls']

            def policy(observation, arm):
                call = calls[observation['round']]
                assert call['observation'] == observation
                assert set(observation) == {'round', 'market', 'portfolio', 'rules',
                                            'last_competitor_outputs', 'history', 'legal_operations'}
                if call['status'] != 'ok':
                    # A structured final response may be present; validate it to expose the exact cause.
                    if call['status'] == 'invalid_structured_answer':
                        action = json.loads(call['accounting']['response_text'])
                        try:
                            sim.validate(action, observation)
                        except ValueError as exc:
                            totals['failure_causes'].append({'call_id': call['call_id'], 'reason': str(exc)})
                        else:
                            raise AssertionError('saved_invalid_action_now_valid')
                    raise CallFailure(call['status'], call['accounting'])
                trace = record['trace'][observation['round'] - 1]
                assert call['action'] == trace['action']
                assert sim.digest(observation) == trace['observation_sha256']
                return call['action']

            reproduced = sim.run_episode(record['task_id'], record['seed'], record['world'],
                                         record['dose'], [record['arm']], record['cfg'], policy)[0]
            for key in ('trace', 'evaluation', 'validity', 'draws_sha256'):
                assert reproduced[key] == record[key], f'exact_replay_mismatch:{key}'
            totals['episodes'] += 1
            totals['valid_episodes' if record['validity']['ok'] else 'invalid_episodes'] += 1
            totals['matched_calls'] += len(calls)
            totals['recorded_rounds'] += len(record['trace'])
        totals['bundles'] += 1
    assert totals['episodes'], 'no_matching_records'
    totals['scope'] = 'Exact deterministic replay in the pinned runtime; same-author audit, no model calls or independent researcher review.'
    print(json.dumps(totals, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('root'); p.add_argument('base'); p.add_argument('attempt')
    a = p.parse_args()
    audit(a.root, a.base, a.attempt)
