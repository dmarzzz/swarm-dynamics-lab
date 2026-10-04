# 2026-10-03 dmarz/sd-ai-content

Lane: population-level detection of AI-generated content (scan-papers-sd-ai-content), run as an isolated
lane on branch lane/sd-ai-content. Per dmarz's override, no claim/touch/done and no edits under lab/tasks/;
the coverage note below stands in for the task's Coverage note and should be copied there at merge.

## What I covered

55 new paper entries, all tagged swarm-detection (two also sybil-resistance, one llm-agent-swarms).
`lab.py verify --agent dmarz/sd-ai-content`: 55 papers, 0 problems. `lab.py check`: 0 errors in my files
(the only errors on the branch are in 1-library/papers/wu-2024-system.md, which predates this lane).

Read in full (5): liang-2024-monitoring (main text and methods, not every appendix table),
kobak-2024-delving, sun-2024-are, la-cava-2025-machines, hao-2025-do. Everything else is abstract depth.

Clusters:
- Corpus-level estimators: liang-2024-monitoring, liang-2024-mapping, liang-2025-widespread,
  kobak-2024-delving, gray-2024-chatgpt, gray-2025-estimating, geng-2024-is, czuma-2026-emergence.
- Measured prevalence in the wild: sun-2024-are (Medium/Quora/Reddit), la-cava-2025-machines (Reddit),
  hao-2025-do (malicious email), brooks-2024-rise and huang-2025-wikipedia (Wikipedia),
  hanley-2023-machine, russell-2025-ai, ansari-2025-echoes (news), macko-2025-beyond (disinformation),
  he-2026-degentweb and dolezal-2026-impact (web), thompson-2024-shocking (machine translation),
  russo-latona-2024-ai (peer review), veselovsky-2023-artificial and xu-2026-penny (crowd workers),
  daniotti-2025-who (code), yang-2024-characteristics and ricker-2024-ai (generated profile faces),
  diresta-2024-how, drolsbach-2025-characterizing, chrysidis-2026-synthetic, matatov-2024-examining,
  goyal-2026-social (Moltbook agents), brzozowski-2026-ghost (ghost-author names on Zenodo).
- Confounds and homogenisation: geng-2025-human, yakura-2024-empirical, sourati-2025-shrinking.
- Limits of per-item detection: sadasivan-2023-can, krishna-2023-paraphrasing, liang-2023-gpt,
  chakraborty-2023-possibilities, weber-wulff-2023-testing, dugan-2024-raid, russell-2025-people,
  geng-2025-detectability, wu-2023-survey (review), mitchell-2023-detectgpt, bao-2023-fast,
  hans-2024-spotting, emi-2024-technical, chen-2024-online.
- Watermarks: kirchenbauer-2023-watermark, kirchenbauer-2023-reliability, dathathri-2024-scalable,
  zhang-2023-watermarks, jovanovic-2024-watermark, gloaguen-2024-black.

## Searches run

- Semantic Scholar forward citations of Liang et al. 2024 (2403.07183, 295 citing papers) and Kobak et al.
  (2406.07016, 239), filtered by title keywords; most new candidates came from this.
- Semantic Scholar keyword search ("estimating fraction of LLM-generated content corpus", "AI-generated
  misinformation community notes characterizing"); several other S2 and all OpenAlex queries returned
  HTTP 429 because many lanes share the rate limit.
- WebSearch: Barracuda/IMC malicious-email study, Daniotti GitHub code study, SynthID Nature paper,
  social-media AIGT prevalence (Medium/Quora/Reddit). After four queries the session's shared WebSearch
  budget (200) was exhausted.
- arXiv export API returned 429 after the first batch; metadata then came from the S2 batch endpoint and
  arxiv.org/abs pages.

## Could not reach or did not catalogue

- Mimecast blog on LLM-generated email (cited by hao-2025-do), Originality.ai and Graphite web-prevalence
  posts: not opened, so not catalogued.
- Product-review prevalence (Amazon, Yelp), YouTube and music "AI slop" (for example Deezer upload shares),
  and short-text platforms (X, Bluesky) have no entry here. The searches for them hit the budget.
- "Quantifying large language model usage in scientific papers" (129 citations, no arXiv id in S2) may
  be the journal version of liang-2024-mapping. Not checked, so it is not claimed in that entry.
- Peer-review detection papers (2410.03019, 2502.19614, 2503.15772) and syntactic-template and style
  papers (2407.00211, 2410.16107) were seen in citation lists but not catalogued.

## What surprised me

- Hao et al. measured that at least 51% of spam in April 2025 was LLM-written. Top spammers use LLMs to
  produce reworded variants of one message, and MinHash clusters were 52-79% LLM-flagged. This is the
  clearest in-the-wild swarm signature in this lane.
- Reddit numbers vary by an order of magnitude with method: about 2.5% of posts (Sun et al., trained
  detector) against peaks of 6-9% in some subreddit-months under a 0.99 Fast-DetectGPT threshold (La Cava
  et al.). La Cava et al. also found that about 2% of users produce all of the flagged text.
- Marker words decay once they are published (geng-2025-human), and humans pick up LLM vocabulary in
  speech (yakura-2024-empirical). Both undercut lexical estimators over time.
- No paper I found estimates the share of covert autonomous agents, as opposed to LLM-assisted
  humans, on any platform. xu-2026-penny looked for browser-use agents among survey respondents and found
  none. goyal-2026-social measures declared agents only.

## Next

Pull the full texts of he-2026-degentweb and chen-2024-online, since they aggregate many weak verdicts
into a decision about one site or one source. Search product reviews and short-text platforms once the
search budget resets.
