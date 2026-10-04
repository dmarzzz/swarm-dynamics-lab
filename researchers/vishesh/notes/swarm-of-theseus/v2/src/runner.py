"""Gated model runner. No scripted experiment mode. Local fixtures belong in tests."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import copy
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time

from analyze import summarize
from domain import ARMS, SCENARIOS, commands, explicit_rule, history, instructions, oracle, rules, tickets, validate_output
from engine import acquire, continuation
from preflight import EXPERIMENT, check_plan, check_review, validate_receipt
from provider import AnthropicPolicy, StopRun, write_new


def assignments(stage):
    result = []
    seeds = (302, 303) if stage == 'S0-repair' else (300, 301) if stage == 'S0' else (400, 401)
    for scenario in SCENARIOS:
        for seed in seeds:
            for arm in (('ceiling', 'learner') if stage.startswith('S0') else ('acquisition',) + ARMS):
                steps = [0, 5] if stage.startswith('S0') else [0, 1] if arm == 'acquisition' else list(range(2, 10))
                result.append({'run': f'{stage}-{scenario}-{seed}-{arm}', 'scenario': scenario, 'seed': seed, 'arm': arm, 'steps': steps,
                               'tldr': f'TLDR: {stage} {scenario}, world {seed}, {arm}. Test learned procedure continuity and selective correction; compare rolling, evidence-tagged, frozen and absent inheritance. Score correct actions, missing votes and command validity. Six stratified synthetic cases per step; no emergent culture claim. See immutable plan for gates and limits.'})
    return result


def qualification(a, policy, emit):
    scenario, seed, arm = a['scenario'], a['seed'], a['arm']
    feedback = []; notebook = ''
    for step in a['steps']:
        cases = tickets(seed, scenario, step, 'qualification')
        observation = {'step': step, 'cases': cases, 'commands': commands(scenario, step),
                       'history': history(seed, scenario), 'feedback': feedback, 'private_notebook': notebook}
        if arm == 'ceiling': observation['explicit_current_rule'] = explicit_rule(seed, scenario, step)
        request = {'instructions': instructions(scenario, 'rolling'), 'observation': observation}
        result = policy.complete(request)
        votes, errors = validate_output(result.get('value'), cases, commands(scenario, step))
        rows = [{'id': c['id'], 'truth': oracle(c, scenario, rules(seed, scenario, step)),
                 'action': votes.get(c['id']), 'correct': votes.get(c['id']) == oracle(c, scenario, rules(seed, scenario, step)),
                 'observed': c['id'] in votes} for c in cases]
        emit({'kind': 'qualification_step', 'scenario': scenario, 'seed': seed, 'arm': arm, 'step': step,
              'cases': cases, 'commands': commands(scenario, step), 'scores': rows,
              'evaluator': {'rule': rules(seed, scenario, step), 'stale_rule': rules(seed, scenario, 0)},
              'calls': [{'request': request, 'result': result, 'validation_errors': errors}]})
        feedback = [{'observation': c, 'accepted_action': r['truth'], 'action': r['action']} for c, r in zip(cases, rows)]
        value = result.get('value')
        if isinstance(value, dict) and isinstance(value.get('notebook'), str): notebook = value['notebook'][:700]


def instrument_hash():
    base = Path(__file__).resolve().parents[1]
    paths = sorted((base / 'src').glob('*.py')) + [base / 'PLAN.md']
    return hashlib.sha256(b''.join(str(p.relative_to(base)).encode() + p.read_bytes() for p in paths)).hexdigest()


def run(config, receipt, stage, output, qualification_root=None):
    root = Path(output)
    source = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    if subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip(): raise StopRun('clean_source_required')
    validate_receipt(receipt, source)
    if config['source_commit'] != source: raise StopRun('config_source_mismatch')
    if stage == 'S1':
        q = Path(qualification_root or '')
        summary = summarize(q)
        qm = json.loads((q / 'manifest.json').read_text())
        if not summary.get('qualification_passed') or qm['instrument_sha256'] != instrument_hash():
            raise StopRun('matching_source_qualification_required')
    if stage == 'S0-repair' and not config.get('prospective_repair_review_url'):
        raise StopRun('prospective_repair_review_required')
    design = assignments(stage)
    review_receipt = check_review(config)
    receipts = [check_plan(config, a['tldr']) for a in design]
    # All registration checks must pass before any provider exists.
    root.mkdir(); (root / 'events').mkdir(); (root / 'outcomes').mkdir()
    write_new(root / 'manifest.json', {'experiment': EXPERIMENT, 'stage': stage, 'evidence_type': 'measured_model_outputs', 'source_commit': source,
                                      'instrument_sha256': instrument_hash(), 'pre_run_review': review_receipt, 'assignments': design, 'config': config, 'deployment_receipt': receipt,
                                      'public_preflights': receipts, 'created_epoch': time.time()})
    sys.path.insert(0, '/usr/local/lib/swarm')
    import swarm_report as report
    policy = AnthropicPolicy(config, receipt, root / 'calls')
    with sqlite3.connect(policy.ledger, timeout=30) as db:
        db.execute('CREATE TABLE IF NOT EXISTS attempts (stage TEXT PRIMARY KEY, output TEXT)')
        try: db.execute('INSERT INTO attempts VALUES (?,?)', (stage, str(root.resolve())))
        except sqlite3.IntegrityError: raise StopRun('stage_already_attempted_no_invisible_reruns')

    def report_checked(kind, run_id, **kwargs):
        if not report.report(kind, EXPERIMENT, run_id, strict=True, **kwargs):
            raise StopRun('hub_event_not_acknowledged')

    def execute(a, work):
        run_id = a['run']
        report_checked('plan', run_id, message=a['tldr'], params=a, url=config['plan_url'])
        report_checked('start', run_id, message=a['tldr'], url=config['plan_url'])
        def emit(event):
            event['run'] = run_id
            event['arm'] = a['arm']
            write_new(root / 'events' / f"{run_id}-{event['step']:02d}.json", event)
            # Measured progress is the live fallback; final replay is generated below.
            n = len(event['scores']); correct = sum(r['correct'] for r in event['scores'])
            report_checked('progress', run_id, message=a['tldr'],
                           metrics={'step': event['step'], 'accuracy': correct / n})
        try:
            value = work(emit)
            write_new(root / 'outcomes' / (run_id + '.json'), {'status': 'complete', 'tldr': a['tldr']})
            report_checked('done', run_id, message=a['tldr'])
            return value
        except Exception as exc:
            reason = str(exc) if isinstance(exc, StopRun) else type(exc).__name__
            write_new(root / 'outcomes' / (run_id + '.json'), {'status': 'failed', 'safe_reason': reason, 'tldr': a['tldr']})
            report_checked('fail', run_id, message=a['tldr'] + ' Failure: ' + reason)
            raise

    def world(scenario, seed):
        selected = {a['arm']: a for a in design if a['scenario'] == scenario and a['seed'] == seed}
        if stage.startswith('S0'):
            for arm in ('ceiling', 'learner'):
                a = selected[arm]; execute(a, lambda emit: qualification(a, policy, emit))
        else:
            checkpoint = execute(selected['acquisition'], lambda emit: acquire(seed, scenario, policy, emit))
            write_new(root / f'checkpoint-{scenario}-{seed}.json', checkpoint)
            # Deterministic seed-based arm order; case streams remain matched.
            import random
            arms = list(ARMS); random.Random(f'{scenario}:{seed}').shuffle(arms)
            for arm in arms:
                execute(selected[arm], lambda emit: continuation(copy.deepcopy(checkpoint), arm, policy, emit))
    try:
        worlds = sorted({(a['scenario'], a['seed']) for a in design})
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(world, scenario, seed) for scenario, seed in worlds]
            for future in futures: future.result()
    finally:
        summary = summarize(root)
        from render import render
        render(root)
    return summary


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--stage', choices=('S0', 'S0-repair', 'S1'), required=True)
    p.add_argument('--config', required=True); p.add_argument('--receipt', required=True)
    p.add_argument('--output', required=True); p.add_argument('--qualification')
    a = p.parse_args()
    try:
        summary = run(json.loads(Path(a.config).read_text()), json.loads(Path(a.receipt).read_text()), a.stage, a.output, a.qualification)
        print(json.dumps({'stage': a.stage, 'qualification_passed': summary.get('qualification_passed'), 'audit_mismatches': summary['audit_mismatches']}))
    except Exception as exc:
        print(json.dumps({'status': 'blocked_or_failed', 'safe_reason': str(exc) if isinstance(exc, (StopRun, ValueError)) else type(exc).__name__}))
        raise SystemExit(1)
