# What changed in the research question atlas

Update 2, 2026-10-03. Owner: dmarz/question-atlas. **Human-requested unreviewed hunches for selection.** No experiments were run or approved by this update.

The bank now contains **202 candidates across 15 areas: 59 new, 36 revised and 107 unchanged**, linked to 301 distinct source records. The refresh retains all 143 original IDs and incorporates research through main `a860443d09c80fda1d87ddb9fc322811fb6801dd`. It includes work that arrived during the refresh: the LLM-swarm survey's response to review and the now-merged simulator survey. The [input inventory](research-delta-v2.json) lists 379 new and 56 edited catalogue records and maps directly cited records to candidate IDs. It records the scope of the comparison, not a claim that every source was read in full or that every new source deserves a new question.

## Candidate change inventory

| Bank | New | Revised originals | Unchanged originals |
|---|---:|---:|---:|
| Physical | 0 | 3 | 35 |
| Society | 8 | 11 | 26 |
| Security | 17 | 11 | 25 |
| Methods | 12 | 11 | 21 |
| Budgets | 22 | 0 | 0 |

**New IDs:** BUD-01–22, SOC-38–45, SEC-37–53, MTH-07–15 and SIM-05–07.

**Revised IDs:** PHY-03, PHY-23, PHY-25, SOC-01, SOC-02, SOC-07, SOC-10, SOC-11, SOC-15, SOC-16, SOC-27, SOC-28, SOC-34, SOC-37, SEC-04, SEC-06, SEC-07, SEC-08, SEC-14, SEC-19, SEC-21, SEC-23, SEC-26, SEC-33, SEC-34, RL-03, MTH-01, MTH-02, MTH-03, MTH-04, MTH-05, MTH-06, SIM-01, SIM-02, SIM-03, SIM-04.

Revised means the editable question, test, evidence relationship or prerequisite changed. Catalogue metadata refreshes alone do not mark a card revised. The rendered bank records the status beside every ID.

## Changes that matter for choosing experiments

| Research input | How it changes the bank |
|---|---|
| Agent budgets, resource allocation and B1–B5 | Adds a fifteenth topic and 22 questions. Distinguishes visible information from enforced limits, one solver's allocation from peer bargaining, useful delegation from quota-driven spawning, and shared-ledger coordination from harmful spending imitation. |
| Revised LLM-swarm survey and correlated-error search | Narrows effective-team-size and diversity claims, adds stronger comparators, and separates wording imitation from belief change. Prior results and counterexamples shape the tests; a diversity benefit is not assumed. |
| New false-name mechanism papers | Adds tests of complementarities, scheduling, trust forwarding, participation costs, temporal reports and voting power. Theorems stay within their stated domains; arbitrary task markets do not inherit auction guarantees. |
| Completed contagion scan and fork-merge setups | Adds matched factual-error versus mock-policy-violation propagation, shared-store reinfection, complete fork-return stages, release from quarantine, and cumulative consequences. Separates prevention from eventual recovery and offline detector quality from the effects of live isolation. |
| New dataset catalogue | Supplies concrete routes for testing trace labels, split leakage, evaluator information, translation, failed-run selection, session-versus-team labels, collection changes, entropy, offline policy evaluation and best-of-many comparisons. Catalogue presence does not establish usable ground truth. |
| Simulator survey and teammate smoke tests | Grounds existing tests in specific environments and reveals missing controls: visibility boundaries, scheduler semantics, blind policies, replay contracts, accounting and joint-action support. Smoke tests inform feasibility; they do not establish new scientific effects or portable throughput. |
| External-evidence and dissent design bundle | Refines the existing retrieved-evidence question with locked private judgments and equal-budget checks, and connects to evidence-based dissent and provenance questions. Its provider/MCP scenarios stay fictional and local; surrogate plots, cost assumptions and unreviewed source claims are not measurements. |
| Agentops hub/reporting and GitHub dashboard work | Updates operational context and possible future reporting paths. No server capacity, paid run, deployment or independent validation is inferred from available infrastructure. |

The external-evidence bundle connects to SOC-07/09/27/28/37, SEC-03/08 and the budget controls. Shared retrieval, peer transmission and final decision quality need separate measurements; evidence-root weights and extra checking need separate ablations. Oracle ancestry is a diagnostic ceiling, and noisy or shuffled ancestry is a control. Its older “nothing built” inventory is superseded by the shared methods toolkit and simulator catalogue. This atlas does not approve the proposed fleet run or budget.

## The original budget hunches are preserved

The [B1–B5 note](../agent-budgets-hunches.md) remains the originating researcher's hunch document. These cards make its comparisons more discriminating; they do not approve its suggested experiment ordering.

| Original hunch | Candidate IDs and distinctions |
|---|---|
| B1: visibility × pooling | BUD-01 tests the interaction; BUD-02 separates aggregate balance from named peer-spend information. |
| B2: identity splitting for quota | BUD-06 tests endogenous excess spawning; BUD-07 separates disclosure from discovery; BUD-08 compares fees and lineage budgets; BUD-09 tests useful work under conservative escrow and faults. |
| B3: who divides the budget | BUD-10 compares peers, coordinator, equal shares and auction; BUD-11 tests cost bids against calibration; BUD-12 tests replan timing; BUD-13 tests difficulty diagnostics. BUD-18/21/22 extend resource accounting, learned allocation and service floors. |
| B4: tacit budget cartels | BUD-14 tests useful coordination through a ledger; BUD-15 randomizes peer-spend norms to distinguish imitation from common task costs; BUD-16 separates authority labels from actual spending rights. Similar spending alone is not evidence of a cartel. |
| B5: misreported budgets | BUD-03 varies displayed versus enforced balance; BUD-04 separates context and spending signals; BUD-05 tests calibrated forecasts. BUD-17/19/20 examine finishing reserves, advisory targets and accounting across compaction/tools. |

## Corrections and limits carried forward

- The R³ allocation study concerns one model dividing a budget across problems; it is not direct evidence about peers negotiating a pool. A separate shared-API-budget study supplies the closer group comparison.
- A hard metering proxy can reject requests; an agent's attempted overspend is different from actual billed spending. Advisory targets and per-request output limits are also different controls.
- The new contagion scan is complete. The older setups report still has stale absence claims, and its claim that every Byzantine threshold needs independent faults is too broad. This bank uses corrected, scoped comparisons; it does not silently amend the original artifact.
- Error spread, harmful instruction adoption, persistent memory changes and weight merging remain distinct experimental objects. End-state recovery does not erase earlier consequences.
- Source depth is inherited catalogue metadata. Targeted primary checks in the lane notes do not upgrade it, establish novelty, or close the read-depth audit.
- Dataset families, repeated turns and generated variations are not automatically independent samples. Ground-truth labels, legal information sets, access, licenses and contamination checks remain prerequisites where specified.
- Recorded-response replay can test execution determinism. It does not show that fresh model calls reproduce the same outputs. Different simulator workloads cannot be ranked by raw throughput as if they perform equivalent work.

## Reviewing the update

Open [review.html](review.html) locally or use the existing local canvas. Filter **New in this update** for additions, **Revised in this update** for changed originals, or **Needs review again** for your older decisions on changed cards. The full bank remains searchable across all fifteen areas.

The browser keeps the same local storage key and stable IDs. It preserves prior status and notes. Revised cards flag old reviews until you explicitly keep your choice or choose a status for the current version; editing a note alone does not acknowledge a revision. New exports include a content fingerprint for each reviewed candidate. Legacy exports remain importable; unknown IDs are skipped and overlapping known IDs replace their local decisions. Keep separate reviewer exports before combining views. Browser and canvas reviews remain separate local stores; nothing is sent automatically.

No automatic ranking or shortlist was added. Formal promotion still requires focused prior-art review, the applicable survey gate, an independently reviewed hypothesis, and a committed protocol. The LLM survey has responded to its earlier **revise** verdict and awaits re-review; this update is not that independent approval. The simulator survey remains in progress despite meeting mechanical floors, and agent budgets still needs its survey.

## Reproduce the review material

The five editable banks are `physical.json`, `society.json`, `security.json`, `methods.json` and `budgets.json`. `revision.json` freezes the research cutoff and original candidate fingerprints. Run `python3 src/question-atlas/build.py` from the repository to validate and regenerate the consolidated bank, Markdown and HTML. Its optional `--canvas` path refreshes the local projection without writing review state.

`src/question-atlas/verify-review.cjs` checks the generated browser using an isolated Chrome profile: legacy selections/notes, revision acknowledgment, filters, import/export and mobile overflow. It requires Playwright on the Node module path and a local server for the generated HTML. Source and brief links are checked by the renderer; editorial judgment about a discriminating test remains a human task.

Detailed reading scope: [societies and budgets](society-scope.md), [security](security-scope.md), [physical systems](physical-scope.md), [datasets and simulators](datasets-scope.md), [overall scope](scope.md).
