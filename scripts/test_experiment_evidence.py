"""Offline checks for evidence coverage and non-destructive metadata rendering."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

import experiment_evidence as evidence


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.document = "5-experiments/studies/alice/study/README.md"
        self.registration = "5-experiments/studies/alice/study/experiment.yaml"
        self.original = "---\ntitle: 'Keep: punctuation'\n---\n\n# Study\n\nOriginal **prose**.\n"
        self.put(self.document, self.original)
        self.put(self.registration, "id: study\n")
        self.put(evidence.RUBRIC, "# Rubric\n")
        self.data = {"schema_version": 1, "assessed_at": "2026-10-04", "assessor": "alice/review",
                     "source_commit": "a" * 40, "studies": [{
                         "id": "study-v1", "title": "Study", "documents": [self.document],
                         "experiment_ids": ["study"], "registration_paths": [self.registration],
                         "evidence_confidence": {"score": 1, "claim": "A bounded pilot.", "rationale": "One task family."},
                         "sample_size_summary": "3 independent roots; 12 paired outcomes.", "sources": [self.document]}]}

    def put(self, path, value):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(value.encode("utf-8"))

    def test_invalid_scores_and_duplicate_ids(self):
        for score in (True, -1, 5, 1.0, "2"):
            data = copy.deepcopy(self.data)
            data["studies"][0]["evidence_confidence"]["score"] = score
            with self.subTest(score=score), self.assertRaisesRegex(ValueError, "invalid score"):
                evidence.validate(self.root, data)
        self.data["studies"].append(copy.deepcopy(self.data["studies"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate study"):
            evidence.validate(self.root, self.data)

    def test_null_is_explicitly_unassessed(self):
        self.data["studies"][0]["evidence_confidence"]["score"] = None
        rendered = evidence.outputs(self.root, self.data)[self.document]
        self.assertIn("**unassessed**", rendered)
        self.assertNotIn("0/4", rendered)

    def test_rejects_path_escape_missing_source_and_external_symlink(self):
        for path in ("../outside.md", "/tmp/outside.md", "missing.md"):
            data = copy.deepcopy(self.data)
            data["studies"][0]["sources"] = [path]
            with self.subTest(path=path), self.assertRaises(ValueError):
                evidence.validate(self.root, data)
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "source.md"
            target.write_text("outside")
            (self.root / "linked.md").symlink_to(target)
            self.data["studies"][0]["sources"] = ["linked.md"]
            with self.assertRaisesRegex(ValueError, "external"):
                evidence.validate(self.root, self.data)

    def test_covers_registrations_and_formal_experiments_but_not_snapshots(self):
        self.put("5-experiments/studies/alice/pi-review-2026-10-04/source/experiment.json", "{}")
        evidence.validate(self.root, self.data)
        self.put("5-experiments/studies/alice/another/experiment.json", "{}")
        with self.assertRaisesRegex(ValueError, "uncovered experiment registrations"):
            evidence.validate(self.root, self.data)
        (self.root / "5-experiments/studies/alice/another/experiment.json").unlink()
        self.put("5-experiments/formal/README.md", "# Formal\n")
        with self.assertRaisesRegex(ValueError, "uncovered formal"):
            evidence.validate(self.root, self.data)
        (self.root / "5-experiments/formal/README.md").unlink()
        for shared in ("studies", "toolkit"):  # folder guides, not formal experiments
            self.put(f"5-experiments/{shared}/README.md", "# Guide\n")
        evidence.validate(self.root, self.data)

    def test_block_rendered_before_layout_move_is_left_untouched_unless_relinked(self):
        self.assertEqual(evidence.legacy(self.document), "researchers/alice/notes/study/README.md")
        self.assertEqual(evidence.legacy("5-experiments/studies/shadow/factory/a.md"), "researchers/shadow/factory/a.md")
        self.assertEqual(evidence.legacy("5-experiments/toolkit/kit/README.md"), "tooling/kit/README.md")
        self.assertEqual(evidence.legacy("5-experiments/formal/README.md"), "experiments/formal/README.md")
        current = evidence.outputs(self.root, self.data)[self.document]
        self.assertIn("[registry](../../../evidence-metadata.json)", current)
        old = current.replace("](../../../evidence-metadata.json)", "](../../../../experiments/evidence-metadata.json)") \
                     .replace("](../../../EVIDENCE-METADATA.md)", "](../../../../experiments/EVIDENCE-METADATA.md)")
        self.put(self.document, old)
        self.assertEqual(evidence.outputs(self.root, self.data)[self.document], old)
        self.assertEqual(evidence.outputs(self.root, self.data, relink=True)[self.document], current)
        self.put(self.document, old.replace("**1/4**", "**4/4**"))  # stale content is still rewritten in full
        self.assertEqual(evidence.outputs(self.root, self.data)[self.document], current)

    def test_preserves_content_line_endings_and_is_idempotent(self):
        for newline in ("\n", "\r\n"):
            original = self.original.replace("\n", newline)
            self.put(self.document, original)
            rendered = evidence.outputs(self.root, self.data)[self.document]
            self.assertTrue(rendered.startswith(original.split("# Study")[0] + "# Study" + newline))
            self.assertTrue(rendered.endswith(newline + "Original **prose**." + newline))
            self.assertEqual(rendered.count(evidence.START), 1)
            self.put(self.document, rendered)
            self.assertEqual(evidence.outputs(self.root, self.data)[self.document], rendered)

    def test_multiple_cohorts_share_one_block(self):
        other = copy.deepcopy(self.data["studies"][0])
        other.update(id="study-v2", title="Second cohort", source_commit="b" * 40)
        self.data["studies"].append(other)
        rendered = evidence.outputs(self.root, self.data)[self.document]
        self.assertEqual(rendered.count(evidence.START), 1)
        self.assertEqual(rendered.count("**sample_size_summary:**"), 2)
        self.assertIn("Second cohort", rendered)
        self.assertIn("Source: `aaaaaaaa`.", rendered)
        self.assertIn("Source: `bbbbbbbb`.", rendered)

    def test_reassessment_keeps_original_and_new_assessors_distinct(self):
        other = copy.deepcopy(self.data["studies"][0])
        other.update(id="study-v2", title="Reassessment", assessor="bob/operator", assessed_at="2026-10-05")
        self.data["studies"].append(other)
        rendered = evidence.outputs(self.root, self.data)[self.document]
        self.assertIn("Assessed 2026-10-04 by alice/review.", rendered)
        self.assertIn("Assessed 2026-10-05 by bob/operator.", rendered)
        self.data["studies"] = [other]
        rendered = evidence.outputs(self.root, self.data)[self.document]
        self.assertIn("Assessed 2026-10-05 by bob/operator;", rendered)
        self.assertNotIn("by alice/review", rendered)

    def test_invalid_reassessment_metadata(self):
        for fields in ({"assessor": ""}, {"assessed_at": "2026-13-01"}):
            data = copy.deepcopy(self.data)
            data["studies"][0].update(fields)
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                evidence.validate(self.root, data)

    def test_frontmatter_title_without_h1_preserves_formal_template(self):
        original = "---\ntitle: Formal study\n---\n\n## Setup\n\nKeep this protocol.\n"
        self.put(self.document, original)
        rendered = evidence.outputs(self.root, self.data)[self.document]
        self.assertTrue(rendered.startswith("---\ntitle: Formal study\n---\n\n"))
        self.assertTrue(rendered.endswith("\n\n## Setup\n\nKeep this protocol.\n"))
        self.assertEqual(rendered.count(evidence.START), 1)
        self.put(self.document, rendered)
        self.assertEqual(evidence.outputs(self.root, self.data)[self.document], rendered)

    def test_malformed_markers_fail_without_rewriting(self):
        for bad in (evidence.START, evidence.END + evidence.START, (evidence.START + evidence.END) * 2):
            self.put(self.document, self.original + bad)
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                evidence.outputs(self.root, self.data)
            self.assertEqual((self.root / self.document).read_text(), self.original + bad)

    def test_check_detects_staleness_and_write_preserves_registration(self):
        self.put(evidence.REGISTRY, json.dumps(self.data))
        args = ["--root", str(self.root)]
        before = (self.root / self.registration).read_bytes()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(evidence.main(args), 1)
            self.assertEqual(evidence.main(args + ["--write"]), 0)
            self.assertEqual(evidence.main(args + ["--check"]), 0)
            path = self.root / self.document
            path.write_text(path.read_text().replace("**1/4**", "**4/4**"))
            self.assertEqual(evidence.main(args + ["--check"]), 1)
        self.assertEqual((self.root / self.registration).read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
