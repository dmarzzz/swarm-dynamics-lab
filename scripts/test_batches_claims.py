"""Offline ownership checks for J003. GitHub has no atomic issue CAS."""
import argparse
import unittest
from unittest.mock import patch
from test_batches_worktree import batches


def issue_for(*bodies, state="OPEN", labels=True):
    return {"state": state, "labels": [{"name": "claimed"}] if labels else [],
            "comments": [{"body": body, "createdAt": f"2026-10-04T12:{n:02d}:00Z"}
                         for n, body in enumerate(bodies)]}


class ClaimTest(unittest.TestCase):
    def test_non_holder_cannot_clear_winner(self):
        for verb in ("released", "done"):
            i = issue_for("claimed by `shadow/a`", f"{verb} by `shadow/b`",
                          "claimed by `shadow/c`")
            self.assertEqual(batches.claim_holder(i), "shadow/a")

    def test_holder_can_release_then_claim(self):
        for verb in ("released", "done"):
            i = issue_for("claimed by `shadow/a`", f"{verb} by `shadow/a`",
                          "claimed by `shadow/c`")
            self.assertEqual(batches.claim_holder(i), "shadow/c")

    def test_reclaim_race_preserved(self):
        i = issue_for("claimed by `shadow/a`", "reclaimed (previous claim stale) by `shadow/b`",
                      "reclaimed (previous claim stale) by `shadow/c`")
        self.assertEqual(batches.claim_holder(i), "shadow/b")

    def test_mutators_reject_non_holder_even_with_force(self):
        for command in (batches.cmd_touch, batches.cmd_release, batches.cmd_done):
            with self.subTest(command=command.__name__):
                a = argparse.Namespace(issue="1", agent="shadow/b", force=True, note="")
                with patch.object(batches, "issue", return_value=issue_for("claimed by `shadow/a`")), \
                     patch.object(batches, "gh") as gh, patch.object(batches.subprocess, "run") as run:
                    with self.assertRaises(SystemExit):
                        command(a)
                    gh.assert_not_called()
                    run.assert_not_called()

    def test_closed_unlabelled_and_unowned_fail_closed(self):
        a = argparse.Namespace(issue="1", agent="shadow/a")
        for i in (issue_for(), issue_for("claimed by `shadow/a`", state="CLOSED"),
                  issue_for("claimed by `shadow/a`", labels=False)):
            with patch.object(batches, "issue", return_value=i):
                with self.assertRaises(SystemExit):
                    batches.require_holder(a)

    def test_holder_touch_and_release(self):
        a = argparse.Namespace(issue="1", agent="shadow/a", note="test")
        with patch.object(batches, "issue", return_value=issue_for("claimed by `shadow/a`")), \
             patch.object(batches, "gh") as gh:
            self.assertEqual(batches.cmd_touch(a), 0)
            self.assertEqual(batches.cmd_release(a), 0)
            self.assertEqual(gh.call_count, 3)


if __name__ == "__main__":
    unittest.main()
