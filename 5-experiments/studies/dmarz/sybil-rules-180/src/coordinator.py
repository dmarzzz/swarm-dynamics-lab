"""The software gates. A stage starts only behind exactly one passed run of the previous stage at the same
source hash, and a batch name is never used twice (no replay). Worker-session runs carry no stage and are ignored."""
import yaml

import study

PREREQUISITE = {'P0': 'S0', 'Q0': 'P0', 'X0': 'Q0', 'S1': 'X0', 'D1': 'S1'}
STRICT_VALID = ('S0', 'P0', 'Q0')        # every assigned unit must be valid; X0 has its own tolerance inside its gate


def stage_runs(runs, stage, source_hash, model=None, replication=None):
    """Runs of `stage` at this source hash and, given a model, of that model's chain and replication only (models and
    replications are never pooled)."""
    return [r for r in runs if (r.get('params') or {}).get('stage') == stage
            and (r.get('params') or {}).get('source_hash') == source_hash
            and (model is None or (r.get('params') or {}).get('model') == model)
            and (model is None or ((r.get('params') or {}).get('replication') or '') == (replication or ''))]


def gate(runs, stage, p):
    """Raise ValueError unless `stage` may start given the experiment's hub runs."""
    if any((r.get('params') or {}).get('batch') == p['batch'] for r in runs):
        raise ValueError('batch_exists_no_replay')
    previous = PREREQUISITE.get(stage)
    if not previous:
        return None
    same = stage_runs(runs, previous, p['source_hash'], p.get('model'), p.get('replication'))
    if len(same) != 1:
        raise ValueError(f'exact_runtime_qualification_required:{previous}')
    run = same[0]
    metrics = run.get('metrics') or {}
    if previous == 'S1':
        # The diagnostic is collected after the economy. It may follow a branch stopped under the material rule,
        # never an integrity failure, a billing stop or a deadline.
        if run.get('status') not in ('done', 'failed') or metrics.get('diagnostic_admissible') != 1:
            raise ValueError('economy_stage_not_admissible_for_diagnostic')
        return run
    if run.get('status') != 'done' or metrics.get('qualification_passed') != 1:
        raise ValueError(f'exact_runtime_qualification_required:{previous}')
    if previous in STRICT_VALID and metrics.get('invalid') != 0:
        raise ValueError(f'exact_runtime_qualification_required:{previous}')
    return run


def register(sr):
    exp = yaml.safe_load((study.ROOT / 'experiment.yaml').read_text())
    assert exp['id'] == study.EXPERIMENT
    sr.register(exp.pop('id'), **exp)
