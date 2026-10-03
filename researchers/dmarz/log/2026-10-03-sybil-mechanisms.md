# 2026-10-03 dmarz/sybil-mechanisms

## What I did

- Task scan-papers-sybil-mechanisms. Catalogued 25 sources tagged sybil-resistance: 22 papers, 1 blog, 2 code repos.
- Full reads: pan-2024-sybil, mazorra-2023-cost, babaioff-2012-bitcoin, conitzer-2010-using. Skims: yokoo-2004-effect, patel-2025-maxshapley, buterin-2019-flexible. The rest are abstract-level.
- Semantic Scholar was rate-limited (429) the whole session, so search and forward-citation chasing ran on OpenAlex and the arXiv API.
- `lab.py check` shows 0 errors and 0 warnings for my files. `lab.py verify` checked 20 papers with 0 problems; 2 entries have no Crossref DOI (ACM 10.5555 identifiers).

## What surprised me

- pan-2024-sybil (authors affiliated with Caltech, Offchain Labs and Flashbots) proves that one extra Sybil is enough to collapse every symmetric, non-wasteful, truthful allocation rule to the second price auction. Bayesian Sybil-proofness reopens the design space, so for Sybil-constrained mechanisms, dominant-strategy and Bayesian implementation are not equivalent.
- mazorra-2023-cost has a section on Sybil commitments: agents that credibly commit sub-identities to act as independent rational players (smart contracts, delegated AI agents) can break mechanisms that resist ordinary Sybils. This is the closest match in this lane to LLM agents spawning sub-agents.
- The same author has a 2026 repo (gh-brunomazorra-llms-sybils) that tests whether LLM agents discover multi-identity strategies against VCG, quadratic funding, quadratic voting and equal-share rewards.
- MaxShapley's max game splits each key point's value equally among the sources that cover it. My own inference, flagged in the entry: an owner who submits duplicate documents gains share unless sources are aggregated by owner.

## What next

- Read the paper PDF in BrunoMazorra/LLMs-Sybils and catalogue it if it is public.
- Find and read Hu et al. 2026, "Dissociative Identity: Language Model Agents Lack Grounding for Reputation Mechanisms".
- Rerun Semantic Scholar citation chasing from yokoo-2004-effect and cheng-2005-sybilproof once the rate limit clears.
- Possible experiment: run equal-split, r(n) = R/2^(n-1) and stake-proportional rewards against LLM agents that can spawn identities at cost c, and measure the price of identity.
