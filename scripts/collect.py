#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""collect.py: source discovery for swarm-lab. Collectors pull raw candidates (X posts, blog URLs) into
data/candidates-raw/ (git-ignored), `batch` dedups them against the library and candidates/SEEN.txt and cuts
them into small single-topic batches under candidates/<source>/<batch-id>.jsonl (committed). batches.py then
turns each batch into a claimable GitHub issue. See PIPELINE.md.

  python3 scripts/collect.py x-search --queries <file> --by <agent-id> [--max 30] [--archive] [--threads]
  python3 scripts/collect.py apify --actor <id> --input <json-file> --by <agent-id> --max-usd 0.50 [--topic t]
  python3 scripts/collect.py links --by <agent-id>                     outbound links in collected posts -> blog candidates
  python3 scripts/collect.py seed --urls <file> --topic <slug> --by <agent-id> [--source blog]   hand-fed URLs
  python3 scripts/collect.py batch --by <agent-id> [--size 10] [--min-score 1]
  python3 scripts/collect.py status

Query file for x-search: one query per line, `<topic-slug>\t<X search query>`; blank lines and # comments ignored.

Secrets are never read from the repo. In order: env X_BEARER_TOKEN / APIFY_TOKEN, else a JSON file named by
env SWARM_LAB_SECRETS, else data/secrets.json (data/ is git-ignored). The file may hold {"x_bearer_token": ..,
"apify_token": ..}. Never commit tokens.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lab import LIB_DIRS, Doc, md_files, norm_url  # noqa: E402

RAW = ROOT / "data" / "candidates-raw"
CAND = ROOT / "candidates"
SEEN = CAND / "SEEN.txt"
XLOG = ROOT / "data" / "x-api-calls.log"
TOPIC_KEYWORDS = {
    "fork-merge-security": ["fork", "merge", "reintegrat", "sub-agent", "subagent", "spawn", "split", "byzantine", "poison", "model merging"],
    "sybil-resistance": ["sybil", "proof of personhood", "identity", "false-name", "reputation", "flashbots", "mev", "searcher"],
    "swarm-detection": ["detect", "bot detection", "honeypot", "canary", "tarpit", "crawler", "fingerprint", "attribution", "coordinated"],
    "llm-agent-swarms": ["multi-agent", "agent swarm", "orchestrat", "ai village", "agents", "hugging face incident", "swarm"],
    "collective-motion": ["flock", "boids", "vicsek", "school", "murmuration"],
    "swarm-robotics": ["kilobot", "drone swarm", "robot swarm"],
    "sync-consensus": ["kuramoto", "swarmalator", "consensus", "synchron"],
    "active-matter": ["active matter", "self-propelled", "active nematic"],
    "crowds-and-traffic": ["crowd", "pedestrian", "evacuation", "traffic"],
    "marl-emergence": ["multi-agent rl", "marl", "emergent communication"],
    "swarm-intelligence": ["particle swarm", "ant colony", "stigmergy"],
}
# a post must mention at least one of these to score above 1 (the X queries are broad and pull in crypto spam)
RELEVANT = ["agent", "swarm", "llm", " ai ", "ai-", "bot", "model", "sybil", "village", "hugging face", "openai",
            "anthropic", "claude", "codex", "alignment", "byzantine", "flock", "boids", "collective"]
NOISE = ["airdrop", "presale", " ca:", "pump.fun", "token launch", "legendary websites", "pdf tools", "product hunt",
         "must-use", "skills for your", "stock token", "giveaway", "whitelist", "$sei", "$icp", "testnet", "bankai",
         "room in sf", "newsletter", "zeru", "jevstocks", "monark", "termix"]
SKIP_HOSTS = ("x.com", "twitter.com", "t.co", "youtu.be", "youtube.com", "instagram.com", "tiktok.com",
              "linkedin.com", "facebook.com", "discord.gg", "t.me", "bit.ly", "amazon.com", "apple.com")


# ------------------------------------------------------------------------------------------------ helpers
def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def secret(name: str) -> str:
    env = {"x_bearer_token": "X_BEARER_TOKEN", "apify_token": "APIFY_TOKEN"}[name]
    if os.environ.get(env):
        return os.environ[env]
    for p in (os.environ.get("SWARM_LAB_SECRETS"), ROOT / "data" / "secrets.json"):
        if p and Path(p).exists():
            d = json.loads(Path(p).read_text())
            if d.get(name):
                return d[name]
    sys.exit(f"missing secret {name}: set env {env}, or put it in the file named by env SWARM_LAB_SECRETS, or data/secrets.json")


def http(url: str, headers=None, data=None, method=None, timeout=60):
    req = urllib.request.Request(url, headers=headers or {}, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r), dict(r.headers)
    except urllib.error.HTTPError as e:
        return {"error": e.code, "body": e.read().decode(errors="replace")[:600]}, dict(e.headers)


def jl_write(path: Path, rows: list[dict], append=True):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a" if append else "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def jl_read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:  # a killed collector can leave a truncated last line
            print(f"  ! skipping a corrupt line in {path.name}", file=sys.stderr)
    return out


def cand_id(source: str, url: str) -> str:
    m = re.search(r"x\.com/[^/]+/status/(\d+)", url)
    if m:
        return f"x:{m.group(1)}"
    return "url:" + norm_url(url)


def guess_topic(text: str, default: str | None) -> str:
    t = text.lower()
    best, score = default or "llm-agent-swarms", 0
    for slug, kws in TOPIC_KEYWORDS.items():
        s = sum(1 for k in kws if k in t)
        if slug == default:
            s += 1
        if s > score:
            best, score = slug, s
    return best


def library_seen() -> set[str]:
    out = set()
    for d in LIB_DIRS:
        for p in md_files(ROOT / "library" / d):
            doc = Doc(p)
            for k in ("url", "repo"):
                if doc.get(k):
                    out.add(cand_id("", str(doc.get(k))))
            if doc.get("type") == "thread":
                m = re.search(r"(\d{15,})$", p.stem)
                if m:
                    out.add(f"x:{m.group(1)}")
    return out


def load_seen() -> set[str]:
    if not SEEN.exists():
        return set()
    return {line.split("\t")[0] for line in SEEN.read_text().splitlines() if line.strip() and not line.startswith("#")}


# ------------------------------------------------------------------------------------------------ X
X_FIELDS = ("tweet.fields=created_at,author_id,conversation_id,public_metrics,entities,referenced_tweets,note_tweet"
            "&expansions=author_id&user.fields=username,name")


def x_get(url: str, _retry: int = 0) -> dict:
    d, h = http(url, headers={"Authorization": f"Bearer {secret('x_bearer_token')}"})
    XLOG.parent.mkdir(parents=True, exist_ok=True)
    with XLOG.open("a") as f:
        f.write(f"{now()}\t{'err' if 'error' in d else 'ok'}\t{h.get('x-rate-limit-remaining', '?')}\t{url[:160]}\n")
    if d.get("error") == 429:
        remaining = int(h.get("x-rate-limit-remaining", "0") or 0)
        if remaining > 0 and _retry < 2:  # per-second throttle on search/all, not the 15-min window
            time.sleep(3)
            return x_get(url, _retry + 1)
        reset = int(h.get("x-rate-limit-reset", "0") or 0)
        wait = max(5, min(900, reset - int(time.time())))
        if _retry >= 4:
            print("  429: giving up on this call after 4 retries", file=sys.stderr)
            return d
        print(f"  429: sleeping {wait}s", file=sys.stderr)
        time.sleep(wait)
        return x_get(url, _retry + 1)
    time.sleep(1.2)  # search/all allows 1 request per second
    return d


def x_rows(d: dict, topic: str, query: str, by: str) -> list[dict]:
    users = {u["id"]: u for u in d.get("includes", {}).get("users", [])}
    rows = []
    for t in d.get("data", []):
        u = users.get(t["author_id"], {})
        text = (t.get("note_tweet") or {}).get("text") or t.get("text", "")
        pm = t.get("public_metrics", {})
        urls = [e.get("expanded_url") for e in t.get("entities", {}).get("urls", []) if e.get("expanded_url")]
        urls = [x for x in urls if not re.search(r"x\.com/[^/]+/status/" + t["id"], x)]
        is_reply = any(r.get("type") == "replied_to" for r in t.get("referenced_tweets") or [])
        url = f"https://x.com/{u.get('username', 'i')}/status/{t['id']}"
        rows.append({
            "id": f"x:{t['id']}", "source": "x", "url": url, "title": text[:140].replace("\n", " "),
            "text": text, "author": "@" + u.get("username", "?"), "date": (t.get("created_at") or "")[:10],
            "topic": guess_topic(text + " " + query, topic), "likes": pm.get("like_count", 0),
            "reposts": pm.get("retweet_count", 0), "replies": pm.get("reply_count", 0),
            "conversation_id": t.get("conversation_id"), "is_reply": is_reply, "links": urls,
            "found_by": by, "query": query, "collected": now(),
        })
    return rows


def cmd_x_search(a):
    lines = [ln for ln in Path(a.queries).read_text().splitlines() if ln.strip() and not ln.startswith("#")]
    ep = "all" if a.archive else "recent"
    out = RAW / f"x-{dt.date.today()}.jsonl"
    total, calls = 0, 0
    for ln in lines:
        topic, q = (ln.split("\t", 1) + [None])[:2] if "\t" in ln else (None, ln)
        q = q.strip()
        url = (f"https://api.x.com/2/tweets/search/{ep}?query={urllib.parse.quote(q)}"
               f"&max_results={max(10, min(100, a.max))}&{X_FIELDS}")
        d = x_get(url)
        calls += 1
        if "error" in d:
            print(f"  ! {q[:60]}: {d['error']} {d.get('body', '')[:120]}")
            continue
        rows = x_rows(d, topic, q, a.by)
        if a.threads:
            # pull the author's own continuation for the strongest roots (self-replies are the thread body)
            roots = sorted((r for r in rows if not r["is_reply"]), key=lambda r: -r["likes"])[:a.threads]
            for r in roots:
                cq = f"conversation_id:{r['conversation_id']} from:{r['author'][1:]}"
                cu = f"https://api.x.com/2/tweets/search/all?query={urllib.parse.quote(cq)}&max_results=100&{X_FIELDS}"
                cd = x_get(cu)
                calls += 1
                if "error" not in cd and cd.get("data"):
                    parts = sorted(cd["data"], key=lambda t: t["id"])
                    r["thread_text"] = "\n\n".join((p.get("note_tweet") or {}).get("text") or p.get("text", "") for p in parts)
                    for p in parts:
                        for e in p.get("entities", {}).get("urls", []):
                            if e.get("expanded_url") and e["expanded_url"] not in r["links"]:
                                r["links"].append(e["expanded_url"])
        jl_write(out, rows)
        total += len(rows)
        print(f"  {len(rows):3d}  [{topic}] {q[:70]}")
    print(f"x-search: {total} posts from {len(lines)} queries, {calls} API calls -> {out.relative_to(ROOT)}")
    return 0


# ------------------------------------------------------------------------------------------------ Apify
def apify_spent(tok: str) -> float:
    d, _ = http(f"https://api.apify.com/v2/users/me/limits?token={tok}")
    if "error" in d:
        sys.exit(f"apify limits call failed: {d}")
    cur, lim = d["data"]["current"], d["data"]["limits"]
    return float(cur["monthlyUsageUsd"]), float(lim["maxMonthlyUsageUsd"])


def cmd_apify(a):
    tok = secret("apify_token")
    spent, cap = apify_spent(tok)
    print(f"apify: ${spent:.3f} of ${cap:.2f} monthly spent before this run")
    if spent + a.max_usd > min(cap, a.hard_cap):
        sys.exit(f"refusing: {spent:.2f} + {a.max_usd:.2f} would exceed the hard cap {min(cap, a.hard_cap):.2f}")
    inp = json.loads(Path(a.input).read_text())
    actor = a.actor.replace("/", "~")
    url = f"https://api.apify.com/v2/acts/{actor}/runs?token={tok}&maxTotalChargeUsd={a.max_usd}&timeout={a.timeout}"
    d, _ = http(url, headers={"Content-Type": "application/json"}, data=json.dumps(inp).encode(), method="POST")
    if "error" in d:
        sys.exit(f"apify start failed: {d}")
    run = d["data"]
    rid, ds = run["id"], run["defaultDatasetId"]
    print(f"  run {rid} started (actor {a.actor}, budget ${a.max_usd})")
    t0 = time.time()
    while time.time() - t0 < a.timeout + 30:
        time.sleep(8)
        s, _ = http(f"https://api.apify.com/v2/actor-runs/{rid}?token={tok}")
        st = s.get("data", {}).get("status")
        if st in {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}:
            break
    else:
        http(f"https://api.apify.com/v2/actor-runs/{rid}/abort?token={tok}", method="POST")
        st = "ABORTED(timeout)"
    items, _ = http(f"https://api.apify.com/v2/datasets/{ds}/items?token={tok}&clean=true&limit=2000")
    items = items if isinstance(items, list) else []
    rows = []
    for it in items:
        if a.kind == "x":
            tid = str(it.get("id") or it.get("id_str") or "")
            author = it.get("author", {}) if isinstance(it.get("author"), dict) else {}
            handle = author.get("userName") or author.get("username") or it.get("username") or "?"
            text = it.get("fullText") or it.get("full_text") or it.get("text") or ""
            if not tid:
                continue
            rows.append({"id": f"x:{tid}", "source": "apify-x", "url": it.get("url") or f"https://x.com/{handle}/status/{tid}",
                         "title": text[:140].replace("\n", " "), "text": text, "author": "@" + handle,
                         "date": str(it.get("createdAt") or "")[:10], "topic": guess_topic(text, a.topic),
                         "likes": it.get("likeCount") or 0, "reposts": it.get("retweetCount") or 0,
                         "replies": it.get("replyCount") or 0, "conversation_id": it.get("conversationId"),
                         "is_reply": bool(it.get("isReply")), "links": [u.get("expanded_url", u) if isinstance(u, dict) else u
                                                                     for u in it.get("entities", {}).get("urls", [])],
                         "found_by": a.by, "query": f"apify:{a.actor}", "collected": now()})
        else:
            u = it.get("url") or it.get("loadedUrl")
            if not u:
                continue
            text = (it.get("text") or it.get("markdown") or "")[:4000]
            rows.append({"id": cand_id("blog", u), "source": "web", "url": u,
                         "title": (it.get("metadata", {}) or {}).get("title") or it.get("title") or u,
                         "text": text[:600], "author": (it.get("metadata", {}) or {}).get("author") or "",
                         "date": "", "topic": guess_topic(text, a.topic), "likes": 0, "links": [],
                         "found_by": a.by, "query": f"apify:{a.actor}", "collected": now()})
    out = RAW / f"apify-{a.kind}-{dt.date.today()}.jsonl"
    jl_write(out, rows)
    spent2, _ = apify_spent(tok)
    print(f"  {st}: {len(items)} items, {len(rows)} candidates -> {out.relative_to(ROOT)}; "
          f"run cost about ${spent2 - spent:.3f}, month total ${spent2:.3f}")
    return 0


# ------------------------------------------------------------------------------------------------ links, seed
def cmd_links(a):
    rows, seen = [], set()
    for p in sorted(RAW.glob("x-*.jsonl")) + sorted(RAW.glob("apify-x-*.jsonl")):
        for r in jl_read(p):
            for u in r.get("links") or []:
                host = urllib.parse.urlparse(u).netloc.lower().removeprefix("www.")
                if any(host == h or host.endswith("." + h) for h in SKIP_HOSTS):
                    continue
                cid = cand_id("blog", u)
                if cid in seen:
                    continue
                seen.add(cid)
                src = "blog"
                if "arxiv.org" in host or "doi.org" in host:
                    src = "paper"
                elif host == "github.com":
                    src = "code"
                rows.append({"id": cid, "source": src, "url": u, "title": u, "text": r.get("title", ""),
                             "author": "", "date": r.get("date", ""), "topic": r.get("topic"),
                             "likes": r.get("likes", 0), "via": r["url"], "links": [], "found_by": a.by,
                             "query": f"link-from:{r['id']}", "collected": now()})
    out = RAW / f"links-{dt.date.today()}.jsonl"
    jl_write(out, rows)
    print(f"links: {len(rows)} outbound urls -> {out.relative_to(ROOT)}")
    return 0


def cmd_seed(a):
    rows, topic = [], a.topic
    for ln in Path(a.urls).read_text().splitlines():
        ln = ln.strip()
        m = re.match(r"^#\s*topic:\s*([a-z0-9-]+)", ln)
        if m:  # `# topic: <slug>` switches the topic for the lines that follow
            topic = m.group(1)
            continue
        if not ln or ln.startswith("#"):
            continue
        url, _, note = ln.partition(" ")
        rows.append({"id": cand_id(a.source, url), "source": a.source, "url": url, "title": note or url, "text": note,
                     "author": "", "date": "", "topic": topic, "likes": 0, "links": [], "found_by": a.by,
                     "query": f"seed:{Path(a.urls).name}", "collected": now(), "seed_score": a.score})
    out = RAW / f"seed-{a.source}-{dt.date.today()}.jsonl"
    jl_write(out, rows)
    print(f"seed: {len(rows)} urls -> {out.relative_to(ROOT)}")
    return 0


# ------------------------------------------------------------------------------------------------ batch
def score(r: dict) -> int:
    if r.get("seed_score") is not None:
        return int(r["seed_score"])
    s = 0.0
    likes = int(r.get("likes") or 0)
    s += min(2.5, math.log10(likes + 1))
    if r.get("links") or r.get("thread_text"):
        s += 0.7
    if len(r.get("text") or "") > 280:
        s += 0.6
    if r.get("is_reply"):
        s -= 0.8
    txt = " " + (r.get("text") or "").lower() + " "
    hits = sum(1 for k in TOPIC_KEYWORDS.get(r.get("topic") or "", []) if k in txt)
    s += min(1.2, 0.4 * hits)
    if r.get("source") in {"blog", "web", "code", "paper"} and r.get("via"):
        s += 0.5  # a human thought it worth linking
    if r.get("source") in {"x", "apify-x"}:
        if not any(k in txt for k in RELEVANT) or hits == 0:
            s = min(s, 1.0)
        if any(k in txt for k in NOISE) or txt.count("$") >= 2 or "#" * 1 in txt and txt.count("#") >= 4:
            s = min(s, 1.0)
    return max(0, min(5, round(s)))


def cmd_batch(a):
    lib = library_seen()
    seen = load_seen()
    raw = []
    for p in sorted(RAW.glob("*.jsonl")):
        raw += jl_read(p)
    fresh, dropped = {}, {"library": 0, "seen": 0, "low": 0, "dupe": 0}
    for r in raw:
        cid = r["id"]
        if cid in lib:
            dropped["library"] += 1
        elif cid in seen:
            dropped["seen"] += 1
        elif cid in fresh:
            dropped["dupe"] += 1
            if int(r.get("likes") or 0) > int(fresh[cid].get("likes") or 0):
                fresh[cid] = r
        else:
            r["score"] = score(r)
            if r["score"] < a.min_score:
                dropped["low"] += 1
                continue
            fresh[cid] = r
    if a.source:
        fresh = {k: v for k, v in fresh.items() if v["source"] in a.source}
    groups: dict[tuple[str, str], list[dict]] = {}
    for r in fresh.values():
        src = "x" if r["source"] in {"x", "apify-x"} else ("blog" if r["source"] in {"blog", "web"} else r["source"])
        groups.setdefault((src, r.get("topic") or "llm-agent-swarms"), []).append(r)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d")
    written = []
    for (src, topic), rows in sorted(groups.items()):
        rows.sort(key=lambda r: (-r["score"], -int(r.get("likes") or 0)))
        if len(rows) < a.min_batch:
            print(f"  skip {src}/{topic}: only {len(rows)} candidates (below --min-batch {a.min_batch}); kept in raw")
            continue
        chunks = [rows[i:i + a.size] for i in range(0, len(rows), a.size)]
        if len(chunks) > 1 and len(chunks[-1]) < max(3, a.size // 3):
            tail = chunks.pop()
            chunks[-1] += tail
        for i, ch in enumerate(chunks, 1):
            n = 1
            while (CAND / src / f"{src}-{topic}-{stamp}-{n:02d}.jsonl").exists():
                n += 1
            bid = f"{src}-{topic}-{stamp}-{n:02d}"
            path = CAND / src / f"{bid}.jsonl"
            for r in ch:
                r["batch"] = bid
            jl_write(path, ch, append=False)
            with SEEN.open("a") as f:
                for r in ch:
                    f.write(f"{r['id']}\t{bid}\t{r['found_by']}\n")
            written.append((bid, len(ch)))
            print(f"  wrote {path.relative_to(ROOT)} ({len(ch)} items)")
    print(f"batch: {len(raw)} raw -> {len(fresh)} fresh ({dropped}) -> {len(written)} batches")
    return 0


def cmd_status(a):
    seen = load_seen()
    print(f"seen ledger: {len(seen)} ids")
    for src in sorted(p.name for p in CAND.iterdir() if p.is_dir() and p.name != "queries"):
        files = sorted((CAND / src).glob("*.jsonl"))
        print(f"{src}: {len(files)} batches, {sum(len(jl_read(f)) for f in files)} items")
    if XLOG.exists():
        print(f"x api calls logged locally: {len(XLOG.read_text().splitlines())}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("x-search"); p.add_argument("--queries", required=True); p.add_argument("--by", required=True)
    p.add_argument("--max", type=int, default=30); p.add_argument("--archive", action="store_true")
    p.add_argument("--threads", type=int, default=0, help="also pull self-reply threads for the top N roots per query")
    p = sub.add_parser("apify"); p.add_argument("--actor", required=True); p.add_argument("--input", required=True)
    p.add_argument("--by", required=True); p.add_argument("--max-usd", type=float, default=0.5)
    p.add_argument("--hard-cap", type=float, default=4.0, help="never let month total pass this")
    p.add_argument("--kind", choices=["x", "web"], default="x"); p.add_argument("--topic", default=None)
    p.add_argument("--timeout", type=int, default=300)
    p = sub.add_parser("links"); p.add_argument("--by", required=True)
    p = sub.add_parser("seed"); p.add_argument("--urls", required=True)
    p.add_argument("--topic", required=True, help="default topic; a `# topic: <slug>` line in the file overrides for following lines")
    p.add_argument("--by", required=True); p.add_argument("--source", default="blog"); p.add_argument("--score", type=int, default=3)
    p = sub.add_parser("batch"); p.add_argument("--by", required=True); p.add_argument("--size", type=int, default=10)
    p.add_argument("--min-score", type=int, default=1); p.add_argument("--min-batch", type=int, default=3)
    p.add_argument("--source", nargs="*", default=None)
    sub.add_parser("status")
    a = ap.parse_args(argv)
    return {"x-search": cmd_x_search, "apify": cmd_apify, "links": cmd_links, "seed": cmd_seed,
            "batch": cmd_batch, "status": cmd_status}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
