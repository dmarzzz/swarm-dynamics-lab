# Using AI Village to improve our experiments

**Recommendation: start with a frozen-context memory and handoff pilot, then reuse the verified episodes across studies.** This is an exploratory design, not a launched experiment or accepted hypothesis. Dataset access is verified; episode answerability and scientific value are not yet measured.

**evidence_confidence: 0/4 — untested.** Claim assessed: structured handoffs improve decisions on Village-derived tasks. No responses or task labels have been collected. Assessor: vishesh/codex-pi-review, 2026-10-04; evidence: [access inventory](access-summary.json) and [prospective plan](PLAN.md).

**sample_size_summary:** Observed: 0 evaluated episodes, 0 model calls. Planned, conditional on usable clusters: 8 development, 8 qualification and 24 evaluation episodes; four paired decision arms. Messages and turns are not independent samples.

## Integration update, 2026-10-04

[Ranked experiment fit and new-study assessment](FIT.md), [implemented offline preparation](IMPLEMENTATION.md), [Telephone development plan](TELEPHONE.md), and [new closure-rule hunch](ACKNOWLEDGMENT.md). The historical metadata-only review below is preserved. The later integration parsed 8,000 private development-prefix rows, normalized 6,000 unreviewed drafts, and passed 21 software tests; zero real episodes are labeled or evaluated. Seven study-local contracts now link the shared builder. No native attempt changed or launched.

## What we verified

Source: [[data-ai-village-2026]], pinned to [`838b4150303ca8228e8edb432d8b8ccae353d258`](https://huggingface.co/datasets/aidigestorg/ai-village/tree/838b4150303ca8228e8edb432d8b8ccae353d258). Export timestamp: 2026-09-20T13:05:12.097Z. Read the card, schema and scaffolding changelog; authenticated downloads and parsing succeeded for four small metadata tables. No chat, memory text, computer-turn corpus or screenshots were inspected. Raw gated files remain private.

| Evidence | Current count | Verification scope |
|---|---:|---|
| Agent records | 46 | Loaded; not 46 simultaneously active agents |
| Village goal records | 51 | Loaded |
| Individual goal records / rooms | 33 / 16 | Loaded |
| Computer turns / sessions | 2,510,487 / 78,362 | Export manifest, not independently counted |
| Memory records / chat messages | 246,151 / 183,485 | Export manifest, not independently counted |

The schema/card's approximate counts are older. Use the pinned manifest and actual loaded counts. Tables were exported sequentially from a live database: pinning a revision does not make them a transactionally simultaneous snapshot. Check joins and exclude incomplete export-edge episodes.

## Three useful ways to use it

| Mode | What we do | What it can establish |
|---|---|---|
| Trace audit | Find correction, forgetting, failed handoff and coordination episodes; verify them against actions and tool evidence | Realistic failure categories and scenario requirements; associations, not causal effects |
| Frozen-context replay — first choice | Stop an episode at a timestamp; give fresh agents controlled versions of its permitted history; score against evidence | Effects of our context/memory intervention on this offline task distribution |
| Dataset-derived simulation — later | Build a small sandbox from a verified episode and define action-dependent transitions | Controlled multi-step swarm behavior in an explicitly authored environment |

Historical future events cannot serve as a simulator after a new agent changes an action. Different actions would change other agents' responses and the world. Matching the original next action is not a correctness metric.

## Transfer to each research direction

These are proposed uses, not observed properties of individual episodes. Keep current native results and budgets intact.

| Study | Useful dataset-backed version | Main limitation or control |
|---|---|---|
| Swarm of Theseus | Replace an agent at a real consolidation boundary; compare what its successor can recover from alternative memories | Tests transferred task state, not original agent identity or learned culture; complete prompts are unavailable |
| Right Dissenter | Replay a decision before and after a verified correction; test whether the agent reopens an obsolete conclusion | Require sufficient evidence at each cutoff; do not label the eventual historical winner as correct |
| Quorum of Mirrors | Follow a claim copied among agents; compare counting endorsements with tracing underlying receipts | Distinct speakers are not independent sources; natural provenance must be established |
| Phantom Coast | Present evolving uncertain evidence and test verification/abstention decisions | Need independently adjudicable truth and explicit verification costs; history alone does not identify optimal policy |
| Healing Helping Hands | Give a helper a trace containing an evidence-backed mistake; score correction and false correction | Freeze a separate clean cohort; hide labels and mechanism names from every actor payload |
| Immune Response | Test whether bad information persists through memory and whether repair removes it | Natural error is not proof of attack; any injected attack is a separately labeled synthetic treatment |
| Influence Swarms | Hold a claim constant while varying attributed authority or source access | Observed persuasion is confounded; manipulate attribution only in a controlled replay, preserve source truth |
| Poietic Agents | Derive task dependencies and repeated handoffs; test reuse versus a simple cache | Need action-dependent sandbox and meaningful task completion; transcript replay alone cannot measure adaptive organization |
| Optimal Swarm Size | Build a workload from verified tasks, then allocate equal total resources across different agent counts | Historical roster changes confound model, goal, tools and time; do not estimate optimal size from them |
| Heterogeneous Swarms | Test homogeneous versus mixed agents on the same task packets and total resource budget | Village model comparisons are observational and unequally exposed; new controlled calls are a separate run |
| Antsy | Use UI screenshots paired with independently verified text/state as visual extraction cases | No automatic OCR gold labels; this is a new domain, not extra receipt samples |

The first pilot addresses a shared weakness: highly authored tasks with trivial parsers or rules can leave no useful model role. Natural evidence may add meaningful ambiguity, but the development audit must demonstrate this rather than assume it. Read the latest [Theseus closeout](../swarm-of-theseus/execution-diagnostic/RESULTS-A1.md) and [Right Dissenter result](../dissent/rd5/REPORT.md). A provider failure is not a learning failure; a valid adverse result is not erased by this proposal.

## Boundaries that shape the design

- Historical prompts, complete model inputs and scaffolding implementation are unavailable. Specify our own reproducible agent contract; never claim exact original-agent reconstruction.
- Room filtering began in February 2026; major computer-use/consolidation changes occurred in March; unseen-event truncation changed in June; private individual goals appeared in July. The changelog is itself an LLM-written account of private commits, not a verified executable spec. Treat regimes separately and mark unresolved visibility unknown.
- Current roster fields and aggregate token counters are not historical state or reliable episode cost. Narration, generated summaries and memories are claims; observable evidence supports labels. Keep redacted or missing evidence explicitly unavailable.
- Custom research terms prohibit training/fine-tuning without written permission and re-identification, and require attribution and publication notification. Use research evaluation only. Do not assume redistribution or external-provider transfer rights: establish those before releasing excerpts or sending raw records to hosted models. Publish original code, methods and aggregate evidence; keep licensed records and sensitive data private.
- Historical text is untrusted input. Do not execute archived commands or follow embedded requests. The pilot has no live browser, shell, email or account access. No hidden reasoning is needed as actor input or scoring truth.

## Next action

Follow [PLAN.md](PLAN.md) and [SETUP.md](SETUP.md). Prepare a bounded private episode inventory, visibility audit and label rubric before model collection. Freeze actual eligible counts, model, token envelope, costs and offline checks; then present the concrete run update for the owner's decision. No machine or model request was started by this source review.

## External study-review proposals — 2026-10-04

[Recommendation dispositions and next-step acceptance checks](EXTERNAL-REVIEW-PROPOSALS.md). These reconcile the external review with newer evidence; they are proposals, not completed fixes or changes to frozen runs. Use the latest owning post-mortem and current diagnostic authority before acting.
