#!/usr/bin/env python3
"""Render the single final figure from preserved aggregates, no source-data loading.

Also repair undefined numeric JSON scalars to null (same result, strict JSON),
retaining the original draft representation in git history.
"""
import argparse
import json
import math
from pathlib import Path

import halflife as H


def finite_json(obj):
    if isinstance(obj, dict):
        return {k: finite_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [finite_json(v) for v in obj]
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    return obj


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--results', required=True)
    a = p.parse_args()
    out = Path(a.results)
    for name in ('summary.json', 'posthoc.json'):
        data = finite_json(json.loads((out/name).read_text()))
        (out/name).write_text(json.dumps(data, indent=1, allow_nan=False)+'\n')
    summary = json.loads((out/'summary.json').read_text())
    extra = json.loads((out/'supplement.json').read_text())
    H.figure(summary, out/'fig-adoption.png', extra['wiki_visible_pages_url'])
    from PIL import Image
    size = Image.open(out/'fig-adoption.png').size
    assert size[0] >= 1600
    print('Figure dimensions:', size, '; undefined JSON scalars converted to null')


if __name__ == '__main__':
    main()
