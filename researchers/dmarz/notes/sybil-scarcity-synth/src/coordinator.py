"""The software gate. A stage is queued only behind exactly one passed run of the previous stage
at the same source hash, and a batch name is never queued twice (no replay).

Model ladder: batch names and the `model` parameter carry the model of an attempt. S0 is scripted
and model-free, so one passed S0 serves every model; P0, Q0 and S1 are gated per model, and a
qualification on one model never qualifies another.

A run that a billing outage stopped (`provider_credit_balance_low`) may be continued by
`<batch>-r1`, `-r2`, ...; the original run and its continuations count as one run of the stage:
it passed when every part but the last ended with a billing stop and the last part is `done`
with `invalid == 0` and `qualification_passed == 1`.
"""
import re

import yaml

import study

PREREQUISITE = {'P0': 'S0', 'Q0': 'P0', 'S1': 'Q0'}


def _params(r):
    return r.get('params') or {}


def _metrics(r):
    return r.get('metrics') or {}


def stage_runs(runs, stage, source_hash, model=None):
    """Runs of one stage for one model at one source hash, ordered: the original batch, then -r1, -r2, ...

    Batch names carry the model (`q0-001` for the first model of the ladder, `q0-001-opus-5` for the
    second), so the runs of another model never count here. S0 is scripted and model-free.
    """
    base = study.base_batch(stage, model)
    wanted = study.stage_model(stage, model)

    def part(r):
        match = re.fullmatch(re.escape(base) + r'(?:-r([1-9][0-9]*))?', str(_params(r).get('batch')))
        return None if not match else int(match.group(1) or 0)
    same = [r for r in runs if _params(r).get('stage') == stage and _params(r).get('source_hash') == source_hash
            and _params(r).get('model') == wanted]
    return sorted(same, key=lambda r: (part(r) is None, part(r) or 0)), [part(r) for r in same]


def is_billing_stop(r):
    return r.get('status') == 'failed' and _metrics(r).get('billing_stop') == 1


def stage_passed(runs, stage, source_hash, model=None):
    """Exactly one run of the stage for this model at this hash (a continuation chain counts as one), and it passed."""
    ordered, parts = stage_runs(runs, stage, source_hash, model)
    if not ordered or None in parts or sorted(parts) != list(range(len(parts))):
        return False
    last = ordered[-1]
    return (all(is_billing_stop(r) for r in ordered[:-1])
            and last.get('status') == 'done' and _metrics(last).get('invalid') == 0
            and _metrics(last).get('qualification_passed') == 1)


def gate(runs, stage, p):
    """Raise ValueError unless the run `p` of `stage` may be queued given the experiment's hub runs."""
    if any(_params(r).get('batch') == p['batch'] for r in runs):
        raise ValueError('batch_exists_no_replay')
    model = None if stage == 'S0' else p['model']
    if p.get('model') != study.stage_model(stage, model) or (model and model not in study.design()['model_ladder']):
        raise ValueError('model_not_in_ladder')
    previous = PREREQUISITE.get(stage)
    # P0 needs the model-free S0; Q0 needs the P0 of the same model; S1 needs the Q0 of the same model.
    if previous and not stage_passed(runs, previous, p['source_hash'], model):
        raise ValueError(f'exact_runtime_qualification_required:{previous}')
    if 'continues' in p:
        # A continuation needs the chain so far to end in a billing stop, and the next free number.
        ordered, parts = stage_runs(runs, stage, p['source_hash'], model)
        expected = study.params(stage, len(ordered), model)
        if (not ordered or None in parts or sorted(parts) != list(range(len(parts)))
                or not all(is_billing_stop(r) for r in ordered)
                or p['batch'] != expected['batch'] or p['continues'] != expected['continues']):
            raise ValueError('continuation_requires_billing_stop')
    elif p['batch'] != study.base_batch(stage, model):
        raise ValueError('batch_name_not_allowed')


def register(sr):
    exp = yaml.safe_load((study.ROOT / 'experiment.yaml').read_text())
    assert exp['id'] == study.EXPERIMENT
    sr.register(exp.pop('id'), **exp)


def enqueue(sr, stage, part=0):
    p = study.params(stage, part)
    runs = sr.runs(study.EXPERIMENT, limit=5000)
    gate(runs, stage, p)
    register(sr)
    return sr.enqueue(study.EXPERIMENT, [p], tags=[stage, p['backend'], 'exploratory'])
