# Pre-run assessment: v3o-a1 (probe, Q0, S1 chain)

- Experiment / owner / operator: discussion-v3-opus / dmarz / dmarz/v3-q0-opus.
- Parents: `v3-q0-a1` (Haiku Q0, failed competence), `v3-d1-a1` (Haiku and Sonnet D1, failed), `d1o-a1`
  (Opus D1, fresh gate 12/12, 72/72 valid, USD 1.495). Previous post-mortems read: `../../reviews/v3-q0-a1-post.md`,
  `../../reviews/v3-d1-a1-post.md`, the D1-Opus post-mortem.
- Review: cross-researcher review waived by the owner ([OWNER-AUTHORIZATION.md](../OWNER-AUTHORIZATION.md)); none performed.

## Design and assessment

Same shape as `v3-q0-a1`: 3 agents, 3 extra rounds, 4 arms (independent, reports, private, board), clean and
attacked exposures, 12 full-evidence diagnostics and 36 memory fixtures. Q0: 6 fresh worlds, 96 cases, 636 calls.
S1 (pass case only): 24 fresh worlds, 384 cases, 2,436 calls. Worlds are the independent units; arms within a
world reuse the same acquisition and checkpoint, so arm contrasts are paired by world. The Q0 gate is the frozen
`model_qualified` rule (execution complete, 5/6 clean diagnostics, 5/6 clean reports-only votes, no missing
usage). S1 has no gate; it is exploratory. Truth stays evaluator-only; actor inputs are the unchanged v3 contexts.

Risks: (1) adaptive thinking at effort high makes swarm turns slower and longer than D1's single decisions;
estimated 6–15 s per call, so Q0 65–160 min and S1 4–10 h. The claim is taken for 14 h and extended if needed.
(2) Long thinking could hit the 16,000 ceiling; such calls fail closed as `provider_incomplete` and count as
invalid. (3) Refusal is possible but unlikely on fictional logistics tasks; counted separately.

## Changes and unresolved issues

Relative to `v3-q0-a1`: model (Haiku 4.5 to Opus 5.5) and request configuration (no temperature; adaptive
thinking; effort high; 16,000-token ceiling; visible 8,000-character cap; 600 s timeout) and fresh world ids.

Two operational changes, both binding inputs from the results analyst relayed by fleet-monitor before launch:
(1) **Clean-first dispatch.** Per world, clean acquisition, clean report snapshot, clean reports-only arm and clean
full-evidence diagnostic run first (66 calls); an early gate (5/6 and 5/6, zero failures so far) stops Q0 if it
fails, leaving the other 570 assignments undispatched by design. Rationale: in D1-Opus all 8 saved-report
abstentions were incomplete-claim ballots (no contradiction of own claims, no wrong vote), so the reports-only gate
turns on whether Opus-written reports carry every needed value; this decides it in about the first 66 calls.
Request contents, records and scoring are unchanged; the order is deterministic and reproduced by replay.
(2) **Transport retry (SOC-07 rule).** At most two retries per logical call, only for HTTP 429 and 529 where the
provider did not run the model, only while the 600 s request window lasts; every attempt is reserved in the ledger
and counted against an attempt cap (planned calls + max(10, 10%)). Model answers are never retried. Tested offline
(`test_transport_retry_rules`, `test_clean_first_order`, early-stop chain test).
Instrument source otherwise byte-identical (bench_v3, tasks.py, providers.py at this commit, including the F1/F2
fixes). Not pooled with Haiku.

## Frozen execution plan

Source pinned to the commit that adds this file; the launch record `../launches/v3o-a1.json` carries every source
hash and is validated in-process before any call. Hard caps: probe 1 call (USD 1 ceiling), Q0 636 calls
(USD 400 reservation ceiling), S1 2,436 calls (USD 1,500 reservation ceiling); actual spend expected about
USD 13 and USD 50. No restarts or fallbacks; transport retries only as above; the chain stops at the first failed gate, including the
Q0 clean-first early gate. Credentials enter
by SOPS -> ssh stdin -> process environment only. Every stage reports `cost_usd` to the hub.

## Visualization mapping

`v3-deliberation-v1` (as used for `v3-q0-a1`): live `frame.json` every 5 s during the run (agents, votes, claims,
false-endorsement trajectory, memory admission), final frame, `replay.json` of every checkpoint/merge/terminal
frame, and `replay.html` from the journal. Missing or failed calls appear as invalid ballots, never interpolated.
Bound to `discussion-v3-opus/v3o-a1-q0` and `discussion-v3-opus/v3o-a1-s1`. Checked against `summary.json` at
close-out.

## Failure-case plan

If Q0 fails the gate, S1 does not start; the post-mortem classifies failures by kind (invalid/refusal/truncation,
abstention despite claims, infeasible choice) and the next attempt follows the README's "If Q0 fails" section on
new worlds. If the probe fails, nothing else runs; fix the adapter offline and probe again as a new attempt.
