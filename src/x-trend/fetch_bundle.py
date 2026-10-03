"""Fetch full author threads for picks.json and write one verbatim bundle per thread."""
import json, pathlib, re, urllib.request
from concurrent.futures import ThreadPoolExecutor
from apify_client import ApifyClient
HERE = pathlib.Path(__file__).parent
TOKEN = pathlib.Path.home().joinpath("tweet-harvester/.apify_token").read_text().strip()
picks = json.load(open(HERE / "picks.json"))
def fx(tid):
    try: return json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.fxtwitter.com/i/status/{tid}", headers={"User-Agent": "Mozilla/5.0"}), timeout=25)).get("tweet") or {}
    except Exception as e: return {"err": str(e)}
roots = {p["root"] for p in picks}
with ThreadPoolExecutor(12) as ex: R = dict(zip(roots, ex.map(fx, roots)))
c = ApifyClient(TOKEN)
def conv(batch):
    r = c.actor("apidojo/tweet-scraper").call(run_input={"searchTerms": batch, "maxItems": 25 * len(batch), "sort": "Latest"})
    r = r.model_dump() if hasattr(r, "model_dump") else r
    return [i for i in c.dataset(r.get("default_dataset_id") or r.get("defaultDatasetId")).iterate_items() if i.get("id")]
terms = sorted({f"conversation_id:{p['root']} from:{(R[p['root']].get('author') or {}).get('screen_name') or p['h']}" for p in picks})
with ThreadPoolExecutor(8) as ex: reps = [i for b in ex.map(conv, [terms[i:i+40] for i in range(0, len(terms), 40)]) for i in b]
by = {}
for i in reps: by.setdefault(i.get("conversationId"), {})[i["id"]] = i
json.dump({"roots": R, "replies": reps}, open(HERE / "raw" / "threads.json", "w"))
n = 0
for p in picks:
    r = R[p["root"]]
    if not r or "err" in r or not r.get("author"): continue
    h = r["author"]["screen_name"]; tid = p["root"]
    eid = re.sub(r"-+", "-", f"x-{h.lower().replace('_','-')}-{tid}").replace("--", "-")
    L = [f"ENTRY_ID: {eid}", f"ROOT_HANDLE: {h}", f"AUTHOR_NAME: {r['author'].get('name')}", f"URL: https://x.com/{h}/status/{tid}",
         f"CREATED: {r.get('created_at')}", f"METRICS at 2026-10-03: likes={r.get('likes')} reposts={r.get('retweets')} replies={r.get('replies')} views={r.get('views')}",
         f"KIND: {p['kind']} (author = poster's name matched the paper's author list; verify)", f"LINKED_LIBRARY_PAPER: {p['pid']} (arXiv {p['ax']})",
         f"PAPER_AUTHORS: {p.get('authors','')}", f"SUGGESTED_TOPICS: {','.join(p['topics'])}", "", "=== ROOT TWEET (verbatim) ===", (r.get("raw_text") or {}).get("text") or r.get("text", "")]
    art = r.get("article")
    if art: L += ["", f"=== X ARTICLE: {art.get('title')} ===", "\n\n".join(b.get("text", "") for b in (art.get("content") or {}).get("blocks", []))]
    q = r.get("quote")
    if q: L += ["", f"=== QUOTED TWEET (not by author) @{(q.get('author') or {}).get('screen_name')} {q.get('url')} ===", q.get("text", "")]
    links = re.findall(r"https?://[^\s\"\\]+", json.dumps(r.get("raw_text", {})))
    own = sorted([t for t in by.get(tid, {}).values() if t["author"]["userName"].lower() == h.lower() and t["id"] != tid], key=lambda t: int(t["id"]))
    for k, t in enumerate(own, 2):
        L += ["", f"=== SELF-REPLY {k} https://x.com/{h}/status/{t['id']} ({t['createdAt']}) ===", t.get("fullText") or t.get("text", "")]
        links += [u.get("expanded_url") for u in (t.get("entities") or {}).get("urls", []) if u.get("expanded_url")]
    L += ["", "=== LINKS ===", *sorted({l.rstrip('",}]') for l in links if l and "t.co/" not in l})]
    (HERE / "bundles" / f"{eid}.txt").write_text("\n".join(L)); n += 1
print(n, "bundles;", len(reps), "conversation tweets")
