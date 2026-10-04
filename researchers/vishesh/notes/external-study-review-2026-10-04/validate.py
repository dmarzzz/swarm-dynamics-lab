"""Offline consistency/link checks for the recommendation package; no experiment dispatch."""
import json
import re
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
manifest = json.loads((HERE / 'recommendations.json').read_text())
coverage = json.loads((HERE / 'coverage.json').read_text())
rows = manifest['recommendations']
assert len(rows) == coverage['ranked_recommendations'] == 229
assert len(manifest['studies']) == coverage['study_documents'] == 15
assert len({r['id'] for r in rows}) == len(rows)
assert Counter(r['disposition'] for r in rows) == coverage['dispositions']
checked_links = 0
for s in manifest['studies']:
    doc = ROOT / s['path']
    text = doc.read_text()
    items = [r for r in rows if r['document'] == s['path']]
    assert len(items) == coverage['per_study'][s['id']]
    assert [r['source_item'] for r in items] == list(range(1, len(items)+1))
    assert len(re.findall(r'^\| \d+\.', text, re.M)) == len(items)
    assert all((ROOT / p).is_file() for p in s['evidence'])
    for r in items:
        assert re.fullmatch('[0-9a-f]{64}', r['source_paragraph_sha256'])
        assert r['recommendation'] in text and r['disposition'] in text
for p in [HERE/'README.md', *[ROOT/s['path'] for s in manifest['studies']]]:
    for dest in re.findall(r'\]\(([^)]+)\)', p.read_text()):
        if '://' in dest or dest.startswith('#'):
            continue
        assert (p.parent / dest.split('#')[0]).resolve().exists(), (p, dest)
        checked_links += 1
print(json.dumps({'ranked_items': len(rows), 'study_documents': len(manifest['studies']), 'local_links_checked': checked_links, 'status': 'pass'}))
