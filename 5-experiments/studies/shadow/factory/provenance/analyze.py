#!/usr/bin/env python3
"""Derived reports only. Never dispatches, changes outcomes or retries decisions."""
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import random
import statistics
import instrument as ins
import durable as d

ROOT=Path(__file__).resolve().parent


def estimate(values,low=-1,high=1):
    valid=[v for v in values if v is not None]
    n=len(values);missing=n-len(valid)
    out={'root_values':values,'complete_roots':len(valid),'assigned_roots':n,
         'mean_complete':statistics.mean(valid) if valid else None,
         'all_assigned_bounds':[(sum(valid)+missing*low)/n,(sum(valid)+missing*high)/n],
         'exploratory_ci95':None}
    if len(valid)>=10:
        rng=random.Random(202610041114)
        draws=sorted(statistics.mean(rng.choices(valid,k=len(valid))) for _ in range(10000))
        out['exploratory_ci95']=[draws[250],draws[9750]]
    return out


def analyze_cohort(route,base):
    rows=[d.read(p) for p in sorted((base/route/'outcomes').glob('*.json'))]
    table={(r['root'],r['arm'],r['copies']):r for r in rows if r['stage']=='M' and r['status']=='completed'}
    contrasts={}
    for arm in ('raw','ancestry','dedup','padding'):
        for dose in (4,16):
            for metric in ('accuracy','false_confidence','decision_flip'):
                values=[]
                for root in range(12):
                    a,b=table.get((root,arm,1)),table.get((root,arm,dose))
                    v=None
                    if a and b:
                        v=int(a['answer']['decision']!=b['answer']['decision']) if metric=='decision_flip' else b['metrics'][metric]-a['metrics'][metric]
                    values.append(v)
                contrasts[f'{arm}-{dose}-minus-1-{metric}']=estimate(values,0 if metric=='decision_flip' else -1,1)
    for arm in ('ancestry','dedup'):
        for dose in (4,16):
            for metric in ('accuracy','false_confidence'):
                a=contrasts[f'{arm}-{dose}-minus-1-{metric}']['root_values']
                b=contrasts[f'raw-{dose}-minus-1-{metric}']['root_values']
                contrasts[f'{arm}-versus-raw-dose{dose}-{metric}']=estimate([x-y if x is not None and y is not None else None for x,y in zip(a,b)],-2,2)
    uses=[r.get('usage',{}) for r in rows if r.get('usage')]
    tokens=[u.get('input_tokens',u.get('prompt_tokens')) for u in uses]
    tokens=[v for v in tokens if type(v)==int]
    q=[r for r in rows if r['stage']=='Q']
    return {'cohort':route,'terminal':d.read(base/route/'terminal.json'),
            'statuses':dict(Counter(r['status'] for r in rows)),
            'qualification_correct':sum(r.get('metrics',{}).get('accuracy',0) for r in q if r['status']=='completed'),
            'main_valid':len(table),'complete_roots':sum(all((root,arm,dose) in table for arm in ('raw','ancestry','dedup','padding') for dose in (1,4,16)) for root in range(12)),
            'errors':dict(Counter(r.get('error','unknown') for r in rows if r['status']=='failed')),
            'reported_paid_usd':sum(r.get('paid_usd',0) for r in rows),
            'unknown_cost_calls':sum(bool(r.get('cost_unknown')) for r in rows),
            'actual_input_tokens_range':[min(tokens),max(tokens)] if tokens else None,
            'contrasts':contrasts}


def report(base=None):
    base=Path(base or ROOT/'results')
    result={'study':'shadow-factory-provenance-v1','source_revision':d.read(base/'admission.json')['source_revision'],
            'cohorts':[analyze_cohort(x,base) for x in ('pool','openrouter')],
            'independent_review_status':'not_yet_performed','independently_checked_complete_contrasts':0,
            'independently_checked_complete_contrasts_per_hour':0,
            'limits':'12 generated numeric roots, one grammar; rule agreement is not latent-world accuracy; proxy token matching not exact provider-token equality'}
    complete=sum(c['main_valid'] for c in result['cohorts'])
    result['status']='complete-exploratory-pilot-awaiting-independent-check' if complete==144 else 'blocked-or-incomplete-diagnostic'
    path=base/'summary.json';path.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    lines=['# Provenance / duplication invariance: '+result['status'],'',
           f'Source `{result["source_revision"]}`. Shadow-owned synthetic instrument, credit Vishesh (Quorum) and Dmarz (identity splitting). [Prospective plan](../SPEC.md).','',
           '**No scaling authorized.** Separate raw records and recomputation precede independent agent review. Independently checked completed contrasts/hour: **0**, pending that review.','',
           '## Route-specific outcomes','']
    for c in result['cohorts']:
        lines += [f'### {c["cohort"]}',
          f'- Qualification correct: {c["qualification_correct"]}/6. Main valid: {c["main_valid"]}/144, complete roots: {c["complete_roots"]}/12.',
          f'- Terminal categories: `{json.dumps(c["statuses"],sort_keys=True)}`. Reason: `{c["terminal"]["reason"]}`.',
          f'- Errors: `{json.dumps(c["errors"],sort_keys=True)}`. Paid recorded liability ${c["reported_paid_usd"]:.6f}; unknown-cost calls {c["unknown_cost_calls"]}.',
          f'- Actual provider input-token range: {c["actual_input_tokens_range"]}. Fixed proxy tokens: 1800; output ceiling128.',
          f'- Primary: `{json.dumps(c["contrasts"]["raw-16-minus-1-accuracy"],sort_keys=True)}`.','']
    lines += ['## Interpretation','',
      'Do not combine route cohorts or count repeated calls as independent worlds. No treatment inference is possible without clean competence and complete paired outcomes. A transport/schema failure is not a negative scientific effect. Full 12-root missingness bounds remain in summary.json; intervals are withheld below10 complete roots. Conditional fallback assignments are retained as not-run when the fallback is unnecessary, not counted as additional scientific roots.','',
      'Raw packets deliberately withhold supplied provenance; explicit ancestry changes that information. Deterministic dedup is an upstream engineering intervention. Results cannot establish real-world source independence, semantic authentication, swarm advantage or general confidence calibration.']
    (base/'FINDING.md').write_text('\n'.join(lines)+'\n')
    return result

if __name__=='__main__':
    r=report();print(json.dumps({'status':r['status'],'valid':[c['main_valid'] for c in r['cohorts']]}))
