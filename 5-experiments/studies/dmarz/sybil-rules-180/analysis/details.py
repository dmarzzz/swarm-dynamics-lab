"""Descriptive details for RESULTS.md: round-by-round adoption in each continuation, paired net profit of the same
owners across continuations, messages and memos. Reads only the records; imports analysis/recompute.py.

    python3 analysis/details.py <results dir of the run>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recompute as rc


def main():
    root = Path(sys.argv[1])
    s1 = next(p for p in root.glob('*s1-*') if p.is_dir())
    recs = rc.rows(s1 / 'rounds.jsonl.gz')
    calls = {c['call_id']: c for c in rc.rows(s1 / 'calls.jsonl.gz')}
    by = {}
    for r in recs:
        by.setdefault(r['label'], []).append(r)
    out = {'timeline': {}, 'net': {}, 'firsts': {}}
    masked = {}
    for label, rs in by.items():
        rs.sort(key=lambda r: (r['round'], r['market']))
        series = {}
        tl = {}
        first = {}
        for r in rs:
            start = {o: None for o in r['owners']}
            row = tl.setdefault(r['round'], {'same_product_register': 0, 'other_product_register': 0, 'transfer_firm_to_firm': 0,
                                             'transfer_from_reserve': 0, 'producing_two_same_product': 0, 'mask_flag': 0,
                                             'rejected': 0, 'void': 0})
            for oid, x in r['owners'].items():
                own_prod = {f['product'] for f in r['firms'] if f['owner'] == oid and f['id'] != x.get('registered_firm')}
                a = x['admin']
                if x['admin_result'] == 'accepted' and a['command'] == 'register':
                    g = 'AB'.index(a['product'])
                    same = any(f['product'] == g and f['owner'] == oid and f['id'] != x.get('registered_firm') for f in r['firms'])
                    row['same_product_register' if same else 'other_product_register'] += 1
                    if same:
                        first.setdefault(oid, {}).setdefault('same_register', r['round'])
                if x['admin_result'] == 'accepted' and a['command'] == 'transfer':
                    row['transfer_from_reserve' if a['from'] == 'reserve' else 'transfer_firm_to_firm'] += 1
                    if a['from'] != 'reserve':
                        first.setdefault(oid, {}).setdefault('firm_transfer', r['round'])
                if max(x['producing_firms']) >= 2:
                    row['producing_two_same_product'] += 1
                    first.setdefault(oid, {}).setdefault('productive_split', r['round'])
                flags = rc.mask_flags(r, oid, x)
                if any(flags):
                    row['mask_flag'] += 1
                    first.setdefault(oid, {}).setdefault('mask', r['round'])
                row['rejected'] += str(x['admin_result']).startswith('rejected')
                row['void'] += x['status'] != 'accepted'
                series.setdefault(oid, []).append((r['round'], flags))
        out['timeline'][label] = tl
        m = {o for o, s in series.items() if rc.sustained(s)}
        masked[label] = m
        # round at which the 3-round streak is first reached
        reach = {}
        for o in m:
            for g in (0, 1):
                run, last = 0, None
                for rnd, fl in series[o]:
                    run = run + 1 if fl[g] and last is not None and rnd == last + 1 and run > 0 else (1 if fl[g] else 0)
                    last = rnd
                    if run >= 3:
                        reach[o] = min(reach.get(o, 99), rnd)
                        break
        out['firsts'][label] = {k: sorted(v.get(k) for v in first.values() if v.get(k) is not None) for k in
                                ('same_register', 'firm_transfer', 'productive_split', 'mask')}
        out['firsts'][label]['sustained_reached'] = sorted(reach.values())
        net = {}
        fees = {}
        for r in rs:
            for oid, x in r['owners'].items():
                net[oid] = net.get(oid, 0) + x['net']
                f = fees.setdefault(oid, [0, 0, 0])
                f[0] += x['fee']; f[1] += x['overhead']; f[2] += sum(x['charge'])
        out['net'][label] = {'net': net, 'fees_overhead_charges': fees}
    # paired comparison: owners masking in A, their net in A versus B and C (same checkpoint, same shocks)
    comp = {}
    for label in ('A', 'A2'):
        group = masked[label]
        comp[label] = {}
        for other in ('B', 'C'):
            d = [out['net'][label]['net'][o] - out['net'][other]['net'][o] for o in group]
            comp[label][other] = {'owners': len(d), 'mean_net_difference': sum(d) / len(d), 'positive': sum(x > 0 for x in d),
                                  'min': min(d), 'max': max(d)}
        fo = [out['net'][label]['fees_overhead_charges'][o] for o in group]
        fb = [out['net']['B']['fees_overhead_charges'][o] for o in group]
        comp[label]['costs_mean'] = {label: [sum(x[i] for x in fo) / len(fo) for i in range(3)], 'B': [sum(x[i] for x in fb) / len(fb) for i in range(3)]}
    out['paired_net'] = comp
    msgs = [(c['call_id'], (c.get('answer') or {}).get('message')) for c in calls.values() if (c.get('answer') or {}).get('message')]
    out['messages'] = sorted(msgs)
    del out['net']
    print(json.dumps(out, indent=1, sort_keys=True, default=str))


if __name__ == '__main__':
    main()
