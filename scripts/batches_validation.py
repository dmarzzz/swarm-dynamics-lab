"""Validate batch completion against local entries or fetched main blobs."""
from pathlib import Path
import subprocess
import tempfile

import lab


def validate_entries(root, entries, issue):
    labels = {item["name"] for item in issue["labels"]}
    sources = [name.split(":", 1)[1] for name in labels if name.startswith("source:")]
    topics = {name.split(":", 1)[1] for name in labels if name.startswith("topic:")}
    kinds = {"x": "thread", "web": "blog", "blog": "blog", "paper": "paper",
             "code": "code", "talk": "talk"}
    if len(sources) != 1 or sources[0] not in kinds or not topics:
        raise ValueError("batch must have one supported source label and a topic label")
    kind = kinds[sources[0]]
    folder = lab.LIB_KIND_DIR[kind]
    contents = []
    for entry in entries:
        path = Path(entry)
        if (path.is_absolute() or path.parts[:2] != (lab.LIBRARY, folder)
                or len(path.parts) != 3 or path.suffix != ".md"
                or not lab.ID_RE.fullmatch(path.stem)):
            raise ValueError(f"not a {kind} library entry under {lab.LIBRARY}/{folder}/: {entry}")
        local = root / path
        if local.exists() or local.is_symlink():
            if not local.is_file() or local.is_symlink() or local.resolve() != root.resolve() / path:
                raise ValueError(f"not a regular in-repository entry: {entry}")
            content = local.read_text(encoding="utf-8")
        else:
            # ls-tree mode rejects trees and symlinks, which cat-file -e accepts.
            tree = subprocess.run(["git", "ls-tree", "origin/main", "--", path.as_posix()],
                                  cwd=root, capture_output=True, text=True, check=True).stdout
            if not tree.startswith(("100644 blob ", "100755 blob ")):
                raise ValueError(f"regular entry not found locally or on origin/main: {entry}")
            content = subprocess.run(["git", "show", f"origin/main:{path.as_posix()}"],
                                     cwd=root, capture_output=True, text=True, check=True).stdout
        contents.append((path, content))

    inventory = lab.Lab()
    # Doc uses ROOT-relative paths. Stage only supplied text in a temporary,
    # ignored directory, then give each parsed document its canonical path.
    data = root / "data"
    data.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="batch-validation-", dir=data) as temp:
        for path, content in contents:
            staged = Path(temp) / path
            staged.parent.mkdir(parents=True, exist_ok=True)
            staged.write_text(content, encoding="utf-8")
            doc = lab.Doc(staged)
            doc.path, doc.rel = root / path, path.as_posix()
            if doc.error or doc.get("type") != kind or not topics.issubset(set(doc.get("topics") or [])):
                raise ValueError(f"invalid frontmatter/type or missing batch topic: {path}")
            previous = inventory.library.get(path.stem)
            if previous and previous.rel != doc.rel:
                raise ValueError(f"entry id already exists in another folder: {path.stem}")
            inventory.library[path.stem] = doc
        errors, _ = lab.check(inventory)
    if errors:
        raise ValueError("lab.py check failed:\n" + "\n".join(errors))
