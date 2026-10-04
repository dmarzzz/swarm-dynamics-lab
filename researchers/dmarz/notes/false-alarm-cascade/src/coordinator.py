"""The software gate. A stage is queued only behind exactly one passed run of the previous stage
at the same source hash, and a batch name is never queued twice (no replay).

One more door, for the billing-outage rule: a continuation of S1 (batch `s1-001-r<k>`) is queued
only when S1 and every earlier continuation at this source hash ended `failed` with the hub metric
`billing_stop == 1`, that is, stopped by `provider_credit_balance_low` and by nothing else."""
import yaml

import study

PREREQUISITE = {'P0': 'S0', 'Q0': 'P0', 'S1': 'Q0'}


def gate(runs, stage, p):
    """Raise ValueError unless `stage` may be queued given the experiment's hub runs."""
    if any((r.get('params') or {}).get('batch') == p['batch'] for r in runs):
        raise ValueError('batch_exists_no_replay')
    previous = PREREQUISITE.get(stage)
    if previous:
        # S0 is model-free; a paid prerequisite must be on the same model (one ladder rung never
        # qualifies another).
        same = [r for r in runs if (r.get('params') or {}).get('stage') == previous
                and (r.get('params') or {}).get('source_hash') == p['source_hash']
                and (previous == 'S0' or (r.get('params') or {}).get('model') == p['model'])]
        passed = [r for r in same if r.get('status') == 'done'
                  and (r.get('metrics') or {}).get('invalid') == 0
                  and (r.get('metrics') or {}).get('qualification_passed') == 1]
        # Exactly one run of the previous stage at this source hash, and it passed.
        if len(same) != 1 or len(passed) != 1:
            raise ValueError(f'exact_runtime_qualification_required:{previous}')


def resume_gate(runs, p, continuation):
    """Raise ValueError unless the k-th continuation of S1 may be queued."""
    if continuation < 1 or p != study.params('S1', continuation):
        raise ValueError('resume_params_mismatch')
    gate(runs, 'S1', p)                         # the batch is new and Q0 passed exactly once at this hash
    family = [study.params('S1', k)['batch'] for k in range(continuation)]
    for batch in family:
        same = [r for r in runs if (r.get('params') or {}).get('batch') == batch
                and (r.get('params') or {}).get('source_hash') == p['source_hash']]
        if len(same) != 1 or same[0].get('status') != 'failed' or (same[0].get('metrics') or {}).get('billing_stop') != 1:
            raise ValueError('resume_requires_credit_stop')
    later = [r for r in runs if (r.get('params') or {}).get('stage') == 'S1'
             and (r.get('params') or {}).get('source_hash') == p['source_hash']
             and (r.get('params') or {}).get('model') == p['model']
             and (r.get('params') or {}).get('batch') not in family]
    if later:
        raise ValueError('resume_out_of_order')


def enqueue(sr, stage, continuation=0):
    p = study.params(stage, continuation)
    runs = sr.runs(study.EXPERIMENT, limit=5000)
    if continuation:
        resume_gate(runs, p, continuation)
    else:
        gate(runs, stage, p)
    exp = yaml.safe_load((study.ROOT / 'experiment.yaml').read_text())
    assert exp['id'] == study.EXPERIMENT
    sr.register(exp.pop('id'), **exp)
    return sr.enqueue(study.EXPERIMENT, [p], tags=[stage, p['backend'], 'exploratory'])
