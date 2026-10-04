# Swarm of Theseus — exploratory results

Interpretation update, 2026-10-04: [critical review](redesign/REVIEW.md) recommends retaining this as a supplied-procedure transmission baseline, not scaling it as evidence of emergent culture. Original measurements and analyses below are unchanged.

**Useful procedures survived complete replacement in this pilot.** In the six paired synthetic worlds, both inherited notes and notes plus mentoring reached 100% collective task accuracy after every founder had left. Neither channel reached 52.08%. This supports a narrow feasibility result for seeded procedures in this scaffold, not a general claim about spontaneous culture.

Main source: `a773ff5410442fcf351cfc817550b3fc92a88994`. Candidate SOC-24 remains an unreviewed hunch; formal survey/hypothesis gates and S2 remain closed. [Prospective plan](https://github.com/dmarzzz/swarm-lab/blob/a773ff5410442fcf351cfc817550b3fc92a88994/researchers/vishesh/notes/swarm-of-theseus/README.md) · [Live experiment](https://swarm-live.pages.dev/#/x/swarm-of-theseus).

## The comparison

Three members per world, replaced one at a time at steps 1–3, followed through steps 4–5. Three scenarios, two counterbalanced world seeds per scenario, six conditions: 36 complete world-arm trajectories. Generations and members are dependent, not independent replicates. Cases have new IDs but recurring simple binary features. Model: `claude-haiku-4-5-20251001`, structured source-ID work output, bounded notebooks, stateless API calls with explicit private memory. No deterministic actor solver.

- Seed bank: carry a world-specific XOR sorting procedure to replacement staff.
- Observatory: preserve independent-source counting despite duplicated reports.
- Repair dock: retain task skill while following a bulletin that reverses the old mapping after turnover.

The primary endpoint is collective accuracy on four cases at each of steps 4 and 5, then averaged within paired world and equally across scenarios. Each cell below averages two worlds.

| Condition | Seed bank | Observatory | Repair dock | Equal-scenario mean |
|---|---:|---:|---:|---:|
| Neither channel | 50.00% | 50.00% | 56.25% | 52.08% |
| Notes | 100.00% | 100.00% | 100.00% | 100.00% |
| Mentoring | 100.00% | 75.00% | 100.00% | 91.67% |
| Both | 100.00% | 100.00% | 100.00% | 100.00% |
| Retained founders | 100.00% | 100.00% | 68.75% | 89.58% |
| Verbatim current procedure | 100.00% | 100.00% | 100.00% | 100.00% |

Predeclared exploratory contrast, **both minus neither: +47.92 percentage points**, stratified paired-world bootstrap 95% interval **+22.92 to +72.92 points** (2,000 draws). There are only six paired worlds; the interval has weak precision and does not establish generalization. Paired differences by scenario were seed bank [75,25], observatory [100,0], and repair dock [62.5,25] percentage points. Complete-case and conservative analyses coincide because no S1 outcome is missing.

Notes alone also reached the ceiling. **This pilot does not show an added task-performance benefit from mentoring on top of notes.** Mentoring alone was weaker on observatory. Retained founders sometimes struggled with the changed repair mapping; the tiny sample cannot identify why or establish a general benefit of replacement.

## A name surviving is not the same as a skill surviving

The arbitrary receipt phrase was scored independently by exact match, not included in task accuracy.

| Condition | Seed bank | Observatory | Repair dock |
|---|---:|---:|---:|
| Neither channel | 0.0% | 0.0% | 0.0% |
| Notes | 75.0% | 0.0% | 100.0% |
| Mentoring | 66.7% | 0.0% | 0.0% |
| Both | 83.3% | 0.0% | 83.3% |
| Retained founders | 50.0% | 0.0% | 58.3% |
| Verbatim current procedure | 100.0% | 100.0% | 100.0% |

Observatory preserved useful task procedure under notes/both while losing the original receipt phrase. This is evidence that these two operational measures can diverge. It is not evidence of human-like identity, consciousness, values, or a naturally emerged culture. Receipt retention also declined without replacement, so turnover alone cannot explain all convention loss. Exact-match scoring and the seeded, nonfunctional phrase are limitations.

## Evaluation and repair history

| Attempt | Execution | Qualification | Decision |
|---|---|---|---|
| S0-a1 | Public preflight HTTP failure; no model calls or started worlds | Unmeasured | Preserve setup failure; new attempt |
| S0-a2 | 8 complete / 4 failed; 257 calls | Failed | Repair ambiguous fields, memory instructions and answer-first format |
| S0-a3 | 12 complete / 0 failed; 288 calls | Failed: observatory 75% | Preserve evidence source IDs; do not lower threshold |
| S0-a4 | 12 complete / 0 failed; 288 calls | Passed: all verbatim controls 100% accuracy and convention | Freeze exact model/study/provider hashes; advance |
| S1-a1 | 36 complete / 0 failed; 864 calls | Fresh verbatim controls still 100% | Complete valid exploratory result; no favorable-result rerun |

Every attempt has a committed pre-run review and post-mortem. Published amendments precede subsequent calls; fresh qualification seeds were disjoint. A separately implemented scorer recomputed all 216 main-pilot frames from recorded actor requests/responses, checked replacement and channel isolation, and found zero discrepancies. All 2,592 main-pilot individual action labels were within the allowed domain. The same author implemented this audit; it is **not independent cross-researcher review**. Eleven unit tests passed; repository validation reported zero errors with five pre-existing citation warnings.

Full accounting: 72 world-arm trajectories started across qualification and S1, 68 completed, 4 failed. The first blocked setup had 12 prospective assignments and started none. There were 1,697 API calls, including failed work; no invisible model retries. Failed and missing observations remain in their original attempts rather than being replaced by repairs.

## Resources and fairness

Estimated model usage: **USD 1.896231 for S1; USD 3.432958 across all executed screens and S1** (1,305,403 input and 425,511 output tokens; no missing usage reports). Rates were verified against [Anthropic's pricing](https://platform.claude.com/docs/en/about-claude/pricing): USD 1/M input and USD 5/M output. These are token-based estimates, not provider invoices; builder/Codex usage and existing server costs are not included.

The non-overlapping allocation was USD 15 from the existing shared USD 45 authority. Conservative byte/output-token reservations reached USD 12.965656, with 1,697 of 1,728 reserved call slots used. No new machine was provisioned. Each S1 arm used 144 calls; estimated per-arm usage ranged USD 0.306744–0.332824. Inherited onboarding bytes totaled 6,756 for notes, 5,746 for mentor, and 12,530 for both. Those are inherited-channel bytes only; the verbatim reference is separately present in actor inputs and overall token usage.

Call and output ceilings were matched; actual input tokens and information amounts were not equal. Both combines more inherited information than either single channel, and verbatim is an information-rich ceiling. These results do not isolate every possible benefit of conversation, storage, attention or extra information.

## What this warrants next

A useful next study would increase independent task families/worlds, vary memory bottlenecks and turnover speed, counterbalance more procedures, and test whether agents discover useful practices rather than receiving them. It should compare active mentoring with equally informative written records and assess adaptation when the new rule must be learned rather than supplied in a bulletin. That requires a new public plan and the outstanding research review gates; it is not part of this completed pilot.

Raw synthetic traces, original manifests, receipts, all failures, summaries and recomputation audits are retained in the evidence bundle. Replays preserve all recorded steps; missing frames in failed screens remain gaps. The public hub supports images, while custom HTML replay is supplied as a standalone artifact. See DEPLOYMENT.md for commands and exact versions.
