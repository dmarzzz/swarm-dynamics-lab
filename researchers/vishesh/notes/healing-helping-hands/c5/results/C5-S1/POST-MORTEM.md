# C5 main-stage post-mortem: reliable execution, unsafe selective routing

**FINISH / PARK.** The approved automatic chain completed once:60 qualification cases followed by432 main cases. No additional approval was requested between stages. Main execution and evidence reconstruction passed; the routing rule failed its prespecified safety criterion. This is a valid adverse result for the frozen Qwen3:0.6B prompt/schema/runtime and Jev1.13 configuration, not a transport failure or a reason to retry for a favorable result.

## Outcomes against the preregistered criteria

| Policy | Correct /432 | Error | Derived Jev consultations |
|---|---:|---:|---:|
| Qwen A |182|57.87%|0|
| Always Jev |432|0%|432|
| Agreement routing |198|54.17%|23|
| Same-count per-family random routing |193|55.32%|23|

Qwen B was187/432 correct. The cascade avoided409/432 (94.68%) Jev consultations in a counterfactual deployment, exceeding the25% savings criterion. It beat the declared matched-random realization by5 decisions (1.157pp), and the analytic uniform-random expectation by0.849pp. Leave-one-family-out matched differences range from−1.515pp to−0.505pp; these are finite sensitivity checks, not population confidence intervals. The safety contrast is **+54.17pp error versus always-Jev**, far beyond the2pp limit. The conjunction of usefulness criteria therefore fails. A small relative routing advantage does not rescue unacceptable absolute error.

Only16/250 Qwen-A errors were referred (6.4% error-detection recall). Of409 agreements accepted without Jev,234 were wrong (57.21%). Seven of23 referrals involved an already-correct A answer. Every authored family retains substantial cascade error, from27.78% to72.22%. No missing outcomes, denominator exclusions or tuned thresholds explain this result.

## Native trace review and cause limits

All1296 main requests, hashes, terminal visible labels and scores were reconstructed. A separate saved-report reference check recomputed all432 labels, including reversed error-rate arithmetic, with zero mismatches. The assessor inspected69 instances covering every observed family × truth × A/B/Jev response pattern, including207 raw visible answers. This covers all observed patterns, not a manual reading of every instance. S0 separately received exhaustive inspection of every qualification miss.

Both Qwen variants emitted **zero SUPPORT labels** across144 SUPPORT cases; A returned132 REFUTE and12 UNCERTAIN. Absent measurements were also often treated as refutation. Examples include80/100 correct versus71/100 baseline classified REFUTE by both variants, and explicit unmeasured accuracy classified REFUTE. Distractor and superseded-evidence cases show the same systematic issue, with occasional disagreements that rescue few errors. The first observable divergence is the raw classification while relevant evidence is present. All864 Qwen calls ended with normal `stop`, not truncation; all432 Jev responses served typesafe/jev-1.13-20260917. Inputs contained opaque identifiers and the declared claim/report only; Jev did not receive Qwen answers.

This verifies correlated error for this configuration. It does not establish whether the underlying model, prompt, constrained JSON decoding or their interaction caused the collapsed label behavior. No hidden reasoning was collected or inferred. A future configuration diagnostic would require a concrete new plan; changing models, prompts, output schemas or thresholds after inspecting this main tape would create a new cohort.

## PI assessment of design, scenarios and inference

The design isolates an option-order disagreement rule, includes the strongest semantic reference and equal-count random controls, retains an analytic random expectation, and preregisters acceptance and stopping. Opaque identifiers remove the verified C4 defect. Actual wire traces and arithmetic are available for replay. These are improvements over the invalid C4 qualification and the earlier transport failures.

The cases provide controlled comparisons, negation, uncertainty, irrelevant metrics, competing targets and superseded evidence. They are answerable, balanced and labels were checked. However, there are only12 authored semantic families with36 nested numeric/surface instances each. Jev has a ceiling and this Qwen configuration has a SUPPORT-label floor. This supports rejecting the present rule on these cases; it cannot estimate transfer to real documents, a broad model ranking, calibrated confidence, or200-agent cooperation. There are no432 independently sampled language domains and no powered noninferiority claim. Same-author audits are disclosed; independent research review was waived, not passed.

## Resources, reliability and process

S1 completed1296/1296 calls (864 Qwen,432 Jev), all432 assigned cases, zero transport/schema failures and no paid retries. S0 completed180 calls. Main API cost wasUSD0.008850996; combined C5 costUSD0.009981426. C4+C5 repair-cycle spendUSD0.011108076 remained belowUSD0.03. Reconciliation preserved all2239 historical entries; original ledger now has2731 reservations, settledUSD0.051998898 plusUSD0.001344 historical unresolved exposure, leavingUSD0.046657102 under the originalUSD0.10 API ceiling. Remaining dollars do not authorize another stage or reset the exhausted approved request envelope.

Recorded main component time: Qwen1147.90 seconds and Jev99.58 seconds. The counterfactual cascade sums to1153.04 observed call-seconds versus99.58 for always-Jev, with derived Jev chargesUSD0.000468846. These serial observations include order/cache effects and are not randomized production-latency estimates. Local Qwen compute has no assigned dollar price here. Thus API-charge savings are not total-cost or speed savings. No new paid VM was created; the original exclusive approved-account allocation is reconciled separately at closeout.

Read-only admission caught a stale C4 plan suffix and a copied model-digest typo before any C5 call. Corrected source179b1cca passed37native offline checks; dispatcher fixes passed four tests and CI. The frozen plan contents and approved scope were unchanged. Public UI review additionally found protocol caching by experiment ID; privatePR368 fixes it with an ID+URL cache key and late-response regression coverage. It is merged for Dmarz/CD deployment; this session did not deploy through another Cloudflare account. Original rendering called a family-grouped reveal chronological replay; reviewed replay wording corrects that without changing data.

## Decision and next action

Complete the evidence archive, public report and verified resource release. Retain always-Jev as the successful simple reference on these fixtures; park this agreement-only rule. Do not relaunch, enlarge the cohort or tune the held-out cases. If revisited, first define a separate development-only diagnosis of Qwen's missing SUPPORT outputs and a new representative task population; any material successor needs its own concrete decision. Current results do not justify immediate external deployment or another200-agent demonstration.
