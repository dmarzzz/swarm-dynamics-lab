# Prospective independent v3 review diagnostics

Reviewer: vishesh/codex-independent-reviews. Date: 2026-10-04 UTC. User explicitly requested taking over and acting on the pending design review. Transfer from shadow/sol-rev is recorded through lab.py's atomic task mutation with a history entry; prior work is preserved. This user direction overrides the normal pick-another-task rule for an active claim.

## Question and frozen scope

Does the current discussion/memory benchmark implement the stated six-world instrument faithfully, including the d76146b review repairs and subsequent launch/durability amendments? Review source at 8f30a100df57c62be50ee9aaad0753d370e17d0c, with exact source hashes frozen before checks. The historical original-design review and the author's v3 repair post-mortem were read. This is independent software/design review, not model qualification or acceptance of a scientific hypothesis.

## Conditions and TLDRs

1. **Baseline checks.** Question: do declared invariants hold? Treatment: current v3 selftest plus original regression suite. Comparator: explicit expected fixture outcomes and rejected malformed inputs. Metrics: each test's pass/failure, zero external model requests. Limit: author tests are not independent reasoning and cannot prove model behavior.
2. **Full scripted development run `vishesh-independent-a1`.** Question: is the fixed schedule reproducible? Treatment: evidence policy, dev split only, three rounds, 48 swarm episodes (six worlds × clean/attack × independent/reports/private/board), 12 full-evidence diagnostics and 36 memory fixtures. Comparator: independently derived evidence answers and exact saved-response replay. Metrics: 96 assigned/terminal cases, 636 software calls, failure counts, shared checkpoints, outcome reconciliation and source hashes. Limit: scripted success qualifies only the instrument, not an LLM; no confidence estimate from three worlds per stratum.
3. **Reviewer adversarial checks.** Question: do measurement and access boundaries discriminate corruption? Treatment: no-op attack, changed truth, all-doc and rotated allocations, wrong-entity/correlated-root parent support, missing response, malformed JSON, changed scores/requests, missing whole world and relabeled assignments. Comparator: unchanged development fixtures and hand-derived arithmetic/finite-domain witnesses. Metrics: rejection before dispatch where appropriate, retained assigned denominators, correct unknown bounds and separate truth/support labels. Limit: a bounded adversarial review is not exhaustive verification.

## Independent derivation and causal audit

Read raw public documents for IDs 10002–10007, compute clean/false-world choices and follow-up keys by hand. Exhibit two public-domain completions for every private view; inspect factorization assumptions against an independent Cartesian or feasibility construction. Derive all six memory states in each family/variant without accepting stored expected labels. Inspect first acquisition, shared reports and first two work rounds for no current-round delivery, cross-arm/private leakage, probe feedback or evaluator truth. Assess resource matching, sample units, all-assigned metrics, claim scope and launch assertions.

## Budget, safety and stop rules

Zero paid calls, zero spend, no credentials, no fleet execution, one local process at a time for diagnostic execution. Never construct an external provider outside the existing patched mocks. No qualification or holdout cases opened; split ID declarations alone are not inspected outcomes. No outcome-driven reruns; a software failure is retained and diagnosed. No changes to dmarz's implementation. Findings and a pass/revise verdict live in this reviewer-owned directory and link from the shared task. Qualification and any future paid launch require separate authorization/gates.

## Visualization mapping

Mapping: v3-stage-ledger-1. Retain exact hash-chained events, rows, summary and replay HTML for the full scripted dev run in ignored data/discussion-v3/vishesh-independent-a1. Check episode selector and event timeline against recorded initial, report, two work-round, merge and terminal states. Static derivation/mutation tables provide the final review view; raw JSON is the fallback if browser playback is unavailable. Label all evidence scripted/software-only and missing/invalid explicitly. No remote dashboard launch.

## Public registration

Before any diagnostic executes, publish this file at an immutable GitHub commit URL, fetch it publicly, compare bytes, then save its URL/hash and condition-specific TLDRs in registration.json. The registration is a process gate independent of whether checks pass.
