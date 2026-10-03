"""Separate exploratory banks; never modify the canonical atlas or review hashes."""
from datetime import datetime, timezone, timedelta
import json
import re
from pathlib import PurePosixPath

STATUS = 'exploratory hunch; not a registered hypothesis'

RECENT_DAYS = 7

def activity_payload(item, now):
    """Explicit publication metadata, never file modification or dashboard deployment time."""
    activity = item.get('activity')
    if activity is None:
        return {'added_at': None, 'tags_added_at': {}, 'is_new': False, 'new_tags': []}
    def stamp(value):
        if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', value):
            raise ValueError('Activity dates must be UTC timestamps ending in Z')
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    added = stamp(activity['added_at'])
    tags = activity.get('tags_added_at', {})
    if not isinstance(tags, dict) or any(tag not in item['briefs'] for tag in tags):
        raise ValueError('Activity tags must be current project-area tags')
    recent = lambda date: timedelta(0) <= now - date < timedelta(days=RECENT_DAYS)
    new_tags = []
    for tag, value in tags.items():
        tagged = stamp(value)
        if tagged < added:
            raise ValueError('Tag cannot predate the item')
        if tagged > added and recent(tagged):
            new_tags.append(tag)
    return {'added_at': activity['added_at'], 'tags_added_at': tags, 'is_new': recent(added), 'new_tags': new_tags}

def build_contributions(root, atlas, library, hypotheses, registry=None, now=None):
    now = now or datetime.now(timezone.utc)
    if registry is None:
        registry = json.loads((root / 'dashboard/contribution-banks.json').read_text())
    canonical = {q['id'] for q in atlas['candidates']}
    seen, records, banks = set(canonical), [], []
    for bank in registry:
        path = PurePosixPath(bank['path'])
        researcher = bank['owner'].split('/')[0]
        if path.is_absolute() or '..' in path.parts or not path.as_posix().startswith(f'researchers/{researcher}/notes/'):
            raise ValueError('Contribution path must be owned researcher notes')
        if not (root / path).resolve().is_relative_to((root / 'researchers' / researcher / 'notes').resolve()):
            raise ValueError('Contribution path escapes owned notes')
        raw = json.loads((root / path).read_text())[bank['collection']]
        for item in raw:
            ident = item['id']
            if ident in seen or not re.fullmatch(re.escape(bank['id']) + r'-[0-9]+', ident):
                raise ValueError(f'Duplicate or invalid contribution ID: {ident}')
            seen.add(ident)
            if item.get('status') != STATUS:
                raise ValueError(f'Contribution must be explicitly exploratory: {ident}')
            question = item.get('question') or item.get('question_and_delta') or item.get('delta')
            required = [question, item.get('title'), item.get('comparison'), item.get('confounds'), item.get('decision_value')]
            if not all(isinstance(v, str) and v.strip() for v in required):
                raise ValueError(f'Incomplete contribution: {ident}')
            sources = item.get('sources', item.get('prior', []))
            if not sources or any(source not in library for source in sources):
                raise ValueError(f'Unknown source in {ident}')
            if not item.get('atlas') or any(q not in canonical for q in item['atlas']):
                raise ValueError(f'Unknown atlas link in {ident}')
            for brief in item['briefs']:
                if not re.fullmatch(r'[a-z0-9-]+', brief) or not (root / 'researchers/vishesh/notes/project-briefs' / (brief + '.md')).is_file():
                    raise ValueError(f'Unknown brief in {ident}: {brief}')
            records.append({**{key: item.get(key, '') for key in ['id','title','prediction','comparison','falsifier','confounds','feasibility','decision_value','scenario']},
                'question': question, 'delta': item.get('delta', item.get('v2_overlap_review', '')),
                'metrics': item.get('metrics', []), 'briefs': item['briefs'], 'atlas': item['atlas'],
                'related': item.get('related', item.get('nearest_existing', [])),
                'sources': sources, 'source_note': item.get('source_note', 'Catalogue references are reading leads, not a fresh methods review or novelty certification.'),
                'activity': activity_payload(item, now),
                'status': STATUS, 'bank': bank['id'], 'owner': bank['owner'], 'source_path': str(path)})
        banks.append({'id': bank['id'], 'owner': bank['owner'], 'path': str(path), 'count': len(raw)})
    if len({b['id'] for b in banks}) != len(banks):
        raise ValueError('Duplicate bank ID')
    for item in records:
        if any(q not in seen for q in item['related']):
            raise ValueError(f"Unknown related contribution: {item['id']}")
    return {'schema': 'swarm-contributions-v1', 'activity_as_of': now.isoformat(), 'recent_days': RECENT_DAYS, 'atlas_count': len(canonical), 'contribution_count': len(records),
        'question_record_count': len(canonical) + len(records), 'registered_hypothesis_count': len(hypotheses),
        'banks': banks, 'questions': records}
