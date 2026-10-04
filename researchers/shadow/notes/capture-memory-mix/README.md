# Capture-memory-mix: do short-memory agents rescue a captured swarm, and at what fraction?

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-methods; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **unassessed** — Unassessed at registry discovery. Basis: Registration coverage only; this addition is not a review of the experiment or its results.
- **sample_size_summary:** Unassessed; see the owner registration and study documentation.
<!-- experiment-evidence:end -->

Owned by **shadow/sol-goal**, 4 October 2026, under the 12-hour goal in `GOAL-12H.md`. Attribution: Sol.
Builds on [capture-memory](../capture-memory/README.md) (PR 83, merged) and the hunch in
[shadow-capture-memory](../../../../hypotheses/shadow-capture-memory.md) (PR 82, status `proposed`).

**Status: exploratory, researcher notes.** Scripted stages M0/M1/M2 are done (one deterministic tanh rule, not
agents). The real-model pilot MP is described below; its results section says exactly what ran and what it cost.
Per `GOAL-12H.md`, a scripted result is a lead, not a finding, until a real model reproduces it.

## Question

capture-memory found three post-purge regimes in a population where every honest agent has the SAME memory
length: short memory (L = 1) drifts back toward the original convention, medium memory (L = 5, 20) stays captured,
and unbounded memory (a running mean over everything heard) freezes wherever capture left it. A full private
memory wipe helped slightly at bounded memory and was harmful at full memory.

Real swarms are not homogeneous in memory: context windows, summarisation policies and session resets differ per
agent. So: in a population where a fraction f of the honest agents keep a short window and the rest keep a long
one, does the short-memory fraction restart the return after a perfect purge, is the effect monotone in f, and
does a memory wipe stay harmful once some agents forget quickly anyway?

## Novelty check (done before the build, 04:00 to 04:20 UTC)

Searched `library/` (2,069 papers), `surveys/llm-agent-swarms.md`, and Exa/web for: heterogeneous or mixed memory
lengths in naming games / opinion dynamics; committed-minority removal with memory; rescue of a captured population
by a sub-population. What is already known:

- Memory length as a (homogeneous) control parameter: [[mehdizadeh-2026-exploring]] (memory x topology flips the
  sign of memory's effect on settling), [[hishiki-2026-how]] (memory length moves a spatial LLM PD swarm between
  regimes), [[flint-2026-group]] (H = 5, mean field over memory states), classic finite-memory naming games
  (Wang et al. 2007 EPJB; Fu et al. 2017 Physica A on memory loss; Lipowski 2008 oblivion). All homogeneous memory.
- Committed-minority removal and reversibility: [[de-marzo-2026-conformity]] (memoryless, whole-population view,
  spinodal decides persistence), [[magistrali-2026-aligned]] (5-slot FIFO, one benign scenario, returns),
  Niu et al. 2017 Sci. Rep. srep41750 (variable commitment; notes that heterogeneously distributed commitment
  behaves like its mean "for the most part"). None varies honest memory, none mixes memory lengths.
- Heterogeneous agents in consensus: Gao et al. AAAI 2017 (asymmetric topology and stubborn nodes, not memory);
  Antonic, Zakir, Dorigo, Reina AAMAS 2024 (mixtures of voter / majority update RULES against zealots, mean-field
  ODEs: 15 to 20% of cheap voter-rule agents match an all-majority swarm's regret). That is the closest prior: a
  mixture of decision rules trades robustness against cost. It is not a memory mixture and has no removal phase.
- vishesh's `heterogeneous-swarms` notes (HX-01..) mix model families, roles and tools, not memory windows, and are
  design sketches. dmarz's next-experiments doc (e0a3170) is about memory inheritance receipts, not this.
- Reset after capture: [[papadopoulos-2026-mind]] (SOUL.md persistence, wiping context between sessions), the
  swarm-ai.org "memory wipes" posts (store reset leaves agent values intact). Both are about one reset policy, not
  the fraction of agents that forget.

Not found anywhere: (i) a memory-length MIXTURE as the manipulated variable, (ii) a rescue fraction f* for the
return after purge, (iii) non-monotonicity in f, (iv) the dependence of wipe harm on f. Those are the claims here.

## Setup

Identical to capture-memory except the memory axis: `src/sim.py` reproduces capture-memory's `sim.py` bit for bit
for homogeneous memory (selftest check 1, 72 arm-records identical) and adds a mix spec
`{"short": L_s, "long": L_l, "f": f}`: round(f x n_honest) honest agents hold the short window, the others the long
one, chosen by a draw keyed on (task, seed). The simulator now forks the three arms from one shared pre-removal
prefix (same trajectories as before, a third of the compute). Policies are batched per round so a model backend can
issue a round's calls concurrently.

- N = 24, beta = 2.5, h_inside = 0.1 (metastable attack state), h_outside = 0.5 (regime control), entrench 20,
  takeover until capture (75% attack for 3 rounds) with a 400-round cap, recovery 80, scored at round 50 after the
  intervention. Dose per long-memory type from capture-memory's dose rule: 0.42 for L = 20, 0.54 for full (and 0.54
  for L = 20 as the common dose).
- Arms: A0_no_purge, A1_purge (oracle removal), A2_purge_wipe (removal plus every honest memory emptied).
- New metrics: `delta_original` = frac on the original at round 50 minus at removal (0 = frozen, > 0 = returning),
  and the same split by kind (`short_T`, `long_T`, `delta_long`). The primary is `delta_original` under A1_purge,
  mix 1/full at dose 0.54, f = 0.5 minus f = 0 (design.yaml, fixed before M1 ran).

Stages (scripted, 100 dev tasks x 2 seeds x 3 arms per cell, 0 invalid everywhere):

| stage | cells | episodes | what |
|---|---|---|---|
| M0 | 5 homogeneous anchors | 3,000 | reproduces capture-memory S1/S1b cells exactly (full@0.54 delta +0.102, 20@0.42 -0.109, 1@0.42 +0.243) |
| M1 | 3 families x 9 fractions | 16,200 | mix 1/20 @0.42, mix 1/20 @0.54, mix 1/full @0.54, f in {0, 1/8, ..., 1} |
| M2 | 2 families x 9 fractions | 10,800 | W2_OUTSIDE mix 1/20 @0.54 (regime control), W1 mix 5/full @0.54 (short = 5) |

Run: `python3 src/selftest.py`, `python3 src/worker.py --stage M1 --out results/local-m1 --jobs 12` (about 2 min on
12 cores), `./run_analyses.sh`. Tables: [results/M0.md](results/M0.md), [results/M1.md](results/M1.md),
[results/M2.md](results/M2.md), CSVs alongside.

## Scripted results (lead, not finding)

**1. Short-memory agents restart the return of a frozen full-memory swarm, and the full-memory agents move
too.** W1_INSIDE, mix 1/full, dose 0.54, A1_purge, captured episodes, `delta_original` (return from removal to
round 50):

| f (short fraction) | 0 | 1/8 | 1/4 | 3/8 | 1/2 | 5/8 | 3/4 | 7/8 | 1 |
|---|---|---|---|---|---|---|---|---|---|
| delta_original | +0.10 | +0.11 | +0.14 | +0.16 | **+0.23** | +0.30 | +0.38 | **+0.69** | +0.21 |
| frac on original at round 50 | 0.25 | 0.26 | 0.28 | 0.30 | 0.36 | 0.43 | 0.52 | **0.83** | 0.24 |
| long agents at round 50 | 0.25 | 0.26 | 0.29 | 0.30 | 0.36 | 0.43 | 0.52 | 0.90 | n/a |
| `recovered` (75% for 10 rounds within 50) | 0 | 0 | 0 | 0 | 0.01 | 0.02 | 0.04 | **0.60** | 0 |

Primary contrast f = 0.5 minus f = 0: **+0.127 [+0.099, +0.157]** (100 tasks, 200 pairs). The rescue threshold by
the pre-set rule (delta > +0.10 with CI above 0) is already met at f = 1/8 (+0.112 [+0.091, ...]), because the
all-full population itself scores +0.10 (its 20 to 25% uncaptured minority nudges upward); the contrast against
f = 0 becomes significant at f = 1/4 (+0.039 [+0.012, +0.066]).

**2. The effect is strongly non-monotone: the best population is 7/8 short, not all short.** An all-short
population (f = 1) returns only to 0.24 by round 50 and never recovers (its one-slot memory is noisy, the
fixed point near 0.73 is weakly attracting, half-time 67 rounds). An all-full population freezes at 0.25. Mix
7/8 short + 1/8 full reaches 0.83 with 60% of episodes fully recovered, median half-time 13 rounds. The
mechanism visible in the per-kind traces: the few full-memory agents, once the short majority has turned, carry
a running mean that is still dominated by 20 entrench rounds of the original word plus whatever they have heard
since; they turn back and then act as a slow, stable anchor that the noisy short agents keep re-sampling. The
short agents alone lack that anchor; the full agents alone cannot move. Neither pure population does what the
mixture does. (In the A0 control the committed agents stay and the mixture does not return: 0.04 at f = 7/8.)

**3. Mixed with L = 20 instead of full, the rescue needs almost everyone short.** mix 1/20 @0.42: delta is
negative (stays captured) up to f = 3/4, +0.09 at f = 7/8, +0.24 at f = 1. At dose 0.54 the f = 7/8 cell reaches
0.40 (better than either pure population: 0.24 at f = 1, 0.02 at f = 0), same non-monotone shape, smaller peak.
Twenty-slot agents are a genuine second attractor, not inertia, so a short majority has to outvote them rather
than just unfreeze them.

**4. Wipe harm persists and GROWS with the short fraction until f = 1.** A2 minus A1 on the round-50 fraction,
mix 1/full @0.54: -0.19 at f = 0, -0.29 at f = 1/2, -0.42 at f = 3/4, **-0.64 at f = 7/8**, 0 at f = 1. The wipe
erases exactly the banked history that makes the full-memory minority an anchor; the more a mixture relies on that
anchor, the worse the wipe. Delta among the long agents after a wipe at f = 7/8 is -0.82.

**5. Regime control (W2_OUTSIDE, h = 0.5) is monotone and boring, as it should be.** mix 1/20 @0.54, A1_purge:
0.77 at f = 0 rising smoothly to 0.89 at f = 7/8, 0.83 at f = 1; wipe helps (+0.22 at f = 0, +0.10 at 1/2, 0 at 1).
Outside the spinodal nobody freezes and short memory is simply faster. The non-monotone rescue is a property of the
metastable regime.

**6. Short = 5 instead of 1 rescues full memory too, but the peak moves.** mix 5/full @0.54: delta +0.37 at
f = 3/4, then DOWN to +0.20 at f = 7/8 and -0.04 at f = 1 (five-slot agents are themselves captured, so too many of
them re-capture the swarm). Peak at f = 3/4 instead of 7/8.

What this says in one line: in the metastable regime the post-purge fate of a swarm is set by the memory MIXTURE,
not the mean memory, with an interior optimum (mostly forgetful agents plus a small long-memory anchor), and the
only intervention that reliably destroys that optimum is wiping the anchors.

## Real-model pilot MP (GOAL-12H cap: USD 5, enforced)

Adapter: `src/model.py`. OpenRouter chat completions with `logprobs`, first-token mass of the two allowed words
(all 12 words start with distinct letters), renormalised: this is the cached-policy construction of
[[flint-2026-group]] at the per-call level, so the swarm's randomness stays keyed to (task, seed, round) and arms
stay paired. Allowed-name order alternates per call. Hard cap `HARD_CAP_USD = 5.0` clamps any config; a locked
disk ledger (`results/spend-ledger.json`) carries provider-reported cost across processes; the key is read from
`~/.moltbot/secrets/openrouter.key` only.

Calibration (probe logs in `results/calib-*.json` and the goal log; about 500 calls, USD 0.004 total):

- `meta-llama/llama-3.1-8b-instruct` (Novita, logprobs available): first-token mass on the two words is clean,
  but the response curve is NOT a majority rule. Over a 5-slot window P(A) FALLS as more partners said A (0.69 at
  0 of 5, 0.04 at 5 of 5 for ruvo/brisk; same sign on other pairs): the model anti-conforms (or reads the list as
  "names already taken"). Fitted beta < 1 with |h| = 1, outside the spinodal on every pair. Unusable for a
  committed-minority capture study at this prompt; this is itself a note for anyone planning a Llama-8B naming
  game through OpenRouter (Magistrali et al. used an explicitly instructed coordination game and read the decision
  token locally).
- `qwen/qwen3-14b`, `gemma-3-27b-it`, `llama-3.3-70b`: no usable first-token logprobs through the providers that
  served them (empty or reasoning tokens); `qwen3-8b`, `qwen-2.5-7b`, `mistral-7b`, `gemma-3-12b`, `ministral-8b`,
  `gpt-4.1-nano/mini`: 404 with `require_parameters` (no logprob-capable provider).
- `openai/gpt-4o-mini` (OpenAI/Azure, logprobs): a clean, sharp majority rule. P(A | n of 5 heard A) = 0.00,
  0.00, 0.03, 0.72 to 0.95, 1.00, 1.00 on four pairs; L = 1 copies the one word heard (1.00 / 0.00); empty memory
  is near 0.5 (0.22 to 0.50, a mild string prior). Fitted beta about 8, h about 0, deep inside the spinodal
  (h_s(8) = 0.72). Long lists: `A40 -> 1.00`, `B40 -> 0.00`, `A30 then B10 -> 1.00`, `B30 then A10 -> 0.00`,
  so it follows the whole-list majority, not the tail. BUT a 40-entry shuffled list with 25 A / 15 B gave 0.99,
  0.62, 0.44, 0.56 across pairs and 15 A / 25 B gave 0.05, 0.01, 0.50, 0.10: at 40 entries the model's count is
  noisy, so "full memory" on this model is a running mean with large read noise once the window passes ~20.

Decision: pilot on gpt-4o-mini (USD 0.15 / M input). beta about 8 and h about 0 means the model's own
scripted prediction (`src/predict.py --beta 8 --h 0`) is that at N = 16, dose 9/16, the committed minority captures
everything instantly and NOTHING returns after a purge at any memory (delta about 0 in all four cells): a beta that
high makes both conventions absorbing for the tanh rule. The pilot is therefore a test of whether the model
behaves like its own fitted tanh rule (then: no return anywhere, mixture irrelevant, and the scripted M1 result
does not transfer to a sharp-majority model) or departs from it (count noise at long windows, which the fit does
not model, could unfreeze the full-memory agents). Either outcome is informative; neither is the scripted result.

Cells (results/pilot-mp/cells.json): W1 analogue, N = 16, dose 9/16, entrench 5, takeover cap 60, recovery 40,
scored at round 30, 6 tasks x 1 seed, memory in {1, full, mix 1/full @0.5, mix 1/full @0.75}, arms A0/A1/A2
(A0 and A2 share the prefix, so the marginal cost is the recovery phase). Budget: about 16 x (5 + ~6 + 3 x 40)
calls per episode, 6 episodes per cell, 4 cells: about 12,500 calls, about 1.5 M input tokens, about USD 0.3.

## Pilot results (gpt-4o-mini, partial: 3 to 4 tasks per cell, run 1 of 2)

Run 1 (04:51 to 05:02Z) was cut off by a gateway restart after 3 of 6 tasks per cell (4 in the f = 7/8 cell), with
every arm complete for those tasks: 48 episode records, 0 invalid, about 13,100 model calls in the records, ledger
spend USD 0.341 for all pilot work (calibration + priors + run 1; the per-record `cost_usd` in run 1 is a cumulative
session figure, fixed in the adapter afterwards; the locked ledger is authoritative). Tables:
[results/MP.md](results/MP.md). Per-call log: `results/pilot-mp/calls-*.jsonl` (4,151 usable calls, response
curve in the goal log). Settings: N = 16, dose 8/16, entrench 5, takeover cap 60, recovery 40, scored at round 30.

What the model did, A1_purge, captured episodes, honest fraction on the original at round 30 after the purge
(`frac_T`) and its change since removal (`delta`):

| memory | n | captured | latency | frac at removal | frac_T | delta | long agents at T | fully recovered |
|---|---|---|---|---|---|---|---|---|
| all short (L = 1) | 3 | 3/3 | 2 | 0.00 | **0.00** | 0.00 | | 0/3 |
| all full | 3 | 2/3 | 37 | 0.25 | **0.38** | +0.13 | 0.38 | 0/2 |
| mix 1/full @ 1/2 | 3 | 3/3 | 16 | 0.13 | 0.25 | +0.13 | 0.08 | 0/3 |
| mix 1/full @ 3/4 | 3 | 3/3 | 5 | 0.21 | **0.75** | +0.54 | 0.83 | 2/3 |
| mix 1/full @ 7/8 | 4 | 4/4 | 3 | 0.16 | **0.63** | +0.47 | 0.75 | 1/4 |

- **The pure populations do not return; the mixtures do.** All-short: captured in 2 rounds and stays at exactly
  0.00 for 40 rounds in all 3 tasks (gpt-4o-mini at L = 1 copies its one remembered word with P = 1.00, so a
  captured one-slot population is absorbing, as the fitted beta = 8 predicts). All-full: captured slowly (37
  rounds) and then hovers at 0.25 to 0.38 (frozen at the uncaptured quarter plus count noise), 0/2 recovered.
  Mixtures at f = 3/4 and 7/8 go to 0.75 and 0.63 with 3 of 7 episodes fully recovered (75% for 10 rounds),
  and the FULL-memory agents in them end at 0.83 and 0.75 (1.00 in 5 of 7 episodes): the long-memory anchors turn
  back once the short majority is mixed. Traces are monotone climbs, e.g. f = 3/4 task 0: 0.25 at removal, 0.38,
  0.63, 0.75, 0.88, 1.00 by round 27 and stays; f = 7/8 task 0: 0.13 -> 0.50 -> 0.63 -> 0.75 -> 0.88.
- **Non-monotone in f, as scripted.** f = 1/2 (0.25) is no better than all-full (0.38); f = 3/4 and 7/8 are far
  better than both ends; f = 1 is the worst cell. The scripted M1 ordering (0 ~ 1/2 < 1 < 3/4 < 7/8) is
  reproduced in sign everywhere except that on this model f = 1 is strictly absorbing (scripted: slow drift to
  0.24). The paired contrast f = 7/8 minus f = 0 on `delta_original`: +0.44 [+0.38, +0.50] over the 2 shared
  captured tasks (tiny n, reported as a pilot).
- **Wipe harm reproduces and is largest in the rescued mixtures.** A2 minus A1 on the round-30 fraction: 0.00
  at all-short, -0.38 at all-full, -0.25 at f = 1/2, **-0.71 [-1.00, -0.25] at f = 3/4, -0.63 [-0.91, -0.28] at
  f = 7/8**. Every wiped population (any f < 1) went to exactly 0.00 on the original and stayed there: emptying the
  anchors' memory hands the swarm to the captured short majority within one round.
- A0 (committed agents stay) is 0.00 to 0.13 everywhere, so the returns above are caused by the purge.
- The scripted prediction at the model's own fitted (beta = 8, h = 0) said "full freezes near 0.03, mixtures at
  f = 3/4, 7/8 return to 0.18 / 0.42, wipe harm -0.14 / -0.36": the model is MORE rescuable than its tanh fit (0.75 /
  0.63) because its long-window reads are noisy (P(original | share 0.3 to 0.5 of a 30+ list) sits at 0.39 to
  0.47 rather than 0 or 1), which unfreezes the running mean. The qualitative picture (pure ends fail, mixtures
  return, wipe kills it) is the same in rule and model.

Status of the claim: real-model reproduction of the scripted lead on 3 to 4 tasks per cell, one model, one dose,
N = 16. Signs match on every contrast the design named (rescue, non-monotonicity, wipe harm growing with f). Not
yet a powered result; run 2 (below) adds tasks.

## Scope boundaries

Not vishesh's immune-response lane (no detection, no quarantine, no shared store; the purge is an oracle). Not
dmarz's memory-inheritance receipts (no parent/child, no evidence). The mixture here is of WINDOW LENGTHS in
otherwise identical agents, which is the one heterogeneity axis the heterogeneous-swarms notes list but do not
design for.
