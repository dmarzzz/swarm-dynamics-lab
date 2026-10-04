"""Streaming adapters. Unknown identities/times stay None; source text is untrusted data."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import csv
import gzip
import json
import re
import subprocess
from typing import Iterator


@dataclass
class Event:
    agent_id: str | None
    time: float | None
    text: str
    thread: str | None = None
    event_id: str = ""
    kind: str = "record"
    metadata: dict = field(default_factory=dict)


def parse_time(value) -> float | None:
    """ISO-8601 with explicit timezone or finite Unix seconds; never guess a timezone."""
    import math
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value) if math.isfinite(value) else None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return dt.timestamp() if dt.tzinfo else None
    except (ValueError, OverflowError):
        return None


def iso_time(value):
    return datetime.fromtimestamp(value, timezone.utc).isoformat() if value is not None else None


def open_text(path):
    path = Path(path)
    return gzip.open(path, "rt", encoding="utf-8") if path.suffix == ".gz" else path.open(encoding="utf-8")


def json_rows(path):
    with open_text(path) as stream:
        for number, line in enumerate(stream, 1):
            if line.strip():
                try:
                    row = json.loads(line)
                    if not isinstance(row, dict):
                        raise ValueError("expected object")
                    yield row
                except (ValueError, TypeError) as exc:
                    raise ValueError(f"Invalid JSON object at line {number}") from exc


def identity(value):
    if value is None:
        return None
    value = str(value).strip()
    return value or None


def table(path) -> Iterator[Event]:
    """CSV/CSV.gz or JSONL/JSONL.gz, required agent_id/time/text keys (nullable)."""
    with open_text(path) as stream:
        is_csv = str(path).removesuffix(".gz").endswith(".csv")
        rows = csv.DictReader(stream) if is_csv else (json.loads(l) for l in stream if l.strip())
        for number, row in enumerate(rows, 1):
            if not all(key in row for key in ("agent_id", "time", "text")):
                raise ValueError(f"Row {number} requires agent_id, time, text")
            yield Event(identity(row["agent_id"]), parse_time(row["time"]), str(row["text"] or ""),
                        identity(row.get("thread")), str(row.get("event_id", number)), str(row.get("kind", "record")))


def wiki(path, identity_field="label") -> Iterator[Event]:
    """Revision snapshots. Optional ip16 mode is a network-block proxy, NOT an agent."""
    path = Path(path)
    if path.is_dir():
        path /= "revisions.jsonl.gz"
    if identity_field not in ("label", "ip16"):
        raise ValueError("wiki identity_field must be label or ip16")
    for row in json_rows(path):
        yield Event(identity(row.get(identity_field)), parse_time(row.get("time")), str(row.get("body") or ""),
                    identity(row.get("page_id")), str(row.get("rev_id", "")), "revision",
                    {"identity_basis": identity_field, "time_grade": row.get("time_grade"),
                     "uncertainty_seconds": row.get("uncertainty_seconds"), "seq": row.get("seq")})


def swarmtraces(path) -> Iterator[Event]:
    """No extraction of claimed names, dates, or commands from hostile payload text."""
    path = Path(path)
    if path.is_dir():
        path /= "redacted.jsonl.gz"
    for row in json_rows(path):
        yield Event(identity(row.get("agent_id")), parse_time(row.get("time_utc")), str(row.get("text") or ""),
                    identity(row.get("parent_id")), str(row.get("id", "")), str(row.get("kind", "artifact")),
                    {"identity_basis": "explicit_top_level_agent_id_only"})


AGENT = re.compile(r"^\[([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)\]\s*")
TASK = re.compile(r"^task:\s*(claim|done|release|touch)\s+(\S+)", re.I)


def git_log(repo, ref="HEAD") -> Iterator[Event]:
    """Non-merge commits, author clock. Agent prefix, not git author or co-author identity."""
    # Resolve first, preventing a user ref from being interpreted as a git option.
    resolved = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "--verify", "--end-of-options", ref + "^{commit}"], text=True).strip()
    raw = subprocess.check_output(["git", "-C", str(repo), "log", resolved, "--no-merges",
                                   "--format=%H%x00%aI%x00%s%x00"], text=True)
    chunks = raw.split("\0")
    for i in range(0, len(chunks) - 2, 3):
        commit, timestamp, subject = chunks[i].strip(), chunks[i + 1], chunks[i + 2]
        match = AGENT.match(subject)
        actor = match[1] if match else None
        text = subject[match.end():] if match else subject
        task = TASK.match(text)
        yield Event(actor, parse_time(timestamp), text, task[2] if task else None, commit,
                    "task_" + task[1].lower() if task else "commit", {"identity_basis": "bracketed_agent_prefix"})


def task_events(repo, ref="HEAD") -> Iterator[Event]:
    """Claim/done/release/touch events observed in task command commit subjects.

    This is a subset of git_log, not an independent source of extra participation.
    Bulk task edits and nonstandard subjects are not reconstructed.
    """
    yield from (event for event in git_log(repo, ref) if event.kind.startswith("task_"))
