"""Software gates between stages. A stage is queued only when exactly one run of the previous
stage exists at the same source hash and it is `done` with no invalid row and its gate passed,
and a batch name is never queued twice. Documents and reviews are outside the source hash, so a
docs-only commit does not invalidate a qualification.

One exception to "a stage is never queued twice": after S1 stopped on a billing outage
(`provider_credit_balance_low`), a continuation batch `s1-<attempt>-r<n>` may be queued for exactly
the assignments that stop left not started. It needs the same passed qualification as S1 and the
stopped S1 run (and every earlier continuation) on the hub with status failed."""
import yaml

import study

PREREQUISITE = {'P0': 'S0', 'Q0': 'P0', 'S1': 'Q0'}


class GateRefused(ValueError):
    pass


def _params(run):
    return run.get('params') or {}


def _passed(runs, stage, source_hash):
    """Exactly one run of `stage` at this source hash, and it passed. Returns it or raises."""
    same = [r for r in runs if _params(r).get('stage') == stage and _params(r).get('source_hash') == source_hash]
    good = [r for r in same if r.get('status') == 'done' and (r.get('metrics') or {}).get('invalid') == 0
            and (r.get('metrics') or {}).get('qualification_passed') == 1]
    if len(same) != 1 or len(good) != 1:
        raise GateRefused(f'exact_runtime_qualification_required:{stage}')
    return good[0]


def check(sr, stage):
    """Returns (params, the passed run of the previous stage or None) or raises GateRefused. Queues nothing."""
    p = study.params(stage)
    runs = sr.runs(study.EXPERIMENT, limit=5000)
    if any(_params(r).get('batch') == p['batch'] for r in runs):
        raise GateRefused('batch_exists_no_replay')
    if any(r.get('status') in ('planned', 'assigned', 'running') for r in runs):
        raise GateRefused('queue_not_empty')
    before = PREREQUISITE.get(stage)
    return p, _passed(runs, before, p['source_hash']) if before else None


def register(sr):
    exp = yaml.safe_load((study.ROOT / 'experiment.yaml').read_text())
    assert exp['id'] == study.EXPERIMENT
    sr.register(exp.pop('id'), **exp)


def enqueue(sr, stage):
    p, _ = check(sr, stage)
    register(sr)
    return sr.enqueue(study.EXPERIMENT, [p], tags=[stage, p['backend'], 'exploratory'])


def check_continuation(sr, n):
    """Returns (params, the original S1 run) for continuation n of S1 or raises GateRefused. Queues nothing."""
    p = dict(study.params('S1')); original = p['batch']; p.update(batch=f'{original}-r{n}', continuation=n)
    runs = sr.runs(study.EXPERIMENT, limit=5000)
    if any(_params(r).get('batch') == p['batch'] for r in runs):
        raise GateRefused('batch_exists_no_replay')
    if any(r.get('status') in ('planned', 'assigned', 'running') for r in runs):
        raise GateRefused('queue_not_empty')
    _passed(runs, PREREQUISITE['S1'], p['source_hash'])
    earlier = [r for r in runs if _params(r).get('stage') == 'S1' and _params(r).get('source_hash') == p['source_hash']]
    names = sorted(_params(r).get('batch') for r in earlier)
    if names != sorted([original] + [f'{original}-r{i}' for i in range(1, n)]) or any(r.get('status') != 'failed' for r in earlier):
        raise GateRefused('stopped_main_stage_required')
    return p, next(r for r in earlier if _params(r).get('batch') == original)


def enqueue_continuation(sr, n):
    p, original = check_continuation(sr, n)
    p['continuation_of'] = original.get('run') or original.get('id')
    return sr.enqueue(study.EXPERIMENT, [p], tags=['S1', p['backend'], 'exploratory', 'continuation'])
