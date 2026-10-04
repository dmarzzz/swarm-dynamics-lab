"""Validated, additive research connections; never rewrite candidate content or status."""
import json
from pathlib import PurePosixPath
import re
from layout import STUDIES, current_path

SOURCE = STUDIES + '/vishesh/research-navigation/navigation.json'


def build_navigation(root, atlas, hypotheses, topics, source=None):
    source = source if source is not None else json.loads((root / SOURCE).read_text())

    def require(ok, message):
        if not ok:
            raise ValueError(f'navigation: {message}')

    def file(path):
        require(isinstance(path, str) and bool(path), 'invalid path')
        p = PurePosixPath(path)
        require(not p.is_absolute() and '..' not in p.parts and '\\' not in path
                and p.as_posix() == path, 'unsafe or missing path')
        path = current_path(path)  # navigation files written before the layout move keep their old paths
        require((root / path).is_file()
                and (root / path).resolve().is_relative_to(root.resolve()), 'unsafe or missing path')
        return root / path

    def ids(rows, label):
        require(isinstance(rows, list), f'invalid {label}')
        seen = set()
        for row in rows:
            require(isinstance(row, dict), f'invalid {label} row')
            ident = row.get('id')
            require(isinstance(ident, str) and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', ident), f'invalid {label} id')
            require(ident not in seen, f'duplicate {label} id')
            seen.add(ident)
        return seen

    def refs(values, known, label):
        require(isinstance(values, list) and all(isinstance(x, str) for x in values), f'invalid {label}')
        require(len(values) == len(set(values)) and set(values) <= set(known), f'unknown or duplicate {label}')
        return values

    require(source.get('schema') == 'swarm-lab-research-navigation-v1', 'unsupported schema')
    for field in ('owner', 'reviewed_at', 'reviewed_atlas_sha256'):
        require(isinstance(source.get(field), str) and bool(source[field]), f'missing {field}')
    questions = {q['id']: q for q in atlas['candidates']}
    crosswalk = json.loads(file(source['project_crosswalk']).read_text())
    projects = []
    for p in crosswalk['projects']:
        path = file(p['path'])
        refs(p['direct_atlas_links'], questions, 'project question')
        direct = [q['id'] for q in atlas['candidates'] if p['path'] in q['briefs']]
        connections = refs(p['reviewer_connected_atlas_ids'], questions, 'project connection')
        title = next(line.lstrip('# ').strip() for line in path.read_text().splitlines() if line.startswith('# '))
        if title == p['brief']:
            title = title.replace('-', ' ').capitalize().replace('Nca ', 'NCA ')
        projects.append({'id': p['brief'], 'name': title, 'path': p['path'],
                         'questions': sorted(set(direct + connections)),
                         'direct_questions': direct, 'reviewer_questions': connections})
    project_ids = ids(projects, 'project')
    focus_ids = ids(source['focus_areas'], 'focus area')
    for focus in source['focus_areas']:
        require(all(isinstance(focus.get(k), str) and focus[k].strip() for k in ('name', 'description')), 'missing focus description')
        refs(focus['questions'], questions, 'focus question')
        require(bool(focus['questions']), 'empty focus area')
    ids(source['designs'], 'design')
    for design in source['designs']:
        file(design['path'])
        require(isinstance(design.get('title'), str) and bool(design['title']), 'missing design title')
        require(design['status'] == 'exploratory design', 'design must not imply hypothesis approval')
        refs(design['focus_areas'], focus_ids, 'design focus area')
        refs(design['projects'], project_ids, 'design project')
        refs(design['topics'], topics, 'design topic')
    tagged_hypotheses = []
    for ident, doc in hypotheses.items():
        fm = doc.fm
        # Only explicit author tags. No inference of acceptance or inheritance from a survey.
        tagged_hypotheses.append({'id': ident, 'title': fm.get('title') or ident,
            'path': doc.rel, 'status': fm.get('status') or 'unspecified',
            # Hypothesis `topics` also carry free keywords; only library topic slugs link to a research area.
            'topics': refs([t for t in dict.fromkeys(fm.get('topics') or []) if t in topics], topics, 'hypothesis topic'),
            'focus_areas': refs(fm.get('focus_areas') or [], focus_ids, 'hypothesis focus area'),
            'projects': refs(fm.get('project_briefs') or [], project_ids, 'hypothesis project')})
    return {'schema': source['schema'], 'owner': source['owner'], 'source_path': SOURCE,
            'reviewed_at': source['reviewed_at'],
            'mapping_stale': source['reviewed_atlas_sha256'] != atlas['content_sha256']
                or crosswalk['atlas_sha256'] != atlas['content_sha256'],
            'focus_areas': source['focus_areas'], 'projects': projects,
            'designs': source['designs'], 'hypotheses': tagged_hypotheses}
