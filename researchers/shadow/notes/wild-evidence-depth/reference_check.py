#!/usr/bin/env python3
"""Separate set-based arithmetic check, same author, not independent peer review."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', required=True, type=Path)
    ap.add_argument('--summary', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    expected = json.loads(args.summary.read_text())
    payloads, ids, texts = set(), set(), set()
    response_parents = []
    all_parents = []
    kinds = Counter()
    count = nonempty = dated = 0
    with gzip.open(args.data, 'rt') as stream:
        for line in stream:
            r = json.loads(line)
            count += 1
            assert r['id'] not in ids
            ids.add(r['id'])
            kinds[r['kind']] += 1
            if r['kind'] == 'payload':
                payloads.add(r['id'])
            if r['kind'] == 'response' and r.get('parent_id'):
                response_parents.append(r['parent_id'])
            if r.get('parent_id'):
                all_parents.append(r['parent_id'])
            if r.get('text'):
                nonempty += 1
                texts.add(hashlib.sha256(r['text'].encode()).hexdigest())
            dated += r.get('time_utc') is not None
    actual = {
        'rows': count,
        'payloads': len(payloads),
        'payloads_with_direct_response': len(payloads & set(response_parents)),
        'response_rows_with_direct_payload_parent': sum(p in payloads for p in response_parents),
        'valid_parent_edges': sum(p in ids for p in all_parents),
        'orphan_parent_rows': sum(p not in ids for p in all_parents),
        'nonnull_timestamp_rows': dated,
        'distinct_nonempty_released_texts': len(texts),
        'nonempty_text_rows': nonempty,
        'components_if_forest': count - sum(p in ids for p in all_parents),
    }
    reported = {
        'rows': expected['rows'],
        'payloads': expected['kinds']['payload']['rows'],
        'payloads_with_direct_response': expected['payload_direct_response_coverage']['numerator'],
        'response_rows_with_direct_payload_parent': expected['response_rows_with_direct_payload_parent']['numerator'],
        'valid_parent_edges': expected['graph']['valid_parent_edges'],
        'orphan_parent_rows': expected['graph']['orphan_parent_rows'],
        'nonnull_timestamp_rows': expected['nonnull_timestamp_rows'],
        'distinct_nonempty_released_texts': expected['text_sensitivity']['distinct_nonempty_released_texts'],
        'nonempty_text_rows': expected['text_sensitivity']['nonempty_rows'],
        'components_if_forest': expected['graph']['components'],
    }
    assert actual == reported, (actual, reported)
    assert dict(kinds) == {k: v['rows'] for k, v in expected['kinds'].items()}
    receipt = {'status': 'pass', 'author': 'shadow/sol-audit-gap',
               'independence': 'Separate implementation, same author; not peer review',
               'checked_metrics': actual, 'kinds': dict(kinds),
               'reference_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.out.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
