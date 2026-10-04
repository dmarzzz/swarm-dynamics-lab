"""One finite worker: takes one queued run, executes one stage once, uploads the record.

  python3 src/worker.py --hub                         take the next queued run from the hub
  python3 src/worker.py --stage s0 --attempt NAME     offline S0 into results/NAME (no hub, no model)

No automatic re-execution: a run the hub hands out a second time is refused. Paid stages need
the committed approval record (launch.py) and the persistent ledger path in SOC07_BUDGET_LEDGER.
"""
import argparse
import gzip
import json
import os
import shutil
import time
from pathlib import Path

import analyze
import config
import coordinator
import journal as journal_module
import launch
import render
import s0
import study


def write_json(path, value):
    with open(path, 'x') as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.flush()
        os.fsync(f.fileno())


def upload(run, path):
    receipt = run.artifact(path, Path(path).name)
    if not receipt or receipt.get('spooled'):
        raise RuntimeError('artifact_not_durably_acknowledged')


def gz(path):
    target = Path(str(path) + '.gz')
    with open(path, 'rb') as src, gzip.open(target, 'wb') as dst:
        shutil.copyfileobj(src, dst)
    return target


def _state(p, mode, plan_counts, **kw):
    base = {'stage': p['stage'], 'mode': mode, 'backend': p['backend'], 'planned_episodes': plan_counts['episodes'],
            'blocks': plan_counts['blocks'], 'blocks_done': 0, 'elapsed': 0.0, 'calls': 0, 'cost_usd': 0.0,
            'input_tokens': 0, 'output_tokens': 0, 'failures': 0}
    base.update(kw)
    return base


def execute_s0(p, out, run=None):
    started = time.monotonic()

    def progress(step, total, label):
        if run:
            run.progress(step, total, message='S0 scripted: ' + label, force=True, model_calls=0, cost_usd=0.0)
    result = s0.run_suite(out, progress, durable=True)
    report = result['report']
    live = result['episodes']['live.evidence_follower']
    summary = result['summaries']['live.evidence_follower']
    counts = {'episodes': 300, 'blocks': 60}
    snapshots = []
    for done in range(0, 61, 5):
        prefix = live[:done * 5]
        agents = [a for e in prefix for a in e['agents']]
        snapshots.append((prefix, _state(
            p, 'live', counts, blocks_done=done, elapsed=time.monotonic() - started if done == 60 else 0.0,
            calls=done * 85, input_tokens=0, output_tokens=0,
            failures=sum(bool(a['flags']) for a in agents),
            series='Shown: the scripted evidence-following policy on the 60 fixtures. All four policies and the '
                   'fault injections: %d of %d checks passed.' % (sum(c['passed'] for c in report.checks), len(report.checks)),
            note='Scripted rehearsal of generator, access rules, scorer and accounting. Not model behaviour.')))
    frames = render.replay(snapshots, out)
    arms = summary['arms']
    doc = {
        'params': p, 'stage': 's0', 'model_calls': 0, 'cost_usd': 0.0,
        'scripted_calls': result['counts']['scripted_calls'], 'worlds': result['counts']['worlds'],
        'episodes': result['counts']['episodes'], 'checks': report.checks,
        'checks_passed': sum(c['passed'] for c in report.checks), 'checks_total': len(report.checks),
        'gate_passed': report.passed(), 'elapsed_seconds': time.monotonic() - started,
        'team_success': {name: {arm: s['arms'][arm]['team_success_equal_weight'] for arm in config.ARMS}
                         for name, s in result['summaries'].items()},
        'visualization': {'mapping': 'v1', 'frames': frames}}
    write_json(out / 'summary.json', doc)
    write_json(out / 'analysis.json', result['summaries'])
    if run:
        for name in ('final_frame.png', 'replay.gif', 'initial_frame.png', 'summary.json', 'analysis.json'):
            upload(run, out / name)
    if not report.passed():
        raise RuntimeError('s0_checks_failed_preserved')
    if run:
        run.done(message='S0 scripted: %d/%d checks passed on 60 fixtures, 4 policies and fault injections; 0 model calls' % (
                     doc['checks_passed'], doc['checks_total']),
                 episodes=doc['episodes'], team_success_private=arms['private']['team_success_equal_weight'],
                 team_success_public=arms['public']['team_success_equal_weight'], private_minus_public=0.0,
                 valid_rate=1.0, failures=doc['checks_total'] - doc['checks_passed'], model_calls=0, cost_usd=0.0,
                 gate_passed=1)
    return doc


def execute_paid(p, out, run=None, adapter_factory=None, ledger=None):
    stage = p['stage']
    launch.check(stage)                         # refuse before any provider object exists
    plan = study.manifest(stage)
    mode = plan['mode']
    write_json(out / 'manifest.json', plan)
    if ledger is None:
        path = os.environ.get('SOC07_BUDGET_LEDGER')
        if not path:
            raise RuntimeError('persistent_budget_ledger_required')
        ledger = study.paid_ledger(path, plan)
    before = ledger.totals()
    if adapter_factory is None:
        from adapter import AnthropicAdapter
        adapter_factory = lambda on_attempt: AnthropicAdapter(on_attempt)
    started = time.monotonic()
    snapshots, last = [], [0.0]
    reporting_errors = []

    def state(controller, done):
        t = controller.totals if controller else {'calls': 0, 'failed': 0, 'input_tokens': 0, 'output_tokens': 0, 'billed_usd': 0.0}
        return _state(p, mode, plan['counts'], blocks_done=done, elapsed=time.monotonic() - started, calls=t['calls'],
                      failures=t['failed'], cost_usd=t['billed_usd'], input_tokens=t['input_tokens'],
                      output_tokens=t['output_tokens'])

    def progress(done, total, episodes, controller):
        current = state(controller, done)
        snapshots.append((list(episodes), current))
        if not run:
            return
        run.progress(done, total, episodes=len(episodes), failures=current['failures'], model_calls=current['calls'],
                     cost_usd=current['cost_usd'],
                     message='halted: ' + controller.halted if controller.halted else None)
        if time.monotonic() - last[0] > 20 or done == total:
            try:
                render.frame(episodes, current).save(out / 'progress.png')
                upload(run, out / 'progress.png')
            except Exception as exc:  # a reporting failure never changes or stops the run
                reporting_errors.append(type(exc).__name__)
            last[0] = time.monotonic()
    snapshots.append(([], state(None, 0)))
    if run:
        render.frame([], snapshots[0][1]).save(out / 'progress.png')
        upload(run, out / 'progress.png')
    episodes, controller, crash = study.run(plan, out, adapter_factory, ledger, progress)
    name = plan['namespace']
    events = list(journal_module.read(out / ('journal-%s.jsonl' % name)))
    stats = analyze.call_stats(events, plan)
    after = ledger.totals()
    if mode == 'qualification':
        analysis = {'qualification': analyze.qualification(episodes)}
        gate = {'checks': {'qualification': analysis['qualification']['passed'],
                           'no_crash_or_halt': crash is None and controller.halted is None},
                'passed': analysis['qualification']['passed'] and crash is None and controller.halted is None}
    else:
        analysis = analyze.summarize(episodes)
        gate = analyze.s1_gate(stats, controller.leaks, crash, controller.halted, mode, analysis)
    completed = [e for e in episodes if e['execution'] == 'completed']
    snapshots.append((list(episodes), state(controller, snapshots[-1][1]['blocks_done'])))
    frames = render.replay(snapshots, out)
    doc = {
        'params': p, 'stage': stage, 'namespace': name, 'mode': mode, 'manifest_hash': plan['manifest_hash'],
        'hashes': plan['hashes'], 'launch_manifest': plan['launch_manifest'],
        'reconciliation': {'planned': len(plan['episodes']), 'terminal': len(episodes), 'completed': len(completed),
                           'interrupted': sum(e['execution'] == 'interrupted' for e in episodes),
                           'incomplete': sum(e['execution'] == 'incomplete' for e in episodes),
                           'graded': sum(e['decision'] != 'unavailable' for e in episodes), 'analyzed': len(episodes)},
        'calls': stats, 'halted': controller.halted, 'crash': crash, 'leaks': controller.leaks, 'gate': gate,
        'stage_billed_usd': after['billed_usd'] - before['billed_usd'],
        'study_ledger_before': before, 'study_ledger_after': after,
        'elapsed_seconds': time.monotonic() - started, 'reporting_errors': reporting_errors,
        'visualization': {'mapping': 'v1', 'frames': frames}}
    write_json(out / 'summary.json', doc)
    write_json(out / 'analysis.json', analysis)
    if run:
        for path in (out / 'summary.json', out / 'analysis.json', out / 'manifest.json',
                     gz(out / ('episodes-%s.jsonl' % name)), gz(out / ('journal-%s.jsonl' % name))):
            upload(run, path)
        for image in ('final_frame.png', 'replay.gif', 'progress.png', 'initial_frame.png'):
            if (out / image).exists():
                upload(run, out / image)   # re-sent in this order so the final frame is the run's first image
    metrics = {'episodes': len(episodes), 'valid_rate': stats['valid_rate'] or 0.0,
               'failures': sum(stats['failures'].values()) + len(episodes) - len(completed),
               'model_calls': stats['sent_to_provider'], 'cost_usd': doc['stage_billed_usd'], 'gate_passed': int(gate['passed'])}
    if mode == 'qualification':
        metrics['solver_accuracy'] = analysis['qualification']['correct'] / max(1, len(episodes))
        message = 'S1-Q: %d/12 correct, %d/12 valid' % (analysis['qualification']['correct'], analysis['qualification']['valid'])
    else:
        arms = analysis['arms']
        metrics.update(team_success_private=arms['private']['team_success_equal_weight'],
                       team_success_public=arms['public']['team_success_equal_weight'],
                       private_minus_public=analysis['primary']['difference'])
        message = '%s: %d/%d episodes completed; private minus public %+.3f (exploratory)' % (
            config.STAGE_LABELS[stage], len(completed), len(episodes), analysis['primary']['difference'])
    if not gate['passed']:
        if run:
            run.fail(message=message + '; gate failed: ' + ', '.join(k for k, v in gate['checks'].items() if not v), **metrics)
        raise RuntimeError('stage_gate_failed_record_preserved')
    if run:
        run.done(message=message, **metrics)
    return doc


def execute(p, out, run=None, **kw):
    if p['source_hash'] != config.source_hash():
        raise RuntimeError('runtime_source_mismatch')
    if p['backend'] != ('scripted' if p['stage'] == 's0' else 'anthropic'):
        raise RuntimeError('backend_does_not_match_stage')
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    return execute_s0(p, out, run) if p['stage'] == 's0' else execute_paid(p, out, run, **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hub', action='store_true')
    ap.add_argument('--stage', choices=['s0'])
    ap.add_argument('--attempt')
    a = ap.parse_args()
    if a.hub:
        import swarm_report as sr
        run = sr.next_run(coordinator.EXPERIMENT)
        if run is None:
            return
        if run.attempt != 1:
            raise RuntimeError('automatic_reexecution_forbidden')
        with run:
            execute(run.params, config.ROOT / 'results' / ('%s-attempt-%s' % (run.id.replace('/', '__'), run.attempt)), run)
    else:
        if a.stage != 's0' or not a.attempt or not a.attempt.replace('-', '').isalnum():
            raise SystemExit('Offline runs are S0 only and need a fresh --attempt name')
        doc = execute(coordinator.params('s0'), config.ROOT / 'results' / a.attempt)
        print(json.dumps({k: doc[k] for k in ('checks_passed', 'checks_total', 'gate_passed', 'episodes', 'scripted_calls', 'model_calls')}))


if __name__ == '__main__':
    main()
