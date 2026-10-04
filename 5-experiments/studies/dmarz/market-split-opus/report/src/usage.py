#!/usr/bin/env python3
"""Summarize billed usage for one attempt without reading private reasoning."""
import argparse
from collections import Counter
import json
from pathlib import Path
from statistics import median


def summarize(base, attempt):
    calls = []
    versions = set()
    bundles = 0
    for folder in sorted(Path(base).iterdir()):
        summary_path = folder / 'summary.json'
        if not summary_path.is_file():
            continue
        summary = json.loads(summary_path.read_text())
        params = summary['params']
        if params.get('attempt_id') != attempt:
            continue
        if params['backend'] != 'anthropic':
            raise ValueError('not_paid_attempt')
        versions.add((params['model'], params['engine_sha256'], params['design_sha256']))
        rows = [json.loads(line) for line in (folder / 'calls.jsonl').read_text().splitlines()]
        if sum(bool(row.get('accounting', {}).get('attempted')) for row in rows) != summary['metrics']['model_calls']:
            raise ValueError('call_accounting_mismatch')
        calls.extend(rows)
        bundles += 1
    if len(versions) != 1:
        raise ValueError('missing_or_mixed_configuration')
    if len({row['call_id'] for row in calls}) != len(calls):
        raise ValueError('duplicate_call')
    accounts = [row['accounting'] for row in calls if row.get('accounting', {}).get('attempted')]
    priced = [account for account in accounts if account.get('usage_reported')]
    outputs = [account['output_tokens'] for account in priced]
    latencies = [account['latency_seconds'] for account in accounts if 'latency_seconds' in account]
    model, engine, design = next(iter(versions))
    return {
        'attempt': attempt, 'model': model, 'engine_sha256': engine, 'design_sha256': design,
        'terminal_bundles_in_input': bundles, 'attempted_calls': len(accounts),
        'priced_calls': len(priced), 'unpriced_calls': len(accounts) - len(priced),
        'input_tokens': sum(account['input_tokens'] for account in priced),
        'output_tokens': sum(outputs),
        'maximum_output_tokens_per_call': max(outputs) if outputs else None,
        'median_output_tokens_per_call': median(outputs) if outputs else None,
        'p95_output_tokens_per_call': sorted(outputs)[max(0, int(.95 * len(outputs)) - 1)] if outputs else None,
        'calls_with_output_at_or_above_8192_ceiling': sum(value >= 8192 for value in outputs),
        'maximum_reported_request_seconds': max(latencies) if latencies else None,
        'api_cost_usd': round(sum(account['actual_usd'] for account in priced), 6),
        'median_reported_request_seconds': median(latencies) if latencies else None,
        'request_latency_observations': len(latencies),
        'call_statuses': dict(Counter(row['status'] for row in calls)),
        'recorded_stop_reasons': dict(Counter(account.get('stop_reason', 'not_recorded') for account in accounts)),
        'scope': 'Input bundles only; this summary does not assert cohort completeness. Billed token counts include thinking; no reasoning content is read or retained.'
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('base')
    parser.add_argument('attempt')
    parser.add_argument('--out')
    args = parser.parse_args()
    result = summarize(args.base, args.attempt)
    text = json.dumps(result, indent=2) + '\n'
    if args.out:
        with Path(args.out).open('x') as stream:
            stream.write(text)
    print(text, end='')
