"""Run the v3 resampling-only sidecar as one hub run (progress, artifacts, metrics). Paid runs need the approved manifest.

  python3 src/resample_v3_hub.py --register
  python3 src/resample_v3_hub.py --backend scripted --output results/resample-v3/<dir>
  python3 src/resample_v3_hub.py --backend anthropic --launch-manifest <approved.json> --output results/resample-v3/<dir>
"""
import argparse
import json
from pathlib import Path
import resample_v3 as rs
from bench_v3.policies import Scripted, anthropic
import gzip
import hashlib

OUTPUTS = ('manifest.json', 'episodes.json', 'events.jsonl', 'summary.json')  # v3 writes episodes.json, not .jsonl
MAX_PART = 1_000_000  # fleet proxy request limit, as in artifacts.py


def prepare_artifacts(out, limit=MAX_PART):
    out = Path(out); upload = out / 'upload'; upload.mkdir(exist_ok=True)
    parts = []; index = {'version': 1, 'files': []}
    for name in OUTPUTS:
        path = out / name
        if not path.exists(): continue
        raw = path.read_bytes(); payload = gzip.compress(raw, mtime=0)
        names = []
        for offset in range(0, max(1, len(payload)), limit):
            part = name + '.gz' + ('' if len(payload) <= limit else f'.part{offset // limit:04d}')
            (upload / part).write_bytes(payload[offset:offset + limit]); parts.append(upload / part); names.append(part)
        index['files'].append({'original': name, 'raw_bytes': len(raw), 'raw_sha256': hashlib.sha256(raw).hexdigest(),
                               'encoding': 'gzip', 'payload_sha256': hashlib.sha256(payload).hexdigest(), 'parts': names})
    idx = upload / 'artifact-index.json'; idx.write_text(json.dumps(index, indent=2)); parts.append(idx)
    return parts


def publish_artifacts(run, out):
    for path in prepare_artifacts(out): run.artifact(path, path.name)

EXPERIMENT = 'discussion-v3-resample'
SPEC = {'title': 'Discussion v3: resampling-only control (exploratory)',
        'description': 'Sidecar to discussion benchmark v3: reports vs private work vs repeated probes of the unchanged '
                       'post-report checkpoint. Separates self-revision from ballot resampling. Exploratory; not an accepted hypothesis.',
        'owner': 'dmarz', 'params': {'stage': {'type': 'str'}, 'backend': {'type': 'str'}, 'rounds': {'type': 'int'}},
        'metrics': ['episodes', 'invalid_calls', 'clean_reports_correct', 'self_revision_vote_target', 'private_drift_vote_target',
                    'resample_drift_vote_target', 'model_calls', 'model_cost_usd'],
        'primary_metric': 'self_revision_vote_target',
        'url': 'https://github.com/dmarzzz/swarm-lab/blob/main/researchers/dmarz/notes/discussion-dose/RESAMPLE-CONTROL.md'}


class Counting:
    """Provider wrapper that reports call progress; behaviour and accounting attributes pass through."""
    def __init__(self, inner, run, total):
        self.inner = inner; self.run = run; self.total = total; self.n = 0

    def __getattr__(self, name): return getattr(self.inner, name)

    def complete(self, request):
        try: return self.inner.complete(request)
        finally:
            self.n += 1
            if self.n % 13 == 0 or self.n == self.total:
                self.run.progress(self.n, self.total, message=f'{self.n}/{self.total} calls')


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--register', action='store_true')
    p.add_argument('--backend', choices=['scripted', 'anthropic'], default='scripted')
    p.add_argument('--launch-manifest', type=Path); p.add_argument('--output', type=Path)
    p.add_argument('--rounds', type=int, default=rs.ROUNDS)
    a = p.parse_args(argv)
    import swarm_report as sr
    if a.register:
        sr.register(EXPERIMENT, **SPEC); print('Registered', EXPERIMENT); return 0
    if a.output is None: p.error('--output required')
    config = None
    if a.backend == 'anthropic':
        config = rs.approved_model_config(a.launch_manifest, a.rounds); provider = anthropic(config)
    else: provider = Scripted()
    _, calls = rs.allocation(rs.cases(), a.rounds)
    run = sr.start(EXPERIMENT, params={'stage': 'S0', 'backend': a.backend, 'rounds': a.rounds,
                                       'worlds': [i for v in rs.WORLDS.values() for i in v], 'model_config': config},
                   message='resample sidecar started')
    counted = Counting(provider, run, calls)
    try:
        summary = rs.run(a.output, a.rounds, counted, config)
    except Exception as exc:
        if a.output.exists(): publish_artifacts(run, a.output)
        run.fail(message=f'{type(exc).__name__}: {exc}'); raise
    publish_artifacts(run, a.output)
    rec = summary['reconciliation']; q = summary['qualification']
    m = summary['mechanism']['vote_target:resolvable']
    cost = sum((g.get('estimated_cost_usd') or 0) for g in summary['resources'].values())
    metrics = dict(episodes=rec['terminal'], invalid_calls=rec['validation_failures'] + rec['provider_failures'],
                   clean_reports_correct=q['clean_reports_correct'], model_calls=rec['physical_model_calls'], model_cost_usd=cost,
                   self_revision_vote_target=m['self_revision']['mean'], private_drift_vote_target=m['private_drift']['mean'],
                   resample_drift_vote_target=m['resample_drift']['mean'], qualification_pass=int(q['model_qualified']))
    passed = q['model_qualified'] or not summary['scientific']
    message = ('Engineering scripted run; not LLM evidence' if not summary['scientific'] else
               'Qualification passed' if passed else f'Qualification failed: {json.dumps(q, sort_keys=True)}')
    (run.done if passed else run.fail)(message=message, **metrics)
    print(json.dumps({'run': run.id, 'qualification': q, 'reconciliation': rec}, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
