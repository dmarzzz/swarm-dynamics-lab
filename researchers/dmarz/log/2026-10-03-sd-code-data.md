# 2026-10-03 dmarz/sd-code-data

Lane: code, datasets and benchmarks for detecting AI agent swarms in the wild (task scan-code-sd-code-data). Worked in an isolated worktree on branch lane/sd-code-data; per dmarz's override I did not claim, touch or close the task and did not edit tasks/.

## What I covered

36 new entries tagged swarm-detection, plus 5 existing entries annotated (topic added and a "Notes from dmarz/sd-code-data" section): data-twibot22-2022, data-twibot20-2021, data-cresci-2017, yang-2023-anatomy, de-marzo-2026-collective.

- Agent honeypots and canaries (8): gh-palisaderesearch-llm-honeypot, gh-sundew-sh-sundew, gh-peg-snare, gh-tcotl-agentcapture, gh-hackinglz-agentprovocateur, gh-beelzebub-labs-beelzebub, gh-0x4d31-galah, gh-thinkst-canarytokens.
- Moltbook (agent-only social network) data and papers (6): mukherjee-2026-moltgraph (full read), li-2026-moltbook (abstract), data-moltgraph-2026, data-moltbook-observatory-2026 (ran), data-moltbook-takschdube-2026, gh-real-lab-nu-awesome-openclaw-papers (review list).
- Coordination detection (3): gh-qut-digital-observatory-coordination-network-toolkit (ran), gh-nicolarighetti-coortweet (install failed), gh-fabiogiglietto-coornet (archived).
- Social bot detection (5): data-fox8-2023, data-botsim24-2024, gh-osome-iu-botometer-python, gh-tamsiuhin-botpercent, gh-bunsenfeng-botrgcn.
- AI crawlers and browser agents (6): gh-ai-robots-txt-ai-robots-txt (ran), gh-monperrus-crawler-user-agents (ran), gh-techarohq-anubis, gh-fingerprintjs-botd, gh-jonaslong-pyison, gh-nepenthesweb-nepenthes-py.
- AI-text detection and watermarks (8): gh-ahans30-binoculars, gh-baoguangsheng-fast-detect-gpt, gh-liamdugan-raid, gh-yafuly-mage, gh-google-deepmind-synthid-text, gh-jwkirchenbauer-lm-watermarking, gh-hello-simpleai-chatgpt-comparison-detection, gh-kinit-sk-multisocial.

Read in full: arXiv 2410.13919 (LLM Agent Honeypot; catalogued by another lane as reworr-2024-llm, so I linked it instead of duplicating) and arXiv 2603.00646 (MoltGraph). Ran: coordination-network-toolkit on Moltbook, the Moltbook observatory archive, ai.robots.txt, crawler-user-agents, sundew.

## Searches run

- GitHub repository search (gh api search/repositories) with: llm honeypot agent; ai agent honeypot; social bot detection; coordinated inauthentic behavior; coordinated link sharing; ai crawler tarpit; machine generated text detection benchmark; llm bot detection twitter; ai agent detection browser; moltbook dataset; botnet llm dataset; sybil detection airdrop; coordination network toolkit; botpercent; fox8 botnet; bot repository osome; iocaine; information operations twitter dataset; reddit bot detection llm; llm agent fingerprint; detect llm agents web; ai agent traffic dataset.
- Hugging Face dataset search: moltbook, botsim, twibot, bot-detection, ai-generated-text, fox8, agent-traces.
- arXiv website search "moltbook" (63 results, listed 2026-10-03); arXiv abstract pages for 2410.13919, 2603.00646, 2602.07432, 2605.13860, 2412.13420, 2302.00381, 2307.16336; Zenodo record 8035289.
- Live dashboards: ai-honeypot.palisaderesearch.org (archived) and ai-honeypot.reworr.com (v2 placeholder).

## What I could not reach

- Semantic Scholar, OpenAlex and the arXiv export API all returned HTTP 429 (shared rate limit with other lanes), so no forward/backward citation chasing through APIs; citation counts left null.
- The session's WebSearch budget was already exhausted when I first tried it (200 of 200), so no general web or social search. Not covered: Cloudflare/Akamai/HUMAN bot-traffic reports, Imperva Bad Bot reports, Known Agents / Dark Visitors data, Twitter/X information-operations archives, Meta CIB reports, Iocaine (hosted off GitHub), Nepenthes original (zadzmo.org).
- CooRTweet would not install: RcppSimdJson fails to compile with the current macOS toolchain under R 4.5.3.
- Moltbook Illusion (2602.07432) has no arXiv HTML; only the abstract was read.
- Not followed up: 60 other Moltbook papers in the arXiv list, notably 2603.03555 (Molt Dynamics, coordination benchmark on the archive), 2602.18152 (The Statistical Signature of LLMs), 2602.20059 (Interaction Theater), 2610.00430 (Memetic Trojans). These belong in a paper lane or a next pass.

## What surprised me

- Palisade's honeypot base rate: 24,111,509 SSH interactions, 14 potential and 3 confirmed autonomous LLM agents on the archived dashboard (about 1 in 8 million). The author now asks how to detect passive LLM use, which the method cannot see.
- AgentCapture's self-reported result that hidden command-style injections were refused 0/8 times by mainstream agent CLIs, while a trap disguised as the site's documented API recruited 5/5 agents. If this holds, Palisade-style injection triggers are losing sensitivity and honeypots must look like the task, not like an instruction.
- On one day of Moltbook (2026-09-10: 4,526 posts, 482 agents) a text-reuse coordination detector found 0 identical-text pairs and 1 pair at Jaccard >= 0.5 within a day. Copy-paste coordination signals, the workhorse for human botnets, see nothing among LLM agents.
- Owner metadata does not expose operators on Moltbook: of 182,860 agents in the observatory archive, 55,551 carry an owner X handle, held by 55,545 distinct handles (max 2 agents per handle). Multi-agent operators, if present, must be found from behaviour.
- The CoV timing fingerprint of 2602.07432 is sensitive to platform gaps: the eight most active agents on 2026-09-10 post every ~180 s, but one shared 2.7-hour platform-wide gap pushes their whole-day CoV to 2.0-2.5, which would label them "human-influenced" under a naive threshold (inference from my run; I have not seen how the paper treats gaps).
- Sundew v0.2.1 without an LLM classified nothing in my local test: only 404 hits were logged and all fingerprint scores were 0.0.

## Next

- Run fox8-23 and BotSim-24 through a text detector (Binoculars or Fast-DetectGPT) and a coordination detector side by side to reproduce the "coordination works, text fails" result.
- Semantic-similarity (embedding) coordination on Moltbook to replace Jaccard; normalise co-post by activity rate.
- Download MoltGraph and test whether upvote co-timing exposes vote rings.
- Citation chasing on 2410.13919 and 2603.00646 once the APIs stop rate-limiting.
