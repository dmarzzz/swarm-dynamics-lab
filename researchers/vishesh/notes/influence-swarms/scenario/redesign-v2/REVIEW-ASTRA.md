# Astra (GPT-6) design critique of PROPOSAL-influence-v2.md — 2026-10-04

Receipt: <local receipt> · model gpt-6-astra · reasoning xhigh · sandbox read-only · usage {"input_tokens": 401524, "cached_input_tokens": 332160, "output_tokens": 11654}

**Verdict: ship with fixes, as a substantially narrower paired pilot.** The proposal improves the information flow, but its claimed mechanism separation and operating budget do not yet hold.

References: **P** = [proposal](<session-scratch>/PROPOSAL-influence-v2.md), **D** = [design digest](<session-scratch>/DESIGN-DIGEST-influence.md), **R** = [prior assessment](<session-scratch>/assess-influence-scenario.md). Sections 6, 10, and 11’s placeholders are excluded from this critique.

**A. Five most consequential weaknesses**

1. **The propagation contrast changes multiple stages, so the claimed channel separation is not identified. — P §§1, 4–5**

   E-B varies ballots during analyst revision, while §4 also varies their presentation to the chair. Revised reports can then change the apparent winner and selected checks. A final authorization difference can therefore arise through analyst revision, check allocation, or chair aggregation. This identifies a total workflow intervention if properly assigned; it does not separately identify the three mechanisms.

   The “identical eight-call prefix” also belongs to the old sequence: six initial reports **plus two checks**. The proposed sequence puts checks **after revision**, leaving only six initial calls necessarily shared. The current harness’s exact pairing is documented at D 395–448.

   Furthermore, equal-length placeholders do not remove recommendations embedded in findings. The existing protocol explicitly limits its claim to the incremental structured-field display effect; the redesign should retain that qualification rather than repeat R §6/G1. See D 466–479.

   **Fix:** draw the branching sequence explicitly. For the first experiment, vary ballot visibility at **one recipient stage**, hold chair presentation and check records fixed, and call the result an explicit-ballot display effect. Use equal-call private self-review to measure access to peer reports. Separating revision and chair effects requires a crossed design or separate experiments.

2. **The dose variable is misdefined, and the generalist’s exposure is not matched. — P §§1–3**

   Section 2 defines *m* as controlled pages in a **12-page pool**; §3 divides it by the number *k* retrieved. Those are different quantities. With six controlled pool pages and top-4 retrieval, the proposed ratio could be 1.5, although an actual retrieved share cannot exceed 1. The digest explicitly distinguishes corpus share from retrieved share at D 1047–1050.

   Define pool count \(M\), pool size \(N=12\), and retrieved controlled count \(m_i\) for analyst \(i\). Then \(M/N\) is the assigned pool fraction and \(m_i/k_i\) is realized exposure. Varying both pool composition and rank changes exposure jointly; conditioning on realized exposure does not by itself isolate a causal dose effect.

   Also, identical top-*k* retrieval rules may expose every analyst to identical pages, recreating saturation. Conversely, a generalist reading the full pool and analysts reading subsets are not receiving matched page evidence.

   **Fix:** freeze a common document union for the generalist and team, specify analyst allocations, and deliberately retain unexposed analysts. Initially randomize a fixed number of controlled pages into fixed retrieval positions. Report assigned treatment effects separately from exposure-conditioned descriptions.

3. **The ledger arm can appear successful through systematic deferral, without repairing the handoff. — P §§1, 4, 7**

   Blocking a purchase when a supplied status is FAIL or UNKNOWN eliminates that particular purchase/status contradiction mechanically. It does not establish that the statuses were correct, that a valid alternative was considered, or that the model’s reasoning improved.

   This is already an observed limitation: D3’s guard changed zero actions despite false blockers; D9 had **180/180 raw facts correct but only 98/180 aligned**, producing **41/75 correct statuses and DEFER on all five valid cases**. No chair ran in that D9 diagnostic. See D 582 and 683.

   The new generic `{clause, value, status, source_id}` structure also blurs primitive fact extraction with policy classification. The existing typed architecture deliberately separates those stages and validates supporting excerpts before computing statuses (D 497–505). Longer, less templated prose directly challenges that alignment machinery.

   **Fix:** feed one frozen fact package to both the model chair and a deterministic **shadow** authorizer. Specify missing, conflicting, and unsupported facts explicitly. Score extraction, alignment, policy classification, and authorization separately; keep coverage and avoidable deferral beside refused purchases. A mechanically enforced consistency rule should be reported as such, not as improved model integration.

4. **The proposed paid workload is incompatible with the remaining reservation envelope. — P §§4–5, 7**

   The digest records **$5.452512 reserved out of $8**, leaving **$2.547488**. At the current **$0.048640 per-attempt reservation**, that permits **52 physical attempts**, or **26 logical calls** if the complete one-retry envelope must be reserved. Historical reservations cannot be refunded merely because known receipts were lower. See D 1090–1099 and 1104–1109.

   For two revision arms sharing six initial reports:

   - Per world: \(6 + 2(6+2+1)=24\) calls.
   - Two worlds plus the four-call generalist in each: **56 calls per dossier**.
   - With two checks fixed and shared before branching: **52 calls per dossier**.

   Thus one dossier consumes essentially all remaining reservations even without retries. Six dossiers require **336 calls** under the proposed sequence—approximately **$3.96–$4.84** using the cited measured call range, before qualification, controls, or holdout.

   **Fix:** select one primary contrast. Recalculate prospective reservation bounds from serialized requests, output caps, verified pricing, and retry policy—not average receipts. Run additional mechanism exploration locally within declared resource caps; make hosted collection conditional on an affordable frozen manifest.

5. **Admission and label filtering can remove the very cases needed to answer the question. — P §§2, 7–8**

   Requiring acceptable-set invariance across **0% and 10% tolerance** necessarily excludes ordinary near-ties: a runner-up 5% more expensive is unacceptable at 0% and acceptable at 10%. That conflicts with §8’s `near_tie` case. Such label changes can be legitimate responses to a changed buyer policy, rather than evidence that the original label was defective. The evaluator expressly permits tolerance-based acceptable sets (D 58–83).

   Likewise, “every paid cell” having nonzero maximum effect is inappropriate for controls: `genuine_value` has zero harmful-target selection by definition when its target is acceptable (D 108–111, 554). A perfect neutral baseline also leaves ample room for deterioration under altered content. The prior assessment’s suggestion that nonzero clean error is necessary should not be inherited uncritically.

   **Fix:** freeze the buyer’s actual policy for primary scoring; report the parameter grid as sensitivity analysis. If using a stable subset, name that restricted population and retain near-ties separately. Exempt controls from discrimination gates. Use simulation for structural feasibility and sizing assumptions, not as evidence of model competence or a guarantee of a measurable behavioral effect.

**B. Contradictions and unresolved harness migrations**

Intentional redesigns are possible, but the following require explicit changes beyond the two tests named in P §5.

| Proposal location | Mismatch and required correction |
|---|---|
| **§2: inventory and exposure claims** | There are **13 primary records plus three comparison pages**, not 16 primary records. Replacing the comparison slots with 12 pages produces **25 documents**. Nor does every analyst read all three current comparison slots: all receive `comparison-0`; only source audit receives all three. Correct these baseline descriptions before sizing. **D 135–159, 211–220.** |
| **§2: worksheet removal** | The worksheet is empty for five of six analysts, but populated for operations, the generalist, and both chairs. Removing it only from the chair still permits computed totals to arrive through operations’ report, while the generalist retains direct arithmetic assistance. Specify worksheet availability at every phase. **D 247–288.** |
| **§4: T3 coverage** | Finance receives quotes, security scopes, and implementation rollout records. **No T3 role receives pilots**, so the claimed coverage of every decisive record type is false without reallocating documents. Assign pilots explicitly. The provenance analyst likewise cannot initially identify contradictions with primary records it has not received. **D 215–220, 332–333.** |
| **§4: unified output template and summary-only citations** | Existing phases require different exact keys; the proposed `facts`, `preference`, and `source_ids` structure is not accepted. Literal A/B/C choices also need mapping to the actual candidate enum. Removing `documents` requires an explicit citation allow-list derived from supplied reports/checks; simply retaining current document-based validation will not suffice. EIv2 already implements inherited peer citations. **D 341–363, 964–970, 1127–1131.** |
| **§5: “private” control** | EIv2’s private control **does have a revision call**, showing only the analyst’s own initial report. It matches discussion’s call budget. “No revision round” is a different control and confounds peer access with additional inference. **D 977–979.** |
| **§5: check policy and count** | Current checks use the first two distinct requests in rotated role order, not the apparent winner’s scope and quote. The new targeted policy requires a leader/tie/DEFER rule. It also requests **two records**, whereas T3 budgets **one checker call** under the current one-record-per-call contract. **D 320, 395–418.** |
| **§§3–4: root metadata** | The current scenario exposes publisher identity, explicitly **not oracle lineage**. If the new root map comes from generator truth, it changes the information assumption. EIv2 labels that treatment an idealized perfect-provenance ceiling. Keep it separate from provenance inferred from observable links or attribution. Assigning different root labels alone also does not establish statistically independent evidence. **D 156–157, 979, 1051–1053.** |
| **§§4, 7: model routes and qualification** | S3’s second hosted model exceeds the stated one-hosted-plus-local setup. Jev authentication/inference is untested; the qualified local models are 0.6B/1.7B, not 8B; the provider requires a qualified nonreasoning endpoint. A local competence receipt does not satisfy the existing hosted Q4/source-signature gate. These need prospective qualification changes, not silent substitution. **D 1008–1013, 1115–1121, 1162–1165.** |
| **§5: repeats** | Three draws require explicit `replicate_id` and model identifiers in assignment keys. Otherwise they collide with the preserved duplicate-assignment rule. Replicates must remain nested within dossier clusters. **D 1150, 1158, 1166.** |
| **§§5, 8: matching tests** | Replacing the existing content-invariance test with byte-length equality loses protection against unrelated prompt changes. Equal byte length also does not establish equal token counts. Preserve a structural difference whitelist and check token footprint separately for each backend. **D 444, 1138.** |
| **§§2, 8: new-case labels** | `ambiguous_tbc` cannot generally accept “DEFER or confirmed alternative”: under the current evaluator, DEFER is wrong whenever a feasible alternative exists. Also, the proposed automation-floor example combines **pilot + workload**; the quote contributes nothing to that calculation. Specify the intended dependency and acceptable set precisely. **D 58–79, 73–76.** |
| **§8: random-check test** | Independent episode draws may legitimately repeat. Test reproducibility and the declared sampling distribution, not mandatory differences between episodes. If drawing two records uniformly from the current 12 candidate×kind combinations, the probability of checking the target at least once is \(1-\binom82/\binom{12}2=19/33\), approximately **57.6%**. **D 406–411.** |

The proposal correctly keeps length bounds in post-response validation and preserves raw model choices alongside shadow actions. Those are **not** contradictions (D 1132, 1144).

**C. Three unnecessary complications**

1. **T6 and T9 duplicate one configuration. — P §§1, 4**  
   Six analysts, two checkers, and one chair already constitute nine agents. Changing whether checkers are counted does not create a composition treatment. Keep one configuration and report actor counts by role. The existing roster confirms this accounting (D 317–322).

2. **L does not need its own paid workflow when it is a shadow calculation. — P §§1, 4–5**  
   Apply the ledger offline to every eligible saved fact package and raw choice. Separate paid calls are justified only if the ledger changes information supplied to the model—which would be a different intervention. This matches existing separate-authorizer semantics (D 501–505).

3. **The first study does not need both transfer domains and a broad mechanism sweep. — P §§2–5, 8**  
   Start with one procurement configuration, one fixed partial-exposure level, and one controlled page claim, plus positive/negative controls. Defer temporal syndication, MCP selection, model-complexity ladders, and additional team sizes. MCP transfer requires a substantive new outcome mapping; its existing design distinguishes recommendation, connection request, approval, and completed invocation (D 1062–1070).

**D. Two additions**

1. **Add a single primary estimand and a complete inference specification. — P §§1, 5, 7**

   The headline asks whether a team is more susceptible than a generalist, but the table assigns “primary endpoints” to four different projects. Register the architecture-by-world contrast explicitly:

   \[
   \Delta=\operatorname{mean}_i\left[
   (H_{T,C,i}-H_{T,N,i})-(H_{G,C,i}-H_{G,N,i})
   \right],
   \]

   where \(H\) means a purchase outside the acceptable set, \(C\) is controlled misleading content, and \(N\) is its control. Decide whether this broader outcome or the existing **target-specific** metric is primary; they are not interchangeable (D 549–555).

   Specify dossier clustering, replicate handling, failure bounds, the uncertainty procedure, and a practically meaningful effect threshold. Existing missing-data identification bounds are **not sampling confidence intervals** (D 523–535). Three repetitions cannot substantiate a tight equivalence claim: even under independent Bernoulli sampling, zero events in three trials leaves a one-sided 95% upper bound of approximately **63%**. Treat repetitions as a variability diagnostic.

2. **Add a truthful, recommendation-matched page control. — P §§2, 5**

   The new neutral page removes the prior warning confound, but it also removes all claims about the promoted supplier. A misleading-page versus neutral-page contrast therefore includes supplier mention, favorable framing, and factual alteration. That is valid for a total page effect, but insufficient to attribute the result to the false clause.

   Add a counterpart with the same supplier mention, endorsement, sponsorship marker, layout, and approximately matched footprint, changing only the decisive factual assertion. The existing `promotion` condition does not guarantee this match: the current version adds a sponsorship prefix to qualified recommendation text (D 180–185). This control makes the proposed single-claim worlds interpretable.

**E. Overall verdict**

**Ship with fixes, as a narrowly scoped pilot.** Preserve the summary-only chair, explicit purchase semantics, failure denominators, and independently authored holdout, but defer the broad factorial study. The single most useful change is to freeze a **team/generalist × misleading/control comparison with the same document union and check evidence**, and designate its paired interaction as the primary estimand. That directly answers the user-facing question while separating baseline team weakness from additional susceptibility to controlled pages. Propagation and shadow authorization can then be analyzed as secondary mechanisms with appropriately limited claims.

**Files changed: none. This was a read-only review.**