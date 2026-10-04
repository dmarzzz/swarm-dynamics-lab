"""One bounded fleet run, adapted from templates/experiment-worker/src/worker.py.

No polling queue or automatic restart: a launch receipt and exclusive output
directory prevent accidental duplicate model spending. Reporting observes only.
"""
import argparse
import copy
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import time

from .cli import approved_model_config, run, audit, write_json
from .contracts import strict_json
from .policies import anthropic, Scripted
from .worlds import cases
from .scoring import reference_winner
from .runner import allocation

EXPERIMENT = 'discussion-dose-v3'
SPEC = {
    'title': 'Discussion and memory v3: model qualification',
    'description': 'Exploratory three-agent qualification: independent votes, reports only, private work and public discussion; paired clean/contaminated evidence and fresh-parent memory probes. Independent review is pending. Not a confirmatory experiment.',
    'owner': 'dmarz',
    'params': {'stage': {'type': 'str', 'role': 'stage'}, 'batch': {'type': 'str', 'role': 'replicate'},
               'rounds': {'type': 'int'}, 'n_agents': {'type': 'int'}, 'model': {'type': 'str'},
               'independent_review': {'type': 'str'}},
    'metrics': ['model_calls', 'model_cost_usd', 'usage_missing_calls', 'episodes', 'invalid_calls', 'parent_unsupported',
                'parent_inherited_error', 'clean_accuracy', 'qualification_passed', 'execution_complete'],
    'primary_metric': 'model_calls',
    'url': 'https://github.com/dmarzzz/swarm-lab/tree/main/researchers/dmarz/notes/discussion-dose/benchmark-v3',
}


class Progress:
    """Map durable events to the existing deliberation frame contract."""
    def __init__(self, destination, worlds, reporter, rounds, planned_calls, rates):
        self.destination = destination; self.worlds = {w['id']: w for w in worlds}
        self.reporter = reporter; self.rounds = rounds; self.planned_calls = planned_calls; self.rates = rates
        self.started = self.finished = self.model_calls = self.invalid = self.episodes = 0
        self.input_tokens = self.output_tokens = self.unsupported = self.inherited = 0
        self.clean = self.correct = self.attack = self.attack_wins = self.false_memory = 0
        self.invalid_episodes = 0
        self.usage_missing = 0
        self.reporting_errors = 0; self.last_frame = 0; self.frames = []; self.current = None
        self.label = None; self.agents = {}; self.trajectory = []; self.memory = None

    def metrics(self):
        metrics = {'model_calls': self.model_calls, 'model_cost_usd': (self.input_tokens * self.rates[0] + self.output_tokens * self.rates[1]) / 1e6,
                'usage_missing_calls': self.usage_missing,
                'episodes': self.episodes, 'invalid_calls': self.invalid,
                'parent_unsupported': self.unsupported, 'parent_inherited_error': self.inherited}
        if self.clean: metrics['clean_accuracy'] = self.correct / self.clean
        return metrics

    def __call__(self, event):
        try: self.observe(event)
        except Exception: self.reporting_errors += 1

    def observe(self, e):
        kind = e['kind']; label = e.get('label', e.get('record', {}).get('id', ''))
        if label and label != self.label:
            self.label = label; self.agents = {}; self.trajectory = []; self.memory = None
        if kind == 'call_start': self.started += 1
        if kind in ('call_response', 'provider_failure'):
            self.finished += 1; self.model_calls += bool(e.get('dispatched'))
            self.usage_missing += int(bool(e.get('dispatched')) and not all(type(e.get('usage', {}).get(k)) is int for k in ('input_tokens', 'output_tokens')))
            self.input_tokens += e.get('usage', {}).get('input_tokens', 0)
            self.output_tokens += e.get('usage', {}).get('output_tokens', 0)
        if kind in ('provider_failure', 'validation_failure'): self.invalid += 1
        if kind == 'terminal':
            self.episodes += 1; row = e['record']; ev = row['evaluation']
            self.invalid_episodes += int(bool(row.get('call_failures') or ev.get('vote_invalid') or ev.get('parent_invalid') or ev.get('invalid')))
            self.unsupported += ev.get('parent_unsupported') or 0
            self.inherited += ev.get('parent_inherited_error') or 0
            if row['kind'] == 'swarm':
                if row['attack']:
                    self.attack += 1; self.attack_wins += ev['vote_target']; self.false_memory += ev['memory_false_target']
                else: self.clean += 1; self.correct += ev['vote_correct']
        parts = label.split(':'); world = self.worlds.get(int(parts[0])) if len(parts) == 3 and parts[0].isdigit() else None
        if world:
            if kind == 'call_start' and type(e.get('agent')) is int:
                self.agents.setdefault(e['agent'], {})['speaking'] = True
            if kind in ('call_response', 'provider_failure') and type(e.get('agent')) is int:
                a = self.agents.setdefault(e['agent'], {}); a['speaking'] = False
                response = e.get('response') or {}
                if type(response) is dict:
                    if 'message' in response: a['msg'] = str(response['message'])[:160]
            if kind == 'checkpoint':
                state = e['state']; values = state['target_values']
                for i in range(3):
                    self.agents.setdefault(i, {}).update(vote=state['votes'][i] if state['votes'][i] != 'INVALID' else None,
                        claim='true' if values[i] == world['truth'][world['target_key']] else 'false' if values[i] == world['false_value'] else None if values[i] is None else 'other', speaking=False)
                self.trajectory.append({'round': e.get('turn', 0), 'false': state['false_endorsements'], 'votes': [a.get('vote') for a in [self.agents[i] for i in range(3)]]})
            if kind == 'merge':
                self.memory = ['true' if r['value'] == world['truth'][world['target_key']] else 'false' if r['value'] == world['false_value'] else 'other'
                               for r in e['memory'] if r['key'] == world['target_key']]
            roles = {v: k for k, v in world['roles'].items()}
            phase = e.get('request', {}).get('phase', kind)
            phase = {'work': 'discuss', 'checkpoint': 'ballot', 'merge': 'parent', 'terminal': 'parent'}.get(phase, phase)
            if phase not in ('report', 'ballot', 'discuss', 'parent'): phase = 'starting'
            self.current = {'kind': 'deliberation', 'protocol': 'v3', 'level': parts[2][:8],
                't': self.episodes, 'ts': round(time.time(), 1),
                'world': {'task': world['id'], 'family': world['family'], 'instructions': world['task']['instructions'],
                          'key': world['target_key'], 'true': world['truth'][world['target_key']], 'false': world['false_value'], 'attacker': world['target'],
                          'answer': reference_winner(world['task'], world['truth'])},
                'arm': {'attack': parts[1] == '1', 'rounds': self.rounds if parts[2] in ('private', 'board') else 0},
                'stage': 'acquisition' if parts[2] == 'acquisition' else 'continuation', 'phase': phase, 'round': e.get('turn', 0),
                'agents': [{'id': i, 'role': roles[i], 'vote': None, 'claim': None, 'speaking': False, 'msg': '', **self.agents.get(i, {})} for i in range(3)],
                'trajectory': copy.deepcopy(self.trajectory), 'memory': self.memory, 'posts': [], 'recent': [],
                'tally': {'episodes': self.episodes, 'attack': self.attack, 'attack_wins': self.attack_wins,
                          'attack_false_memory': self.false_memory, 'clean': self.clean, 'clean_correct': self.correct, 'invalid': self.invalid_episodes}}
            if kind in ('checkpoint', 'merge', 'terminal'): self.frames.append(copy.deepcopy(self.current))
        if self.reporter:
            try:
                self.reporter.progress(self.finished, self.planned_calls,
                    message=f'{self.episodes}/96 cases; {self.finished}/{self.planned_calls} calls; independent review pending', **self.metrics())
                if self.current and time.monotonic() - self.last_frame >= 5:
                    self.save_frame(); self.reporter.artifact(self.destination / 'frame.json', 'frame.json'); self.last_frame = time.monotonic()
            except Exception: self.reporting_errors += 1

    def save_frame(self):
        if self.current:
            (self.destination / 'frame.json').write_text(json.dumps(self.current, separators=(',', ':')))

    def finish(self):
        self.save_frame()
        (self.destination / 'replay.json').write_text(json.dumps({'kind': 'deliberation-replay', 'protocol': 'v3', 'level': None,
                                                                'thinned': 0, 'frames': self.frames}, separators=(',', ':')))


def publish(reporter, destination):
    """Chunk raw records below the fleet proxy limit; never rerun model work."""
    folder = destination / 'upload'; folder.mkdir(exist_ok=True); index = {'files': []}
    for path in sorted(destination.iterdir()):
        if not path.is_file(): continue
        raw = path.read_bytes()
        if path.name in ('frame.json', 'replay.json') and len(raw) < 1_000_000:
            reporter.artifact(path, path.name); continue
        compressed = path.suffix in ('.jsonl', '.html') or len(raw) >= 1_000_000
        data = gzip.compress(raw, mtime=0) if compressed else raw
        name = path.name + ('.gz' if compressed else '')
        names = []
        for offset in range(0, max(1, len(data)), 1_000_000):
            part = name if len(data) <= 1_000_000 else name + f'.part{offset // 1_000_000:04d}'
            output = folder / part; output.write_bytes(data[offset:offset + 1_000_000])
            reporter.artifact(output, part); names.append(part)
        index['files'].append({'name': path.name, 'sha256': hashlib.sha256(raw).hexdigest(), 'encoding': 'gzip' if compressed else 'identity', 'parts': names})
    index_path = folder / 'artifact-index.json'; index_path.write_text(json.dumps(index, indent=2)); reporter.artifact(index_path)


def execute(sr, launch_path, destination, batch, backend='anthropic'):
    launch = strict_json(launch_path.read_text())
    split, rounds = launch['split'], launch['rounds']
    config = approved_model_config(launch_path, split, rounds)
    worlds = cases(split)
    if config['max_calls'] != allocation(worlds, rounds)[1]:
        raise ValueError('model call allowance must match planned allocation')
    provider = anthropic(config) if backend == 'anthropic' else Scripted()
    run_id = f'{EXPERIMENT}/{batch}'
    if destination.exists(): raise ValueError('output already exists; no automatic restart')
    if any(r['run'] == run_id for r in sr.runs(EXPERIMENT, limit=5000)):
        raise ValueError('batch already exists on hub; inspect rather than relaunch')
    # The receipt persists even if the hub or process fails between start and run.
    destination.parent.mkdir(parents=True, exist_ok=True)
    write_json(destination.with_suffix('.launch-receipt.json'), {'run': run_id, 'launch_sha256': hashlib.sha256(launch_path.read_bytes()).hexdigest(),
               'created_utc': datetime.now(timezone.utc).isoformat(), 'backend': backend})
    sr.register(EXPERIMENT, **SPEC)
    reporter = sr.start(EXPERIMENT, run=run_id, params={'batch': batch, 'stage': 'S0', 'split': split, 'rounds': rounds,
        'n_agents': 3, 'model': config['model'], 'backend': backend, 'planned_calls': config['max_calls'],
        'independent_review': 'pending', 'authorization': launch['status']}, message='Operator-authorized engineering qualification; independent review pending')
    tracker = Progress(destination, worlds, reporter, rounds, config['max_calls'],
                       (config['input_usd_per_million'], config['output_usd_per_million']))
    try:
        result = run(destination, split, rounds, provider, config, observer=tracker, launch_record=launch)
        tracker.finish()
        checked = audit(destination); write_json(destination / 'audit.json', checked)
        write_json(destination / 'reporting.json', {'reporting_errors': tracker.reporting_errors})
        publish(reporter, destination)
        q = result['qualification']; rec = result['reconciliation']
        message = ('Execution and replay complete. Model qualification ' + ('passed' if q['model_qualified'] else 'did not pass') +
                   f'; clean diagnostic {q["clean_full_evidence_correct"]}/6, clean reports {q["clean_reports_correct"]}/6; independent review pending.')
        reporter.done(message=message, **tracker.metrics(), qualification_passed=int(q['model_qualified']), execution_complete=int(q['execution_complete']))
        print(json.dumps({'run': run_id, 'qualification': q, 'reconciliation': rec, 'metrics': tracker.metrics()}))
        return result
    except BaseException as exc:
        if destination.exists():
            tracker.finish()
            try: publish(reporter, destination)
            except Exception: pass
        reporter.fail(message=f'Incomplete qualification: {type(exc).__name__}; preserve ledger and inspect locally', **tracker.metrics())
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--launch-manifest', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--batch', required=True)
    args = parser.parse_args()
    import swarm_report as sr
    execute(sr, args.launch_manifest, args.output, args.batch)


if __name__ == '__main__': main()
