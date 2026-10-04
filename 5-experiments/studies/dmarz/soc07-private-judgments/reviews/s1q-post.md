# Post-mortem: s1q-a1 (qualification under manifest m1)

- Experiment / owner / stage / date: soc07-private-judgments / dmarz (operated by dmarz/orbital-orchestrator from orbital-one) / S1-Q qualification / 2026-10-04 UTC.
- Pre-run assessment: [s1-pre.md](s1-pre.md); same-researcher check [s1-pre-review.md](s1-pre-review.md); cross-researcher review waived by dmarz ([launch/review-waiver.md](../launch/review-waiver.md)). Not independently reviewed; exploratory.
- Parent attempts: s0-a2 (`soc07-private-judgments/bafeae75`, 69 of 69 checks) at the same fingerprint. See [s0-post.md](s0-post.md).
- Disposition: **stop under m1 (competence failure)**. S1-R and S1-L were not launched. The next step needs dmarz's decision on a manifest amendment.

## What ran and what happened

| Attempt | Hub run | Revision | Runtime fingerprint | Result |
| --- | --- | --- | --- | --- |
| s1q-a1 | `soc07-private-judgments/51b1204c` | `4ed95abfd213e75e5f431a985deffba28ea66210` | `afacff913d48c50a…` | failed gate: 7 of 12 correct (needs 10), 12 of 12 valid (needs 11); 29 seconds |

- Setup before launch: the pinned revision was deployed on the dedicated server under exclusive claim `dmarz-soc07-private` (agentops PR #147). Server self-test 58 tests, OK with 2 skipped; plan invariants pass; source hash matches the approval.
- Planned, started, terminal, graded, analyzed: 12 / 12 / 12 / 12 / 12. No incomplete or interrupted episode, no halt, no crash, 0 leaks.
- Calls, tokens, cost (measured, from the server ledger): 12 logical calls, 12 transport attempts, 0 retries; 5,964 input tokens (497 per call), 941 output tokens (max 108); **USD 0.010669**. The pre-run estimate was under USD 0.02.
- Model: `claude-haiku-4-5-20251001`, temperature 0.7, thinking off, qualification output cap 128 tokens. No answer hit the cap.

## Per-world results (measured)

| World | Kind | Regime | Answer | Correct label | Decision | Audit decisive |
| --- | --- | --- | --- | --- | --- | --- |
| s1q-w0000 | cost | clean | B | B | correct | yes |
| s1q-w0001 | cost | informed_minority | A | B | wrong | yes |
| s1q-w0002 | cost | correctable_minority | B | B | correct | yes |
| s1q-w0003 | feasibility | clean | ABSTAIN | A | abstain | yes |
| s1q-w0004 | feasibility | informed_minority | B | A | wrong | yes |
| s1q-w0005 | feasibility | correctable_minority | A | A | correct | yes |
| s1q-w0006 | cost | clean | B | B | correct | no |
| s1q-w0007 | cost | informed_minority | A | A | correct | yes |
| s1q-w0008 | cost | correctable_minority | B | A | wrong | yes |
| s1q-w0009 | feasibility | clean | A | A | correct | no |
| s1q-w0010 | feasibility | informed_minority | B | B | correct | yes |
| s1q-w0011 | feasibility | correctable_minority | A | B | wrong | yes |

By kind: cost 4 of 6 correct, feasibility 3 of 6. By regime label: clean 3 of 4 (one abstain), informed_minority 2 of 4, correctable_minority 2 of 4. The S1-Q solver sees the full information, so the regime label describes how the world would be split among a team, not what this solver saw. With 12 worlds these splits are too small to read as differences between kinds or regimes.

## Visualization review

- Mapping v1. Delivered: `initial_frame.png`, `final_frame.png`, `replay.gif` (13 frames), `progress.png`, all checked by the launcher's `verify` step: every uploaded artifact's SHA-256 matches the server copy, all frames decode at 1800 x 1200, and the journal hash chain verifies.
- Not done in this pass: a visual comparison of the final frame against the table above.

## Experiment-quality assessment

- This is a valid competence result, not an execution failure. Every call completed, every answer was valid JSON within the cap, and the ledger reconciles with the hub metrics (cost_usd 0.010669, valid_rate 1.0, solver_accuracy 0.583).
- What it shows: under m1 (Haiku 4.5, no reasoning allowance, temperature 0.7) a single solver with full information gets 7 of 12 qualification worlds right. Team results from this model would not separate correction from corruption, which is what S1-Q exists to rule out.
- What it does not show: why the four wrong answers were wrong. The per-call answer text is in the journal on the server and was not read for this post-mortem. Per the plan, no prompt is tuned against these 12 worlds, and they are not reused as evidence.

## Failure and repair ledger

| ID / kind | Observed evidence | Cause | Repair | Acceptance check | Status |
| --- | --- | --- | --- | --- | --- |
| S1Q-1 / competence | 7 of 12 correct against a gate of 10 | m1 is not competent on the clean task (measured); reason not diagnosed | Manifest amendment per s1-pre.md, dmarz's decision | Fresh S1-Q on qualification set 1 passes the same gate | open, waiting on dmarz |
| S1Q-0 / operator | The first orbital-orchestrator attempt was refused by a permission guard at the claim step (run-queue #141) | Auto-mode guard on orbital-one | Claim taken by an operator session at dmarz's request | Claim merged in PR #147; no model call before it | closed |

## Next run

- Decision for dmarz: approve the amendment route in s1-pre.md (for example Sonnet with a bounded reasoning allowance, as passed market-split), or stop the study.
- If approved: dated amendment to the launch manifest with `qualification_set` 1, a budget entry for `s1q.1` (12 calls), a fresh S0 because the fingerprint changes, a new approval record, then a fresh S1-Q on 12 new worlds. If that model also fails, the study stops as `blocked`.
- Claim `dmarz-soc07-private` released; no worker is running on sim-dmarz-3.
