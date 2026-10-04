"""Software gates between stages. A stage is queued only when exactly one run of the previous
stage is `done` at the same source hash with no invalid row and its gate passed, and a batch
name is never queued twice. Documents and reviews are outside the source hash.

Two pre-registered models share the hub experiment. Every gate looks only at runs of this chain's model
(params.model); batch names carry the model tag. The two chains may run at the same time on different
servers: a run of the other model that is assigned or running does not block a stage, but a planned
(not yet taken) run of either model does, because the hub hands out the next planned run of the
experiment and a chain must never take the other model's run.

One exception to "a stage is never queued twice": after S1 stopped on a billing outage
(`provider_credit_balance_low`), a continuation batch `s1-<attempt>-r<n>` may be queued for exactly
the units left not started (chain.py resume)."""
import yaml

import study

PREREQUISITE = {'P0': 'S0', 'Q0': 'P0', 'S1': 'Q0'}


class GateRefused(ValueError):
    pass


def _runs(sr):
    return sr.runs(study.EXPERIMENT, limit=5000)


def _mine(runs):
    model = study.config_name()
    return [r for r in runs if (r.get('params') or {}).get('model') == model]


def _busy(runs):
    """A planned run of any model, or an assigned or running run of this chain's model."""
    return any(r.get('status') == 'planned' for r in runs) or any(r.get('status') in ('assigned', 'running') for r in _mine(runs))


def _passed(runs, stage, source_hash):
    return [r for r in _mine(runs) if (r.get('params') or {}).get('stage') == stage
            and (r.get('params') or {}).get('source_hash') == source_hash and r.get('status') == 'done'
            and (r.get('metrics') or {}).get('invalid') == 0 and (r.get('metrics') or {}).get('qualification_passed') == 1]


def check(sr, stage):
    """Returns (params, prerequisite run or None) or raises GateRefused. Queues nothing."""
    p = study.params(stage); runs = _runs(sr)
    if any((r.get('params') or {}).get('batch') == p['batch'] for r in runs):
        raise GateRefused('batch_exists_no_replay')
    if _busy(runs):
        raise GateRefused('queue_not_empty')
    before = PREREQUISITE.get(stage); run = None
    if before:
        candidates = _passed(runs, before, p['source_hash'])
        if len(candidates) != 1:
            raise GateRefused('exact_runtime_qualification_required')
        run = candidates[0]
    return p, run


def passed_run(sr, stage):
    """The single passed run of a stage at the current source hash, or None."""
    candidates = _passed(_runs(sr), stage, study.source_hash())
    return candidates[0] if len(candidates) == 1 else None


def enqueue(sr, stage):
    p, _ = check(sr, stage)
    exp = yaml.safe_load((study.ROOT / 'experiment.yaml').read_text())
    sr.register(exp.pop('id'), **exp)
    return sr.enqueue(study.EXPERIMENT, [p], tags=[stage, p['backend'], 'exploratory'])


def check_continuation(sr, n):
    """Returns params for continuation n of S1 or raises GateRefused. Queues nothing. Allowed only
    when the latest S1 run at this source hash ended failed and resumable (a billing stop)."""
    p = dict(study.params('S1')); original = p['batch']; p.update(batch=f'{original}-r{n}', continuation=n)
    runs = _runs(sr)
    if any((r.get('params') or {}).get('batch') == p['batch'] for r in runs):
        raise GateRefused('batch_exists_no_replay')
    if _busy(runs):
        raise GateRefused('queue_not_empty')
    if len(_passed(runs, 'Q0', p['source_hash'])) != 1:
        raise GateRefused('exact_runtime_qualification_required')
    chain = [original] + [f'{original}-r{i}' for i in range(1, n)]
    by_batch = {}
    for r in _mine(runs):
        if (r.get('params') or {}).get('source_hash') == p['source_hash']: by_batch.setdefault((r.get('params') or {}).get('batch'), []).append(r)
    if any(len(by_batch.get(b, [])) != 1 for b in chain):
        raise GateRefused('earlier_s1_runs_missing')
    last = by_batch[chain[-1]][0]
    if last.get('status') != 'failed' or (last.get('metrics') or {}).get('resumable') != 1:
        raise GateRefused('last_s1_run_is_not_a_billing_stop')
    return p


def enqueue_continuation(sr, n):
    p = check_continuation(sr, n)
    return sr.enqueue(study.EXPERIMENT, [p], tags=['S1', p['backend'], 'exploratory', 'continuation'])
