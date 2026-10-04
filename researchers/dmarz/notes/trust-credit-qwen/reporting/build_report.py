"""Build the sanitized records and print every number used in RESULTS.md from the saved rows.

    python3 reporting/build_report.py <results directory of the run> [--verify <launcher verify json>] [--write]

Reads chain-status.json and each stage's saved files, regrades every row and recomputes totals and
the analysis with the study's own code (src/), and with --write copies sanitized records into
records/. Makes no network request and no model call. Outside the source hash.
"""
import argparse
import csv
import gzip
import json
import os
import re
import shutil
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / 'src'))
import analyze, chain, manifest, study, worker  # noqa: E402

SENSITIVE = re.compile(r'(\b\d{1,3}(?:\.\d{1,3}){3}\b|https?://|Bearer|Authorization|x-api-key|sk-or-|sk-ant-|SWARM_HUB_TOKEN|/srv/|/home/|/Users/)')


def jl(path):
    with gzip.open(path, 'rt') as f: return [json.loads(line) for line in f if line.strip()]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('results'); ap.add_argument('--verify'); ap.add_argument('--write', action='store_true')
    a = ap.parse_args(); base = Path(a.results); out = {}
    status = json.loads((base / 'chain-status.json').read_text())
    assert status['source_hash'] == study.source_hash(), 'the saved run was made at another source hash'
    dirs = {s: base / os.path.basename(e['directory']) for s, e in status['stages'].items()}
    rows = {s: jl(dirs[s] / 'episodes.jsonl.gz') for s in study.STAGES}
    assigned = {s: jl(dirs[s] / 'assignments.jsonl.gz') for s in study.STAGES}
    summaries = {s: json.loads((dirs[s] / 'summary.json').read_text()) for s in study.STAGES}
    ref = manifest.load(); recon = {}
    for s in study.STAGES:
        by = {x['id']: x for x in assigned[s]}; rr = rows[s]; good = [r for r in rr if r['status'] == 'completed']
        saved = json.loads((dirs[s] / 'analysis.json').read_text()); grid = [r for r in rr if r['kind'] in ('pilot', 'clean')]
        e = status['stages'][s]
        recon[s] = {'assigned': len(by), 'started': sum(r['status'] != 'not_started' for r in rr), 'terminal': len(rr), 'graded': len(good),
                    'analyzed': len(good), 'failed': sum(r['status'] == 'failed' for r in rr),
                    'manifest_digest_matches': manifest.stage_entry(assigned[s])['digest'] == ref['stages'][s]['digest'],
                    'every_row_regraded_equal': all(chain.close(r['evaluation'], study.evaluate(by[r['id']], r['answer'])) and
                                                    chain.close(r['reference_evaluation'], study.evaluate(by[r['id']], study.scripted(by[r['id']]['packet']))) for r in good),
                    'analysis_recomputed_equal': chain.close(saved, json.loads(json.dumps(analyze.analyze(rr)))) if grid else saved.get('cells') == [],
                    'totals': worker.totals(rr, len(by)), 'worker_seconds': round(summaries[s]['elapsed_seconds'], 1),
                    'hub_started': e['started'], 'hub_ended': e['ended'], 'run': e['run']}
    out['reconciliation'] = recon
    s1 = rows['S1']; A = analyze.analyze(s1); d = study.design()
    out['primary'] = {k: A['primary'][k] for k in ('estimate', 'interval', 'roots', 'positive_roots')}
    out['primary']['per_root'] = [x['difference'] for x in A['primary']['per_root']]
    out['secondary'] = {k: {x: v[x] for x in ('estimate', 'interval', 'roots', 'positive_roots')} for k, v in A['secondary'].items()}
    out['escalation'] = [{x: e[x] for x in ('attacker_pass', 'rule', 'estimate', 'interval', 'positive_roots')} for e in A['escalation']]
    out['levels_propagated_minus_direct'] = A['levels']
    out['model_propagated_minus_direct'] = A['model_propagated_minus_direct']
    cells = A['cells']
    for c in cells:
        w = c['model']['rare_wrong']; c['wrong_equal_to_fabricated_share'] = (c['model']['rare_fabricated'] / w) if w else None
        c['model_minus_reference'] = {f: c['model'][f] - c['reference'][f] for f in ('rare_correct', 'rare_wrong', 'rare_abstain')}
    out['cells'] = cells
    # per-root seat ranges for the level caveat
    seats = defaultdict(list)
    for r in s1:
        if r['kind'] == 'pilot': seats[(r['attacker_pass'], r['rule'], r['checks'])].append(r['admission']['attacker_seats'])
    out['seat_ranges'] = {f'{k[0]}|{k[1]}|{k[2]}': [min(v), statistics.median(v), max(v)] for k, v in sorted(seats.items())}
    lvl = defaultdict(dict)
    for r in s1:
        if r['kind'] == 'pilot': lvl[(r['task'], r['attacker_pass'], r['checks'])][r['rule']] = r['admission']['attacker_seats']
    out['roots_where_direct_seats_more_than_propagated'] = {f'{rate}|{b}': sum(v['direct'] > v['propagated'] for k, v in lvl.items() if k[1] == rate and k[2] == b)
                                                            for rate in d['attacker_pass'] for b in d['check_budgets']}
    # provider metadata over all paid calls
    paid = [r for s in ('P0', 'Q0', 'S1') for r in rows[s]]; acc = [r['accounting'] for r in paid]
    out['provider'] = {'calls': len(paid), 'response_models': dict(Counter(x.get('response_model') for x in acc)),
                       'response_providers': dict(Counter(x.get('response_provider') for x in acc)),
                       'finish_reasons': dict(Counter(x.get('finish_reason') for x in acc)),
                       'reasoning_tokens': dict(Counter(str(x.get('reasoning_tokens')) for x in acc)),
                       'cost_reported_by_provider': sum(x.get('provider_reported_usd') is not None for x in acc),
                       'reported_equals_snapshot_price': sum(x.get('provider_reported_usd') is not None and abs(x['provider_reported_usd'] - x['computed_usd']) < 5e-7 for x in acc),
                       'reported_over_computed_max': max((x['provider_reported_usd'] / x['computed_usd'] for x in acc if x.get('provider_reported_usd')), default=None),
                       'attempts': dict(Counter(x.get('attempts') for x in acc)),
                       'tokens_per_byte_min_max': [min(x['input_tokens'] / x['request_bytes'] for x in acc), max(x['input_tokens'] / x['request_bytes'] for x in acc)],
                       'input_tokens_min_mean_max': [min(x['input_tokens'] for x in acc), sum(x['input_tokens'] for x in acc) / len(acc), max(x['input_tokens'] for x in acc)],
                       'output_tokens_min_mean_max': [min(x['output_tokens'] for x in acc), sum(x['output_tokens'] for x in acc) / len(acc), max(x['output_tokens'] for x in acc)],
                       'latency_seconds_median_p95_max': [statistics.median(x['latency_seconds'] for x in acc), sorted(x['latency_seconds'] for x in acc)[int(.95 * len(acc))], max(x['latency_seconds'] for x in acc)]}
    out['probe'] = summaries['P0']['probe']; out['qualification'] = summaries['Q0']['qualification']
    groups = defaultdict(list)
    for r in s1: groups[(r['task'], r['packet_hash'])].append(json.dumps(r['answer'], sort_keys=True))
    rep = [v for v in groups.values() if len(v) > 1]
    out['repeated_packets'] = {'groups': len(rep), 'calls': sum(len(v) for v in rep), 'identical_answers': sum(len(set(v)) == 1 for v in rep)}
    for split in ('engineering', 'comparison'):
        h = study.historical_audit(split)
        out['historical_audit_' + split] = {'snapshots': len(h), 'with_dangling': sum(x['dangling'] > 0 for x in h), 'same_admitted_set': sum(x['same_admitted_set'] for x in h),
                                            'same_set_without_dangling': sum(x['same_admitted_set'] for x in h if x['dangling'] == 0), 'without_dangling': sum(x['dangling'] == 0 for x in h),
                                            'seats_different_when_not_same': sorted(x['seats_different'] for x in h if not x['same_admitted_set']),
                                            'max_attacker_seat_difference': max(abs(x['attacker_seats_historical'] - x['attacker_seats_propagated']) for x in h),
                                            'mean_attacker_seats_historical_vs_propagated_strong': {b: [analyze.mean(x['attacker_seats_historical'] for x in h if x['checks'] == b and x['attacker_pass'] == 0.1),
                                                                                                     analyze.mean(x['attacker_seats_propagated'] for x in h if x['checks'] == b and x['attacker_pass'] == 0.1)] for b in d['check_budgets']}}
    out['ledger'] = status.get('ledger')
    if a.write:
        rec = HERE / 'records'; rec.mkdir(exist_ok=True)
        clean = json.loads(json.dumps(status))
        for e in clean['stages'].values(): e['directory'] = '<study-base>/results/' + os.path.basename(e['directory'])
        (rec / 'chain-status.json').write_text(json.dumps(clean, indent=2, sort_keys=True) + '\n')
        for s in study.STAGES:
            for name in ('summary.json', 'analysis.json'):
                (rec / f'{s.lower()}-{name}').write_text(json.dumps(json.loads((dirs[s] / name).read_text()), indent=1, sort_keys=True) + '\n')
            for name in ('episodes.jsonl.gz', 'assignments.jsonl.gz', 'audits.jsonl.gz'):
                if s == 'S0' and name == 'assignments.jsonl.gz': continue        # regenerated offline by `src/worker.py --stage S0`
                shutil.copyfile(dirs[s] / name, rec / f'{s.lower()}-{name}')
        if a.verify:
            v = json.loads(Path(a.verify).read_text())
            (rec / 'verify-summary.json').write_text(json.dumps({'exit': v['exit'], 'revision': v['revision'], 'server': v['host'], 'chain_active': v['chain_active'],
                                                                  'worker_active': v['worker_active'], 'result': v['result']}, indent=1, sort_keys=True) + '\n')
        with (rec / 's1-cells.csv').open('w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['kind', 'attacker_pass', 'rule', 'checks', 'assigned', 'valid', 'attacker_seats', 'attacker_seat_share', 'specialist_retention', 'truth_available',
                        'truth_plurality', 'model_rare_correct', 'model_rare_wrong', 'model_rare_abstain', 'model_wrong_equal_fabricated', 'reference_rare_correct',
                        'reference_rare_wrong', 'reference_rare_abstain', 'input_tokens', 'output_tokens', 'cost_usd'])
            for c in cells:
                w.writerow([c['kind'], c['attacker_pass'], c['rule'], c['checks'], c['assigned'], c['valid']] +
                           [round(c['admission'][k], 4) for k in ('attacker_seats', 'attacker_seat_share', 'specialist_retention', 'truth_available', 'truth_plurality')] +
                           [round(c['model'][k], 4) for k in ('rare_correct', 'rare_wrong', 'rare_abstain', 'rare_fabricated')] +
                           [round(c['reference'][k], 4) for k in ('rare_correct', 'rare_wrong', 'rare_abstain')] + [c['input_tokens'], c['output_tokens'], round(c['cost_usd'], 6)])
        (rec / 'report-numbers.json').write_text(json.dumps(out, indent=1, sort_keys=True) + '\n')
        hits = []
        for p in sorted(rec.iterdir()):
            text = gzip.open(p, 'rt').read() if p.suffix == '.gz' else p.read_text()
            for m in SENSITIVE.finditer(text): hits.append((p.name, m.group(0), text[max(0, m.start() - 40):m.end() + 40]))
        out['sensitive_scan'] = {'files': len(list(rec.iterdir())), 'hits': hits[:20], 'hit_count': len(hits)}
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == '__main__':
    main()
