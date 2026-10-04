# Pre-run assessment: chain s0-001 → p0-001 → q0-001 (fleet S0, probe, Q0)

- Experiment / owner / stage: sybil-newcomer-opus / dmarz / fleet S0 (scripted) then one-call Opus probe then Q0, chained on sim-dmarz-13 under exclusive claim `dmarz-sybil-newcomer-opus`.
- Parent: [s0-local-001-post](s0-local-001-post.md). Review: owner waiver (SETUP.md G0), not an independent review.
- Status: ready.

## Design and assessment

S0: 198 scripted observations on engineering worlds 6900–6901 through the hub path, checking the exact public revision, uploads and frames. Probe p0-001: one Opus call on an engineering-world pilot packet (not a Q0 or S1 packet), counted in the study ledger; passes only if the call returns `end_turn`, the returned model id is `claude-opus-5-5`, and the text block parses and validates. Its purpose is to catch interface errors (HTTP 400 from rejected parameters, thinking-block handling, output cap) before a batch; it is not a capability measurement. Q0: the parent's 36 clean packets with unchanged thresholds (per shape ≥95% field accuracy, ≥90% exact packets, 100% abstention on absent fields, all calls valid). Each step runs only if the previous one exited cleanly; the chain stops itself on the first failure and nothing later is dispatched.

## Changes and unresolved issues

| Issue / prior evidence | Change | Expected effect | Acceptance check |
|---|---|---|---|
| Opus 5.5 rejects temperature and disabled thinking (compositional q0-006: 24× HTTP 400) | request omits temperature and thinking; effort low | calls accepted | probe valid |
| Thinking tokens count as output | max_tokens 4,000; answer ≤2,000 chars on text block | no truncation | no `output_cap` failures |
| Model change can alter abstention | none (measured by Q0) | — | Q0 abstention 100% |

## Frozen execution plan

Pinned public revision and source hash recorded in DEPLOYMENT.md. Two concurrent requests in Q0, 180 s timeout, no retries; reservations from max_tokens 4,000 (worst case about USD 0.18 per call). Study caps 2,050 calls / USD 400 reservation. Credentials as environment aliases only. On failure: preserve all records, post-mortem, diagnose on development packets; never relabel or lower thresholds.

## Visualization mapping

Inherited mapping v1: S0 eight-frame replay, Q0 nine-frame completion-prefix GIF, live progress and final PNGs, bound to each run ID in DEPLOYMENT.md. The probe's JSON record is its receipt.
