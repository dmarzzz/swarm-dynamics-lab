import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import numpy as np
from . import adapters
from .core import analyze
from .report import render, write_report


def checksum(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def run(source, data, output, name=None, ref='HEAD', threshold=.7, window=100, wiki_identity='label'):
    path = Path(data)
    if source == 'wiki':
        path = path / 'revisions.jsonl.gz' if path.is_dir() else path
        events = adapters.wiki(path, wiki_identity)
    elif source == 'swarmtraces':
        path = path / 'redacted.jsonl.gz' if path.is_dir() else path
        events = adapters.swarmtraces(path)
    elif source == 'git':
        events = adapters.git_log(path, ref)
    else:
        events = adapters.table(path)
    result = analyze(events, name or source, threshold, window)
    provenance = {'adapter': source, 'python': platform.python_version(), 'numpy': np.__version__}
    if source == 'git':
        provenance['git_ref'] = subprocess.check_output(['git', '-C', str(path), 'rev-parse', '--verify', '--end-of-options', ref + '^{commit}'], text=True).strip()
        provenance['time_basis'] = 'git author timestamp, not validated real execution time'
    else:
        provenance.update({'file': path.name, 'sha256': checksum(path), 'bytes': path.stat().st_size})
    if source == 'wiki':
        provenance['identity_basis'] = wiki_identity
        result['limits'].append('Wiki records are full revision snapshots; retained page content and shared handles can mimic adoption.')
    if source == 'swarmtraces':
        result['limits'].append('Artifact kinds include attack payloads and recovered copies. No verified actor field or clock exists in this redacted release; content sign-offs are not extracted.')
    if source == 'git':
        result['limits'].append('Agent prefixes are self-asserted; administrative commit templates can produce lexical reuse without research-idea transmission.')
    result['source'] = provenance
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'metrics.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    write_report(result, output / 'report.html')
    print(json.dumps({'name': result['name'], **result['summary']}, allow_nan=False))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description='Ask the same descriptive questions of any agent/time/text table. No API calls.')
    sub = parser.add_subparsers(dest='command', required=True)
    one = sub.add_parser('analyze')
    one.add_argument('--source', choices=['table', 'wiki', 'swarmtraces', 'git'], required=True)
    one.add_argument('--data', required=True)
    one.add_argument('--out', required=True)
    one.add_argument('--name')
    one.add_argument('--ref', default='HEAD')
    one.add_argument('--threshold', type=float, default=.7)
    one.add_argument('--window', type=int, default=100)
    one.add_argument('--wiki-identity', choices=['label', 'ip16'], default='label')
    comparison = sub.add_parser('compare')
    comparison.add_argument('metrics', nargs='+')
    comparison.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    if args.command == 'analyze':
        run(args.source, args.data, args.out, args.name, args.ref, args.threshold, args.window, args.wiki_identity)
    else:
        results = [json.loads(Path(p).read_text()) for p in args.metrics]
        destination = Path(args.out)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render(results), encoding='utf-8')
        print(destination)


if __name__ == '__main__':
    main()
