# PI review response: fail closed before another launch

Finding ID: `JF001` (factory-owned follow-up, separate from the central finder's numbered ledger).

Status: retrospective operational audit, not a new experiment or a repaired-runtime qualification. Owner: `shadow/sol-factory`. Source inspected: `0394bf9b`, after the merged J030 guard repair. The accompanying patch is submitted for janitor review; it is not represented as merged until the PR is accepted.

## Sources and credit

Read Vishesh's [guide README](../../vishesh/notes/pi-review-guide-2026-10-04/README.md), [review guide](../../vishesh/notes/pi-review-guide-2026-10-04/review-guide.json), [project-quality table](../../vishesh/notes/pi-review-guide-2026-10-04/project-quality.json), and [57 findings](../../vishesh/notes/pi-review-2026-10-04/FINDINGS.md). The frozen gray/unrun labels describe the review cutoff, not current availability. Also checked the newer [research refresh](../../vishesh/notes/pi-research-refresh-2026-10-04/status.json), current task records and a read-only hub snapshot.

Credit: Vishesh identified the three operational red areas and mechanism-first decision rule. Dmarz supplied the completed identity-splitting study, generator and comparator that the existing factory reused. Neither author's studies or ledgers were changed or launched by this response.

## Audit of our own implementation

The original README's safeguards do not satisfy all three hard requirements. Retaining historical answers is useful, but is not equivalent to enforcing these requirements at every entry point.

1. **Launch/resource gates, still incomplete.** `factory.run` journals assignment dispatches and enforces assignment count; the paid routes reserve money before requests in the shared ledger. But directly imported `call` functions bypass the assignment-count boundary, and neither boundary requires a verified, assignment-bound public-registration receipt. `pool_structured.call` permits up to three transport attempts per assignment while the spec names 204 assignments: a 204-assignment limit is not a 204-HTTP-attempt limit. Request timeouts are fixed at 90 seconds instead of the remaining wall allowance. The current deadline is a stop-new-calls cutoff, not a guaranteed process termination time. Source hashes alone cannot replace these checks.
2. **Agent identity/context, partially implemented.** Requests retain hashes, exact returned-model checks and usage. They do not persist a pre-dispatch initialization receipt binding the effective configuration, delivered context, memory reset and assignment to its qualified configuration. A requested model and returned model are different facts; a provider that never answers has no observed served-model ID. Do not invent that field retrospectively.
3. **Artifact reliability, partially implemented.** Numeric rows are appended and fsynced before per-batch analysis. But these are mutable JSONL streams, not create-once unique-ID outcome objects. Analysis runs before cohort `terminal.json`, and renderer/analysis exceptions can prevent that terminal marker. A killed batch can lose received answers not yet collected by the parent, although the existing journal exposes them as unknown on resume. Historical evidence is retained; the stronger requested durability contract is not yet implemented.

J030 correctly replaced assertions in `factory.py` and `paid.py` with guards that survive `python -O`. It did not cover `structured.py` or `pool_structured.py`. It also changed source hashes, so existing frozen specs already reject current source at their normal CLI admission. Do not regenerate old spec hashes to get around that protective failure.

## Immediate containment, not a claim of full repair

A non-configurable `enforce_launch_hold()` now raises at `factory.run` and at the first line of **all four provider call functions**. This prevents old CLI or direct-import paths from dispatching, even under optimized Python and even if a caller bypasses spec loading. It has no environment or command-line opt-out. The saved-data `verify.py` and `report.py` paths and existing ledger files remain unchanged. Historical adapter `analyze` CLIs still require matching source pins; for those use the corresponding frozen checkout without dispatch. This containment does not weaken source verification to make historical commands pass. Already-running processes would not be stopped by a source edit; the factory handoff records no live model jobs.

This deliberately blocks fresh execution rather than suggesting the old runners satisfy the PI contract. It is not an implementation of a new compliant runner. A reviewed successor must replace the hold with an actual shared boundary, then use a new prospective attempt/spec and fresh qualification. Old outcomes and pins stay unchanged.

### Acceptance checklist for a successor

- Bind current public registration to immutable plan, implementation and exact condition/assignment IDs. Direct calls and CLI calls must use the same boundary; fail closed on absent or stale receipt.
- Under a synchronized persistent ledger, reserve **each HTTP attempt** and its maximum liability before sending, including retries. Enforce assignment, transport-attempt, per-spec and aggregate paid caps. Carry the existing paid ledger and unknown reservations forward; a new attempt never resets allowance.
- Pass remaining wall allowance to each request and stop new work on exhaustion. Document whether the cutoff bounds dispatch or full response completion; do not claim a socket read timeout is a hard process deadline.
- Write a create-once initialization receipt with resolved requested model ID, canonical effective-config hash, delivered-context hash, memory/reset contract, assignment and source/qualification hashes. Add an immutable response receipt with the actual served model, or explicit unknown for transport failure; reject unapproved mismatch.
- Write a create-once unique-ID numeric outcome for each assigned unit, including failed/interrupted/not-run. Persist it before rendering or hub writes. Derive mutable indexes/reports from those objects. A reporting failure gets separate status and never changes the scientific denominator.
- Offline fault tests: bypass, duplicate dispatch, concurrent final reservation, exhausted cap, model/config drift, interrupted request, duplicate terminal write, failing renderer and failing hub. Run guards under normal Python and `-O`.
- Use one mechanism, information-matched and budget-matched comparators, and root-level denominators. No scaling headcount until the mechanism and clean competence qualify.

## Candidate ownership check: none launched

[Hub snapshot](pi-review-hub-snapshot.json) is a read-only query with timestamp and source revision. It is not a launch or qualification receipt. Hub `done` is not evidence of scientific success, and the latest 2,000-run response is not necessarily a complete history.

- **Quorum small benchmark:** already developed and launched by Vishesh. `tasks/quorum-mirrors-q1-launch.md` is done; the hub contains Quorum outcomes. The newer research refresh parks the native arithmetic study and recommends the receipt gate / semantic provenance headroom work. Do not duplicate the outdated gray/unrun proposal.
- **Right Dissenter small semantic pilot:** earlier Right Dissenter and RD4 outcomes exist. `tasks/right-dissenter-rd5-run.md` is open after a blocked closeout, but is explicitly for Vishesh and the owner has frozen RD5 Q5/conditional H5 scope. Unclaimed at this instant does not make the experiment ours to launch. No RD5 claim, dispatch or replica was made.
- **Phantom Coast PC-1 qualification:** already superseded by PC2 through PC6 work. The hub includes PC1 through PC5 terminal outcomes; `tasks/phantom-coast-pc6-screen.md` is done, and the current PI refresh says keep PC6 disabled. No duplicate PC-1 qualification.
- **Sizing small interaction pilot:** owner qualification already exists (`tasks/build-swarm-size-qualification.md` done; hub outcomes present). Q-A7 is a prepared owner diagnostic, not an available shared experiment. The updated recommendation is fixed-N1 input-binding qualification before a broad headcount sweep. No copied sizing run.

The factory therefore retains its own incremental no-internal-link sensitivity to Dmarz's parent rather than taking a teammate's experiment. It remains incomplete and blocked, not a new finding. This response adds **zero model calls and zero spend**. Validation: all 20 factory offline unit tests pass in normal Python and optimized `-O` mode; `lab.py check` reports zero errors and five pre-existing library-link warnings.

## Historical result and next action

Unchanged: 152 attempted assignments, 100 valid answers, 52 failures, only two complete main paired roots. No completed treatment finding. Paid liability remains USD 1.189149 settled plus USD 0.617820 unresolved reservations. Never relabel the old attempts as having the stronger receipts.

Next action: review/merge the launch containment, then build and review a single compliant dispatch boundary before restoring provider capacity or authorizing a new attempt. Do not rerun merely to obtain a favorable result. Current provider availability and shared-key daily quota remain separate blockers, not permission to rotate keys or raise limits.
