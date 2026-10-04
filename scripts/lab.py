#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""lab.py: the swarm-lab tool. Validates the repo, enforces the prior-art gate, scaffolds entries,
claims tasks atomically through git, and rebuilds STATUS.md and library/INDEX.md.

  python3 scripts/lab.py check [--urls]            validate everything (run before every push)
  python3 scripts/lab.py index                     rebuild STATUS.md and library/INDEX.md (CI does this)
  python3 scripts/lab.py find <text>               search the library by id, title, url, doi, arxiv
  python3 scripts/lab.py new <kind> <id> --agent A scaffold an entry from templates/ (kinds below)
  python3 scripts/lab.py claim <task> --agent A    claim an open or stale task (pulls, commits, pushes)
  python3 scripts/lab.py touch <task> --agent A    heartbeat on a task you hold
  python3 scripts/lab.py done <task> --agent A [--output path ...]
  python3 scripts/lab.py release <task> --agent A [--note "why"]
  python3 scripts/lab.py sync --agent A [--every 600]   commit and push every changed file that passes the check
  python3 scripts/lab.py add-researcher <name>
  python3 scripts/lab.py gate <survey-id>          show exactly what a survey still needs to pass the gate
  python3 scripts/lab.py verify [--agent A]        check paper titles against arXiv and Crossref (catches phantom citations)

Kinds for `new`: paper blog thread code dataset talk survey hypothesis experiment review task agent.
Needs PyYAML (`pip install pyyaml`, or run with `uv run scripts/lab.py ...`).
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("lab.py needs PyYAML: pip install pyyaml   (or: uv run scripts/lab.py ...)")

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------------------------------------------
# The prior-art gate. These floors are the quality bar. Raise them if surveys come in thin; lower them only by
# team agreement, in a commit that says why.
GATE = {
    "min_cited": 20,          # distinct library entries cited in the survey body
    "min_papers": 10,
    "min_code": 3,
    "min_informal": 2,        # blog + thread + talk
    "min_recent": 3,          # entries from the last `recent_years` years
    "recent_years": 2,
    "min_full_reads": 5,      # cited papers with read_depth: full
    "min_seminal": 3,         # frontmatter `seminal:` ids, each cited
    "min_search_rounds": 8,
    "saturation_rounds": 2,   # the last N search rounds must each be below...
    "saturation_max_new": 0.15,  # ...this fraction of new (not already in library) results
}
# Every survey's search log must touch each of these groups at least once.
SEARCH_GROUPS = {
    "scholarly index": {"semantic-scholar", "google-scholar", "openalex", "dblp", "pubmed"},
    "preprints": {"arxiv", "biorxiv", "openreview"},
    "code": {"github", "papers-with-code", "huggingface"},
    "social": {"x", "bluesky", "hn", "reddit", "lesswrong"},
    "web": {"web", "youtube"},
    "backward citations": {"citations-backward"},
    "forward citations": {"citations-forward"},
}
SEARCH_WHERE = set().union(*SEARCH_GROUPS.values())
SURVEY_SECTIONS = ["Scope", "Search log", "Landscape", "What is known", "Open problems and disagreements",
                   "Code, data and tools", "Gaps", "Saturation"]
HYPOTHESIS_SECTIONS = ["Claim", "Grounding", "Novelty", "Prediction", "Minimal experiment", "Kill criteria"]
EXPERIMENT_SECTIONS = ["Setup", "Protocol", "Metrics", "Results", "Analysis"]
CLAIM_TTL_HOURS = 3
# ---------------------------------------------------------------------------------------------------------------

LIB_DIRS = {"papers": "paper", "blogs": "blog", "threads": "thread", "code": "code", "datasets": "dataset",
            "talks": "talk"}
LIB_KIND_DIR = {v: k for k, v in LIB_DIRS.items()}
READ_DEPTHS = {"abstract", "skim", "full", "ran"}
INFORMAL = {"blog", "thread", "talk"}
TASK_KINDS = {"scan", "survey", "synthesis", "review", "build", "experiment", "admin", "question"}
TASK_STATUS = {"open", "claimed", "done", "blocked"}
SURVEY_STATUS = {"in-progress", "complete"}
HYP_STATUS = {"draft", "proposed", "accepted", "testing", "supported", "refuted", "parked", "rejected"}
HYP_NEEDS_REVIEW = {"accepted", "testing", "supported", "refuted"}
EXP_STATUS = {"planned", "running", "done", "abandoned"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
AGENT_RE = re.compile(r"^([a-z0-9_-]+)/([a-z0-9_.-]+)$")
CITE_RE = re.compile(r"\[\[([a-z0-9][a-z0-9-]*)\]\]")


def today() -> str:
    return dt.date.today().isoformat()


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def parse_time(s) -> dt.datetime | None:
    if not s:
        return None
    s = str(s).strip().replace("Z", "+00:00")
    for fmt in (None,):
        try:
            t = dt.datetime.fromisoformat(s)
            return t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)
        except ValueError:
            pass
    return None


# ------------------------------------------------------------------------------------------------ documents
class Doc:
    def __init__(self, path: Path):
        self.path = path
        self.rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        self.fm: dict = {}
        self.body = text
        self.error = None
        if text.startswith("---\n"):
            end = text.find("\n---", 4)
            if end == -1:
                self.error = "frontmatter opened with --- but never closed"
            else:
                try:
                    self.fm = yaml.safe_load(text[4:end]) or {}
                    if not isinstance(self.fm, dict):
                        raise ValueError("frontmatter is not a mapping")
                except Exception as e:  # noqa: BLE001
                    self.error = f"frontmatter is not valid YAML: {e}"
                    self.fm = {}
                self.body = text[end + 4:].lstrip("\n")
        else:
            self.error = "missing YAML frontmatter (file must start with ---)"

    def get(self, k, default=None):
        return self.fm.get(k, default)

    def sections(self) -> dict[str, str]:
        out, cur, buf = {}, None, []
        for line in self.body.splitlines():
            m = re.match(r"^##\s+(.+?)\s*$", line)
            if m:
                if cur is not None:
                    out[cur] = "\n".join(buf).strip()
                cur, buf = m.group(1), []
            elif cur is not None:
                buf.append(line)
        if cur is not None:
            out[cur] = "\n".join(buf).strip()
        return out

    def cites(self) -> list[str]:
        return list(dict.fromkeys(CITE_RE.findall(self.body)))

    def write(self):
        fm = yaml.safe_dump(self.fm, sort_keys=False, allow_unicode=True, width=1000)
        self.path.write_text(f"---\n{fm}---\n\n{self.body.rstrip()}\n", encoding="utf-8")


def md_files(d: Path, pattern="*.md"):
    return sorted(p for p in d.glob(pattern) if p.name not in {"README.md", "INDEX.md"})


class Lab:
    def __init__(self):
        self.researchers = sorted(p.name for p in (ROOT / "researchers").iterdir()
                                  if p.is_dir() and (p / "README.md").exists())
        self.topics = {t["slug"]: t for t in (yaml.safe_load((ROOT / "library/topics.yaml").read_text()) or [])}
        self.library: dict[str, Doc] = {}
        self.lib_dupes: list[tuple[str, Doc]] = []
        for d in LIB_DIRS:
            for p in md_files(ROOT / "library" / d):
                doc = Doc(p)
                if p.stem in self.library:
                    self.lib_dupes.append((p.stem, doc))
                self.library[p.stem] = doc
        self.surveys = {p.stem: Doc(p) for p in md_files(ROOT / "surveys")}
        self.hypotheses = {p.stem: Doc(p) for p in md_files(ROOT / "hypotheses")}
        self.experiments = {p.parent.name: Doc(p) for p in sorted((ROOT / "experiments").glob("*/README.md"))}
        self.reviews = {p.stem: Doc(p) for p in md_files(ROOT / "reviews")}
        self.tasks = {p.stem: Doc(p) for p in md_files(ROOT / "tasks")}
        self.agents = {f"{p.parent.parent.name}/{p.stem}": Doc(p)
                       for p in sorted((ROOT / "researchers").glob("*/agents/*.md"))}

    # ------------------------------------------------------------------ derived state
    def passing_reviews(self, target: str, owner_researcher: str | None) -> list[Doc]:
        out = []
        for r in self.reviews.values():
            if r.get("target") != target or r.get("verdict") != "pass":
                continue
            m = AGENT_RE.match(str(r.get("reviewer", "")))
            if m and m.group(1) != owner_researcher:
                out.append(r)
        return out

    def survey_state(self, sid: str) -> str:
        s = self.surveys.get(sid)
        if not s:
            return "missing"
        if s.get("status") != "complete" or self.gate_problems(s):
            return "in-progress"
        return "reviewed" if self.passing_reviews(sid, s.get("owner")) else "complete"

    def gate_problems(self, s: Doc) -> list[str]:
        """Everything a survey still lacks before it may be marked complete."""
        g, probs = GATE, []
        secs = s.sections()
        for name in SURVEY_SECTIONS:
            if not secs.get(name):
                probs.append(f"section '## {name}' is missing or empty")
        if "TODO" in s.body:
            probs.append("body still contains TODO")
        cites = s.cites()
        known = [c for c in cites if c in self.library]
        unknown = [c for c in cites if c not in self.library]
        if unknown:
            probs.append(f"cites ids not in library/: {', '.join(unknown)}")
        types = [self.library[c].get("type") for c in known]
        cnt = lambda pred: sum(1 for t in types if pred(t))  # noqa: E731
        checks = [
            (len(known), g["min_cited"], "distinct library entries cited"),
            (cnt(lambda t: t == "paper"), g["min_papers"], "papers cited"),
            (cnt(lambda t: t == "code"), g["min_code"], "code repos cited"),
            (cnt(lambda t: t in INFORMAL), g["min_informal"], "blogs/threads/talks cited"),
        ]
        cutoff = dt.date.today().year - g["recent_years"]
        recent = sum(1 for c in known if _int(self.library[c].get("year")) >= cutoff)
        checks.append((recent, g["min_recent"], f"entries from {cutoff} or later cited"))
        full = sum(1 for c in known if self.library[c].get("type") == "paper"
                   and self.library[c].get("read_depth") == "full")
        checks.append((full, g["min_full_reads"], "cited papers with read_depth: full"))
        for have, need, what in checks:
            if have < need:
                probs.append(f"{what}: {have}/{need}")
        seminal = s.get("seminal") or []
        if len(seminal) < g["min_seminal"]:
            probs.append(f"frontmatter seminal: {len(seminal)}/{g['min_seminal']} ids")
        for sid in seminal:
            if sid not in cites:
                probs.append(f"seminal id '{sid}' is not cited in the body")
        log = s.get("search_log") or []
        if len(log) < g["min_search_rounds"]:
            probs.append(f"search_log rounds: {len(log)}/{g['min_search_rounds']}")
        wheres = set()
        for i, row in enumerate(log):
            if not isinstance(row, dict):
                probs.append(f"search_log[{i}] must be a mapping")
                continue
            for k in ("where", "query", "date", "results", "new"):
                if row.get(k) in (None, ""):
                    probs.append(f"search_log[{i}] missing '{k}'")
            w = row.get("where")
            if w and w not in SEARCH_WHERE:
                probs.append(f"search_log[{i}] where '{w}' not one of {sorted(SEARCH_WHERE)}")
            wheres.add(w)
        for group, members in SEARCH_GROUPS.items():
            if not wheres & members:
                probs.append(f"search_log never covers {group} ({'/'.join(sorted(members))})")
        tail = [r for r in log if isinstance(r, dict)][-g["saturation_rounds"]:]
        if len(tail) == g["saturation_rounds"]:
            for r in tail:
                res, new = _int(r.get("results")), _int(r.get("new"))
                if res <= 0 or new / res > g["saturation_max_new"]:
                    probs.append(f"not saturated: last {g['saturation_rounds']} rounds must each have "
                                 f"new/results <= {g['saturation_max_new']} (round '{r.get('query')}' "
                                 f"has {new}/{res}); keep searching")
                    break
        return probs


def _int(v, default=0) -> int:
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def norm_url(u: str) -> str:
    u = str(u).strip().lower()
    m = re.search(r"arxiv\.org/(?:abs|pdf|html)/([0-9]{4}\.[0-9]{4,5}|[a-z\-]+/[0-9]{7})", u)
    if m:
        return "arxiv:" + m.group(1)
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^(www\.|mobile\.)", "", u)
    u = u.replace("twitter.com/", "x.com/")
    u = re.sub(r"#.*$", "", u)
    if "?" in u:  # keep identifying query params (plos ?id=, youtube ?v=), drop tracking ones
        base, q = u.split("?", 1)
        keep = [kv for kv in q.split("&") if kv and not kv.startswith(("utm_", "ref=", "s=", "t=", "fbclid"))]
        u = base + ("?" + "&".join(keep) if keep else "")
    return u.rstrip("/")


# ------------------------------------------------------------------------------------------------ check
def check(lab: Lab, urls=False) -> tuple[list[str], list[str]]:
    E, W = [], []
    err = lambda d, m: E.append(f"{d.rel}: {m}")  # noqa: E731
    warn = lambda d, m: W.append(f"{d.rel}: {m}")  # noqa: E731

    def agent_ok(d, field, value, required=True):
        if not value:
            if required:
                err(d, f"'{field}' is required")
            return
        m = AGENT_RE.match(str(value))
        if not m:
            err(d, f"'{field}' must look like <researcher>/<agent>, got '{value}'")
        elif m.group(1) not in lab.researchers:
            err(d, f"'{field}' names unknown researcher '{m.group(1)}' (known: {', '.join(lab.researchers)})")

    def common(d, kind, stem):
        if d.error:
            err(d, d.error)
            return False
        if d.get("id") != stem:
            err(d, f"id '{d.get('id')}' must equal the filename stem '{stem}'")
        if not ID_RE.match(stem):
            err(d, "filename must be lowercase a-z, 0-9 and hyphens")
        if d.get("type") != kind:
            err(d, f"type must be '{kind}', got '{d.get('type')}'")
        return True

    def topics_ok(d):
        for t in d.get("topics") or []:
            if t not in lab.topics:
                err(d, f"unknown topic '{t}': add it to library/topics.yaml first")

    # ---- library
    for stem, d in lab.lib_dupes:
        err(d, f"id '{stem}' exists in two library folders")
    seen_keys: dict[str, str] = {}
    all_ids: dict[str, str] = {}
    for stem, d in lab.library.items():
        kind = LIB_DIRS[d.path.parent.name]
        all_ids[stem] = d.rel
        if not common(d, kind, stem):
            continue
        for f in ("title", "url", "topics", "added_by", "accessed", "read_depth", "relevance", "year"):
            if d.get(f) in (None, "", []):
                err(d, f"'{f}' is required")
        if kind in {"paper", "talk", "blog"} and not d.get("authors"):
            err(d, "'authors' is required")
        if kind == "paper" and len(str(d.get("cite") or "")) < 40:
            err(d, "'cite' (full formatted reference: authors, year, title, venue, volume/pages) is required for papers")
        if kind == "thread" and not d.get("author_handle"):
            err(d, "'author_handle' is required for threads")
        if kind == "code" and not d.get("repo"):
            err(d, "'repo' (owner/name) is required for code")
        url = str(d.get("url") or "")
        if url and not url.startswith(("http://", "https://")):
            err(d, "url must be http(s)")
        rd = d.get("read_depth")
        if rd and rd not in READ_DEPTHS:
            err(d, f"read_depth must be one of {sorted(READ_DEPTHS)}")
        if rd == "ran" and kind not in {"code", "dataset"}:
            err(d, "read_depth 'ran' is only for code and datasets")
        rel = _int(d.get("relevance"), -1)
        if d.get("relevance") is not None and not 1 <= rel <= 5:
            err(d, "relevance must be 1-5")
        agent_ok(d, "added_by", d.get("added_by"))
        topics_ok(d)
        if "TODO" in d.body or "TODO" in yaml.safe_dump(d.fm):
            err(d, "still contains TODO: fill it in or delete the entry")
        if not d.sections().get("Summary") or len(d.sections().get("Summary", "").split()) < 25:
            err(d, "'## Summary' needs at least 25 words in your own words")
        keys = [norm_url(url)] if url else []
        if d.get("doi"):
            keys.append("doi:" + str(d.get("doi")).lower().strip())
        if d.get("arxiv"):
            keys.append("arxiv:" + re.sub(r"v\d+$", "", str(d.get("arxiv")).lower().strip()))
        if kind == "code" and d.get("repo"):
            keys.append("repo:" + str(d.get("repo")).lower())
        for k in keys:
            if k in seen_keys and seen_keys[k] != stem:
                err(d, f"duplicate of '{seen_keys[k]}' (same {k}); add notes to that entry instead")
            seen_keys.setdefault(k, stem)
        for c in d.cites():
            if c not in lab.library:
                warn(d, f"links [[{c}]] which is not in the library yet")

    # ---- surveys
    for stem, d in lab.surveys.items():
        if not common(d, "survey", stem):
            continue
        if d.get("owner") not in lab.researchers:
            err(d, f"owner must be a researcher name, got '{d.get('owner')}'")
        if d.get("status") not in SURVEY_STATUS:
            err(d, f"status must be one of {sorted(SURVEY_STATUS)}")
        topics_ok(d)
        if not d.get("questions"):
            err(d, "'questions' (what this survey answers) is required")
        if d.get("status") == "complete":
            for p in lab.gate_problems(d):
                err(d, f"marked complete but fails the prior-art gate: {p}")
        else:
            for c in d.cites():
                if c not in lab.library:
                    warn(d, f"cites [[{c}]] which is not in the library yet")

    # ---- reviews
    for stem, d in lab.reviews.items():
        if not common(d, "review", stem):
            continue
        agent_ok(d, "reviewer", d.get("reviewer"))
        tgt = d.get("target")
        owner = None
        if tgt in lab.surveys:
            owner = lab.surveys[tgt].get("owner")
        elif tgt in lab.hypotheses:
            owner = lab.hypotheses[tgt].get("owner")
        elif tgt in lab.experiments:
            owner = lab.experiments[tgt].get("owner")
        else:
            err(d, f"target '{tgt}' is not a survey, hypothesis or experiment id")
        if d.get("verdict") not in {"pass", "revise"}:
            err(d, "verdict must be 'pass' or 'revise'")
        m = AGENT_RE.match(str(d.get("reviewer", "")))
        if m and owner and m.group(1) == owner:
            err(d, "a review must come from a different researcher's agent than the target's owner")

    # ---- hypotheses: the gate
    for stem, d in lab.hypotheses.items():
        if not common(d, "hypothesis", stem):
            continue
        if d.get("owner") not in lab.researchers:
            err(d, f"owner must be a researcher name, got '{d.get('owner')}'")
        st = d.get("status")
        if st not in HYP_STATUS:
            err(d, f"status must be one of {sorted(HYP_STATUS)}")
        surveys = d.get("surveys") or []
        if not surveys:
            err(d, "PRIOR-ART GATE: 'surveys' must list at least one complete survey")
        for s in surveys:
            state = lab.survey_state(s)
            if state in {"missing", "in-progress"}:
                err(d, f"PRIOR-ART GATE: survey '{s}' is {state}; no hypotheses until it passes")
            elif st in HYP_NEEDS_REVIEW and state != "reviewed":
                err(d, f"status '{st}' needs survey '{s}' reviewed by another researcher (it is {state})")
        cp = d.get("closest_prior") or []
        if len(cp) < 3:
            err(d, "'closest_prior' needs at least 3 library ids, with the difference stated under ## Novelty")
        for c in cp + d.cites():
            if c not in lab.library:
                err(d, f"cites '{c}' which is not in the library")
        secs = d.sections()
        for name in HYPOTHESIS_SECTIONS:
            if not secs.get(name):
                err(d, f"section '## {name}' is missing or empty")
        if st in HYP_NEEDS_REVIEW and not lab.passing_reviews(stem, d.get("owner")):
            err(d, f"status '{st}' needs a passing review from another researcher in reviews/")

    # ---- experiments
    for stem, d in lab.experiments.items():
        if not common(d, "experiment", stem):
            continue
        if d.get("owner") not in lab.researchers:
            err(d, f"owner must be a researcher name, got '{d.get('owner')}'")
        if d.get("status") not in EXP_STATUS:
            err(d, f"status must be one of {sorted(EXP_STATUS)}")
        h = lab.hypotheses.get(d.get("hypothesis"))
        if not h:
            err(d, f"hypothesis '{d.get('hypothesis')}' does not exist")
        elif h.get("status") not in HYP_NEEDS_REVIEW:
            err(d, f"hypothesis '{h.get('id')}' is '{h.get('status')}'; experiments need an accepted hypothesis")
        secs = d.sections()
        for name in EXPERIMENT_SECTIONS:
            if name not in secs:
                err(d, f"section '## {name}' is missing")
        if d.get("status") == "done" and not secs.get("Results"):
            err(d, "status done needs ## Results filled")

    # ---- tasks
    for stem, d in lab.tasks.items():
        if not common(d, "task", stem):
            continue
        for f in ("title", "kind", "status", "priority", "created"):
            if not d.get(f):
                err(d, f"'{f}' is required")
        if d.get("kind") and d.get("kind") not in TASK_KINDS:
            err(d, f"kind must be one of {sorted(TASK_KINDS)}")
        if d.get("status") and d.get("status") not in TASK_STATUS:
            err(d, f"status must be one of {sorted(TASK_STATUS)}")
        if d.get("priority") not in {"p0", "p1", "p2"}:
            err(d, "priority must be p0, p1 or p2")
        if d.get("status") in {"claimed", "done"}:
            agent_ok(d, "owner", d.get("owner"))
        if d.get("for") and d.get("for") not in lab.researchers:
            err(d, f"'for' must be a researcher name, got '{d.get('for')}'")
        for dep in d.get("depends_on") or []:
            if dep not in lab.tasks:
                err(d, f"depends_on '{dep}' is not a task id")
        topics_ok(d)

    # ---- agents
    for key, d in lab.agents.items():
        if d.error:
            err(d, d.error)
            continue
        if d.get("agent") != key:
            err(d, f"agent must be '{key}' (matches researchers/<name>/agents/<file>.md)")

    # ---- ids are unique across kinds
    for coll in (lab.surveys, lab.hypotheses, lab.experiments, lab.reviews, lab.tasks):
        for stem, d in coll.items():
            if stem in all_ids:
                err(d, f"id '{stem}' is already used by {all_ids[stem]}")
            all_ids[stem] = d.rel

    if urls:
        E.extend(check_urls(lab))
    return E, W


def check_urls(lab: Lab) -> list[str]:
    import urllib.request
    out = []
    for d in lab.library.values():
        u = d.get("url")
        if not u or "x.com/" in u or "twitter.com/" in u:
            continue
        req = urllib.request.Request(u, method="GET", headers={"User-Agent": "Mozilla/5.0 swarm-lab-check"})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                if r.status >= 400:
                    out.append(f"{d.rel}: url returns {r.status}")
        except Exception as e:  # noqa: BLE001
            code = getattr(e, "code", None)
            if code not in (401, 403, 429):  # paywalls and bot walls are not proof the source is fake
                out.append(f"{d.rel}: url failed ({code or e})")
    return out


# ------------------------------------------------------------------------------------------------ index
def esc(s) -> str:
    return str(s if s is not None else "").replace("|", "\\|").replace("\n", " ")


def build_index(lab: Lab):
    gen = "<!-- generated by scripts/lab.py index; do not edit by hand -->"
    # library/INDEX.md
    L = [gen, "", "# Library index", "", f"{len(lab.library)} entries.", ""]
    for d_name, kind in LIB_DIRS.items():
        docs = [d for d in lab.library.values() if d.path.parent.name == d_name and not d.error]
        L += [f"## {d_name.capitalize()} ({len(docs)})", ""]
        if not docs:
            L += ["None yet.", ""]
            continue
        L += ["| id | title | year | rel | depth | topics | added by |", "|---|---|---|---|---|---|---|"]
        docs.sort(key=lambda d: (-_int(d.get("relevance")), str(d.get("id"))))
        for d in docs:
            L.append(f"| [{d.get('id')}]({d_name}/{d.path.name}) | {esc(d.get('title'))} | {esc(d.get('year'))} "
                     f"| {esc(d.get('relevance'))} | {esc(d.get('read_depth'))} | "
                     f"{esc(', '.join(d.get('topics') or []))} | {esc(d.get('added_by'))} |")
        L.append("")
    (ROOT / "library/INDEX.md").write_text("\n".join(L), encoding="utf-8")
    build_bib(lab)

    # STATUS.md
    S = [gen, "", "# Status", ""]
    S += ["## Library by topic", "", "| topic | papers | code | blogs | threads | datasets | talks | total |",
          "|---|---|---|---|---|---|---|---|"]
    for slug in lab.topics:
        row = {k: 0 for k in LIB_DIRS.values()}
        for d in lab.library.values():
            if slug in (d.get("topics") or []) and d.get("type") in row:
                row[d.get("type")] += 1
        S.append(f"| {slug} | {row['paper']} | {row['code']} | {row['blog']} | {row['thread']} | "
                 f"{row['dataset']} | {row['talk']} | {sum(row.values())} |")
    S.append("")

    S += ["## Tasks", ""]
    order = {"claimed": 0, "open": 1, "blocked": 2, "done": 3}
    tasks = sorted(lab.tasks.values(), key=lambda d: (order.get(d.get("status"), 9), str(d.get("priority")),
                                                      str(d.get("id"))))
    S += ["| task | status | pri | kind | owner | for | updated | title |", "|---|---|---|---|---|---|---|---|"]
    for d in tasks:
        status = d.get("status")
        if status == "claimed" and is_stale(d):
            status = "claimed (stale)"
        S.append(f"| [{d.get('id')}](tasks/{d.path.name}) | {status} | {d.get('priority')} | {d.get('kind')} | "
                 f"{esc(d.get('owner') or '')} | {esc(d.get('for') or '')} | "
                 f"{esc(d.get('updated') or d.get('claimed_at') or '')} | {esc(d.get('title'))} |")
    S.append("")

    S += batch_section()

    S += ["## Agents", ""]
    if lab.agents:
        S += ["| agent | state | task | updated | doing |", "|---|---|---|---|---|"]
        for k, d in sorted(lab.agents.items(), key=lambda kv: str(kv[1].get("updated")), reverse=True):
            S.append(f"| {k} | {esc(d.get('state'))} | {esc(d.get('task') or '')} | {esc(d.get('updated'))} | "
                     f"{esc(d.get('doing') or '')} |")
    else:
        S.append("No agents registered yet.")
    S.append("")

    S += ["## Surveys (prior-art gate)", ""]
    if lab.surveys:
        S += ["| survey | owner | state | cited | gate problems |", "|---|---|---|---|---|"]
        for sid, d in lab.surveys.items():
            probs = lab.gate_problems(d) if not d.error else ["unparseable"]
            S.append(f"| [{sid}](surveys/{d.path.name}) | {esc(d.get('owner'))} | {lab.survey_state(sid)} | "
                     f"{len([c for c in d.cites() if c in lab.library])} | {len(probs)} |")
    else:
        S.append("None yet. Hypotheses are blocked until a survey passes the gate.")
    S.append("")

    S += ["## Hypotheses", ""]
    if lab.hypotheses:
        S += ["| hypothesis | owner | status | surveys | title |", "|---|---|---|---|---|"]
        for hid, d in lab.hypotheses.items():
            S.append(f"| [{hid}](hypotheses/{d.path.name}) | {esc(d.get('owner'))} | {esc(d.get('status'))} | "
                     f"{esc(', '.join(d.get('surveys') or []))} | {esc(d.get('title'))} |")
    else:
        S.append("None yet.")
    S.append("")

    S += ["## Experiments", ""]
    if lab.experiments:
        S += ["| experiment | owner | status | hypothesis |", "|---|---|---|---|"]
        for eid, d in lab.experiments.items():
            S.append(f"| [{eid}](experiments/{eid}/README.md) | {esc(d.get('owner'))} | {esc(d.get('status'))} | "
                     f"{esc(d.get('hypothesis'))} |")
    else:
        S.append("None yet.")
    S.append("")
    (ROOT / "STATUS.md").write_text("\n".join(S), encoding="utf-8")


def batch_section() -> list[str]:
    """Candidate batches (GitHub issues labelled `batch`, see PIPELINE.md). Skipped quietly without gh or network."""
    import json
    try:
        r = subprocess.run(["gh", "issue", "list", "-R", "dmarzzz/swarm-lab", "--label", "batch", "--state", "all",
                            "--limit", "500", "--json", "number,state,labels,title,updatedAt"],
                           capture_output=True, text=True, timeout=60)
        issues = json.loads(r.stdout) if r.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        issues = None
    if issues is None:
        return []
    claimed = [i for i in issues if i["state"] == "OPEN" and any(l["name"] == "claimed" for l in i["labels"])]
    free = [i for i in issues if i["state"] == "OPEN" and i not in claimed]
    closed = [i for i in issues if i["state"] != "OPEN"]
    S = ["## Candidate batches", "",
         f"{len(free)} free, {len(claimed)} claimed, {len(closed)} done. Claim with "
         "`python3 scripts/batches.py claim <n> --agent <id>` (PIPELINE.md).", ""]
    if claimed or free:
        S += ["| issue | state | updated | batch |", "|---|---|---|---|"]
        for i in sorted(claimed, key=lambda i: i["number"]) + sorted(free, key=lambda i: i["number"])[:15]:
            S.append(f"| [#{i['number']}](https://github.com/dmarzzz/swarm-lab/issues/{i['number']}) | "
                     f"{'claimed' if i in claimed else 'free'} | {i['updatedAt'][:16]}Z | {esc(i['title'])} |")
        if len(free) > 15:
            S.append(f"| | | | {len(free) - 15} more free batches |")
    S.append("")
    return S


def build_bib(lab: Lab):
    """library/references.bib: one BibTeX record per paper and talk, keyed by library id."""
    out = ["% generated by scripts/lab.py index; do not edit by hand", ""]
    for stem in sorted(lab.library):
        d = lab.library[stem]
        if d.error or d.get("type") not in {"paper", "talk"}:
            continue
        authors = d.get("authors") or []
        fields = {
            "title": "{" + str(d.get("title", "")) + "}",
            "author": " and ".join(str(a) for a in authors) if isinstance(authors, list) else str(authors),
            "year": str(d.get("year", "")),
            "howpublished" if d.get("type") == "talk" else "journal": str(d.get("venue") or ""),
            "doi": str(d.get("doi") or ""),
            "eprint": str(d.get("arxiv") or ""),
            "url": str(d.get("url") or ""),
            "note": "library/" + d.rel.split("library/", 1)[-1],
        }
        if fields["eprint"]:
            fields["archiveprefix"] = "arXiv"
        kind = "misc" if d.get("type") == "talk" or not d.get("venue") else "article"
        body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields.items() if v and v != "{}")
        out.append(f"@{kind}{{{stem},\n{body}\n}}\n")
    (ROOT / "library/references.bib").write_text("\n".join(out), encoding="utf-8")


def _norm_title(s) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def cmd_verify(a, lab):
    """Check paper metadata against DataCite (arXiv DOIs) and Crossref: the id resolves and the title matches."""
    import difflib
    import json
    import time
    import urllib.request

    def fetch(url):
        for i in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "swarm-lab-verify/1.0"})
                with urllib.request.urlopen(req, timeout=30) as r:
                    return r.read()
            except Exception as e:  # noqa: BLE001
                if getattr(e, "code", None) == 404:
                    return None
                time.sleep(3 * (i + 1))
        return b"ERR"

    only = None
    if a.since:
        r = git("diff", "--name-only", "--diff-filter=AM", a.since, "HEAD", "--", "library/papers")
        if r.returncode != 0:
            print(f"cannot diff against {a.since}; verifying everything")
        else:
            only = set(r.stdout.split())
            print(f"verifying {len(only)} paper(s) added or changed since {a.since[:12]}")
    bad = checked = 0
    for stem, d in sorted(lab.library.items()):
        if d.error or d.get("type") != "paper":
            continue
        if a.agent and d.get("added_by") != a.agent:
            continue
        if only is not None and d.rel not in only:
            continue
        want = _norm_title(d.get("title"))
        got, src = None, None
        if d.get("arxiv"):
            aid = re.sub(r"v\d+$", "", str(d.get("arxiv")).strip())
            raw = fetch(f"https://api.datacite.org/dois/10.48550/arXiv.{aid}")
            src = f"arXiv {aid}"
            if raw and raw != b"ERR":
                got = (json.loads(raw)["data"]["attributes"].get("titles") or [{}])[0].get("title")
        elif d.get("doi"):
            doi = str(d.get("doi")).strip()
            raw = fetch(f"https://api.crossref.org/works/{doi}")
            src = f"DOI {doi}"
            if raw and raw != b"ERR":
                got = (json.loads(raw)["message"].get("title") or [None])[0]
        else:
            print(f"warn  {d.rel}: no arxiv or doi to verify against (url only)")
            continue
        checked += 1
        if raw == b"ERR":
            print(f"skip  {d.rel}: {src} lookup failed (network); rerun later")
            checked -= 1
            continue
        if not got:
            print(f"BAD   {d.rel}: {src} does not resolve")
            bad += 1
            continue
        have = _norm_title(got)
        ratio = difflib.SequenceMatcher(None, want, have).ratio()
        a_w, b_w = set(want.split()), set(have.split())
        if a_w and b_w:  # word-order tolerant: arXiv and journal versions often swap title halves
            ratio = max(ratio, len(a_w & b_w) / len(a_w | b_w))
        short, long_ = sorted((want, have), key=len)
        if len(short) >= 15 and long_.startswith(short):  # subtitle dropped on one side
            ratio = 1.0
        if ratio < a.threshold:
            print(f"BAD   {d.rel}: title mismatch ({ratio:.2f}) entry='{d.get('title')}' {src}='{' '.join(got.split())}'")
            bad += 1
    print(f"\n{checked} papers checked against arXiv/Crossref, {bad} problems")
    return 1 if bad else 0


def is_stale(d: Doc) -> bool:
    t = parse_time(d.get("updated") or d.get("claimed_at"))
    return bool(t) and dt.datetime.now(dt.timezone.utc) - t > dt.timedelta(hours=CLAIM_TTL_HOURS)


# ------------------------------------------------------------------------------------------------ git tasks
def git(*args, check=False) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=check)


def mutate_task(task_id: str, agent: str, fn, verb: str) -> int:
    path = ROOT / "tasks" / f"{task_id}.md"
    rel = path.relative_to(ROOT).as_posix()
    for attempt in range(6):
        p = git("pull", "--rebase", "--autostash")
        if p.returncode != 0:
            print(f"git pull failed:\n{p.stderr}", file=sys.stderr)
            return 1
        if not path.exists():
            print(f"no task '{task_id}' in tasks/", file=sys.stderr)
            return 1
        d = Doc(path)
        problem = fn(d)
        if problem:
            print(problem, file=sys.stderr)
            return 1
        d.write()
        if not git("status", "--porcelain", "--", rel).stdout.strip():
            print(f"{verb} {task_id}: already up to date")
            return 0
        c = git("commit", "-m", f"[{agent}] task: {verb} {task_id}", "--", rel)
        if c.returncode != 0:
            print(f"git commit failed:\n{c.stdout}{c.stderr}", file=sys.stderr)
            return 1
        if git("push").returncode == 0:
            print(f"{verb} {task_id} as {agent}")
            return 0
        # someone pushed first: drop our commit and re-evaluate on fresh state
        git("reset", "--soft", "HEAD~1")
        git("restore", "--staged", "--", rel)
        git("checkout", "--", rel)
        print(f"push rejected (attempt {attempt + 1}); re-reading the task", file=sys.stderr)
    print("gave up after repeated push rejections", file=sys.stderr)
    return 1


def require_agent(lab: Lab, agent: str):
    m = AGENT_RE.match(agent or "")
    if not m or m.group(1) not in lab.researchers:
        sys.exit(f"--agent must be <researcher>/<agent> with a known researcher ({', '.join(lab.researchers)})")


def cmd_claim(a, lab):
    require_agent(lab, a.agent)

    def fn(d):
        st = d.get("status")
        for dep in d.get("depends_on") or []:
            dd = lab.tasks.get(dep)
            if dd and dd.get("status") != "done" and not a.force_deps:
                return f"'{d.get('id')}' depends on '{dep}' which is {dd.get('status')} (use --force-deps to override)"
        if st == "claimed" and d.get("owner") != a.agent and not is_stale(d):
            return f"'{d.get('id')}' is held by {d.get('owner')} (updated {d.get('updated')}); pick another task"
        if st in {"done", "blocked"}:
            return f"'{d.get('id')}' is {st}"
        if st == "claimed" and d.get("owner") != a.agent:
            d.fm.setdefault("history", []).append(f"{now()} reclaimed from stale {d.get('owner')}")
        d.fm["status"], d.fm["owner"], d.fm["claimed_at"], d.fm["updated"] = "claimed", a.agent, now(), now()
        return None
    return mutate_task(a.task, a.agent, fn, "claim")


def _held(d, agent):
    if d.get("status") != "claimed" or d.get("owner") != agent:
        return f"'{d.get('id')}' is not claimed by {agent} (status {d.get('status')}, owner {d.get('owner')})"
    return None


def cmd_touch(a, lab):
    require_agent(lab, a.agent)

    def fn(d):
        p = _held(d, a.agent)
        if not p:
            d.fm["updated"] = now()
        return p
    return mutate_task(a.task, a.agent, fn, "touch")


def cmd_done(a, lab):
    require_agent(lab, a.agent)

    def fn(d):
        p = _held(d, a.agent)
        if p:
            return p
        d.fm["status"], d.fm["updated"] = "done", now()
        if a.output:
            d.fm["outputs"] = list(dict.fromkeys((d.get("outputs") or []) + a.output))
        return None
    return mutate_task(a.task, a.agent, fn, "done")


def cmd_release(a, lab):
    require_agent(lab, a.agent)

    def fn(d):
        p = _held(d, a.agent)
        if p:
            return p
        d.fm["status"], d.fm["owner"], d.fm["updated"] = "open", None, now()
        d.fm.pop("claimed_at", None)
        if a.note:
            d.fm.setdefault("history", []).append(f"{now()} released by {a.agent}: {a.note}")
        return None
    return mutate_task(a.task, a.agent, fn, "release")


# ------------------------------------------------------------------------------------------------ scaffolding
def cmd_new(a, lab):
    kind, ident = a.kind, a.id
    if not ID_RE.match(ident):
        sys.exit("id must be lowercase a-z, 0-9 and hyphens")
    needs_agent = True
    if kind in LIB_KIND_DIR:
        dest = ROOT / "library" / LIB_KIND_DIR[kind] / f"{ident}.md"
    elif kind == "survey":
        dest = ROOT / "surveys" / f"{ident}.md"
    elif kind == "hypothesis":
        dest = ROOT / "hypotheses" / f"{ident}.md"
    elif kind == "experiment":
        dest = ROOT / "experiments" / ident / "README.md"
    elif kind == "review":
        dest = ROOT / "reviews" / f"{ident}.md"
    elif kind == "task":
        dest = ROOT / "tasks" / f"{ident}.md"
    elif kind == "agent":
        dest = None
    else:
        sys.exit(f"unknown kind '{kind}'")
    if needs_agent:
        require_agent(lab, a.agent)
    researcher, agent_name = a.agent.split("/")
    if kind == "agent":
        dest = ROOT / "researchers" / researcher / "agents" / f"{agent_name}.md"
    else:
        hit = [p for p in ROOT.glob(f"**/{ident}.md") if ".git" not in p.parts] + \
              ([ROOT / "experiments" / ident] if (ROOT / "experiments" / ident).exists() else [])
        if hit:
            sys.exit(f"'{ident}' already exists: {hit[0].relative_to(ROOT)}. Extend it instead of duplicating.")
    if dest.exists():
        sys.exit(f"{dest.relative_to(ROOT)} already exists")
    tpl = (ROOT / "templates" / f"{kind}.md").read_text(encoding="utf-8")
    for k, v in {"id": ident, "agent": a.agent, "researcher": researcher, "date": today(), "now": now(),
                 "agent_name": agent_name}.items():
        tpl = tpl.replace("{{" + k + "}}", v)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(tpl, encoding="utf-8")
    print(dest.relative_to(ROOT))
    return 0


def cmd_add_researcher(a, lab):
    name = a.name.lower()
    if not re.match(r"^[a-z0-9_-]+$", name):
        sys.exit("researcher name must be lowercase a-z, 0-9, _ or -")
    d = ROOT / "researchers" / name
    if d.exists():
        sys.exit(f"{d.relative_to(ROOT)} already exists")
    for sub in ("agents", "log", "notes"):
        (d / sub).mkdir(parents=True)
        (d / sub / ".gitkeep").write_text("")
    for f in ("README.md", "inbox.md"):
        src = (ROOT / "templates" / "researcher" / f).read_text(encoding="utf-8")
        (d / f).write_text(src.replace("{{researcher}}", name), encoding="utf-8")
    print(f"created researchers/{name}/")
    return 0


def cmd_find(a, lab):
    q = a.text.lower()
    qn = norm_url(a.text)
    hits = 0
    for stem, d in lab.library.items():
        hay = " ".join(str(d.get(k, "")) for k in ("id", "title", "url", "doi", "arxiv", "repo", "authors")).lower()
        if q in hay or (d.get("url") and qn == norm_url(d.get("url"))):
            print(f"{d.rel}  [{d.get('type')}, rel {d.get('relevance')}, {d.get('read_depth')}]  {d.get('title')}")
            hits += 1
    if not hits:
        print("no match in library/ (also try the arXiv id, DOI, repo owner/name or a title word)")
    return 0


def cmd_gate(a, lab):
    s = lab.surveys.get(a.survey)
    if not s:
        sys.exit(f"no survey '{a.survey}'")
    probs = lab.gate_problems(s)
    print(f"{a.survey}: state {lab.survey_state(a.survey)}")
    if probs:
        print("still needs:")
        for p in probs:
            print(f"  - {p}")
    else:
        print("passes the mechanical gate. Mark status: complete, then open a review task for another researcher.")
    return 0


GENERATED = {"STATUS.md", "library/INDEX.md", "library/references.bib"}
PROTECTED = ("AGENTS.md", "CLAUDE.md", "README.md", "project.yaml", "artifacts.yaml", "artifacts.lock.json",
             "scripts/", "templates/", ".github/", ".flightdeck/", ".claude/", ".agents/", ".codex/", ".cursor/")


def tree_errors(rev: str) -> set[str]:
    """Return reported errors; raise if the clean-tree checker did not finish reliably.

    Infrastructure failures must not become error-set members: sync subtracts
    baseline errors, which would cancel a repeated checker failure into success.
    """
    import shutil
    import tempfile
    d = tempfile.mkdtemp(prefix="lab-sync-")
    try:
        if git("worktree", "add", "--detach", d, rev).returncode != 0:
            raise RuntimeError("could not create a worktree to verify the commit")
        r = subprocess.run([sys.executable, str(Path(d) / "scripts/lab.py"), "check"], capture_output=True, text=True)
        error_lines = [line[6:] for line in r.stdout.splitlines() if line.startswith("ERROR ")]
        errors = set(error_lines)
        summaries = re.findall(r"^(\d+) errors, \d+ warnings\. .+$", r.stdout, re.MULTILINE)
        if (len(summaries) != 1 or int(summaries[0]) != len(error_lines)
                or r.returncode != (1 if errors else 0)):
            # Do not echo arbitrary stderr: a crashed checker could print secrets.
            raise RuntimeError(f"clean-tree checker failed or returned incomplete output (exit {r.returncode})")
        return errors
    finally:
        git("worktree", "remove", "--force", d)
        shutil.rmtree(d, ignore_errors=True)


def heartbeat_tasks(researcher: str) -> list[str]:
    """Refresh `updated` on tasks held by this researcher's agents that report state: working."""
    lab, touched = Lab(), []
    for d in lab.tasks.values():
        owner = str(d.get("owner") or "")
        if d.get("status") != "claimed" or not owner.startswith(researcher + "/"):
            continue
        agent = lab.agents.get(owner)
        if not agent or not str(agent.get("state", "")).startswith("working"):
            continue
        seen = parse_time(agent.get("updated"))  # a dead session stops refreshing its status file
        if not seen or dt.datetime.now(dt.timezone.utc) - seen > dt.timedelta(hours=CLAIM_TTL_HOURS):
            continue
        t = parse_time(d.get("updated") or d.get("claimed_at"))
        if t and dt.datetime.now(dt.timezone.utc) - t < dt.timedelta(minutes=20):
            continue
        d.fm["updated"] = now()
        d.write()
        touched.append(d.rel)
    return touched


def sync_once(agent: str, include_protected=False) -> int:
    """Commit and push every changed file that passes the check; leave failing or off-limits files for later.
    The commit is re-checked on a clean checkout before pushing, so a file that changed mid-sync, or a
    duplicate that only shows up across files, never reaches main."""
    import time
    researcher = agent.split("/")[0]
    heartbeat_tasks(researcher)
    # list changes first, then check: a file created after the listing is simply not staged this round
    st = git("status", "--porcelain", "-uall").stdout.splitlines()
    paths = [line[3:].split(" -> ")[-1].strip().strip('"') for line in st]
    E, _ = check(Lab())
    failing = {e.split(":", 1)[0] for e in E}
    stage, skipped = [], []
    for path in paths:
        if path in GENERATED:
            continue
        if not include_protected and path.startswith(PROTECTED):
            skipped.append((path, "protected (pass --include-protected only with human approval)"))
        elif path.startswith("researchers/") and path.split("/")[1] != researcher:
            skipped.append((path, f"belongs to researcher {path.split('/')[1]}"))
        elif path in failing:
            skipped.append((path, "fails `lab.py check`; fix it and the next sync picks it up"))
        else:
            stage.append(path)
    if not stage:
        for path, why in skipped:
            print(f"skip  {path}: {why}")
        print(f"{now()} sync: nothing to push")
        return 0
    baseline = tree_errors("HEAD")  # errors already on the branch are not ours to block on
    git("add", "-A", "--", *stage)
    for _ in range(4):
        by = {}
        for s in stage:
            fp = ROOT / s
            if s.startswith("library/") and fp.exists():
                a = Doc(fp).get("added_by") or "?"
                by[a] = by.get(a, 0) + 1
        body = "\n".join(f"{n:4d} library entries by {a}" for a, n in sorted(by.items(), key=lambda kv: -kv[1]))
        msg = f"[{agent}] sync: {len(stage)} file(s)" + (f"\n\n{body}" if body else "")
        if git("commit", "-m", msg, "--", *stage).returncode != 0:
            print("commit failed", file=sys.stderr)
            return 1
        new_errs = tree_errors("HEAD") - baseline
        if not new_errs:
            break
        bad = set()
        for e in new_errs:
            f = e.split(":", 1)[0]
            if f in stage:
                bad.add(f)
            m = re.search(r"duplicate of '([^']+)'", e)
            if m:
                bad.update(s for s in stage if s.endswith(f"/{m.group(1)}.md"))
        git("reset", "--soft", "HEAD~1")
        if not bad:
            git("restore", "--staged", "--", *stage)
            print("sync: the commit would add errors that cannot be traced to staged files; not pushing:", file=sys.stderr)
            for e in sorted(new_errs):
                print(f"  {e}", file=sys.stderr)
            return 1
        git("restore", "--staged", "--", *bad)
        for b in sorted(bad):
            skipped.append((b, "fails the check on the committed tree (changed mid-sync, or a duplicate)"))
        stage = [s for s in stage if s not in bad]
        if not stage:
            print(f"{now()} sync: nothing left to push after verification")
            return 0
    else:
        git("reset", "--soft", "HEAD~1")
        git("restore", "--staged", "--", *stage)
        print("sync: could not produce a clean commit; nothing pushed", file=sys.stderr)
        return 1
    for path, why in skipped:
        print(f"skip  {path}: {why}")
    for attempt in range(5):
        # merge rather than rebase: never stashes or rewrites files other agents may be editing in this clone
        pl = git("pull", "--no-rebase", "--no-edit")
        if pl.returncode != 0:
            print(f"pull failed (resolve by hand, then rerun sync):\n{pl.stdout}{pl.stderr}", file=sys.stderr)
            return 1
        # Pull may introduce cross-file conflicts (for example duplicate library
        # ids) without a Git conflict. Validate this exact merged HEAD each time.
        merged_errors = tree_errors("HEAD") - baseline
        if merged_errors:
            print("sync: merged tree introduces validation errors; not pushing:", file=sys.stderr)
            for error in sorted(merged_errors):
                print(f"  {error}", file=sys.stderr)
            return 1
        if git("push").returncode == 0:
            print(f"{now()} sync: pushed {len(stage)} file(s)")
            return 0
        time.sleep(3 * (attempt + 1))
    print("push kept failing; the commit is local and the next sync will retry", file=sys.stderr)
    return 1


def cmd_sync(a, lab):
    import time
    require_agent(lab, a.agent)
    while True:
        try:
            sync_once(a.agent, a.include_protected)
        except Exception as e:  # noqa: BLE001  a background timer must survive one bad round
            print(f"{now()} sync error: {e}", file=sys.stderr)
        sys.stdout.flush()
        if not a.every:
            return 0
        time.sleep(a.every)


def cmd_check(a, lab):
    E, W = check(lab, urls=a.urls)
    if a.agent:
        mine = {d.rel for d in lab.library.values() if d.get("added_by") == a.agent}
        mine |= {d.rel for d in list(lab.surveys.values()) + list(lab.hypotheses.values())
                 if a.agent in (d.get("agents") or [])}
        mine |= {d.rel for d in lab.tasks.values() if d.get("owner") == a.agent}
        E = [e for e in E if e.split(":", 1)[0] in mine]
        W = [w for w in W if w.split(":", 1)[0] in mine]
    for w in W:
        print(f"warn  {w}")
    for e in E:
        print(f"ERROR {e}")
    print(f"\n{len(E)} errors, {len(W)} warnings. "
          f"{len(lab.library)} library entries, {len(lab.surveys)} surveys, {len(lab.hypotheses)} hypotheses, "
          f"{len(lab.tasks)} tasks.")
    return 1 if E else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("check")
    p.add_argument("--urls", action="store_true", help="also fetch every library url (slow)")
    p.add_argument("--agent", help="only report problems in files this agent added or owns")
    p = sub.add_parser("verify")
    p.add_argument("--agent", help="only verify papers this agent added")
    p.add_argument("--threshold", type=float, default=0.85)
    p.add_argument("--since", help="only papers added or changed since this git revision (CI uses the push's base)")
    sub.add_parser("index")
    p = sub.add_parser("find")
    p.add_argument("text")
    p = sub.add_parser("new")
    p.add_argument("kind")
    p.add_argument("id", nargs="?", default="")
    p.add_argument("--agent", required=True)
    for name in ("claim", "touch", "done", "release"):
        p = sub.add_parser(name)
        p.add_argument("task")
        p.add_argument("--agent", required=True)
        if name == "claim":
            p.add_argument("--force-deps", action="store_true")
        if name == "done":
            p.add_argument("--output", nargs="*", default=[])
        if name == "release":
            p.add_argument("--note", default="")
    p = sub.add_parser("sync")
    p.add_argument("--agent", required=True)
    p.add_argument("--every", type=int, default=0, help="seconds between rounds; 0 = run once")
    p.add_argument("--include-protected", action="store_true")
    p = sub.add_parser("add-researcher")
    p.add_argument("name")
    p = sub.add_parser("gate")
    p.add_argument("survey")
    a = ap.parse_args(argv)
    if a.cmd == "new" and a.kind == "agent" and not a.id:
        a.id = a.agent.split("/")[-1].replace(".", "-")
    lab = Lab()
    return {
        "check": cmd_check, "index": lambda a, lab: build_index(lab) or 0, "find": cmd_find, "new": cmd_new,
        "claim": cmd_claim, "touch": cmd_touch, "done": cmd_done, "release": cmd_release,
        "add-researcher": cmd_add_researcher, "gate": cmd_gate, "verify": cmd_verify, "sync": cmd_sync,
    }[a.cmd](a, lab)


if __name__ == "__main__":
    sys.exit(main())
