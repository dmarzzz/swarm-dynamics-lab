# R60 response to advisory PI feedback

2026-10-04. Advisory feedback assessed against the current R60 proposal and SP-02 closeout. No new owner authorization, native calls, spending or allocation. The pending concrete owner decision is unchanged; neither PI guidance nor draft decisions can supply it.

## Offline corrections completed

1. **Nested actor/gold leak:** actor_only previously selected the evidence container wholesale. It now constructs every evidence object from an explicit field allowlist and deep-copies the result. A fault test injects nested label, justification and URL-locator fields and verifies that they cannot enter actor context or leak through later evaluator mutation.
2. **False document identity:** URL normalization previously discarded all query parameters, potentially merging different vote records or documents. It now retains semantic parameters and drops only specified tracking parameters, while normalizing archived URL aliases. This changes document IDs prospectively; old intake receipts remain historical, not current runtime hashes.
3. **Split contamination:** a metadata-only scan of3,568 train/dev records groups normalized claims, fact-check articles and evidence documents transitively. All29 unique candidates from both development intakes are excluded, including uninspected members conservatively treated as development.1,394 rows are in their linked components;1,823 train and351 dev rows remain outside those components. No fresh qualification/evaluation content was opened or selected by this audit.
4. **Validation:**17 offline checks pass, including semantic query identity, archived/normalized cross-split matches, transitive exposure and nested gold isolation. These are software checks, not native qualification or independent scientific validation.

See [metadata audit](group-audit.json), [contract](contract.py), [grouping](group_audit.py) and [tests](test_contract.py).

## Unresolved scientific defects

**Packet support and semantic event identity remain launch blockers.** Published independent labels are not enough when the supplied evidence has ambiguous predicates, direct answer disclosure or a label/evidence mismatch. Initial content audit retained8 development controls, limited4 and quarantined12. The repaired candidate intake has not received a complete independent adjudication of packet support. Existing public labels are independent of this experiment, but the owning-agent audit is not a second independent annotation.

The largest metadata component contains1,343 rows. Shared generic reference pages can over-group unrelated events; conversely, different documents may describe the same event without an exact matching URL. Do not call the1,784 metadata components independent events. Use this conservative exclusion as a lower-level guard, then audit semantic event grouping and packet support. Do not relax it retrospectively based on model performance. Any case inspected for tuning remains development-only.

**Evidence provenance is not external truth.** A quotation from an annotated QA answer verifies what that answer says, not whether its source supports it. The intended task remains retrospective, evidence-assisted verdict synthesis. Real-time verification, raw-document grounding and authenticated independent acquisitions are outside this pilot.

**Eight roots provide feasibility evidence only.** Preserve the1/6-agent and matched private-reconsideration controls, the60-agent fork parents, all assigned denominators and per-root results. No agent-level significance, general superiority or cross-model strength inference. The board is a capped evidence-grouping policy; its omissions and actual context must be traced.

## Recommendation and exact owner decision

Recommend proceeding with the proposed staged scope only after the remaining gates pass: six-claim GPT-6 Sol qualification, conditionally followed by eight fresh event clusters with1/6/60-agent comparisons and peer/private60 forks. Maximum1,594 physical calls; USD45.39712 new API envelope and USD0.50 incremental infrastructure within the documented prospective USD50 cumulative promising tier. Original settled costs, unknown holds and ledger remain authoritative. No budget amendment has been applied and no current allocation is claimed.

The exact pending decision is **owner approval of this concrete R60 scientific scope and bounded staged execution**, not PI approval, an additional researcher signature or an extra budget request. Approval alone cannot pass corpus/support, actor/gold, model/price/context, native fork runner, runtime/public-plan or exclusive approved-account admission checks. If the final clean corpus or complete context cannot fit the proposal, publish a concrete amendment rather than silently reducing evidence or expanding calls.

Disposition: **DECISION NEEDED plus scientific/runtime HOLD**. No launch. Continue corpus quality preparation and implementation offline; qualify the exact native interface only after the genuine owner decision and all admission evidence are current.
