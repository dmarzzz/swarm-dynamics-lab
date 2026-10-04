#!/usr/bin/env python3
"""Saved-data-only analysis; never makes model calls."""
import csv
import json
from pathlib import Path
import random
import statistics
import successor_run as r

ROOT = Path(__file__).resolve().parent

def ci(values):
    if not values:
        return [None, None]
    rng = random.Random(20261004)
    boots = sorted(statistics.mean(rng.choices(values, k=len(values))) for _ in range(10000))
    return [boots[249], boots[9749]]


def analyze():
    data = json.loads((ROOT / 'input.json').read_text())
    rows = r.read_journal()
    starts = [x for x in rows if x['event'] == 'start']
    terminals = [x for x in rows if x['event'] == 'terminal']
    assert len(starts) == len({x['id'] for x in starts})
    assert len(terminals) == len({x['id'] for x in terminals})
    assert {x['id'] for x in terminals} <= {x['id'] for x in starts}
    terminal = {x['id']: x for x in terminals}
    hs = {h['id']: h for h in data['histories']}
    scored = []
    for a in data['assignments']:
        h = hs[a['history']]
        t = terminal.get(a['id'], {})
        s = r.score(t.get('response', {}))
        scored.append({'id': a['id'], 'history': a['history'], 'stage': a['stage'], 'representation': a['representation'],
                       'order': a['order'], 'length': len(h['events']), 'majority': h['majority'], 'last': h['events'][-1],
                       'conflict': h['conflict'], 'started': a['id'] in {x['id'] for x in starts}, 'terminal': bool(t),
                       'valid': s['valid'], 'reason': None if s['valid'] else t.get('error', s['reason']),
                       'choice': s.get('choice'), 'p_majority': s['p'][h['majority']] if s['valid'] else None,
                       'p_last': s['p'][h['events'][-1]] if s['valid'] else None, 'mass': s.get('mass')})
    costs = [(t.get('response', {}).get('usage') or {}).get('cost') for t in terminals]
    by = {(x['history'], x['representation'], x['order']): x for x in scored if x['stage'] == 'S1'}
    scientific = [h for h in data['histories'] if h['stage'] == 'S1']
    contrasts = {}
    for name, rep, order, absolute in [('primary_abs_raw_reverse_minus_chrono', 'raw', 'reversed', True),
                                       ('abs_raw_shuffle_minus_chrono', 'raw', 'shuffled', True),
                                       ('signed_summary_chrono_minus_raw_chrono', 'summary', 'chronological', False)]:
        values = []
        for h in scientific:
            baseline = by[h['id'], 'raw', 'chronological']
            treatment = by[h['id'], rep, order]
            if baseline['valid'] and treatment['valid']:
                diff = treatment['p_majority'] - baseline['p_majority']
                values.append(abs(diff) if absolute else diff)
        contrasts[name] = {'n_histories': len(values), 'mean': statistics.mean(values) if values else None, 'ci95': ci(values)}
        if absolute:
            contrasts[name]['all_assigned_missingness_bounds'] = [sum(values) / 24, (sum(values) + (24 - len(values))) / 24]
    conditions = []
    for rep, order in r.r.CONDITIONS:
        rs = [x for x in scored if x['stage'] == 'S1' and x['representation'] == rep and x['order'] == order]
        valid = [x for x in rs if x['valid']]
        conditions.append({'representation': rep, 'order': order, 'assigned_histories': len(rs), 'valid_histories': len(valid),
                           'mean_p_majority': statistics.mean(x['p_majority'] for x in valid) if valid else None,
                           'mean_p_last': statistics.mean(x['p_last'] for x in valid) if valid else None,
                           'majority_choices': sum(x['choice'] == x['majority'] for x in valid),
                           'last_choices': sum(x['choice'] == x['last'] for x in valid)})
    summary = {'model': r.r.MODEL, 'independent_unit': 'synthetic frozen history', 'qualification': r.qualify(data, rows),
               'assigned': len(scored), 'started': len(starts), 'terminal': len(terminals),
               'valid': sum(x['valid'] for x in scored), 'scientific_assigned_histories': 24,
               'scientific_valid_calls': sum(x['valid'] for x in scored if x['stage'] == 'S1'),
               'actual_reported_usd': sum(float(x) for x in costs if x is not None),
               'actual_total_usd': sum(float(x) for x in costs) if costs and all(x is not None for x in costs) and len(starts) == len(terminals) else None,
               'terminal_cost_unknown': sum(x is None for x in costs), 'ambiguous_started': len(starts) - len(terminals),
               'retained_reservations_usd': sum(x['reservation_usd'] for x in starts), 'cap_usd': r.CAP,
               'contrasts': contrasts, 'conditions': conditions, 'input_sha256': r.r.digest((ROOT / 'input.json').read_bytes()),
               'journal_sha256': r.r.digest((ROOT / 'results-r2/journal.jsonl').read_bytes())}
    summary['strata'] = []
    for length in (16, 64, 256):
        for conflict in (False, True):
            for rep, order in r.r.CONDITIONS:
                group = [x for x in scored if x['stage'] == 'S1' and x['length'] == length
                         and x['conflict'] == conflict and x['representation'] == rep and x['order'] == order]
                valid = [x for x in group if x['valid']]
                summary['strata'].append({'length': length, 'conflict': conflict, 'representation': rep, 'order': order,
                                         'assigned_histories': len(group), 'valid_histories': len(valid),
                                         'mean_p_majority': statistics.mean(x['p_majority'] for x in valid) if valid else None,
                                         'mean_p_last': statistics.mean(x['p_last'] for x in valid) if valid else None,
                                         'majority_choices': sum(x['choice'] == x['majority'] for x in valid),
                                         'last_choices': sum(x['choice'] == x['last'] for x in valid)})
    out = ROOT / 'results-r2'
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    with (out / 'scored.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(scored[0]))
        writer.writeheader()
        writer.writerows(scored)
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1050" viewBox="0 0 1600 1050">',
           '<rect width="1600" height="1050" fill="#f7f5ef"/>',
           '<g font-family="monospace" fill="#222"><text x="35" y="40" font-size="24">Frozen histories: P(majority name), gpt-4o-mini</text>',
           '<text x="35" y="70" font-size="16">Each row is ONE planned history. Synthetic diagnostic, not a swarm replication. Cross = invalid/missing.</text>']
    if not any(x['valid'] for x in scored if x['stage'] == 'S1'):
        svg.append('<text x="35" y="975" font-size="20" fill="#a22">NO SCIENTIFIC MODEL OBSERVATIONS. Qualification blocked; all scientific cells are unstarted.</text>')
    for j, (rep, order) in enumerate(r.r.CONDITIONS):
        x = 245 + j * 220
        svg.append(f'<text x="{x}" y="105" font-size="14">{rep}/{order}</text>')
        svg.append(f'<text x="{x}" y="126" font-size="12">0                  1</text>')
    for i, h in enumerate(scientific):
        y = 160 + i * 33
        svg.append(f'<text x="25" y="{y+4}" font-size="14">{h["id"]} n={len(h["events"])} last={"conflict" if h["conflict"] else "match"}</text>')
        for j, (rep, order) in enumerate(r.r.CONDITIONS):
            x = 245 + j * 220
            s = by[h['id'], rep, order]
            svg.append(f'<line x1="{x}" x2="{x+180}" y1="{y}" y2="{y}" stroke="#ccc"/>')
            if s['valid']:
                px = x + 180 * s['p_majority']
                svg.append(f'<circle cx="{px:.3f}" cy="{y}" r="5" fill="#265c7a"><title>{s["id"]}: {s["p_majority"]:.9f}</title></circle>')
            else:
                svg.append(f'<text x="{x+90}" y="{y+5}" fill="#a22">x</text>')
    svg += ['<text x="35" y="1010" font-size="14">Indexed chronology and last-event metadata preserved across every representation. Summary includes exact positions.</text>', '</g></svg>']
    (out / 'paired-history.svg').write_text('\n'.join(svg))
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    analyze()
