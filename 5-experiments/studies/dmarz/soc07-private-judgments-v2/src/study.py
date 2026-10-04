"""Planned ledger (manifest) and the stage runner.

manifest(): every planned block, episode and call of a stage, fixed before execution, with the
source, prompt, generator and scorer hashes. run(): executes the manifest once, in order, and
reconciles every planned episode to exactly one terminal record, whatever happened.
"""
import json
import os
import time

import budget
import config
import generate
import journal as journal_module
import protocol
import score

MODES = {'s1q': 'qualification', 's1r': 'replay', 's1l': 'live'}
REPLAY_ARMS = ('private', 'public', 'never', 'prepare')


def worlds(stage):
    """Every (world, truth) of a stage, each cross-checked by the independent solver."""
    out = []
    for index in range(config.stage_config(stage)['worlds']):
        world, truth = generate.generate(stage, index)
        score.check_world(world, truth)
        out.append((world, truth))
    return out


def manifest(stage, mode=None, namespace=None, arms=None, world_indices=None):
    cfg = config.stage_config(stage)
    mode = mode or MODES[stage]
    namespace = namespace or config.seed_stage(stage)
    pairs = worlds(stage)
    if world_indices is not None:
        pairs = [pairs[i] for i in world_indices]
    blocks, episodes, calls, public_view = [], [], [], []
    repeats = 1 if mode == 'qualification' else cfg['repeats']
    for world, truth in pairs:
        for repeat in range(repeats):
            pres = generate.presentation(world, truth, repeat)
            prefix = '%s/w%04d/r%02d' % (namespace, world['world_index'], repeat)
            base = 'soc07-%s-w%04d-r%02d-a-' % (namespace, world['world_index'], repeat)
            public_view.append({'world': {k: v for k, v in world.items() if k != 'meta'},
                                'evidence_id': pres['evidence_id'], 'repeat': repeat})
            if mode == 'qualification':
                blocks.append({'world_index': world['world_index'], 'repeat': 0, 'arm_order': ['single']})
                episodes.append(base + 'single')
                calls.append({'call_id': prefix + '/single/a0/qualification', 'pool': 'public'})
                continue
            allowed = arms or (REPLAY_ARMS if mode == 'replay' else cfg['arms'])
            order = [arm for arm in pres['arm_order'] if arm in allowed]
            actors = [generate.replay_focal(world)] if mode == 'replay' else list(range(config.AGENTS))
            blocks.append({'world_index': world['world_index'], 'repeat': repeat, 'arm_order': order})
            if any(arm in config.SHARED_INITIAL_ARMS for arm in order):
                calls += [{'call_id': '%s/shared/a%d/initial' % (prefix, a), 'pool': 'public'} for a in actors]
            for arm in order:
                episodes.append(base + arm)
                phases = (['initial'] if arm == 'prepare' else []) + ['discussion', 'final_public', 'final_private']
                calls += [{'call_id': '%s/%s/a%d/%s' % (prefix, arm, a, phase), 'pool': protocol.POOL_OF[phase]}
                          for phase in phases for a in actors]
    counts = {'public': sum(c['pool'] == 'public' for c in calls), 'aux': sum(c['pool'] == 'aux' for c in calls)}
    body = {
        'study': 'soc07-private-judgments-v2', 'stage': stage, 'namespace': namespace, 'mode': mode,
        'blocks': blocks, 'episodes': episodes, 'calls': calls,
        'counts': dict(counts, total=len(calls), episodes=len(episodes), blocks=len(blocks), worlds=len(pairs)),
        'hashes': dict(config.group_hashes(), source=config.source_hash(), public_worlds=config.digest(public_view)),
        'model': config.launch_manifest()['model'], 'launch_manifest': config.launch_manifest(),
    }
    body['manifest_hash'] = config.digest(body)
    return body


def incomplete_episode(episode_id, stage, namespace, execution):
    return {'episode': episode_id, 'stage': stage, 'namespace': namespace, 'execution': execution,
            'decision': 'unavailable', 'reconciled': True, 'agents': [], 'flags': [],
            'usage': {'calls': 0, 'input_tokens': 0, 'output_tokens': 0, 'billed_usd': 0.0}}


def reconcile(plan, episodes, journal_path):
    """Every planned episode gets exactly one terminal record. An episode the journal shows as
    started but not ended is 'interrupted'; one never started is 'incomplete'."""
    seen = {}
    for e in episodes:
        if e['episode'] in seen:
            raise AssertionError('duplicate episode record: ' + e['episode'])
        seen[e['episode']] = e
    unknown = set(seen) - set(plan['episodes'])
    if unknown:
        raise AssertionError('episode outside the planned ledger: %s' % sorted(unknown)[:3])
    started = {ev['episode'] for ev in journal_module.read(journal_path) if ev['kind'] == 'episode_start'}
    out = []
    for episode_id in plan['episodes']:
        if episode_id in seen:
            out.append(seen[episode_id])
        else:
            out.append(incomplete_episode(episode_id, plan['stage'], plan['namespace'],
                                          'interrupted' if episode_id in started else 'incomplete'))
    return out


def run(plan, out, adapter_factory, ledger, progress=None, extra_forbidden=(), tamper=None, limits=None, durable=True):
    """Execute one manifest. adapter_factory(on_attempt) -> adapter. Returns (episodes, controller, crash)."""
    stage, namespace, mode = plan['stage'], plan['namespace'], plan['mode']
    journal_path = out / ('journal-%s.jsonl' % namespace.replace('/', '_'))
    log = journal_module.Journal(journal_path, {'study': plan['study'], 'stage': stage, 'namespace': namespace,
                                                'manifest_hash': plan['manifest_hash'], 'hashes': plan['hashes'],
                                                'model': plan['model'], 'launch_manifest': plan['launch_manifest'],
                                                'counts': plan['counts']}, durable=durable)
    adapter = adapter_factory(lambda call_id: ledger.attempt(call_id, namespace))
    controller = protocol.Controller(stage, adapter, ledger, log, namespace=namespace)
    controller.extra_forbidden = tuple(extra_forbidden)
    controller.tamper = tamper
    if limits:
        controller.limits = dict(controller.limits, **limits)
    world_table = {w['world_index']: (w, t) for w, t in worlds(stage)}
    deadline = time.monotonic() + config.execution()['limits']['stage_timeout_seconds']
    episodes, crash = [], None
    sink = open(out / ('episodes-%s.jsonl' % namespace.replace('/', '_')), 'x')

    def keep(episode):
        sink.write(json.dumps(episode, sort_keys=True) + '\n')
        sink.flush()
        if durable:
            os.fsync(sink.fileno())
        episodes.append(episode)
    controller.on_episode = keep
    try:
        for n, block in enumerate(plan['blocks']):
            if time.monotonic() > deadline:
                controller._halt('stage_deadline')
            world, truth = world_table[block['world_index']]
            if mode == 'qualification':
                controller.run_qualification(world, truth)
            else:
                controller.run_block(world, truth, block['repeat'], mode, arms=block['arm_order'])
            if progress:
                progress(n + 1, len(plan['blocks']), episodes, controller)
    except BaseException as exc:  # includes an injected crash; the record is reconciled, never dropped
        crash = type(exc).__name__
        log.append('crash', error=crash)
    sink.close()
    log.append('journal_close', halted=controller.halted, crash=crash, leaks=controller.leaks)
    log.close()
    return reconcile(plan, episodes, journal_path), controller, crash


def scripted_ledger(path, plan, durable=True, **override):
    caps = budget.caps_for({plan['namespace']: dict(plan['counts'], **override)}, config.execution(), scripted=True)
    return budget.Ledger(path, caps, durable=durable)


def paid_ledger(path, plan):
    caps = budget.caps_for({plan['namespace']: plan['counts']}, config.execution())
    return budget.Ledger(path, caps)
