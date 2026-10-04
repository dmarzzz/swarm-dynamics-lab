# Reviewer check of the S1 pre-run assessment (dmarz/fleet-monitor)

Date: 2026-10-04 UTC. Reviewer: dmarz/fleet-monitor, an agent of the study's owner. This is the same-researcher check that dmarz chose in place of cross-researcher review ([launch/review-waiver.md](../launch/review-waiver.md)). It is not independent approval and the stages it covers stay exploratory.

**Verdict: go for S1-Q, S1-R and S1-L under launch manifest m1**, at runtime fingerprint `afacff913d48c50a8fb5b00efd8775454cfbc62dba841a8f6be919ea7144d9fe`, with the conditions below. S2 stays closed.

## What I read

At swarm-lab `61216b98`: `src/prompts.py`, `contexts.py`, `generate.py`, `protocol.py`, `score.py`, `parse.py`, `state.py`, `adapter.py`, `budget.py`, `coordinator.py`, `launch.py`, `study.py`, `worker.py`, the gate functions in `analyze.py`, `execution.json`, [s1-pre.md](s1-pre.md), `DEPLOYMENT.md`, the waiver, and the private launcher `scripts/run-soc07-private.py` at agentops `29eab77`. I did not read `selftest.py`, `s0.py`, `render.py`, `policy.py` or `journal.py` line by line.

## What I ran myself

On a clean checkout of `main`, standard library only, no model call:

- Regenerated every world of S1-Q (12), S1-R (24) and S1-L (24). The independent solver in `score.py` agrees with the generator's answer key for all 60, including which option the old records favour and whether the audit is decisive.
- Regimes are 4/4/4, 8/8/8 and 8/8/8. The displayed correct label is A in exactly half of the (world, repeat) presentations of every regime in every stage.
- Built the first-pass context of all five agents for every presentation (540 contexts). None contains the truth canary, the world id, a regime name or the word "correct". Agents whose own records imply the wrong option number 20, 80 and 80, which is what the two minority regimes are designed to produce.
- Planned call counts from `study.manifest`: 12, 672 (480 + 192) and 4,080 (2,880 + 1,200). They equal the declared caps.
- The fingerprint computed on `main` equals the one on the S0 hub run `soc07-private-judgments/bafeae75` (69 of 69 checks, 0 model calls), which I read from the hub.

I did not run the unit tests; I rely on the two S0 hub runs and the builder's report for those.

## Findings

1. **Truth separation is structural.** The context builder is given records, the display mapping and published snapshots, never the truth or the regime. The canary search before dispatch would catch only an injected canary; it is a tripwire, not the protection. Acceptable.
2. **Scoring.** Deterministic, through the per-repeat label mapping; team decision needs 3 of the 5 assigned agents on the same valid label; abstentions and missing votes never count; unfinished episodes stay in the denominator. No model judge.
3. **Phase barriers.** One shared first pass cloned into PRIVATE, PUBLIC, NEVER and VOTE; PREPARE separate; discussion published only after all calls of the phase return; public and private finals fork from the same frozen context. PUBLIC is the only arm that receives first choices, and only `choice` and `confidence`.
4. **Money.** Reservation before dispatch from request bytes plus the output cap, settled from reported usage, unknown outcomes keep their reservation; per-stage call caps and a USD 40 study cap in one locked ledger on the server. Units are consistent (micro-dollars).
5. **Credentials.** Decrypted on the operator's machine, sent over ssh standard input, placed only in the worker's environment. The launcher prints a sanitized error for paid steps.
6. **Launch gate.** `launch.check` refuses a paid stage without an approval record that names the stage and pins the fingerprint, the pre-run assessment and the waiver by hash; the worker checks again before building the provider adapter.
7. **Known weak points, none blocking.** The real provider exchange has never run, so a malformed-request rejection on the first S1-Q call would halt the stage. Arm order is random, not balanced (PRIVATE is first in 11 blocks, PUBLIC in 7), and 8 worlds per regime cannot balance the special role over five agents. Team success may sit at the ceiling once the facts are released. The premature-choice screen for PREPARE is a word pattern.

## Conditions

- The reviewer's machine is being shut down tonight (agentops issue 123), so there is no reviewer check between stages. The software gates decide whether S1-R and S1-L start. The operator, dmarz/orbital-orchestrator, writes the stage post-mortem and reports to dmarz before launching the next stage, and stops if a gate fails. dmarz can stop the sequence at any point.
- If S1-Q fails competence, nothing else runs under m1. The amendment route in [s1-pre.md](s1-pre.md) needs a new approval record; that decision is dmarz's, because this reviewer will not be available.
- Each post-mortem reports the first-answer table by regime, results by arm-order position, actual calls, tokens and dollars, and every invalid output.
- Nothing produced here may be described as independently reviewed.
