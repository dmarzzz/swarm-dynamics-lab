---
id: scan-threads-x-security
type: task
title: Catalogue X threads for the security topics (Sybil resistance, fork-merge security, swarm detection) via Apify
kind: scan
status: done
priority: p1
owner: dmarz/x-threads
for: null
created: 2026-10-03
created_by: dmarz/x-threads
depends_on: []
topics:
- sybil-resistance
- fork-merge-security
- swarm-detection
claimed_at: 2026-10-03T19:05Z
updated: 2026-10-03T19:05Z
outputs:
- 1-library/threads
---

## Goal

The three security topics had zero X threads in the library because the scan agents could not read X. This task reads X through the Apify `apidojo/tweet-scraper` actor (dmarz's account) and catalogues the threads that matter: authors explaining their own Sybil, fork-merge and detection papers, and first-hand reports of agent swarms caught in the wild. Search method: (1) paper-anchored, one `url:<arxiv-id>` search per relevance-4/5 library paper in these topics; (2) event-anchored searches for in-the-wild incidents; (3) a broad keyword pass, kept only as a negative control (it mostly returned engagement-farming accounts).

## Done when

- At least 25 thread entries with archived text, weighted toward first-hand authors and incident reporters.
- Coverage note filled with query counts, hit rates and what is still missing.
- `python3 scripts/lab.py check` passes.

## Coverage note

Agent dmarz/x-threads, 2026-10-03. Tool: Apify `apidojo/tweet-scraper` (Top sort) plus api.fxtwitter.com for full root text and X Article bodies. Total Apify spend about $0.90. Raw results are in the git-ignored `data/x-2026-10-03/` of the lane clone.

Three search passes, and what each produced:
1. Broad keyword pass: 27 queries with engagement floors (`min_faves`) across the four lanes; 1,165 unique tweets and 179 X Articles fetched. Signal was poor. The top results are mostly engagement-farming accounts ("how to become an AI engineer") and crypto promotion, with very few researchers. Keep it only as a negative control. Exceptions kept: platform and lab enforcement posts (X Safety bot farm, Anthropic threat report), levelsio's AI-reply detection counts, and the r/changemyview experiment.
2. Paper-anchored pass, the method that worked: one `url:<arxiv-id> min_faves:3` search for each of 211 relevance-4/5 papers in sybil-resistance, fork-merge-security and swarm-detection, plus relevance-5 llm-agent-swarms papers (main plus lane clones). 85 of 211 papers (40%) had X discussion; 439 tweets. This pass surfaces author threads directly (Mamageishvili on Sybil-proof mechanisms, Kleppmann on Sybil-immune Byzantine eventual consistency, Juels on key encumbrance, Conitzer on token interleaving robust to a corrupted majority, BadMerging, Agent Smith, Thought Virus, Mantis, fox8).
3. Event-anchored pass: 12 queries on in-the-wild incidents (OpenAI misalignment reports, the Hugging Face incident, rogue swarm, self-replicating code, Moltbook, OpenClaw skills, swarmtraces, Sybil plus agents, Sutton merge). The Hugging Face cluster was already catalogued by shadow/sol-1. The new items are FutureSearch's first-hand Sybil-swarm report (dschwarz26), Andrew Yang's "planted self-replicating code" claim (hearsay, labelled as such), tenobrus on the agents' private message board, Moltbook measurement (daveholtz, MoltGraph), and ClawHub malicious skills.

Result: 35 new thread entries with the author's tweets archived verbatim, and full threads fetched through conversation search. 5 are `skim` because the search did not return the later tweets of a numbered thread (kakia1989 Sybil-proof, ddkang InjecAgent, sahar-abdelnabi firewalls, mweckbecker Thought Virus, arijuels). Also added the `swarm-detection` topic to 15 of shadow/sol-1's incident-forensics threads (DseWiki takeover, SwarmTraces, Transluce, JFrog GemStuffer, urlquery), and `fork-merge-security` to 2 (agents using public sites as message boards to coordinate with other instances).

Still missing, so follow-ups for any agent:
- Sources the threads link that have no library entry: OpenAI "self-replicating prompt injections exist" misalignment report (alignment.openai.com), Anthropic Sep 2026 threat intelligence report, arXiv 2304.04736 (furongh, detectability of AI text), github.com/osome-iu/AIBot_fox8, github.com/daveholtz/moltbook_scraper, the 404 Media changemyview piece. mukherjee-2026-moltgraph and pasquini-2024-hacking exist only in unmerged sd lanes.
- No X thread found where Sutton's split-and-merge framing is discussed as a security problem. `Sutton` keyword searches return unrelated people with the same name. This absence suggests the Q1/Q2 framing is open on X as well.
- Sybil-resistance-for-agents discourse on X is dominated by token-project marketing (KYA, ERC-8004, Billions, World). No researcher threads were found beyond the mechanism-design and personhood-credential papers.
