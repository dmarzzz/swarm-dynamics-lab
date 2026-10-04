import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
import prepare_development as p

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'doc').mkdir()
        raw = b'<html><body><form><p>Source <script>bad()</script> statement.</p></form></body></html>'
        (self.root / 'doc' / 'raw.html').write_bytes(raw)
        text = p.normalized(p.html.fromstring(raw).xpath('//p')[0])
        self.entry = {'document_id': 'doc', 'raw_sha256': hashlib.sha256(raw).hexdigest(), 'xpath': '//p', 'start': 0, 'end': len(text), 'text_sha256': hashlib.sha256(text.encode()).hexdigest(), 'evidence_id': 'E1', 'source_url': 'https://web.archive.org/web/20200101/https://example.org/source'}
        self.case = {'case_id': 'fixture', 'claim': 'Fixture', 'claim_date': None, 'source_key': 'private-gold-id', 'published_label': 'Supported', 'event_key': 'fixture-event', 'support_map': 'DO_NOT_DELIVER', 'limitations': 'development', 'evidence': [self.entry]}
    def test_form_wrapped_article_and_actor_gold_separation(self):
        actors, evaluators = p.prepare({'cases': [self.case]}, self.root)
        self.assertEqual(len(actors[0]['evidence']), 1)
        self.assertEqual(actors[0]['evidence'][0]['text'], 'Source statement.')
        self.assertEqual(actors[0]['evidence'][0]['source_host'], 'example.org')
        self.assertNotIn('published_label', actors[0])
        self.assertNotIn('support_map', actors[0])
        self.assertEqual(evaluators[0]['support_map'], 'DO_NOT_DELIVER')
    def test_changed_source_refused(self):
        (self.root / 'doc' / 'raw.html').write_text('<p>changed</p>')
        with self.assertRaisesRegex(ValueError, 'source_hash'):
            p.prepare({'cases': [self.case]}, self.root)
    def test_changed_passage_refused(self):
        self.entry['text_sha256'] = 'bad'
        with self.assertRaisesRegex(ValueError, 'passage_hash'):
            p.prepare({'cases': [self.case]}, self.root)
    def test_invalid_offsets_refused(self):
        self.entry['end'] = 999
        with self.assertRaisesRegex(ValueError, 'source_offsets'):
            p.prepare({'cases': [self.case]}, self.root)
    def test_missing_xpath_refused(self):
        self.entry['xpath'] = '//article'
        with self.assertRaisesRegex(ValueError, 'source_xpath'):
            p.prepare({'cases': [self.case]}, self.root)
    def test_archive_is_not_new_source(self):
        self.assertEqual(p.source_host('https://web.archive.org/web/20200101/http://example.org/source'), p.source_host('http://example.org/source'))

if __name__ == '__main__':
    unittest.main()
