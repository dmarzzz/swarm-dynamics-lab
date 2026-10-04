"""Template-derived reporting bridge for a completed local qualification.

Invoke on a fleet host with a copied, audited result directory. It runs no models,
creates no queue work, and uploads once; an existing receipt refuses duplication.
"""
import argparse
import hashlib
import json
from pathlib import Path
import swarm_report as sr


def publish(directory, definition):
    receipt = directory / 'hub-receipt.json'
    if receipt.exists():
        raise SystemExit('This result directory already has a hub receipt')
    manifest = json.loads((directory / 'manifest.json').read_text())
    summary = json.loads((directory / 'summary.json').read_text())
    if not manifest['complete'] or summary['episodes'] != 144:
        raise SystemExit('Incomplete qualification; report the failure separately')
    spec = json.loads(definition.read_text())
    exp = spec.pop('id')
    sr.register(exp, **spec)
    # A stable ID also prevents accidental copies being presented as independent runs.
    digest = hashlib.sha256((directory / 'episodes.jsonl').read_bytes()).hexdigest()[:12]
    run_id = f'{exp}/{manifest["backend"]}-S0-{digest}'
    receipt.write_text(json.dumps({'run': run_id, 'upload_complete': False}))
    with sr.start(exp, run=run_id, params={'backend': manifest['backend'], 'stage': 'S0', 'code': manifest['code']}) as run:
        for name in ('manifest.json', 'summary.json', 'episodes.jsonl', 'assignments.json', 'replay.html'):
            run.artifact(directory / name, name)
        run.done(message='Local exploratory qualification; no Jev calls; see clean competence gate',
                 episodes=summary['episodes'], invalid=summary['invalid'],
                 qualified=int(summary['clean_qualification_pass']))
    receipt.write_text(json.dumps({'run': run_id, 'upload_complete': True}))
    print(json.dumps({'run': run_id, 'upload_complete': True}))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', required=True, type=Path)
    ap.add_argument('--definition', required=True, type=Path)
    a = ap.parse_args()
    publish(a.results, a.definition)
