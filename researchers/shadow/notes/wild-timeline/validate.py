#!/usr/bin/env python3
"""Same-author saved-data reconciliation; never writes input rows."""
import argparse
import collections
import csv
import gzip
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    summary = json.loads((args.out / 'summary.json').read_text())
    checks = {}
    root = args.data
    t = root / 'transluce/urlquery-agent-activity-2026-09-22-v5'
    daily = list(csv.DictReader((t / 'daily-counts.csv').open()))
    sources = list(csv.DictReader((t / 'daily-source-counts.csv').open()))
    checks['transluce_count_reconciles'] = sum(int(r['total']) for r in daily) == summary['transluce']['included_reports_in_chart']
    checks['source_count_reconciles'] = sum(int(r['reports']) for r in sources) == sum(int(r['total']) for r in daily)
    events = collections.Counter()
    for line in gzip.open(root / 'collusion-wiki/events.jsonl.gz', 'rt'):
        events[json.loads(line)['event_type']] += 1
    revisions = sum(1 for _ in gzip.open(root / 'collusion-wiki/revisions.jsonl.gz', 'rt'))
    checks['wiki_saves_equal_revisions'] = events['save'] == revisions == summary['wiki']['held_revisions']
    checks['wiki_deletions_reconcile'] = events['delete'] == summary['wiki']['admin_deletions']
    kinds = collections.Counter()
    times = collections.Counter()
    for line in gzip.open(root / 'swarmtraces/redacted.jsonl.gz', 'rt'):
        row = json.loads(line)
        kinds[row['kind']] += 1
        times['non_null' if row.get('time_utc') else 'null_or_missing'] += 1
    checks['swarmtraces_count_reconciles'] = dict(kinds) == summary['swarmtraces']['by_kind']
    checks['swarmtraces_all_times_null'] = times['non_null'] == 0 and times['null_or_missing'] == summary['swarmtraces']['records']
    # Independent direct host extraction, using the eight reported domains.
    domains = {'unctad.org', 'aihw.gov.au', 'max.gov', 'sec.gov', 'healthdata.org', 'datausa.io', 'usaspending.gov', 'api.census.gov'}
    import re
    count = 0
    for line in gzip.open(root / 'collusion-wiki/revisions.jsonl.gz', 'rt'):
        body = json.loads(line).get('body') or ''
        hosts = []
        # Splitting at every scheme also finds target URLs embedded in proxy paths.
        for tail in re.split(r'https?://', body, flags=re.I)[1:]:
            authority = re.split(r'[/\s\"\'<>\]\)|]', tail, maxsplit=1)[0].rstrip('.,;')
            hosts.append(urlsplit('https://' + authority).hostname)
        count += any(h and (h == d or h.endswith('.' + d)) for h in hosts for d in domains)
    print('Independent host union:', count, 'vs reported:', summary['wiki']['revisions_linking_transluce_tracked_host'])
    checks['independent_host_union_reconciles'] = count == summary['wiki']['revisions_linking_transluce_tracked_host']
    from PIL import Image
    checks['figures_at_least_1600px'] = all(Image.open(args.out / p).width >= 1600 for p in ['timeline.png', 'shared.png'])
    inputs = ['transluce/urlquery-agent-activity-2026-09-22-v5/' + p for p in ['daily-counts.csv', 'daily-source-counts.csv', 'methods.json', 'report-sources.csv']]
    inputs += ['collusion-wiki/' + p for p in ['revisions.jsonl.gz', 'events.jsonl.gz', 'pages.jsonl.gz', 'shortener-logs.json.gz', 'other-wikis.json.gz']]
    inputs += ['swarmtraces/redacted.jsonl.gz']
    hashes = {}
    for path in inputs:
        digest = hashlib.sha256()
        with (root / path).open('rb') as handle:
            for chunk in iter(lambda: handle.read(1048576), b''):
                digest.update(chunk)
        hashes[path] = digest.hexdigest()
    result = {'assessor': 'shadow/sol-timeline', 'date': '2026-10-04', 'independent_researcher_review': False,
              'checks': checks, 'passed': all(checks.values()), 'input_sha256': hashes,
              'code_sha256': hashlib.sha256((args.out / 'timeline.py').read_bytes()).hexdigest()}
    (args.out / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(checks, indent=2))
    if not result['passed']:
        raise SystemExit('Reconciliation failed')


if __name__ == '__main__':
    main()
