---
slug: silo-bench
title: "Silo-Bench: A Scalable Environment for Evaluating Distributed Coordination in Multi-Agent LLM Systems"
authors: Yuzhe Zhang, Feiran Liu, Yi Shan, Xinyi Huang, Xin Yang, Yueqi Zhu, Xuxin Cheng, Cao Liu, Ke Zeng, Terry Jingchen Zhang, Wenyuan Jiang
org_or_venue: ACL 2026 Main Conference (accepted); arXiv:2603.01045 (cs.MA / cs.AI); 20 pages, 7 figures
date: 2026-03-01 (v1); v2 2026-04-13 (version read = v2)
status: found
fetched: 2026-10-03
urls_loaded:
  - "https://export.arxiv.org/api/query?search_query=ti:%22Silo-Bench%22+OR+ti:%22SiloBench%22+OR+ti:%22Silo+Bench%22&max_results=10"
  - "https://arxiv.org/abs/2603.01045"
  - "https://arxiv.org/html/2603.01045v2"
library_ids:
  - zhang-2026-silo
---

## What it is (2-4 sentences)

A benchmark built to answer one sharp question: when you shard information across agents to escape a
context limit, can the agents actually **compute** over the distributed state, or can they only
**exchange** it? Each of N agents gets only its own local shard and must coordinate to produce the
global answer, over 30 algorithmic tasks at three communication-complexity levels, 54 configurations,
1,620 experiments, agent counts from 2 to 100. The headline finding is a **Communication-Reasoning
Gap**: agents spontaneously form sensible coordination topologies and do exchange information
successfully, then fail at the *integration* step — and the coordination overhead grows until it
eliminates the parallelization gain entirely. This is the most directly relevant source in the
shortlist for any project about siloed evidence.

## Method / setup (what they actually did; models, N, tasks, baselines)

- **The silo construction (§3.2):** global input X is partitioned into shards; "Each agent receives
  only its local shard X_i and must coordinate to determine y*". Role-agnostic — no agent is given a
  special job, so topology formation is emergent rather than prescribed.
- **30 algorithmic tasks in three levels by communication complexity (Appendix E, Table 9):**
  - **Level I — Aggregation, O(N) comms (10 tasks):** Global Maximum, Word Frequency, Distributed
    Vote, Any Match, Range Count, Checksum (XOR), Average Value, Set Union Size, Top-K Selection,
    Standard Deviation.
  - **Level II — Mesh Network, O(N) comms (10 tasks):** Prefix Sum, Moving Average, Longest
    Palindrome, 1D Life Game, Pattern Search, Trapping Rain, Diff Array, List Ranking, Merge
    Neighbors, Pipeline Hash.
  - **Level III — Global Shuffle, O(N log N)-O(N^2) comms (10 tasks):** Distributed Sort, Median of
    Medians, Graph Components, BFS Distance, K-Means Iteration, Global Distinct, Collaborative
    Filtering, PageRank Step, Load Balance, Matrix Multiply.
  Note the virtue of this design: **ground truth is computable and the required communication
  volume is known analytically**, so "did they talk enough" and "did they compute right" are
  separable by construction.
- **Configurations (§4.1):** 6 agent scales x 3 communication protocols x 3 models = **54**;
  30 tasks x 54 = **1,620 experiments**.
- **Agent counts:** N in {2, 5, 10, 20, 50, 100}.
- **Models (all open-weight, run locally, default temperature, 128K context):** DeepSeek-V3.1,
  GPT-OSS-120B, Qwen3-Next-80B-A3B.
- **Communication protocols / topologies (Appendix A, Fig. 3):** **P2P** (directed agent-addressed
  messaging), **BP** (broadcast, all-to-all), **SFS** (shared file system / indirect coordination
  through a shared key-value store).
- **Baseline — a centralized N=1 oracle** that receives the complete global input. Explicitly framed
  as the upper bound: "the N=1 oracle represents the upper bound; Silo-Bench asks whether distributed
  agents can approach this bound through coordination alone" (§4.1).
- **Metrics (§3.3) — four, and the pairing is the clever part:**
  1. **Success Rate (S)** = (1/N) sum 1[y_hat_i = y*]; a task instance succeeds only when S = 1
     (every agent holds the right answer).
  2. **Partial Correctness Score (P)** = (1/N) sum q_i — continuous answer quality (Level I:
     fraction within tolerance; Level II: correctly computed elements per segment; Level III:
     longest correctly ordered subsequence).
  3. **Token Consumption (C)** per round.
  4. **Communication Density (D)** = (sum m_i) / (N(N-1)) — interaction intensity normalized by the
     possible edges.
  **The gap P - S "quantifies performance lost specifically at the reasoning-integration stage"
  (§3.3)** — that is the operationalization of the whole paper.
  5. Derived: **Relative Coordination Cost RCC = 1 - SR(N=k)/SR(N=1)** — the fraction of
     single-agent performance lost to coordination (§4.1).

## Key results (numbers with units; mark each "measured" or "claimed")

- **Overall, by model — measured (Table 1).** Success Rate / Partial Correctness / tokens-per-round
  / comms density: **DeepSeek-V3.1 36.9% / 47.1% / 323.0 / 0.82**;
  **GPT-OSS-120B 16.9% / 38.3% / 313.8 / 1.01**;
  **Qwen3-Next-80B-A3B 8.2% / 19.8% / 873.6 / 0.25**.
  Note Qwen spends **2.7x** the tokens of DeepSeek for **1/4.5** the success — token spend is not
  the binding constraint.
- **By difficulty level, DeepSeek-V3.1 — measured (Table 1).**
  Level I: **SR 62.0%, PCS 88.0%, 184.0 tokens/round**;
  Level II: **SR 35.1%, PCS 59.7%, 355.9**;
  Level III: **SR 11.7%, PCS 27.9%, 439.2**.
- **The Communication-Reasoning Gap — measured (§4.2).** At Level I, **88.0% PCS vs 62.0% SR = a
  26-percentage-point gap**. The information is acquired; it is not synthesized. At **N >= 50 on
  Level III: SR = 0% while PCS = 8-16%** — agents demonstrably hold partial global information and
  still cannot produce a correct answer.
- **Scaling in agent count, DeepSeek-V3.1, averaged across protocols — measured (Table 3).**
  Success rate by N (Level I / Level II / Level III / average):
  N=2 **85.0 / 61.7 / 36.2 / 61.2%**;
  N=5 **72.0 / 55.3 / 17.2 / 48.5%**;
  N=10 **68.7 / 28.3 / 10.0 / 39.9%**;
  N=20 **65.7 / 29.5 / 5.7 / 33.6%**;
  N=50 **38.1 / 17.4 / 0.0 / 19.0%**;
  N=100 **40.6 / 14.3 / 0.0 / 18.1%**.
  **Monotone decline in N at every level** — the average falls from 61.2% to 18.1% going 2 -> 100
  agents. Level III hits **exactly 0% at N >= 50**. The authors describe it as "performance degrades
  multiplicatively with scale and complexity".
- **Relative Coordination Cost, GPT-OSS-120B — measured (Table 2).** RCC by scale
  (Level I / II / III): k=2 **15.2 / 31.1 / 48.8%**; k=5 **30.3 / 32.9 / 70.0%**;
  k=10 **33.1 / 70.0 / 85.0%**; k=50 **45.9 / 80.0 / 100%**; k=100 **50.0 / 62.4 / 100%**.
  **RCC = 100% at N=50 on Level III** means distributed teams scored **0% where the centralized
  baseline scored 26.7%** — the parallelization gain is not merely reduced, it is gone.
- **The N=1 centralized oracle — measured (Table 2, GPT-OSS-120B).** Level I **96.7%**,
  Level II **90.0%**, Level III **80.0%**. So the tasks are easy for one agent with full
  information; everything lost is lost to distribution.
- **Token cost in N — measured (Table 1 / Fig. 4b, DeepSeek-V3.1).** Tokens per round:
  N=2 **12.1**; N=5 **44.2**; N=10 **91.3**; N=20 **211.0**; N=50 **510.3**; N=100 **1,093.8**.
  Roughly **linear** in agent count. So you pay linearly and your accuracy falls — the worst shape.
- **Communication density collapses as N grows — measured (Fig. 4c).** From **~2.8 at N=2 to ~0.14
  at N=100**. The authors' reading: "agents become sparser in interaction precisely when denser
  coordination is most needed". This is arguably the paper's most useful mechanism finding — the
  failure is partly that agents *under*-communicate at scale.
- **Failure-mode distribution — measured (Table 4, over 301 analyzed runs).**
  Success **50.8% (153/301)**; **Premature Submission 37.2% (112)** — the most prevalent;
  **Consensus Failure 29.9% (90)**; **Computation Error 28.6% (86)**. (Categories overlap, hence
  >100% total.)
- **Protocol comparison — measured (Fig. 6, DeepSeek-V3.1).** **BP (broadcast) 40.4% > P2P 38.9% >
  SFS 31.5%** success. SFS underperforms "despite comparable information transfer" (§4.3) — i.e.
  indirect/shared-store coordination is worse than direct messaging even when the bits arrive.
- **Claimed.** That the gap is "localized to the reasoning-integration stage" is an inference from
  the P - S decomposition rather than a direct measurement of an internal stage; that "naively
  scaling agent count cannot circumvent context limitations" generalizes beyond algorithmic tasks.

## Limitations the source admits + ones you noticed

**Admitted (Limitations section):**
- **Only three communication protocols**; no hierarchical protocols, gossip-based dissemination, or
  hybrid approaches.
- **Homogeneous agents** — uniform underlying model, whereas real systems are heterogeneous.
- **No closed-source models**, excluded for cost at this scale and "unverifiable, incomparable
  reported token usage".
- **Three frontier LLMs** may not capture the full spectrum of failure modes.

**Noticed:**
- **The tasks are algorithmic, and that is both the strength and the ceiling.** Exact ground truth
  and analytically known communication complexity are what make the P - S decomposition valid — but
  distributed sort and PageRank are not what agent systems are usually asked to do, and LLMs are
  known to be weak at exact multi-step arithmetic independent of any coordination issue. **Some of
  the measured "integration failure" is plausibly just arithmetic failure**, and the paper's own
  Computation Error category (28.6%) concedes a large share of it. The N=1 oracle at 80-96.7%
  partly controls for this, which is the right move, but the control is per-task-level, not
  per-token-of-reasoning.
- **S requires *all N* agents to be correct** (S = 1 for success). That is a brutally strict
  criterion that mechanically penalizes large N: at N=100, one confused agent fails the instance.
  Part of the monotone decline in Table 3 is this definition, not coordination per se. A
  "did any/the designated agent get it right" variant would separate the two, and is not reported.
- **Premature Submission at 37.2% may be a scaffold artifact.** If the harness lets an agent submit
  before consensus, the most common failure mode is partly a protocol-design choice rather than a
  model limitation.
- **N=301 for the failure-mode analysis** out of 1,620 runs — the qualitative table rests on ~19% of
  the corpus, and the selection rule for those 301 is not stated in what I could retrieve.
- **No round budget reported.** C is defined as tokens per round divided by R_max, but the value of
  R_max is not in what I retrieved — so whether agents simply ran out of rounds at large N is
  unresolved, and it is a live alternative explanation for the density collapse.
- The RCC table is reported for GPT-OSS-120B while the scaling and level tables are DeepSeek-V3.1;
  mixing them in one argument is easy to do accidentally and wrong.

## Relevance to the hackathon shortlist

- **Collective Sensing (local/global/no comms, partial obs, known truth):** this is **the same
  experiment**, and the project should treat it as prior art to extend rather than rediscover. Four
  concrete transfers. (1) **Its three protocols are your three comms conditions, already named and
  measured**: BP = global, P2P = local/directed, SFS = indirect — and the measured ranking is
  **BP 40.4% > P2P 38.9% > SFS 31.5%**, so "global beats local beats indirect" is the result to
  reproduce or overturn. (2) **Steal the P - S metric pair outright** — a known-truth partial-
  observation task lets you compute exactly their "did they get the information" vs "did they
  integrate it" split, and the 26pp Level-I gap is your reference magnitude. (3) **Use the N=1
  full-observation oracle as the baseline** (they measure 80-96.7%), and report RCC = 1 - SR(N)/SR(1)
  so your numbers are directly comparable. (4) **The pitfall that will bite you**: their success
  criterion demands all N agents be right, which manufactures part of the scaling decline — define
  yours explicitly and, if you can, report both the strict and the any-agent variant. Also note
  their density collapse (~2.8 at N=2 to ~0.14 at N=100): if your swarm under-communicates at scale,
  that is a known effect, not a bug in your harness.
- **Quorum (independent evidence vs repeated copies; false commit vs delay):** the two headline
  numbers are made for this project. **Premature Submission is the single most prevalent failure at
  37.2%** — that is false commit, measured, as the dominant failure mode of distributed agent
  reasoning, and it is the strongest available justification for building a quorum mechanism at all.
  **Consensus Failure at 29.9%** is the delay/no-commit side. So the false-commit-vs-delay dial your
  project proposes is not hypothetical: **both ends are already measured at ~30-37% incidence in the
  same corpus**, which means a good quorum rule has a very large target. Second transfer: because
  each agent holds a *genuinely different shard*, Silo-Bench is the clean setting for the
  independent-evidence-vs-repeated-copies distinction — their **Communication Density D =
  sum(m_i)/(N(N-1))** is a ready-made measure of how much message traffic is circulating, and
  pairing it with P - S lets you show messages went up while integration did not. Their SFS result
  (shared store underperforms despite equal information transfer) is a direct warning for any quorum
  built on a shared blackboard rather than addressed messages.
- **Telephone (atomic claims through retellings; lost evidence, inflated certainty):** the
  Communication-Reasoning Gap is the generalized form of Telephone's thesis, and the P - S
  decomposition is the metric you want, adapted: let P be per-atomic-claim fidelity after k
  retellings and S be final-answer correctness, and the gap is your "evidence lost while confidence
  preserved" measurement. Their Level II mesh tasks (Prefix Sum, Moving Average, Merge Neighbors,
  **Pipeline Hash**) are literally chain/neighbour-passing structures — **Pipeline Hash is a
  telephone game with checkable ground truth** and is worth reading as a task-design template.
  Reference magnitudes to anchor against: Level II success falls **61.7% (N=2) -> 14.3% (N=100)**
  while PCS stays well above SR, which is the shape "answer degrades faster than information does"
  that your project predicts. Pitfall: their tasks have exact answers, so "inflated certainty" is
  invisible in their metrics — they never measure stated confidence at all. That is your opening,
  and it means you must add a calibration measurement they do not have.

## Quotable (<=15 words each, verbatim, with location)

- "whether agents can reliably compute with distributed information, rather than merely exchange it" — abstract
- "systematically fail to synthesize distributed state into correct answers" — abstract
- "This coordination overhead compounds with scale, eventually eliminating parallelization gains entirely" — abstract
- "naively scaling agent count cannot circumvent context limitations" — abstract
- "agents become sparser in interaction precisely when denser coordination is most needed" — Section 4.2 (per extraction)
- "The gap P-S quantifies performance lost specifically at the reasoning-integration stage" — Section 3.3 (per extraction, notation simplified)

## Not found / could not verify (queries tried, what was ambiguous)

- **R_max (the round budget) was not in the retrieved text**, though it appears in the definition of
  the token-consumption metric. Without it, "agents ran out of rounds" remains an unexcluded
  alternative explanation for the large-N collapse.
- **The selection rule for the 301 runs** in the Table 4 failure-mode analysis (out of 1,620) was
  not stated in what I retrieved.
- Whether the Table 4 categories are mutually exclusive: they sum to **146.5%** across 301 runs, so
  they are evidently overlapping labels, but the paper's own statement of that was not retrieved.
- The code repository is cited in the abstract as
  `https://github.com/jwyjohn/acl26-silo-bench` (reported by the arXiv API summary of the v2 entry);
  **Not fetched: or verify that the repository exists or is populated.**
- All numbers above were extracted by the page fetcher over the arXiv HTML of v2, not read directly
  off the PDF. Table/section attributions are as that reader reported them.
- Discovery note: found on the first arXiv API title query
  (`ti:"Silo-Bench" OR ti:"SiloBench" OR ti:"Silo Bench"`); no web search fallback was needed.
- Venue is stated in the arXiv comment field as "Accepted at ACL 2026 Main Conference"; **I did not
  independently confirm this against an ACL Anthology entry** (ACL 2026 proceedings may not be
  posted yet as of 2026-10-03).
