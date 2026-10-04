#!/usr/bin/env python3
"""batches.py: candidate batches <-> GitHub issues. One issue per candidates/<source>/<batch-id>.jsonl.
Needs the `gh` CLI, logged in with push or triage on the repo. See PIPELINE.md.

  python3 scripts/batches.py setup                       create the labels (idempotent)
  python3 scripts/batches.py publish [--batch <id> ...]  one issue per batch that has none yet
  python3 scripts/batches.py list [--open|--free]        batches and their issues
  python3 scripts/batches.py claim <issue> --agent <id>  assign yourself, label claimed, comment
  python3 scripts/batches.py touch <issue> --agent <id>  hb_signal comment; run every 30 min (claims go stale after 90 min of silence)
  python3 scripts/batches.py done <issue> --agent <id> --entries <library paths...> [--skipped "<why>"]
  python3 scripts/batches.py release <issue> --agent <id> --note "<where you got to>"
  python3 scripts/batches.py stale                       claimed issues with no activity for 90 min
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAND = ROOT / "candidates"
MAP = CAND / "ISSUES.tsv"  # batch-id \t issue-number \t issue-url
REPO = "dmarzzz/swarm-lab"
STALE_MIN = 90  # touch every 30 min; three missed touches and the batch is up for grabs
LIB_DIR = {"x": "library/threads/", "blog": "library/blogs/", "web": "library/talks/", "code": "library/code/", "paper": "library/papers/", "talk": "library/talks/"}
NEW_KIND = {"x": "thread", "blog": "blog", "web": "blog", "code": "code", "paper": "paper", "talk": "talk"}


def gh(*args, inp=None) -> str:
    r = subprocess.run(["gh", *args], capture_output=True, text=True, input=inp)
    if r.returncode != 0:
        sys.exit(f"gh {' '.join(args[:3])} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def gh_json(*args):
    return json.loads(gh(*args) or "null")


def topics() -> list[str]:
    import yaml
    return [t["slug"] for t in yaml.safe_load((ROOT / "library/topics.yaml").read_text())]


def read_map() -> dict[str, tuple[str, str]]:
    out = {}
    if MAP.exists():
        for ln in MAP.read_text().splitlines():
            if ln.strip() and not ln.startswith("#"):
                b, n, u = ln.split("\t")
                out[b] = (n, u)
    return out


def batches() -> dict[str, Path]:
    return {p.stem: p for src in CAND.iterdir() if src.is_dir() for p in sorted(src.glob("*.jsonl"))}


def rows(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


# ------------------------------------------------------------------------------------------------ setup
def cmd_setup(a):
    want = {"batch": ("0E8A16", "a claimable batch of source candidates (see PIPELINE.md)"),
            "claimed": ("FBCA04", "an agent is working this batch; stale after 90 min without a comment"),
            "needs-review": ("D93F0B", "entries written but something is off; a second agent should look"),
            "source:x": ("1D76DB", "X posts and threads -> library/threads"),
            "source:blog": ("1D76DB", "blogs and long-form web -> library/blogs"),
            "source:web": ("1D76DB", "other web pages"),
            "source:code": ("1D76DB", "repos -> library/code"),
            "source:paper": ("1D76DB", "papers -> library/papers"),
            "source:talk": ("1D76DB", "recorded talks and lectures -> library/talks")}
    for t in topics():
        want[f"topic:{t}"] = ("5319E7", f"topic slug {t} from library/topics.yaml")
    have = {l["name"] for l in gh_json("label", "list", "-R", REPO, "--limit", "200", "--json", "name")}
    for name, (color, desc) in want.items():
        if name in have:
            continue
        gh("label", "create", name, "-R", REPO, "--color", color, "--description", desc)
        print(f"  created label {name}")
    print(f"labels: {len(want)} wanted, {len([n for n in want if n not in have])} created")
    return 0


# ------------------------------------------------------------------------------------------------ publish
def issue_body(bid: str, src: str, topic: str, items: list[dict]) -> str:
    lib = LIB_DIR.get(src, "library/")
    kind = NEW_KIND.get(src, "blog")
    lines = [f"Batch `{bid}`: {len(items)} {src} candidates, topic `{topic}`. File: `candidates/{src}/{bid}.jsonl` "
             f"on `main`.", "",
             "**How to work it** (full flow in `PIPELINE.md`):", "",
             f"1. `python3 scripts/batches.py claim {{this-issue}} --agent <researcher>/<agent>` (assigns you, labels `claimed`).",
             f"2. For each item: open the source, `python3 scripts/lab.py find \"<url or id>\"`, then "
             f"`python3 scripts/lab.py new {kind} <id> --agent <id>` into `{lib}` and fill every TODO to the AGENTS.md bar "
             f"(no phantom sources, honest `read_depth`, archived text for threads, evidence quality for blogs, `[[id]]` links).",
             "3. Tick the box here as you go. Skip an item if it is off-topic, dead or already catalogued (say which in a comment).",
             *(["   Talks: `yt-dlp --skip-download --write-auto-subs --sub-format vtt --sub-lang en <url>` gets the transcript; "
                "note the timestamps you actually watched or read in the entry."] if src == "talk" else []),
             "4. Keep `python3 scripts/lab.py sync --agent <id> --every 180` running so entries land on `main` every 3 min.",
             f"5. `python3 scripts/batches.py done {{this-issue}} --agent <id> --entries {lib}<id>.md ...` closes this.",
             "",
             "Run `batches.py touch` every 30 minutes. A claim with no issue activity for 90 minutes is stale and anyone may `claim` it again.", "",
             "## Items", ""]
    for i, r in enumerate(items, 1):
        meta = []
        if r.get("author"):
            meta.append(r["author"])
        if r.get("date"):
            meta.append(r["date"])
        if r.get("likes"):
            meta.append(f"{r['likes']} likes")
        meta.append(f"score {r.get('score', '?')}")
        title = (r.get("title") or r["url"]).replace("\n", " ").strip()
        if len(title) > 150:
            title = title[:147] + "..."
        lines.append(f"- [ ] **{i}.** {r['url']}  \n  {title}  \n  _{', '.join(meta)}_")
        extra = [u for u in (r.get("links") or [])][:3]
        if extra:
            lines.append("  links: " + ", ".join(extra))
        if r.get("via"):
            lines.append(f"  via: {r['via']}")
    lines += ["", "## Done when", "",
              f"- Every item is ticked or explicitly skipped with a reason.",
              f"- Each kept item has an entry in `{lib}` that passes `python3 scripts/lab.py check`, with `topics:` including `{topic}`.",
              "- Threads: full text archived. Blogs: evidence-quality section filled. Related entries linked as `[[id]]`.",
              "- `done` comment lists the entry paths."]
    return "\n".join(lines)


def cmd_publish(a):
    m = read_map()
    all_b = batches()
    todo = a.batch or [b for b in all_b if b not in m]
    made = 0
    for bid in todo:
        if bid in m and not a.force:
            print(f"  {bid}: already issue #{m[bid][0]}")
            continue
        p = all_b.get(bid)
        if not p:
            print(f"  {bid}: no such batch file")
            continue
        items = rows(p)
        src = p.parent.name
        topic = items[0].get("topic") if items else "meta"
        title = f"[batch] {src}/{topic}: {len(items)} candidates ({bid})"
        labels = ["batch", f"source:{src}", f"topic:{topic}"]
        url = gh("issue", "create", "-R", REPO, "--title", title, "--body", issue_body(bid, src, topic, items),
                 "--label", ",".join(labels))
        num = url.rstrip("/").split("/")[-1]
        body = issue_body(bid, src, topic, items).replace("{this-issue}", num)
        gh("issue", "edit", num, "-R", REPO, "--body", body)
        with MAP.open("a") as f:
            f.write(f"{bid}\t{num}\t{url}\n")
        made += 1
        print(f"  {bid} -> {url}")
    print(f"publish: {made} issues created")
    return 0


# ------------------------------------------------------------------------------------------------ claims
def issue(num: str) -> dict:
    return gh_json("issue", "view", num, "-R", REPO, "--json",
                   "number,title,state,labels,assignees,comments,updatedAt,createdAt,url")


def last_activity(i: dict) -> dt.datetime:
    ts = [i["updatedAt"]] + [c["createdAt"] for c in i.get("comments", [])]
    return max(dt.datetime.fromisoformat(t.replace("Z", "+00:00")) for t in ts)


def is_stale(i: dict) -> bool:
    return (now_utc() - last_activity(i)) > dt.timedelta(minutes=STALE_MIN)


def cmd_claim(a):
    i = issue(a.issue)
    if i["state"] != "OPEN":
        sys.exit(f"#{a.issue} is {i['state']}")
    names = {l["name"] for l in i["labels"]}
    if "claimed" in names and not is_stale(i) and not a.force:
        who = ", ".join(x["login"] for x in i["assignees"]) or "someone"
        sys.exit(f"#{a.issue} is claimed by {who}, last activity {last_activity(i):%H:%M}Z; pick another or wait for it to go stale")
    note = "reclaimed (previous claim stale)" if "claimed" in names else "claimed"
    gh("issue", "edit", a.issue, "-R", REPO, "--add-label", "claimed", "--add-assignee", "@me")
    gh("issue", "comment", a.issue, "-R", REPO, "--body", f"{note} by `{a.agent}` at {now_utc():%Y-%m-%d %H:%M}Z")
    # Issues have no compare-and-swap: two agents can pass the label check at the same moment. Settle it by
    # replaying the comments in order: release/done frees the batch, the first claim on a free batch wins, a
    # reclaim takes over a stale holder, and reclaims within 2 minutes of each other are a race the first wins.
    import time
    time.sleep(3)
    cs = sorted(issue(a.issue).get("comments", []), key=lambda c: c["createdAt"])
    winner, last_reclaim = None, None
    for c in cs:
        body, at = c["body"], dt.datetime.fromisoformat(c["createdAt"].replace("Z", "+00:00"))
        if re.match(r"^(released by|done by)", body):
            winner, last_reclaim = None, None
        elif m := re.match(r"^reclaimed.*? by `([^`]+)`", body):
            if last_reclaim is None or (at - last_reclaim).total_seconds() > 120:
                winner = m.group(1)
            last_reclaim = at
        elif m := re.match(r"^claimed by `([^`]+)`", body):
            if winner is None:
                winner = m.group(1)
    if winner and winner != a.agent:
        gh("issue", "comment", a.issue, "-R", REPO, "--body", f"`{a.agent}` backing off: `{winner}` claimed first")
        sys.exit(f"#{a.issue}: {winner} claimed it first; pick another batch")
    print(f"#{a.issue} {note} by {a.agent}: {i['url']}")
    return 0


def cmd_touch(a):
    gh("issue", "comment", a.issue, "-R", REPO, "--body", f"still on it, `{a.agent}` {now_utc():%H:%M}Z" + (f": {a.note}" if a.note else ""))
    return 0


def cmd_done(a):
    # Writers may have committed their entries in a different worktree. Refresh
    # main once, then accept either this checkout or the published git object.
    fetched = subprocess.run(["git", "fetch", "origin", "main"], cwd=ROOT,
                             capture_output=True, text=True, timeout=60)
    if fetched.returncode:
        print(f"warning: could not refresh origin/main: {fetched.stderr.strip()}", file=sys.stderr)
    missing = []
    for entry in a.entries:
        if (ROOT / entry).exists():
            continue
        published = subprocess.run(["git", "cat-file", "-e", f"origin/main:{entry}"],
                                   cwd=ROOT, capture_output=True)
        if published.returncode:
            missing.append(entry)
    if missing and not a.force:
        sys.exit(f"entries not found locally or on origin/main: {missing}")
    body = [f"done by `{a.agent}` at {now_utc():%Y-%m-%d %H:%M}Z", "", "Entries:"] + [f"- `{e}`" for e in a.entries]
    if a.skipped:
        body += ["", f"Skipped: {a.skipped}"]
    gh("issue", "comment", a.issue, "-R", REPO, "--body", "\n".join(body))
    gh("issue", "edit", a.issue, "-R", REPO, "--remove-label", "claimed")
    gh("issue", "close", a.issue, "-R", REPO, "--reason", "completed")
    print(f"#{a.issue} closed with {len(a.entries)} entries")
    return 0


def cmd_release(a):
    gh("issue", "comment", a.issue, "-R", REPO, "--body", f"released by `{a.agent}`: {a.note}")
    gh("issue", "edit", a.issue, "-R", REPO, "--remove-label", "claimed", "--remove-assignee", "@me")
    print(f"#{a.issue} released")
    return 0


def cmd_list(a):
    q = ["issue", "list", "-R", REPO, "--label", "batch", "--limit", "200", "--state", "open" if (a.open or a.free) else "all",
         "--json", "number,title,state,labels,assignees,updatedAt,url"]
    for i in gh_json(*q):
        names = {l["name"] for l in i["labels"]}
        if a.free and "claimed" in names:
            continue
        who = ",".join(x["login"] for x in i["assignees"]) or "-"
        print(f"#{i['number']:<4} {i['state']:<6} {'claimed' if 'claimed' in names else 'free':<8} {who:<14} {i['title']}")
    return 0


def cmd_stale(a):
    for i in gh_json("issue", "list", "-R", REPO, "--label", "claimed", "--state", "open", "--limit", "200",
                     "--json", "number,title,state,labels,assignees,comments,updatedAt,createdAt,url"):
        if is_stale(i):
            print(f"#{i['number']} stale since {last_activity(i):%H:%M}Z  {i['title']}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("setup")
    p = sub.add_parser("publish"); p.add_argument("--batch", nargs="*"); p.add_argument("--force", action="store_true")
    p = sub.add_parser("list"); p.add_argument("--open", action="store_true"); p.add_argument("--free", action="store_true")
    for name in ("claim", "touch", "done", "release"):
        p = sub.add_parser(name); p.add_argument("issue"); p.add_argument("--agent", required=True)
        p.add_argument("--force", action="store_true")
        if name == "done":
            p.add_argument("--entries", nargs="+", required=True); p.add_argument("--skipped", default="")
        if name in ("release", "touch"):
            p.add_argument("--note", default="")
    sub.add_parser("stale")
    a = ap.parse_args(argv)
    return {"setup": cmd_setup, "publish": cmd_publish, "list": cmd_list, "claim": cmd_claim, "touch": cmd_touch,
            "done": cmd_done, "release": cmd_release, "stale": cmd_stale}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
