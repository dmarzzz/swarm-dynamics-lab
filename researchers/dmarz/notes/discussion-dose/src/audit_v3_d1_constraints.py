"""Separate direct arithmetic check for the six already-open D1 worlds."""
import argparse
import json
from pathlib import Path
from bench_v3.worlds import make_case


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('output', type=Path)
    args = p.parse_args()
    rows = []
    for world in range(20001, 20007):
        case = make_case(world, 'resolvable' if world <= 20003 else 'ambiguous')
        task = case['task']; rules = task['rules']; options = []
        for option in ('A', 'B', 'C'):
            facts = {k.split('.')[1]: v for k, v in case['truth'].items() if k.startswith(option + '.')}
            if case['family'] == 'capacity':
                checks = {'sufficient_power': facts['power'] >= rules['power_min'],
                          'within_access_limit': facts['access'] <= rules['access_max']}
                eligible = all(checks.values())
            elif case['family'] == 'total_cost':
                checks = {'within_budget': facts['base'] + facts['freight'] <= rules['budget'],
                          'within_deadline': facts['days'] <= rules['deadline']}
                eligible = all(checks.values())
            else:
                checks = {'sufficient_direct': facts['direct'] >= rules['required'],
                          'backup_and_transfer': facts['backup'] == 1 and facts['transfer'] <= rules['transfer_max']}
                eligible = any(checks.values())
            options.append({'option': option, 'facts': facts, 'checks': checks, 'feasible': eligible})
        feasible = [o['option'] for o in options if o['feasible']]
        assert len(feasible) == 1
        rows.append({'world': world, 'family': case['family'], 'rules': rules,
                     'options': options, 'unique_feasible_winner': feasible[0]})
    result = {'scope': 'Six open D1 worlds only; no new qualification or holdout IDs generated.',
              'method': 'Direct comparisons, no call to production feasible/reference_winner. Same owner audit, not independent researcher review.',
              'worlds': rows}
    with args.output.open('x') as stream:
        json.dump(result, stream, sort_keys=True, indent=2); stream.write('\n')
    print(json.dumps({'worlds': 6, 'options_checked': 18, 'unique_winners': [r['unique_feasible_winner'] for r in rows]}))


if __name__ == '__main__':
    main()
