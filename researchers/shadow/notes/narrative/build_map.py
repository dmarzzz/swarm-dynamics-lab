#!/usr/bin/env python3
"""Pinned, zero-model-call narrative map. Editorial judgments are explicit, never inferred evidence."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.request import Request, urlopen
import yaml

HERE = Path(__file__).resolve().parent
BASE = 'https://github.com/dmarzzz/swarm-lab/blob/'
OWNERS = ('dmarz', 'vishesh', 'shadow')
AUDIT_ROOT = 'researchers/shadow/notes/completed-findings-xcheck/'


def clean(text):
    return str(text or '').replace('\u2014', ', ').replace('\u2013', '-').strip()


def owner_of(author, subject=''):
    if author.lower() in ('swarm-lab-bot', 'github-actions[bot]') or subject.startswith('[bot]'):
        return None, None
    prefix = re.match(r'\[([^\]]+)\]', subject)
    agent = prefix.group(1) if prefix else None
    if agent and agent.split('/')[0] in OWNERS:
        owner = agent.split('/')[0]
        return owner, agent if '/' in agent else owner + '/unprefixed'
    aliases = {'dmarzzz': 'dmarz', 'dmarz': 'dmarz', 'ultron': 'vishesh', 'cytonomy': 'vishesh',
               'codex': 'vishesh', 'wakesync': 'shadow', 'shad0w': 'shadow'}
    # Brackets like [docs] are a commit type, not a researcher/lane identity.
    return aliases.get(author.lower()), None


def stamp(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace('Z', '+00:00')).astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


class Snapshot:
    def __init__(self, repo, ref):
        self.repo = Path(repo)
        self.sha = self.git('rev-parse', ref).strip()
        self.paths = set(self.git('ls-tree', '-r', '--name-only', self.sha).splitlines())
        self.cache = {}
        self.used = {}

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.repo), *args], text=True)

    def text(self, path):
        if path not in self.paths:
            return ''
        if path not in self.cache:
            self.cache[path] = self.git('show', f'{self.sha}:{path}')
        text = self.cache[path]
        self.used[path] = hashlib.sha256(text.encode()).hexdigest()
        return text

    def data(self, path, default=None):
        text = self.text(path)
        return json.loads(text) if text else default

    def link(self, path):
        return BASE + self.sha + '/' + path


def frontmatter(text):
    if text.startswith('---\n'):
        return yaml.safe_load(text.split('---', 2)[1]) or {}
    return {}


def classify(text, themes):
    text = text.lower()
    hits = [(sum(key in text for key in theme['keywords']), theme['id']) for theme in themes]
    hits.sort(reverse=True)
    return [key for count, key in hits if count][:2] or ['metascience']


def excerpts(text, pattern, limit=3):
    # Do not publish unrelated operational, identity or network details.
    lines = []
    for line in text.splitlines():
        if re.search(pattern, line, re.I) and not re.search(r'key|token|secret|credential|ssh|\bIP\b|account|@', line, re.I):
            line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)
            line = clean(re.sub(r'^[#>*\s-]+', '', line))
            if line and len(line) < 900:
                lines.append(line[:550])
        if len(lines) == limit:
            break
    return lines


def fetch_hub(path, offline):
    url = 'https://swarm-live.pages.dev/api/state'
    try:
        if offline:
            return {'available': False, 'reason': 'Offline build; no live-status claim.', 'url': url}, {}
        with urlopen(Request(url, headers={'User-Agent': 'CommonThread/1.0 (public research map)', 'Accept': 'application/json'}), timeout=25) as response:
            raw = response.read(16_000_000)
        data = json.loads(raw)
        experiments = {}
        for exp in data.get('experiments', []):
            runs = exp.get('runs', [])
            counts = Counter(str(r.get('status', 'unknown')) for r in runs)
            experiments[str(exp['id'])] = {'id': str(exp['id']), 'run_status_counts': dict(counts),
                'active_runs': sum(r.get('status') in ('running', 'assigned') for r in runs),
                'stale_active_runs': sum(r.get('status') in ('running', 'assigned') and
                    float(data.get('now', 0)) - float(r.get('updated') or 0) > 600 for r in runs),
                'url': 'https://swarm-live.pages.dev/#/x/' + str(exp['id'])}
        # Persist only an allowlisted projection, never hosts, arbitrary events or run payloads.
        receipt = {'available': True, 'url': url, 'observed_at': datetime.now(timezone.utc).isoformat(),
            'sha256': hashlib.sha256(raw).hexdigest(), 'experiment_count': len(experiments),
            'note': 'Execution status only; done runs may be scripted, failed gates or diagnostics.'}
        if path:
            Path(path).write_text(json.dumps({'receipt': receipt, 'experiments': experiments}, indent=2) + '\n')
        return receipt, experiments
    except Exception as exc:
        return {'available': False, 'url': url, 'reason': type(exc).__name__ + ': public hub unavailable' + (' (HTTP ' + str(exc.code) + ')' if hasattr(exc, 'code') else '')}, {}


def scientific_status(row):
    status = row.get('status_at_assessment', '').lower()
    score = (row.get('evidence_confidence') or {}).get('score')
    if any(x in status for x in ('negative', 'failed', 'does_not', 'unqualified')):
        return 'negative'
    if 'running' in status:
        return 'running'
    if any(x in status for x in ('complete', 'analyz', 'pilot', 'finding', 'observed', 'qualified')) and score:
        return 'result'
    if score and 'script' in status:
        return 'result'
    if score:
        return 'result'
    return 'gated' if any(x in status for x in ('gate', 'block', 'qualification', 'fail')) else 'designing'


def activity_phase(subject):
    """Explicit commit cues only. Unknown activity is not silently relabeled as design."""
    subject = subject.lower()
    if re.search(r'\b(blocked|qualification failed|gate failed|gate failure|http429|http 429)\b', subject):
        return 'gated'
    if re.search(r'\b(task: done|closeout|close .+diagnostic|completed)\b', subject):
        return 'done'
    if re.search(r'\b(recomput|analy[sz]|audit|review)', subject):
        return 'analyzing'
    if re.search(r'\b(design|plan|preregistration|nothing launched|not launched|not started|unrun)\b', subject):
        return 'designing'
    if re.search(r'\b(qualification|probe|qualifying)\b', subject):
        return 'qualifying'
    if re.search(r'\b(running|launched|started|executing)\b', subject):
        return 'running (reported)'
    return 'phase unverified'


def score_headline(candidate, nodes, weights):
    evidence = [nodes[k] for k in candidate['evidence_ids'] if k in nodes]
    eligible = [n for n in evidence if n['strength'] > 0]
    # Per-owner balancing prevents one productive lane swamping everyone else.
    owner_scores = {owner: max((n['strength'] for n in eligible if n['owner'] == owner), default=0) for owner in OWNERS}
    present_scores = [s for s in owner_scores.values() if s]
    ev = sum(present_scores) / len(present_scores) if present_scores else 0
    coverage = len(present_scores) / len(OWNERS)
    availability = len(evidence) / len(candidate['evidence_ids'])
    components = {'evidence': ev, 'brief_fit': candidate['brief_fit'], 'coverage': coverage,
                  'readiness': candidate['readiness'] * availability}
    score = 100
    for key, value in components.items():
        score *= value ** weights[key]
    return dict(candidate, components=components, owner_strengths=owner_scores, score=round(score, 2),
                evidence_present=[n['id'] for n in evidence], missing_evidence=[k for k in candidate['evidence_ids'] if k not in nodes])


def build(args):
    snap = Snapshot(args.repo, args.ref)
    config = json.loads(Path(args.editorial).read_text())
    now = stamp(args.as_of) if args.as_of else datetime.now(timezone.utc)
    if not now:
        raise ValueError('Invalid --as-of timestamp')
    registry = snap.data('experiments/evidence-metadata.json', {'studies': []})
    snap.text('experiments/EVIDENCE.md')
    snap.text('experiments/EVIDENCE-METADATA.md')
    frozen_review_path = 'researchers/dmarz/notes/latest-results-review-2026-10-04/evidence.json'
    frozen_review = snap.data(frozen_review_path, {})
    review_rows = frozen_review.get('studies', [])
    featured = {f['id']: f for f in config['featured']}
    hub_receipt, hub = fetch_hub(args.hub_receipt, args.offline)
    nodes = {}
    for row in registry['studies']:
        docs = row.get('documents', [])
        path = next((p for p in docs if p in snap.paths), None)
        if not path:
            continue
        owner = path.split('/')[1] if path.startswith('researchers/') else 'vishesh'
        if owner not in OWNERS:
            continue
        rid = row['id']
        meta = row.get('evidence_confidence') or {}
        score = meta.get('score') or 0
        content = snap.text(path)
        # Read the sources, but never promote a status line into a scientific finding.
        citations = [p for p in row.get('sources', []) if p in snap.paths]
        for p in citations:
            if p.endswith('.md') and ('RESULT' in p.upper() or 'FINDING' in p.upper()):
                snap.text(p)
        status = scientific_status(row)
        text = ' '.join([rid, row.get('title', ''), meta.get('claim', '')])
        themes = featured.get(rid, {}).get('themes') or classify(text, config['themes'])
        observed_scripted = ('scripted' in row.get('status_at_assessment', '').lower() or
                            ('0 model calls' in row.get('sample_size_summary', '') and 'scripted' in text.lower()))
        kind = 'design' if not score else 'scripted' if observed_scripted else 'pilot' if score >= 2 else 'diagnostic / descriptive'
        strength = 0 if not score else .2 if observed_scripted else .55 if score >= 2 else .4
        edit = featured.get(rid, {})
        audit = AUDIT_ROOT + edit['audit'] if edit.get('audit') else None
        audit_available = bool(audit and audit in snap.paths)
        if edit.get('replicated') and score:
            kind, strength = 'cross-model replication', .70
        if audit_available:
            snap.text(audit)
            kind, strength = ('aggregate arithmetic checked', .65) if rid == 'sybil-scale-opus' else ('independently recomputed', .80)
        if edit.get('negative'):
            status = 'negative'
        claim = clean(meta.get('claim', 'Unassessed; see the source documentation.'))
        # This registry entry was initially unassessed. Use the explicitly scoped frozen review instead.
        if rid == 'capture-memory-mix' and not score:
            reviewed = next((r for r in review_rows if 'Capture and memory mix' in r['name']), None)
            if reviewed:
                claim = clean(reviewed['result'])
                score, strength, kind = 1, .4, 'diagnostic / descriptive'
                citations = [frozen_review_path] + citations
        nodes[rid] = {'id': rid, 'owner': owner, 'label': clean(edit.get('label', row.get('title', rid))),
            'title': clean(row.get('title', rid)), 'type': 'study', 'themes': themes, 'status': status,
            'claim': claim, 'sample': clean(row.get('sample_size_summary', 'Unassessed')),
            'limits': clean(meta.get('rationale', 'See source for scope and limitations.')),
            'evidence_score': score, 'strength': strength, 'strength_label': kind,
            'assessment_status': clean(row.get('status_at_assessment', 'unassessed')),
            'assessment_date': str(row.get('assessed_at', registry.get('assessed_at', 'unknown'))),
            'source': {'path': path, 'url': snap.link(path)},
            'support': [{'path': p, 'url': snap.link(p)} for p in citations[:6]],
            'audit': {'url': snap.link(audit), 'scope': edit['audit_scope']} if audit_available else None,
            'featured': rid in featured,
            'blockers': excerpts(re.sub(r'<!-- experiment-evidence:start -->.*?<!-- experiment-evidence:end -->', '', content, flags=re.S),
                                  r'\b(blocked|failed|unrun|not started|not run|awaiting|requires approval)\b', 2),
            'hub': next((hub[x] for x in row.get('experiment_ids', [rid]) if x in hub), None)}
    # Discover newly shipped corpus findings before registry convergence, without inventing numeric claims.
    for entry in config['featured']:
        rid = entry['id']
        if rid in nodes or not rid.startswith('wild-'):
            continue
        path = f'researchers/shadow/notes/{rid}/FINDING.md'
        if path not in snap.paths:
            continue
        content = snap.text(path)
        findings = excerpts(content, r'\d', 3)
        nodes[rid] = {'id': rid, 'owner': 'shadow', 'label': entry['label'], 'title': entry['label'],
            'type': 'study', 'themes': entry['themes'], 'status': 'result', 'claim': findings[0] if findings else 'Published descriptive archive analysis; registry assessment pending.',
            'sample': 'Registry assessment pending. See the linked finding for exact archive units.',
            'limits': 'Dependent observational archive census; no causal or generalization inference.',
            'evidence_score': None, 'strength': .4, 'strength_label': 'diagnostic / descriptive',
            'assessment_status': 'owner-published finding; registry pending', 'assessment_date': now.date().isoformat(),
            'source': {'path': path, 'url': snap.link(path)}, 'support': [], 'audit': None, 'featured': True, 'blockers': [], 'hub': hub.get(rid)}
    # Audits are nodes, not extra experiments or empirical observations.
    for rid, owner, label, path in [
        ('audit-xcheck', 'shadow', 'Independent endpoint replay', AUDIT_ROOT + 'README.md'),
        ('audit-dmarz', 'dmarz', 'Cross-researcher results review', frozen_review_path),
        ('audit-vishesh', 'vishesh', 'PI review and design transfers', 'researchers/vishesh/notes/pi-review-2026-10-04/SCIENTIFIC-REVIEW.md')]:
        if path in snap.paths:
            snap.text(path)
            nodes[rid] = {'id': rid, 'owner': owner, 'label': label, 'title': label, 'type': 'audit', 'themes': ['metascience'],
                'status': 'result', 'claim': 'Review artifact. Its presence is not a new experimental observation.',
                'sample': 'Not a scientific sample.', 'limits': 'Read the review for its exact source cutoff and coverage.',
                'evidence_score': None, 'strength': 0, 'strength_label': 'review artifact', 'source': {'path': path, 'url': snap.link(path)},
                'support': [], 'audit': None, 'featured': True, 'blockers': [], 'hub': None}
    tasks = []
    for path in sorted(snap.paths):
        if path.startswith('tasks/') and path.endswith('.md'):
            text = snap.text(path)
            m = frontmatter(text)
            owner = str(m.get('owner') or '').split('/')[0]
            if owner not in OWNERS or m.get('status') != 'claimed':
                continue
            updated = stamp(m.get('updated'))
            tasks.append({'id': m.get('id'), 'title': clean(m.get('title')), 'owner': owner,
                'agent': m.get('owner'), 'kind': m.get('kind'), 'status': m.get('status'), 'topics': m.get('topics', []),
                'updated': str(m.get('updated')), 'stale_claim': not updated or (now-updated).total_seconds() > 10800,
                'themes': classify(' '.join([str(m.get('id')), str(m.get('title')), ' '.join(m.get('topics', []))]), config['themes']),
                'blockers': excerpts(text, r'\b(blocked|awaiting|not run|not started)\b', 2), 'url': snap.link(path)})
    raw_log = snap.git('log', snap.sha, '--since=' + (now-timedelta(hours=24)).isoformat(),
                       '--format=%H%x1f%cI%x1f%an%x1f%s')
    commits, ignored, unmapped = [], 0, 0
    for line in raw_log.splitlines():
        parts = line.split('\x1f', 3)
        if len(parts) != 4:
            continue
        sha, timestamp, author, subject = parts
        t = stamp(timestamp)
        if not t or t > now:
            continue
        owner, agent = owner_of(author, subject)
        if not owner:
            ignored += 'bot' in author.lower() or subject.startswith('[bot]')
            unmapped += not ('bot' in author.lower() or subject.startswith('[bot]'))
            continue
        commits.append({'sha': sha, 'time': timestamp, 'owner': owner, 'agent': agent or owner + '/unprefixed',
                        'subject': clean(subject), 'url': 'https://github.com/dmarzzz/swarm-lab/commit/' + sha})
    threads = []
    by_agent = defaultdict(list)
    for c in commits:
        by_agent[c['agent']].append(c)
    for agent, records in by_agent.items():
        records.sort(key=lambda c: c['time'])
        last = stamp(records[-1]['time'])
        if (now-last).total_seconds() > 43200:
            continue
        owned = [t for t in tasks if t['agent'] == agent]
        relevant = ' '.join(c['subject'] for c in records[-8:])
        lane_theme = classify(relevant, config['themes'])
        status = activity_phase(records[-1]['subject'])
        # Commit language is activity, not a license to mark a scientific result complete.
        label = owned[0]['title'] if owned else agent.split('/', 1)[-1].replace('-', ' ')
        threads.append({'id': 'lane:' + agent, 'agent': agent, 'owner': records[0]['owner'], 'label': label,
            'themes': lane_theme, 'status': status, 'status_basis': 'Task and recent commit activity; not a scientific state or live-worker receipt.',
            'first': records[0]['time'], 'last': records[-1]['time'], 'commits_24h': len(records),
            'commits_12h': sum(stamp(r['time']) >= now-timedelta(hours=12) for r in records),
            'commits_3h': sum(stamp(r['time']) >= now-timedelta(hours=3) for r in records),
            'latest': records[-1], 'task_ids': [t['id'] for t in owned],
            'blockers': [b for t in owned for b in t['blockers']],
            'stale_claim': any(t['stale_claim'] for t in owned)})
    # Commit lanes are visible satellites, never extra findings or evidence-bearing samples.
    top_lanes = {owner: max((t for t in threads if t['owner'] == owner), key=lambda t: t['commits_3h'], default=None) for owner in OWNERS}
    for thread in threads:
        owner = thread['owner']
        task_path = 'tasks/' + thread['task_ids'][0] + '.md' if thread['task_ids'] else None
        agent_path = 'researchers/' + owner + '/agents/' + thread['agent'].split('/', 1)[-1] + '.md'
        path = task_path if task_path in snap.paths else agent_path if agent_path in snap.paths else 'researchers/' + owner + '/README.md'
        snap.text(path)
        nodes[thread['id']] = {'id': thread['id'], 'owner': owner, 'label': thread['label'], 'title': thread['agent'],
            'type': 'thread', 'themes': thread['themes'], 'status': thread['status'],
            'claim': 'Latest commit: ' + thread['latest']['subject'],
            'sample': str(thread['commits_3h']) + ' commits in 3h; ' + str(thread['commits_12h']) + ' in 12h. Activity is not a scientific sample.',
            'limits': thread['status_basis'], 'evidence_score': None, 'strength': 0, 'strength_label': 'activity only',
            'assessment_date': now.isoformat(), 'assessment_status': 'commit lane, not a study cohort',
            'source': {'path': path, 'url': snap.link(path)},
            'support': [{'path': 'Latest commit', 'url': thread['latest']['url']}], 'audit': None,
            'featured': top_lanes[owner] is thread and thread['commits_3h'] > 0,
            'blockers': thread['blockers'], 'hub': None}
    # Extra context is inventoried and hashed. Summaries below distinguish editorial synthesis from extracted facts.
    context_paths = sorted(p for p in snap.paths if (p.startswith(('surveys/', 'synthesis/')) and p.endswith('.md')) or
        p in ['researchers/shadow/notes/submission/WRITEUP.md', 'researchers/shadow/notes/submission/RESULTS.md',
              'researchers/dmarz/notes/overnight-program-2026-10-04/program.json',
              'researchers/vishesh/notes/pi-review-guide-2026-10-04/review-guide.json',
              'researchers/vishesh/notes/pi-review-2026-10-04/FINDINGS.md', 'HACKATHON.md'])
    for p in context_paths:
        snap.text(p)
    note_index = []
    for p in sorted(snap.paths):
        if re.match(r'researchers/(dmarz|vishesh|shadow)/notes/(?:[^/]+/){1,3}README.md$', p):
            txt = snap.text(p)
            note_index.append({'path': p, 'title': clean(next((x.lstrip('# ') for x in txt.splitlines() if x.startswith('# ')), p)),
                               'url': snap.link(p)})
    transfers = []
    for edge in config['transfers']:
        if edge['source'] in snap.paths and edge['from'] in nodes and edge['to'] in nodes:
            snap.text(edge['source'])
            transfers.append(dict(edge, url=snap.link(edge['source'])))
    paragraphs = {
        'dmarz': ('Identity, admission and incentives are the center of gravity: the Sybil scaling, fixed-resource splitting and market-rule cohorts supply the strongest controlled endpoints. The v5 program points toward a 180-controller economy plus trust, verification-cost and memory-handoff follow-ups. That program is a design, not evidence that 180 agents have completed a run. Cross-researcher reviews connect the controlled work to Vishesh\'s sensing tasks and Shadow\'s memory results.', ['researchers/dmarz/notes/sybil-split-opus/RESULTS.md', 'researchers/dmarz/notes/overnight-program-2026-10-04/program.json', frozen_review_path]),
        'vishesh': ('The work is converging on which evidence a group acquires, preserves and acts on: Phantom Coast, Quorum of Mirrors, dissent, selective checking and inheritance. Saved pilots expose useful failures, including repeated sensing and source dependence, but several broader swarm claims remain behind qualification or interface limits. PI reviews explicitly narrow next steps and transfer Dmarz\'s risk, cost and admission lessons instead of treating every larger run as progress.', ['researchers/vishesh/notes/phantom-coast/pc5/README.md', 'researchers/vishesh/notes/phantom-coast/pc5/DESIGN-TRANSFER.md', 'researchers/vishesh/notes/pi-review-2026-10-04/SCIENTIFIC-REVIEW.md']),
        'shadow': ('The emphasis is moving from memory-and-capture experiments and literature coverage to tools that question real archives and the lab itself. AskSwarm asks the same questions of three corpora; the identity and evidence-depth analyses expose missingness and inherited-text confounds. Independent replay checks Dmarz\'s saved endpoints. The memory-mixture negative result stays in the story as a model-dependence limit, not a universal rescue mechanism.', ['researchers/shadow/notes/wild-askswarm/FINDING.md', 'researchers/shadow/notes/wild-identity/FINDING.md', 'researchers/shadow/notes/wild-evidence-depth/FINDING.md', AUDIT_ROOT+'README.md', 'researchers/shadow/notes/capture-memory-mix/README.md'])}
    if 'researchers/dmarz/notes/sybil-rules-180/RESULTS.md' in snap.paths:
        paragraphs['dmarz'] = ('Identity and incentives now connect packet-level Sybil assays to a genuinely interacting 180-owner economy. In the original checkpoint-forked economy, sustained firm-level masking occurred for 55 of 180 owners without a prohibition sentence and zero with it; those 180 owners are dependent, not 180 experimental replications. The older splitting and verification cohorts have scoped external arithmetic checks. Follow-up records probe model/configuration transfer and memory-source adherence, while a failed qualification remains an instrument limit, not a replicated treatment effect.', ['researchers/dmarz/notes/sybil-rules-180/RESULTS.md', 'researchers/dmarz/notes/sybil-split-opus/RESULTS.md', 'researchers/dmarz/notes/memory-handoff-qwen/RESULTS.md', 'researchers/dmarz/notes/sybil-split-xmodel/RESULTS.md', frozen_review_path])
    village = 'researchers/vishesh/notes/ai-village-replay-2026-10-04/README.md'
    if village in snap.paths:
        village_text = snap.text(village)
        village_claim = (' A new AI Village preparation pipeline links real-trace material to seven study contracts. Its source still reports zero evaluated real episodes: this is a bridge toward less artificial tasks, not an in-the-wild efficacy result.' if re.search(r'zero real episodes|0 evaluated episodes', village_text, re.I) else ' The AI Village work now links real-trace material to the experimental program. Consult its current episode and evaluation status separately from the synthetic results.')
        paragraphs['vishesh'] = (paragraphs['vishesh'][0] + village_claim, paragraphs['vishesh'][1] + [village])
    researchers = []
    for owner in OWNERS:
        counts = {str(h): sum(c['owner'] == owner and stamp(c['time']) >= now-timedelta(hours=h) for c in commits) for h in (3, 12, 24)}
        checked = [n['id'] for n in nodes.values() if n['owner'] == owner and n['audit']]
        para, refs = paragraphs[owner]
        researchers.append({'id': owner, 'name': 'shadow / Sol' if owner == 'shadow' else owner,
            'commits': counts, 'commits_per_hour': {k: round(v/int(k), 2) for k,v in counts.items()},
            'checked_cohorts': checked, 'checked_note': 'Distinct displayed cohorts with scoped external arithmetic checks, not independently replicated hypotheses. Cutoff is each linked review.',
            'active_threads_3h': sum(t['owner'] == owner and t['commits_3h'] > 0 for t in threads),
            'active_threads_12h': sum(t['owner'] == owner for t in threads),
            'direction': para, 'direction_kind': 'Editorial synthesis of cited material; not a forecast or owner instruction.',
            'sources': [{'path': p, 'url': snap.link(p)} for p in refs if p in snap.paths]})
    headlines = sorted([score_headline(h, nodes, config['weights']) for h in config['headlines']], key=lambda h:h['score'], reverse=True)
    out = {'schema_version': 1, 'as_of': now.isoformat(), 'source_commit': snap.sha, 'source_ref': args.ref,
        'deadline': '2026-10-04T23:00:00+00:00', 'refresh_minutes': 45,
        'design_context': {'audience': 'The three researchers preparing one hackathon submission, and judges inspecting its evidence.',
            'use_case': 'Find a shared defensible headline, trace contributions, and choose remaining work.',
            'tone': 'Dark editorial research observatory, neutral, cited, precise. Doto display and Space Mono instrument labels.'},
        'method': {'activity': 'Non-bot commits by committer timestamp, last 24 hours; bracketed researcher/lane prefixes take precedence over author aliases. Merge commits count if attributed. Unmapped authors are excluded and counted.',
            'ignored_bot_commits': ignored, 'unmapped_commits': unmapped,
            'themes': 'Deterministic keyword matches, at most two per generic study/lane; featured overrides are explicit in editorial.json.',
            'evidence': 'Registry claims and independent-unit descriptions are preserved. New named archive FINDING.md files can appear before registry refresh. This page does not re-run experiments.',
            'score_formula': '100 × evidence^wE × brief_fit^wB × coverage^wC × readiness^wR. Evidence = mean of each represented owner\'s strongest selected artifact; coverage = represented owners / 3; readiness = editorial readiness × fraction of referenced artifacts present.',
            'strength_rubric': {'design / review artifact': 0, 'scripted': .2, 'diagnostic / descriptive': .4, 'pilot': .55, 'aggregate arithmetic checked': .65, 'cross-model replication': .7, 'independently recomputed': .8},
            'warning': 'Scores rank editorial packaging, not scientific truth, causal identification, award probability or launch approval. Diagnostics and negative findings count only within their narrow claims. No activity count enters the score.',
            'staleness': 'Git is one immutable source snapshot. Registry and reviews have their own assessment cutoffs and can lag newer closeouts. Hub execution is separately sampled and never upgrades scientific evidence.'},
        'weights': config['weights'], 'researchers': researchers, 'themes': config['themes'],
        'findings': list(nodes.values()), 'threads': threads, 'tasks': tasks, 'commits': commits,
        'transfers': transfers, 'headlines': headlines, 'hub': hub_receipt,
        'context': [{'path': p, 'url': snap.link(p)} for p in context_paths], 'note_index': note_index,
        'provenance': {'files': snap.used, 'editorial_sha256': hashlib.sha256(Path(args.editorial).read_bytes()).hexdigest(),
            'builder_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'model_calls': 0}}
    Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'source': snap.sha[:8], 'nodes': len(nodes), 'threads': len(threads), 'commits':len(commits),
                      'headlines': [(h['id'], h['score']) for h in headlines], 'output': str(args.output)}))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default=str(HERE.parents[3]))
    parser.add_argument('--ref', default='origin/main')
    parser.add_argument('--as-of', help='Reproduce activity cutoff (ISO UTC)')
    parser.add_argument('--editorial', default=str(HERE/'editorial.json'))
    parser.add_argument('--output', default=str(HERE/'narrative.json'))
    parser.add_argument('--hub-receipt', help='Save allowlisted hub projection, no private host/run fields')
    parser.add_argument('--offline', action='store_true')
    build(parser.parse_args())


if __name__ == '__main__':
    main()
