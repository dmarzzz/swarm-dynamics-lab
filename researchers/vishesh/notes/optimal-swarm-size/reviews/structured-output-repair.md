# Output-contract investigation and prospective repair

2026-10-04 UTC. Written before implementation. Owner requested documentation, investigation and fixes after Q-A2. This amendment changes the instrument; it does not authorize replaying or rescoring historical outcomes and does not claim live qualification.

## TLDR

Replace prompt-only JSON formatting with native Anthropic JSON Schema output constraints for planning, item work and integration. Test the request contract, strict validation and failure paths offline; require a fresh public-plan/source/budget/allocation preflight and bounded live qualification before any scientific escalation. Same task semantics and evaluator; no fence stripping, retries, model changes or new funds.

## Question and prediction

Q-A2's four saved format events establish fenced, unparseable planning responses despite explicit no-fences wording. All failures preceded work. We do not have the rejected response bodies and cannot prove their inner content was semantically correct; Q-A1 has weaker diagnostics. Code inspection shows native_payload omitted output_config.format entirely: the API was asked for unconstrained text while the engine required strict JSON. Stronger prose left that interface mismatch intact. Predict a schema-constrained request removes this ordinary formatting failure mode, while refusals, truncation, transport faults and semantic mistakes still fail validation.

## Setup

Authoritative API reference checked 2026-10-04: https://platform.claude.com/docs/en/build-with-claude/structured-outputs . Use output_config.format with type=json_schema and a closed object schema. Keep the pinned native model and existing rate/budget/claim checks. Public task identifiers define schemas; hidden evaluator truth never enters them. Schemas constrain structure, not correct numeric answers, valid source semantics or dependency correctness.

## Protocol

Publish this amendment before implementation. Build explicit phase schemas: planning/repair requires all dependency-map item keys with string-array parents; evidence work requires artifact {value: integer, source_ids: string[]}; repository work requires artifact string; integration requires the existing answers/files maps and exact public keys. Transport diagnostic has {ok: boolean}. All objects disallow extra fields. Local strict_json, plan validation and evaluator remain authoritative; no generic text fallback when schema mode is enabled. Retain compatibility only for explicitly identified historic prompt-only configurations.

Validate schema mode and phase before budget reservation, include schema bytes in the payload size cap, and preserve all existing finish-reason/usage/route checks. Record non-secret schema hashes with reservation events. Distinguish refusal from truncated/incomplete response without logging provider body/error text. Improve plan-repair feedback using fixed safe parse-versus-plan error labels. No additional model retries.

Regression checks cover both task families and all phases, JSON-string escaping, missing/extra keys, invalid types, original fenced/duplicate/nonfinite input rejection, request wiring and fail-closed schema configuration. Preserve evaluator hashes and old results. Record actual validation scope; offline scripted calls never become model results. The next live attempt must use a new identity, the original canonical Q1 ledger ($0.328990 exposure before this repair), and a fresh claim/public receipt. Released allocation is not reusable without a new claim. Q-B/core remain closed.

## Metrics

Offline schema/request/engine checks and code hashes; later qualification must separately measure response validity, semantic success, latency (including schema compilation), usage, cost, refusal/truncation and public delivery. No paid requests in this engineering repair. Do not call the hosted path verified until a prospective bounded live attempt passes.

## Visualization mapping

Existing replay remains event-driven. Reservation events gain contract/schema identity; response-format events retain raw-JSON/fence status. All prior failed timelines remain unchanged. No fabricated successful task animation.
