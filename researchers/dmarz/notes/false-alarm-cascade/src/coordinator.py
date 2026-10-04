"""The software gate. A stage is queued only behind exactly one passed run of the previous stage
at the same source hash, and a batch name is never queued twice (no replay)."""
import yaml

import study

PREREQUISITE = {'P0': 'S0', 'Q0': 'P0', 'S1': 'Q0'}


def gate(runs, stage, p):
    """Raise ValueError unless `stage` may be queued given the experiment's hub runs."""
    if any((r.get('params') or {}).get('batch') == p['batch'] for r in runs):
        raise ValueError('batch_exists_no_replay')
    previous = PREREQUISITE.get(stage)
    if previous:
        same = [r for r in runs if (r.get('params') or {}).get('stage') == previous
                and (r.get('params') or {}).get('source_hash') == p['source_hash']]
        passed = [r for r in same if r.get('status') == 'done'
                  and (r.get('metrics') or {}).get('invalid') == 0
                  and (r.get('metrics') or {}).get('qualification_passed') == 1]
        # Exactly one run of the previous stage at this source hash, and it passed.
        if len(same) != 1 or len(passed) != 1:
            raise ValueError(f'exact_runtime_qualification_required:{previous}')


def enqueue(sr, stage):
    p = study.params(stage)
    runs = sr.runs(study.EXPERIMENT, limit=5000)
    gate(runs, stage, p)
    exp = yaml.safe_load((study.ROOT / 'experiment.yaml').read_text())
    assert exp['id'] == study.EXPERIMENT
    sr.register(exp.pop('id'), **exp)
    return sr.enqueue(study.EXPERIMENT, [p], tags=[stage, p['backend'], 'exploratory'])
