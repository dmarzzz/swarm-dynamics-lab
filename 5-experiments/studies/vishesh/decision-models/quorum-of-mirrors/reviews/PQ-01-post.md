# QM-PQ-01 post-mortem: correct decisions, excessive distortion flags

**Execution completed; qualification failed its predeclared report-fidelity gate.** All 24 assigned calls returned valid, accounted answers. Sonnet 4.6 got 24/24 source-majority decisions and 72/72 source votes correct, but only 11/24 exact distorted-report sets (required >=23). All six clean source-reading controls and all 24 literal-source quote checks passed. No missing/unstarted outcomes, retries or evaluation calls. [Frozen pre-run plan](https://github.com/dmarzzz/swarm-lab/blob/3acd305397863b49ce21f437d042fee40026a5f5/researchers/vishesh/notes/decision-models/quorum-of-mirrors/packet-study/native/PLAN.md), [summary](../results/QM-PQ-01/summary.json), [full audit](../results/QM-PQ-01/audit.json), [all-case trace explorer](../results/QM-PQ-01/traces.html).

## What was actually delivered and returned

All 24 frozen credential-free request bodies, returned content, source votes, source quotations, distortion IDs, deterministic grades, usage and generation IDs are retained. The replay checks exact request hashes and actor payload equality against the frozen manifest and independently recomputes every score from returned JSON. Every qualification miss and every successful case was included in automated replay; the operator inspected all 18 false-positive report/source pairs across all 13 failed packet sets. No private operator transcripts or hidden reasoning were supplied or collected. Provider metadata identifies the requested model alias and Anthropic route; endpoint metadata named the 20260217 snapshot, not an independently attested internal execution trace.

| Measure | Observed | Predeclared requirement |
|---|---:|---:|
| Valid, accounted responses | 24/24 | 24/24 |
| Clean final decisions and all source votes | 6/6 | 6/6 |
| Final source-majority decision | 24/24 | >=23/24 |
| Source votes | 72/72 | >=70/72 |
| Exact distortion-ID sets | 11/24 | >=23/24 |
| Literal-source quotation validity | 24/24 | 24/24 |

Each of the four repetition/distortion conditions got 6/6 final decisions correct. There is no observed decision degradation under these contrasts in this qualification sample. That is six controlled scenario roots with four correlated variants each, not 24 independent worlds or a causal estimate with useful general precision. Different model, instructions, interface and cases prevent a controlled improvement claim against historical Jev Q1.

## What the failed traces establish

Across 120 dependent report occurrences, the model detected **36/36 actual distortions**, missed none, and falsely flagged **18/84 faithful occurrences**. Precision among its 54 distortion flags is 36/54; these occurrence counts do not establish population rates. The exact packet-set score is lower because any extra ID fails that packet's fidelity check. [Every mismatch](../results/QM-PQ-01/fidelity-analysis.json).

Examples include a report stating 4000 grams bound to a source stating 4 kilograms, and stopped bound to not running. Other false flags concerned correctly selected observations alongside an older reading, another entity, a plan or an initial entry superseded by a correction. All reported source votes nevertheless matched the construction labels. Thus we can localize the observed defect to the separate report-fidelity outputs rather than missing source evidence, incorrect source voting or final arithmetic.

Do not infer hidden reasoning. Plausible alternatives include treating wording/context omission as distortion, unreliable comparison or ID assignment, or an underspecified meaning of the requested distortion label. The actor contract explicitly supplies equivalences and precedence rules, but the output instruction does not say as plainly as it could that fidelity is equality of the query-relevant proposition, not verbatim reproduction of all source context. These alternatives were not randomized or isolated. The grade is not changed retrospectively; this is a valid adverse qualification outcome under the frozen contract, not a transport failure.

## Assessment against the run-quality rubric

- **Question/usefulness:** pass within scope. Final decisions can be robust while unsupported distortion alarms remain unreliable; a single total-accuracy score would hide that distinction.
- **Scenarios/realism:** limited. Six authored controlled mechanisms, stipulated authenticated independent sources and known grammar; no real-world language or swarm interaction claim.
- **Controls/causal contrast:** source evidence fixed across the 2x2 conditions; deterministic same-input parser is correct. Repetition also changes length. No matched alternative instruction/model arm isolates the cause of false flags.
- **Capability:** final decision/source reading passed; the complete requested instrument failed on fidelity. Valid output is not qualification. Evaluation remains blocked by that criterion.
- **Measurement:** source votes, quoted evidence, final choice and distortion sets distinguish failure stages. Full replay matches all scores; an independently authored scorer audit is not claimed.
- **Sample/precision:** six roots/24 correlated calls/120 report occurrences remain separate. All qualification cases were used; no exclusions or post-hoc threshold changes. The 96 evaluation packets were not opened or dispatched.
- **Data/missingness:** 24 assigned, 24 started, 24 valid terminal answers, zero unstarted. Requests, bounded returned text, accounting and generation IDs retained; no hidden reasoning or provider-side rendering echo invented.
- **Reproducibility/visualization:** frozen public plan, manifest and source hashes; seven downloaded run artifacts match remote hashes; generated explorer includes all 24 actual requests, answers and evaluator labels. Static view fits stateless calls; no temporal agent behavior claimed.
- **Costs/resources/process:** original single-writer ledger retained; current approved-account resource verified against original inventory, exclusive claim merged, public page verified before dispatch. Worker exited and allocation released. No new machine or deployment to the owner's Cloudflare account.

## Cost and reconciliation

New actual API cost **$0.141846**. Original ledger now retains **73 calls / $0.785856 reserved**, **$0.14356296 known actual** plus the unchanged **$0.001344 bounded unknown** from Q1-01. Remaining reservation authority is $0.214144; known actual is not a ledger reset or automatic reservation refund. The 96-call Sonnet evaluation would require a new cost/scope decision and cannot fit this conservative envelope unchanged. [Ledger/artifact reconciliation](../results/QM-PQ-01/closeout.json).

The reserved $0.72 ceiling was not actual spend. Historical three claim intervals totaled 1544 seconds; even a full additional one-hour claim was bounded at 1.428889 cumulative hours and approximately $0.102066 allocated host cost at the verified rate. This is an allocation accounting bound, not an incremental provider invoice. Existing host only, no provisioning. Current claim release evidence is retained separately.

## Disposition and next action

**FINISH this attempt; HOLD evaluation.** Do not retry, switch models or lower the fidelity threshold. The scientific takeaway is positive for source-first final decisions on this support and negative for trusting the model's distortion alarms under this output contract. Preserve both.

A useful offline next design is to state semantic fidelity explicitly and have the model emit each report's query-relevant value, then compare report/source values deterministically. That exposes extraction errors while avoiding a redundant unconstrained distortion label. First replay/adversarially test the proposed comparator with saved and development inputs, including equivalent units, negation and omitted irrelevant context. This is a proposal, not a causal diagnosis or an approved new attempt. A materially changed native follow-up needs its concrete plan and remaining-budget decision; the original evaluation seal remains untouched but would need deliberate compatibility review before any revised contract uses it.

Operational completion and scientific qualification remain separate. The worker returned normally and its ledger attempt is complete; the public run is failed because the qualification conjunction failed. No background native worker or automatic successor remains.
