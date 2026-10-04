#!/usr/bin/env python3
"""Offline robustness on the frozen three corpora; derived exports only.

Optional blind review text lives exclusively outside the repository, never in results.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import re
import time
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
from askswarm import wiki, swarmtraces, git_log
from askswarm.cli import save_result, checksum
from askswarm.robustness import robustness, root_ids
from askswarm.report import render, table
from run_all import FROZEN_REF


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def prepare_sample(source, events, report, rng):
    links = report['_reuse_links']
    lookup = {e.event_id: e for e in events}
    roots = root_ids(events)
    samples = []
    for link in rng.sample(links, min(15, len(links))):
        a, b = lookup[link['prior_event']], lookup[link['later_event']]
        names = {e.agent_id for e in (a, b) if e.agent_id}
        def redact(text):
            for name in sorted(names, key=len, reverse=True):
                text = re.sub(re.escape(name), '[HANDLE]', text, flags=re.I)
            # Conceal explicit wall-clock/date cues, but preserve numerical content otherwise.
            return re.sub(r'\b20\d\d-\d\d-\d\d(?:[T ][0-9:.+Z-]+)?\b', '[DATE]', text)
        texts = [redact(a.text), redact(b.text)]
        flip = rng.choice([False, True])
        if flip:
            texts.reverse()
        samples.append({'source': source, 'prior_event': a.event_id, 'later_event': b.event_id,
                        'same_root': roots[a.event_id] == roots[b.event_id],
                        'prior_time': a.time, 'later_time': b.time, 'flipped': flip,
                        'text_sha256': [hashlib.sha256(e.text.encode()).hexdigest() for e in (a, b)],
                        'texts': texts})
    return samples, len(links)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', required=True)
    p.add_argument('--repo', required=True)
    p.add_argument('--out', default='results/robustness-v1')
    p.add_argument('--audit-local', help='Local review directory outside repository; never commit raw texts')
    args = p.parse_args()
    out, data = Path(args.out), Path(args.data)
    if out.exists():
        raise SystemExit('Refusing to overwrite existing robustness run')
    audit = Path(args.audit_local).resolve() if args.audit_local else None
    if audit and (audit == Path(args.repo).resolve() or Path(args.repo).resolve() in audit.parents):
        raise SystemExit('Audit raw review text must stay outside repository')
    if audit:
        audit.mkdir(parents=True, exist_ok=True)
    rng = random.Random(202610041114)
    samples, populations, summaries, all_reports = [], {}, {}, []
    start = time.monotonic()
    for source, loader, path in [('wiki', wiki, data / 'collusion-wiki'),
                                 ('git', lambda p: git_log(p, FROZEN_REF), Path(args.repo)),
                                 ('swarmtraces', swarmtraces, data / 'swarmtraces')]:
        print('start', source, flush=True)
        rows = list(loader(path))
        result = robustness(rows, name=source)
        if audit:
            selected, population = prepare_sample(source, rows, result['reports']['baseline'], rng)
            samples.extend(selected)
            populations[source] = population
        summaries[source] = {'transformations': result['transformations'], 'comparisons': result['comparisons']}
        for arm, report in result['reports'].items():
            clean = {k: v for k, v in report.items() if not k.startswith('_')}
            clean['source'] = {'frozen_baseline': '../../../' + source + '/metrics.json',
                               'git_ref': FROZEN_REF if source == 'git' else None,
                               'transformation': arm, 'receipt': result['transformations'][arm],
                               'code_sha256': {f.name: checksum(f) for f in sorted(Path('askswarm').glob('*.py'))}}
            save_result(clean, out / source / arm)
            all_reports.append(clean)
        dump(out / source / 'rank-scores.json', result['scores'])
        dump(out / source / 'comparison.json', summaries[source])
        print('done', source, {a: r['summary']['records'] for a, r in result['reports'].items()}, flush=True)
    if audit:
        rng.shuffle(samples)
        blind, key = [], []
        for index, sample in enumerate(samples, 1):
            sample_id = f'B{index:02}'
            blind.append({'sample_id': sample_id, 'A': sample['texts'][0], 'B': sample['texts'][1]})
            key.append({'sample_id': sample_id, **{k:v for k,v in sample.items() if k != 'texts'}})
        dump(audit / 'blind.json', blind)
        dump(audit / 'key.json', key)
        # Short deterministic context excerpts for initial reading; full blind pair retained locally.
        blocks = []
        for pair in blind:
            blocks.append('\n## ' + pair['sample_id'])
            for side in ('A', 'B'):
                text = pair[side]
                if len(text) > 5000:
                    text = text[:2000] + '\n[... OMITTED; full pair in blind.json ...]\n' + text[len(text)//2:len(text)//2+1000] + '\n[...]\n' + text[-2000:]
                blocks.append(f'### {side} ({len(pair[side])} original characters)\n{text}')
        (audit / 'blind.md').write_text('\n'.join(blocks))
        dump(out / 'audit-sampling.json', {'seed': 202610041114, 'populations': populations,
                                           'sample_sizes': {s:sum(k['source'] == s for k in key) for s in populations},
                                           'blind_packet_sha256': checksum(audit / 'blind.json'),
                                           'key_sha256': checksum(audit / 'key.json'),
                                           'unit': 'directed prior-identity to first-later-identity lexical-credit link'})
    dump(out / 'summary.json', summaries)
    dump(out / 'runtime.json', {'seconds': round(time.monotonic() - start, 3), 'processes': 1,
                                'model_calls': 0, 'paid_api_calls': 0})
    (out / 'comparison.html').write_text(render(all_reports, 'AskSwarm / all robustness arms'))
    # The rank diagnostic is separate from full per-arm answers to keep both navigable.
    html = '<!doctype html><meta charset="utf-8"><title>AskSwarm robustness ranks</title><h1>Descriptive rank movement</h1>'
    html += '<p>Top 10 includes boundary ties. Spearman uses common support; entries/exits are separate. No causal influence is identified.</p>'
    for source, result in summaries.items():
        html += '<h2>' + source + '</h2>'
        rows = []
        for arm, comparison in result['comparisons'].items():
            for metric, values in comparison['identity_rankings'].items():
                rows.append([arm, metric] + [values[k] for k in ('before_ranked', 'after_ranked', 'common', 'exited', 'entered', 'common_spearman', 'mean_absolute_rank_shift', 'top_overlap', 'top_jaccard')])
        html += table(['Arm','Ranking','Before','After','Common','Exited','Entered','Spearman','Mean shift','Top overlap','Top Jaccard'], rows)
    (out / 'rankings.html').write_text(html)


if __name__ == '__main__':
    main()
