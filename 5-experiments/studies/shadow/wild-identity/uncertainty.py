#!/usr/bin/env python3
"""Post-hoc paired page-cluster bootstrap; see UNCERTAINTY-PLAN.md."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import random

from analyze import added_text, digest, matcher, references, rows


def quantile(values, p):
    a = sorted(values)
    if not a:
        raise ValueError('No valid replicates')
    index = (len(a) - 1) * p
    lo = int(index)
    return a[lo] + (a[min(lo + 1, len(a) - 1)] - a[lo]) * (index - lo)


def metrics(totals):
    n, snapshot, fresh = totals
    if n <= 0 or fresh <= 0:
        raise ValueError('Zero denominator')
    return {'snapshot_fraction': snapshot / n, 'fresh_fraction': fresh / n,
            'difference': (snapshot - fresh) / n, 'ratio': snapshot / fresh}


def resample(pages, repetitions, seed):
    if repetitions < 2 or len(pages) < 2:
        raise ValueError('Need at least two pages and replicates')
    totals = [sum(p[i] for p in pages) for i in range(3)]
    point = metrics(totals)
    rng = random.Random(seed)
    draws = {key: [] for key in point}
    rejected = 0
    for _ in range(repetitions):
        counts = [0, 0, 0]
        for _ in pages:
            page = pages[rng.randrange(len(pages))]
            for i in range(3):
                counts[i] += page[i]
        try:
            result = metrics(counts)
        except ValueError:
            rejected += 1
            continue
        for key in draws:
            draws[key].append(result[key])
    leave_one_out = []
    leave_one_out_rejected = 0
    for page in pages:
        try:
            leave_one_out.append(metrics([totals[i] - page[i] for i in range(3)]))
        except ValueError:
            leave_one_out_rejected += 1
    return {'seed': seed, 'replicates_requested': repetitions,
            'replicates_valid': repetitions - rejected, 'replicates_rejected': rejected,
            'pages': len(pages), 'totals': dict(zip(['attributed', 'snapshot', 'fresh'], totals)),
            'point': point,
            'conditional_95pct_ci': {key: [quantile(v, .025), quantile(v, .975)] for key, v in draws.items()},
            'leave_one_page_out_range': {key: [min(r[key] for r in leave_one_out), max(r[key] for r in leave_one_out)] for key in point} if leave_one_out else {},
            'leave_one_out_rejected': leave_one_out_rejected}


def figure(result, out):
    point, ci = result['point'], result['conditional_95pct_ci']
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="660" viewBox="0 0 1800 660">',
             '<rect width="1800" height="660" fill="#fafaf7"/>',
             '<g font-family="sans-serif" fill="#222">',
             '<text x="90" y="85" font-size="38">Retained text inflates observable name-reference activity</text>',
             '<text x="90" y="130" font-size="23">Paired page-cluster bootstrap, 2,000 resamples. Conditional 95% CIs, not causal effects.</text>']
    left, width = 580, 1000
    for pct in range(0, 61, 10):
        x = left + width * pct / 60
        parts.append(f'<path d="M{x} 175V400" stroke="#d5d5cf"/><text x="{x-22}" y="440" font-size="22">{pct}%</text>')
    for key, title, color, y in [('snapshot_fraction', 'Retained full-page text', '#be5836', 240), ('fresh_fraction', 'Inserted/replaced hunk text', '#217766', 345)]:
        value = point[key]
        lo, hi = ci[key]
        x, a, b = [left + width * v / .6 for v in [value, lo, hi]]
        parts.append(f'<text x="90" y="{y+7}" font-size="26">{title}</text><path d="M{a} {y}H{b}M{a} {y-12}V{y+12}M{b} {y-12}V{y+12}" stroke="{color}" stroke-width="5"/><circle cx="{x}" cy="{y}" r="9" fill="{color}"/><text x="{b+22}" y="{y+7}" font-size="23">{value*100:.2f}%</text>')
    parts.extend(['<text x="580" y="487" font-size="24">Attributed revisions containing at least one non-self known-label reference</text>',
                  f'<text x="90" y="550" font-size="25">{result["pages"]:,} page clusters; {result["totals"]["attributed"]:,} attributed revisions. Same labels and matcher in both views.</text>',
                  '<text x="90" y="595" font-size="23">Unverified independent-page assumption. Cross-page copying and shared actors can invalidate coverage.</text>',
                  '</g></svg>'])
    out.write_text('\n'.join(parts) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True, type=Path)
    parser.add_argument('--results', required=True, type=Path)
    args = parser.parse_args()
    source = args.data / 'collusion-wiki/revisions.jsonl.gz'
    summary = json.loads((args.results / 'summary.json').read_text())
    if digest(source) != summary['input_sha256']['collusion-wiki/revisions.jsonl.gz']:
        raise ValueError('Source hash differs from frozen census')
    data = list(rows(source))
    regex = matcher(r['label'] for r in data if r.get('label'))
    pages = collections.defaultdict(lambda: [0, 0, 0])
    for r in data:
        actor = r.get('label')
        if not actor:
            continue
        counts = pages[r['page_id']]
        counts[0] += 1
        counts[1] += bool(references(regex, r.get('body', ''), actor))
        counts[2] += bool(references(regex, added_text(r), actor))
    ordered = sorted(pages.items())
    result = resample([v for _, v in ordered], 2000, 20261004)
    expected = {'attributed': summary['wiki']['attributed_events'],
                'snapshot': summary['wiki']['graphs']['snapshot']['referencing_events'],
                'fresh': summary['wiki']['graphs']['fresh']['referencing_events']}
    if result['totals'] != expected:
        raise ValueError('Supplement does not reconcile to frozen census')
    result['design'] = 'Post-hoc saved-data report, paired page-cluster bootstrap'
    result['ci_interpretation'] = 'Conditional model-based 95% percentile CIs assume exchangeable independent pages. Within-page dependence preserved; cross-page dependence not modeled. No guaranteed coverage for unseen agents, other archives or causal effects.'
    result['input_sha256'] = {'revisions': digest(source), 'summary': digest(args.results / 'summary.json'), 'script': digest(Path(__file__))}
    with (args.results / 'page-reference-aggregates.csv').open('w') as f:
        writer = csv.writer(f)
        writer.writerow(['page_digest', 'attributed_revisions', 'snapshot_reference_revisions', 'fresh_reference_revisions'])
        for page, counts in ordered:
            writer.writerow([hashlib.sha256(('wiki-page:' + page).encode()).hexdigest()[:16], *counts])
    (args.results / 'uncertainty.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    figure(result, args.results / 'reference-uncertainty.svg')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
