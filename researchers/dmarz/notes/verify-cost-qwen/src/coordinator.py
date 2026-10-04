"""Software gates between stages. A stage is queued only when exactly one run of the previous stage is
`done` at the same source hash with no invalid row and its gate passed, and a batch name is never
queued twice. Documents and reviews are outside the source hash, so a post-mortem-only commit does not
invalidate a qualification.

One exception to "a stage is never queued twice": after S1 stopped on a billing outage
(`provider_credit_balance_low`), a continuation batch `s1-001-r<n>` may be queued for exactly the units
that stop left not started. It needs the same qualification as S1 and the stopped S1 run."""
import yaml

import study

PREREQUISITE = {'P0': 'S0', 'Q0': 'P0', 'S1': 'Q0'}
ACTIVE = ('planned', 'assigned', 'running')


class GateRefused(ValueError):
    pass


def _params(r):
    return r.get('params') or {}


def passed_runs(runs, stage, source_hash):
    """Runs of `stage` at this source hash that are done with no invalid row and a passed gate."""
    return [r for r in runs if _params(r).get('stage') == stage and _params(r).get('source_hash') == source_hash
            and r.get('status') == 'done' and (r.get('metrics') or {}).get('invalid') == 0
            and (r.get('metrics') or {}).get('qualification_passed') == 1]


def check(sr, stage):
    """Returns (params, prerequisite run or None) or raises GateRefused. Queues nothing."""
    p = study.params(stage)
    runs = sr.runs(study.EXPERIMENT, limit=5000)
    if any(_params(r).get('batch') == p['batch'] for r in runs): raise GateRefused('batch_exists_no_replay')
    if any(r.get('status') in ACTIVE for r in runs): raise GateRefused('queue_not_empty')
    before = PREREQUISITE.get(stage); run = None
    if before:
        candidates = passed_runs(runs, before, p['source_hash'])
        if len(candidates) != 1: raise GateRefused('exact_runtime_qualification_required')
        run = candidates[0]
    return p, run


def probe_run(sr):
    """The one passed P0 run at this source hash, or raises GateRefused."""
    candidates = passed_runs(sr.runs(study.EXPERIMENT, limit=5000), 'P0', study.source_hash())
    if len(candidates) != 1: raise GateRefused('exact_runtime_probe_required')
    return candidates[0]


def enqueue(sr, stage):
    p, _ = check(sr, stage)
    exp = yaml.safe_load((study.ROOT / 'experiment.yaml').read_text())
    sr.register(exp.pop('id'), **exp)
    return sr.enqueue(study.EXPERIMENT, [p], tags=[stage, p['backend'], 'exploratory'])


def check_continuation(sr, n):
    """Returns (params, original S1 run) for continuation n of S1 or raises GateRefused. Queues nothing."""
    p = dict(study.params('S1')); original = p['batch']; p.update(batch=f'{original}-r{n}', continuation=n)
    runs = sr.runs(study.EXPERIMENT, limit=5000)
    if any(_params(r).get('batch') == p['batch'] for r in runs): raise GateRefused('batch_exists_no_replay')
    if any(r.get('status') in ACTIVE for r in runs): raise GateRefused('queue_not_empty')
    if len(passed_runs(runs, PREREQUISITE['S1'], p['source_hash'])) != 1: raise GateRefused('exact_runtime_qualification_required')
    earlier = [r for r in runs if _params(r).get('stage') == 'S1' and _params(r).get('source_hash') == p['source_hash']]
    names = sorted(_params(r).get('batch') for r in earlier)
    if names != sorted([original] + [f'{original}-r{i}' for i in range(1, n)]) or any(r.get('status') != 'failed' for r in earlier):
        raise GateRefused('stopped_main_stage_required')
    return p, next(r for r in earlier if _params(r).get('batch') == original)


def enqueue_continuation(sr, n):
    p, original = check_continuation(sr, n)
    p['continuation_of'] = original.get('run') or original.get('id')
    return sr.enqueue(study.EXPERIMENT, [p], tags=['S1', p['backend'], 'exploratory', 'continuation'])
