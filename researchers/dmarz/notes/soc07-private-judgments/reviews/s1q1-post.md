# Post-mortem: s0-a3 and s1q.1-a1 (manifest m2, Sonnet 4.6)

- Experiment / owner / stages / date: soc07-private-judgments / dmarz (operated by dmarz/orbital-orchestrator from orbital-one) / S0 scripted and S1-Q qualification set 1 / 2026-10-04 UTC.
- Pre-run assessment: [s1-pre.md](s1-pre.md), section "Manifest m2". Approval: `launch/s1-approval.json` at swarm-lab `6531af3e` (dmarz's go; not a fleet-monitor review). Parent: [s1q-post.md](s1q-post.md) (m1, 7 of 12).
- Host and claim: sim-dmarz-8, exclusive claim `dmarz-soc07-private` (agentops PR 168). The live budget ledger is on sim-dmarz-8; the sim-dmarz-3 copy (SHA-256 471a7635…) is retired and was not written after the copy.
- Disposition: **S1-Q.1 failed competence (9 of 12, gate 10). Stop under m2.** S1-R and S1-L were not launched. dmarz's instruction relayed at ~07:36 UTC ("use opus for everything going forward please") arrived after S1-Q.1 had already dispatched; the next manifest is Opus.

## What ran and what happened

| Attempt | Hub run | Revision | Fingerprint | Result |
| --- | --- | --- | --- | --- |
| s0-a3 | `soc07-private-judgments/eed24e49` | `45f9c48d07b9be865c8e1e1ba5a1f341706ba1bc` | `475140d4…` | done; 69 of 69 checks; 0 model calls |
| s1q.1-a1 | `soc07-private-judgments/5f681258` | `6531af3edab4b6e36a10645d7cc25963b4973ca7` | `475140d4…` | failed gate: 9 of 12 correct (needs 10), 12 of 12 valid |

- S1-Q.1: 12 planned, dispatched, valid; 0 failures, 0 retries, no halt or crash. 5,976 input tokens (max 498 per call), 941 output tokens; **USD 0.032043** (measured, ledger). Study ledger after: 24 calls, USD 0.042712 committed, inside the USD 40 cap.
- Server self-test before each deploy: 58 run, OK with 2 skipped.

## Per-world results (measured)

| World | Kind | Regime label | Answer | Correct | Decision |
| --- | --- | --- | --- | --- | --- |
| s1q.1-w0000 | cost | clean | B | A | wrong |
| s1q.1-w0001 | cost | informed_minority | B | A | wrong |
| s1q.1-w0002 | cost | correctable_minority | A | A | correct |
| s1q.1-w0003 | feasibility | clean | B | B | correct |
| s1q.1-w0004 | feasibility | informed_minority | B | B | correct |
| s1q.1-w0005 | feasibility | correctable_minority | B | B | correct |
| s1q.1-w0006 | cost | clean | B | B | correct |
| s1q.1-w0007 | cost | informed_minority | A | A | correct |
| s1q.1-w0008 | cost | correctable_minority | A | B | wrong |
| s1q.1-w0009 | feasibility | clean | A | A | correct |
| s1q.1-w0010 | feasibility | informed_minority | B | B | correct |
| s1q.1-w0011 | feasibility | correctable_minority | A | A | correct |

All three misses are cost worlds (cost 3 of 6, feasibility 6 of 6). Under m1, Haiku missed in both kinds. With 12 worlds this split is suggestive only. The answer text was not read for this post-mortem; why the model chose these answers is not observed.

## Visualization review

- Both runs: `initial_frame.png`, `final_frame.png` and `replay.gif` at 1800 x 1200; every uploaded artifact's SHA-256 matches the copy on sim-dmarz-8 (S1-Q.1: 9 artifacts; S0: 5). The S1-Q.1 journal reads cleanly (38 records).
- The launcher's `verify` action now fails with `missing_local_artifact` because it walks every run of the study and the m1 runs' files are on sim-dmarz-3. The two m2 runs were checked directly with the same hash, frame and journal logic. A launcher fix (verify only runs whose files are on the selected host) is noted below.

## Experiment-quality assessment

- Valid competence result, not an execution failure: every call completed with valid structured output within its cap.
- Moving from Haiku (7 of 12) to Sonnet 4.6 (9 of 12) on fresh worlds did not reach the gate. Without a reasoning allowance, both models miss cost worlds where, per the m1 reviewer's reading, a later audit overrides an earlier estimate in a single short call.
- No prompt was tuned against either set of 12 worlds; neither set is reused as evidence.

## Failure and repair ledger

| ID / kind | Observed evidence | Cause | Repair | Acceptance check | Status |
| --- | --- | --- | --- | --- | --- |
| S1Q1-1 / competence | 9 of 12 against a gate of 10 | m2 not competent on the clean task (measured); reason not diagnosed | Manifest m3 on Claude Opus 5.5 with a reasoning allowance, qualification set 2, fresh S0, dmarz's approval | Fresh S1-Q.2 passes the unchanged gate | open |
| S1Q1-2 / operator | Setup at 72a36c93 was cut off when orbital-one ran out of memory (~06:07 UTC; unrelated crawler crash loop) | Host incident | Setup rerun at 45f9c48d after a record correction | Setup OK, S0 69/69 | closed |
| S1Q1-3 / record | `execution.json` said the m1 reviewer had gone offline | Operator error | Corrected at 45f9c48d before S0 | Reviewer field accurate | closed |
| S1Q1-4 / tooling | Launcher `verify` fails after the host move | Verify walks all runs | Manual check above; launcher change to follow | m2 runs verified | open |

## Next run

- Manifest m3: `claude-opus-5-5` (Models API confirmed 2026-10-04; it accepts only adaptive thinking and rejects temperature), USD 4 / 20 per million (official pricing page), qualification set 2, fresh S0, approval recorded from dmarz's instruction, then S1-Q.2 (12 calls). This needs an adapter change, because the current adapter sends temperature when no reasoning budget is set and sends the older thinking format otherwise.
- Before any S1-R or S1-L under m3, a cost estimate from S1-Q.2's measured tokens per call goes to dmarz.
