"""J002: each mapped source must create entries in its actual kind folder."""
import unittest
from test_batches_worktree import batches


class DestinationTest(unittest.TestCase):
    def test_every_mapped_source_matches_kind(self):
        folders = {"thread": "threads", "blog": "blogs", "talk": "talks",
                   "paper": "papers", "code": "code"}
        self.assertEqual(set(batches.LIB_DIR), set(batches.NEW_KIND))
        for source, kind in batches.NEW_KIND.items():
            with self.subTest(source=source):
                destination = f"1-library/{folders[kind]}/"
                self.assertEqual(batches.LIB_DIR[source], destination)
                body = batches.issue_body("example", source, "meta", [])
                self.assertIn(f"lab.py new {kind} <id>", body)
                self.assertIn(f"into `{destination}`", body)
                self.assertIn(f"--entries {destination}<id>.md", body)


if __name__ == "__main__":
    unittest.main()
