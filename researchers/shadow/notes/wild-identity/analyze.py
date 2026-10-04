#!/usr/bin/env python3
"""Offline, descriptive identity observability audit. Never executes dataset text."""
import argparse
import bisect
import collections
import csv
import datetime as dt
import gzip
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import subprocess

VERSION = '1.0.1'
AGENT = re.compile(r'^\[(?P<id>[a-z][a-z0-9_-]*/[a-zA-Z0-9][a-zA-Z0-9_.-]*)\]')
SIGNOFF = re.compile(r'(?m)^\s*[-\u2014\u2013]{1,2}\s+([A-Za-z][A-Za-z0-9_. -]{1,59})\s*$')
EXPLICIT_SIGNOFF = re.compile(r'(?im)^\s*(?:signed(?: by)?|sign[- ]?off)\s*:\s*([A-Za-z][A-Za-z0-9_. -]{1,59})\s*$')


def rows(path):
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        for line in f:
            yield json.loads(line)


def timestamp(value):
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
        return parsed.timestamp() if parsed.tzinfo else None
    except (ValueError, TypeError):
        return None


def gini(values):
    a = sorted(values)
    total = sum(a)
    if not a or not total:
        return 0.0
    n = len(a)
    return sum((2*i-n-1)*x for i, x in enumerate(a, 1)) / (n*total)


def matcher(names):
    # Exact case-sensitive known identifiers; longest alternatives first.
    names = sorted(set(names), key=lambda x: (-len(x), x))
    if not names:
        return re.compile(r'(?!)')
    return re.compile(r'(?<![\w./-])(?:' + '|'.join(re.escape(x) for x in names) + r')(?![\w./-])')


def references(regex, text, source):
    return {m.group(0) for m in regex.finditer(text)} - {source}


def added_text(row):
    """Use archive diff hunk target line ranges, not full retained snapshots."""
    # Archive hunk offsets count the empty trailing line after a newline.
    lines = row.get('body', '').split('\n')
    out = []
    for h in row.get('hunks', []):
        if h.get('op') in ('insert', 'replace'):
            b0, b1 = h['b0'], h['b1']
            if not 0 <= b0 <= b1 <= len(lines):
                raise ValueError('Invalid target diff range: ' + row['rev_id'])
            out.extend(lines[b0:b1])
    return '\n'.join(out)


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def public_id(dataset, name):
    return hashlib.sha256((dataset + ':' + name).encode()).hexdigest()[:16]


class Population:
    def __init__(self, name):
        self.name = name
        self.ids = {}
        self.total = self.anonymous = self.missing_time = 0
        self.start = self.end = None
        self.edges = {'snapshot': collections.Counter(), 'fresh': collections.Counter()}
        self.reference_events = collections.Counter()
        self.referencing_ids = {'snapshot': set(), 'fresh': set()}

    def event(self, name, time):
        self.total += 1
        if time is None:
            self.missing_time += 1
        else:
            self.start = time if self.start is None else min(self.start, time)
            self.end = time if self.end is None else max(self.end, time)
        if not name:
            self.anonymous += 1
            return
        stats = self.ids.setdefault(name, {'count': 0, 'times': [], 'fresh_reference_events': 0})
        stats['count'] += 1
        if time is not None:
            stats['times'].append(time)

    def graph_event(self, name, text, regex, mode):
        if name not in self.ids:
            return
        refs = references(regex, text, name)
        if refs:
            self.reference_events[mode] += 1
            self.referencing_ids[mode].add(name)
            if mode == 'fresh':
                self.ids[name]['fresh_reference_events'] += 1
        for target in refs:
            self.edges[mode][name, target] += 1

    def summarize(self):
        counts = [r['count'] for r in self.ids.values()]
        spans = [(max(r['times'])-min(r['times']))/3600 for r in self.ids.values() if r['times']]
        positive = [x for x in spans if x > 0]
        window = (self.end-self.start)/3600 if self.start is not None else 0
        n = len(counts)
        med = statistics.median(spans) if spans else None
        cross = {}
        for bucket, predicate in [('at_or_below_median', lambda x: x <= med), ('above_median', lambda x: x > med)]:
            cohort = [r for r in self.ids.values() if r['times'] and predicate((max(r['times'])-min(r['times']))/3600)]
            cross[bucket] = {'identities': len(cohort), 'referencing_identities': sum(r['fresh_reference_events'] > 0 for r in cohort),
                             'events': sum(r['count'] for r in cohort), 'fresh_reference_events': sum(r['fresh_reference_events'] for r in cohort)}
        return {
            'event_unit': 'revision' if self.name == 'wiki' else 'commit',
            'events': self.total, 'attributed_events': sum(counts), 'unattributed_events': self.anonymous,
            'missing_time_events': self.missing_time, 'identities': n,
            'identities_with_time': len(spans), 'singleton_identities': sum(x == 1 for x in counts),
            'zero_span_identities': sum(x == 0 for x in spans),
            'span_at_most_1h_identities': sum(x <= 1 for x in spans),
            'median_span_hours': med, 'median_positive_span_hours': statistics.median(positive) if positive else None,
            'max_span_hours': max(spans) if spans else None, 'observation_window_hours': window,
            'median_span_fraction_of_window': med/window if window and med is not None else None,
            'first_time_utc': dt.datetime.fromtimestamp(self.start, dt.timezone.utc).isoformat() if self.start else None,
            'last_time_utc': dt.datetime.fromtimestamp(self.end, dt.timezone.utc).isoformat() if self.end else None,
            'gini': gini(counts), 'top_10pct_identity_count': math.ceil(n/10),
            'top_10pct_event_share': sum(sorted(counts, reverse=True)[:math.ceil(n/10)])/sum(counts) if sum(counts) else None,
            'top_identity_event_share': max(counts)/sum(counts) if counts else None,
            'casefold_identities': len({x.casefold() for x in self.ids}),
            'graphs': {mode: graph_summary(self, mode) for mode in self.edges},
            'span_reference_cross_tab': cross,
        }


def graph_summary(pop, mode):
    edges = pop.edges[mode]
    nodes = set(pop.ids)
    adj = {x: set() for x in nodes}
    indegree, outdegree = collections.Counter(), collections.Counter()
    for a, b in edges:
        if b not in nodes:
            raise ValueError('Unknown graph target')
        adj[a].add(b); adj[b].add(a)
        indegree[b] += 1; outdegree[a] += 1
    remaining = set(nodes)
    sizes = []
    while remaining:
        todo = [remaining.pop()]; size = 0
        while todo:
            a = todo.pop(); size += 1
            for b in sorted(adj[a]):
                if b in remaining:
                    remaining.remove(b); todo.append(b)
        sizes.append(size)
    return {'directed_edges': len(edges), 'event_edge_occurrences': sum(edges.values()),
            'referencing_events': pop.reference_events[mode], 'referencing_identities': len(pop.referencing_ids[mode]),
            'touched_identities': sum(bool(adj[x]) for x in nodes),
            'weak_components_including_isolates': len(sizes), 'largest_weak_component': max(sizes, default=0),
            'reciprocal_edge_fraction': sum((b, a) in edges for a, b in edges)/len(edges) if edges else 0,
            'max_indegree': max(indegree.values(), default=0), 'max_outdegree': max(outdegree.values(), default=0)}


def wiki_analysis(root):
    path = root/'collusion-wiki/revisions.jsonl.gz'
    data = list(rows(path))
    pop = Population('wiki')
    grades = collections.Counter()
    revisions = set()
    for r in data:
        if r['rev_id'] in revisions:
            raise ValueError('Duplicate wiki revision')
        revisions.add(r['rev_id'])
        pop.event(r.get('label'), timestamp(r.get('time')))
        grades[r.get('time_grade')] += 1
    regex = matcher(pop.ids)
    sign = collections.Counter()
    known_labels = set(pop.ids)
    unknown_signs = set()
    for r in data:
        actor = r.get('label'); body = r.get('body', '')
        fresh = added_text(r)
        for mode, text in [('snapshot', body), ('fresh', fresh)]:
            pop.graph_event(actor, text, regex, mode)
            names = set(SIGNOFF.findall(text))
            sign[mode + '_candidate_events'] += bool(names)
            known = names & known_labels
            unknown_signs.update(names - known_labels)
            sign[mode + '_known_signoff_events'] += bool(known)
            sign[mode + '_known_signoff_occurrences'] += len(known)
            sign[mode + '_mismatching_signoff_occurrences'] += sum(n != actor for n in known)
    validation = collections.Counter()
    table = root/'collusion-wiki/labels.jsonl.gz'
    for r in rows(table):
        name = r.get('label')
        if not name:
            validation['blank_label_table_rows'] += 1
            continue
        validation['nonblank_label_table_rows'] += 1
        observed = pop.ids.get(name)
        if observed is None:
            validation['table_labels_not_in_revisions'] += 1
            continue
        validation['count_mismatches'] += observed['count'] != r['stored_revisions']
        if observed['times']:
            validation['first_time_mismatches'] += min(observed['times']) != timestamp(r.get('first_write'))
            validation['last_time_mismatches'] += max(observed['times']) != timestamp(r.get('last_write'))
    result = pop.summarize()
    result.update({'time_grades': dict(grades), 'signoffs': dict(sign),
                   'unknown_signoff_candidate_strings': len(unknown_signs), 'label_table_validation': dict(validation)})
    return pop, result


def git_analysis(args):
    if args.git_log:
        blob = args.git_log.read_text()
        commit = args.commit
    else:
        commit = subprocess.check_output(['git', '-C', str(args.repo), 'rev-parse', args.commit], text=True).strip()
        blob = subprocess.check_output(['git', '-C', str(args.repo), 'log', commit, '--format=%H%x1f%cI%x1f%B%x1e'], text=True)
    records = []
    hashes = set()
    for raw in blob.split('\x1e'):
        raw = raw.strip('\n')
        if not raw:
            continue
        sha, date, text = raw.split('\x1f', 2)
        if sha in hashes:
            raise ValueError('Duplicate commit')
        hashes.add(sha)
        records.append((date, text))
    pop = Population('swarm_lab')
    for date, text in records:
        m = AGENT.match(text)
        pop.event(m.group('id') if m else None, timestamp(date))
    regex = matcher(pop.ids)
    for date, text in records:
        m = AGENT.match(text)
        if m:
            # Do not count the obligatory actor prefix as a reference.
            pop.graph_event(m.group('id'), text[m.end():], regex, 'fresh')
            pop.graph_event(m.group('id'), text[m.end():], regex, 'snapshot')
    result = pop.summarize()
    result['snapshot_commit'] = commit
    result['unattributed_note'] = 'Includes bot indexing, merge, human and unprefixed commits. Not separate agent identities.'
    return pop, result


def swarmtraces_analysis(root):
    counts = collections.Counter(); fields = collections.Counter(); timed = 0; parents = 0; null_times = 0
    candidates = collections.Counter(); runtime_records = 0; unique_runtime_markers = set()
    with gzip.open(root/'swarmtraces/redacted.jsonl.gz', 'rt') as f:
        for ln in f:
            r = json.loads(ln)
            counts[r.get('kind')] += 1; fields.update(r.keys())
            timed += timestamp(r.get('time_utc')) is not None
            null_times += r.get('time_utc') is None
            parents += bool(r.get('parent_id'))
            text = r.get('text', '')
            candidates['standalone_dash_candidate_records'] += bool(SIGNOFF.search(text))
            candidates['explicit_signoff_candidate_records'] += bool(EXPLICIT_SIGNOFF.search(text))
            markers = re.findall(r'\[REDACTED:runtime_identifier(?::\d+)?\]', text)
            runtime_records += bool(markers); unique_runtime_markers.update(markers)
    return {'records': sum(counts.values()), 'by_kind': dict(counts), 'timestamped_records': timed,
            'null_time_records': null_times,
            'records_with_parent_id': parents, 'field_presence': dict(fields),
            'records_with_runtime_identifier_redaction': runtime_records,
            'distinct_runtime_redaction_placeholders': len(unique_runtime_markers),
            'signoff_probe': dict(candidates),
            'identity_lifetime_gini_graph': None,
            'not_identifiable_reason': 'No structured actor field or timestamps; code/file-list sign-off candidates and redaction placeholders are not authors. Parent links are decoding provenance, not agent communication.'}


def write_csv(path, fields, rows_):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows_)


def curves(populations, out, swarm_result):
    curve_rows, stats_rows, degrees = [], [], []
    for pop in populations:
        ids = pop.ids
        for name, r in sorted(ids.items()):
            span = (max(r['times'])-min(r['times']))/3600 if r['times'] else None
            stats_rows.append({'swarm': pop.name, 'identity_digest': public_id(pop.name, name), 'events': r['count'],
                               'observed_span_hours': span, 'fresh_reference_events': r['fresh_reference_events']})
        counts = sorted(r['count'] for r in ids.values())
        cumsum = 0
        curve_rows.append({'swarm': pop.name, 'curve': 'lorenz', 'x': 0, 'y': 0})
        for i, x in enumerate(counts, 1):
            cumsum += x
            curve_rows.append({'swarm': pop.name, 'curve': 'lorenz', 'x': i/len(counts), 'y': cumsum/sum(counts)})
        spans = sorted((max(r['times'])-min(r['times']))/3600 for r in ids.values() if r['times'])
        window = (pop.end-pop.start)/3600
        for x in sorted(set(spans)):
            y = bisect.bisect_right(spans, x)/len(spans)
            curve_rows.append({'swarm': pop.name, 'curve': 'span_cdf', 'x': x, 'y': y})
            curve_rows.append({'swarm': pop.name, 'curve': 'normalized_span_cdf', 'x': x/window if window else 0, 'y': y})
        for mode, edges in pop.edges.items():
            indegree, outdegree = collections.Counter(), collections.Counter()
            for a, b in edges: outdegree[a] += 1; indegree[b] += 1
            histogram = collections.Counter((indegree[x], outdegree[x]) for x in ids)
            for (i, o), count in sorted(histogram.items()):
                degrees.append({'swarm': pop.name, 'graph': mode, 'indegree': i, 'outdegree': o, 'identities': count})
    if len({(r['swarm'], r['identity_digest']) for r in stats_rows}) != len(stats_rows):
        raise ValueError('Digest collision')
    write_csv(out/'curves.csv', ['swarm', 'curve', 'x', 'y'], curve_rows)
    write_csv(out/'identity-aggregates.csv', ['swarm', 'identity_digest', 'events', 'observed_span_hours', 'fresh_reference_events'], stats_rows)
    write_csv(out/'degree-histograms.csv', ['swarm', 'graph', 'indegree', 'outdegree', 'identities'], degrees)
    make_svg(curve_rows, out/'identity-observability.svg', swarm_result)


def make_svg(curve_rows, path, swarm_result):
    """Dependency-free vector figure. A missing third curve is intentional."""
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="960" viewBox="0 0 1800 960">',
             '<rect width="1800" height="960" fill="#faf9f6"/>',
             '<style>text{font-family:Arial,sans-serif;fill:#19232b} .title{font-size:32px;font-weight:bold} .small{font-size:20px}</style>',
             '<text x="80" y="60" class="title">Observable names are not persistent agent identities</text>']
    colors = {'wiki': '#15776b', 'swarm_lab': '#ad493a'}
    panels = [('span_cdf', 'Observed name span CDF', 'Hours between first and last event', 0, 0, True),
              ('lorenz', 'Participation Lorenz curve', 'Cumulative share of named identities', 1, 0, False),
              ('normalized_span_cdf', 'Span / observation window', 'Fraction of each archive window', 0, 1, False)]
    for curve, title, xlabel, col, row, log in panels:
        x0, y0, w, h = 110+col*880, 135+row*385, 700, 260
        values = [r for r in curve_rows if r['curve'] == curve]
        xmax = max(r['x'] for r in values) if log else 1
        def xx(x): return x0+w*(math.log1p(x)/math.log1p(xmax) if log else x)
        def yy(y): return y0+h*(1-y)
        parts.append(f'<text x="{x0}" y="{y0-25}" font-size="25">{title}</text>')
        for tick in [0, .25, .5, .75, 1]:
            y = yy(tick)
            parts += [f'<line x1="{x0}" y1="{y}" x2="{x0+w}" y2="{y}" stroke="#d4d8d6"/>', f'<text x="{x0-50}" y="{y+6}" class="small">{tick:g}</text>']
        xticks = [0, 1, 6, 24, 168, 720] if log else [0, .25, .5, .75, 1]
        for tick in xticks:
            if tick > xmax: continue
            x = xx(tick)
            parts.append(f'<text x="{x-10}" y="{y0+h+27}" class="small">{tick:g}</text>')
        parts.append(f'<text x="{x0}" y="{y0+h+62}" class="small">{xlabel}' + (' (log1p axis)' if log else '') + '</text>')
        if curve == 'lorenz':
            parts.append(f'<line x1="{x0}" y1="{y0+h}" x2="{x0+w}" y2="{y0}" stroke="#8e9795" stroke-dasharray="8 6"/>')
        for swarm, color in colors.items():
            points = [(r['x'], r['y']) for r in values if r['swarm'] == swarm]
            # Draw CDFs as right-continuous steps, Lorenz as linear interpolation.
            coords = []
            for x, y in points:
                if curve != 'lorenz' and coords:
                    coords.append((xx(x), coords[-1][1]))
                coords.append((xx(x), yy(y)))
            pts = ' '.join(f'{x:.2f},{y:.2f}' for x, y in coords)
            parts.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="4"/>')
    for i, (label, color) in enumerate([('collusion.wiki labels', colors['wiki']), ('swarm-lab commit ids', colors['swarm_lab'])]):
        parts.append(f'<rect x="{990+i*355}" y="490" width="25" height="8" fill="{color}"/><text x="{1028+i*355}" y="504" class="small">{label}</text>')
    parts += ['<text x="990" y="570" class="title">SwarmTraces: not identifiable</text>',
              f'<text x="990" y="620" font-size="24">{swarm_result["records"]:,} records; {swarm_result["timestamped_records"]:,} structured timestamps.</text>',
              '<text x="990" y="660" font-size="24">No author field in the redacted export.</text>',
              '<text x="990" y="700" class="small">Payload/recovery rows and parent links are not agents.</text>',
              '<text x="990" y="750" class="small">A third lifetime, Gini or coordination curve would invent data.</text>',
              '<text x="80" y="925" class="small">Finite archive descriptions. Spans are not survival estimates; text references are not verified communication. Git snapshot: 4959a80b.</text>', '</svg>']
    path.write_text('\n'.join(parts))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', type=Path, required=True)
    p.add_argument('--repo', type=Path)
    p.add_argument('--git-log', type=Path, help='Private git export: git log SHA --format=%H%x1f%cI%x1f%B%x1e')
    p.add_argument('--commit', default='4959a80b')
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    if not (args.repo or args.git_log): p.error('Supply --repo or --git-log')
    args.out.mkdir(parents=True, exist_ok=True)
    wiki, wiki_result = wiki_analysis(args.data)
    lab, lab_result = git_analysis(args)
    swarm = swarmtraces_analysis(args.data)
    hashes = {str(path.relative_to(args.data)): digest(path) for path in [args.data/'collusion-wiki/revisions.jsonl.gz', args.data/'collusion-wiki/labels.jsonl.gz', args.data/'swarmtraces/redacted.jsonl.gz']}
    if args.git_log: hashes['private_git_log'] = digest(args.git_log)
    result = {'analysis_version': VERSION, 'design': 'Descriptive, post-hoc census; not a causal experiment',
              'input_sha256': hashes, 'wiki': wiki_result, 'swarm_lab': lab_result, 'swarmtraces': swarm}
    (args.out/'summary.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    curves([wiki, lab], args.out, swarm)
    print(json.dumps({'wiki': {'events': wiki.total, 'identities': len(wiki.ids)}, 'swarm_lab': {'events': lab.total, 'identities': len(lab.ids)}, 'swarmtraces': {'records': swarm['records'], 'timestamps': swarm['timestamped_records']}}))


if __name__ == '__main__':
    main()
