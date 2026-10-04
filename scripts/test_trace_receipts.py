import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from experiment_ops import trace_receipts as t


class TraceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        ref = t.retain(self.root / 'private', b'PRIVATE_TEST_CANARY')
        ref['path'] = 'private/' + ref['path']
        self.ref = ref
        self.manifest = {'schema_version': 1, 'study': 'study', 'attempt': 'a1',
                         'source_sha256': 'a'*64, 'config_sha256': 'b'*64,
                         'assignments': [{'id': 'one', 'unit': 'receipt1', 'arm': 'A'},
                                         {'id': 'two', 'unit': 'receipt1', 'arm': 'B'}],
                         'calls': [{'assignment': 'one', 'call_id': 'physical1', 'status': 'valid',
                                    'artifacts': {k: copy.deepcopy(ref) for k in t.KINDS}},
                                   {'assignment': 'two', 'call_id': None, 'status': 'unstarted', 'artifacts': {}}]}

    def audit(self):
        (self.root/'trace-manifest.json').write_text(json.dumps(self.manifest))
        value = t.audit(self.root, 'study', 'a1')
        self.assertNotIn('PRIVATE_TEST_CANARY', json.dumps(value))
        self.assertNotIn('private/', json.dumps(value))
        return value

    def test_counts_and_units(self):
        a = self.audit()
        self.assertEqual(a['status'], 'verified_declared_coverage')
        self.assertEqual(a['assignment_count'], 2)
        self.assertEqual(a['distinct_unit_labels'], 1)
        self.assertEqual(a['counts']['unstarted'], 1)
        self.assertEqual(a['coverage']['response']['verified'], 1)

    def test_missing_and_tampered_bytes(self):
        (self.root/self.ref['path']).write_bytes(b'changed')
        self.assertEqual(self.audit()['mismatched_artifacts'], len(t.KINDS))
        (self.root/self.ref['path']).unlink()
        self.assertEqual(self.audit()['missing_artifacts'], len(t.KINDS))

    def test_missing_manifest_is_unknown(self):
        self.assertEqual(t.audit(self.root)['status'], 'unavailable')

    def test_unresolved_start_not_success(self):
        self.manifest['calls'][0]['status'] = 'started'
        self.assertEqual(self.audit()['unresolved_started'], 1)
        self.assertEqual(self.audit()['status'], 'gaps')

    def test_duplicate_assignment_and_physical_call(self):
        self.manifest['assignments'].append(copy.deepcopy(self.manifest['assignments'][0]))
        self.assertEqual(self.audit()['status'], 'invalid')
        self.manifest['assignments'].pop()
        self.manifest['calls'][1] = copy.deepcopy(self.manifest['calls'][0])
        self.manifest['calls'][1]['assignment'] = 'two'
        self.assertEqual(self.audit()['status'], 'invalid')

    def test_all_assignments_accounted(self):
        self.manifest['calls'].pop()
        self.assertEqual(self.audit()['status'], 'invalid')

    def test_traversal_and_symlink(self):
        original = self.manifest['calls'][0]['artifacts']['input']['path']
        for path in ('../outside', '/etc/passwd'):
            self.manifest['calls'][0]['artifacts']['input']['path'] = path
            self.assertEqual(self.audit()['status'], 'invalid')
        self.manifest['calls'][0]['artifacts']['input']['path'] = original
        (self.root/original).unlink(); (self.root/original).symlink_to('/etc/passwd')
        self.assertEqual(self.audit()['status'], 'invalid')

    def test_required_input_cannot_be_waived(self):
        self.manifest['calls'][0]['artifacts']['input'] = {'absent': 'not_applicable'}
        self.assertEqual(self.audit()['status'], 'invalid')
        self.manifest['calls'][0]['artifacts']['input'] = {'absent': 'legacy_missing'}
        self.assertEqual(self.audit()['status'], 'gaps')

    def test_unknown_metadata_never_printed(self):
        self.manifest['secret'] = 'PRIVATE_TEST_CANARY'
        self.assertEqual(self.audit()['status'], 'invalid')

    def test_wrong_identity(self):
        self.audit()
        self.assertEqual(t.audit(self.root, 'other', 'a1')['status'], 'invalid')
        self.assertEqual(t.audit(self.root, 'study', 'a2')['status'], 'invalid')

    def test_retain_idempotent_and_no_clobber(self):
        self.assertEqual(t.retain(self.root/'private', b'PRIVATE_TEST_CANARY')['sha256'], self.ref['sha256'])
        (self.root/self.ref['path']).write_bytes(b'corrupted')
        with self.assertRaises(t.InvalidReceipt):
            t.retain(self.root/'private', b'PRIVATE_TEST_CANARY')

    def test_partial_and_duplicate_json(self):
        for raw in ('{"schema_version":', '{"schema_version":1,"schema_version":1}'):
            (self.root/'trace-manifest.json').write_text(raw)
            self.assertEqual(t.audit(self.root)['status'], 'invalid')

    def test_private_file_mode(self):
        self.assertEqual((self.root/self.ref['path']).stat().st_mode & 0o777, 0o600)

    def test_malformed_types_safe(self):
        for value in (None, [], 123, 'PRIVATE_TEST_CANARY'):
            (self.root/'trace-manifest.json').write_text(json.dumps(value))
            self.assertEqual(t.audit(self.root)['status'], 'invalid')


if __name__ == '__main__': unittest.main()
