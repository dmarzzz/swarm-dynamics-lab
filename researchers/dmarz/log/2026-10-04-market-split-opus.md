# 2026-10-04 dmarz/market-split-opus

- Started as a sub-agent of dmarz/fleet-monitor on halcyon to run an Opus replication of the Sonnet market-splitting pilot on fresh markets. Phase 1 scope: plan, configuration, offline checks, scripted rehearsal, pre-run review. No model inference call in Phase 1.
- Confirmed `claude-opus-5-5` with the provider's Models API (metadata call, no inference). It lists manual thinking (`enabled`) as unsupported and adaptive thinking, effort levels and structured outputs as supported. Prices read from the official pricing page: USD 4 input and USD 20 output per million tokens.
- Copied the Sonnet V5 source. `sim.py`, `prompt.txt`, `render.py`, `policy.py` and `analyze.py` are byte-identical. Changes are in `provider.py`, `coordinator.py`, `worker.py`, `probe.py`, `common.py` and `selftest.py` and are listed in the README table.
- Conflict noted: agentops `docs/RUN-QUEUE.md` says dmarz's runs are launched from orbital-one through the run queue, not from a laptop. The reviewer session instructed this run from halcyon and relays dmarz. Recorded as issue O3; the reviewer decides before any paid stage.
- Server changed by the reviewer from `sim-dmarz-5` (claimed by another dmarz session while I was preparing) to `sim-test-01`.
- Surprise: no market-split launcher script exists on agentops main or in the Codex worktrees; the Sonnet pilot was launched by hand. The new launcher follows the sybil launchers' pattern.
- Reviewer's API note applied before any call: output ceiling raised from the pilot's 3,072 to 8,192 tokens (thinking is billed as output and counts against it), request timeout 180 s, refusal as its own failure category, no fallback parameter. Recorded as known differences between the two cohorts.
- Claimed `sim-test-01` (claim `dmarz-market-split-opus`), deployed commit 8c27b690, 18/18 offline tests on the server, scripted S0 `s0-fleet-001`: 6/6 bundles, 12/12 valid scripted episodes, 42 artifacts verified, zero model calls.
- Cost estimate from the pilot's measured tokens per call and official Opus prices: about USD 25 central (I0 0.12, Q0 0.69, S1 24.48); USD 42 if Opus produces twice the pilot's output; above USD 45 beyond about 2,100 output tokens per S1 call. Thinking volume is unmeasured until I0 and Q0.
- Not mine, left alone: `experiment_evidence.py --check` fails on main for another study's README block (sybil-scale-xl) and an unregistered sybil-specialists-opus experiment.yaml.
- Next: wait for the reviewer's go. Then I0, Q0, projection check, S1.
