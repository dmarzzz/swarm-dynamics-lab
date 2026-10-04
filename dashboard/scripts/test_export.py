"""Validate dashboard data with unittest and the exporter's existing PyYAML dependency."""
import copy
import json
from pathlib import Path
import unittest
from types import SimpleNamespace
from research_navigation import build_navigation, SOURCE

import export as exporter

DATA = Path(__file__).resolve().parents[1] / 'public/data'

def load(name):
    return json.loads((DATA / f'{name}.json').read_text())

class ContractTest(unittest.TestCase):
    def test_counts_and_identity(self):
        entries, summary = load('library'), load('summary')
        self.assertEqual(len(entries), summary['counts']['total'])
        self.assertEqual(len(entries), len({e['id'] for e in entries}))
        mapping = {'papers':'paper','blogs':'blog','threads':'thread','code':'code','datasets':'dataset','talks':'talk'}
        for folder, kind in mapping.items():
            self.assertEqual(summary['counts'][folder], sum(e['kind'] == kind for e in entries))
        for entry in entries:
            self.assertIsInstance(entry['topics'], list)
            self.assertIsInstance(entry['authors'], str)
            self.assertLessEqual(len(entry['summary']), 280)
        self.assertTrue(all(e['added_at'] for e in entries))

    def test_graph_and_sizes(self):
        graph = load('graph')
        ids = {n['id'] for n in graph['nodes']}
        self.assertEqual(ids, {e['id'] for e in load('library')})
        self.assertTrue(all(e['s'] in ids and e['t'] in ids for e in graph['edges']))
        for path in DATA.glob('*.json'):
            self.assertLessEqual(path.stat().st_size, 5_000_000)

    def test_threads(self):
        library, threads = load('library'), load('threads')
        self.assertEqual({t['id'] for t in threads}, {e['id'] for e in library if e['kind'] == 'thread'})
        for t in threads:
            self.assertTrue(t['handle'].startswith('@'), t['id'])
            self.assertGreaterEqual(t['posts'], 1)
            self.assertLessEqual(len(t['first_line']), 160)
            for k in ('likes', 'reposts', 'replies', 'views'):
                self.assertTrue(t[k] is None or isinstance(t[k], int))
            json.dumps(t).encode('utf-8')

    def test_agents_and_gate(self):
        self.assertEqual(sum(a['entries_added'] for a in load('agents')), len(load('library')))
        for survey in load('surveys'):
            self.assertEqual(survey['gate']['passes'], not survey['gate']['missing'])
        self.assertTrue(all(row['n_entries'] > 0 for row in load('timeline')))

    def test_questions_preserve_canonical_atlas(self):
        canonical = json.loads(exporter.ATLAS.read_text(encoding='utf-8'))
        questions = load('questions')
        # Compare the entire object, including prose, source relationships, hashes and ordering.
        self.assertEqual(questions, canonical)
        ids = {row['id'] for row in questions['candidates']}
        self.assertEqual(len(ids), len(questions['candidates']))
        self.assertEqual({row['area'] for row in questions['candidates']}, set(questions['topics']))
        self.assertTrue(all(row['status'] == 'unreviewed-hunch' for row in questions['candidates']))
        self.assertFalse(ids & {row['id'] for row in load('hypotheses')})
        self.assertEqual(load('summary')['hypotheses'], len(load('hypotheses')))
        self.assertEqual(load('summary')['experiments'], len(load('experiments')))


class NavigationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas = json.loads(exporter.ATLAS.read_text())
        cls.source = json.loads((exporter.ROOT / SOURCE).read_text())
        cls.lab = exporter.helpers.Lab()

    def build(self, source=None, hypotheses=None):
        return build_navigation(exporter.ROOT, self.atlas,
                                hypotheses if hypotheses is not None else self.lab.hypotheses,
                                self.lab.topics, source if source is not None else self.source)

    def test_export_and_projects_preserve_atlas(self):
        before = copy.deepcopy(self.atlas)
        nav = self.build()
        self.assertEqual(nav, load('navigation'))
        self.assertEqual(self.atlas, before)
        self.assertEqual(len(nav['projects']), 16)
        self.assertEqual(len(nav['hypotheses']), len(self.lab.hypotheses))
        immune = next(f for f in nav['focus_areas'] if f['id'] == 'immune-response')
        self.assertIn('SEC-07', immune['questions'])
        self.assertNotIn('BUD-03', immune['questions'])

    def test_unknown_and_duplicate_members_fail(self):
        for member in ('NOT-999', self.source['focus_areas'][0]['questions'][0]):
            source = copy.deepcopy(self.source)
            source['focus_areas'][0]['questions'].append(member)
            with self.assertRaisesRegex(ValueError, 'unknown or duplicate focus question'):
                self.build(source)

    def test_paths_and_status_cannot_escape(self):
        for path in ('../AGENTS.md', '/etc/passwd', 'missing.md'):
            source = copy.deepcopy(self.source)
            source['designs'][0]['path'] = path
            with self.assertRaisesRegex(ValueError, 'unsafe or missing path'):
                self.build(source)
        source = copy.deepcopy(self.source)
        source['designs'][0]['status'] = 'accepted'
        with self.assertRaisesRegex(ValueError, 'must not imply hypothesis approval'):
            self.build(source)

    def test_snapshot_change_warns_without_rewriting(self):
        source = copy.deepcopy(self.source)
        source['reviewed_atlas_sha256'] = 'old'
        self.assertTrue(self.build(source)['mapping_stale'])

    def test_hypothesis_topics_require_canonical_unique_slugs(self):
        for tags, diagnostic in [(['message-board'], "unknown=['message-board']"),
                                 (['llm-agent-swarms', 'llm-agent-swarms'],
                                  "duplicates=['llm-agent-swarms']")]:
            with self.subTest(tags=tags):
                doc = SimpleNamespace(fm={'status': 'proposed', 'topics': tags},
                                      rel='hypotheses/example.md')
                with self.assertRaises(ValueError) as error:
                    self.build(hypotheses={'example': doc})
                self.assertIn('hypothesis topic in hypotheses/example.md', str(error.exception))
                self.assertIn(diagnostic, str(error.exception))

    def test_hypothesis_keywords_are_not_navigation_topics(self):
        doc = SimpleNamespace(fm={'status': 'proposed', 'topics': ['llm-agent-swarms'],
                                  'keywords': ['message-board', 'broadcast']},
                              rel='hypotheses/example.md')
        before = copy.deepcopy(doc.fm)
        nav = self.build(hypotheses={'example': doc})
        self.assertEqual(nav['hypotheses'][0]['topics'], ['llm-agent-swarms'])
        self.assertEqual(nav['hypotheses'][0]['status'], 'proposed')
        self.assertEqual(doc.fm, before)

    def test_explicit_hypothesis_tags_and_untagged_fallback(self):
        def doc(fm):
            return SimpleNamespace(fm=fm, rel='4-hypotheses/example.md')
        hypotheses = {'example': doc({'status': 'proposed', 'topics': ['llm-agent-swarms'],
                        'focus_areas': ['immune-response'], 'project_briefs': ['memory']}),
                      'untagged': doc({'status': 'draft'})}
        nav = self.build(hypotheses=hypotheses)
        self.assertEqual(nav['hypotheses'][0]['status'], 'proposed')
        self.assertEqual(nav['hypotheses'][0]['projects'], ['memory'])
        self.assertEqual(nav['hypotheses'][1]['topics'], [])
        hypotheses['example'].fm['focus_areas'] = ['unknown']
        with self.assertRaisesRegex(ValueError, 'unknown or duplicate hypothesis focus area'):
            self.build(hypotheses=hypotheses)


class QuestionsValidationTest(unittest.TestCase):
    """Bad atlas data must stop an export instead of silently losing review information."""
    @classmethod
    def setUpClass(cls):
        cls.canonical = json.loads(exporter.ATLAS.read_text(encoding='utf-8'))
        data = exporter.helpers.Lab()
        cls.library_paths = {ident: doc.rel for ident, doc in data.library.items()}
        cls.topics = data.topics

    def validate(self, payload):
        exporter.validate_questions(payload, self.library_paths, self.topics)

    def test_validating_does_not_rewrite_review_content(self):
        payload = copy.deepcopy(self.canonical)
        self.validate(payload)
        self.assertEqual(payload, self.canonical)

    def test_rejects_duplicate_ids_and_missing_fields(self):
        duplicate = copy.deepcopy(self.canonical)
        duplicate['candidates'].append(copy.deepcopy(duplicate['candidates'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicate candidate id'):
            self.validate(duplicate)
        missing = copy.deepcopy(self.canonical)
        del missing['candidates'][0]['falsifier']
        with self.assertRaisesRegex(ValueError, 'missing required fields'):
            self.validate(missing)

    def test_rejects_invalid_review_types_and_promotion(self):
        for field, value, message in [('metrics', 'quality', 'invalid metrics'),
                                      ('status', 'accepted', 'invalid candidate status'),
                                      ('change', [], 'invalid change')]:
            with self.subTest(field=field):
                payload = copy.deepcopy(self.canonical)
                payload['candidates'][0][field] = value
                with self.assertRaisesRegex(ValueError, message):
                    self.validate(payload)

    def test_rejects_unknown_topics_sources_and_mismatched_paths(self):
        payload = copy.deepcopy(self.canonical)
        payload['candidates'][0]['area'] = 'nonexistent-topic'
        with self.assertRaisesRegex(ValueError, 'unknown area'):
            self.validate(payload)
        payload = copy.deepcopy(self.canonical)
        payload['candidates'][0]['prior'][0]['id'] = 'nonexistent-source'
        with self.assertRaisesRegex(ValueError, 'unknown source'):
            self.validate(payload)
        payload = copy.deepcopy(self.canonical)
        payload['candidates'][0]['prior'][0]['path'] = 'AGENTS.md'
        with self.assertRaisesRegex(ValueError, 'source path does not match'):
            self.validate(payload)

    def test_rejects_missing_or_escaping_briefs(self):
        for path in ('5-experiments/studies/dmarz/question-atlas/nonexistent-brief.md',
                     '../AGENTS.md', str(exporter.ROOT / 'AGENTS.md')):
            with self.subTest(path=path):
                payload = copy.deepcopy(self.canonical)
                payload['candidates'][0]['briefs'] = [path]
                with self.assertRaisesRegex(ValueError, 'unknown or invalid brief path'):
                    self.validate(payload)

    def test_rejects_stale_card_and_enriched_content_hashes(self):
        payload = copy.deepcopy(self.canonical)
        payload['candidates'][0]['test'] += ' Changed intervention.'
        with self.assertRaisesRegex(ValueError, 'candidate hash mismatch'):
            self.validate(payload)
        payload = copy.deepcopy(self.canonical)
        payload['candidates'][0]['prior'][0]['title'] += ' Changed source metadata.'
        with self.assertRaisesRegex(ValueError, 'content hash mismatch'):
            self.validate(payload)

    def test_rejects_stale_change_index(self):
        payload = copy.deepcopy(self.canonical)
        row = payload['candidates'][0]
        payload['changes'][row['change']].remove(row['id'])
        with self.assertRaisesRegex(ValueError, 'change index does not match'):
            self.validate(payload)


class ContributionTest(unittest.TestCase):
    def setUp(self):
        import tempfile
        from contributions import build_contributions
        self.build = build_contributions
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / '5-experiments/studies/vishesh/bank.json'
        self.path.parent.mkdir(parents=True)
        brief = self.path.parent / 'project-briefs/memory.md'
        brief.parent.mkdir()
        brief.write_text('fixture')
        self.row = {'id':'EX-01', 'title':'Title', 'status':'exploratory hunch; not a registered hypothesis',
            'question':'Question', 'comparison':'Comparison', 'confounds':'Confounds', 'decision_value':'Decision',
            'sources':['source'], 'atlas':['A-01'], 'briefs':['memory'], 'related':[]}
        self.registry = [{'id':'EX', 'owner':'vishesh/codex-methods', 'path':str(self.path.relative_to(self.root)), 'collection':'ideas'}]

    def build_fixture(self, rows=None, registry=None):
        self.path.write_text(json.dumps({'ideas': rows if rows is not None else [self.row]}))
        return self.build(self.root, {'candidates':[{'id':'A-01'}]}, {'source':{}}, {}, self.registry if registry is None else registry)

    def test_counts_follow_input_not_fixed_snapshot(self):
        data = self.build_fixture()
        self.assertEqual((data['atlas_count'], data['contribution_count'], data['question_record_count']), (1,1,2))
        row2 = {**self.row, 'id':'EX-02', 'related':['EX-01']}
        data = self.build_fixture([self.row, row2])
        self.assertEqual(data['question_record_count'], 3)
        self.assertEqual(data['banks'][0]['count'], 2)

    def test_duplicate_and_canonical_collision_rejected(self):
        with self.assertRaises(ValueError): self.build_fixture([self.row, self.row])
        self.row['id'] = 'A-01'
        with self.assertRaises(ValueError): self.build_fixture()

    def test_unknown_links_and_status_rejected(self):
        for field in ['sources','atlas','briefs','related']:
            with self.subTest(field=field):
                with self.assertRaises(ValueError): self.build_fixture([{**self.row, field:['missing']}])
        with self.assertRaises(ValueError): self.build_fixture([{**self.row, 'status':'accepted'}])

    def test_paths_cannot_escape_owner_notes(self):
        for path in ['../secret.json', '/secret.json', '5-experiments/studies/dmarz/bank.json', '5-experiments/studies/vishesh/../../bank.json']:
            with self.subTest(path=path):
                with self.assertRaises(ValueError): self.build_fixture(registry=[{**self.registry[0], 'path':path}])

    def test_published_counts_and_original_atlas_remain_separate(self):
        data = load('contributions')
        canonical = load('questions')
        self.assertEqual(data['atlas_count'], len(canonical['candidates']))
        self.assertEqual(data['contribution_count'], sum(b['count'] for b in data['banks']))
        self.assertFalse({q['id'] for q in data['questions']} & {q['id'] for q in canonical['candidates']})
        self.assertEqual(data['registered_hypothesis_count'], len(load('hypotheses')))

class ContributionActivityTest(unittest.TestCase):
    def test_publication_expiry_and_independent_tag_additions(self):
        from contributions import activity_payload
        from datetime import datetime, timezone
        row = {'briefs':['memory','quorum'], 'activity': {'added_at':'2026-10-01T12:00:00Z',
            'tags_added_at': {'memory':'2026-10-01T12:00:00Z','quorum':'2026-10-08T10:00:00Z'}}}
        now = datetime(2026,10,8,12,tzinfo=timezone.utc)
        result = activity_payload(row, now)
        self.assertFalse(result['is_new'])  # Exactly seven days old.
        self.assertEqual(result['new_tags'], ['quorum'])
        row['activity']['added_at'] = '2026-10-01T12:00:01Z'
        row['activity']['tags_added_at']['memory'] = row['activity']['added_at']
        self.assertTrue(activity_payload(row, now)['is_new'])
        self.assertEqual(activity_payload(row, datetime(2026,10,16,tzinfo=timezone.utc))['new_tags'], [])

    def test_unknown_and_future_dates_are_not_new(self):
        from contributions import activity_payload
        from datetime import datetime, timezone
        now = datetime(2026,10,3,tzinfo=timezone.utc)
        self.assertFalse(activity_payload({'briefs':[]}, now)['is_new'])
        self.assertFalse(activity_payload({'briefs':[], 'activity': {'added_at':'2026-10-04T00:00:00Z'}}, now)['is_new'])

    def test_invalid_dates_unknown_tags_and_backdating_rejected(self):
        from contributions import activity_payload
        from datetime import datetime, timezone
        now = datetime(2026,10,3,tzinfo=timezone.utc)
        for metadata in [
            {'added_at':'2026-10-03'},
            {'added_at':'2026-99-03T00:00:00Z'},
            {'added_at':'2026-10-03T00:00:00Z','tags_added_at':{'missing':'2026-10-03T01:00:00Z'}},
            {'added_at':'2026-10-03T00:00:00Z','tags_added_at':{'memory':'2026-10-02T00:00:00Z'}},
        ]:
            with self.subTest(metadata=metadata):
                with self.assertRaises(ValueError): activity_payload({'briefs':['memory'], 'activity':metadata}, now)


class IdeaScoreContractTest(unittest.TestCase):
    def test_complete_initial_coverage_and_nullable_reviewers(self):
        from idea_scores import validate_record
        scores = load('idea-scores')
        ids = {q['id'] for q in load('questions')['candidates']} | {q['id'] for q in load('contributions')['questions']}
        self.assertEqual(set(scores['ideas']), ids)
        for ident, idea in scores['ideas'].items():
            self.assertEqual(set(idea['ratings']), {'vishesh', 'dmarz', 'shadow'})
            for record in idea['ratings'].values():
                validate_record(record, ident)
        # Other reviewers may contribute later; no test freezes their ratings at NA.
        self.assertTrue(any(q['ratings']['vishesh'] is not None for q in scores['ideas'].values()))

    def test_validation_zero_missing_and_bad_totals(self):
        from idea_scores import validate_record
        record = {'dimensions': {'visual': 0, 'practical': 0, 'theory': 0, 'novelty': 0}, 'score': 0,
                  'rationale': 'Zero is not missing', 'assessed_by': 'test', 'assessed_at': '2026-10-04', 'candidate_sha256': 'a'}
        validate_record(None, 'SOC-01')
        validate_record(record, 'SOC-01')
        for value in (-1, 101, float('nan'), float('inf'), True, '50'):
            bad = copy.deepcopy(record); bad['dimensions']['visual'] = value
            with self.assertRaises(ValueError): validate_record(bad, 'SOC-01')
        with self.assertRaises(ValueError): validate_record({**record, 'score': 1}, 'SOC-01')

    def test_content_fingerprints_ignore_activity_not_research(self):
        from idea_scores import fingerprint
        item = load('contributions')['questions'][0]
        altered = copy.deepcopy(item); altered['activity'] = {'is_new': False}
        self.assertEqual(fingerprint(item), fingerprint(altered))
        altered['question'] += ' Changed question.'
        self.assertNotEqual(fingerprint(item), fingerprint(altered))

    def test_missing_new_idea_defaults_to_na_and_old_score_is_stale(self):
        from idea_scores import build_scores
        atlas = copy.deepcopy(load('questions'))
        contributions = copy.deepcopy(load('contributions'))
        original = atlas['candidates'][0]['id']
        atlas['candidates'][0]['candidate_sha256'] = 'changed'
        atlas['candidates'].append({'id': 'NEW-01', 'title': 'New unreviewed idea', 'candidate_sha256': 'new'})
        scores = build_scores(exporter.ROOT, atlas, contributions)
        self.assertTrue(scores['ideas'][original]['ratings']['vishesh']['stale'])
        self.assertEqual(scores['ideas']['NEW-01']['ratings'], {'vishesh': None, 'dmarz': None, 'shadow': None})
        self.assertEqual(scores['ideas'][original]['ratings']['vishesh']['candidate_sha256'], load('idea-scores')['ideas'][original]['ratings']['vishesh']['candidate_sha256'])

class LayoutTest(unittest.TestCase):
    def test_old_layout_paths_resolve_and_current_paths_are_stable(self):
        from layout import current_path
        cases = {'library/papers/a.md': '1-library/papers/a.md',
                 'surveys/a.md': '2-surveys/a.md', 'reviews/a.md': '2-surveys/reviews/a.md',
                 'synthesis/a.md': '3-synthesis/a.md', 'hypotheses/a.md': '4-hypotheses/a.md',
                 'experiments/EVIDENCE.md': '5-experiments/EVIDENCE.md',
                 'tooling/x/README.md': '5-experiments/toolkit/x/README.md',
                 'researchers/vishesh/notes/project-briefs/memory.md': '5-experiments/studies/vishesh/project-briefs/memory.md',
                 'researchers/shadow/qa/a.md': '5-experiments/studies/shadow/qa/a.md',
                 'researchers/dmarz/inbox.md': 'lab/researchers/dmarz/inbox.md',
                 'tasks/t.md': 'lab/tasks/t.md', 'candidates/x/b.jsonl': 'lab/candidates/x/b.jsonl',
                 'templates/a.md': 'lab/templates/a.md', 'STATUS.md': 'lab/STATUS.md',
                 'dashboard/DEPLOY.md': 'dashboard/DEPLOY.md', 'src/x.py': 'src/x.py'}
        for old, new in cases.items():
            self.assertEqual(current_path(old), new)
            self.assertEqual(current_path(new), new)

    def test_atlas_paths_resolve_to_files_in_this_checkout(self):
        from layout import current_path
        for question in load('questions')['candidates']:
            for path in [s['path'] for s in question['prior']] + question['briefs']:
                self.assertTrue((exporter.ROOT / current_path(path)).is_file(), path)


if __name__ == '__main__':
    unittest.main()
