"""Register the hub experiment and queue one run per stage, with exact-runtime gates between stages."""
import json
import subprocess

import config
import launch

EXPERIMENT = 'soc07-private-judgments'
PREREQUISITE = {'s1q': 's0', 's1r': 's1q', 's1l': 's1r'}


def params(stage, attempt=1):
    if stage not in config.STAGES:
        raise ValueError('stage not authorized (S2 is closed)')
    backend = 'scripted' if stage == 's0' else 'anthropic'
    launch_manifest = config.launch_manifest()
    caps = config.phase_caps()
    return {'stage': stage, 'backend': backend,
            'model': 'none' if stage == 's0' else launch_manifest['model'],
            'reasoning_tokens': config.thinking_budget(),
            'output_caps': '/'.join(str(caps[k]) for k in ('initial', 'discussion', 'final_public', 'final_private', 'qualification')),
            'launch_manifest': launch_manifest['version'],
            'batch': '%s-a%d' % (config.seed_stage(stage), attempt), 'source_hash': config.source_hash(),
            'code': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=config.ROOT, text=True).strip()}


def register(sr):
    exp = json.loads((config.ROOT / 'experiment.json').read_text())
    return sr.register(exp.pop('id'), **exp)


def enqueue(sr, stage, attempt=1):
    p = params(stage, attempt)
    runs = sr.runs(EXPERIMENT, limit=5000)
    if any(r.get('params', {}).get('batch') == p['batch'] for r in runs):
        raise ValueError('batch_exists_no_replay')
    need = PREREQUISITE.get(stage)
    if need:
        launch.check(stage)
        passed = [r for r in runs if r.get('params', {}).get('stage') == need and r['status'] == 'done'
                  and r.get('params', {}).get('source_hash') == p['source_hash']
                  and r.get('metrics', {}).get('gate_passed') == 1]
        if not passed:
            raise ValueError('exact_runtime_prerequisite_required:' + need)
    register(sr)
    return sr.enqueue(EXPERIMENT, [p], tags=[config.STAGE_LABELS[stage], p['backend'], 'exploratory'])
