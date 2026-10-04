# External evidence injection and the value of dissent — experimental-design bundle

**Superseded proposal:** the active implementation is [How to win agents and influence swarms](../influence-swarms/scenario/README.md). The broad mechanism grid below is historical, not the current launch plan. See the [review response](../influence-swarms/scenario/REVIEW-RESOLUTION.md).

**Status: HUNCH / experimental-design proposal — not a hypothesis; the prior-art gate has not been passed for this question.**
Nothing here belongs in `hypotheses/`, nothing here is a measured result, and no code has been built. It is a design document plus the supporting notes it rests on, filed for comment.

## The question

An outside party who controls none of the swarm's members, but does control content the swarm retrieves, can write pages that steer which provider or MCP server the swarm picks — including toward an option the party fabricated. The open questions this bundle exists to ask are: **does independently sourced dissent actually improve a swarm's robustness to that channel, under what conditions does it stop helping, and what does it cost at equal budget?** The primary mechanism we would test is a **dissent-rewarding aggregation rule** — weighting reports by the independence of their evidence roots rather than by their count, with a convergence brake that fires when evidence diversity collapses. We do not know whether it helps. The design's job is to make the answer falsifiable, including the answer "it does not", and to keep apart three things the literature routinely pools: shared retrieval, peer propagation, and decision quality.

## Map of the bundle

| file | what it is |
|---|---|
| `experimental-design.md` | the proposal: scenario, three-layer model, dissent operationalisation, three aggregation schemes, full design (units, corpus worlds, arms, 18 metrics, power), cheap-agent tier, build plan, evidence-and-boundaries, ~210 numbered references |
| `experimental-design.html` | the same material as a self-contained offline page with inline diagrams and a seeded surrogate simulation. Every chart is labelled model output, not measurement |
| `sources/attack-surface.md` | what the injector can measurably do to a retrieval channel |
| `sources/collective-dynamics.md` | why swarms converge wrongly; the mechanisms by which dissent protects |
| `sources/dissent-incentives.md` | scoring rules, peer prediction, robust aggregation, three candidate value functions |
| `sources/cheap-agents.md` | whether the question changes for very small models; the competence-vs-robustness confound; cost arithmetic |
| `sources/prior-guide-digest.md` | adopt / adapt / contest verdict per claim of an owner-supplied prior guide |

An internal review of the first draft returned **fix-first** (8 high, 2 medium); all ten items were applied before this copy was made. The review's design-level findings are under **Gaps** below, because applying a fix is not the same as the question being settled.

## Feedback wanted

Specific asks, not general comment. Mostly for **dmarz** (1, 2, 6, 8) and **shadow** (3, 4, 5).

1. **Preflight gates — unit of assignment.** `synthesis/pre-experiment-research.md` gate 3 asks for the unit of assignment and the independent unit of analysis. Ours: assignment = injection campaign × task instance, randomised per instance with retrieval rank logged; analysis = the episode, clustered at task. Does that satisfy the gate, and is `unresolved mechanism` as a first-class episode outcome the category you intended?
2. **The pre-registered objection.** The same synthesis parks a *Causal trace analysis* row against the external-influence brief: *"the available trace cannot identify the proposed mechanism."* We claim assignment-level randomisation answers it rather than a post-hoc trace. Does it, in your reading?
3. **Split naming.** We adopt **operator/campaign-disjoint** from shadow's evaluation design as the split name. Right term, and is our unknown-operator fallback rule compatible with yours?
4. **"Decoy listing" vs "honeypot".** `synthesis/swarm-detection-methods.md` §3 uses honeypot for a detection *sensor*. Ours is a fabricated *listing inside the choice set*, so we say "decoy listing" throughout. Is that the term you want repo-wide, or should we defer to yours?
5. **Overlap with fork-merge Q1.** `synthesis/fork-merge-questions.md` §6 Q1 (shared-input k-of-n sweep) is the same adversarial-correlation mechanism in a fork-and-merge topology; ours is provider-selection. Is one sentence enough separation, or is this one question that should be run once?
6. **The `fm-bft-aggregation` lane.** Its coverage note already states the gap we would fill. Cite it as our prior-art basis and stay out, or is the aggregation arm better run inside that lane?
7. **In-protocol slot.** The existing complete survey's review returned `verdict: revise`, capping any hypothesis listing it at `draft`/`proposed`. Is the right slot a **new survey** (retrieval-channel influence + dissent-rewarding elicitation, ~30 new entries to clear the gate) or a **`kind: question` task**? We have claimed none of the three open `survey-*` tasks.
8. **Compute on the fleet.** The cheap tier's pilot is 300 episodes on small local models; the full sweep is ~1.2M decisions and prices at roughly a $100 line item on a nano tier. Is there fleet capacity, and what is the API-budget convention? We found none in the repo.

## Gaps

Design-level and unresolved — not closed by an edit.

- **Identification is argued, not demonstrated.** The exposure model is assignment-level by construction, but no run exists to show the clustering assumptions hold; `σ_d` and the experiment-recognition rate are assumptions until a pilot supplies them, and the power arithmetic says so.
- **Oracle risk in the defence.** Independence weighting needs evidence-root identity, which a simulator supplies. A result in that setting does **not** validate lineage inferred from text, which deployment would need. The imperfect-provenance and root-shuffling controls bound this; they do not remove it.
- **The primary contrast is bundled** — the aggregation arm changes the rule *and* adds checks. Weights-only and brake-only decompositions are specified, but they are extra cells, not free.
- **Budget confound.** Dissent may simply buy more evidence. There is a mandatory equal-budget arm, but token-matching is not compute-matching across model tiers.
- **Reversibility is unknown.** Two 2026 sources disagree on whether capture persists after the injecting agents stop; we would measure it rather than assume either.
- **Cheap-tier robustness may be incompetence** — small models score well on susceptibility partly by emitting nothing usable, so a validity rate is required beside every susceptibility number.
- **Operator economics are unpriced.** Cost per published page, crawl-to-index latency, takedown hazard, and the realistic operator share of a production retrieved set appear in no source we found: swept parameters, never cited constants.
- **Two effect sizes are unavailable** (publisher-elided, non-OA) for the canonical genuine-vs-contrived dissent comparisons — direction only, no magnitudes stated.
- **The event's judging criteria are unfilled** (`tasks/admin-hackathon-brief.md`), so nothing here can be scored against stated criteria.

## Built vs not built

| Built (repo-relative) | Not built — needed by this design |
|---|---|
| `scripts/lab.py` — check · verify · index · find · new · claim/touch/done/release · gate · sync | Any experiment harness: no agent runner, no model config, no retrieval stack, no decision environment |
| `scripts/collect.py` — source discovery | A corpus the injector can write into: no retrieval, web-corpus or recommendation dataset in `library/datasets/` |
| `scripts/batches.py`, `candidates/`, `.github/ISSUE_TEMPLATE/batch.md` — claimable scan batches | A provider/MCP choice set with ground-truth quality per option (must be authored from scratch) |
| `scripts/test_batches_worktree.py` — the repo's only test | A dissent-rewarding value function implementation (nearest prior work is catalogued, not vendored) |
| `src/x-trend/` — trend, crawl, classify, fetch, `trend_data.json` | A cheap-agent population runner (small model + fast decision rule); precedents catalogued only |
| `artifacts/agent-discourse-x/`, `attestations/`, `artifacts.lock.json` | Measurement code for the five stages: exposure / acceptance / propagation / outcome / profiling value |
| `synthesis/` (6 documents), 1 `complete` survey, 2 in-progress, 1 review (`revise`) | Any `hypotheses/` or `experiments/` entry — both directories are README-only |
| `library/` — swarm-detection, fork-merge-security, sybil-resistance, llm-agent-swarms | A `library/topics.yaml` slug for retrieval / search / persuasion / mechanism design; entries for peer prediction, proper scoring rules, surprisingly-popular elicitation |
| `library/datasets/` — 20+ entries, licence and access audited | A reusable environment: the nearest catalogued information environment with a recommender is not vendored and needs a model endpoint |

**What this design needs that exists nowhere in the repo:** the harness; the decision environment and its oracle; the corpus generator with ancestry labels and the nine corpus worlds; the decoy-listing generator; the metrics module (18 metrics with denominators, arm subscripting enforced in code); the three aggregation rules behind one frozen interface; and the analysis notebook (paired clustered bootstrap, McNemar).

## How we would implement it

Ordered, with **builder-hour estimates that are ours and unmeasured**. Full table and dependencies: `experimental-design.md` → *Demonstration & build plan* §2–§3.

| step | deliverable | hours |
|---|---|---|
| B1 | fixture + oracle: task generator, rubric, held-out set, regret function, arithmetic self-check as a unit test | 4–6 |
| B2 | corpus builder: pages per task family, ancestry labels, nine corpus worlds as length- and coverage-matched transforms | 5–7 |
| B3 | retrieval harness: deterministic search over a frozen corpus, k and position exposed, non-exposure recorded as an outcome | 4–6 |
| B4 | agent loop: five roles, claim ledger, **private scores locked before any message**, lineage-carrying rounds, admissibility verifier | 6–9 |
| B5 | aggregators: plurality · confidence-weighted · quorum · independence-weighted with brake, one interface frozen across arms | 4–6 |
| B6 | surrogate simulation + the interactive page, seeded, model-output labelling on every chart | 6–8 |
| B7 | metrics + analysis: 18 metrics, arm subscripting enforced in code, paired clustered bootstrap, McNemar | 4–5 |
| B8 | cheap-tier pilot: 300 episodes, local models, pinned version and seeds | 5–7 |
| B9 | primary contrast: 35 tasks × 5 seeds, within one corpus world at the mid dose | 4–6 |
| B10 | replication across ≥3 model families, cells frozen before B9 is read | 3–5 |
| B11 | write-up, figures, diagrams | 5–7 |

**Total 50–72 h. B1–B7 (≈33–47 h) is a deliverable on its own** — a harness, a transparent surrogate, a pre-registered protocol, and one pilot number that is ours rather than inherited. If the window collapses: one frozen corpus, three mock providers, five agents, a claim ledger, two independent check slots, truthful-vs-injected worlds, random-vs-targeted checking.

The `templates/hypothesis.md` fields it would fill (`surveys:`, `closest_prior:`, Claim, Grounding, Novelty, Prediction, Minimal experiment, Kill criteria) and the `templates/experiment.md` fields (`code:`, Setup, Protocol, Metrics, Results, Analysis) are drafted in `experimental-design.md` → *Demonstration & build plan* §4.1 and §4.2 — including the three mandatory comparisons in `closest_prior:` with their discriminating question, and the rule that Protocol and Metrics are committed before the first real run.

## Sources

- [`sources/attack-surface.md`](sources/attack-surface.md) — injector capability and the retrieval channel
- [`sources/collective-dynamics.md`](sources/collective-dynamics.md) — convergence failure and protective dissent
- [`sources/dissent-incentives.md`](sources/dissent-incentives.md) — elicitation, scoring rules, robust aggregation
- [`sources/cheap-agents.md`](sources/cheap-agents.md) — small-model populations, confounds, cost
- [`sources/prior-guide-digest.md`](sources/prior-guide-digest.md) — adopt / adapt / contest on an owner-supplied prior guide

Every claim in `experimental-design.md` carries a numbered reference resolving to a URL in its References section, and each number is marked for how the source was read; listing-level sources are marked as such and are not load-bearing for a headline number. The owner-supplied prior guide is digested in `sources/prior-guide-digest.md`; the guide itself is a local file and is **not** in this repository, so its claims are reachable here only through that digest. References are numbered rather than `[[id]]` links because this is a hunch bundle and not a survey; converting them is part of the survey work in Feedback wanted item 7.
