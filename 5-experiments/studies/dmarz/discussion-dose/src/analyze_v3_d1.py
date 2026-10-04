"""Export audited D1 scores without actor contexts or private deployment metadata."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import statistics


def read(path):
    return json.loads(path.read_text())


def write_csv(path, rows):
    fields = sorted({key for row in rows for key in row})
    with path.open('x', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('verified_directory', type=Path)
    p.add_argument('output', type=Path)
    args = p.parse_args()
    verification = read(args.verified_directory / 'verification.json')
    local_audit = read(args.verified_directory / 'local-exact-audit.json')
    assert local_audit['ok'] and local_audit['complete_journal']
    records = args.verified_directory / 'records'
    assert verification['audit']['ok'] and verification['audit']['complete_journal']
    for row in verification['verified_files']:
        raw = (records / row['name']).read_bytes()
        assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
    manifest = read(records / 'manifest.json')
    assert manifest['scientific'] is True and manifest['attempt'] == 'v3-d1-a1'
    summary = read(records / 'summary.json'); outcomes = read(records / 'outcomes.json')
    assert summary['assigned_calls'] == len(manifest['schedule']) == 120
    assert len(outcomes) == summary['terminal'] and len({r['call_id'] for r in outcomes}) == len(outcomes)
    assert verification['audit']['outcomes_recomputed'] == len(outcomes)
    assert local_audit['outcomes_recomputed'] == len(outcomes)
    cache_tokens = sum(r['usage'].get('cache_read_input_tokens', 0) + r['usage'].get('cache_creation_input_tokens', 0) for r in outcomes)
    assert cache_tokens == 0, 'Cached-token pricing needs an explicit analysis amendment'
    rows = []
    for row in outcomes:
        usage = row['usage']; answer = row['response'] or {}; score = row['score']
        rates = manifest['rates_usd_per_million'][row['model']]
        cost = (usage['input_tokens'] * rates['input'] + usage['output_tokens'] * rates['output']) if all(k in usage for k in ('input_tokens', 'output_tokens')) else None
        rows.append({**{k: row[k] for k in ('call_id', 'pair', 'q0_call_id', 'model', 'status', 'reason', 'latency_seconds', 'dispatched')},
                     **{k: score.get(k) for k in ('group', 'world', 'agent', 'state', 'family', 'variant')},
                     'vote': answer.get('vote'), 'parent_value': answer.get('value'),
                     'input_tokens': usage.get('input_tokens'), 'output_tokens': usage.get('output_tokens'),
                     'observed_cost_microusd': cost, **score['evaluation']})
    models = {}
    for name, model in summary['models'].items():
        keep = {k: v for k, v in model.items() if k != 'latency_seconds'}
        latency = model['latency_seconds']
        keep['latency'] = {'observed': len(latency), 'sum_seconds': round(sum(latency), 6),
                           'median_seconds': statistics.median(latency) if latency else None,
                           'max_seconds': max(latency) if latency else None}
        models[name] = keep
        own = [r for r in rows if r['model'] == name]
        assert len(own) == model['terminal']
        assert sum(r['observed_cost_microusd'] or 0 for r in own) == model['observed_usage_cost_microusd']
        assert sum(r.get('truth_correct') == 1 for r in own if r['group'] == 'diagnostic') == model['diagnostic_gate']['full_evidence_correct']
    result = {'attempt': manifest['attempt'], 'source_commit': manifest['source_commit'],
              'frozen_manifest_sha256': manifest['preflight']['manifest_sha256'],
              'assigned_calls': summary['assigned_calls'], 'started': summary['started'],
              'terminal': summary['terminal'], 'unresolved': summary['unresolved'],
              'models': models, 'qualification': False, 'holdout_opened': False,
              'successors_dispatched': False, 'limitations': summary['limitations'],
              'verified_raw_files': verification['verified_files'],
              'retained_archive_sha256': verification['archive_sha256'],
              'exact_source_audit': verification['audit'],
              'local_exact_source_audit': {k: v for k, v in local_audit.items() if k != 'summary'},
              'cache_tokens_observed': cache_tokens}
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'analysis.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    write_csv(args.output / 'per-item.csv', rows)
    (args.output / 'paired-differences.json').write_text(json.dumps(summary['paired_items'], sort_keys=True, indent=2) + '\n')
    print(json.dumps({'assigned': 120, 'terminal': len(rows), 'gates': {m: v['diagnostic_gate'] for m, v in models.items()},
                      'observed_cost_usd': sum(m['observed_usage_cost_microusd'] for m in models.values()) / 1e6}))


if __name__ == '__main__':
    main()
