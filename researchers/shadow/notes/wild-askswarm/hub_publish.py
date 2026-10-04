#!/usr/bin/env python3
"""Publish derived baseline reports through the sanctioned swarm_report client.

Requires swarm_report on PYTHONPATH and SWARM_HUB_URL/TOKEN/SOURCE in the environment.
No credentials are read from files, printed or committed by this script. No model calls.
Run only after run_all.py and verify_results.py finish. Serial, small bounded write burst.
"""
import json
from pathlib import Path
import time
import swarm_report as sr

ROOT = Path(__file__).resolve().parent


def main():
    spec = json.loads((ROOT / 'hub_spec.json').read_text())
    experiment = spec.pop('id')
    sr.register(experiment, **spec)
    receipt = {'experiment': experiment, 'scope': 'post-run publication of derived aggregates; no launch', 'runs': []}
    for source in ('wiki', 'swarmtraces', 'git'):
        folder = ROOT / 'results' / source
        result = json.loads((folder / 'metrics.json').read_text())
        run_id = f'{experiment}/{source}-4959a80b-v011'
        run = sr.start(experiment, run=run_id,
                       params={'source': source, 'threshold': .7, 'git_ref': '4959a80b2e48050066630c5d22ea5d1fa1b0beb2'},
                       message='Completed offline census. Records are dependent artifacts, not independent trials.')
        for filename in ('metrics.json', 'report.html'):
            run.artifact(folder / filename, filename)
            time.sleep(.5)
        metrics = {key: value for key, value in result['summary'].items()
                   if key in spec['metrics'] and type(value) in (int, float)}
        ok = run.done(message='No causal influence claim. Missing identity/time metrics are unavailable, not zero effects.',
                      **metrics, model_calls=0, cost_usd=0)
        time.sleep(.5)
        saved = sr.get_run(run_id)
        state = saved['run'] if isinstance(saved.get('run'), dict) else saved
        receipt['runs'].append({'run': run_id, 'done_event_acknowledged': bool(ok),
                                'readback_status': state.get('status') if isinstance(state, dict) else None,
                                'artifacts': ['metrics.json', 'report.html']})
    (ROOT / 'results' / 'hub-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
