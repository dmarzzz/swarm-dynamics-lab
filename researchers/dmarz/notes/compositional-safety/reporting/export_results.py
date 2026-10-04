"""Export small, auditable working results without changing frozen execution inputs.

Only the explicitly listed synthetic result files are published. This performs no
model calls, registration, network access, or ledger mutation.
"""
import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def export(source, output):
    source, output = Path(source), Path(output)
    raw = (source / 'episodes.jsonl').read_bytes()
    episodes = [json.loads(line) for line in raw.splitlines()]
    manifest = json.loads((source / 'manifest.json').read_text())
    summary = json.loads((source / 'summary.json').read_text())
    expected = {(a['task_id'], a['domain'], a['variant'], a['arm'], a['seed'])
                for a in manifest['assignments']}
    observed = {(e['task_id'], e['domain'], e['variant'], e['arm'], e['seed'])
                for e in episodes}
    assert expected == observed and len(expected) == len(episodes)
    assert len({e['episode_id'] for e in episodes}) == len(episodes)
    assert all(e['commit'] == manifest['commit'] and e['hashes'] == manifest['hashes']
               for e in episodes)
    assert summary['recorded'] == len(episodes)
    hashes = json.loads((source / 'artifact-hashes.json').read_text())
    assert hashes['episodes.jsonl'] == sha256(raw)
    # These files have been reviewed as synthetic task evidence, not arbitrary logs.
    copies = ('summary.json', 'manifest.json', 'public-plan-receipt.json',
              'artifact-hashes.json')
    output.mkdir(parents=True, exist_ok=True)
    written = []
    for name in copies:
        (output / name).write_bytes((source / name).read_bytes())
        written.append(name)
    zipped = gzip.compress(raw, compresslevel=9, mtime=0)
    assert gzip.decompress(zipped) == raw
    (output / 'episodes.jsonl.gz').write_bytes(zipped)
    written.append('episodes.jsonl.gz')
    fields = ['episode_id', 'task_id', 'domain', 'variant', 'arm', 'seed',
              'structure_sha256', 'task_sha256', 'valid', 'safe_completion',
              'violation', 'outcome', 'completed_effects', 'turns', 'calls',
              'input_tokens', 'output_tokens', 'actual_usd', 'reserved_usd']
    with (output / 'outcomes.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fields)
        writer.writeheader()
        for e in sorted(episodes, key=lambda e: e['episode_id']):
            usage = [t.get('usage', {}) for t in e['trace']]
            valid = e['validity']['ok']
            safe = bool(e['evaluation']['completion'] and valid)
            violation = bool(e['evaluation']['violation'])
            row = {key: e[key] for key in fields[:8]}
            row.update(valid=int(valid), safe_completion=int(safe),
                       violation=int(violation),
                       outcome=('invalid' if not valid else 'violation' if violation
                                else 'safe_complete' if safe else 'incomplete'),
                       completed_effects=e['evaluation']['completed_effects'],
                       turns=len(e['events']),
                       calls=sum(bool(u.get('attempted')) for u in usage),
                       input_tokens=sum(u.get('input_tokens', 0) for u in usage),
                       output_tokens=sum(u.get('output_tokens', 0) for u in usage),
                       actual_usd=f"{sum(u.get('actual_usd', 0) for u in usage):.6f}",
                       reserved_usd=f"{sum(u.get('reserved_usd', 0) for u in usage):.6f}")
            writer.writerow(row)
    written.append('outcomes.csv')
    with (output / 'events.jsonl').open('w') as handle:
        for e in sorted(episodes, key=lambda e: e['episode_id']):
            for event in e['events']:
                handle.write(json.dumps({'episode_id': e['episode_id'], **event},
                                        sort_keys=True) + '\n')
    written.append('events.jsonl')
    provenance = {
        'attempt': manifest['attempt'], 'execution_commit': manifest['commit'],
        'execution_hashes': manifest['hashes'], 'episodes': len(episodes),
        'source_episodes_bytes': len(raw), 'source_episodes_sha256': sha256(raw),
        'compression': 'gzip level 9, mtime 0; decompression preserves original bytes',
        'exporter': 'reporting/export_results.py',
        'scope': 'Working raw results; all assignments retained. Original artifact-hashes.json covers the full server bundle, not just this Git subset.',
        'files': {name: {'bytes': (output / name).stat().st_size,
                         'sha256': sha256((output / name).read_bytes())} for name in written},
    }
    (output / 'publication-manifest.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(json.dumps({'episodes': len(episodes), 'source_bytes': len(raw),
                      'compressed_bytes': len(zipped), 'exported_files': len(written) + 1}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    export(args.source, args.output)
