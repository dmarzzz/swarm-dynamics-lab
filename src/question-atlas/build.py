"""Validate and render the human-requested, unreviewed research candidate bank.

Run from any directory. No network calls, experiments, or review-state writes.

The atlas inputs (lane files, revision.json, research-delta-v2.json) were written before the repo moved to the
research-phase layout and are frozen: per-candidate and whole-bank hashes are computed over them, and review
exports quote the bank hash. They name repo files by their pre-move paths (`researchers/<name>/notes/...`,
`synthesis/...`, `library/...`). The data written here keeps that vocabulary so the hashes stay reproducible;
`current_path` resolves a pre-move path to where the file lives now whenever a file is read or a link is emitted.

By default the outputs are written into the study folder beside the inputs. `--out DIR` writes them elsewhere
(for a dry run) and leaves the study folder untouched.
"""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import re
import yaml

REPO_URL = 'https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/'
LIBRARY = '1-library'
STUDIES = '5-experiments/studies'
# Pre-move path -> current path. Same table as dashboard/scripts/layout.py; the layout itself is defined in
# scripts/lab.py. Duplicated so that src/ stays self-contained.
PREFIXES = (('library/', '1-library/'), ('surveys/', '2-surveys/'), ('reviews/', '2-surveys/reviews/'),
            ('synthesis/', '3-synthesis/'), ('hypotheses/', '4-hypotheses/'), ('experiments/', '5-experiments/'),
            ('tooling/', '5-experiments/toolkit/'), ('tasks/', 'lab/tasks/'), ('candidates/', 'lab/candidates/'),
            ('templates/', 'lab/templates/'))
EXACT = {'STATUS.md': 'lab/STATUS.md', 'PIPELINE.md': 'lab/PIPELINE.md'}
STUDY = r'^researchers/([^/]+)/(?:notes/|(?=(?:factory|qa)/))'


def current_path(path):
    """Pre-move repo path -> current path. A path already in the current layout is returned unchanged."""
    if path in EXACT:
        return EXACT[path]
    match = re.match(STUDY, path)
    if match:
        return f'{STUDIES}/{match.group(1)}/' + path[match.end():]
    if path.startswith('researchers/'):
        return 'lab/' + path
    for old, new in PREFIXES:
        if path.startswith(old):
            return new + path[len(old):]
    return path


def frozen_path(path):
    """Current path of a library entry -> the pre-move spelling the frozen atlas data uses."""
    assert path.startswith(LIBRARY + '/'), path
    return 'library/' + path[len(LIBRARY) + 1:]


ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--canvas', type=Path, help='Optional managed canvas projection path')
parser.add_argument('--out', type=Path, help='Write candidates.json, research-delta-v2.json, README.md and '
                    'review.html to this folder instead of the study folder')
args = parser.parse_args()
SRC = ROOT / STUDIES / 'dmarz/question-atlas'
OUT = args.out or SRC
OUT.mkdir(parents=True, exist_ok=True)
TOPICS = yaml.safe_load((ROOT / LIBRARY / 'topics.yaml').read_text())
AREAS = {t['slug']: t['name'] for t in TOPICS}
FIELDS = ['id', 'area', 'title', 'question', 'hypothesis', 'test', 'baseline', 'metrics',
          'falsifier', 'confounds', 'prior', 'novelty', 'feasibility', 'needs', 'briefs']
NOVELTY = {'replication', 'boundary-test', 'extension', 'measurement', 'speculative'}
FEASIBILITY = {'offline', 'api-small', 'training', 'hardware', 'access-dependent'}
REVISION = json.loads((SRC / 'revision.json').read_text())
BASELINE = REVISION['baseline_candidate_sha256']
records = {}
for p in (ROOT / LIBRARY).glob('*/*.md'):
    text = p.read_text()
    if text.startswith('---'):
        fm = yaml.safe_load(text.split('---', 2)[1])
        if fm and fm.get('id'):
            records[fm['id']] = (p, fm)

candidates = []
for lane in ['physical', 'society', 'security', 'methods', 'budgets', 'markets']:
    rows = json.loads((SRC / f'{lane}.json').read_text())
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
                          path=frozen_path(p.relative_to(ROOT).as_posix()),
                          url=fm.get('url', ''),
                          catalogued_depth=fm.get('read_depth', 'unspecified'))
        for brief in row['briefs']:
            assert (ROOT / current_path(brief)).is_file(), (row['id'], 'missing brief', brief)
        candidates.append(row)

assert len({r['id'] for r in candidates}) == len(candidates), 'duplicate ids'
assert set(BASELINE) <= {r['id'] for r in candidates}, 'existing candidate IDs must be preserved'
assert len({r['question'].strip().lower() for r in candidates}) == len(candidates), 'duplicate questions'
assert set(r['area'] for r in candidates) == set(AREAS), 'missing research area'
briefs = sorted((ROOT / STUDIES / 'vishesh/project-briefs').glob('*.md'))
mapped = {r['id']: {current_path(b) for b in r['briefs']} for r in candidates}
for brief in briefs:
    if brief.name == 'README.md':
        continue
    rel = brief.relative_to(ROOT).as_posix()
    assert any(rel in mapped[r['id']] for r in candidates), ('unmapped project brief', rel)

digest = hashlib.sha256(json.dumps(candidates, sort_keys=True).encode()).hexdigest()
changes = {kind: [r['id'] for r in candidates if r['change'] == kind]
           for kind in ['new', 'revised', 'unchanged']}
payload = dict(version=REVISION['version'], date=REVISION['date'], status='Human-requested unreviewed hunches',
               source_snapshot=REVISION['source_snapshot'], previous_atlas_commit=REVISION['previous_atlas_commit'],
               changes=changes, content_sha256=digest, topics=AREAS,
               candidates=candidates)
(OUT / 'candidates.json').write_text(json.dumps(payload, indent=2, ensure_ascii=False)+'\n')
delta = json.loads((SRC / 'research-delta-v2.json').read_text())
for record in delta['records']:
    record['cited_by'] = [r['id'] for r in candidates
                          if any(s['id'] == record['id'] for s in r['prior'])]
(OUT / 'research-delta-v2.json').write_text(json.dumps(delta, indent=2, ensure_ascii=False)+'\n')

def link(path):
    return REPO_URL + current_path(path)

counts = collections.Counter(r['area'] for r in candidates)
lines = ['# Research question atlas', '',
         f'{len(candidates)} candidate questions, tentative hypotheses and test sketches across all {len(AREAS)} research areas.', '',
         'Owner: dmarz/question-atlas. Human-requested brainstorming, 2026-10-03. **Every item is an unreviewed hunch.** These are selection materials, not accepted hypotheses, approved protocols, measured effects, or novelty claims.', '',
         '[Start with the synthesis and review guide](../../../../3-synthesis/research-question-atlas.md). '
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
    ids = [f'[{r["id"]}](#{r["id"].lower()})' for r in candidates if rel in mapped[r['id']]]
    lines.append(f'- [{brief.stem}]({link(rel)}): '+', '.join(ids))
(OUT / 'README.md').write_text('\n'.join(lines)+'\n')
embedded = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c')
# The templates build their links in the browser from the frozen paths, so they get the same table.
layout = json.dumps(dict(repo=REPO_URL, studies=STUDIES, prefixes=PREFIXES, exact=EXACT, study=STUDY))
HERE = Path(__file__).resolve().parent
template = (HERE / 'review-template.html').read_text()
(OUT / 'review.html').write_text(template.replace('__LAYOUT_MAP__', layout).replace('__ATLAS_DATA__', embedded))
canvas = (HERE / 'canvas-template.txt').read_text()
if args.canvas:
    args.canvas.write_text(canvas.replace('__LAYOUT_MAP__', layout).replace('__ATLAS_DATA__', embedded))
print(json.dumps(dict(candidates=len(candidates), topics=len(counts),
                      changes={k: len(v) for k, v in changes.items()},
                      unique_sources=len({s['id'] for r in candidates for s in r['prior']}),
                      briefs=len(briefs)-1, counts=dict(counts)), indent=2))
