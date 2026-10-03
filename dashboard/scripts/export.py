#!/usr/bin/env python3
"""Export Swarm Lab's static dashboard contract. Requires only Python and PyYAML.

One git history scan supplies first-add provenance and the chronological river.
No per-document git subprocesses. GH batch enrichment is optional and bounded.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import time
from collections import Counter
from research_navigation import build_navigation

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import lab as helpers

KINDS = helpers.LIB_DIRS
OUT = ROOT / 'dashboard/public/data'
ATLAS = ROOT / 'researchers/dmarz/notes/question-atlas/candidates.json'
QUESTION_FIELDS = ('id', 'area', 'title', 'question', 'hypothesis', 'test', 'baseline',
                   'metrics', 'falsifier', 'confounds', 'prior', 'novelty', 'feasibility',
                   'needs', 'briefs')
QUESTION_NOVELTY = {'replication', 'boundary-test', 'extension', 'measurement', 'speculative'}
QUESTION_FEASIBILITY = {'offline', 'api-small', 'training', 'hardware', 'access-dependent'}
QUESTION_CHANGES = {'new', 'revised', 'unchanged'}

def atlas_hash(value):
    """Match src/question-atlas/build.py, including its default ASCII serialization."""
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()

def validate_questions(payload, library_paths, topic_slugs, root=ROOT):
    """Validate the atlas without rewriting content, source metadata or review hashes."""
    def require(condition, message):
        if not condition:
            raise ValueError(f'questions.json: {message}')

    def string(value):
        return isinstance(value, str) and bool(value.strip())

    def repo_file(value):
        if not string(value) or '\\' in value:
            return False
        path = PurePosixPath(value)
        return (not path.is_absolute() and '..' not in path.parts
                and path.as_posix() == value
                and (root / value).resolve().is_relative_to(root.resolve())
                and (root / value).is_file())

    required = {'version', 'date', 'status', 'source_snapshot', 'previous_atlas_commit',
                'changes', 'content_sha256', 'topics', 'candidates'}
    require(isinstance(payload, dict) and required <= payload.keys(), 'missing atlas fields')
    require(type(payload['version']) is int and payload['version'] > 0, 'invalid version')
    require(payload['status'] == 'Human-requested unreviewed hunches', 'invalid atlas status')
    for field in ('date', 'source_snapshot', 'previous_atlas_commit', 'content_sha256'):
        require(string(payload[field]), f'invalid {field}')
    topics = payload['topics']
    require(isinstance(topics, dict) and bool(topics), 'invalid topics')
    require(set(topics) <= set(topic_slugs) and all(string(v) for v in topics.values()),
            'unknown topic or missing topic name')
    rows = payload['candidates']
    require(isinstance(rows, list) and bool(rows), 'candidates must be a nonempty array')
    ids = set()
    changes = {kind: [] for kind in ('new', 'revised', 'unchanged')}
    for row in rows:
        require(isinstance(row, dict) and set(QUESTION_FIELDS) <= row.keys(),
                'candidate missing required fields')
        ident = row['id']
        require(string(ident) and re.fullmatch(r'[A-Z]+-\d+', ident) is not None,
                'invalid candidate id')
        require(ident not in ids, f'duplicate candidate id {ident}')
        ids.add(ident)
        for field in set(QUESTION_FIELDS) - {'metrics', 'prior', 'briefs'}:
            require(string(row[field]), f'{ident}: invalid {field}')
        require(row['area'] in topics, f'{ident}: unknown area')
        require(row.get('status') == 'unreviewed-hunch',
                f'{ident}: invalid candidate status')
        require(row['novelty'] in QUESTION_NOVELTY, f'{ident}: invalid novelty')
        require(row['feasibility'] in QUESTION_FEASIBILITY, f'{ident}: invalid feasibility')
        require(string(row.get('change')) and row['change'] in QUESTION_CHANGES,
                f'{ident}: invalid change')
        require(string(row.get('lane')), f'{ident}: missing lane')
        require(isinstance(row['metrics'], list) and len(row['metrics']) >= 2
                and all(string(x) for x in row['metrics']), f'{ident}: invalid metrics')
        require(isinstance(row['prior'], list) and len(row['prior']) >= 2,
                f'{ident}: invalid prior')
        for source in row['prior']:
            require(isinstance(source, dict)
                    and {'id', 'relation', 'title', 'path', 'url', 'catalogued_depth'} <= source.keys(),
                    f'{ident}: missing source fields')
            require(all(string(source[field]) for field in ('id', 'relation', 'title', 'path', 'catalogued_depth'))
                    and isinstance(source['url'], str), f'{ident}: invalid source fields')
            require(source['id'] in library_paths, f'{ident}: unknown source {source["id"]}')
            require(source['path'] == library_paths[source['id']] and repo_file(source['path']),
                    f'{ident}: source path does not match {source["id"]}')
        require(isinstance(row['briefs'], list) and all(repo_file(x) for x in row['briefs']),
                f'{ident}: unknown or invalid brief path')
        # Hash only the editable card and prior relationships, before atlas enrichment.
        editable = {field: row[field] for field in QUESTION_FIELDS}
        editable['prior'] = [{'id': source['id'], 'relation': source['relation']}
                             for source in row['prior']]
        require(row.get('candidate_sha256') == atlas_hash(editable),
                f'{ident}: candidate hash mismatch; rebuild the canonical atlas')
        changes[row['change']].append(ident)
    require(set(row['area'] for row in rows) == set(topics), 'topics and represented areas differ')
    require(payload['changes'] == changes, 'change index does not match candidates')
    require(payload['content_sha256'] == atlas_hash(rows),
            'content hash mismatch; rebuild the canonical atlas')

def questions_payload(data):
    payload = json.loads(ATLAS.read_text(encoding='utf-8'))
    validate_questions(payload, {ident: doc.rel for ident, doc in data.library.items()}, data.topics)
    return payload

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, timeout=20)

def agent_from(message):
    match = re.search(r'\[([^\]\s]+/[^\]\s]+)\]', message)
    if not match:
        match = re.search(r'\bagent[:= ]+([\w.-]+/[\w.-]+)', message)
    return match.group(1) if match else 'unknown/unknown'

def history():
    first, additions = {}, []
    # Reverse history means the first observed A record really is the first addition.
    raw = git('log', '--reverse', '--diff-filter=AR', '--name-status',
              '--format=@@%H\t%aI\t%s', '--', 'library/')
    current = None
    for line in raw.splitlines():
        if line.startswith('@@'):
            sha, stamp, message = line[2:].split('\t', 2)
            current = {'sha': sha, 't': stamp, 'agent': agent_from(message)}
            continue
        if current and line.startswith('R'):
            # Renamed entry keeps its original addition stamp and agent.
            _, old, new = line.split('\t', 2)
            if new.endswith('.md'):
                first.setdefault(new, dict(first.get(old, current)))
            continue
        if current and line.startswith('A\t'):
            path = line[2:]
            parts = Path(path).parts
            if len(parts) != 3 or parts[1] not in KINDS or not path.endswith('.md') or parts[2] in {'README.md','INDEX.md'}:
                continue
            first.setdefault(path, dict(current))
            additions.append({**current, 'path': path, 'kind': KINDS[parts[1]]})
    return first, additions

def short_authors(value):
    if isinstance(value, list):
        return ', '.join(str(x) for x in value[:3]) + (' et al.' if len(value) > 3 else '')
    return str(value or '')

def counts(entries):
    c = Counter(e['kind'] for e in entries)
    return {**{folder: c[kind] for folder, kind in KINDS.items()}, 'total': len(entries)}

def docs_payload(docs):
    return [{'id': ident, **doc.fm} for ident, doc in docs.items()]

POST_HEAD = re.compile(r'^\*\*(\d+)\. @(\S+?), (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) UTC(?:, (\d+) likes)?\*\*', re.M)
METRIC = {'likes': r'(\d+) likes?', 'reposts': r'(\d+) reposts?', 'replies': r'(\d+) repl(?:y|ies)', 'views': r'(\d+) views'}

def metric(text, key):
    match = re.search(METRIC[key], text or '')
    return int(match.group(1)) if match else None

def thread_payload(ident, doc):
    """X thread extras: handle, root post date, engagement, post count and the opening line."""
    fm = doc.fm
    body = doc.sections().get('Archived text', '')
    heads = POST_HEAD.findall(body)
    handle = str(fm.get('author_handle') or (f'@{heads[0][1]}' if heads else '')).strip()
    date = heads[0][2] if heads else None
    if not date:
        stamp = re.search(r'(\d{4}-\d{2}-\d{2})T\d{2}:\d{2}', body)
        date = stamp.group(1) if stamp else None
    first = ''
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith(('**', '---', 'Verbatim text', 'Quoted tweet', '>', '#')):
            continue
        first = s
        break
    metrics = fm.get('metrics') or ''
    likes = metric(metrics, 'likes')
    if likes is None and heads and heads[0][4]:
        likes = int(heads[0][4])
    clean = lambda s: str(s).encode('utf-8', 'ignore').decode('utf-8')  # drop lone surrogates from scraped text
    return {'id': ident, 'handle': clean(handle), 'name': clean(fm.get('author_name') or ''), 'date': date,
            'likes': likes, 'reposts': metric(metrics, 'reposts'), 'replies': metric(metrics, 'replies'),
            'views': metric(metrics, 'views'), 'posts': max(1, len(heads)), 'first_line': clean(first[:160])}

def batch_payload():
    mapped = {}
    mapping = ROOT / 'candidates/ISSUES.tsv'
    if mapping.exists():
        for line in mapping.read_text().splitlines():
            if not line.strip() or line.startswith('#'):
                continue
            bid, number, url = line.split('\t')
            mapped[bid] = {'number': int(number), 'url': url}
    result = []
    for path in sorted((ROOT / 'candidates').glob('*/*.jsonl')):
        rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        row = rows[0] if rows else {}
        result.append({'id': path.stem, 'source': path.parent.name,
                       'topic': row.get('topic'), 'n_candidates': len(rows),
                       'state': 'unknown' if path.stem in mapped else 'free',
                       'assignees': [], 'updated': None, **mapped.get(path.stem, {})})
    if os.environ.get('GH_TOKEN'):
        try:
            command = ['gh', 'issue', 'list', '-R', 'dmarzzz/swarm-lab', '-l', 'batch',
                       '--state', 'all', '--limit', '1000', '--json',
                       'number,title,state,labels,assignees,updatedAt,url,body']
            p = subprocess.run(command, text=True, capture_output=True, timeout=15, check=True)
            issues = {i['number']: i for i in json.loads(p.stdout)}
            for batch in result:
                issue = issues.get(batch.get('number'))
                if not issue:
                    continue
                labels = [x['name'] for x in issue['labels']]
                batch.update(state='closed' if issue['state'] == 'CLOSED' else 'claimed' if 'claimed' in labels else 'free',
                             labels=labels, assignees=[x['login'] for x in issue['assignees']],
                             updated=issue['updatedAt'], title=issue['title'], url=issue['url'])
        except (OSError, subprocess.SubprocessError, ValueError) as exc:
            print(f'Batch API enrichment unavailable: {exc}', file=sys.stderr)
    return result

def export():
    started = time.monotonic()
    data = helpers.Lab()
    questions = questions_payload(data)
    provenance, additions = history()
    entries = []
    timeline_counts = Counter()
    agent_counts = Counter()
    agent_last = {}
    for ident, doc in sorted(data.library.items()):
        fm = doc.fm
        origin = provenance.get(doc.rel, {})
        agent = fm.get('added_by') or origin.get('agent', 'unknown/unknown')
        stamp = origin.get('t')
        kind = fm.get('type') or KINDS.get(doc.path.parent.name, 'paper')
        topics = fm.get('topics') or []
        if isinstance(topics, str):
            topics = [topics]
        entries.append({'id': ident, 'kind': kind, 'title': fm.get('title') or ident,
                        'url': fm.get('url') or '', 'topics': topics,
                        'year': fm.get('year'), 'date': fm.get('date'),
                        'authors': short_authors(fm.get('authors', fm.get('author'))),
                        'relevance': fm.get('relevance'), 'read_depth': fm.get('read_depth'),
                        'added_by': agent, 'added_at': stamp,
                        'summary': doc.sections().get('Summary', '')[:280], 'links': doc.cites()})
        agent_counts[agent] += 1
        if stamp:
            agent_last[agent] = max(stamp, agent_last.get(agent, ''))
    # Include all A records, even if a source was subsequently removed or renamed.
    by_path = {doc.rel: doc for doc in data.library.values()}
    for addition in additions:
        doc = by_path.get(addition['path'])
        agent = doc.get('added_by') if doc else None
        agent = agent or addition['agent']
        timeline_counts[(addition['t'], agent.split('/')[0], agent, addition['kind'])] += 1
    # Latest actual commit, including metadata updates, for every registered agent.
    for line in git('log', '--format=%aI\t%s').splitlines():
        stamp, message = line.split('\t', 1)
        agent = agent_from(message)
        agent_last[agent] = max(stamp, agent_last.get(agent, ''))
    agents = []
    for ident in sorted(set(data.agents) | set(agent_counts)):
        doc = data.agents.get(ident)
        fm = doc.fm if doc else {}
        agents.append({'id': ident, 'team': ident.split('/')[0],
                       'model': fm.get('model', fm.get('tool')), 'state': fm.get('state', 'unknown'),
                       'task': fm.get('task'), 'doing': fm.get('doing', ''), 'updated': fm.get('updated'),
                       'entries_added': agent_counts[ident], 'last_commit_at': agent_last.get(ident)})
    surveys = []
    for ident, doc in data.surveys.items():
        missing = data.gate_problems(doc) if not doc.error else [doc.error]
        surveys.append({'id': ident, 'topic': doc.get('topic') or ident,
                        'status': data.survey_state(ident), 'gate': {'passes': not missing, 'missing': missing},
                        'sources': len([c for c in doc.cites() if c in data.library]),
                        'reviewed_by': [r.get('reviewer') for r in data.reviews.values() if r.get('target') == ident]})
    tasks = docs_payload(data.tasks)
    summary = {'generated_at': dt.datetime.now(dt.timezone.utc).isoformat(),
               'head_sha': git('rev-parse', 'HEAD').strip(), 'counts': counts(entries),
               'topics': [{'slug': slug, 'name': topic['name'],
                           'counts': counts([e for e in entries if slug in e['topics']]),
                           'total': sum(slug in e['topics'] for e in entries)} for slug, topic in data.topics.items()],
               'surveys': {'n': len(surveys), 'passing': sum(s['gate']['passes'] for s in surveys)},
               'hypotheses': len(data.hypotheses), 'experiments': len(data.experiments),
               'tasks': {state: sum(t.get('status') == state for t in tasks) for state in ['open','claimed','done','blocked']},
               'agents': {'active': sum(a['state'] in {'active','working','running','busy'} for a in agents), 'total': len(agents)}}
    ids = {e['id'] for e in entries}
    edges = set()
    for entry in entries:
        for target in entry['links']:
            if target in ids and target != entry['id']:
                edges.add(tuple(sorted((entry['id'], target))))
    # Sparse topic chain plus four neighbors, not a quadratic topic clique.
    for slug in data.topics:
        members = sorted(e['id'] for e in entries if slug in e['topics'])
        for i, source in enumerate(members):
            for target in members[i+1:i+5]:
                if len(edges) < 20000:
                    edges.add((source, target))
    threads = [thread_payload(ident, doc) for ident, doc in sorted(data.library.items())
               if (doc.fm.get('type') or KINDS.get(doc.path.parent.name)) == 'thread']
    payloads = {'summary': summary, 'library': entries, 'agents': agents, 'tasks': tasks, 'threads': threads,
                'batches': batch_payload(), 'surveys': surveys,
                'timeline': [{'t': t, 'team': team, 'agent': agent, 'kind': kind, 'n_entries': n}
                             for (t, team, agent, kind), n in sorted(timeline_counts.items())],
                'graph': {'nodes': [{'id': e['id'], 'kind': e['kind'], 'topic': e['topics'][0] if e['topics'] else None} for e in entries],
                          'edges': [{'s': s, 't': t} for s, t in sorted(edges)]},
                'hypotheses': docs_payload(data.hypotheses), 'experiments': docs_payload(data.experiments),
                'questions': questions,
                'navigation': build_navigation(ROOT, questions, data.hypotheses, data.topics)}
    OUT.mkdir(parents=True, exist_ok=True)
    for name, payload in payloads.items():
        text = json.dumps(payload, ensure_ascii=False, separators=(',', ':'), default=str) + '\n'
        if len(text.encode()) > 5_000_000:
            raise ValueError(f'{name}.json exceeds 5 MB contract limit')
        (OUT / f'{name}.json').write_text(text, encoding='utf-8')
        print(f'{name}.json: {len(text.encode()):,} bytes')
    print(f'Exported {len(entries)} entries in {time.monotonic()-started:.2f}s')

if __name__ == '__main__':
    export()
