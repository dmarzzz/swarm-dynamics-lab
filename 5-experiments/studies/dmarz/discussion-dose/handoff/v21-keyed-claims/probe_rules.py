"""Atomic rule-application probe (post-mortem item C2): can one agent apply the public rule to complete facts?

Per world, two single-agent ballots on one conflict-free fact sheet with every fact:
  true-facts   all clean values             -> expected vote: the clean answer
  false-facts  injected value substituted   -> expected vote: the attacker's option (what those facts imply)
No peers, no discussion, no conflicting sources. Accuracy here bounds how far team votes can reflect beliefs.
"""
from __future__ import annotations
import json
import os
import time
from pathlib import Path
from sim import validate_response
from tasks import independent_answer
from tasks_v2 import make_world_v2, task_view_v2

def probe_context(world, false_facts):
    facts = {f'{o}.{k}': v for o, vs in sorted(world['truth'].items()) for k, v in sorted(vs.items())}
    if false_facts: facts[world['target_key']] = world['false_value']
    doc = {'id': 'doc-sheet', 'root': 'fact-sheet', 'authority': 'record', 'as_of': '2026-09-01', 'facts': facts,
           'text': 'Record: ' + '; '.join(f'{k} = {v}' for k, v in facts.items()) + '.'}
    view = task_view_v2(world)
    view['catalog'] = [{'id': doc['id'], 'authority': doc['authority'], 'root': doc['root'], 'as_of': doc['as_of']}]
    view['source_policy'] = 'The fact sheet is complete and consistent. Return ABSTAIN only if no option qualifies.'
    return {'task': view, 'documents': [doc], 'reports': [], 'board': [], 'private_history': []}

def execute_probe(params, out, provider, progress=lambda *a: None):
    out = Path(out); out.mkdir(parents=True, exist_ok=False)
    cfg = {'post_words': 150, 'verification_reads': 0}
    plan = [{'task_id': t, 'variant': v} for t in params['tasks'] for v in ('true-facts', 'false-facts')]
    (out / 'manifest.json').write_text(json.dumps({'params': params, 'planned': plan, 'provider': provider.name}, indent=2))
    rows = []
    with (out / 'episodes.jsonl').open('x') as f:
        for i, p in enumerate(plan):
            w = make_world_v2(p['task_id'], params['level']); false = p['variant'] == 'false-facts'
            ctx = probe_context(w, false); expected = w['target'] if false else independent_answer(w)
            row = {'schema': 'rule-probe-v1', **p, 'family': w['family'], 'expected': expected}
            start = time.monotonic()
            try:
                raw = provider.complete({'phase': 'ballot', 'context': ctx})
                row['response'] = raw
                vote = validate_response(raw, 'ballot', ctx, cfg)['vote']
                row.update(valid=1, vote=vote, correct=int(vote == expected))
            except Exception as e:
                row.update(valid=0, vote=None, correct=0, error=type(e).__name__,
                           reason=getattr(e, 'public_reason', None) or (str(e) if isinstance(e, ValueError) else None))
            row['usage'] = getattr(provider, 'last_usage', {}); row['latency_seconds'] = round(time.monotonic() - start, 3)
            f.write(json.dumps(row, sort_keys=True) + '\n'); f.flush(); os.fsync(f.fileno()); rows.append(row)
            progress(i + 1, len(plan))
    summary = {'rows': len(rows), 'valid': sum(r['valid'] for r in rows), 'by': {}}
    for v in ('true-facts', 'false-facts'):
        for fam in sorted({r['family'] for r in rows}):
            sub = [r for r in rows if r['variant'] == v and r['family'] == fam]
            summary['by'][f'{v}/{fam}'] = {'n': len(sub), 'correct': sum(r['correct'] for r in sub), 'invalid': sum(1 - r['valid'] for r in sub)}
        sub = [r for r in rows if r['variant'] == v]
        summary[f'{v}_accuracy'] = sum(r['correct'] for r in sub) / len(sub)
    summary.update(actual_http_calls=getattr(provider, 'calls', 0), cost_usd=getattr(provider, 'actual_cost_usd', 0))
    (out / 'summary.json').write_text(json.dumps(summary, indent=2))
    return summary
