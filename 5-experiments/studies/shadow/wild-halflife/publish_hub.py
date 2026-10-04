#!/usr/bin/env python3
"""Publish only owned derived results with existing sanctioned hub client.

No model execution or raw source rows. Requires swarm_report on PYTHONPATH and
configured URL/token; never reads, prints or writes credential values. Serialized
artifact burst; Retry-After / retry policy are handled by configured hub client.
"""
import json
import os
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent


def main():
    import swarm_report as sr
    config = sr._config()
    if not config.get('SWARM_HUB_URL') or not config.get('SWARM_HUB_TOKEN'):
        raise SystemExit('BLOCKED: hub URL/token unavailable; offline results remain complete')
    os.environ['SWARM_SOURCE'] = 'shadow/sol-halflife'
    spec = json.loads((ROOT/'experiment.json').read_text())
    summary = json.loads((ROOT/'results/summary.json').read_text())
    sr.register(spec['id'], **{k:v for k,v in spec.items() if k != 'id'})
    time.sleep(.5)
    run_id = 'wild-halflife/retrospective-66fa0aa6-v1'
    run = sr.start(spec['id'], run=run_id,
                   params={'git_ref': summary['inputs']['git']['rev'], 'stage': 'retrospective-census'},
                   message='Completed saved-data analysis, retrospective display only; no launch or causal gate approval')
    artifacts = ['results/summary.json', 'results/supplement.json', 'results/fig-adoption.png', 'FINDING.md']
    for file in artifacts:
        run.artifact(ROOT/file, Path(file).name)
        time.sleep(.5)
    ok = run.done(message='Two dependent corpora; exact-unit reuse not semantic idea copying. All intervals and process limits linked.',
                  wiki_url_beta=summary['wiki']['A']['url']['activity']['beta'],
                  git_url_beta=summary['git']['A']['url']['activity']['beta'],
                  wiki_url_conditional_median_records=summary['wiki']['A']['url']['activity']['cond_median_time_to_2nd'],
                  git_url_conditional_median_records=summary['git']['A']['url']['activity']['cond_median_time_to_2nd'],
                  wiki_records=summary['wiki']['records'], git_records=summary['git']['records'],
                  bootstrap_resamples=summary['n_boot'], model_calls=0, cost_usd=0)
    time.sleep(.5)
    saved = sr.get_run(run_id)
    state = saved['run'] if isinstance(saved.get('run'), dict) else saved
    status = state.get('status') if isinstance(state, dict) else None
    receipt = dict(experiment=spec['id'], run=run_id, retrospective=True,
                   done_event_acknowledged=bool(ok), readback_status=status, artifacts=artifacts)
    (ROOT/'results/hub-receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))
    if not ok or status != 'done':
        raise SystemExit('Hub completion not verified; inspect receipt before claiming publication')


if __name__ == '__main__':
    main()
