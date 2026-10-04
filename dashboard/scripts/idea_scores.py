"""Independent, nullable researcher assessments; never alter research content hashes."""
import hashlib
import json
import math
from pathlib import Path

REVIEWERS = ('vishesh', 'dmarz', 'shadow')
WEIGHTS = {'visual': .30, 'practical': .30, 'theory': .25, 'novelty': .15}

def fingerprint(item):
    if item.get('candidate_sha256'):
        return item['candidate_sha256']
    content = {k: v for k, v in item.items() if k not in ('activity', 'scores')}
    return hashlib.sha256(json.dumps(content, sort_keys=True, ensure_ascii=True).encode()).hexdigest()

def validate_record(record, ident):
    if record is None:
        return
    if not isinstance(record, dict) or set(record.get('dimensions', {})) != set(WEIGHTS):
        raise ValueError(f'{ident}: all four score dimensions are required')
    for value in record['dimensions'].values():
        if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError(f'{ident}: score dimensions must be finite numbers from 0 to 100')
    expected = math.floor(sum(record['dimensions'][k] * w for k, w in WEIGHTS.items()) + .5)
    if type(record.get('score')) is not int or record['score'] != expected:
        raise ValueError(f'{ident}: score must be the rounded weighted total ({expected})')
    for field in ('rationale', 'assessed_by', 'assessed_at', 'candidate_sha256'):
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f'{ident}: missing {field}')

def build_scores(root, atlas, contributions):
    folder = root / 'dashboard/idea-scores'
    rubric = json.loads((folder / 'rubric.json').read_text())
    if rubric['weights'] != WEIGHTS:
        raise ValueError('Score rubric weights require a versioned implementation change')
    items = atlas['candidates'] + contributions['questions']
    known = {q['id'] for q in items}
    if len(known) != len(items):
        raise ValueError('Duplicate idea IDs')
    reviews = {}
    for reviewer in REVIEWERS:
        path = folder / f'{reviewer}.json'
        payload = json.loads(path.read_text())
        if payload.get('schema') != 'swarm-idea-review-v1' or payload.get('reviewer') != reviewer or payload.get('rubric_version') != rubric['version']:
            raise ValueError(f'{reviewer}: invalid score-file identity or rubric')
        values = payload['ratings']
        if not isinstance(values, dict) or set(values) - known:
            raise ValueError(f'{reviewer}: unknown idea IDs')
        for ident, record in values.items():
            validate_record(record, ident)
        reviews[reviewer] = values
    result = {}
    for item in items:
        ident, sha = item['id'], fingerprint(item)
        result[ident] = {'title': item['title'], 'candidate_sha256': sha, 'ratings': {}}
        for reviewer in REVIEWERS:
            record = reviews[reviewer].get(ident)
            result[ident]['ratings'][reviewer] = ({**record, 'stale': record['candidate_sha256'] != sha} if record is not None else None)
    return {'schema': 'swarm-idea-scores-v1', 'rubric': rubric, 'ideas': result}
