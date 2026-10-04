#!/usr/bin/env python3
"""Reproduce all three frozen-source reports. No networking, model calls or raw exports."""
import argparse
import json
import os
from pathlib import Path
import time

os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
from askswarm.cli import run
from askswarm.report import render, lorenz_svg

FROZEN_REF = '4959a80b2e48050066630c5d22ea5d1fa1b0beb2'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', required=True, help='Parent directory containing collusion-wiki and swarmtraces')
    parser.add_argument('--repo', required=True)
    parser.add_argument('--ref', default=FROZEN_REF)
    parser.add_argument('--out', default='results')
    parser.add_argument('--sensitivity', action='store_true', help='Additional wiki/git runs at Jaccard .5 and .9')
    args = parser.parse_args()
    root, out = Path(args.data), Path(args.out)
    sources = [('wiki', root / 'collusion-wiki', 'collusion.wiki'),
               ('swarmtraces', root / 'swarmtraces', 'SwarmTraces'),
               ('git', Path(args.repo), 'swarm-lab')]
    results, timing = [], []
    for source, path, name in sources:
        start = time.monotonic()
        result = run(source, path, out / source, name, args.ref)
        results.append(result)
        timing.append({'source': source, 'threshold': .7, 'elapsed_seconds': round(time.monotonic() - start, 3)})
    (out / 'comparison.html').write_text(render(results))
    svg = lorenz_svg(results).replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="820" ', 1)
    svg = svg.replace('<path ', '<rect width="800" height="410" fill="#111719"/><path ', 1)
    svg = svg.replace('viewBox="0 0 800 410"', 'viewBox="0 0 1600 820"')
    opening, drawing = svg.split('>', 1)
    svg = opening + '><g transform="scale(2)">' + drawing.replace('</svg>', '</g></svg>')
    (out / 'participation.svg').write_text(svg)
    sensitivity = []
    if args.sensitivity:
        for threshold in (.5, .9):
            for source, path, name in (sources[0], sources[2]):
                start = time.monotonic()
                result = run(source, path, out / 'sensitivity' / f'{source}-{threshold}', name, args.ref, threshold)
                sensitivity.append({'source': source, 'threshold': threshold, 'summary': result['summary'], 'diagnostics': result['diagnostics']})
                timing.append({'source': source, 'threshold': threshold, 'elapsed_seconds': round(time.monotonic() - start, 3)})
    (out / 'sensitivity.json').write_text(json.dumps(sensitivity, indent=2) + '\n')
    (out / 'runtime.json').write_text(json.dumps({'runs': timing, 'total_seconds': sum(row['elapsed_seconds'] for row in timing),
                                               'processes': 1, 'model_calls': 0, 'paid_api_calls': 0}, indent=2) + '\n')


if __name__ == '__main__':
    main()
