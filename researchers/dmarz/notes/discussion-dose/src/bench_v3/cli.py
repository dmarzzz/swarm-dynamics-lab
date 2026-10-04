"""Offline by default; no implicit model, provider, launch or holdout access."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
from tasks import digest
from . import VERSION
from .worlds import cases, SPLITS
from .runner import Runner, allocation
from .journal import Journal, Replay, read_events
from .policies import Scripted, anthropic
from .analysis import summarize
from .contracts import SYSTEM, strict_json
from .replay_view import render
from .portable_audit import summary_equal


def source_hashes():
    source = Path(__file__).resolve().parent
    paths = list(source.glob('*.py')) + [source.parent / 'tasks.py', source.parent / 'providers.py']
    return {str(p.relative_to(source.parent)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def manifest(split, rounds, provider, model_config=None):
    worlds = cases(split)
    assigned, calls = allocation(worlds, rounds)
    return {'schema': VERSION, 'created_utc': datetime.now(timezone.utc).isoformat(), 'split': split,
            'runtime': {'python': platform.python_version(), 'system': platform.system(), 'machine': platform.machine()},
            'rounds': rounds, 'n_agents': 3, 'worlds': [c['id'] for c in worlds],
            'world_hashes': {str(c['id']): digest(c) for c in worlds},
            'source_hashes': source_hashes(), 'system_hash': digest(SYSTEM), 'provider': provider.name,
            'scientific': provider.scientific, 'model_config': model_config, 'assignments': assigned,
            'planned_calls': calls, 'retry_policy': 'none', 'reserved_holdout': SPLITS['holdout']}, worlds


def write_json(path, value):
    with open(path, 'x', encoding='utf-8') as stream:
        json.dump(value, stream, sort_keys=True, indent=2); stream.write('\n')


def run(destination, split='dev', rounds=3, provider=None, model_config=None, observer=None, launch_record=None):
    provider = provider or Scripted()
    frozen, worlds = manifest(split, rounds, provider, model_config)
    if launch_record is not None: frozen['launch_record'] = launch_record
    # Exclusive directory creation prevents accidental overwrite/duplicate dispatch.
    destination.mkdir(parents=True, exist_ok=False)
    write_json(destination / 'manifest.json', frozen)
    journal = Journal(destination / 'events.jsonl', observer=observer)
    try:
        journal.emit('manifest', manifest_hash=digest(frozen))
        rows = Runner(provider, journal, rounds).execute(worlds, frozen['assignments'])
        journal.emit('complete', episodes=len(rows))
        write_json(destination / 'episodes.json', rows)
        summary = summarize(frozen, rows, journal.events)
        write_json(destination / 'summary.json', summary)
        render(journal.events, rows, destination / 'replay.html')
        return summary
    finally:
        journal.close()


def audit(directory):
    frozen = strict_json((directory / 'manifest.json').read_text())
    if frozen['source_hashes'] != source_hashes():
        raise ValueError('source hashes changed; audit with the recorded source revision')
    events = read_events(directory / 'events.jsonl')
    if not events or events[0].get('manifest_hash') != digest(frozen): raise ValueError('manifest hash mismatch')
    if events[-1]['kind'] != 'complete': raise ValueError('interrupted run; assignments remain unresolved')
    saved = strict_json((directory / 'episodes.json').read_text())
    terminals = [e['record'] for e in events if e['kind'] == 'terminal']
    if terminals != saved: raise ValueError('terminal records differ from saved episodes')
    playback = Replay(events)
    journal = Journal()
    regenerated = Runner(playback, journal, frozen['rounds']).execute(cases(frozen['split']), frozen['assignments'])
    playback.finish()
    if regenerated != saved: raise ValueError('saved-response outcome replay mismatch')
    summary = summarize(frozen, regenerated, events)
    if not summary_equal(strict_json((directory / 'summary.json').read_text()), summary): raise ValueError('summary mismatch')
    rec = summary['reconciliation']
    if rec['missing'] or rec['unresolved_calls'] or rec['started_calls'] != frozen['planned_calls']:
        raise ValueError('assignment or call accounting mismatch')
    return {'ok': True, 'episodes': len(saved), 'requests_replayed': playback.calls, 'journal_events': len(events),
            'source_hashes_verified': True, 'summary_recomputed': True}


def approved_model_config(path, split, rounds):
    if path is None: raise ValueError('paid launch requires a separately reviewed launch manifest')
    launch = strict_json(path.read_text())
    required = {'status', 'source_hashes', 'split', 'rounds', 'v2_results_review', 'independent_review', 'model_config'}
    operator = launch.get('status') == 'operator-authorized-qualification'
    if operator:
        required.add('operator_authorization')
        if split != 'qualification' or type(rounds) is not int or not 0 <= rounds <= 3:
            raise ValueError('operator authorization permits only bounded qualification, never holdout')
        if launch.get('independent_review') != {'status': 'pending', 'task': 'review-discussion-benchmark-v3'}:
            raise ValueError('operator authorization must preserve pending independent review')
    if set(launch) != required or (not operator and launch['status'] != 'approved'):
        raise ValueError('launch manifest is not approved or operator-authorized')
    if launch['split'] != split or launch['rounds'] != rounds or launch['source_hashes'] != source_hashes():
        raise ValueError('launch manifest does not match this source/configuration')
    for name in ('v2_results_review', 'operator_authorization' if operator else 'independent_review'):
        proof = launch[name]
        if type(proof) is not dict or set(proof) != {'path', 'sha256'}:
            raise ValueError('review evidence must identify a file and digest')
        review = (path.parent / proof['path']).resolve()
        if hashlib.sha256(review.read_bytes()).hexdigest() != proof['sha256']:
            raise ValueError('review evidence hash mismatch')
    config = launch['model_config']
    if type(config) is not dict or set(config) != {'model', 'max_calls', 'max_output_tokens', 'max_input_bytes',
                                                  'timeout', 'max_cost_usd', 'input_usd_per_million', 'output_usd_per_million'}:
        raise ValueError('model configuration must contain only the documented nonsecret fields')
    return config


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('run'); p.add_argument('--output', type=Path, required=True)
    p.add_argument('--split', choices=list(SPLITS), default='dev'); p.add_argument('--rounds', type=int, default=3)
    p.add_argument('--backend', choices=['scripted', 'anthropic'], default='scripted')
    p.add_argument('--policy', choices=['evidence', 'abstain', 'copy_count', 'wrong_entity'], default='evidence')
    p.add_argument('--launch-manifest', type=Path)
    p = sub.add_parser('audit'); p.add_argument('directory', type=Path)
    p = sub.add_parser('inspect'); p.add_argument('--split', choices=list(SPLITS), default='dev')
    args = parser.parse_args(argv)
    try:
        if args.command == 'audit': result = audit(args.directory)
        elif args.command == 'inspect':
            frozen, worlds = manifest(args.split, 3, Scripted())
            result = {'manifest': frozen, 'examples': [{'id': c['id'], 'task': c['task'], 'allocation': c['allocation'],
                                                       'documents': c['documents']} for c in worlds]}
        else:
            config = None
            if args.backend == 'anthropic':
                config = approved_model_config(args.launch_manifest, args.split, args.rounds)
                # Reject a reserved split before constructing any network adapter.
                worlds = cases(args.split)
                if config.get('max_calls') != allocation(worlds, args.rounds)[1]: raise ValueError('model call allowance must match planned allocation')
                provider = anthropic(config)
            else: provider = Scripted(args.policy)
            launch_record = strict_json(args.launch_manifest.read_text()) if config is not None else None
            result = run(args.output, args.split, args.rounds, provider, config, launch_record=launch_record)
            result = {'scientific': result['scientific'], 'reconciliation': result['reconciliation'], 'output': str(args.output.resolve())}
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (ValueError, OSError) as exc:
        # These errors are local; provider exceptions are handled inside the journal.
        print(f'Benchmark stopped: {type(exc).__name__}: {exc}', file=sys.stderr)
        return 2
