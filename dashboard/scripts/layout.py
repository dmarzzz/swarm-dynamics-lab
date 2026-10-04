"""Repo layout for the dashboard exporter, and the map from the flat layout the repo used before the
research-phase move. Study files written before the move (the question atlas, the navigation crosswalk) are
hash-bound and keep their old paths; `current_path` resolves those to where the file lives now."""
import re

LIBRARY = '1-library'
STUDIES = '5-experiments/studies'
CANDIDATES = 'lab/candidates'
REPO = 'dmarzzz/swarm-dynamics-lab'

_PREFIXES = (('library/', '1-library/'), ('surveys/', '2-surveys/'), ('reviews/', '2-surveys/reviews/'),
             ('synthesis/', '3-synthesis/'), ('hypotheses/', '4-hypotheses/'), ('experiments/', '5-experiments/'),
             ('tooling/', '5-experiments/toolkit/'), ('tasks/', 'lab/tasks/'), ('candidates/', 'lab/candidates/'),
             ('templates/', 'lab/templates/'))
_EXACT = {'STATUS.md': 'lab/STATUS.md', 'PIPELINE.md': 'lab/PIPELINE.md'}
_STUDY = re.compile(r'^researchers/([^/]+)/(?:notes/|(?=(?:factory|qa)/))')


def current_path(path):
    """Old-layout repo path -> current path. A path already in the current layout is returned unchanged."""
    if not isinstance(path, str):
        return path
    if path in _EXACT:
        return _EXACT[path]
    match = _STUDY.match(path)
    if match:
        return f'{STUDIES}/{match.group(1)}/' + path[match.end():]
    if path.startswith('researchers/'):
        return 'lab/' + path
    for old, new in _PREFIXES:
        if path.startswith(old):
            return new + path[len(old):]
    return path
