# Post-mortem: i0-003

- Parent q0-004; [pre-run assessment](i0-003-pre.md); I0, 2026-10-04 UTC, dmarz.
- Source c4c69163575d7711b0f9fa974fadcaf4c9b733f0, pinned Sonnet 5, disabled thinking/high effort/default sampling.
- Disposition: repair-and-rerun diagnostic. Full Q0/P1 remain blocked.

## What ran and what happened

Sixteen assigned, started, terminal, graded and analyzed one-decision requests: eight original packets and their eight clarified counterparts. Original: 6/8 valid, 0/8 advancing, two provider refusals. Clarified: 8/8 valid, 3/8 advancing, no refusal in this small sample. The clarified condition fails the predeclared 8/8 advancing screen. These are deliberately selected reused states, not independent full episodes.

Clarification enabled both D1 packaging decisions and the benign D1 reader. It did not move any of the four D2 approval decisions beyond inspect, and the previously refused D1 risk reader also chose inspect. The original two refusals reproduced. This supports further interface investigation but does not establish a complete repair or a stable refusal rate. No world action or treatment comparison was executed.

Sixteen calls, all with usage: 32,082 input and 211 output tokens; $0.066274 actual, $0.360376 retained reservations, 24.90 seconds. Study totals: 1,626 calls, $5.406371 actual, $28.393474 reserved. Source packet reconstruction and request readback establish that only the declared static contract differs within each pair. No expected action, previous probe output or evaluator state entered a request.

## Visualization and evidence review

All 23 hashed files reconcile. Sixteen unique case/condition pairs match the manifest; expected-action scoring was recomputed for every response. Exact credential-free request bodies were compared to saved parent observations. The 1600×900 final frame shows the four D2 rows gray in both columns, two D1 packaging improvements blue, two original refusal cells red, and only the benign clarified reader blue. Its labels agree with all sixteen responses. The 17-frame GIF decodes completely and retains actual shuffled completion order. No missing responses were interpolated.

The diagnostic hub run is done with 24 artifacts, an empty reporting spool and an exited worker. Public-plan receipt binds the immutable rendered GitHub plan, source/configuration hashes and public experiment registration before run_start. Original qualification failures remain untouched.

## Experiment quality and issue ledger

| Issue | Evidence / cause confidence | Next check / status |
|---|---|---|
| Incomplete execution/history contract | Three selected D1 decisions improve; approval decisions do not | Candidate partly useful, not qualified |
| Model/interface interaction | Sonnet repeats inspect even when initial state and complete history are explicit | Compare the same fixed diagnostic with the earlier valid Haiku baseline |
| Provider suitability | Original refusals reproduce; clarified responses valid here | No claim that refusals are solved; fresh qualification still required |
| Runtime registration | Exact public plan and fail-closed source/content check now wired into dispatch | Admission regression passes; historical attempts not relabeled |

## Next run

i0-004 retains all eight observations, condition order, prompt, task policies, menus and scoring but uses the previous pinned Haiku 4.5 configuration. That baseline earlier completed 20/24 tasks with 24/24 validity, including 11/12 approval tasks, making it a justified comparison to Sonnet's repeated approval stalls. This changes model and decoding settings together; do not infer a pure model effect. All sixteen calls are explicit new diagnostic observations, with no retries or overwritten outcomes. Require 8/8 valid and advancing clarified decisions before adopting this combination for fresh disjoint Q0. If it fails, inspect the remaining response behavior before another amendment; never lower the gate.
