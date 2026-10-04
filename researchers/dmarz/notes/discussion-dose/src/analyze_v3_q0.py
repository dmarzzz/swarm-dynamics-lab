"""Read-only post-run analysis; run with Python 3.12 and retained q0 artifacts.

This lives outside bench_v3 so it does not change the frozen runtime's hashes.
No provider is constructed and no model request can be dispatched.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

from bench_v3.cli import audit
from bench_v3.scoring import checkpoint, parent_context, reference_winner
from bench_v3.evidence import supported_parent
from bench_v3.worlds import cases


def read(path):
    return json.loads(path.read_text())


def fingerprint(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--review-receipt', type=Path, required=True)
    args = parser.parse_args()
    run = args.run
    replay_audit = audit(run)
    rows, summary, manifest = [read(run / n) for n in
                               ('episodes.json', 'summary.json', 'manifest.json')]
    assert replay_audit['ok'] and len(rows) == 96
    assert all(r['status'] == 'completed' for r in rows)
    assert read(args.review_receipt)['source_hashes'] == manifest['source_hashes']
    remote = read(run.parent / 'v3-q0-a1-remote-inventory.json')['files']
    for name, expected in remote.items():
        assert fingerprint(run / name) == {'bytes': expected['size'], 'sha256': expected['sha256']}, name
    hub = read(run.parent / 'v3-q0-a1-hub-verification.json')['hub_downloads_verified']
    for entry in hub:
        local = run / entry['name']
        if not local.exists():
            local = run / 'upload' / entry['name']
        assert fingerprint(local) == {k: entry[k] for k in ('bytes', 'sha256')}, entry['name']
    worlds = {c['id']: c for c in cases('qualification')}

    def aggregate(group):
        metrics = sorted({k for r in group for k in r['evaluation']})
        return {'assigned': len(group), 'observed': len(group), 'missing': 0,
                'totals': {k: math.fsum(r['evaluation'][k] for r in group
                                      if r['evaluation'].get(k) is not None) for k in metrics}}

    arms = ('independent', 'reports', 'private', 'board')
    swarm = [r for r in rows if r['kind'] == 'swarm']
    swarm_groups = {f'{"attacked" if attack else "clean"}:{arm}': aggregate(
        [r for r in swarm if r['arm'] == arm and r['attack'] == attack])
        for attack in (False, True) for arm in arms}
    memory = [r for r in rows if r['kind'] == 'memory']
    memory_groups = {state: aggregate([r for r in memory if r['state'] == state])
                     for state in sorted({r['state'] for r in memory})}
    diagnostics = []
    for row in sorted((r for r in rows if r['kind'] == 'diagnostic' and not r['attack']), key=lambda r: r['world']):
        case = worlds[row['world']]
        extracted = {k: v['value'] if v else None for k, v in row['answer']['claims'].items()}
        diagnostics.append({'world': row['world'], 'family': row['family'],
                            'rules': case['task']['rules'], 'true_values': case['truth'],
                            'all_values_extracted_correctly': extracted == case['truth'],
                            'expected_vote': reference_winner(case['task'], case['truth']),
                            'observed_vote': row['answer']['vote']})
    clean_reports = [{'world': r['world'], **checkpoint(worlds[r['world']], r['ballots'])}
                     for r in sorted(swarm, key=lambda r: r['world'])
                     if not r['attack'] and r['arm'] == 'reports']
    strict_citations = []
    for row in swarm:
        if not row['attack'] and row['evaluation']['parent_unsupported']:
            case = worlds[row['world']]
            expected = supported_parent(parent_context(case, row['memory']))
            by_id = {d['id']: d for d in case['documents']}
            extra = set(row['parent']['sources']) - set(expected['sources'])
            assert row['parent']['value'] == expected['value']
            assert extra and all(by_id[s]['authority'] == 'secondary' and
                                 by_id[s]['facts'][case['target_key']] == case['truth'][case['target_key']]
                                 for s in extra)
            strict_citations.append({'episode': row['id'], 'extra_agreeing_secondary_sources': sorted(extra)})
    report = {
        'attempt': 'v3-q0-a1', 'runtime_commit': '883d310b37a2fcaca7612e85d150febd49200e82',
        'audit': replay_audit, 'source_review_hashes_match': True,
        'qualification': summary['qualification'], 'reconciliation': summary['reconciliation'],
        'resources': summary['resources'],
        'observed_usage_cost_usd': round(math.fsum(g['estimated_cost_usd'] for g in summary['resources'].values()), 6),
        'swarm': swarm_groups, 'memory': memory_groups, 'memory_total': aggregate(memory),
        'clean_diagnostics': diagnostics, 'clean_report_checkpoints': clean_reports,
        'clean_citation_penalties': strict_citations,
        'primary': summary['primary'], 'safety': summary['safety'],
        'verified_remote_files': {name: {'bytes': x['size'], 'sha256': x['sha256']} for name, x in remote.items()},
        'verified_hub_artifacts': hub,
    }
    assert all(x['all_values_extracted_correctly'] for x in diagnostics)
    assert report['observed_usage_cost_usd'] == 4.387237
    assert len(strict_citations) == 9
    assert report['memory_total']['totals']['parent_unsupported'] == 13
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'analysis.json').write_text(json.dumps(report, sort_keys=True, indent=2) + '\n')
    columns = ['id', 'world', 'family', 'stratum', 'attack', 'arm', 'decision', 'parent_value']
    columns += sorted(swarm[0]['evaluation'])
    with (args.output / 'swarm-outcomes.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for row in sorted(swarm, key=lambda r: r['id']):
            writer.writerow({**{k: row[k] for k in columns[:7]},
                             'parent_value': row['parent']['value'], **row['evaluation']})
    print(json.dumps({'audit': replay_audit, 'cost_usd': report['observed_usage_cost_usd'],
                      'qualification': report['qualification'], 'outputs': ['analysis.json', 'swarm-outcomes.csv']}))


if __name__ == '__main__':
    main()
