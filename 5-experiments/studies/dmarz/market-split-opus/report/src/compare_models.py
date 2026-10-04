#!/usr/bin/env python3
"""Side-by-side descriptive table of two model cohorts that ran on DIFFERENT market tasks.

Nothing is pooled and nothing is paired across models: the Sonnet pilot used tasks 36-41 and
this study uses 110-115. Inputs are each study's saved paired-task table and usage summary."""
import argparse, csv, json
from pathlib import Path
from statistics import mean

def cells(path):
    rows = list(csv.DictReader(Path(path).open()))
    out = {}
    for rule in ('none', 'firm', 'owner'):
        rs = [r for r in rows if r['regulator'] == rule]
        out[rule] = {'tasks': sorted(int(r['task_id']) for r in rs), 'flexible_episodes': len(rs),
                     'registered': sum(r['registered_round'] != '' for r in rs),
                     'sustained_fragmentation': sum(r['dynamic_fragmentation'] == 'True' for r in rs),
                     'sustained_evasion': sum(r['dynamic_evasion'] == 'True' for r in rs),
                     'mean_flexible_profit': mean(float(r['dynamic_profit']) for r in rs),
                     'mean_locked_profit': mean(float(r['locked_profit']) for r in rs),
                     'mean_paired_profit_difference': mean(float(r['profit_difference']) for r in rs),
                     'mean_flexible_fines': mean(float(r['dynamic_fines']) for r in rs),
                     'mean_locked_fines': mean(float(r['locked_fines']) for r in rs)}
    by = {(int(r['task_id']), r['regulator']): r for r in rows}
    tasks = sorted({t for t, _ in by})
    diffs = [int(by[t, 'firm']['dynamic_fragmentation'] == 'True') - int(by[t, 'owner']['dynamic_fragmentation'] == 'True') for t in tasks]
    return out, {'task_clusters': len(tasks), 'task_differences': dict(zip(tasks, diffs)), 'paired_difference': mean(diffs)}

def usage(path):
    u = json.loads(Path(path).read_text())
    n = u['priced_calls']
    return {'model': u['model'], 'calls': u['attempted_calls'], 'input_tokens': u['input_tokens'], 'output_tokens': u['output_tokens'],
            'input_tokens_per_call': u['input_tokens'] / n, 'output_tokens_per_call': u['output_tokens'] / n,
            'median_output_tokens_per_call': u['median_output_tokens_per_call'], 'maximum_output_tokens_per_call': u['maximum_output_tokens_per_call'],
            'api_cost_usd': u['api_cost_usd'], 'median_request_seconds': u['median_reported_request_seconds']}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for name in ('sonnet_pairs', 'sonnet_usage', 'opus_pairs', 'opus_usage', 'out'): p.add_argument(name)
    a = p.parse_args()
    result = {'scope': 'Two model configurations on different market tasks from one generator. Descriptive, not pooled, not paired across models. Request settings differ (thinking control, output ceiling, tokenizer); see the study README.', 'cohorts': {}}
    for label, pairs, use in (('sonnet-4-6 pilot, tasks 36-41', a.sonnet_pairs, a.sonnet_usage), ('opus-5-5 replication, tasks 110-115', a.opus_pairs, a.opus_usage)):
        c, contrast = cells(pairs)
        result['cohorts'][label] = {'by_regulation': c, 'primary_contrast_firm_minus_owner': contrast, 'usage': usage(use)}
    Path(a.out).write_text(json.dumps(result, indent=2) + '\n'); print(json.dumps(result, indent=2))
