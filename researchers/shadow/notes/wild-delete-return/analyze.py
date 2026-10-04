#!/usr/bin/env python3
"""Bounded offline deletion-return diagnostic. Source bodies are never interpreted."""
import argparse
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import random
import statistics

HORIZONS = (300, 1800, 3600)
GUARD = 60
EXPECTED = {
 'events.jsonl.gz': '989780118de3dc05031ee5920a761c565a97b64d3721688593adc0794fcfb7b8',
 'revisions.jsonl.gz': '9c2a4ef0ccbfb5b42be8422342a6bd3a389a4a047bc891e3148354dd65b63c96',
}


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def timestamp(value):
    if value is None or value == '':
        return None
    t = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if t.tzinfo is None:
        raise ValueError('Unzoned timestamp')
    return t.timestamp()


def utc(t):
    return datetime.fromtimestamp(t, timezone.utc).isoformat().replace('+00:00', 'Z') if t is not None else None


def clock_reason(row):
    if timestamp(row.get('time')) is None:
        return 'missing_time'
    if row.get('time_grade') not in ('reqlog', 'rclog'):
        return 'ineligible_time_grade'
    value = row.get('uncertainty_seconds')
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 1:
        return 'ineligible_uncertainty'
    return None


def rows(path):
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        for line in stream:
            yield json.loads(line)


def select_assignments(events, revisions):
    event_ids, revision_ids = set(), set()
    deletes = defaultdict(list)
    saves = defaultdict(list)
    quality = Counter()
    event_kinds = Counter()
    for row in events:
        ident = row.get('event_id')
        if not ident or ident in event_ids:
            raise ValueError('Missing/duplicate event id')
        event_ids.add(ident)
        event_kinds[row.get('event_type')] += 1
        if row.get('event_type') != 'delete' or row.get('success_observed') is not True:
            continue
        quality['successful_delete_events'] += 1
        if not row.get('page_key'):
            quality['successful_delete_missing_page_key'] += 1
            continue
        deletes[row['page_key']].append({k: row.get(k) for k in (
            'event_id', 'page_key', 'time', 'time_grade', 'uncertainty_seconds')})
    for row in revisions:
        ident = row.get('rev_id')
        if not ident or ident in revision_ids:
            raise ValueError('Missing/duplicate revision id')
        revision_ids.add(ident)
        if not row.get('page_key'):
            quality['revision_missing_page_key'] += 1
            continue
        reason = clock_reason(row)
        if reason:
            quality['revision_' + reason] += 1
            continue
        saves[row['page_key']].append(timestamp(row['time']))
        quality['admissible_revision_rows'] += 1
    for values in saves.values():
        values.sort()
    all_times = [t for values in saves.values() for t in values]
    if not all_times:
        raise ValueError('No admissible revision timestamps: blocked')
    low, high = min(all_times), max(all_times)
    assignments = []
    for page, candidates in deletes.items():
        missing = any(timestamp(e.get('time')) is None for e in candidates)
        if missing:
            chosen = min(candidates, key=lambda e: e['event_id'])
            reason = 'unknown_first_deletion_missing_time'
            t = None
        else:
            chosen = min(candidates, key=lambda e: (timestamp(e['time']), e['event_id']))
            t = timestamp(chosen['time'])
            reason = clock_reason(chosen)
        if reason is None and not (low <= t - 1800 and t + 1800 <= high):
            reason = 'primary_release_edge'
        a = {'page_sha256': hashlib.sha256(page.encode()).hexdigest(),
             'first_delete_time': utc(t), 'deletion_day': utc(t)[:10] if t is not None else None,
             'successful_delete_events_for_page': len(candidates),
             'eligible': reason is None, 'exclusion': reason, 'windows': {}}
        if reason is None:
            values = saves.get(page, [])
            quality['primary_pages_with_any_admissible_revision'] += bool(values)
            for horizon in HORIZONS:
                label = str(horizon)
                if not (low <= t - horizon and t + horizon <= high):
                    a['windows'][label] = {'eligible': False, 'exclusion': 'secondary_release_edge'}
                    continue
                before = bisect_left(values, t - GUARD) - bisect_left(values, t - horizon)
                after_begin = bisect_right(values, t + GUARD)
                after_end = bisect_right(values, t + horizon)
                after = after_end - after_begin
                a['windows'][label] = {
                    'eligible': True, 'before': before, 'after': after, 'difference': after-before,
                    'any_return': after > 0,
                    'first_return_latency_seconds': values[after_begin]-t if after else None,
                }
        assignments.append(a)
    assignments.sort(key=lambda a: a['page_sha256'])
    return assignments, {'event_rows': len(event_ids), 'event_kinds': dict(sorted(event_kinds.items())),
        'revision_rows': len(revision_ids), 'quality_counts': dict(sorted(quality.items())),
        'selected_pages': len(assignments),
        'eligible_primary_pages': sum(a['eligible'] for a in assignments),
        'exclusion_counts': dict(sorted(Counter(a['exclusion'] for a in assignments if not a['eligible']).items())),
        'admissible_revision_time_range': [utc(low), utc(high)]}


def quantile(values, q):
    position = (len(values)-1)*q
    lower = int(position)
    upper = min(lower+1, len(values)-1)
    return values[lower] + (values[upper]-values[lower])*(position-lower)


def summarize(assignments, accounting):
    output = {'accounting': accounting, 'window_results': {}, 'model_calls': 0, 'cost_usd': 0,
              'claim_boundary': 'Paired observed write counts, not causal suppression, content restoration or agent identity.'}
    for horizon in HORIZONS:
        entries = [(a, a['windows'].get(str(horizon), {})) for a in assignments if a['eligible']]
        entries = [(a,w) for a,w in entries if w.get('eligible')]
        before = sum(w['before'] for _,w in entries)
        after = sum(w['after'] for _,w in entries)
        daily = defaultdict(lambda: {'pages': 0, 'before': 0, 'after': 0, 'any_return': 0})
        for a,w in entries:
            d = daily[a['deletion_day']]
            d['pages'] += 1
            d['before'] += w['before']
            d['after'] += w['after']
            d['any_return'] += w['any_return']
        n = len(entries)
        result = {'pages': n, 'before': before, 'after': after,
                  'mean_after_minus_before': (after-before)/n if n else None,
                  'after_before_ratio': after/before if before else None,
                  'pages_with_return': sum(w['any_return'] for _,w in entries),
                  'return_fraction': sum(w['any_return'] for _,w in entries)/n if n else None,
                  'pages_increased': sum(w['difference'] > 0 for _,w in entries),
                  'pages_unchanged': sum(w['difference'] == 0 for _,w in entries),
                  'pages_decreased': sum(w['difference'] < 0 for _,w in entries),
                  'median_return_latency_given_return': statistics.median([w['first_return_latency_seconds'] for _,w in entries if w['any_return']]) if any(w['any_return'] for _,w in entries) else None,
                  'deletion_day_clusters': len(daily), 'daily': dict(sorted(daily.items()))}
        if horizon == 1800:
            result['status'] = 'descriptive_pilot' if n >= 10 else 'feasibility_only'
            result['day_cluster_bootstrap_95_interval'] = None
            if len(daily) >= 5 and n >= 10:
                groups = [daily[day] for day in sorted(daily)]
                rng = random.Random(20261004)
                contrasts = []
                for _ in range(5000):
                    sample = [rng.choice(groups) for _ in groups]
                    contrasts.append(sum(d['after']-d['before'] for d in sample)/sum(d['pages'] for d in sample))
                contrasts.sort()
                result['day_cluster_bootstrap_95_interval'] = [quantile(contrasts, .025), quantile(contrasts, .975)]
                result['bootstrap'] = {'seed': 20261004, 'draws': 5000, 'unit': 'observed deletion UTC day',
                    'interpretation': 'Resampling variation among observed days, not a causal or population interval'}
        output['window_results'][str(horizon)] = result
    return output


def figure(summary):
    primary = summary['window_results']['1800']
    denominator = max(primary['before'], primary['after'], 1)
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="700" viewBox="0 0 1600 700">',
             '<rect width="1600" height="700" fill="#10161e"/>', '<g font-family="monospace" fill="#edf3f7">',
             '<text x="60" y="80" font-size="31">Observed writes around first successful page deletion</text>',
             f'<text x="60" y="135" font-size="24">{primary["pages"]:,} eligible pages; paired 29-minute windows with 60-second guard</text>']
    for y, name, color in ((235, 'before', '#8999aa'), (370, 'after', '#77d9b5')):
        value = primary[name]
        parts.extend([f'<text x="60" y="{y}" font-size="28">{name}: {value:,} saves</text>',
                      f'<rect x="60" y="{y+25}" width="{1400*value/denominator:.2f}" height="58" fill="{color}"/>'])
    parts += [f'<text x="60" y="555" font-size="25">{primary["pages_with_return"]:,}/{primary["pages"]:,} pages have a post-guard return within 30 minutes</text>',
              '<text x="60" y="615" font-size="22">Descriptive pairing only. Selection, task completion and missing captures confound causality.</text>',
              '<text x="60" y="655" font-size="22">A later save does not show that the same content or agent returned.</text></g></svg>']
    return '\n'.join(parts)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    if args.out.exists():
        raise SystemExit('Refusing to overwrite an existing attempt directory')
    hashes = {name: sha(args.data/name) for name in EXPECTED}
    if hashes != EXPECTED:
        raise SystemExit('Frozen input hashes differ; do not silently run a new cohort')
    if any((args.data/name).stat().st_mode & 0o222 for name in EXPECTED):
        raise SystemExit('Raw input copies must be read-only before this bounded pilot')
    assignments, accounting = select_assignments(rows(args.data/'events.jsonl.gz'), rows(args.data/'revisions.jsonl.gz'))
    summary = summarize(assignments, accounting)
    if {name: sha(args.data/name) for name in EXPECTED} != hashes:
        raise SystemExit('Input changed during analysis')
    summary['provenance'] = {'input_sha256': hashes, 'analyzer_sha256': sha(__file__),
                             'raw_input_mode': 'read-only', 'source': 'https://collusion.wiki/explorer/download'}
    args.out.mkdir(parents=True)
    (args.out/'assignments.json').write_text(json.dumps(assignments, indent=2)+'\n')
    (args.out/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    (args.out/'contrast.svg').write_text(figure(summary))
    print(json.dumps({'accounting': accounting, 'primary': summary['window_results']['1800']}, indent=2))

if __name__ == '__main__':
    main()
