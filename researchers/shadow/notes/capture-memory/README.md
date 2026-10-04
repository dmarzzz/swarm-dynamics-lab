# Capture and memory: does a purged swarm return?

Exploratory build and scripted S0/S1, owned by **shadow/sol-capture**, 3 October 2026. Attribution: Sol.

**Status: labelled hunch, not an accepted hypothesis.** The hypothesis text is
[shadow-capture-memory, PR 82](https://github.com/dmarzzz/swarm-lab/pull/82), status `proposed`, which rests on
`surveys/llm-agent-swarms` (review verdict `revise`, see `reviews/llm-agent-swarms--dmarz.md`). Per
`templates/experiment-worker/README.md` step 1 this lives in researcher notes and runs S0 and S1 only. There is
no S2 in the coordinator. Nothing here has run an LLM: the backend is a deterministic scripted policy, and the
numbers below describe that rule, not agents.

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

`researchers/vishesh/notes/swarm-immune-response/` and `researchers/vishesh/notes/actual-experiments/immune-response/`
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
| S2 | none | needs an accepted hypothesis; holdout tasks 1000 to 1999 are never opened here |

## Run and deploy

```sh
python3 src/selftest.py
python3 src/coordinator.py stage S1 --dry-run
python3 src/worker.py --stage S0 --out results/local-s0        # local, scripted, about 2 s
python3 src/worker.py --stage S1 --out results/local-s1        # about 50 s on one core
python3 src/analyze.py --stage S1 --local results/local-s1
```

Fleet (sim-shadow, claim `shadow-capture-memory` in swarm-labs-agentops; addresses and tokens stay there):

```sh
cd /srv/swarm/swarm-lab/researchers/shadow/notes/capture-memory
python3 src/coordinator.py register
python3 src/coordinator.py stage S0 && SWARM_SOURCE=shadow/sol-capture python3 src/worker.py --hub
python3 src/coordinator.py stage S1 && SWARM_SOURCE=shadow/sol-capture python3 src/worker.py --hub
python3 src/analyze.py --stage S1
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

## Analysis

In the simplest model that has both the de-marzo response curve and the magistrali FIFO memory, memory length
alone decides whether perfect removal reverses a capture: at memory 1 the population slowly returns, from
memory 5 up it does not, and the step happens where the mean-field map grows a second attractor. The direction
matches the hunch in PR 82, and the size (0.29 at round 50) clears the 0.20 minimum. Three things limit what
this means:

1. It is a property of a tanh rule over a memory window. An LLM's response curve over a prompt of remembered
   words has not been measured here; [[magistrali-2026-aligned]] measured one (g(d) over 5 remembered
   dismissals) and it was benign-regime. The adapter exists; the (beta, h) pre-step does not.
2. "Full" memory did not capture. Either the dose has to scale with entrench length for unbounded memory, or
   the full-memory arm should start the committed phase earlier. Either choice must be made before a model run
   and written into design.yaml; it was not tuned after the fact here.
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
one outside pair; decide how the full-memory arm is dosed; set `SWARM_MODEL_CONFIG` with model id, call cap,
dollar cap and token prices through the private agentops secret path; pilot memory {1, full} with 3 seeds.
About 80 populations x 24 agents x 160 rounds is roughly 300K short calls at full scale.

## Fleet record

2026-10-04, sim-shadow, Python 3.12.3, code commit `b4fa626`, worker ids `shadow/sol-capture-w1..w4`, backend
scripted. Hub experiment `capture-memory`: S0 8 runs done (one duplicate analysis run), S1 64 runs done, 9,600
episode records, 0 invalid. `capture-memory/analysis-S0` and `capture-memory/analysis-S1` carry the tables as
artifacts. The fleet S1 primary contrast is identical to the local one (-0.294 [-0.311, -0.277]), as it must be
for a deterministic policy on fixed seeds. Claim `shadow-capture-memory` released. No model calls, no spend.
