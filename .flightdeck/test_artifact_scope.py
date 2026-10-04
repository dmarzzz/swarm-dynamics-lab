"""J041: publication adds only the new version's facts and statement, offline."""
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import fd


class ArtifactScopeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "project.yaml").write_text("name: fixture\n")
        for name, value in (("git_remote_url", None), ("git_commit", None),
                            ("session_from_env", {}), ("model_of", None)):
            mock = patch.object(fd, name, return_value=value)
            mock.start()
            self.addCleanup(mock.stop)
        artifacts = []
        for aid in ("private-input", "changed-input", "absent-artifact", "mtime-only"):
            rel = f"artifacts/{aid}/{aid}-v1.svg"
            target = self.root / rel
            target.parent.mkdir(parents=True)
            target.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="900"/>')
            (self.root / f"{aid}.txt").write_text("Historical input\n")
            artifacts.append({"id": aid, "category": "content", "type": "figure", "title": aid,
                              "versions": [{"v": 1, "date": "2026-10-04", "path": rel,
                                            "ingredients": [f"{aid}.txt"], "by": "codex"}]})
        self.manifest = {"manifest": 1, "project": "fixture", "artifacts": artifacts}
        fd.write_yaml(str(self.root / "artifacts.yaml"), self.manifest)
        fd.refresh_lock(str(self.root), self.manifest)
        self.before = fd.ac.load_lock(str(self.root))
        self.before["extension"] = {"historical": [1, 2]}
        self.before["entries"]["private-input@1"]["extension"] = ["preserve me"]
        fd.ac.write_lock(str(self.root), self.before)
        for aid in (a["id"] for a in artifacts):
            Path(fd.bundle_path(str(self.root), aid, 1)).write_bytes(b"synthetic signed bundle\n")
        self.old_files = {p.relative_to(self.root): p.read_bytes()
                          for p in (self.root / "attestations").iterdir()}
        (self.root / "private-input.txt").unlink()
        (self.root / "changed-input.txt").write_text("New unrelated input, not used by the historical build\n")
        (self.root / "artifacts/absent-artifact/absent-artifact-v1.svg").unlink()
        p = self.root / "artifacts/mtime-only/mtime-only-v1.svg"
        os.utime(p, (p.stat().st_atime, p.stat().st_mtime + 100))
        self.source = self.root / "new.svg"
        self.source.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1000"/>')

    def add(self, aid):
        return fd.main(["add", str(self.source), "--id", aid, "--type", "figure",
                        "--title", "New figure", "--ingredient", "changed-input.txt",
                        "--prompt", "File the derived figure", "--by", "codex",
                        "--copy", "--strict", "--folder", str(self.root)])

    def assert_preserved(self, aid, version):
        after = fd.ac.load_lock(str(self.root))
        key = f"{aid}@{version}"
        new = after["entries"].pop(key)
        self.assertEqual(after, self.before)
        for path, content in self.old_files.items():
            self.assertEqual((self.root / path).read_bytes(), content, str(path))
        new_statement = Path(fd.statement_path(str(self.root), aid, version))
        self.assertEqual(set((self.root / "attestations").iterdir()),
                         {self.root / p for p in self.old_files} | {new_statement})
        self.assertEqual(new["sha256"], hashlib.sha256(self.source.read_bytes()).hexdigest())
        self.assertEqual(new["ingredients"][0]["sha256"],
                         hashlib.sha256((self.root / "changed-input.txt").read_bytes()).hexdigest())
        self.assertEqual(new["prompt_sha256"], fd.ac.prompt_digest("File the derived figure"))
        self.assertEqual(json.loads(new_statement.read_text())["subject"][0]["digest"]["sha256"], new["sha256"])
        manifest, _ = fd.read_yaml(str(self.root / "artifacts.yaml"))
        target = next(a for a in manifest["artifacts"] if a["id"] == aid)
        target["versions"].pop(0)
        if version == 1:
            manifest["artifacts"].remove(target)
        self.assertEqual(manifest, self.manifest)
        return json.loads(new_statement.read_text())

    def test_new_artifact_preserves_all_historical_provenance(self):
        self.assertEqual(self.add("new-figure"), 0)
        self.assert_preserved("new-figure", 1)

    def test_new_version_preserves_v1_and_uses_saved_supersedes_digest(self):
        self.assertEqual(self.add("private-input"), 0)
        statement = self.assert_preserved("private-input", 2)
        supersedes = [d for d in statement["predicate"]["buildDefinition"]["resolvedDependencies"]
                      if d.get("annotations", {}).get("supersedes")]
        self.assertEqual(supersedes, [{"uri": self.before["entries"]["private-input@1"]["path"],
                                     "digest": {"sha256": self.before["entries"]["private-input@1"]["sha256"]},
                                     "annotations": {"supersedes": True}}])

    def test_bad_existing_lock_fails_before_any_write(self):
        for bad in ("{", "[]", "null", '{"lock":1,"entries":[]}',
                    '{"lock":1,"entries":{"x":null}}', '{"lock":2,"entries":{}}'):
            with self.subTest(lock=bad):
                (self.root / "artifacts.lock.json").write_text(bad)
                before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
                with self.assertRaises(ValueError):
                    self.add("new-figure")
                self.assertEqual(before, {p.relative_to(self.root): p.read_bytes()
                                          for p in self.root.rglob("*") if p.is_file()})

    def test_first_add_without_lock_does_not_backfill_old_artifacts(self):
        (self.root / "artifacts.lock.json").unlink()
        self.assertEqual(self.add("new-figure"), 0)
        self.assertEqual(set(fd.ac.load_lock(str(self.root))["entries"]), {"new-figure@1"})
        for path, content in self.old_files.items():
            self.assertEqual((self.root / path).read_bytes(), content)

    def test_selected_fill_does_not_mutate_input_lock(self):
        original = copy.deepcopy(self.before)
        result = fd.ac.fill_lock(str(self.root), self.manifest, self.before, selected_keys=set())
        result["entries"]["private-input@1"]["extension"].append("different")
        self.assertEqual(self.before, original)

    def test_explicit_bulk_fill_still_refreshes_all(self):
        fd.refresh_lock(str(self.root), self.manifest)
        after = fd.ac.load_lock(str(self.root))
        self.assertNotIn("absent-artifact@1", after["entries"])
        self.assertIsNone(after["entries"]["private-input@1"]["ingredients"][0]["sha256"])
        self.assertNotEqual(after["entries"]["changed-input@1"], self.before["entries"]["changed-input@1"])


if __name__ == "__main__":
    unittest.main()
