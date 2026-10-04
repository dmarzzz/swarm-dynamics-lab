#!/usr/bin/env python3
"""Validate and render editorial evidence metadata; never launch or modify experiments."""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import sys

REGISTRY = "experiments/evidence-metadata.json"
RUBRIC = "experiments/EVIDENCE-METADATA.md"
INDEX = "experiments/EVIDENCE.md"
START, END = "<!-- experiment-evidence:start -->", "<!-- experiment-evidence:end -->"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def repo_file(root, value):
    require(isinstance(value, str) and bool(value), "expected a repository file path")
    path = PurePosixPath(value)
    require(not path.is_absolute() and ".." not in path.parts and "\\" not in value
            and path.as_posix() == value, f"unsafe repository path: {value}")
    target = root / value
    require(target.resolve().is_relative_to(root.resolve()) and target.is_file(),
            f"missing or external repository file: {value}")
    return target


def text(value):
    return isinstance(value, str) and bool(value.strip()) and START not in value and END not in value


def validate(root, data):
    require(isinstance(data, dict) and type(data.get("schema_version")) is int
            and data["schema_version"] == 1, "unsupported schema_version")
    require(text(data.get("assessed_at")), "missing assessed_at")
    require(date.fromisoformat(data["assessed_at"]).isoformat() == data["assessed_at"], "invalid assessed_at")
    require(text(data.get("assessor")), "missing assessor")
    require(isinstance(data.get("source_commit"), str)
            and re.fullmatch(r"[0-9a-f]{40}", data["source_commit"]), "invalid source_commit")
    repo_file(root, RUBRIC)
    require(isinstance(data.get("studies"), list) and data["studies"], "studies must be nonempty")
    ids, registrations, documents = set(), set(), set()
    for row in data["studies"]:
        require(isinstance(row, dict), "study must be an object")
        ident = row.get("id")
        require(isinstance(ident, str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", ident), "invalid study id")
        require(ident not in ids, f"duplicate study id: {ident}")
        ids.add(ident)
        for field in ("title", "sample_size_summary"):
            require(text(row.get(field)), f"{ident}: missing {field}")
        require(len(row["sample_size_summary"]) <= 500, f"{ident}: sample_size_summary exceeds 500 characters")
        if "source_commit" in row:
            require(isinstance(row["source_commit"], str) and re.fullmatch(r"[0-9a-f]{40}", row["source_commit"]),
                    f"{ident}: invalid source_commit")
        if "assessor" in row:
            require(text(row["assessor"]), f"{ident}: invalid assessor")
        if "assessed_at" in row:
            require(text(row["assessed_at"]), f"{ident}: invalid assessed_at")
            require(date.fromisoformat(row["assessed_at"]).isoformat() == row["assessed_at"],
                    f"{ident}: invalid assessed_at")
        for field in ("documents", "registration_paths", "sources", "experiment_ids"):
            values = row.get(field)
            require(isinstance(values, list) and all(text(x) for x in values)
                    and len(values) == len(set(values)), f"{ident}: invalid {field}")
            if field != "experiment_ids":
                for value in values:
                    repo_file(root, value)
        require(row["documents"] and row["sources"], f"{ident}: documents and sources must be nonempty")
        require(all(p.endswith(".md") for p in row["documents"]), f"{ident}: documents must be Markdown")
        require(all(PurePosixPath(p).name in {"experiment.yaml", "experiment.json"}
                    for p in row["registration_paths"]), f"{ident}: invalid registration filename")
        confidence = row.get("evidence_confidence")
        require(isinstance(confidence, dict), f"{ident}: missing evidence_confidence")
        require("score" in confidence and (confidence["score"] is None
                or type(confidence["score"]) is int and 0 <= confidence["score"] <= 4), f"{ident}: invalid score")
        require(all(text(confidence.get(k)) for k in ("claim", "rationale")), f"{ident}: missing confidence scope or rationale")
        registrations.update(row["registration_paths"])
        documents.update(row["documents"])
    discovered = {p.relative_to(root).as_posix() for pattern in ("experiment.yaml", "experiment.json")
                  for p in root.glob(f"researchers/*/notes/**/{pattern}")
                  if not any(part.startswith("pi-review-") for part in p.parts)}
    missing = sorted(discovered - registrations)
    require(not missing, "uncovered experiment registrations: " + ", ".join(missing))
    formal = {p.relative_to(root).as_posix() for p in root.glob("experiments/*/README.md")}
    require(not formal - documents, "uncovered formal experiments: " + ", ".join(sorted(formal - documents)))


def score_label(row):
    score = row["evidence_confidence"]["score"]
    return "unassessed" if score is None else f"{score}/4"


def relative(document, target):
    return posixpath.relpath(target, posixpath.dirname(document))


def block(document, rows, data):
    commits = {row.get("source_commit", data["source_commit"]) for row in rows}
    assessments = {(row.get("assessed_at", data["assessed_at"]),
                    row.get("assessor", data["assessor"])) for row in rows}
    if len(assessments) == 1:
        assessed_at, assessor = next(iter(assessments))
        assessment_note = f"Assessed {assessed_at} by {assessor}"
    else:
        assessment_note = "Assessment dates and assessors shown per cohort"
    source_note = (f"source `{next(iter(commits))[:8]}`" if len(commits) == 1
                   else "source snapshots shown per cohort")
    lines = [START, "## Evidence metadata", "",
             f"{assessment_note}; {source_note} "
             f"([registry]({relative(document, REGISTRY)}), [rubric]({relative(document, RUBRIC)})). "
             "Scores describe evidence for the stated claim, not a probability of truth."]
    for row in rows:
        confidence = row["evidence_confidence"]
        if len(rows) > 1:
            lines += ["", f"**{row['title']}** (`{row['id']}`)"]
        if len(commits) > 1:
            lines += [f"Source: `{row.get('source_commit', data['source_commit'])[:8]}`."]
        if len(assessments) > 1:
            lines += [f"Assessed {row.get('assessed_at', data['assessed_at'])} "
                      f"by {row.get('assessor', data['assessor'])}."]
        lines += ["", f"- **evidence_confidence:** **{score_label(row)}** — {confidence['claim']} "
                  f"Basis: {confidence['rationale']}",
                  f"- **sample_size_summary:** {row['sample_size_summary']}"]
    return "\n".join(lines + [END])


def update_document(original, rendered):
    newline = "\r\n" if "\r\n" in original else "\n"
    rendered = rendered.replace("\n", newline)
    require(original.count(START) == original.count(END) <= 1, "malformed or duplicate evidence block")
    if START in original:
        first, last = original.index(START), original.index(END)
        require(first < last, "reversed evidence block markers")
        return original[:first] + rendered + original[last + len(END):]
    offset = 0
    if re.match(r"\A---\r?\n", original):
        end = re.search(r"(?m)^(?:---|\.\.\.)[ \t]*\r?$", original[4:])
        require(end is not None, "unclosed YAML frontmatter")
        offset = 4 + end.end()
    heading = re.search(r"(?m)^# [^\r\n]*(?:\r?\n|$)", original[offset:])
    # lab.py's formal experiment template puts the title in YAML, without an H1.
    at = offset + heading.end() if heading else offset
    prefix = "" if original[:at].endswith("\n") else newline
    return original[:at] + prefix + newline + rendered + newline + original[at:]


def index_text(data):
    def cell(value):
        return str(value).replace("|", "\\|").replace("\n", " ")
    lines = ["# Experiment evidence index", "", f"Registry initiated {data['assessed_at']} by {data['assessor']}. "
             "Current cohort assessors and dates are shown in the linked study documents.", "",
             f"[Rubric](EVIDENCE-METADATA.md) · [Machine-readable registry](evidence-metadata.json)", "",
             f"Source snapshot: `{data['source_commit']}`; individual rows may pin another source commit. "
             "Scores are scoped editorial assessments, not probabilities or launch approval. "
             "Repeated calls, agents and treatment outcomes are not automatically independent samples.", "",
             "| Study / cohort | Evidence confidence | Sample size |",
             "| --- | --- | --- |"]
    for row in data["studies"]:
        lines.append(f"| [{cell(row['title'])}]({relative(INDEX, row['documents'][0])}) (`{row['id']}`) "
                     f"| {score_label(row)} | {cell(row['sample_size_summary'])} |")
    return "\n".join(lines) + "\n"


def outputs(root, data):
    validate(root, data)
    by_document = defaultdict(list)
    for row in data["studies"]:
        for document in row["documents"]:
            by_document[document].append(row)
    result = {}
    for document, rows in sorted(by_document.items()):
        original = (root / document).read_bytes().decode("utf-8")
        try:
            result[document] = update_document(original, block(document, rows, data))
        except ValueError as error:
            raise ValueError(f"{document}: {error}") from error
    result[INDEX] = index_text(data)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="validate and check rendered metadata (default)")
    mode.add_argument("--write", action="store_true", help="refresh only metadata blocks and the evidence index")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--registry", default=REGISTRY)
    args = parser.parse_args(argv)
    try:
        data = json.loads(repo_file(args.root, args.registry).read_text(encoding="utf-8"))
        rendered = outputs(args.root, data)
        stale = [path for path, content in rendered.items() if not (args.root / path).exists()
                 or (args.root / path).read_bytes() != content.encode("utf-8")]
        if args.write:
            for path in stale:
                (args.root / path).write_bytes(rendered[path].encode("utf-8"))
        elif stale:
            raise ValueError("stale evidence metadata; run --write: " + ", ".join(stale))
        print(f"Evidence metadata: {len(data['studies'])} cohorts, {len(rendered) - 1} documents; "
              + (f"updated {len(stale)} files" if args.write else "valid and current"))
        return 0
    except (ValueError, OSError) as error:
        print(f"Evidence metadata error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
