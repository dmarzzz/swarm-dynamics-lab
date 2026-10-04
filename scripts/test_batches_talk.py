"""J001: talk batches must instruct writers to create talk entries."""
import unittest
from test_batches_worktree import batches


class TalkInstructionsTest(unittest.TestCase):
    def test_talk_issue_instructions(self):
        body = batches.issue_body("talk-example", "talk", "meta", [])
        self.assertIn("lab.py new talk <id>", body)
        self.assertIn("into `1-library/talks/`", body)
        self.assertIn("--entries 1-library/talks/<id>.md", body)
        self.assertIn("yt-dlp --skip-download", body)
        self.assertNotIn("lab.py new blog", body)


if __name__ == "__main__":
    unittest.main()
