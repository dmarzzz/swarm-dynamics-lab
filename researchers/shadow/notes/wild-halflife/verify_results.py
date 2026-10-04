#!/usr/bin/env python3
"""Same-author reference arithmetic, independent grouping but shared source loaders.

Checks reach and conditional medians for all 12 baseline combinations. Does not
independently audit extraction, source truth, bootstrap or KM assumptions.
"""
import argparse
import json
from pathlib import Path
import statistics

import numpy as np
import halflife as H


def reference(records, kind, identity):
    by_unit = {}
    for record in records:
        actor = record[identity]
        if actor is None:
            continue
        for unit in record['units'][kind]:
            people = by_unit.setdefault(unit, {})
            people[actor] = min(people.get(actor, float('inf')), record['t'])
    clock = sorted(r['t'] for r in records)
    waits, wall = [], []
    reached = {2: 0, 5: 0}
    for people in by_unit.values():
        times = sorted(people.values())
        for k in reached:
            reached[k] += len(people) >= k
        if len(people) >= 2:
            first, second = times[:2]
            waits.append(int(np.searchsorted(clock, second, side='left') -
                             np.searchsorted(clock, first, side='left')))
            wall.append((second-first)/3600.)
    return dict(units=len(by_unit), units_ge2=reached[2], units_ge5=reached[5],
                median_activity=statistics.median(waits), median_wall_h=statistics.median(wall))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', required=True)
    ap.add_argument('--repo', required=True)
    ap.add_argument('--results', required=True)
    args = ap.parse_args()
    folder = Path(args.results)
    summary = json.loads((folder/'summary.json').read_text())
    assert H.sha256_file(Path(args.data)/'revisions.jsonl.gz') == summary['inputs']['wiki']['sha256']
    records = {'wiki': H.load_wiki(args.data)[0],
               'git': H.load_git(args.repo, summary['inputs']['git']['rev'])[0]}
    checks = []
    for source, rows in records.items():
        for who in ('a', 'b'):
            for kind in ('url', 'line', 'host'):
                ref = reference(rows, kind, who)
                saved = summary[source][who.upper()][kind]
                for k in ('units', 'units_ge2', 'units_ge5'):
                    assert ref[k] == saved[k], (source, who, kind, k)
                assert ref['median_activity'] == saved['activity']['cond_median_time_to_2nd']
                assert ref['median_wall_h'] == saved['wall_h']['cond_median_time_to_2nd']
                checks.append(dict(source=source, identity=who.upper(), kind=kind,
                                   expected=ref, passed=True))
    result = dict(status='12/12 reference checks passed', independence='same author; shared loaders',
                  limits='No independent extraction/source-truth audit; no causal assumptions validated',
                  checks=checks)
    (folder/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'])


if __name__ == '__main__':
    main()
