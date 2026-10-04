---
slug: proxifield
title: "Proxifield: Decentralized Multi-Agent Communication through Semantic Proximity"
authors: Pradyumna Tambwekar, Yenchia Feng, Deep Patel, Karime Maamari (Distyl AI)
org_or_venue: arXiv preprint (arXiv:2609.20889v1, cs.MA)
date: 2026-09-16
status: found
fetched: 2026-10-03
urls_loaded:
  - "http://export.arxiv.org/api/query?search_query=all:Proxifield&max_results=5"
  - "https://arxiv.org/abs/2609.20889"
  - "https://arxiv.org/html/2609.20889v1"
library_ids:
  - tambwekar-2026-proxifield
---

## What it is (2-4 sentences)

A training-free communication protocol for LLM agent teams that rebuilds a **sparse directed message graph every round** from semantic signals computed at inference time, with no orchestrator and no learned topology generator. Each round an agent drafts a provisional action, the router decides who hears whose proposal, agents evaluate the proposals they received, then commit an action. The pitch is that decentralized semantic routing beats a centralized star topology, and the gap *widens* as the team grows and as agents start failing.

## Method / setup (what they actually did; models, N, tasks, baselines)

**Protocol — five stages per round:** (1) Proposal Generation, (2) Typed Semantic Routing, (3) Proposal Delivery and Peer Evaluation, (4) Action Commitment, (5) Environment Update.

**Four inference-time routing signals** (all computed from embeddings, no training):
1. **Direct address** — indicator of whether the sender explicitly named the recipient.
2. **Need matching** — max cosine similarity between the sender's stated information *request* embeddings and the target's observations/memory.
3. **Plan alignment** — cosine similarity between agents' current messages and action rationales (optionally mean-centred once ≥3 agents have valid representations).
4. **Information complementarity** — `1 − (average cosine similarity of observations and memories)`; deliberately favours *dissimilar* peers.

**Graph construction:** two capacity knobs — `k` = outgoing-edge budget per sender, `c_in` = max incoming edges per receiver. Direct-address edges are admitted first, subject to the same capacities. Remaining candidate edges are ranked by `max{λ_ask·s_ask, λ_align·s_align, λ_comp·s_comp}` with fixed weights **λ_ask=0.90, λ_align=0.85, λ_comp=0.80** (set by importance ordering, not tuned). A coverage pass guarantees every agent gets ≥1 incoming message where possible.

**Hyperparameters:** `k ∈ {1,2}`, `c_in = 3`, memory consolidation window `Δ_mem = 5` rounds, episode length `T = 100` (DSSE) / `T = 15` (HiddenBench).

**Environment 1 — Drone Swarm Search Environment (DSSE):** grid-based maritime search-and-rescue; drones must find drifting survivors. The authors modify it two ways: (a) **asymmetric roles** — *Scouts* see a global probability forecast plus direct sightings within radius 6 cells; *Searchers* see only their own cell's probability and must take an explicit `SEARCH` action to confirm a survivor; (b) a **scaling scheme** where grid area ≈ `80N` cells and survivor count = `4S`, with `N = 5S` total agents. Swarm sizes tested: **N ∈ {5, 25, 50}**.

**Environment 2 — HiddenBench:** collective decision-making under distributed information. Shared facts point at the *wrong* answer; each agent holds one unique private fact, and the private facts collectively support the right answer — so the team only wins if private evidence is surfaced and integrated. **80 task instances**, N ∈ {3,4,5,6,7} (fixed by task design), `T = 15`.

**Models:** all Qwen3.5 mixture-of-experts — **Qwen3.5-35B-A3B**, **Qwen3.5-122B-A10B**, **Qwen3.5-397B-A17B**. All agents in a condition share a model, *except* the Star orchestrator, which always runs on 397B-A17B.

**Baselines:**
- **Independent / No-Comm** — act on local observation + memory only, zero exchange.
- **Star (centralized)** — a dedicated orchestrator that coordinates but does not act in the environment; workers send provisional actions + info summaries, orchestrator returns consolidated directives. Costs `2N+1` model calls/round. **Excluded from HiddenBench** because the orchestrator would receive every private fact and trivially solve the task.
- **Shared Context / Blackboard** — all agents write to and read a common context (inspired by Decentralized Language Models, DeLM); no agent-to-agent messaging. Costs `≤5N` calls/round.
- **Discussion** — HiddenBench's native discussion protocol, for comparative context only.

Proxifield itself costs **2N–3N** calls/round (N proposal + N reply + 0–N commitment).

## Key results (numbers with units; mark each "measured" or "claimed")

**Model-scale (RQ1), DSSE at N=5 — measured:** Proxifield (k=1) task reward **6.97** at 35B vs Star **4.74**; at 397B, Proxifield **7.57** vs Star **6.99**. The authors emphasise that the Star orchestrator was *always* the 397B model, so a 35B decentralized team beat the same 35B agents supervised by a far bigger model.

**HiddenBench — measured:** Shared Context leads at 35B (**0.77** vs Proxifield **0.63** post-discussion accuracy); Proxifield overtakes at 397B (**0.79–0.81** vs **0.78**). So the ordering *flips* with model capability — a result worth taking seriously rather than averaging away.

**Agent-count scaling (RQ2) — measured:** Proxifield's task-reward advantage over Star is **+5.4% at N=5**, **+53.0% at N=25**, **+59.5% at N=50**. Star's *participation rate* (fraction of agents earning non-zero reward) collapses **75% → 33%** from N=5 to N=25; Proxifield holds **≥50% even at N=50**.

**Permanent agent failure (RQ3), N=25, cumulative failure probability q=0.8 — measured:** Proxifield retains **73.6%** of its no-failure task reward (21.2 of 28.8) vs Shared Context **58.3%** and Star **38.8%**. Participation at q=0.8: Proxifield **39%**, No-Comm **11%**, Star **8%**, Shared Context **10%**. In absolute terms: **60 of 100 available survivors rescued across five runs** vs **12** (No-Comm) and **10 each** (Shared Context, Star).

**Cost — measured:** Shared Context is consistently the most expensive (maintaining/updating the shared window needs extra LLM calls every step) and has the steepest cost growth in N; Proxifield scales more favourably.

**Edge budget — measured:** `k=2` vs `k=1` makes almost no difference (**0.02–0.1 accuracy**). Notably they do **not** report per-signal ablations, so the individual contribution of each of the four signals is unmeasured.

## Limitations the source admits + ones you noticed

**Admitted:**
- "Evaluation across more domains is needed to establish the generalizability of our approach."
- Scaling and robustness (RQ2, RQ3) were tested in **one environment only** (DSSE).
- No comparison against other *decentralized / dynamic-topology* methods — only centralized and shared-context baselines.
- The λ weights were set by importance ordering, not empirically calibrated.
- **Anomaly:** Qwen3.5-122B-A10B underperformed the 35B model on *all* tasks and *all* baselines; they call it model-specific, not a scaling effect, and leave it unexplained.

**Noticed here:**
- **No per-signal ablation** is the biggest gap: the headline claim is "semantic proximity routing works", but we cannot tell whether direct-address alone (a trivially cheap signal) delivers most of the gain, or whether complementarity actually earns its place.
- **Single model family.** All three sizes are Qwen3.5 MoE. The 122B anomaly makes the "scales with model size" claim rest on two usable points.
- **The Star baseline is partly straw.** The orchestrator does not act in the environment, so at N=25 and N=50 it is a single serialised bottleneck trying to direct 25–50 actors through one context window. Participation collapse is the expected consequence of that design, not necessarily evidence about centralization in general.
- **Shared Context is charged for a design choice.** Its `≤5N` cost comes from LLM-mediated context maintenance; a cheaper append-only blackboard would change the cost comparison.
- **q=0.8 is a brutal regime.** Retaining 73.6% of reward when 80% of agents are dead is a strong result, but it is one failure model (permanent, independent) in one environment.

## Relevance to the hackathon shortlist

- **Collective Sensing (local/global/no comms, partial obs, known truth):** This is the closest paper to that project and it hands you a ready-made design. **Steal the DSSE asymmetry**: Scouts with global-ish observation (forecast + radius-6 sightings) vs Searchers with single-cell observation plus a confirm-action. **Steal the scaling law** `grid area ≈ 80N, survivors = 4S, N = 5S` so difficulty stays constant as you add agents — otherwise your N-sweep conflates crowding with coordination. **Steal the baseline ladder**: No-Comm / Star / Shared-Context / your-protocol is exactly the local-vs-global-vs-none contrast, and the paper proves the ladder discriminates. **Steal the second metric**: *participation rate* (fraction of agents with non-zero reward) exposed Star's collapse long before mean reward did — mean reward alone would have hidden it. And **steal the failure-injection axis**: a `q` sweep of permanent agent death is cheap to implement and produced their most dramatic separation. Pitfall to avoid: don't ship only a mean-reward bar chart at one N — their N=5 gap was 5.4% (noise-adjacent) and only became 59.5% at N=50.
- **Quorum (independent evidence vs repeated copies; false commit vs delay):** **HiddenBench is your benchmark and you should probably just use it** — 80 instances, shared facts favouring the wrong answer, one unique private fact per agent, N=3–7. It is purpose-built for "did independent evidence actually get surfaced, or did the team ratify the popular wrong answer." Two directly transferable design facts: (1) **a centralized orchestrator invalidates the task** — the authors had to *exclude* Star because the orchestrator sees all private facts, which is precisely the "repeated copies vs independent evidence" confound in architectural form; design your quorum so no node can see all evidence. (2) **Information complementarity as an explicit routing signal** — `1 − avg cosine similarity` is a concrete, implementable way to weight *dissimilar* evidence over echoes, which is the core Quorum mechanic. The flip at 35B (Shared Context 0.77 > Proxifield 0.63) is a warning: with weak agents, a blackboard that everyone reads can beat clever routing, so include a blackboard arm or you will overclaim.
- **Telephone (atomic claims through retellings; lost evidence, inflated certainty):** Less direct, but it supplies the **hop-count control knob**. Proxifield's `k` (out-degree) and `c_in = 3` (in-degree) plus the coverage pass are exactly the parameters that set how many hops a claim must survive and how many times it can be re-encoded. Their round structure — propose, route, *peer-evaluate what you received*, commit — is a clean retelling harness: the peer-evaluation step is where a claim gets re-expressed and where provenance is lost. Also note the negative evidence: `k=2` vs `k=1` changed accuracy by only 0.02–0.1, which suggests raw message volume is not the lever; *which* claim reaches *whom* is. For Telephone, that argues for measuring per-hop claim fidelity directly rather than hoping more messages preserve more truth.

## Quotable (<=15 words each, verbatim, with location)

- "task-reward advantage over Star widens from 5.4% at (N=5) to 53.0% at (N=25)" — Abstract
- "Proxifield retains 73.6% of its no-failure task reward" — Results, RQ3
- "coordination occurs through shared state rather than direct agent-to-agent messaging" — §5.2, Shared Context baseline
- "Evaluation across more domains is needed to establish the generalizability of our approach." — §7 Limitations & Future Work
- "Qwen3.5-122B-A10B underperformed the smaller model across all tasks and baselines." — §7 Limitations & Future Work
- "max cosine similarity between request embeddings and target's observations or memory" — §4.3, need-matching signal

## Not found / could not verify (queries tried, what was ambiguous)

- Discovery was clean: `http://export.arxiv.org/api/query?search_query=all:Proxifield&max_results=5` returned exactly one entry (2609.20889v1) on the first try. No web search fallback needed.
- **No `comments` field** on the abs page, so page count, figure count, and any venue/submission target are unknown.
- **Per-signal ablation numbers do not exist in the paper** — confirmed absent, not merely unfetched. Appendix E ("Additional Results") was not read in full, so a buried ablation table cannot be 100% excluded.
- Appendices A–G were listed but not individually fetched; prompts (Appendix F) and exact DSSE reward shaping were not read.
- The absolute no-failure reward baseline at N=25 (28.8) is reported, but the corresponding Star/Shared-Context absolute no-failure rewards at N=25/N=50 were given as percentages only in what was loaded.
