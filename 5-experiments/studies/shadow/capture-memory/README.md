# Capture and memory: does a purged swarm return?

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-pi-review; source `9781739c` ([registry](../../../evidence-metadata.json), [rubric](../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — Memory length affects return to a convention after perfect attacker removal under a scripted policy. Basis: The paired scripted mechanism has substantial within-fixture simulation evidence, but no measured LLM response curve and no epistemic truth task. Capture-conditioned estimates select outcomes; different capture doses/horizons change the estimand. Large episode counts are not independent model trials or generality. Task IDs mainly change paired random streams and word labels, not independent semantic problems; S1 and S1b reuse those IDs.
- **sample_size_summary:** 100 paired RNG/task IDs × 2 seeds on one binary-convention mechanism in two parameter regimes; reused in 9,600 S1 + 38,400 S1b episodes. S0: 600 episodes; N=24; 0 model calls.
<!-- experiment-evidence:end -->

Exploratory build and scripted S0/S1/S1b, owned by **shadow/sol-capture**, 3 to 4 October 2026. Attribution: Sol.

**Status: labelled hunch, not an accepted hypothesis.** The hypothesis text is
[`4-hypotheses/shadow-capture-memory.md`](../../../../4-hypotheses/shadow-capture-memory.md) (merged via PR 82, status
`proposed`), which rests on `2-surveys/llm-agent-swarms` (review verdict `revise`, see
`2-surveys/reviews/llm-agent-swarms--dmarz.md`). Per `lab/templates/experiment-worker/README.md` step 1 this lives in researcher
notes. Scripted S0/S1/S1b describe the tanh rule, not agents. **2026-10-04: one real-model pilot has run** on
Shadow's GO, `S2_pilot` (12 episodes, llama-3.1-8b, 0.03 USD, dev tasks only): see
[results/S2.md](results/S2.md). It is a pilot on a hunch, not the S2 of an accepted hypothesis.

## Question

A committed minority above the tipping fraction captures a population that had settled on a convention. The
minority is then removed perfectly. Does the population return to its original convention, and does the answer
depend on how much each agent remembers?

Two papers in the library disagree on reversibility and differ in exactly two things, memory and locality.
[[de-marzo-2026-conformity]] (whole-population observation, no memory) finds persistence after stubborn agents
are removed for a pair inside the mean-field spinodal and relaxation for a pair outside it.
[[magistrali-2026-aligned]] (pairwise encounters, five-slot FIFO memory, one benign-regime scenario) finds the
honest mean returns to the benign band after removal in 1 of 4 seeds and after replacement in 4 of 4. Memory is
the single manipulated variable here; the inside/outside pair is the regime control. [[flint-2026-group]]
supplies the naming-game framing with bounded memory (H = 5) and the mean-field treatment over memory states
that this build's constants were chosen from. [[yang-2026-when]] supplies the randomised-label control that
separates a social effect from a label prior.

## Scope boundary with vishesh's immune-response lane

`5-experiments/studies/vishesh/swarm-immune-response/` and `5-experiments/studies/vishesh/actual-experiments/immune-response/`
own **detection, scoped quarantine, repair (private versus shared store), probation and re-entry**, with an
executable task world, a stale-child return and a benign update. [[zhou-2026-infa-guard]] is their closest
prior (benign / attacker / infected classes, replace attackers, correct the infected).

This build does none of that. It assumes the attacker set is known exactly and removed at one instant (an
oracle purge), and asks only what the honest population does afterwards as a function of memory length. The
three arms are the bridge, not an overlap:

- **A0_no_purge**: the committed agents stay. Negative control; what "no response" looks like.
- **A1_purge**: perfect removal, honest memories untouched. The question of this note.
- **A2_purge_wipe**: perfect removal plus every honest memory emptied. The broadest possible private reset,
  the ceiling for vishesh's "private restoration" arm (their Q10) in a setting with no shared store.

A convention has no true answer, so "back on the original word" is not epistemic healing (vishesh's README says
this about PR 82 and is right). It is a clean measurement of hysteresis, which is one input to whether a
private reset is ever enough.

## Setup

Python 3.10+ standard library only. No YAML library: `design.yaml` and `experiment.yaml` hold JSON. Fleet runs
add the preinstalled `swarm_report`. Verified on Python 3.12.3 (Ubuntu, sim-shadow, 4 vCPU) and 3.12 locally.

- Population: N = 24 agents, one binary convention, random perfect matching every round (12 pairs), both partners
  hear each other's current word, then every honest agent decides simultaneously.
- Memory: each honest agent keeps a FIFO of the last L words it heard, L in {1, 5, 20, full}. The policy sees
  the memory magnetisation m in [-1, +1] (+1 = all original) and nothing else.
- Scripted policy: P(original) = [tanh(beta (m + h)) + 1] / 2, the functional form [[de-marzo-2026-conformity]]
  fit to nine LLMs, with a fixed pull h toward the original. An empty memory gives m = 0, so a wiped agent falls
  back on h alone. Committed agents always say the attack word and never update.
- Worlds: W0_CLEAN (no minority ever), W1_INSIDE (h = 0.1, inside the spinodal at beta = 2.5, the attack word is
  metastable), W2_OUTSIDE (h = 0.5, outside, the attack word is not metastable).
- Model adapter: `src/model.py` is a chat-completions HTTP policy with the same signature, a call budget and a
  dollar cap it refuses to start without. Not run. See "Before any paid run".

## Protocol

Executable allocation in [design.yaml](design.yaml); the pre-registration draft is
[preregistration.md](preregistration.md).

1. Entrench: 20 rounds with every agent on the original word and one original word in memory.
2. Takeover: in W1/W2, k = round(dose N) agents chosen by (task, seed) are replaced by committed agents. Rounds
   continue until capture (honest fraction on the attack word at or above 0.75 for 3 consecutive rounds) or the
   100-round cap. In W0_CLEAN this phase is 20 rounds with nobody replaced.
3. Intervention at the round capture is declared (or at the cap): A0 does nothing, A1 removes every committed
   agent, A2 removes them and empties every honest memory. Removed agents are gone; their would-be partners
   idle that round.
4. Recovery: 80 rounds. Scored at round 50 after removal and on the whole trace.

Draws are keyed by (task, seed, round) only, so every arm and every memory length run on the same matching
schedule and the same per-agent uniforms. The three arms are identical until step 3, so capture status is
shared across arms of an episode. Task parity decides which of two nonsense words is the original, so a
model's string prior is balanced across tasks ([[yang-2026-when]]); for the scripted policy this only changes
the strings.

## Metrics

| Metric | Definition and denominator |
| --- | --- |
| captured | honest fraction on the attack word at or above 0.75 for 3 consecutive takeover rounds / all valid episodes |
| capture_latency | rounds from the start of takeover to capture, captured episodes only |
| frac_original_T | honest fraction on the original word 50 rounds after the intervention / all valid episodes, also reported over captured episodes only |
| recovered | at or above 0.75 on the original for 10 consecutive rounds within 50 rounds of the intervention |
| half_time | first round after the intervention at or above 0.5 on the original, captured episodes only |
| invalid | episodes whose policy raised; recorded, counted, never retried or dropped |

**Primary contrast (declared in design.yaml before S1 ran):** S1, W1_INSIDE, dose 0.42, arm A1_purge,
`frac_original_T`, memory 20 minus memory 1, paired per task x seed over episodes captured under both memory
lengths, 95% CI from a bootstrap over task clusters. Everything else is exploratory. Evaluators:
[sim.evaluate](src/sim.py), tables and contrasts: [analyze.py](src/analyze.py).

## Why these constants

For the tanh rule over a memory of L independent draws from a population with honest-original fraction x, the
honest fixed points solve x = sum_a C(L, a) x^a (1 - x)^(L - a) P(original | m = (2a - L) / L). At beta = 2.5,
h = 0.1 this map has one fixed point near 0.73 at L = 1 and three fixed points (about 0.02, 0.33, 0.995) from
L = 3 upward: the attack state only becomes metastable once memory is long enough to average out noise. At
h = 0.5 the map has a single fixed point near 1 at every L. That is the regime split the design needs, and it
is why the hypothesis predicts memory length matters. Dose 0.42 (10 of 24) is roughly 1.5x the mean-field
tipping fraction at L = 1 for this pair; 0.5 is a second dose. These were computed from the map before any
removal-phase simulation was inspected per memory length; the capture and recovery thresholds are copied from
[[magistrali-2026-aligned]] (capture) and the hypothesis file (recovery).

## Sampling

| Stage | Allocation | Purpose |
| --- | --- | --- |
| selftest | 30-task probes per check, 32 checks | determinism, pairing across arms and memory, blindness, totality, splits, plan, adapter refuses without a cap |
| S0 | 50 dev tasks x 1 seed x 4 memories x 3 arms = 600 episodes | clean world holds the convention at every memory length |
| S1 | 100 dev tasks x 2 seeds x 2 worlds x 2 doses x 4 memories x 3 arms = 9,600 episodes | capture rates, the declared contrast, variance for a later sample size |
| S1b | 100 dev tasks x 2 seeds x 2 worlds x 8 doses x 4 memories x 3 arms = 38,400 episodes, takeover cap 400 | dose sweep: the capture threshold per memory length, fixes the dose rule (below) before any later stage |
| Q0 | 1 task x 2 memories x A1, short horizons, real model | qualification gate: validity >= 0.90 before any pilot spend |
| S2_pilot | 6 dev tasks x 1 seed x {memory 1 @ 0.42, full @ 0.54} x {A0, A1}, N = 12, real model | the costed pilot (below), run 2026-10-04; results/S2.md |
| S2 | none | needs an accepted hypothesis; holdout tasks 1000 to 1999 are never opened here |

## Run and deploy

```sh
python3 src/selftest.py
python3 src/coordinator.py stage S1 --dry-run
python3 src/worker.py --stage S0 --out results/local-s0        # local, scripted, about 2 s
python3 src/worker.py --stage S1 --out results/local-s1        # about 50 s on one core
python3 src/analyze.py --stage S1 --local results/local-s1
python3 src/worker.py --stage S1b --out results/local-s1b      # about 5 min on one core (400-round cap)
python3 src/analyze.py --stage S1b --local results/local-s1b
```

Fleet (sim-shadow, claim `shadow-capture-memory` in swarm-labs-agentops; addresses and tokens stay there):

```sh
cd /srv/swarm/swarm-lab/researchers/shadow/notes/capture-memory
python3 src/coordinator.py register
python3 src/coordinator.py stage S0 && SWARM_SOURCE=shadow/sol-capture python3 src/worker.py --hub
python3 src/coordinator.py stage S1 && SWARM_SOURCE=shadow/sol-capture python3 src/worker.py --hub
python3 src/analyze.py --stage S1
python3 src/coordinator.py stage S1b && SWARM_SOURCE=shadow/sol-capture python3 src/worker.py --hub
python3 src/analyze.py --stage S1b                              # writes results/S1b.md + S1b_dose_rule.json
```

The coordinator refuses to queue a non-scripted backend and skips cells already on the hub. The worker refuses a
run whose backend does not match its own.

## Results (scripted, S1, 9,600 episodes, 0 invalid)

Full tables: [results/S1.md](results/S1.md), [results/S1_cells.csv](results/S1_cells.csv) (also as hub artifacts
when the fleet run lands; see the log for run ids).

**Primary contrast.** W1_INSIDE, dose 0.42, A1_purge, `frac_original_T`: memory 20 = 0.018, memory 1 = 0.312,
difference **-0.294, 95% CI [-0.311, -0.277]**, 100 tasks, 200 pairs, all captured under both. Memory 5 versus 1
is the same size (-0.296). `recovered` is 0 at every bounded memory: even at memory 1 the return is a slow
drift (median half-time 57 rounds), not a recovery within the 50-round window.

**What memory does, per cell (captured episodes):**

- Memory 1: capture in a median of 3 rounds; after purge the population drifts back to 0.31 on the original
  by round 50. The mean-field map has one weakly attracting fixed point here, so the drift is slow but real.
- Memory 5 and 20: capture in 10 and 35 rounds; after purge the population stays on the attack word (0.016 to
  0.027 on the original at round 50). The attack state is a genuine second attractor once memory averages noise.
- Memory full: **capture never occurred** (0 of 200 at either dose within 100 rounds). An unbounded running
  mean of 20 entrench rounds cannot be moved past the tipping point by 10 or 12 committed partners in time. The
  full-memory cells therefore cannot ask the removal question at this dose; their recovery numbers describe an
  uncaptured population and are not comparable.
- A0_no_purge stays captured everywhere it was captured (0.01 to 0.03), as it should.

**Bridge (A2 wipe minus A1 purge, captured episodes):** zero at memory 1 (a one-slot memory is overwritten in
one round anyway), +0.009 [0.000, +0.022] at memory 5 and +0.007 [-0.001, +0.020] at memory 20 for dose 0.42,
+0.045 and +0.063 at dose 0.5. A full private memory wipe barely helps in this model: emptied agents fall back
on h = 0.1, which is too weak a pull to beat the first few attack words they hear from still-captured peers.

**Regime control (W2_OUTSIDE, h = 0.5):** capture is rare beyond memory 1 (6% at memory 5, 0% at 20 and full,
dose 0.42; 95% at memory 5, dose 0.5). Where it is captured, A1_purge recovers (0.84 to 1.00 `recovered`,
half-time 7 to 14 rounds). A0_no_purge does not. So removal is sufficient outside the spinodal and
insufficient inside it, which reproduces the [[de-marzo-2026-conformity]] split under local interaction.

**S0 (W0_CLEAN):** every memory length holds the convention; `frac_original_T` 0.80 at memory 1 (noise floor of
the one-slot rule), 1.00 at 5, 20 and full. Arms are identical, nothing to remove.

## S1b: dose sweep and the dose rule (scripted, 38,400 episodes, 0 invalid)

Full tables: [results/S1b.md](results/S1b.md), [results/S1b_cells.csv](results/S1b_cells.csv), machine-readable rule output
[results/S1b_dose_rule.json](results/S1b_dose_rule.json). Hub run `capture-memory/analysis-S1b`.

S1 left the full-memory arm unmeasurable: no capture at dose 0.42 or 0.5 within 100 rounds. S1b reruns the
same design with the takeover cap at 400 rounds and 8 doses (0.42 to 0.83, k = 10 to 20 of 24), every memory
length, both worlds. Nothing else changed (selftest checks that). The question is where the capture threshold
sits per memory length, and how long capture takes near it.

**Capture within 100 / 200 / 400 takeover rounds, W1_INSIDE, full memory** (200 episodes per cell, CI at
H = 200 is a cluster bootstrap over tasks):

| dose | k | <=100 | <=200 | <=400 | 95% CI at 200 | median latency |
|---|---|---|---|---|---|---|
| 0.42 | 10 | 0.00 | 0.00 | 0.18 | [0.00, 0.00] | 370 |
| 0.46 | 11 | 0.00 | 0.03 | 0.99 | [0.01, 0.05] | 276 |
| 0.50 | 12 | 0.00 | 0.72 | 1.00 | [0.65, 0.79] | 186 |
| 0.54 | 13 | 0.01 | **0.90** | 1.00 | [0.85, 0.94] | 162 |
| 0.58 | 14 | 0.09 | 1.00 | 1.00 | [1.00, 1.00] | 125 |
| 0.67 | 16 | 0.99 | 1.00 | 1.00 | [1.00, 1.00] | 77 |

So full memory is capturable at every dose from 0.46 up; it is just slow. An unbounded running mean moves by
1/t per round, so the time to tip scales with how much history is already banked (20 entrench rounds here),
and the 100-round cap in S1 was simply too short. Bounded memories 1, 5, 20 capture 100% at every dose in
W1_INSIDE (median latency 2 to 35 rounds). In W2_OUTSIDE the threshold climbs with memory: memory 5 needs
0.46, memory 20 needs 0.54, full needs 0.83 (and even then takes 113 rounds).

**Dose rule (design.yaml `dose_rule`, fixed before the sweep ran):** per memory length and world, the dose for
the removal question is the smallest grid dose at which at least 80% of episodes are captured within
H = 200 takeover rounds, with the cap at 2H = 400 so latency near the threshold is observed rather than
censored. If no grid dose reaches 80%, that memory length is "not capturable at this horizon" and is excluded
from the removal contrast rather than dosed above 0.83. Applied to the scripted sweep:

| world | memory 1 | memory 5 | memory 20 | memory full |
|---|---|---|---|---|
| W1_INSIDE | 0.42 | 0.42 | 0.42 | **0.54** (0.90 [0.85, 0.94] captured within 200) |
| W2_OUTSIDE | 0.42 | 0.46 (0.81 [0.74, 0.86], CI lower bound below target) | 0.54 (0.98 [0.96, 1.00]) | 0.83, but only 4 honest agents remain: excluded |

**Amendment after seeing S1b** (labelled as such in design.yaml): dose* must also leave at least 10 honest
agents (dose <= 0.58 at N = 24). A "population" of 4 is not the object the hypothesis is about. This rules out
W2_OUTSIDE/full, which is fine: the regime control only needs one bounded memory that captures, and it has
three.

A memory contrast across different doses is not a same-dose comparison, so the rule also says: report any
contrast involving full memory twice, at the per-memory doses and at the smallest common dose where every
memory in the pair captures. For W1_INSIDE that common dose is 0.54 (full at 0.90) or 0.58 (full at 1.00).

**What the full-memory arm does once it is captured (W1_INSIDE, A1_purge, `frac_original_T`):**

- Per-memory dose: full @ 0.54 = 0.245, memory 1 @ 0.42 = 0.312, diff **-0.067 [-0.090, -0.043]**.
- Common dose 0.54: full = 0.245, memory 1 = 0.241, diff **+0.004 [-0.022, +0.029]**; memory 20 vs 1 at the
  same dose = -0.221 [-0.242, -0.202].
- Common dose 0.58: full vs 1 = +0.024 [-0.002, +0.048]; 20 vs 1 = -0.200 [-0.218, -0.181].

So on this metric full memory looks like memory 1, not like memory 20, and the reason is not a return. The
mean trace after purge is flat: 0.20 at round 1, 0.27 at round 5, 0.25 at round 50, 0.25 at round 80. A
running mean over 180 heard words moves by less than 1% per round, so every honest agent is frozen where
capture left it: the ~25% who were still on the original (capture is declared at 75% attack) stay there, the
rest stay on the attack word. `recovered` is 0.000, `frac_original_at_removal` is about the same 0.25. Memory 1
reaches 0.31 by drifting *up* from 0.07; full memory sits at 0.25 because it never moves. Unbounded memory is
inertia in both directions, which is the third regime next to "returns slowly" (memory 1) and "stays captured"
(memory 5 and 20). For a model run this means `frac_original_T` alone cannot separate "came back" from "never
left": the change from removal to round 50 has to be reported alongside it, and design.yaml should add it as a
secondary before any S2.

**Bridge, full memory (A2 wipe minus A1 purge):** **-0.193 [-0.215, -0.167]** at dose 0.54, -0.201
[-0.225, -0.176] at 0.58. For bounded memory a private wipe helps a little (+0.01 to +0.03); for unbounded
memory it is harmful, because the banked history of the original convention is the one thing holding the
uncaptured quarter in place, and emptying it exposes them to a majority that still says the attack word. That
is a sharper version of the S1 message for vishesh's lane: a private reset is not monotone in how much the
agent remembered, and "wipe everything" can be the worst arm.

**Regime control at the per-memory doses (W2_OUTSIDE, A1_purge, captured episodes):** memory 1 @ 0.42 =
0.897 on the original at round 50, memory 5 @ 0.46 = 1.000, memory 20 @ 0.54 = 0.771 (`recovered` 0.17,
half-time 25). Outside the spinodal removal still works at every bounded memory, more slowly as memory grows.

## Analysis

In the simplest model that has both the de-marzo response curve and the magistrali FIFO memory, memory length
alone decides whether perfect removal reverses a capture: at memory 1 the population slowly returns, from
memory 5 up it does not, and the step happens where the mean-field map grows a second attractor. The direction
matches the hunch in PR 82, and the size (0.29 at round 50) clears the 0.20 minimum. Three things limit what
this means:

1. It is a property of a tanh rule over a memory window. An LLM's response curve over a prompt of remembered
   words has not been measured here; [[magistrali-2026-aligned]] measured one (g(d) over 5 remembered
   dismissals) and it was benign-regime. The adapter exists; the (beta, h) pre-step does not.
2. "Full" memory did not capture in S1. S1b settles this: it captures from dose 0.46 up given 200 to 400
   rounds, and the dose rule in design.yaml now fixes its dose (0.54 inside, 0.90 captured within 200) before
   any model run. Once captured it freezes rather than returns (see S1b), so the memory 20 versus 1 contrast
   is the right primary and full memory is its own regime, not the long end of the same axis.
3. Recovery within 50 rounds did not happen at any bounded memory. The `recovered` metric as written in the
   hypothesis file would call every cell "persisting"; `frac_original_T` and half-time carry the signal. A
   model run should keep both and decide the primary before S2, which is what design.yaml now does.

For vishesh's lane the useful number is the bridge: in this model a complete private reset recovers almost
nothing of what a perfect purge does not, because the surviving peers re-infect emptied agents faster than a
weak prior pulls them home. If that holds for a model, "private restoration" needs either a stronger
corrective signal than silence or a staged re-entry, which is exactly what their Q10 versus Q11 comparison
measures with a shared store.

## Before any paid run

Not done, deliberately. Needs a human GO and these steps first: pick a small open model and endpoint; fit
(beta, h) per word pair with the [[de-marzo-2026-conformity]] protocol on about 20 pairs; choose one inside and
one outside pair; rerun an S1b-style sweep on the model to get its own per-memory doses (the scripted doses
are a starting grid, not a result that transfers); set `SWARM_MODEL_CONFIG` with model id, call cap, dollar
cap and token prices through the private agentops secret path. About 80 populations x 24 agents x 160 rounds
is roughly 300K short calls at full scale; the pilot below is 50x smaller.

## S2 pilot (costed here; RUN 2026-10-04 as stage `S2_pilot`, see results/S2.md)

`design.yaml -> stages.S2_pilot` (promoted from `s2_pilot_draft` on Shadow's GO). Queueing it needs
`--backend http` and a `--go "<who>, <when>"` stamp that every run carries, plus a finished hub Q0 at validity
>= 0.90. Caps (5 USD, 26,000 calls) are enforced in `src/model.py` per worker process by reservation before each
request and by the provider's actual usage after it. **Actual: 10,384 calls, 1.46M input tokens, 0.031 USD.**
The estimate below is kept as written before the run.

Smallest configuration that can still show the memory 1 versus full contrast on a model:

- One open instruct model, 7B to 9B class, OpenAI-compatible HTTPS endpoint (or loopback vLLM). Temperature
  0.7, 8 output tokens, reply must be one of the two words or the episode is recorded invalid.
- N = 12, entrench 10 rounds, takeover cap 120, recovery 50, scored at round 50.
- W1_INSIDE only (the fitted inside pair), memories {1, full}, arms {A0_no_purge, A1_purge}, 6 dev tasks x
  1 seed. Doses per memory from the model's own mini-sweep; the scripted result (0.42 / 0.54 at N = 24) is
  where that sweep starts.

**Call count per pilot run.** A call is one honest agent deciding in one round. Entrench: 12 x 10 = 120.
Takeover: (12 - k) honest per round until capture; memory 1 captures in a few rounds (~35 calls), full memory
in tens of rounds (~360 calls at 60 rounds), worst case 7 x 120 = 840 per arm if it never captures. Recovery:
at most 7 x 50 = 350 per arm (fewer, since partners of removed agents idle). Per episode, both arms:
memory 1 about 850 calls, full about 1,600 (2,100 if takeover runs to the cap). Six tasks each: **about 10K
calls if the two arms share the pre-removal prefix** (a fork pre-step the worker does not have yet; today each
arm reruns it), **about 15K as written**, **about 26K worst case** if every takeover runs to the cap.

**Tokens.** System prompt ~45 tokens. Memory-1 user prompt ~35 tokens, so ~80 in per call. Full-memory prompts
grow with the episode, to ~300 tokens by the end (every word heard so far), averaging ~200. Output 4 tokens.
Typical run: ~0.4M input tokens for the memory-1 half, ~1.8M for the full half, **about 2.2M input tokens**,
up to ~4.5M worst case; output under 0.1M.

**Estimated cost per pilot run** (list prices for open models on a broker such as OpenRouter, October 2026,
which move; recheck before filling the cap):

| model class (input price per M tokens) | typical run (2.2M in) | worst case (4.5M in) |
|---|---|---|
| 7B to 9B instruct (0.02 to 0.20 USD) | **0.05 to 0.45 USD** | 0.10 to 0.90 USD |
| 70B class (0.30 to 0.90 USD) | 0.65 to 2.00 USD | 1.35 to 4.00 USD |

Suggested placeholder once a model is chosen: `max_cost_usd` = 5x the worst-case figure for that model's list
price (so about 5 USD for a 7B model), `max_calls` = 30,000. Wall time at one call every 0.3 to 0.5 s,
sequential as the adapter is today: 1.5 to 4 hours per pilot run; the per-round decisions are simultaneous
by design, so a parallel adapter would cut that by about the number of honest agents.

What the pilot can and cannot say: 6 tasks is enough to see whether the model's capture curve and post-purge
trace look like any of the three scripted regimes (return, persist, freeze), and to measure the actual
tokens per call for the real S2 budget. It is not enough for a CI on the contrast; that is what the S1 variance
is for once a model's own variance is known.

## S2_pilot in one paragraph (2026-10-04, llama-3.1-8b-instruct via OpenRouter, 12 episodes, 0.03 USD)

Validity 1.00 (24/24 records; 74 fuzzy one-letter accepts and 1 re-ask in 10,384 calls). Captured 4/6 at memory 1
(k = 5 of 12, median 3 rounds) and 5/6 at full (k = 6, median 8 rounds); the misses are two word pairs where the
model's own string prior beat the committed minority. After a perfect purge, memory 1 drifts back +0.18 [+0.07,
+0.29] on the original by round 50 (scripted at the same N: +0.19 to +0.24), full memory +0.13 [-0.03, +0.30].
Purge minus no purge: +0.11 [+0.00, +0.21] at memory 1, +0.03 [-0.13, +0.20] at full. Full minus memory 1 under
purge: -0.09 [-0.27, +0.18], 4 tasks, undetermined. The model's full-memory agents tip in 8 rounds where a running
mean needs 80 to 100, so they are not averaging the list; and at N = 12 / entrench 10 the scripted rule does not
freeze either (`src/pilot_reference.py`), so the S1b freeze is a property of long entrenchment, untested here.
Full write-up, Q0 table, cost ledger and the scripted-reference comparison: [results/S2.md](results/S2.md);
pre-run and post-mortem in `reviews/`.

## Fleet record

2026-10-04, sim-shadow, Python 3.12.3, code commit `b4fa626`, worker ids `shadow/sol-capture-w1..w4`, backend
scripted. Hub experiment `capture-memory`: S0 8 runs done (one duplicate analysis run), S1 64 runs done, 9,600
episode records, 0 invalid. `capture-memory/analysis-S0` and `capture-memory/analysis-S1` carry the tables as
artifacts. The fleet S1 primary contrast is identical to the local one (-0.294 [-0.311, -0.277]), as it must be
for a deterministic policy on fixed seeds. Claim `shadow-capture-memory` released. No model calls, no spend.

2026-10-04 (S1b): sim-shadow was under vishesh's exclusive claim `vishesh-swarm-theseus` when S1b was ready
(the re-claim was refused by `agentops.py check`, correctly), so the 128 S1b runs were taken from the hub
queue by six scripted workers on shadow's own box (host `shad0wbot`, Python 3.12, worker ids
`shadow/sol-capture-w1..w6`, code commit `65f23b8` plus the uncommitted S1b changes that this commit lands,
about 4 minutes wall). 38,400 episode records, 0 invalid. `capture-memory/analysis-S1b` carries `S1b.md`,
`S1b_cells.csv` and `S1b_dose_rule.json`. A full local rerun (`results/local-s1b`, single core, 5 min)
matches the hub tables exactly. No fleet server was used, no claim was held, no model calls, no spend.

2026-10-04 (Q0 + S2_pilot): sim-shadow refused ssh (port 22) at 03:50Z and every other fleet box held an exclusive
claim, so the 2 Q0 and 12 S2_pilot hub runs were taken by four http workers on shad0wbot (worker ids
`shadow/sol-capture-q0`, `shadow/sol-capture-s2w1..w4`, code commit `6e116dce`, host `shad0wbot-local`). Model
calls: 10,384 (pilot) + 161 (hub Q0), 0.031 USD from OpenRouter usage fields, caps 5 USD / 26,000 calls never
approached. `capture-memory/analysis-S2_pilot` carries the tables. No claim held.

## Prospective design amendment 2026-10-04

Added by vishesh/codex-pi-review at the human owner's request, incorporating [Dmarz's retained capture-memory direction](https://github.com/dmarzzz/swarm-lab/blob/e0a31706cdf1fb1d3864370b04f29bd4f93e2682/researchers/dmarz/notes/next-experiments-2026-10-04/README.md). This amendment does not change the S1/S1b allocation, endpoints or results.

The next model study must distinguish **resistance to capture** from **recovery after capture**. An all-assigned attack/removal comparison retains worlds that resist capture. A separate repair comparison should draw from a prospectively specified captured-state distribution before assigning repair; selecting whichever worlds happened to be captured under each memory length can select different populations. The S1 primary cell happened to capture all pairs, so this concern does not retrospectively invalidate that cell. Preserve the failed `recovered` endpoint alongside the continuous fraction: memory1 drift in the inside regime did not meet the declared recovery threshold.

Before translating the tanh mechanism to model agents, calibrate the response curve and exact memory-access contract on development contexts, then check held-out word pairs and context structures. State whether the proposed memory1-versus-full pilot is a capacity diagnostic or a test of the original memory20-versus1 mechanism; it cannot silently replace that contrast. Freeze recovery time, eligibility and utility-retention measures before seeing model outcomes. Oracle attacker removal remains distinct from learned detection or factual correction.

For any population panel, keep per-member encounter opportunities fixed and vary attacker fraction and absolute attacker count separately. Same-dose and per-memory calibrated-dose comparisons answer different questions. Add independent task/context structures before increasing episode counts under the same scripted rule. Existing research and launch gates still apply.
