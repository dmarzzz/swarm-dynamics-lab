"""Adapted from templates/experiment-worker/src/sim.py; paired stopping-rule tape."""
import collections
import hashlib
import json
import random
import time

OPTIONS = ('A', 'B', 'C')
ARMS = ('majority', 'fixed', 'adaptive', 'central')


def task(task_id):
    return {'task_id': task_id, 'a_star': random.Random(f'task:{task_id}').choice(OPTIONS)}


def draw_reports(t, seed, world, rounds=6):
    if world not in ('clean', 'copied-true', 'late-correction'):
        raise ValueError('world')
    rng = random.Random(f'{t["task_id"]}:{seed}')
    wrong = rng.choice([a for a in OPTIONS if a != t['a_star']])
    tape = []
    for r in range(1, rounds + 1):
        roots = [i % (2 if r < 3 else 3) for i in range(5)]
        if world != 'clean' and r < 3:
            roots = [0] * 5
        elif world != 'clean':
            roots = [1 + i % 3 for i in range(5)]
        rng.shuffle(roots)
        tape.append([{'agent': i, 'root': f'benchmark-{root}',
                      'recommendation': wrong if world == 'late-correction' and root == 0 else t['a_star']}
                     for i, root in enumerate(roots)])
    return tape


def visible(reports):
    roots = {}
    for report in reports:
        roots[report['root']] = report['recommendation']
    return [{'root': root, 'recommendation': choice} for root, choice in sorted(roots.items())]


def scripted(reports):
    counts = collections.Counter(r['recommendation'] for r in reports)
    best = max(counts.values())
    winners = [k for k, n in counts.items() if n == best]
    return winners[0] if len(winners) == 1 else 'ABSTAIN'


def stop(votes, reports, arm, step, deadline):
    floor = 0 if arm == 'majority' else (2 if arm == 'adaptive' and step == deadline else 3)
    for option in OPTIONS:
        supporters = [i for i, vote in enumerate(votes) if vote == option]
        roots = {reports[i]['root'] for i in supporters}
        if len(supporters) >= 3 and len(roots) >= floor:
            return option
    return None


def evaluate(t, choice, valid):
    return {'a_star': t['a_star'], 'correct': valid and choice == t['a_star'],
            'committed': valid and choice is not None,
            'false_commit': valid and choice is not None and choice != t['a_star'],
            'loss': 1 if not valid else (0.3 if choice is None else float(choice != t['a_star']))}


def run_episode(task_id, seed, world, dose, arms, cfg):
    deadline = int(dose)
    t = task(task_id)
    tape = draw_reports(t, seed, world, deadline)
    decide = cfg.get('decide', scripted)
    history, trace = [], []
    team_error = central_error = None
    inference_calls = 0
    started = time.monotonic()
    for step, reports in enumerate(tape, 1):
        votes, central = [], 'ABSTAIN'
        if team_error is None:
            try:
                for report in reports:
                    inference_calls += 1
                    vote = decide(visible(history + [report]))
                    if vote not in (*OPTIONS, 'ABSTAIN'):
                        raise ValueError('invalid_choice')
                    votes.append(vote)
            except Exception as exc:
                team_error = type(exc).__name__
        if central_error is None:
            try:
                inference_calls += 1
                central = decide(visible(history + reports))
                if central not in (*OPTIONS, 'ABSTAIN'):
                    raise ValueError('invalid_choice')
            except Exception as exc:
                central_error = type(exc).__name__
        trace.append({'round': step, 'reports': reports, 'votes': votes, 'central': central})
        history += reports
    elapsed = time.monotonic() - started
    digest = hashlib.sha256(json.dumps(tape, sort_keys=True).encode()).hexdigest()
    output = []
    for arm in arms:
        error = central_error if arm == 'central' else team_error
        choice, delay = None, deadline
        if error is None:
            for frame in trace:
                candidate = frame['central'] if arm == 'central' else stop(
                    frame['votes'], frame['reports'], arm, frame['round'], deadline)
                if candidate not in (None, 'ABSTAIN'):
                    choice, delay = candidate, frame['round']
                    break
        output.append({'task_id': task_id, 'seed': seed, 'world': world, 'dose': deadline,
                       'arm': arm, 'reports_hash': digest, 'trace': trace,
                       'decision': {'choice': choice, 'delay': delay},
                       'evaluation': evaluate(t, choice, error is None),
                       'validity': {'ok': error is None, 'error': error},
                       'cost_actual': {'policy_calls': delay * (1 if arm == 'central' else 5),
                                       'shared_tape_calls': inference_calls, 'shared_tape_wall_s': elapsed}})
    return output
