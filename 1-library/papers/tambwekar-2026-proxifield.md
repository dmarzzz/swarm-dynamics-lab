---
id: tambwekar-2026-proxifield
type: paper
title: "Proxifield: Decentralized Multi-Agent Communication through Semantic Proximity"
authors:
- Pradyumna Tambwekar
- Yenchia Feng
- Deep Patel
- Karime Maamari
year: 2026
venue: arXiv preprint (cs.MA)
url: https://arxiv.org/abs/2609.20889
doi: null
arxiv: '2609.20889'
cite: "Tambwekar, P., Feng, Y., Patel, D., & Maamari, K. (2026). Proxifield: Decentralized multi-agent communication through semantic proximity. arXiv preprint arXiv:2609.20889."
topics:
- llm-agent-swarms
added_by: vishesh/senku-1
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: "not retrieved (2026-10-03)"
code: []
---

## Summary

A training-free communication protocol for teams of language-model agents that rebuilds a sparse directed message graph every round from embedding-derived signals, with no orchestrator and no learned topology generator. Each round an agent drafts a provisional action, a router decides who hears whose proposal, recipients evaluate what they received, then everyone commits. Evaluated on a modified drone-swarm maritime search environment at N = 5, 25 and 50 and on an 80-instance hidden-information decision benchmark at N = 3 to 7, against no-communication, centralised-orchestrator and shared-blackboard baselines. The reported pattern is that the advantage over the centralised baseline widens with team size and with agent failure rate, while a shared blackboard wins at the smallest model size.

## Contribution

Shows that useful communication topology can be derived at inference time from semantic signals alone, and reports the scaling direction explicitly: the gap over a star topology grows from noise-adjacent at N = 5 to large at N = 50. It also supplies participation rate (the fraction of agents earning non-zero reward) as a second metric that exposes a centralised baseline's collapse long before mean reward does.

## Key results

- Model scale on the search environment at N = 5: Proxifield task reward 6.97 at the 35B model versus the centralised baseline 4.74; at 397B, 7.57 versus 6.99. Measured. The centralised orchestrator always ran on the largest model, so the smaller decentralised team beat a far larger supervisor.
- Hidden-information benchmark: the shared blackboard leads at 35B (0.77 versus 0.63 post-discussion accuracy) and Proxifield overtakes at 397B (0.79 to 0.81 versus 0.78). Measured. The ordering flips with model capability.
- Task-reward advantage over the centralised baseline: +5.4% at N = 5, +53.0% at N = 25, +59.5% at N = 50. Measured.
- Participation rate for the centralised baseline falls from 75% to 33% between N = 5 and N = 25; Proxifield holds at or above 50% even at N = 50. Measured.
- Permanent agent failure at N = 25 with cumulative failure probability 0.8: Proxifield retains 73.6% of its no-failure task reward (21.2 of 28.8) against 58.3% for the shared blackboard and 38.8% for the centralised baseline. Participation at that failure rate: Proxifield 39%, no-communication 11%, shared blackboard 10%, centralised 8%. In absolute terms 60 of 100 available survivors rescued across five runs, versus 12 (no communication) and 10 each for the other two. Measured.
- Outgoing-edge budget k = 2 versus k = 1 changes accuracy by only 0.02 to 0.1. Measured. Raw message volume is not the lever.
- Cost: the shared blackboard is consistently the most expensive and has the steepest growth in N because it needs extra model calls to maintain the shared window. Proxifield costs 2N to 3N calls per round; the centralised baseline costs 2N+1; the blackboard up to 5N. Measured for the comparison, structural for the call counts.
- No per-signal ablation is reported, so the individual contribution of each of the four routing signals is unmeasured.

## Methods and models

Five stages per round: proposal generation, typed semantic routing, proposal delivery and peer evaluation, action commitment, environment update. Four inference-time routing signals, all from embeddings: direct address (did the sender name the recipient), need matching (max cosine similarity between the sender's stated information request and the target's observations or memory), plan alignment (cosine similarity of current messages and action rationales), and information complementarity (1 minus average cosine similarity of observations and memories, deliberately favouring dissimilar peers). Graph construction uses an out-degree budget k in {1, 2} and in-degree cap c_in = 3; direct-address edges are admitted first, remaining candidates ranked by max of weighted signal scores with fixed weights 0.90, 0.85, 0.80 set by importance ordering rather than tuning, and a coverage pass guarantees each agent at least one incoming message. Memory consolidation window 5 rounds; episode length 100 ticks in the search environment, 15 in the decision benchmark. Environment 1 is a grid maritime search-and-rescue task modified two ways: asymmetric roles (scouts see a global probability forecast plus sightings within 6 cells; searchers see only their own cell and must take an explicit confirm action) and a scaling scheme holding difficulty roughly constant (grid area about 80N cells, survivors 4S, total agents N = 5S). Environment 2 distributes facts so that shared facts point at the wrong answer and each agent holds one unique private fact that is needed for the right one; the centralised baseline is excluded there because the orchestrator would receive every private fact and solve it trivially. Models are three sizes of one mixture-of-experts family (35B-A3B, 122B-A10B, 397B-A17B active-parameter configurations).

## Limitations and open questions

The authors admit that generalisability needs more domains, that the scaling and failure-robustness studies were run in one environment only, that no other decentralised or dynamic-topology method is compared against, and that the routing weights were set by importance ordering rather than calibrated. They also report an unexplained anomaly: the middle model size underperformed the smallest on all tasks and all baselines, which they call model-specific. Noticed beyond that: the missing per-signal ablation is the biggest gap, since direct address alone is a trivially cheap signal that might carry most of the gain; one model family across three sizes plus the middle-size anomaly leaves the capability claim resting on two usable points; the centralised baseline is partly a straw comparison because its orchestrator does not act and becomes a single serialised bottleneck directing 25 to 50 actors through one context window, so participation collapse is partly a consequence of that design rather than evidence about centralisation in general; the blackboard baseline is charged for a design choice, since a cheaper append-only board would change the cost comparison; and the 0.8 failure rate is one failure model (permanent, independent) in one environment. Appendices, including the prompts and the exact reward shaping, were not read.

## Relevance to us

The most directly reusable experimental design in the shortlist. The asymmetric-observation roles (global-ish scouts versus single-cell searchers with a confirm action) are a ready-made partial-observation setup; the scaling scheme keeps difficulty constant as N grows, which stops an agent-count sweep from conflating crowding with coordination; the baseline ladder (none, star, blackboard, protocol) is exactly the no-comms / local / global contrast and is shown to discriminate; participation rate is the second metric that mean reward would have hidden; and the failure-probability sweep is cheap to implement and produced the largest separation. Two warnings. The N = 5 gap was 5.4%, which is noise-adjacent, so a single-N bar chart proves nothing. And the blackboard beating this protocol at the smallest model size means a blackboard arm is mandatory or the comparison overclaims. For evidence-aggregation work, the hidden-information benchmark is directly usable, and the fact that a centralised orchestrator had to be excluded because it would see all private facts is the architectural form of the repeated-copies-versus-independent-evidence confound. Information complementarity (1 minus average cosine similarity) is a concrete implementable way to weight dissimilar evidence over echoes. Compare [[kim-2025-towards]], whose centralised architecture suppressed errors best at small N (the opposite direction from this paper's large-N result, which is worth reconciling), [[zhang-2026-silo]] on shared-store coordination underperforming addressed messaging, and [[choi-2025-debate]] on aggregation beating exchange among homogeneous agents.
