"""Freeze an exact finite manifest; do not open the confirmatory holdout."""
import argparse
import json
import random
import re
import time
from pathlib import Path
import common


def assignments(stage, attempt=None):
    d=common.design()
    if stage == 'I0':
        diagnostic = d['diagnostics'].get(attempt, {})
        if diagnostic.get('mode') != 'closed-loop' or diagnostic.get('withdrawn_before_dispatch'): raise ValueError('unregistered_diagnostic')
        rows = []
        for case in diagnostic['cases']:
            if case['domain'] not in ('D1','D2') or case['task_id'] >= d['holdout_min_task_id']: raise ValueError('heldout_task')
            if case['arm'] not in ('C','S'): raise ValueError('diagnostic_arm')
            conditions = list(diagnostic.get('conditions', ['original','clarified']))
            if not conditions or len(set(conditions)) != len(conditions) or set(conditions) - {'original','clarified'}: raise ValueError('diagnostic_conditions')
            random.Random(f'{attempt}:{case}').shuffle(conditions)
            rows += [dict(**case, condition=c, seed=0) for c in conditions]
        return rows
    if stage not in ('S0','Q0','P1'): raise ValueError('stage_disabled')
    s=d['stages'][stage]; rows=[]
    if any(a not in d['arms'] for a in s['arms']): raise ValueError('arm_disabled')
    if s['backend']!='scripted' and 'D3' in s['domains']: raise ValueError('heldout_domain')
    if any(t>=d['holdout_min_task_id'] for t in s['tasks']): raise ValueError('heldout_task')
    for t in s['tasks']:
        for domain in s['domains']:
            for variant in s['variants']:
                arms=list(s['arms']); random.Random(f'{t}:{domain}:{variant}:arm-order').shuffle(arms)
                rows += [dict(task_id=t,domain=domain,variant=variant,arm=a,seed=0) for a in arms]
    return rows


def prepare(stage, attempt, qualification=None):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}',attempt): raise ValueError('bad_attempt_id')
    commit=common.frozen(attempt); aa=assignments(stage, attempt)
    if stage=='P1':
        if not qualification: raise ValueError('qualification_required')
        qpath=Path(qualification)
        q=json.loads((qpath/'summary.json').read_text()); qm=json.loads((qpath/'manifest.json').read_text())
        if q['stage']!='Q0' or not q.get('qualification_pass') or qm['hashes']!=common.hashes(): raise ValueError('qualification_not_current')
    out=common.ROOT/'results'/attempt
    out.mkdir(parents=True,exist_ok=False)
    registration=json.loads((common.ROOT/'registration'/f'{attempt}.json').read_text())
    common.dump(out/'public-plan-receipt.json',dict(registration,launch_verified_at=time.time()))
    m=dict(attempt=attempt,stage=stage,commit=commit,hashes=common.hashes(),created=time.time(),
           backend='anthropic' if stage=='I0' else common.design()['stages'][stage]['backend'],assignments=aa,
           plan_url=registration['url'],registered_tldr=registration['registered_tldr'],
           qualification=str(qualification) if qualification else None)
    if stage=='I0': m['parent_attempt']=common.design()['diagnostics'][attempt]['parent_attempt']
    m.update(model=common.design()['model'],inference=common.design().get('inference'))
    common.dump(out/'manifest.json',m)
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('stage'); p.add_argument('attempt'); p.add_argument('--qualification'); a=p.parse_args()
    print(prepare(a.stage,a.attempt,a.qualification))
