"""Monthly discourse on X, Jan 2023 to Oct 2026: top-engagement tweets (min_faves:50) per term per month."""
import json, pathlib, datetime
from concurrent.futures import ThreadPoolExecutor
from apify_client import ApifyClient
HERE = pathlib.Path(__file__).parent
TOKEN = pathlib.Path.home().joinpath("tweet-harvester/.apify_token").read_text().strip()
TERMS = {
 # Sybil
 "sybil (all)": 'sybil OR sybils OR "sybil attack" OR "anti-sybil"',
 "sybil x AI agents": '(sybil OR sybils) (agent OR agents OR AI OR LLM OR bots)',
 "proof of personhood": '"proof of personhood" OR "proof of humanity" OR "personhood credentials" OR "proof of human"',
 "agent identity / KYA": '"agent identity" OR "know your agent" OR "ERC-8004" OR "agent passport"',
 # multi-agent concepts
 "multi-agent (LLM)": '("multi-agent" OR "multi agent" OR multiagent) (LLM OR LLMs OR GPT OR Claude OR "AI agents")',
 "agent swarm": '"agent swarm" OR "agent swarms" OR "swarm of agents" OR "AI swarm" OR "AI swarms"',
 "subagents": 'subagent OR subagents OR "sub-agent" OR "sub-agents"',
 "agent-to-agent": '"agent-to-agent" OR A2A OR "agent2agent"',
 # projects
 "AutoGPT / BabyAGI": 'AutoGPT OR "Auto-GPT" OR BabyAGI',
 "Generative Agents (Smallville)": '"generative agents" OR Smallville',
 "AutoGen": 'AutoGen (Microsoft OR agents OR multi-agent)',
 "CrewAI": 'CrewAI OR crewAIInc',
 "MetaGPT / ChatDev / CAMEL": 'MetaGPT OR ChatDev OR "CAMEL-AI" OR camelaiorg',
 "LangGraph": 'LangGraph',
 "OpenAI Swarm / Agents SDK": '"OpenAI Swarm" OR "Agents SDK" OR (openai swarm framework)',
 "ElizaOS / ai16z": 'ElizaOS OR ai16z OR "eliza framework"',
 "Virtuals": '"Virtuals Protocol" OR virtuals_io',
 "AI Village": '"AI Village" OR "agent village"',
 "Moltbook": 'Moltbook',
 "OpenClaw / Clawdbot": 'OpenClaw OR Clawdbot OR Moltbot',
 "Hermes Agent": '"Hermes Agent" OR "hermes agent"',
 "x402": 'x402',
}
def months():
    d = datetime.date(2023, 1, 1)
    while d <= datetime.date(2026, 10, 1):
        n = (d.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
        yield d, n; d = n
M = list(months())
def run(key):
    out = HERE / "raw" / (key.replace("/", "_").replace(" ", "_") + ".json")
    if out.exists(): return key, "cached"
    q = TERMS[key]
    terms = [f"({q}) since:{a} until:{b} min_faves:50 -filter:retweets" for a, b in M]
    c = ApifyClient(TOKEN)
    r = c.actor("apidojo/tweet-scraper").call(run_input={"searchTerms": terms, "maxItems": 3000, "sort": "Top", "includeSearchTerms": True})
    r = r.model_dump() if hasattr(r, "model_dump") else r
    items = [{k: i.get(k) for k in ("id", "createdAt", "likeCount", "retweetCount", "replyCount", "viewCount", "text", "searchTerm")} | {"h": (i.get("author") or {}).get("userName"), "fol": (i.get("author") or {}).get("followers")}
             for i in c.dataset(r.get("default_dataset_id") or r.get("defaultDatasetId")).iterate_items() if i.get("id")]
    out.write_text(json.dumps(items))
    return key, len(items)
with ThreadPoolExecutor(11) as ex:
    for k, n in ex.map(run, TERMS): print(k, n, flush=True)
