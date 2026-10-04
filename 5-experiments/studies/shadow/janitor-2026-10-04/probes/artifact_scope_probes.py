"""J041: reproduce unrelated provenance mutation only in a temporary fixture.

Run from any cwd. No real manifest/lock/attestation or network access is used.
Output describes pre-fix behavior; a corrected implementation should preserve
all historical lock entries and statements while adding only new-figure@1.
"""
import importlib.util
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[5]
spec = importlib.util.spec_from_file_location("janitor_fd", ROOT / ".flightdeck/fd.py")
fd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fd)


def run():
    with tempfile.TemporaryDirectory(prefix="janitor-j041-") as tmp:
        root = Path(tmp)
        (root / "project.yaml").write_text("name: fixture\n")
        artifacts = []
        for aid in ("private-input", "changed-input", "absent-artifact"):
            rel = f"artifacts/{aid}/{aid}-v1.md"
            target = root / rel
            target.parent.mkdir(parents=True)
            target.write_text(f"Synthetic existing artifact {aid}\n")
            ing = root / f"{aid}.txt"
            ing.write_text("Original ingredient\n")
            artifacts.append({"id": aid, "category": "content", "type": "doc", "title": aid,
                              "versions": [{"v": 1, "date": "2026-10-04", "path": rel,
                                            "ingredients": [ing.name], "by": "codex"}]})
        manifest = {"manifest": 1, "project": "fixture", "artifacts": artifacts}
        fd.write_yaml(str(root / "artifacts.yaml"), manifest)
        with patch.object(fd, "git_remote_url", return_value=None):
            fd.refresh_lock(str(root), manifest)
            before_lock = fd.ac.load_lock(str(root))
            before_statements = {p.name: p.read_bytes() for p in (root / "attestations").glob("*.intoto.json")}
            (root / "private-input.txt").unlink()
            (root / "changed-input.txt").write_text("An unrelated new ingredient, not the historical source\n")
            (root / "artifacts/absent-artifact/absent-artifact-v1.md").unlink()
            source = root / "figure.svg"
            source.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900"/>')
            with patch.object(fd, "session_from_env", return_value={}), \
                    patch.object(fd, "model_of", return_value=None), \
                    patch.object(fd, "git_commit", return_value=None):
                fd.main(["add", str(source), "--id", "new-figure", "--type", "figure",
                         "--title", "Synthetic new figure", "--ingredient", "changed-input.txt",
                         "--by", "codex", "--copy", "--folder", str(root)])
        after_lock = fd.ac.load_lock(str(root))
        old_entries = before_lock["entries"]
        new_entries = after_lock["entries"]
        changed = sorted(k for k, v in old_entries.items() if k in new_entries and v != new_entries[k])
        removed = sorted(set(old_entries) - set(new_entries))
        statement_changes = sorted(name for name, content in before_statements.items()
                                   if (root / "attestations" / name).read_bytes() != content)
        results = {
            "fixture_only": True,
            "new_entry_present": "new-figure@1" in new_entries,
            "unrelated_lock_entries_changed": changed,
            "unrelated_lock_entries_removed": removed,
            "unrelated_statements_rewritten": statement_changes,
            "private_ingredient_digest_before": old_entries["private-input@1"]["ingredients"][0]["sha256"],
            "private_ingredient_digest_after": new_entries["private-input@1"]["ingredients"][0]["sha256"],
            "historical_dependency_digest_recomputed": old_entries["changed-input@1"]["ingredients"][0]["sha256"] != new_entries["changed-input@1"]["ingredients"][0]["sha256"],
        }
        print(json.dumps(results, indent=2))
        return results


if __name__ == "__main__":
    run()
