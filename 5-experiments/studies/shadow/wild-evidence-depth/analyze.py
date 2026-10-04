#!/usr/bin/env python3
"""Offline parent-aware artifact census. Never executes or decodes source text.

Standard library only. Outputs aggregates, not raw dataset rows or payload text.
"""
import argparse
from collections import Counter, defaultdict, deque
import csv
import gzip
import hashlib
import html
import json
from pathlib import Path
import platform

KINDS = ('payload', 'recovered_text', 'response')
BINS = ('0', '1-255', '256-1023', '1024-4095', '4096+')


def length_bin(n):
    return BINS[0 if n == 0 else 1 if n < 256 else 2 if n < 1024 else 3 if n < 4096 else 4]


def sha_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def fraction(n, d):
    return {'numerator': n, 'denominator': d, 'fraction': n / d if d else None}


def census(rows):
    nodes = {}
    for row in rows:
        ident = row.get('id')
        kind = row.get('kind')
        text = row.get('text')
        parent = row.get('parent_id')
        if not isinstance(ident, str) or not ident or ident in nodes:
            raise ValueError('Missing or duplicate record id')
        if kind not in KINDS:
            raise ValueError('Unknown record kind')
        if text is not None and not isinstance(text, str):
            raise ValueError('Text must be a string or null')
        if parent is not None and not isinstance(parent, str):
            raise ValueError('Parent must be a string or null')
        nodes[ident] = {
            'kind': kind, 'parent': parent or None,
            'length': len(text or ''), 'text_null': text is None,
            'hash': hashlib.sha256(text.encode('utf-8')).hexdigest() if text else None,
            'dated': row.get('time_utc') is not None,
            'children': 0, 'size': 1, 'desc_mask': 0, 'direct_response': 0,
        }
    counts = Counter(n['kind'] for n in nodes.values())
    edges = Counter()
    orphan = Counter()
    roots = Counter()
    for ident, n in nodes.items():
        parent = n['parent']
        if parent == ident:
            raise ValueError('Self-linked parent: cyclic provenance')
        if parent in nodes:
            p = nodes[parent]
            p['children'] += 1
            p['direct_response'] += n['kind'] == 'response'
            edges[(n['kind'], p['kind'])] += 1
        elif parent:
            orphan[n['kind']] += 1
        else:
            roots[n['kind']] += 1
    # Leaf-to-root accumulation computes descendants without recursive depth limits.
    pending = {i: n['children'] for i, n in nodes.items()}
    queue = deque(i for i, degree in pending.items() if degree == 0)
    processed = 0
    components = []
    bits = {kind: 1 << i for i, kind in enumerate(KINDS)}
    while queue:
        ident = queue.popleft()
        n = nodes[ident]
        processed += 1
        parent = n['parent']
        if parent in nodes:
            p = nodes[parent]
            p['size'] += n['size']
            p['desc_mask'] |= n['desc_mask'] | bits[n['kind']]
            pending[parent] -= 1
            if pending[parent] == 0:
                queue.append(parent)
        else:
            components.append(n['size'])
    if processed != len(nodes):
        raise ValueError('Cyclic provenance graph')
    assert sum(components) == len(nodes)
    by_hash = defaultdict(Counter)
    per_kind = {}
    for n in nodes.values():
        if n['hash']:
            by_hash[n['hash']][n['kind']] += 1
    for kind in KINDS:
        group = [n for n in nodes.values() if n['kind'] == kind]
        texts = Counter(n['hash'] for n in group if n['hash'])
        per_kind[kind] = {
            'rows': len(group),
            'nonempty_text_rows': sum(texts.values()),
            'empty_text_rows': sum(n['length'] == 0 and not n['text_null'] for n in group),
            'null_text_rows': sum(n['text_null'] for n in group),
            'unique_nonempty_released_texts': len(texts),
            'redundant_text_rows': sum(texts.values()) - len(texts),
            'rows_in_repeated_text_groups': sum(v for v in texts.values() if v > 1),
            'max_text_multiplicity': max(texts.values(), default=0),
            'nonnull_timestamp_rows': sum(n['dated'] for n in group),
            'no_parent_rows': roots[kind],
            'orphan_parent_rows': orphan[kind],
        }
    payloads = [n for n in nodes.values() if n['kind'] == 'payload']
    categories = Counter()
    bins = {label: {'payloads': 0, 'with_direct_response': 0, 'with_response_descendant': 0}
            for label in BINS}
    for n in payloads:
        response = bool(n['desc_mask'] & bits['response'])
        recovered = bool(n['desc_mask'] & bits['recovered_text'])
        category = ('response_descendant' if response else
                    'recovered_without_response' if recovered else
                    'other_descendants_only' if n['size'] > 1 else 'no_descendants')
        categories[category] += 1
        b = bins[length_bin(n['length'])]
        b['payloads'] += 1
        b['with_direct_response'] += n['direct_response'] > 0
        b['with_response_descendant'] += response
    for b in bins.values():
        b['direct_response_fraction'] = (b['with_direct_response'] / b['payloads']) if b['payloads'] else None
    n_direct = sum(n['direct_response'] > 0 for n in payloads)
    nonempty = sum(sum(kinds.values()) for kinds in by_hash.values())
    multiplicity = Counter(sum(kinds.values()) for kinds in by_hash.values())
    cross_kind = {f'{a}__{b}': sum(a in kinds and b in kinds for kinds in by_hash.values())
                  for i, a in enumerate(KINDS) for b in KINDS[i + 1:]}
    return {
        'schema_version': 1,
        'scope': 'Census of one selected released artifact corpus; no independent-event, actor, execution or success estimate.',
        'rows': len(nodes), 'kinds': per_kind,
        'payload_direct_response_coverage': fraction(n_direct, len(payloads)),
        'payload_response_descendant_coverage': fraction(categories['response_descendant'], len(payloads)),
        'payload_descendant_categories': {c: categories[c] for c in (
            'response_descendant', 'recovered_without_response', 'other_descendants_only', 'no_descendants')},
        'response_rows_with_direct_payload_parent': fraction(edges[('response', 'payload')], counts['response']),
        'graph': {
            'valid_parent_edges': sum(edges.values()), 'orphan_parent_rows': sum(orphan.values()),
            'no_parent_rows': sum(roots.values()), 'components': len(components),
            'singleton_components': sum(size == 1 for size in components),
            'max_component_rows': max(components, default=0),
            'component_size_histogram': dict(sorted(Counter(components).items())),
            'child_parent_kind_edges': [{'child_kind': a, 'parent_kind': b, 'count': v}
                                       for (a, b), v in sorted(edges.items())],
        },
        'text_sensitivity': {
            'nonempty_rows': nonempty, 'distinct_nonempty_released_texts': len(by_hash),
            'redundant_rows': nonempty - len(by_hash),
            'rows_in_repeated_text_groups': sum(size * groups for size, groups in multiplicity.items() if size > 1),
            'max_multiplicity': max(multiplicity, default=0),
            'multiplicity_histogram': dict(sorted(multiplicity.items())),
            'cross_kind_shared_text_hashes': cross_kind,
            'warning': 'Equal redacted strings can arise from redaction or reconstruction; neither text hashes nor parent components certify independent events.',
        },
        'payload_length_strata_characters': bins,
        'nonnull_timestamp_rows': sum(n['dated'] for n in nodes.values()),
        'cost_usd': 0, 'model_calls': 0,
    }


def read_rows(path):
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rt', encoding='utf-8') as stream:
        for line in stream:
            if line.strip():
                yield json.loads(line)


def pct(n, d):
    return f'{100 * n / d:.2f}%' if d else 'unavailable'


def render_svg(result):
    total = result['kinds']['payload']['rows']
    direct = result['payload_direct_response_coverage']['numerator']
    categories = result['payload_descendant_categories']
    values = [('Direct response child (primary)', direct, '#77d9b5')]
    values += [(name.replace('_', ' '), value, color) for (name, value), color in zip(
        categories.items(), ('#77d9b5', '#c4b5fd', '#f0bf70', '#8999aa'))]
    text = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="830" viewBox="0 0 1600 830">',
            '<rect width="1600" height="830" fill="#10161e"/>',
            '<g font-family="monospace" fill="#edf3f7">',
            '<text x="60" y="75" font-size="32">SwarmTraces: evidence depth, not attack success</text>',
            f'<text x="60" y="120" font-size="22">{total:,} payload artifacts; {result["rows"]:,} released rows</text>']
    for i, (label, value, color) in enumerate(values):
        y = 180 + i * 105
        if i == 1:
            text.append('<text x="60" y="259" font-size="17">Below: mutually exclusive descendant categories (not additional samples)</text>')
        text += [f'<text x="60" y="{y}" font-size="19">{html.escape(label)}: {value:,}/{total:,} ({pct(value, total)})</text>',
                 f'<rect x="60" y="{y+14}" width="1480" height="30" fill="#28323e"/>',
                 f'<rect x="60" y="{y+14}" width="{1480*value/total if total else 0:.3f}" height="30" fill="{color}"/>']
    text += ['<text x="60" y="750" font-size="20">Response artifact != successful execution. Missing response != failed execution.</text>',
             '<text x="60" y="790" font-size="18">One selected corpus; no IID uncertainty or temporal ordering inferred.</text></g></svg>']
    return '\n'.join(text)


def render_html(result):
    d = result['payload_direct_response_coverage']
    return ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
            '<title>SwarmTraces evidence depth</title><style>body{background:#10161e;color:#edf3f7;font:18px/1.6 monospace;'
            'max-width:1100px;margin:40px auto;padding:24px}img{width:100%}pre{overflow:auto;font-size:13px}a{color:#77d9b5}</style>'
            '<h1>What does this incident export actually let us observe?</h1>'
            f'<p><strong>{d["numerator"]:,}/{d["denominator"]:,} payload artifacts ({pct(d["numerator"], d["denominator"])})</strong>'
            ' have a direct response child. This is artifact linkage, not an attack-success rate.</p>'
            '<img src="coverage.svg" alt="Payload response and reconstruction coverage with full denominators">'
            '<p>Parent links are reconstruction provenance, not conversation turns. Exact equal redacted texts do not prove shared origin.'
            ' No payload is executed, decoded or sent to a model. Null timestamps are left null.</p>'
            '<p>Source: <a href="https://swarmtraces.org/">SwarmTraces</a>. '
            '<a href="summary.json">Aggregate JSON and fingerprints</a>.</p>'
            '<details><summary>All derived counts</summary><pre>' + html.escape(json.dumps(result, indent=2)) + '</pre></details></html>')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    result = census(read_rows(args.data))
    result['provenance'] = {
        'source_filename': args.data.name, 'compressed_input_sha256': sha_file(args.data),
        'analyzer_sha256': sha_file(__file__), 'python': platform.python_version(),
        'source_url': 'https://swarmtraces.org/data/final/redacted.jsonl.gz',
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    (args.out / 'coverage.svg').write_text(render_svg(result))
    (args.out / 'index.html').write_text(render_html(result))
    with (args.out / 'length-strata.csv').open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=['text_length_characters', 'payloads', 'with_direct_response',
                                                   'with_response_descendant', 'direct_response_fraction'])
        writer.writeheader()
        for label, counts in result['payload_length_strata_characters'].items():
            writer.writerow({'text_length_characters': label, **counts})
    print(json.dumps({k: result[k] for k in ('rows', 'payload_direct_response_coverage',
                     'payload_response_descendant_coverage', 'payload_descendant_categories', 'nonnull_timestamp_rows')}, indent=2))


if __name__ == '__main__':
    main()
