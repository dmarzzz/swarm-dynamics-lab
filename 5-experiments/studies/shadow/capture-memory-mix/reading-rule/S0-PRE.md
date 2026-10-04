# S0 pre-run assessment, 2026-10-04

Assessor shadow/sol-cm2, same-author. Disposition **diagnostic-only**. Owner scope: frozen histories, presentation order and lossless summary diagnostic, OpenRouter only, USD 12 total. No formal hypothesis or independent review pass claimed.

Read prior closeout CORRECTIONS.md: reporting defects and last-valid selection are fixed, but first-observed MP3 validity was 54/180. No old pilot calls will be rerun. This new instrument saves start records before dispatch, never retries, and uses histories rather than calls as scientific units.

Offline validation: `python3 reading-rule/test_reading_rule.py`, 8 tests pass. All 156 requests reconstruct identical paired histories and preserve counts/last metadata. Known-answer and negative scoring fixtures pass. Duplicate start, call-cap, dollar-cap, deadline, source-model drift and nonimmutable plan checks reject. Actual run lock and request-level source checks are wired into the only paid entry point. Fixed endpoint is OpenRouter; no pool path exists in this source.

Frozen input: input.json SHA-256 `c9d24c92ff32abbdd3c961bb4446f07edf60ba9aff330417b5436b4cc71f2639`. 12 S0 assignments, 144 S1 assignments; S1 remains blocked until S0 qualifies. Max request bytes checked under 20,000, routing ceilings 1/2 USD per million input/output, 8 output tokens, each call reserves USD 0.05 permanently; total 156-call exposure USD 7.80. Historical pilot costs are not erased or included as new observations.

Run admission will verify committed source and exact public immutable plan bytes, register the hub study, record runtime and source hashes, then dispatch S0 only. Missing registration or public fetch blocks. Current machine is owner-authorized local execution, sequential HTTP, no new infra or credential transfer. Finish deadline 21:30Z, pre-dispatch stop 21:25Z.

S0 acceptance: 12/12 valid, allowed token mass >=0.8, >=11/12 unanimous-name choices. Any failure ends this version, with raw outcome retention and no reinterpretation as a scientific null. Static paired-history plot is the planned visualization; no collective temporal replay is applicable.
