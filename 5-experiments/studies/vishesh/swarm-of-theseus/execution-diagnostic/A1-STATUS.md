# Theseus A1: stopped on first HTTP429, no scientific result

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-theseus; source `dd09575d` ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4** — Withheld-policy acquisition remains untested after a provider failure. Basis: First request returnedHTTP429 with no model text/usage;203slots unstarted. This is no evidence of acquisition success/failure or cultural preservation. Prior R1 remains separate.
- **sample_size_summary:** Planned: six fixed acquisition roots,12learners and96test case/family pairs. Observed:1/204calls endedHTTP429,0valid responses,203unstarted;0executor decisions and no root outcomes. No culture test.
<!-- experiment-evidence:end -->

A1 actually launched under the owner-approved direct path.204assigned,1started/terminal provider failure,0valid model responses,203unstarted; no retry. Learning and execution accuracy are unobserved. [Postmortem](RESULTS-A1.md), [actual trace](results/A1/TRACE-REVIEW.md), [setup](A1-SETUP.md), [plan](A1-PLAN.md).

Source dd09575d050e54fd8e4202d05cf1cc4aaa38033c. Sixteen offline checks passed, source/public-plan/account/claim/credential/runtime gates passed before dispatch. Queue295 was fenced and closed; exclusivePR303 used existing sim-shadow, no provisioning. Worker exited and12evidence artifacts were uploaded/readback verified. Final claim release is in results/A1/closeout.json.

Prior estimatedUSD0.8122310437 plus unknown-charge reserveUSD0.010452 =USD0.8226830437 of originalUSD5. No budget reset. Provider category/Retry-After were not retained, so underlying429cause is unknown. Stop this attempt; no second A1 or culture run. Any future request needs resolved provider availability, safer diagnostics and separate scope admission. Operator prompts/transcripts are not published.
