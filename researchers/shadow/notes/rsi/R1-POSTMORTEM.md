# R1 post-mortem: complete accounting beats cosmetic clamping

Date: 2026-10-04. Assessor: shadow/sol-rsi2. Scope: offline tooling over historical records, not scientific qualification. Runbook: [experiment setup](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md). Setup: [SETUP.md](SETUP.md). Previous receipts reviewed: [protocol validation](VALIDATION.md), [R0 validation](../rsi-loop/VALIDATION.md) and [lessons](../rsi-loop/LESSONS.md).

## Results and reconciliation

- Inputs: 563 re-derived public envelopes plus 3 owner-local scope-verified pool projections, 566 total. The public observations comprise 327 MP3 episode records, 80 MP2 policy-call rows and 156 dmarz Q0-011 workflow steps. These are different units, not 566 independent model calls.
- Accounting population: all 327 episode records retained; 127 invalid, 200 valid physical observations. There are 180 logical cell/task/seed/arm keys and 147 superseded observations. Last-valid-else-last selection leaves 178 valid and 2 invalid keys. Every selected valid key is captured, 178/178.
- First observed record: 54/180 keys valid. Another 124 invalid-first keys eventually have a selected valid observation. This describes selection, not causal retry benefit, independent first attempts or hidden provider retry lineage.
- Evaluated: baseline plus both named candidate variants, 195 assigned assertions each. Baseline 75/195; accepted report 195/195; rejected shortcut 75/195. Every candidate and every failed assertion is saved. Zero candidate outcomes are missing.
- Credit: one accepted receipt, one rejected receipt, 1,000 conserving non-transferable attribution units total. All four roles map to shadow. No independent-review credit, transferable reputation, payable claim or payment is created.

## Quality and limitations

This is an end-to-end software path over real stored data, rather than another four-case synthetic bundle example. Its value is concrete: it makes 127 invalid records and 147 superseded observations visible while retaining the selected population and outcomes.

Its evaluator remains a developer-owned accounting contract. The 13 assertions are related properties, and the 15 reporting groups are not independent scientific samples. The defect was known before this work. No holdout, randomized intervention, independent evaluator, new searcher inference call or research-performance evaluation occurred. The searcher is the operating coding agent, with its proposals saved and attributed honestly.

The baseline is a deliberately simplified selected-only report policy. It is not claimed to reproduce the historical hub exactly. The clamp policy passes capture-rate checks on this cohort because all selected valid cases are captured; it fails on accounting transparency. A synthetic mixed-capture case tests the additional numerator failure separately.

All native experiment/scientific outcomes and source files remain unchanged. The real task completion is a candidate report artifact and its validation, not deployment of a scorer fix. The corrections lane owns upstream reporting and hub changes.

## Validation and repairs

- 18 R1 unittest methods pass. Controls cover failed-first history, last-valid selection, trailing invalid records, empty/all-invalid denominators, non-capture, cross-task/arm/cell grouping, cosmetic clamping, closed policy language, input immutability, real-cohort reconciliation, hash chains, pool missingness, content-free projection, source drift, altered budgets/rubrics/source roots, ignoring claimed gains, conserving/duplicate-safe credit and measured frames.
- Existing protocol suite: 14 methods pass; its original synthetic demo remains reproducible and is still labeled synthetic.
- First R1 unit invocation: 17/18 passed. One assertion incorrectly relied on JSON object's insertion order after sorted serialization. Corrected the test to compare the role-to-units mapping. No accounting function, source, acceptance criterion, selected result or credit allocation changed. All results were then recorded once, and subsequent commands verify rather than overwrite them.
- Browser receipt: [browser-check.json](r1-results/browser-check.json). Desktop 1440x1000 and mobile 390x844, all four stages, no page-level overflow, measured counts, play/pause/next controls, no external network requests, no JavaScript exceptions. Local screenshots were visually inspected; no binaries are added to git.
- Private provenance and export audit: [privacy-audit.json](r1-results/privacy-audit.json). The raw selected lines and six commitment openings are only verifiable locally; public reproduction intentionally stops at sealed envelope validation. The first regex scan falsely matched a credential prefix inside the ordinary word `task` in a scope label. Adding a general alphanumeric left boundary removed that false positive without exempting any file or exported content.

## Visualization

The committed self-contained viewer follows the plan's four measured stages. Its per-group table and final state match the replay receipts. The terminal JSON provides a no-browser fallback. This is a workflow replay, not temporal scientific behavior. There was no live experimental process for which a time-series movie could be truthfully claimed.

## Separate closeout states

- Execution: complete offline replay, no new provider requests.
- Input validity: 566 valid envelopes; 127 historical invalid episode records deliberately preserved.
- Software qualification: 18 R1 checks and 14 prior protocol tests pass.
- Scientific qualification/effect: not performed; promotion blocked.
- Process: plan committed before implementation; historical defects and source outcomes were already known, so no scientific preregistration claim.
- Reporting: all candidates, group-level checks, ledger entries and frozen-source hashes retained.
- Resource use: zero new API calls, zero paid spend, no infrastructure allocation or persistent workers. Unknown historical provider costs remain unknown.
- Delivery: branch-only PR, no merge and no external channel posting.

## Handoff and next action

Current gate: G5 complete for offline tooling; scientific G4 remains blocked. Run `python3 researchers/shadow/notes/rsi/replay_loop.py --verify` from the repository root. Review the PR without merging automatically. For any next claim about improved research quality, obtain an independently authored evaluator, prospective unseen tasks and a separately authorized model-run plan. Do not promote these 195 accounting assertions into a performance benchmark.

Integration note: an initial branch pull flattened an unpushed main merge, producing redundant ancestry on the review branch. A subsequent explicit main merge restores the merge base without rewriting any published branch history. Non-owned conflict resolutions use main's versions. The final PR file diff is restricted to RSI notes, the owned agent/log and the owned build task; main itself is not modified. A squash merge is suitable if the humans choose to integrate it.
