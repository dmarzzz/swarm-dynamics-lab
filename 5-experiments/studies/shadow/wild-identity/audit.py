#!/usr/bin/env python3
"""Cross-check derived metrics against source label table and aggregate curves."""
import argparse
import csv
import datetime
import gzip
import json
from pathlib import Path
import statistics


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--data', type=Path, required=True)
    p.add_argument('--results', type=Path, required=True)
    args = p.parse_args()
    summary = json.loads((args.results/'summary.json').read_text())
    checks = {}
    with gzip.open(args.data/'collusion-wiki/labels.jsonl.gz', 'rt') as f:
        labels = [json.loads(ln) for ln in f]
    labels = [r for r in labels if r['label']]
    counts = sorted(r['stored_revisions'] for r in labels)
    total = sum(counts)
    shares = [0]; cumulative = 0
    for x in counts:
        cumulative += x
        shares.append(cumulative/total)
    # Gini from trapezoid area under the Lorenz curve, not the rank formula.
    alternate_gini = 1 - sum(shares[i]+shares[i+1] for i in range(len(counts)))/len(counts)
    def ts(s): return datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))
    spans = [(ts(r['last_write'])-ts(r['first_write'])).total_seconds()/3600 for r in labels]
    wiki = summary['wiki']
    checks['wiki_count_from_label_table'] = total == wiki['attributed_events']
    checks['wiki_identity_count_from_label_table'] = len(labels) == wiki['identities']
    checks['wiki_gini_lorenz_alternate'] = abs(alternate_gini-wiki['gini']) < 1e-12
    checks['wiki_median_span_from_label_table'] = statistics.median(spans) == wiki['median_span_hours']
    checks['wiki_zero_spans_from_label_table'] = sum(x == 0 for x in spans) == wiki['zero_span_identities']
    with (args.results/'identity-aggregates.csv').open() as f: identities = list(csv.DictReader(f))
    with (args.results/'curves.csv').open() as f: curves = list(csv.DictReader(f))
    with (args.results/'degree-histograms.csv').open() as f: degrees = list(csv.DictReader(f))
    for swarm in ['wiki', 'swarm_lab']:
        result = summary[swarm]
        subset = [r for r in identities if r['swarm'] == swarm]
        checks[swarm+'_aggregate_rows'] = len(subset) == result['identities']
        checks[swarm+'_aggregate_events'] = sum(int(r['events']) for r in subset) == result['attributed_events']
        checks[swarm+'_total_accounting'] = result['attributed_events']+result['unattributed_events'] == result['events']
        checks[swarm+'_positive_span_median'] = statistics.median(float(r['observed_span_hours']) for r in subset if float(r['observed_span_hours'])>0) == result['median_positive_span_hours']
        lorenz = [r for r in curves if r['swarm'] == swarm and r['curve'] == 'lorenz']
        checks[swarm+'_curve_endpoint'] = float(lorenz[-1]['x']) == float(lorenz[-1]['y']) == 1
        for mode in ['snapshot', 'fresh']:
            ds = [r for r in degrees if r['swarm'] == swarm and r['graph'] == mode]
            checks[swarm+'_'+mode+'_degree_indegree_sum'] = sum(int(r['indegree'])*int(r['identities']) for r in ds) == result['graphs'][mode]['directed_edges']
            checks[swarm+'_'+mode+'_degree_outdegree_sum'] = sum(int(r['outdegree'])*int(r['identities']) for r in ds) == result['graphs'][mode]['directed_edges']
    st = summary['swarmtraces']
    checks['swarmtraces_kind_accounting'] = sum(st['by_kind'].values()) == st['records']
    checks['swarmtraces_no_imputed_metrics'] = st['timestamped_records'] == 0 and st['identity_lifetime_gini_graph'] is None
    report = {'checks': checks, 'passed': sum(checks.values()), 'total': len(checks), 'alternate_wiki_gini': alternate_gini}
    (args.results/'audit.json').write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, indent=2))
    if not all(checks.values()): raise SystemExit(1)


if __name__ == '__main__':
    main()
