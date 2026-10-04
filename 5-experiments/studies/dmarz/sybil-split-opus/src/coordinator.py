"""Software gates between stages. A stage is queued only when exactly one run of the previous
stage is `done` at the same source hash with no invalid row and its gate passed, and a batch
name is never queued twice. Documents and reviews are outside the source hash, so a
post-mortem-only commit does not invalidate a qualification."""
import yaml

import study

PREREQUISITE = {'P0': 'S0', 'Q0': 'P0', 'S1': 'Q0'}


class GateRefused(ValueError):
    pass


def check(sr, stage):
    """Returns (params, prerequisite run or None) or raises GateRefused. Queues nothing."""
    p = study.params(stage)
    runs = sr.runs(study.EXPERIMENT, limit=5000)
    if any((r.get('params') or {}).get('batch') == p['batch'] for r in runs):
        raise GateRefused('batch_exists_no_replay')
    if any(r.get('status') in ('planned', 'assigned', 'running') for r in runs):
        raise GateRefused('queue_not_empty')
    before = PREREQUISITE.get(stage); run = None
    if before:
        candidates = [r for r in runs if (r.get('params') or {}).get('stage') == before
                      and (r.get('params') or {}).get('source_hash') == p['source_hash'] and r.get('status') == 'done'
                      and (r.get('metrics') or {}).get('invalid') == 0
                      and (r.get('metrics') or {}).get('qualification_passed') == 1]
        if len(candidates) != 1:
            raise GateRefused('exact_runtime_qualification_required')
        run = candidates[0]
    return p, run


def enqueue(sr, stage):
    p, _ = check(sr, stage)
    exp = yaml.safe_load((study.ROOT / 'experiment.yaml').read_text())
    sr.register(exp.pop('id'), **exp)
    return sr.enqueue(study.EXPERIMENT, [p], tags=[stage, p['backend'], 'exploratory'])
