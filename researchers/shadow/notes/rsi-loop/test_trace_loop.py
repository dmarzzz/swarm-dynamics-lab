import json
from pathlib import Path
import tempfile
import unittest

import trace_loop as t


class TraceTests(unittest.TestCase):
    def test_typed_status_policy(self):
        for value in (None, 0, False, True, "1", "error"):
            self.assertFalse(t.candidate({"details": {"exitCode": value}}))
        for value in (1, -9, 127):
            self.assertTrue(t.candidate({"details": {"exitCode": value}}))
        self.assertTrue(t.candidate({"isError": True}))
        self.assertFalse(t.candidate({"isError": "true"}))
        self.assertFalse(t.candidate({"details": {"status": "running"}}))

    def test_no_content_or_untrusted_strings_exported(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "session.jsonl"
            sentinel = "PRIVATE_SENTINEL_DO_NOT_EXPORT"
            events = [
                {"type": "message", "message": {"role": "user", "content": sentinel}},
                {"type": "message", "message": {"role": "assistant", "model": sentinel, "provider": sentinel, "content": sentinel, "errorMessage": sentinel, "usage": {"input": 3, "output": 7, "cost": {"total": 0.2}}, "stopReason": "stop"}},
                {"type": "message", "message": {"role": "toolResult", "toolName": sentinel, "toolCallId": sentinel, "isError": False, "content": sentinel, "details": {"exitCode": 2, "aggregated": sentinel, "cwd": sentinel, "error": sentinel}}},
            ]
            p.write_text("".join(json.dumps(e) + "\n" for e in events))
            rec, score = t.normalize({"path": str(p), "run_id": "shadow-test", "partition": "replay"})
            encoded = t.safe_dump(rec)
            self.assertNotIn(sentinel, encoded)
            self.assertNotIn(str(p), encoded)
            self.assertEqual(rec["models"], {"other": 1})
            self.assertEqual(score["baseline_detected"], 0)
            self.assertEqual(score["candidate_detected"], 1)
            self.assertEqual(rec["outcome"], "ungraded")
            self.assertIsNone(rec["billed_cost_usd"])
            self.assertEqual(rec["coverage"]["complete_episode"], "unknown")
            self.assertEqual(rec["usage"]["estimated_cost_usd"]["sum_observed"], 0.2)
            self.assertIsNone(rec["usage"]["cache_read"]["sum_observed"])

    def test_malformed_and_truncated_lines_remain_visible(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "session.jsonl"
            p.write_bytes(b'not-json\n[]\n{"type":"message","message":false}\n{"type":')
            rec, _ = t.normalize({"path": str(p), "run_id": "shadow-test", "partition": "development"})
            self.assertEqual(rec["counts"]["malformed_lines"], 2)
            self.assertEqual(rec["counts"]["incomplete_lines"], 1)
            self.assertEqual(rec["counts"]["malformed_messages"], 1)
            self.assertEqual(rec["coverage"]["parse_integrity"], "partial")
            self.assertIsNone(rec["usage"]["input"]["sum_observed"])

    def test_manifest_requires_scope_and_unique_files(self):
        with tempfile.TemporaryDirectory() as d:
            p, m = Path(d) / "source", Path(d) / "manifest"
            p.write_text("")
            entry = {"run_id": "shadow-test", "partition": "replay", "path": str(p)}
            m.write_text(json.dumps({"sessions": [entry]}))
            with self.assertRaises(ValueError): t.load_manifest(m)
            m.write_text(json.dumps({"approved_scope": "swarm-hackathon", "sessions": [entry, {**entry, "run_id": "shadow-test-two"}]}))
            with self.assertRaises(ValueError): t.load_manifest(m)
            m.write_text(json.dumps({"approved_scope": "swarm-hackathon", "sessions": [entry]}))
            self.assertEqual(len(t.load_manifest(m)), 1)

    def test_secret_scan(self):
        with self.assertRaises(ValueError):
            t.safe_dump({"text": "sk-" + "x" * 32})
        with self.assertRaises(ValueError):
            t.safe_dump({"text": "api_key=" + "x" * 32})
        with self.assertRaises(ValueError): t.safe_dump({"n": float("nan")})

    def test_usage_rejects_nonfinite_and_boolean(self):
        self.assertFalse(t.number(True))
        self.assertFalse(t.number(float("inf")))
        self.assertFalse(t.number(-1))
        self.assertTrue(t.number(0))


if __name__ == "__main__":
    unittest.main()
