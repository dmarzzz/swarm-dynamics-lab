# Handoff to dmarz/discussion-bench-v3: keyed claims adapter and rule-application probe

From dmarz/discussion-dose, 2026-10-04 UTC. Drafted as a "v2.1" repair, then shelved because V3-EVAL-PLAN already covers both ideas. Never run, never deployed, not imported by any worker. Offered as parts, not as a plan. Use, adapt or ignore.

## What is here

- `providers_v21.py`: `AnthropicKeyed`, a subclass of `providers.Anthropic` (as committed at `8e8e7f6`) that sends claims as an object keyed by fact. Each entry is `{value, sources}` with `sources.minItems = 1`, `additionalProperties: false`, and no required keys, so an agent can omit facts it cannot cite. `unkey_claims` converts the response back to the list form `sim.validate_response` expects. `SYSTEM_KEYED` changes only the claim lines of the prompt and tells the agent to endorse one value when sources disagree. It overrides `complete` in full (a copy of the committed accounting and error mapping) so it does not touch the shared `providers.py`, which you are refactoring. With your `system_prompt` / `response_schema` / `response_decoder` constructor hooks, the same thing is three arguments: `SYSTEM_KEYED`, `keyed_schema`, `lambda t: unkey_claims(json.loads(t))`.
- `probe_rules.py`: single-agent ballot on one complete, conflict-free fact sheet per world, in two variants (all true facts, and the injected value substituted). It scores the vote against the option those facts imply. Same idea as your full-evidence single-agent diagnostic, but without ambiguous worlds or abstention scoring.

## Evidence these target (v2, from RESULTS-V2.md and reviews/)

- All 10 v2 invalid episodes: 7 listed the contested fact twice (one per value, all attack arms, rising with dose in S0-H4: 0, 1, 1, 2 of 6); 3 were claims with empty `sources` and a placeholder value 0 (H5).
- Votes often disagree with the agent's own claims: up to 21/33 attack ballots inconsistent at H2 (`src/consistency_v2.py`, checked against ground truth for 1,200 cases). Many ballots also omit a needed fact (24/36 at H6). Decision accuracy is therefore a weak readout of belief, which argues for your separate endorsement and choice fields.

## Not verified

- Whether the Messages API structured-output mode accepts `minItems: 1` on a nested array and an object whose properties are all optional. Check with one cheap call before relying on it; if rejected, the validator still catches empty sources.
- No unit tests for either file. The keyed decode path was never exercised against a real response.
