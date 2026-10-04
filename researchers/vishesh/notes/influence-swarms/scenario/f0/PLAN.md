# F0: diagnose structured-output whitespace degeneration

Prospective diagnostic proposal, 2026-10-04. No B2-E0 restart or retry authority is implied.

## TLDR
A B2 evaluation response reached3072completiontokens after emitting2579trailing spaces outside a closed rationale string. It omitted the remaining JSON fields/closing object. Test a12-request2×2 formatting discriminator on that fixed captured self-check context and an unaffected successful cost self-check: original versus compact-format instruction, and original versus relaxed backend free-text constraints. Preserve the model, provider,3072token cap, all task facts, output keys and strict local validation. Rawresponses stay private; public results are numeric diagnostics and provenance.

## Question and prediction
Is the failure sensitive to compact-format guidance, backend string constraints, both, or neither? Merely raising the token cap could permit longer whitespace loops. The diagnostic distinguishes this from long reasoning, tool invocation, content filtering or missing task evidence. It cannot estimate a rare population failure rate from twelve selected calls. All-success is inconclusive about the original stochastic failure mechanism, not proof of a cure.

## Setup
Freeze two exact native request bodies privately by SHA-256: the failed b2-location-2 neutral simple self-check and a successful b2-cost-0 neutral simple self-check. Preserve each captured previous report. These are inspected development contexts for this repair; no holdout claim. Four conditions: original prompt/original schema; compact prompt/original schema; original prompt/relaxed text schema; compact prompt/relaxed text schema. For each condition use two fresh executions of the failed context and one of the unaffected context:12calls, no replacement.

The compact suffix asks for minified JSON with no whitespace outside strings, conditions≤80characters and rationale≤100characters, with every required field completed. The relaxed schema removes only pattern/maxLength constraints on backend string fields. Required keys, types, enums, numeric fields and all local160/120character/ASCII limits remain unchanged. Invalid or semantically wrong replies stay outcomes. No salvage or trimming is accepted as native completion.

## Protocol
Run the frozen twelve requests once each, paced≤4starts/second with at most4independent requests. A known returned length/schema failure is the diagnostic endpoint and does not suppress later planned diagnostic cells. A transport, served-route, missing-usage or cost violation stops new dispatch and drains/account in-flight responses. No retries, newmodel, fallback or machine. Use the existing original ledger and allocation, finite maximumUSD0.058368 if explicitly assigned from unspent scope. Record every reservation, provider dispatch, reply,finish_reason,usage,whitespace suffix and local structural/semantic assessment.

## Metrics
Per condition/context: structurally complete outputs, exact local contract pass, trailing-whitespace count, completion/reasoning tokens, reported cost, acceptable action and full candidate checks/costs. Report every physical request and no independence claim beyond these two selected contexts. Do not select a condition because it produces a desired procurement choice. A credible repair candidate must satisfy localstructure and semantics on both contexts, with no whitespace degeneration; an equal all-success result leaves repair mechanism uncertain.

## Decision and boundaries
Publish the failed B2-E0 operational/scientific closeout, retaining64reservations,61validated outputs, one known lengthfailure, two relay-denied calls and1856unstarted requests. Existing relayjournals prove the two denials precededproviderdispatch; reservations are preserved and originalsummary is not silently rewritten. B2's successful96-call qualification remains valid only for its original outputcontract.

A later full study requires its own prospective execution decision. It may need an explicitly bounded, accounted recovery policy for known returned format failures rather than globally abandoning all independent cells after one malformed reply. That policy must never retry ambiguous transport or valid bad decisions, erase first-attempt failures or invent new funds. This diagnostic authorizes no such main-study change.
