# A2: completed; acquisition qualification failed

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-theseus; source `b5484ca0` ([registry](../../../../evidence-metadata.json), [rubric](../../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — On these fixed cases, acquisition failed while supplied true-policy execution passed; wrong learned policies explain all21 wrong actions. Basis: 6/12 qualified policies; learned67/88 observed, ceiling96/96; all196 traces audited with zero disagreements. Synthetic fixed roots, single model route; no turnover or culture evidence.
- **sample_size_summary:** Six fixed synthetic roots;12 nested learners,184 observed of192 assigned paired actions;196 total terminal calls of204 assigned. Eight dependent actions unstarted after invalid mapping. Not196 independent samples.
<!-- experiment-evidence:end -->

A2 ran via the owner-approved OpenRouter route. 196 of 204 assigned calls completed, with zero provider errors/retries; eight dependent calls remained unstarted after an invalid learned mapping. Six of twelve policies qualified. Learned-policy actions: 67/88 observed correct (67/96 assigned); true-policy ceiling:96/96. All21 wrong actions faithfully followed a wrong learned policy.

**FINISH / PARK.** Read [the post-mortem](RESULTS-A2.md). No A3 or turnover run is authorized by this closeout. New cost USD0.156627; cumulative estimated plus unresolved exposure USD0.9793100437 of originalUSD5. A1unknownUSD0.010452 retained. Direct-Anthropic recovery remains unestablished.

The worker exited; twelve uploaded artifacts passed hash readback. Exclusive machine claim released in [PR354](https://github.com/dmarzzz/swarm-labs-agentops/pull/354).
