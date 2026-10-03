"""Validate and render the human-requested, unreviewed research candidate bank.

Run from any directory. No network calls, experiments, or review-state writes.
"""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import re
import yaml

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--canvas', type=Path, help='Optional managed canvas projection path')
args = parser.parse_args()
OUT = ROOT / 'researchers/dmarz/notes/question-atlas'
TOPICS = yaml.safe_load((ROOT / 'library/topics.yaml').read_text())
AREAS = {t['slug']: t['name'] for t in TOPICS}
FIELDS = ['id', 'area', 'title', 'question', 'hypothesis', 'test', 'baseline', 'metrics',
          'falsifier', 'confounds', 'prior', 'novelty', 'feasibility', 'needs', 'briefs']
NOVELTY = {'replication', 'boundary-test', 'extension', 'measurement', 'speculative'}
FEASIBILITY = {'offline', 'api-small', 'training', 'hardware', 'access-dependent'}
REVISION = json.loads((OUT / 'revision.json').read_text())
BASELINE = REVISION['baseline_candidate_sha256']
records = {}
for p in (ROOT / 'library').glob('*/*.md'):
    text = p.read_text()
    if text.startswith('---'):
        fm = yaml.safe_load(text.split('---', 2)[1])
        if fm and fm.get('id'):
            records[fm['id']] = (p, fm)

candidates = []
for lane in ['physical', 'society', 'security', 'methods', 'budgets']:
    rows = json.loads((OUT / f'{lane}.json').read_text())
    for row in rows:
        assert all(k in row for k in FIELDS), (lane, row.get('id'), 'missing fields')
        assert all(row[k] for k in FIELDS if k != 'briefs'), row['id']
        assert row['area'] in AREAS, (row['id'], 'area')
        assert row['novelty'] in NOVELTY, (row['id'], 'novelty')
        assert row['feasibility'] in FEASIBILITY, (row['id'], 'feasibility')
        assert len(row['prior']) >= 2 and len(row['metrics']) >= 2, row['id']
        # Hash editable content before enriching sources with catalogue metadata.
        row['candidate_sha256'] = hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest()
        row['change'] = ('new' if row['id'] not in BASELINE else
                         'unchanged' if BASELINE[row['id']] == row['candidate_sha256'] else 'revised')
        row['lane'] = lane
        row['status'] = 'unreviewed-hunch'
        for source in row['prior']:
            assert source['id'] in records, (row['id'], 'missing source', source['id'])
            assert source['relation'].strip(), row['id']
            p, fm = records[source['id']]
            source.update(title=fm.get('title', source['id']),
                          path=p.relative_to(ROOT).as_posix(),
                          url=fm.get('url', ''),
                          catalogued_depth=fm.get('read_depth', 'unspecified'))
        for brief in row['briefs']:
            assert (ROOT / brief).is_file(), (row['id'], 'missing brief', brief)
        candidates.append(row)

assert len({r['id'] for r in candidates}) == len(candidates), 'duplicate ids'
assert set(BASELINE) <= {r['id'] for r in candidates}, 'existing candidate IDs must be preserved'
assert len({r['question'].strip().lower() for r in candidates}) == len(candidates), 'duplicate questions'
assert set(r['area'] for r in candidates) == set(AREAS), 'missing research area'
briefs = sorted((ROOT / 'researchers/vishesh/notes/project-briefs').glob('*.md'))
for brief in briefs:
    if brief.name == 'README.md':
        continue
    rel = brief.relative_to(ROOT).as_posix()
    assert any(rel in r['briefs'] for r in candidates), ('unmapped project brief', rel)

digest = hashlib.sha256(json.dumps(candidates, sort_keys=True).encode()).hexdigest()
changes = {kind: [r['id'] for r in candidates if r['change'] == kind]
           for kind in ['new', 'revised', 'unchanged']}
payload = dict(version=REVISION['version'], date=REVISION['date'], status='Human-requested unreviewed hunches',
               source_snapshot=REVISION['source_snapshot'], previous_atlas_commit=REVISION['previous_atlas_commit'],
               changes=changes, content_sha256=digest, topics=AREAS,
               candidates=candidates)
(OUT / 'candidates.json').write_text(json.dumps(payload, indent=2, ensure_ascii=False)+'\n')

def link(path):
    return 'https://github.com/dmarzzz/swarm-lab/blob/main/' + path

counts = collections.Counter(r['area'] for r in candidates)
lines = ['# Research question atlas', '',
         f'{len(candidates)} candidate questions, tentative hypotheses and test sketches across all {len(AREAS)} research areas.', '',
         'Owner: dmarz/question-atlas. Human-requested brainstorming, 2026-10-03. **Every item is an unreviewed hunch.** These are selection materials, not accepted hypotheses, approved protocols, measured effects, or novelty claims.', '',
         '[Start with the synthesis and review guide](../../../../synthesis/research-question-atlas.md). '
         '[Open the local review browser](review.html). [Machine-readable bank](candidates.json). '
         '[Review scope and limitations](scope.md).', '',
         f'Update {REVISION["version"]}: **{len(changes["new"])} new, {len(changes["revised"])} revised, '
         f'{len(changes["unchanged"])} unchanged** candidates. All original IDs are retained. '
         '[What changed and why](update-v2.md).', '',
         'Feasibility labels describe a possible first test, not a verified installation, price or runtime. Source depths are inherited catalogue metadata, not claims that this pass fully read those sources. The open evidence-depth audit still applies.', '',
         '## Areas', '']
for area, name in AREAS.items():
    lines.append(f'- [{name}](#{area}): {counts[area]} candidates.')
lines += ['', '## Shared design requirements', '',
          'For any selected candidate: define the independent assignment unit, interference boundary, primary outcome, smallest effect worth pursuing, and an uncertainty-aware decision rule before a confirmatory run. An estimate near zero with a wide interval is inconclusive. Set seed/case counts from a pilot and the intended precision, then freeze the comparison. Log unsuccessful runs and all tuning costs. Use held-out worlds, operators or model families only when the labels really support that split.', '',
          'API tests need matched inference and communication budgets. Training tests need matched steps, capacity and tuning effort. Simulators need explicit scheduling, observation and boundary rules. Security tests use synthetic or authorized environments. Oracle information is a diagnostic ceiling only. Replication, measurement and boundary tests can be valuable without claiming a new mechanism.', '']
for area, name in AREAS.items():
    lines += [f'<a id="{area}"></a>', f'## {name}', '']
    for r in [x for x in candidates if x['area'] == area]:
        lines += [f'<a id="{r["id"].lower()}"></a>', f'### {r["id"]} — {r["title"]}', '',
                  f'**Update {REVISION["version"]}:** {r["change"]}.', '',
                  f'**Question:** {r["question"]}', '', f'**Candidate hypothesis:** {r["hypothesis"]}', '',
                  f'**How to test:** {r["test"]}', '', f'**Comparison:** {r["baseline"]}', '',
                  '**Measurements:** '+ '; '.join(r['metrics'])+'.', '',
                  f'**Would count against it:** {r["falsifier"]}', '',
                  f'**Main confounds:** {r["confounds"]}', '',
                  f'**Framing / first-test class:** {r["novelty"]} / {r["feasibility"]}.', '',
                  f'**Before promotion:** {r["needs"]}', '', '**Closest prior and evidence limits:**', '']
        for s in r['prior']:
            lines.append(f'- [[{s["id"]}]] — [{s["title"]}]({link(s["path"])}). {s["relation"]} Catalogue depth: {s["catalogued_depth"]}.')
        if r['briefs']:
            lines += ['', '**Related team work:** '+ ', '.join(f'[{Path(b).stem}]({link(b)})' for b in r['briefs'])+'.']
        lines += ['']
lines += ['## Original brief coverage', '']
for brief in briefs:
    if brief.name == 'README.md': continue
    rel = brief.relative_to(ROOT).as_posix()
    ids = [f'[{r["id"]}](#{r["id"].lower()})' for r in candidates if rel in r['briefs']]
    lines.append(f'- [{brief.stem}]({link(rel)}): '+', '.join(ids))
(OUT / 'README.md').write_text('\n'.join(lines)+'\n')
embedded = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c')
template = (ROOT / 'src/question-atlas/review-template.html').read_text()
(OUT / 'review.html').write_text(template.replace('__ATLAS_DATA__', embedded))
canvas = (ROOT / 'src/question-atlas/canvas-template.txt').read_text()
if args.canvas:
    args.canvas.write_text(canvas.replace('__ATLAS_DATA__', embedded))
print(json.dumps(dict(candidates=len(candidates), topics=len(counts),
                      changes={k: len(v) for k, v in changes.items()},
                      unique_sources=len({s['id'] for r in candidates for s in r['prior']}),
                      briefs=len(briefs)-1, counts=dict(counts)), indent=2))
