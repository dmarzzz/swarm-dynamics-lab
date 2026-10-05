#!/usr/bin/env python3
"""Regenerates scenes/roadmap.data.js (FILM.data.roadmap) from the repository. No network.

  python3 scenes/roadmap.build.py        (run from anywhere; paths are resolved from this file)

Sources
  5-experiments/studies/dmarz/question-atlas/candidates.json   the 219 candidates, their `area` (15) and `lane` (6)
  5-experiments/evidence-metadata.json                         registered cohorts: evidence score, claim, study folders
  study folders named by the registry                          atlas ids cited in README / experiment.yaml / design.yaml /
                                                               preregistration.md = "an experiment bears on this candidate"
Editorial inputs (the only hand-written part) are AREA_SHORT, SITE_TRACKS and RESULTS below. Each link in RESULTS says
whether the study itself cites the atlas id ("cited") or the link is by content or lineage ("content"); see `basis`.
"""
import collections, glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
ATLAS = '5-experiments/studies/dmarz/question-atlas/candidates.json'
REGISTRY = '5-experiments/evidence-metadata.json'

# Sector order, clockwise from the top, and the short label drawn on the ring (full names stay in the data).
# Large areas sit top and bottom, small ones on the sides, so that labels stack without overlapping.
AREA_SHORT = [
    ('llm-agent-swarms', 'LLM agent swarms'),
    ('meta', 'meta and tooling'),
    ('marl-emergence', 'multi-agent RL'),
    ('swarm-robotics', 'swarm robotics'),
    ('criticality-measurement', 'criticality'),
    ('collective-motion', 'collective motion'),
    ('sybil-resistance', 'sybil resistance'),
    ('agent-budgets', 'agent budgets'),
    ('fork-merge-security', 'fork-merge security'),
    ('collective-decision', 'decision-making'),
    ('active-matter', 'active matter'),
    ('sync-consensus', 'sync, consensus'),
    ('crowds-and-traffic', 'crowds, traffic'),
    ('swarm-intelligence', 'swarm intelligence'),
    ('swarm-detection', 'swarm detection'),
]

# The seven public research tracks on swarmsafety.org/research.html ("from questions to tracks", research.json `tracks`,
# read 2026-10-04). They group the lab's 34 projects, not the 219 candidates, so they are carried as names only.
SITE_TRACKS = [
    ('fake identities', 12), ('steering by evidence', 3), ('discussion and dissent', 4), ('when to check', 1),
    ('memory and recovery', 6), ('scale and safe action', 3), ('swarms in the wild', 5),
]

RESULTS = [
    {
        'n': 1, 'name': 'Thou shalt not split', 'study': '5-experiments/studies/dmarz/sybil-rules-180',
        'registry_id': 'sybil-rules-180', 'site_track': 'fake identities',
        # Lineage: sybil-rules-180/README.md:18 names the market-split studies as its predecessors;
        # market-split/README.md and market-split/experiment.yaml cite MKT-03 and MKT-11. The study folder cites no atlas id.
        'lights': [('MKT-11', 'content', 'sybils against a regulator'), ('MKT-03', 'content', 'one principal, several firms')],
        'sentence': 'Reproducible lab evidence that agents split an identity to slip a per-firm rule, and that one sentence stops it.',
        'open': 'one model, two economies',
        # reviews/chain-004-post.md "Not tested"; RESULTS.md:41 (R2 on gpt-6-luna did not run)
        'next': ['the same economy on a second model', 'the rule without the regulator hint'],
        'next_src': ['5-experiments/studies/dmarz/sybil-rules-180/reviews/chain-004-post.md',
                     '5-experiments/studies/dmarz/sybil-rules-180/RESULTS.md'],
    },
    {
        'n': 2, 'name': 'How to win agents and influence swarms', 'study': '5-experiments/studies/vishesh/external-influence-v2',
        'registry_id': 'influence-v2', 'site_track': 'steering by evidence',
        # By content only: the study folder cites no atlas id. SOC-37 = a bounded external document shifting a group's
        # decisions; SOC-29 = whether a check that comes back actually changes the response.
        'lights': [('SOC-37', 'content', 'influence through what agents read'), ('SOC-29', 'content', 'a report that leads to a response')],
        'sentence': 'Checking was not the weak point. The teams got true numbers back and did not use them.',
        'open': 'one fixture per domain',
        # reviews/quality-post.md failure and repair ledger: Q1 (enforced final rubric, live qualification pending),
        # Q3 (three-domain S0, odd and even tasks, doses 2 and 8, not collected)
        'next': ['a decision rule that must apply the check', 'more tasks per domain, two attack doses'],
        'next_src': ['5-experiments/studies/vishesh/external-influence-v2/reviews/quality-post.md',
                     '5-experiments/evidence-metadata.json'],
    },
    {
        'n': 3, 'name': 'Swarm of Theseus', 'study': '5-experiments/studies/vishesh/swarm-of-theseus',
        'registry_id': 'theseus-v1', 'site_track': 'memory and recovery',
        # SOC-24 is cited by the study (README.md:1, experiment.yaml:2). SOC-25 by content: README.md:40 predicts that an
        # old procedure may become harmful after the environment changes.
        'lights': [('SOC-24', 'cited', 'what survives full turnover'), ('SOC-25', 'content', 'retiring an obsolete convention')],
        'sentence': 'A written note carried the job through all 50 replacements. Dialogue added nothing.',
        'open': 'one synthetic world, one generation',
        # RESULTS.md "What this warrants next" (line 71)
        'next': ['more task worlds, tighter memory', 'agents that find the practice themselves'],
        'next_src': ['5-experiments/studies/vishesh/swarm-of-theseus/RESULTS.md'],
    },
]

ID = re.compile(r'\b([A-Z]{2,3}-\d{2})\b')
REG_FILES = ('README.md', 'experiment.yaml', 'design.yaml', 'preregistration.md')


def main():
    atlas = json.load(open(os.path.join(REPO, ATLAS)))
    cands = atlas['candidates']
    known = {c['id'] for c in cands}
    order = [a for a, _ in AREA_SHORT]
    assert sorted(order) == sorted({c['area'] for c in cands}), 'area list out of date'

    reg = json.load(open(os.path.join(REPO, REGISTRY)))
    by_reg = {s['id']: s for s in reg['studies']}
    folders = set()
    for s in reg['studies']:
        for d in s.get('documents', []) + s.get('registration_paths', []):
            m = re.match(r'(5-experiments/studies/[^/]+/[^/]+)/', d)
            if m:
                folders.add(m.group(1))
    cited = collections.defaultdict(set)
    for folder in sorted(folders):
        if '/question-atlas' in folder or '/atlas-review' in folder:
            continue
        for name in REG_FILES:
            for path in glob.glob(os.path.join(REPO, folder, name)):
                for cid in set(ID.findall(open(path, errors='replace').read())):
                    if cid in known:
                        cited[cid].add(folder.split('studies/')[1])
    film = {l[0] for r in RESULTS for l in r['lights']}
    assert film <= known

    areas = []
    for a, short in AREA_SHORT:
        mine = [c for c in cands if c['area'] == a]
        areas.append({'id': a, 'label': short, 'name': atlas['topics'][a], 'n': len(mine),
                      'covered': sum(1 for c in mine if c['id'] in cited or c['id'] in film)})
    title = {c['id']: c['title'] for c in cands}
    area_of = {c['id']: c['area'] for c in cands}
    results = []
    for r in RESULTS:
        ev = by_reg[r['registry_id']]['evidence_confidence']
        results.append({
            'n': r['n'], 'name': r['name'], 'study': r['study'], 'siteTrack': r['site_track'],
            'evidence': ev['score'], 'evidenceOf': 4, 'claim': ev['claim'],
            'lights': [{'id': cid, 'title': title[cid], 'short': short, 'area': area_of[cid], 'basis': basis} for cid, basis, short in r['lights']],
            'areas': sorted({area_of[l[0]] for l in r['lights']}, key=order.index),
            'sentence': r['sentence'], 'open': r['open'], 'next': r['next'], 'nextSrc': r['next_src'],
        })
    out = {
        'built_from': [ATLAS, REGISTRY],
        'atlas_version': atlas.get('version'), 'atlas_date': atlas.get('date'), 'atlas_status': atlas.get('status'),
        'total': len(cands),
        'coveredCited': len(cited), 'coveredAny': len(set(cited) | film),
        'areas': areas,
        'lanes': dict(collections.Counter(c['lane'] for c in cands)),
        'siteTracks': [{'name': n, 'projects': k} for n, k in SITE_TRACKS],
        # one row per candidate: [id, area index (into areas), 1 if a registered study's own files cite it]
        'candidates': [[c['id'], order.index(c['area']), 1 if c['id'] in cited else 0] for c in cands],
        'citedBy': {k: sorted(v) for k, v in sorted(cited.items())},
        'results': results,
    }
    js = ('// Generated by scenes/roadmap.build.py from ' + ATLAS + ' and ' + REGISTRY + '. Do not edit by hand.\n'
          'FILM.data = FILM.data || {};\nFILM.data.roadmap = ' + json.dumps(out, separators=(',', ':'), ensure_ascii=False) + ';\n')
    dest = os.path.join(HERE, 'roadmap.data.js')
    open(dest, 'w').write(js)
    print('wrote', dest, len(js), 'bytes')
    print('candidates', len(cands), '| cited by a registered study', len(cited), '| plus film links', len(set(cited) | film))
    for a in areas:
        print('  %-26s %3d  covered %d' % (a['label'], a['n'], a['covered']))


if __name__ == '__main__':
    main()
