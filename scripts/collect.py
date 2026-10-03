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
  python3 scripts/collect.py openalex --seeds <file> --by <agent-id> [--max 600] [--refs 'refs/remotes/origin/lane/*']
  python3 scripts/collect.py oa-locate --list <file> --by <agent-id>   free copies of named (paywalled) papers
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
         "room in sf", "newsletter", "zeru", "jevstocks", "monark", "termix",
         # writer feedback 2026-10-03 (w1): token/campaign shill, product promos, scraper/browser-tool ads
         "$wld", "$trx", "$b.ai", "b.ai", "worldcoin app", "tron", "staking", "tokenomics", "mint now", "join the waitlist",
         "sign up free", "free trial", "use code", "promo", "% off", "launching today", "we just launched", "our scraper",
         "scraping api", "proxy", "residential ip", "web unlocker", "no-code", "try it free", "link in bio", "dm me",
         "follow for more", "thread 🧵 below", "pre-order", "early access", "sponsored", "#ad "]
# a post that is only a pointer ("great thread", "must read", "thoughts?") with no claim of its own
DIGEST = ["must read", "great thread", "worth reading", "thoughts?", "interesting take", "this is huge", "bookmark this",
          "weekly roundup", "top 10", "top 5", "here's everything", "daily digest", "in case you missed", "icymi"]
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


# ------------------------------------------------------------------------------------------------ free sources
# Three collectors that cost nothing: LessWrong/Alignment Forum GraphQL (tag feeds + search), plain RSS/Atom feeds,
# and yt-dlp search for talks. Plus `jina`, which fetches clean markdown for blog candidates through r.jina.ai so
# the batcher can score them on real text instead of a bare url.
UA = {"User-Agent": "swarm-lab-collector (github.com/dmarzzz/swarm-lab)"}
LW_SITES = {"lesswrong": "https://www.lesswrong.com", "alignmentforum": "https://www.alignmentforum.org"}


def lw_gql(site: str, query: str) -> dict:
    d, _ = http(f"{LW_SITES[site]}/graphql", headers={"Content-Type": "application/json", **UA},
                data=json.dumps({"query": query}).encode(), method="POST")
    if "error" in d or d.get("errors"):
        print(f"  ! {site} graphql: {str(d)[:160]}", file=sys.stderr)
        return {}
    return d.get("data") or {}


def lw_rows(posts: list[dict], site: str, topic: str | None, by: str, query: str) -> list[dict]:
    rows = []
    for p in posts:
        url = p.get("pageUrl") or ""
        if not url:
            continue
        desc = ((p.get("contents") or {}).get("plaintextDescription") or "")[:1500]
        user = p.get("user") or {}
        tags = " ".join(t.get("slug", "") for t in p.get("tags") or [])
        rows.append({"id": cand_id("blog", url), "source": "blog", "url": url, "title": p.get("title") or url,
                     "text": desc, "author": user.get("displayName") or user.get("username") or "",
                     "date": (p.get("postedAt") or "")[:10], "topic": guess_topic(f"{p.get('title', '')} {desc} {tags}", topic),
                     "likes": int(p.get("baseScore") or 0), "words": p.get("wordCount") or 0, "af": bool(p.get("af")),
                     "tags": tags, "links": [], "found_by": by, "query": query, "collected": now()})
    return rows


LW_FIELDS = "_id title pageUrl baseScore postedAt wordCount af user { username displayName } tags { slug } contents { plaintextDescription }"


def cmd_lesswrong(a):
    """--tags slug[:topic] ... pulls the tagRelevance view for each tag; --search 'topic<TAB>terms' lines filter the
    recent/top posts list by title+description keywords (LW has no public full-text search endpoint we can reach)."""
    out = RAW / f"lw-{dt.date.today()}.jsonl"
    total = 0
    for spec in a.tags or []:
        slug, _, topic = spec.partition(":")
        d = lw_gql(a.site, '{ tags(input:{terms:{view:"tagBySlug", slug:"%s"}}) { results { _id name postCount } } }' % slug)
        res = (d.get("tags") or {}).get("results") or []
        if not res:
            print(f"  ! no tag {slug}")
            continue
        tid = res[0]["_id"]
        d = lw_gql(a.site, '{ posts(input:{terms:{view:"tagRelevance", tagId:"%s", limit:%d}}) { results { %s } } }'
                   % (tid, a.limit, LW_FIELDS))
        posts = (d.get("posts") or {}).get("results") or []
        # tagRelevance pads short tags with site-wide top posts; keep only posts that actually carry the tag
        posts = [p for p in posts if int(p.get("baseScore") or 0) >= a.min_karma
                 and slug in {t.get("slug") for t in p.get("tags") or []}]
        rows = lw_rows(posts, a.site, topic or None, a.by, f"lw-tag:{slug}")
        if a.keywords:
            kws = [k.strip().lower() for k in a.keywords.split(",") if k.strip()]
            rows = [r for r in rows if any(k in (r["title"] + " " + r["text"]).lower() for k in kws)]
        jl_write(out, rows)
        total += len(rows)
        print(f"  {len(rows):3d}  [{topic or 'guess'}] tag {slug} ({res[0]['postCount']} posts on {a.site})")
    if a.search:
        lines = [ln for ln in Path(a.search).read_text().splitlines() if ln.strip() and not ln.startswith("#")]
        pool = []
        for view in ("new", "top"):
            d = lw_gql(a.site, '{ posts(input:{terms:{view:"%s", limit:%d, af:%s}}) { results { %s } } }'
                       % (view, a.pool, "true" if a.site == "alignmentforum" else "false", LW_FIELDS))
            pool += (d.get("posts") or {}).get("results") or []
        for ln in lines:
            topic, _, terms = ln.partition("\t")
            kws = [k.strip().lower() for k in terms.split(",") if k.strip()]
            # title or the opening of the post, so a stray word deep in the body does not count
            hit = [p for p in pool if any(k in f"{p.get('title', '')} {((p.get('contents') or {}).get('plaintextDescription') or '')[:400]}".lower() for k in kws)]
            rows = lw_rows(hit, a.site, topic.strip() or None, a.by, f"lw-search:{terms[:60]}")
            jl_write(out, rows)
            total += len(rows)
            print(f"  {len(rows):3d}  [{topic}] search {terms[:60]} (pool {len(pool)})")
    print(f"lesswrong: {total} posts -> {out.relative_to(ROOT)}")
    return 0


def cmd_rss(a):
    """--feeds file: `<topic-slug><TAB><feed url>[<TAB>kw1,kw2]` per line. Plain xml.etree, no feedparser needed."""
    import html
    import xml.etree.ElementTree as ET
    out = RAW / f"rss-{dt.date.today()}.jsonl"
    total = 0
    for ln in Path(a.feeds).read_text().splitlines():
        if not ln.strip() or ln.startswith("#"):
            continue
        parts = ln.split("\t")
        topic, feed = parts[0].strip(), parts[1].strip()
        kws = [k.strip().lower() for k in (parts[2] if len(parts) > 2 else "").split(",") if k.strip()]
        try:
            req = urllib.request.Request(feed, headers=UA)
            with urllib.request.urlopen(req, timeout=40) as r:
                body = r.read()
            root = ET.fromstring(body)
        except Exception as e:  # noqa: BLE001
            print(f"  ! {feed[:70]}: {str(e)[:80]}")
            continue
        ns = {"a": "http://www.w3.org/2005/Atom", "dc": "http://purl.org/dc/elements/1.1/",
              "content": "http://purl.org/rss/1.0/modules/content/"}
        items = root.findall(".//item") or root.findall(".//a:entry", ns)
        rows = []
        for it in items[:a.limit]:
            def g(*names):
                for n in names:
                    el = it.find(n, ns)
                    if el is not None:
                        if el.text and el.text.strip():
                            return el.text.strip()
                        if el.get("href"):
                            return el.get("href")
                return ""
            url = g("link", "a:link", "guid", "a:id")
            if not url.startswith("http"):
                continue
            title = html.unescape(g("title", "a:title"))
            desc = re.sub(r"<[^>]+>", " ", html.unescape(g("description", "content:encoded", "a:summary", "a:content")))
            desc = re.sub(r"\s+", " ", desc).strip()[:1500]
            lede = (title + " " + desc[:300]).lower()
            if kws and not any(re.search(r"\b" + re.escape(k), lede) for k in kws):
                continue  # title or the lede only, word-start match ("ant" must not hit "quantum")
            date = g("pubDate", "dc:date", "a:published", "a:updated")
            try:
                import email.utils
                dd = email.utils.parsedate_to_datetime(date)
                date = dd.strftime("%Y-%m-%d")
            except Exception:  # noqa: BLE001
                date = date[:10]
            rows.append({"id": cand_id("blog", url), "source": "blog", "url": url, "title": title or url, "text": desc,
                         "author": g("dc:creator", "author", "a:author/a:name"), "date": date,
                         "topic": guess_topic(title + " " + desc, topic), "likes": 0, "links": [], "found_by": a.by,
                         "query": f"rss:{urllib.parse.urlparse(feed).netloc}", "collected": now(), "seed_score": a.score})
        jl_write(out, rows)
        total += len(rows)
        print(f"  {len(rows):3d}/{len(items):<3d} [{topic}] {feed[:70]}")
    print(f"rss: {total} items -> {out.relative_to(ROOT)}")
    return 0


def cmd_ytsearch(a):
    """--queries file: `<topic-slug><TAB><search terms>` per line; uses yt-dlp flat search (no download, no key)."""
    import shutil
    import subprocess
    ytdlp = a.ytdlp or shutil.which("yt-dlp") or os.path.expanduser("~/.local/bin/yt-dlp")
    out = RAW / f"talks-{dt.date.today()}.jsonl"
    total = 0
    for ln in Path(a.queries).read_text().splitlines():
        if not ln.strip() or ln.startswith("#"):
            continue
        topic, _, q = ln.partition("\t")
        q = q.strip()
        r = subprocess.run([ytdlp, f"ytsearch{a.n}:{q}", "--flat-playlist", "--dump-json", "--no-warnings"],
                           capture_output=True, text=True, timeout=180)
        rows = []
        for line in r.stdout.splitlines():
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            dur = int(d.get("duration") or 0)
            if dur and dur < a.min_minutes * 60:
                continue  # shorts and trailers are not talks
            url = f"https://www.youtube.com/watch?v={d.get('id')}"
            text = (d.get("description") or "")[:600]
            rows.append({"id": cand_id("talk", url), "source": "talk", "url": url, "title": d.get("title") or url,
                         "text": f"{d.get('channel') or d.get('uploader') or ''} | {dur // 60} min | {text}",
                         "author": d.get("channel") or d.get("uploader") or "", "date": "",
                         "topic": guess_topic(f"{d.get('title', '')} {text} {q}", topic.strip() or None),
                         "likes": int(d.get("view_count") or 0), "duration_min": dur // 60, "links": [],
                         "found_by": a.by, "query": f"ytsearch:{q}", "collected": now(), "seed_score": a.score})
        jl_write(out, rows)
        total += len(rows)
        print(f"  {len(rows):3d}  [{topic}] {q[:70]}" + (f"  ! {r.stderr.strip()[:80]}" if r.returncode else ""))
    print(f"ytsearch: {total} talks -> {out.relative_to(ROOT)}")
    return 0


def jina(url: str, timeout: int = 60) -> str:
    req = urllib.request.Request("https://r.jina.ai/" + url, headers={**UA, "X-Return-Format": "markdown"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode(errors="replace")
    except Exception as e:  # noqa: BLE001
        return f"!! {str(e)[:120]}"


def cmd_jina(a):
    """Fetch markdown through r.jina.ai for blog/web rows in raw that have no real text yet (links pass output, seeds).
    Rewrites title from the page, fills text (first 1500 chars), drops rows that are 404/parked/empty when --prune."""
    seen = load_seen() | library_seen()
    done = 0
    for p in sorted(RAW.glob("*.jsonl")):
        if p.name.startswith(("x-", "apify-x", "talks-")):
            continue
        rows = jl_read(p)
        changed = False
        for r in rows:
            if r.get("source") not in {"blog", "web"} or r.get("jina") or r["id"] in seen:
                continue
            if len(r.get("text") or "") > 400 and r.get("title") != r.get("url"):
                continue
            if done >= a.max:
                break
            md = jina(r["url"])
            done += 1
            r["jina"] = now()
            if md.startswith("!!") or len(md) < 300:
                r["jina_error"] = md[:120]
                r["score_hint"] = 0
                print(f"  dead  {r['url'][:80]} {md[:60]}")
            else:
                m = re.match(r"Title:\s*(.+)", md)
                if m and m.group(1).strip():
                    r["title"] = m.group(1).strip()[:200]
                body = md.split("Markdown Content:", 1)[-1] if "Markdown Content:" in md else md
                body = re.sub(r"\s+", " ", re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body)).strip()
                r["text"] = body[:1500]
                r["words"] = len(body.split())
                r["topic"] = guess_topic(r["title"] + " " + body[:3000], r.get("topic"))
                print(f"  ok    {r['url'][:80]} ({r['words']} words) {r['title'][:50]}")
            changed = True
            time.sleep(a.sleep)
        if changed:
            if a.prune:
                rows = [r for r in rows if not r.get("jina_error")]
            jl_write(p, rows, append=False)
    print(f"jina: fetched {done} pages")
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


# ------------------------------------------------------------------------------------------------ openalex
OA = "https://api.openalex.org"


def _title_key(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()[:120]


def known_papers(refs: list[str]) -> tuple[set[str], set[str], dict[str, dict]]:
    """dois, normalised titles and {library id: frontmatter} for library/papers in the working tree plus each git
    ref (e.g. origin/lane/*), so unmerged lanes count as already catalogued."""
    import subprocess
    dois, titles, byid = set(), set(), {}

    def take(lid: str, text: str):
        fm = {}
        for k in ("doi", "url", "title"):
            m = re.search(rf"^{k}:\s*(.+)$", text, re.M)
            if m:
                fm[k] = m.group(1).strip().strip("'\"")
        if fm.get("doi") and fm["doi"] != "null":
            dois.add(fm["doi"].lower())
        if fm.get("title"):
            titles.add(_title_key(fm["title"]))
        byid.setdefault(lid, fm)

    for p in (ROOT / "library" / "papers").glob("*.md"):
        take(p.stem, p.read_text(encoding="utf-8", errors="replace")[:3000])
    for ref in refs:
        r = subprocess.run(["git", "-C", str(ROOT), "grep", "-h", "--no-color", "-E", "-e", "^(doi|url|title):",
                            "-e", "^id:", ref, "--", "library/papers"], capture_output=True, text=True)
        names = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "--name-only", f"{ref}:library/papers"],
                               capture_output=True, text=True).stdout.split()
        for line in r.stdout.splitlines():
            k, _, v = line.partition(":")
            v = v.strip().strip("'\"")
            if k == "doi" and v and v != "null":
                dois.add(v.lower())
            elif k == "title":
                titles.add(_title_key(v))
        for n in names:  # resolve seed ids from lanes lazily, below
            byid.setdefault(n.removesuffix(".md"), {"_ref": ref})
    return dois, titles, byid


def _lib_fm(lid: str, byid: dict) -> dict:
    import subprocess
    fm = byid.get(lid) or {}
    if fm.get("_ref"):
        text = subprocess.run(["git", "-C", str(ROOT), "show", f"{fm['_ref']}:library/papers/{lid}.md"],
                              capture_output=True, text=True).stdout[:3000]
        fm = {}
        for k in ("doi", "url", "title"):
            m = re.search(rf"^{k}:\s*(.+)$", text, re.M)
            if m:
                fm[k] = m.group(1).strip().strip("'\"")
    return fm


def oa_get(path: str, params: dict) -> dict:
    if os.environ.get("OPENALEX_API_KEY"):
        params = {**params, "api_key": os.environ["OPENALEX_API_KEY"]}
    for attempt in range(5):
        d, _ = http(f"{OA}{path}?{urllib.parse.urlencode(params)}", headers={"User-Agent": "swarm-lab-collect/1"})
        if d.get("error") in (429, 503):
            time.sleep(5 * (attempt + 1))
            continue
        time.sleep(0.15)
        return d
    return d


def oa_resolve(seed: str, byid: dict) -> dict | None:
    """seed = a library id, doi:<doi>, arxiv:<id>, W<openalex id> or a title."""
    s = seed.strip()
    if re.fullmatch(r"W\d+", s):
        return oa_get(f"/works/{s}", {})
    fm = _lib_fm(s, byid) if re.fullmatch(r"[a-z0-9-]+-\d{4}-[a-z0-9-]+", s) else {}
    doi = s[4:] if s.startswith("doi:") else (fm.get("doi") if fm.get("doi") not in (None, "null") else None)
    arx = s[6:] if s.startswith("arxiv:") else None
    if not arx and fm.get("url"):
        m = re.search(r"arxiv\.org/(?:abs|pdf|html)/([0-9]{4}\.[0-9]{4,5})", fm["url"])
        arx = m.group(1) if m else None
    for cand in ([f"doi:{doi}"] if doi else []) + ([f"doi:10.48550/arxiv.{arx}"] if arx else []):
        d = oa_get(f"/works/{cand}", {})
        if d.get("id"):
            return d
    title = fm.get("title") or (s if " " in s else None)
    if title:
        d = oa_get("/works", {"search": title, "per-page": 1})
        res = d.get("results") or []
        if res and _title_key(res[0].get("title"))[:60] == _title_key(title)[:60]:
            return res[0]
    return None


def oa_abstract(w: dict) -> str:
    inv = w.get("abstract_inverted_index") or {}
    pos = sorted((i, word) for word, idx in inv.items() for i in idx)
    return " ".join(word for _, word in pos)


def oa_row(w: dict, topic: str, query: str, by: str, kws: list[str]) -> dict:
    abstract = oa_abstract(w)
    ids = w.get("ids") or {}
    loc = (w.get("primary_location") or {}).get("landing_page_url") or ""
    arx = next((l.get("landing_page_url") for l in w.get("locations") or [] if "arxiv.org" in (l.get("landing_page_url") or "")), None)
    url = arx or (ids.get("doi") or loc or w["id"])
    text = f"{w.get('title') or ''} {abstract}".lower()
    hits = sum(1 for k in (kws or TOPIC_KEYWORDS.get(topic, [])) if k in text)
    year = w.get("publication_year") or 0
    sc = min(3, hits) + (1 if (w.get("cited_by_count") or 0) >= 20 else 0) + (1 if year >= 2024 else 0)
    return {"id": cand_id("paper", url), "source": "paper", "url": url, "title": w.get("title") or "",
            "text": abstract[:1500], "author": ", ".join(a["author"]["display_name"] for a in (w.get("authorships") or [])[:4]),
            "date": w.get("publication_date") or str(year), "topic": topic, "likes": w.get("cited_by_count") or 0,
            "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None, "openalex": w["id"],
            "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
            "links": [], "found_by": by, "query": query, "collected": now(), "seed_score": sc if hits else 0}


def cmd_openalex(a):
    """--seeds file: `<topic><TAB><fwd|back|both><TAB><seed>[<TAB>kw1,kw2]` per line. Seed = library id (resolved
    from main or any --refs lane), doi:..., arxiv:..., W123 or an exact title. Forward = works citing the seed,
    newest relevant first; back = the seed's references. Rows with no keyword hit get seed_score 0 (dropped by
    `batch`). Rows already in library/ (by doi or title, across --refs) are dropped here."""
    import subprocess
    refs = []
    for pat in a.refs or []:
        refs += subprocess.run(["git", "-C", str(ROOT), "for-each-ref", "--format=%(refname)", pat],
                               capture_output=True, text=True).stdout.split()
    dois, titles, byid = known_papers(refs)
    print(f"known papers: {len(dois)} dois, {len(titles)} titles across worktree + {len(refs)} refs")
    out = RAW / f"openalex-{dt.date.today()}.jsonl"
    log = []
    for ln in Path(a.seeds).read_text().splitlines():
        if not ln.strip() or ln.startswith("#"):
            continue
        parts = ln.split("\t")
        topic, direction, seed = parts[0].strip(), parts[1].strip(), parts[2].strip()
        kws = [k.strip().lower() for k in parts[3].split(",")] if len(parts) > 3 and parts[3].strip() else []
        w = oa_resolve(seed, byid)
        if not w or not w.get("id"):
            print(f"  ! could not resolve {seed}")
            log.append({"seed": seed, "resolved": None})
            continue
        wid = w["id"].rsplit("/", 1)[-1]
        works = []
        if direction in ("fwd", "both"):
            cursor, got = "*", 0
            q = {"filter": f"cites:{wid}", "per-page": 200, "sort": "cited_by_count:desc"}
            if kws and (w.get("cited_by_count") or 0) > a.max:  # too many citers to page through: search within them
                q["search"] = " OR ".join(f'"{k}"' if " " in k else k for k in kws)
            while cursor and got < a.max:
                d = oa_get("/works", {**q, "cursor": cursor})
                res = d.get("results") or []
                works += [("fwd", r) for r in res]
                got += len(res)
                cursor = (d.get("meta") or {}).get("next_cursor") if res else None
        if direction in ("back", "both"):
            refs_ = [r.rsplit("/", 1)[-1] for r in w.get("referenced_works") or []]
            for i in range(0, len(refs_), 50):
                d = oa_get("/works", {"filter": "openalex:" + "|".join(refs_[i:i + 50]), "per-page": 50})
                works += [("back", r) for r in d.get("results") or []]
        rows, known = [], 0
        for kind, r in works:
            doi = (r.get("doi") or "").replace("https://doi.org/", "").lower()
            if (doi and doi in dois) or _title_key(r.get("title")) in titles:
                known += 1
                continue
            rows.append(oa_row(r, topic, f"openalex-{kind}:{seed}", a.by, kws))
        relevant = [r for r in rows if r["seed_score"]]
        jl_write(out, relevant)
        print(f"  {seed} ({wid}, cited {w.get('cited_by_count')}): {len(works)} looked at, {known} already in library, "
              f"{len(rows)} new, {len(relevant)} on-topic")
        log.append({"seed": seed, "openalex": wid, "direction": direction, "results": len(works), "known": known,
                    "new": len(rows), "on_topic": len(relevant)})
    jl_write(ROOT / "data" / f"openalex-log-{dt.date.today()}.jsonl", log)
    print(f"openalex: rows -> {out.relative_to(ROOT)}; per-seed counts (for survey search_log rows) -> data/openalex-log-*.jsonl")
    return 0


def cmd_oa_locate(a):
    """--list file: `<topic><TAB><seed>[<TAB>note]` per line (seed as in `openalex`). Finds each named paper in
    OpenAlex and the best free copy it knows of (arXiv, repository, author PDF, OA publisher page). Papers with a
    free copy become candidates whose url is that copy; the rest are listed in data/oa-locate-<date>.tsv as
    needing a browser or library access."""
    dois, titles, byid = known_papers([])
    out = RAW / f"oa-locate-{dt.date.today()}.jsonl"
    rep = ROOT / "data" / f"oa-locate-{dt.date.today()}.tsv"
    found, report = [], []
    for ln in Path(a.list).read_text().splitlines():
        if not ln.strip() or ln.startswith("#"):
            continue
        parts = ln.split("\t")
        topic, seed, note = parts[0].strip(), parts[1].strip(), (parts[2].strip() if len(parts) > 2 else "")
        w = oa_resolve(seed, byid)
        if not w or not w.get("id"):
            report.append((seed, "not-in-openalex", "", note))
            print(f"  ?  {seed}: not found in OpenAlex")
            continue
        doi = (w.get("doi") or "").replace("https://doi.org/", "").lower()
        if (doi and doi in dois) or _title_key(w.get("title")) in titles:
            report.append((seed, "already-in-library", "", note))
            print(f"  =  {seed}: already in library")
            continue
        locs = [w.get("best_oa_location") or {}] + [l for l in w.get("locations") or [] if l.get("is_oa")]
        oa = next((l.get("pdf_url") or l.get("landing_page_url") for l in locs if l and (l.get("pdf_url") or l.get("landing_page_url"))), None)
        row = oa_row(w, topic, f"oa-locate:{seed}", a.by, [])
        row["seed_score"] = 4  # named by a lane log as worth catalouging
        row["oa_url"], row["oa_status"] = oa, (w.get("open_access") or {}).get("oa_status")
        if note:
            row["text"] = (note + " | " + row["text"]).strip(" |")
        if oa:
            row["url"], row["id"] = (row["url"] if "arxiv.org" in row["url"] else oa), cand_id("paper", row["url"] if "arxiv.org" in row["url"] else oa)
            found.append(row)
            report.append((seed, "free-copy", oa, note))
            print(f"  +  {seed}: {oa}")
        else:
            report.append((seed, "paywalled-only", (w.get("doi") or w["id"]), note))
            print(f"  -  {seed}: no free copy ({w.get('doi') or w['id']})")
    jl_write(out, found)
    rep.parent.mkdir(parents=True, exist_ok=True)
    rep.write_text("seed\tstatus\turl\tnote\n" + "".join("\t".join(r) + "\n" for r in report))
    print(f"oa-locate: {len(found)} with a free copy -> {out.relative_to(ROOT)}; report -> {rep.relative_to(ROOT)}")
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
    if r.get("source") in {"blog", "web"}:
        if r.get("jina_error") or r.get("score_hint") == 0:
            return 0  # fetched through jina and it was dead or empty
        if int(r.get("words") or 0) >= 800:
            s += 0.6  # long-form, worth a blog entry
        if r.get("af"):
            s += 0.5  # crossposted to the Alignment Forum
        if r.get("query", "").startswith("lw-") and likes >= 50:
            s += 0.5
    if r.get("source") in {"x", "apify-x"}:
        if not any(k in txt for k in RELEVANT) or hits == 0:
            s = min(s, 1.0)
        if any(k in txt for k in NOISE) or re.search(r"\$[a-z]{2,6}\b", txt) or txt.count("$") >= 2 or txt.count("#") >= 4:
            return 0  # shill / promo: out, not merely down-ranked
        if any(k in txt for k in DIGEST) and len(txt) < 400 and not r.get("thread_text"):
            s = min(s, 1.0)  # pointer post with no content of its own; the links pass will pick up what it points at
        if r.get("links") and any("github.com" in u or "arxiv.org" in u for u in r["links"]) and len(txt) < 200:
            s -= 0.5  # the tweet is just an announcement; prefer the primary source it links to
    return max(0, min(5, round(s)))


_REPO_CACHE: dict[str, bool] = {}


def repo_alive(url: str) -> bool:
    """gh api repos/<owner>/<repo> returns non-zero on 404 / renamed-away repos."""
    import subprocess
    m = re.search(r"github\.com/([^/\s#?]+)/([^/\s#?]+)", url)
    if not m:
        return True
    key = f"{m.group(1)}/{m.group(2).removesuffix('.git')}"
    if key not in _REPO_CACHE:
        r = subprocess.run(["gh", "api", f"repos/{key}", "--jq", ".full_name"], capture_output=True, text=True)
        _REPO_CACHE[key] = r.returncode == 0
        if not _REPO_CACHE[key]:
            print(f"  dead repo {key}", file=sys.stderr)
    return _REPO_CACHE[key]


def cmd_batch(a):
    lib = library_seen()
    seen = load_seen()
    raw = []
    for p in sorted(RAW.glob("*.jsonl")):
        raw += jl_read(p)
    fresh, dropped = {}, {"library": 0, "seen": 0, "low": 0, "dupe": 0, "linked-in-library": 0, "dead-repo": 0}
    for r in raw:
        cid = r["id"]
        if cid in lib:
            dropped["library"] += 1
        elif r.get("source") in {"x", "apify-x"} and any(cand_id("", u) in lib for u in r.get("links") or []):
            dropped["linked-in-library"] += 1  # the thing the tweet points at is already catalogued
        elif r.get("source") == "code" and not a.no_repo_check and not repo_alive(r["url"]):
            dropped["dead-repo"] += 1
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
        src = "x" if r["source"] in {"x", "apify-x"} else ("blog" if r["source"] in {"blog", "web"} else r["source"])  # talk, code, paper keep their own dir
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
    p = sub.add_parser("lesswrong", help="LessWrong / Alignment Forum via public GraphQL (free)")
    p.add_argument("--site", choices=list(LW_SITES), default="lesswrong"); p.add_argument("--by", required=True)
    p.add_argument("--tags", nargs="*", help="tag-slug[:topic-slug] ..."); p.add_argument("--limit", type=int, default=40)
    p.add_argument("--min-karma", type=int, default=20); p.add_argument("--keywords", default=None, help="comma list, keep only tag posts mentioning one")
    p.add_argument("--search", default=None, help="file of `topic<TAB>kw1,kw2` lines matched against the new+top pools")
    p.add_argument("--pool", type=int, default=300)
    p = sub.add_parser("rss", help="RSS/Atom feeds: `topic<TAB>url[<TAB>kw1,kw2]` per line"); p.add_argument("--feeds", required=True)
    p.add_argument("--by", required=True); p.add_argument("--limit", type=int, default=60); p.add_argument("--score", type=int, default=2)
    p = sub.add_parser("ytsearch", help="talk discovery with yt-dlp flat search: `topic<TAB>query` per line")
    p.add_argument("--queries", required=True); p.add_argument("--by", required=True); p.add_argument("--n", type=int, default=15)
    p.add_argument("--min-minutes", type=int, default=8); p.add_argument("--score", type=int, default=2); p.add_argument("--ytdlp", default=None)
    p = sub.add_parser("jina", help="fetch page text through r.jina.ai for blog rows that only have a url")
    p.add_argument("--by", required=True); p.add_argument("--max", type=int, default=60); p.add_argument("--sleep", type=float, default=1.0)
    p.add_argument("--prune", action="store_true", help="drop rows whose page is dead or empty")
    p = sub.add_parser("openalex", help="forward/backward citation chasing via OpenAlex: `topic<TAB>fwd|back|both<TAB>seed[<TAB>kws]`")
    p.add_argument("--seeds", required=True); p.add_argument("--by", required=True); p.add_argument("--max", type=int, default=600)
    p.add_argument("--refs", nargs="*", default=["refs/remotes/origin/lane/*"], help="git refs whose library/papers count as known")
    p = sub.add_parser("oa-locate", help="find free copies of named papers via OpenAlex: `topic<TAB>seed[<TAB>note]`")
    p.add_argument("--list", required=True); p.add_argument("--by", required=True)
    sub.add_parser("status")
    a = ap.parse_args(argv)
    return {"x-search": cmd_x_search, "apify": cmd_apify, "links": cmd_links, "seed": cmd_seed,
            "lesswrong": cmd_lesswrong, "rss": cmd_rss, "ytsearch": cmd_ytsearch, "jina": cmd_jina,
            "openalex": cmd_openalex, "oa-locate": cmd_oa_locate, "batch": cmd_batch, "status": cmd_status}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
