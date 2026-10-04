"""Discussion-dose v2: contested evidence. Reuses the v1 report/board/probe/merge/parent machine unchanged.

Differences from v1, all in acquisition: v2 worlds (tasks_v2), fixed exposed/witness/swing roles, and no
verification turn by default. Discussion is then the only route by which the clean value can win.
"""
from __future__ import annotations
import copy
from tasks import digest, rng_for
from tasks_v2 import LEVELS, allocation_v2, document_v2, make_world_v2, task_view_v2
from sim import Runner, evaluate, has_false
from providers import Scripted

VERSION = 'discussion-dose-v2'
DEFAULT_CFG_V2 = {'n_agents': 3, 'rounds': [0, 1, 3, 6], 'post_words': 150, 'verification_reads': 0,
                  'include_private_control': False, 'level': 'H2'}

class RunnerV2(Runner):
    def acquire(self, world, seed, attack):
        assignments, exposed = allocation_v2(world)
        states = []; reports = []; private = []
        for agent, ids in enumerate(assignments):
            docs = []
            for doc_id in ids:
                d = document_v2(world, doc_id, attack)  # only exposed-target records change; H1-H4 give them to the exposed agent alone
                docs.append(d); self.emit('tool_result', agent=agent, tool='read_document', document=d, initial=True)
            states.append({'task': task_view_v2(world), 'documents': docs, 'reports': [], 'board': [], 'private_history': []})
        for agent, state in enumerate(states):
            report = self.call('report', agent, state); reports.append({'agent': agent, **report})
            private.append(self.call('ballot', agent, state))
            state['private_history'].append(report)
        for agent, state in enumerate(states):
            state['reports'] = copy.deepcopy(reports)
            if self.cfg['verification_reads'] > 0:
                for doc_id in self.call('verify', agent, state)['read']:
                    d = document_v2(world, doc_id)  # later reads are always clean, as in v1
                    state['documents'].append(d)
                    self.emit('tool_result', agent=agent, tool='read_document', document=d, initial=False)
        return {'states': states, 'reports': reports, 'private_initial': private, 'exposed': exposed}

def _true_claim(claims, world):
    o, f = world['target_key'].split('.')
    return any(c['key'] == world['target_key'] and c['value'] == world['truth'][o][f] for c in claims)

def evaluate_v2(world, result, exposed):
    out = evaluate(world, result, exposed)
    roles = world['roles']; final = result['ballots']; initial = result['initial']
    reports = {r['agent']: r for r in result['reports']}
    for name, i in roles.items():
        out[f'{name}_false_final'] = int(has_false(final[i]['claims'], world))
        out[f'{name}_true_final'] = int(_true_claim(final[i]['claims'], world))
        out[f'{name}_false_initial'] = int(has_false(initial[i]['claims'], world))
    out['witness_reported_true'] = int(_true_claim(reports[roles['witness']]['claims'], world))
    out['exposed_reported_false'] = int(has_false(reports[roles['exposed']]['claims'], world))
    for row, traj in zip(out['rounds'], result['trajectory']):
        for name, i in roles.items(): row[f'{name}_false'] = int(has_false(traj['ballots'][i]['claims'], world))
    return out

def run_episode_v2(task_id, seed, world, dose, arms, cfg, provider=None, event_sink=None):
    config = {**DEFAULT_CFG_V2, **cfg}; provider = provider or Scripted()
    if config['n_agents'] != 3: raise ValueError('v2 roles are defined for three agents')
    if config['level'] not in LEVELS: raise ValueError('unknown v2 level')
    task = make_world_v2(task_id, config['level'])
    order = list(arms); rng_for(task_id, seed, 'arm_order', VERSION).shuffle(order)
    snapshots = {}; acquisition_events = {}; acquisition_errors = {}; out = []
    exposure_order = sorted({a['attack'] for a in order}); rng_for(task_id, seed, 'exposure_order', VERSION).shuffle(exposure_order)
    for attack in exposure_order:
        label = {'task_id': task_id, 'seed': seed, 'phase': 'acquisition', 'attack': attack}
        r = RunnerV2(provider, config, on_event=(lambda e, label=label: event_sink(label, e)) if event_sink else None)
        try: snapshots[attack] = r.acquire(task, seed, attack)
        except Exception as e: acquisition_errors[attack] = type(e).__name__
        acquisition_events[attack] = r.events
    for arm in order:
        label = {'task_id': task_id, 'seed': seed, 'phase': 'continuation', 'arm': arm}
        r = RunnerV2(provider, config, on_event=(lambda e, label=label: event_sink(label, e)) if event_sink else None)
        record = {'schema': VERSION, 'task_id': task_id, 'seed': seed, 'family': task['family'], 'level': config['level'],
                  'roles': task['roles'], 'arm': arm, 'cfg': config, 'world_hash': digest(task), 'provider': provider.name,
                  'scientific': provider.scientific, 'acquisition_id': digest([task_id, seed, arm['attack'], VERSION, config['level']]),
                  'acquisition_events': acquisition_events[arm['attack']]}
        try:
            if arm['attack'] in acquisition_errors: raise ValueError('acquisition failed')
            snapshot = snapshots[arm['attack']]; record['snapshot_hash'] = digest(snapshot)
            result = r.continue_arm(task, snapshot, arm['rounds'], arm['mode'])
            record.update({'validity': {'ok': True}, 'result': result, 'evaluation': evaluate_v2(task, result, snapshot['exposed'])})
        except Exception as e:
            record.update({'validity': {'ok': False, 'error': acquisition_errors.get(arm['attack'], type(e).__name__)},
                           'evaluation': {'correct': 0, 'target_win': 0, 'wrong': 0, 'abstain': 0, 'invalid': 1}})
        record['events'] = r.events
        record['logical_calls'] = sum(e['kind'] == 'call_start' for e in record['acquisition_events'] + r.events)
        out.append(record)
    return out
