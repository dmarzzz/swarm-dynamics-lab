import tempfile,unittest
from pathlib import Path
from finalize_native import import_evidence,inventory

class CloseoutImport(unittest.TestCase):
    def test_external_results_become_verified_relative_path(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);repo=root/'repo';repo.mkdir();results=root/'worker-results';results.mkdir()
            (results/'trace.jsonl').write_text('{"kind":"example"}\n');(results/'outcome.json').write_text('{}')
            relative=import_evidence(repo,results,'q-a7')
            self.assertFalse(relative.startswith('/'));self.assertEqual(inventory(repo/relative),inventory(results))
            self.assertEqual(import_evidence(repo,results,'q-a7'),relative)
            (repo/relative/'outcome.json').write_text('{"changed":true}')
            with self.assertRaisesRegex(ValueError,'evidence_changed'):import_evidence(repo,results,'q-a7')
    def test_symlink_and_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);results=root/'results';results.mkdir();(root/'private').write_text('test fixture')
            (results/'link').symlink_to(root/'private')
            with self.assertRaisesRegex(ValueError,'evidence_symlink'):import_evidence(root,results,'q-a7')
            with self.assertRaisesRegex(ValueError,'invalid_attempt'):import_evidence(root,results,'../escape')

if __name__=='__main__':unittest.main()
