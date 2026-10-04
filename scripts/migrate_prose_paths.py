#!/usr/bin/env python3
"""Rewrite old-layout repo paths written outside markdown links: in backticks, prose, YAML frontmatter and
JSON string values, shell commands in documentation, and default-branch GitHub URLs.

A path token is rewritten only when all of these hold:
  * it starts at an old top-level name (library/, surveys/, reviews/, synthesis/, hypotheses/, experiments/,
    tooling/, researchers/, tasks/, candidates/, templates/, STATUS.md, PIPELINE.md) and is not part of a URL
    or a longer path (not preceded by `/`, a word character, `.` or `-`);
  * the mapped new path exists (file or directory; `<id>` without `.md` counts), or the token has a glob or
    placeholder segment (`*`, `<name>`, `{id}`, `$VAR`) and the concrete directory in front of it exists;
  * it does not also resolve relative to the file's own directory, or to an enclosing study / toolkit
    project directory (a study's own `reviews/`, `experiments/`, `templates/` ... stay as they are);
  * the line is not a statement about the move itself (it already names the new path, or says "formerly",
    "old layout", "moved from" ...).
`github.com/dmarzzz/swarm-lab/(blob|tree|raw)/main/<path>` and raw.githubusercontent.com URLs become
`swarm-dynamics-lab` URLs with the new path when the target exists. Commit-pinned permalinks never match.

Never touched: artifacts/, attestations/, agentops/, node_modules, .git, .flightdeck/, the artifact manifest
and lock (scripts/migrate_artifact_paths.py owns those), generated files, binary files, the migration
scripts themselves, and class (b) hash-recorded files (see scripts/migrate_common.py).

Reported, not rewritten:
  * code files (`.py .sh .mjs .ts .tsx .html`) everywhere. Under the studies they are the code that ran an
    experiment; elsewhere (scripts/, src/, dashboard/) every old path still written in code is there on
    purpose: a fallback for old-layout lanes or a translator of pre-move paths. Each one needs a person.
  * data files (`.json .yaml .yml .toml .txt`) inside the research record: 5-experiments/studies/,
    5-experiments/toolkit/, a registered experiment's src/ or results/, and src/ (artifact ingredients).
    `--study-data` opts these in.
  * markdown kept as captured input inside the record (a path segment named inputs, prompts, traces,
    transcripts, raw or snapshots): those are copies of what a run or review read.
Inside 5-experiments/, a token under `reviews/`, `experiments/`, `templates/`, `tasks/`, `candidates/` or
`tooling/` is rewritten only when it names an existing file: a bare `reviews/` or `reviews/<attempt>-pre.md`
there means the study's own folder.

    python3 scripts/migrate_prose_paths.py                              # dry run: summary + 20 samples
    python3 scripts/migrate_prose_paths.py --write [--include-recorded] # apply (class (a) with the flag)
    python3 scripts/migrate_prose_paths.py --only <path-prefix> ...     # restrict to files under a prefix
    python3 scripts/migrate_prose_paths.py --samples 50 --list-held --list-unresolved
"""
import os, re, sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import migrate_common as mc

os.chdir(mc.ROOT)
DOC_EXT = (".md", ".txt")
DATA_EXT = (".yaml", ".yml", ".json", ".toml")
CODE_EXT = (".py", ".sh", ".mjs", ".ts", ".tsx", ".html")
SKIP_PREFIX = ("artifacts/", "attestations/", "agentops/", "dashboard/node_modules/", "dashboard/dist/",
               "dashboard/public/data/", ".git/", ".flightdeck/", "scripts/migrate_", "data/")
SKIP_FILES = {"artifacts.yaml", "artifacts.lock.json", "lab/STATUS.md", "1-library/INDEX.md",
              "5-experiments/EVIDENCE.md", "dashboard/package-lock.json",
              # these know about the old layout on purpose (legacy evidence-block links)
              "scripts/experiment_evidence.py", "scripts/test_experiment_evidence.py"}
RECORD_TREES = re.compile(r"^5-experiments/(studies|toolkit)/|^5-experiments/[^/]+/(src|results)/|^src/")
CAPTURED = re.compile(r"/(inputs|prompts|traces|transcripts|raw|snapshots)/")
AMBIGUOUS = ("reviews/", "experiments/", "templates/", "tasks/", "candidates/", "tooling/")
PROJECT_DIR = re.compile(r"^(5-experiments/studies/[^/]+/[^/]+|5-experiments/toolkit/[^/]+|5-experiments/(?!studies/|toolkit/)[^/]+)(/|$)")

SEG = r"(?:[\w.@%+~=*$-]|<[\w .|-]+>|\{[\w .,|-]+\})+"
TOKEN = re.compile(r"(?<![\w./\\-])(?:(?:%s)/(?:%s(?:/%s)*/?)?|(?:STATUS|PIPELINE)\.md(?![\w-]))" % ("|".join(mc.OLD_TOPS), SEG, SEG))
GH = re.compile(r"((?:github\.com/dmarzzz/(?:swarm-lab|swarm-dynamics-lab)/(?:blob|tree|raw)/main/)"
                r"|(?:raw\.githubusercontent\.com/dmarzzz/(?:swarm-lab|swarm-dynamics-lab)/(?:refs/heads/)?main/))"
                r"(%s(?:/%s)*/?)" % (SEG, SEG))
HISTORY = re.compile(r"(?i)\b(formerly|old layout|flat layout|old paths?|pre-move|before the (move|reorg\w*|migration)|"
                     r"renamed from|moved from|used to live)\b")
WINDOW = 160
WILD = re.compile(r"[*<>{}$]|^\.\.\.$")


def resolves(path, base=""):
    """Does a (new-layout or local) path exist under base? Globs/placeholders need their concrete parent."""
    p = path.rstrip("/").rstrip(".")
    if not p:
        return False
    segs = p.split("/")
    for i, s in enumerate(segs):
        if WILD.search(s):
            return i >= 1 and os.path.isdir(os.path.join(base, *segs[:i]))
    full = os.path.join(base, p)
    return os.path.lexists(full) or os.path.isfile(full + ".md")


def local(token, f):
    """Does the token resolve from the file's own directory, or from an enclosing study/toolkit project?"""
    here = os.path.dirname(f)
    if here and resolves(token, here):
        return True
    m = PROJECT_DIR.match(f)
    if m:
        d = here
        while d and len(d) >= len(m.group(1)):
            if resolves(token, d):
                return True
            d = os.path.dirname(d)
    return False


def rewrite(f, text, stats, samples):
    out, n = [], 0
    in_experiments = f.startswith("5-experiments/")
    for line in text.splitlines(keepends=True):

        def gh(m):
            nonlocal n
            head, path = m.group(1), m.group(2)
            new = mc.remap(path, mc.FORWARD)
            new_head = head.replace("/swarm-lab/", "/swarm-dynamics-lab/")
            if not resolves(new) or (new == path and new_head == head):
                if new_head != head or new != path:
                    stats["url target missing"] += 1
                return m.group(0)
            n += 1
            samples.append((f, m.group(0), new_head + new))
            return new_head + new

        def tok(m):
            nonlocal n
            t = m.group(0)
            if m.start() >= 2 and line[m.start() - 2:m.start()] == "](":
                stats["markdown link target (migrate_links.py)"] += 1
                return t
            if t.startswith("experiments/studies") or t.startswith("experiments/toolkit") or t.startswith("surveys/reviews"):
                stats["not an old-layout path"] += 1
                return t
            new = mc.remap(t, mc.FORWARD)
            if not resolves(new):
                stats["unresolved"] += 1
                unresolved[t] += 1
                return t
            if local(t, f):
                stats["local to the file's own folder"] += 1
                return t
            if in_experiments and t.startswith(AMBIGUOUS) and not (
                    t.count("/") >= 1 and not t.endswith("/") and os.path.isfile(new.rstrip("."))):
                stats["study-local folder name"] += 1
                return t
            near = line[max(0, m.start() - WINDOW):m.start()] + line[m.end():m.end() + WINDOW]
            if HISTORY.search(near) or re.search(r"(?<![\w./-])" + re.escape(new.rstrip("/").rstrip(".")), near):
                stats["line describes the move"] += 1
                return t
            n += 1
            samples.append((f, t, new))
            return new

        line = GH.sub(gh, line)
        out.append(TOKEN.sub(tok, line))
    return "".join(out), n


unresolved = Counter()


def area(f):
    parts = f.split("/")
    if parts[0] == "5-experiments" and len(parts) > 2 and parts[1] in ("studies", "toolkit"):
        return "5-experiments/" + parts[1]
    return parts[0] if len(parts) > 1 else "(root files)"


def main():
    argv = sys.argv[1:]
    write, include, study_data = "--write" in argv, "--include-recorded" in argv, "--study-data" in argv
    only = mc.only_args(argv)
    n_samples = int(argv[argv.index("--samples") + 1]) if "--samples" in argv else 20
    stats, samples, counts, candidates = Counter(), [], {}, {}
    report_only = defaultdict(int)
    for f in mc.tracked():
        ext = os.path.splitext(f)[1].lower()
        if ext not in DOC_EXT + DATA_EXT + CODE_EXT or not mc.under(f, only):
            continue
        if f.startswith(SKIP_PREFIX) or "/node_modules/" in f or f in SKIP_FILES or mc.is_snapshot_path(f):
            continue
        raw = open(f, "rb").read()
        if b"\0" in raw[:4096]:
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if not any(t in text for t in mc.OLD_TOPS + ("STATUS.md", "PIPELINE.md", "swarm-lab/")):
            continue
        local_samples = []
        new_text, n = rewrite(f, text, stats, local_samples)
        if not n:
            continue
        record = bool(RECORD_TREES.match(f))
        kind = ("code" if ext in CODE_EXT else
                "data" if record and (ext in DATA_EXT or ext == ".txt") and not study_data else
                "captured input" if record and CAPTURED.search("/" + f) else None)
        if kind:
            report_only[kind + " in " + area(f)] += n
            report_only["_files"] += 1
            continue
        counts[f] = n
        candidates[f] = (raw, new_text.encode("utf-8"))
        samples += local_samples
    recorded = mc.Recorded()
    written, held_a, held_b, touched = mc.settle(recorded, candidates, include, write)
    tok = lambda files: sum(counts[f] for f in files)
    verb = "rewrote" if write else "would rewrite"
    print(f"{verb} {tok(written)} path tokens in {len(written)} files")
    by_area = Counter()
    for f in written:
        by_area[area(f)] += counts[f]
    for a, c in sorted(by_area.items(), key=lambda x: -x[1]):
        print(f"  {c:6d}  {a}")
    if touched:
        print(f"{'updated' if write else 'would update'} {sum(touched.values())} recorded digests in {len(touched)} registry files")
    print(f"held, class (a) registry-recorded (rewritten with --include-recorded): {tok(held_a)} tokens in {len(held_a)} files")
    print(f"held, class (b) recorded in the research record (always byte-identical): {tok(held_b)} tokens in {len(held_b)} files")
    n_ro = report_only.pop("_files", 0)
    print(f"reported only (code, record data, captured inputs): {sum(report_only.values())} tokens in {n_ro} files")
    for k, c in sorted(report_only.items(), key=lambda x: -x[1]):
        print(f"  {c:6d}  {k}")
    print("left alone: " + "; ".join(f"{c} {k}" for k, c in stats.most_common()))
    if n_samples and samples:
        ok = set(written)
        shown = [s for s in samples if s[0] in ok]
        step = max(1, len(shown) // n_samples)
        print(f"samples ({min(n_samples, len(shown))} of {len(shown)}):")
        for f, old, new in shown[::step][:n_samples]:
            print(f"  {f}: {old}  ->  {new}")
    if "--list-held" in argv:
        for f in sorted(held_a):
            print(f"  held (a) {counts[f]:4d}  {f}  <- {held_a[f][0]}")
        for f in sorted(held_b):
            print(f"  held (b) {counts[f]:4d}  {f}  <- {held_b[f][0]}")
    if "--list-unresolved" in argv:
        for t, c in unresolved.most_common(60):
            print(f"  unresolved {c:4d}  {t}")


if __name__ == "__main__":
    main()
