"""Crawl A: tweets linking every library arXiv paper (url:<id>, min_faves:2, no retweets)."""
import json, pathlib, sys
from concurrent.futures import ThreadPoolExecutor
from apify_client import ApifyClient
HERE = pathlib.Path(__file__).parent
TOKEN = pathlib.Path.home().joinpath("tweet-harvester/.apify_token").read_text().strip()
P = json.load(open(HERE / "papers.json"))
ids = list(P)
batches = [ids[i:i + 40] for i in range(0, len(ids), 40)]
def run(k):
    out = HERE / "raw" / f"papers-{k:03d}.json"
    if out.exists(): return k, "cached"
    c = ApifyClient(TOKEN)
    terms = [f"url:{ax} -filter:retweets min_faves:2" for ax in batches[k]]
    r = c.actor("apidojo/tweet-scraper").call(run_input={"searchTerms": terms, "maxItems": 30 * len(terms), "sort": "Top"})
    r = r.model_dump() if hasattr(r, "model_dump") else r
    items = [i for i in c.dataset(r.get("default_dataset_id") or r.get("defaultDatasetId")).iterate_items() if i.get("id")]
    out.write_text(json.dumps(items))
    return k, len(items)
with ThreadPoolExecutor(8) as ex:
    for k, n in ex.map(run, range(len(batches))): print(k, n, flush=True)
