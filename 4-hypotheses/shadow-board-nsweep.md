---
id: shadow-board-nsweep
type: hypothesis
title: A persistent shared board moves the wrong-consensus to polarisation crossover to larger N than pairwise exchange
owner: shadow
agents: [shadow/sol-1]
status: proposed
created: 2026-10-03
surveys: [llm-agent-swarms]
closest_prior: [pavlova-2026-flag, fukushima-2026-message, zhang-2026-silo, liu-2026-social, gh-killy-netsphere-sealed-swarm-transcripts]
topics: [message-board, broadcast, group-size, polarisation, wrong-consensus]
---

<!-- PROPOSAL ONLY. Not accepted, not run. Lower priority than shadow-neff-evidence-board and
shadow-capture-memory; filed so the board N-sweep has a written claim and kill criteria. -->

## Claim

With private partial evidence and ground truth, populations that communicate through a persistent shared
board reach wrong consensus more often and polarise less than pairwise populations of the same N, so the N
at which wrong consensus gives way to polarisation is at least twice as large on a board.

## Grounding

- [[pavlova-2026-flag]]: in pairwise exchange (GPT-4o, 40 seeds per N), wrong consensus falls from 26 to 34%
  at N = 4 to 0% at N = 128 while polarisation rises to 57 to 60%; accuracy peaks at N = 16. Broadcast was run
  only at N = 8.
- [[gh-killy-netsphere-sealed-swarm-transcripts]]: a sealed small-model swarm with a shared board
  synchronises onto one frontier and a bad recipe spreads faster than a correct one. One arm, no N sweep, no
  accuracy curve.
- The incident setting the hackathon is about was a persistent board, not pairwise chat. On a board every
  agent sees the same accumulated majority, which should make the majority force N-independent and suppress
  the fragmentation that produces polarisation in pairwise runs.
- [[fukushima-2026-message]]: bounded inbox reading has its own transitions (message capacity around 6.4 of
  31), so board visibility (how many recent posts an agent reads) has to be held fixed or swept.

## Novelty

- [[pavlova-2026-flag]]: the same endpoint classes and an N sweep, pairwise only, closed models. We sweep N on
  a board with open models. Honest difference: protocol and model family; design borrowed.
- [[fukushima-2026-message]]: sweeps reading capacity at fixed N = 32, binary claims. We sweep N at fixed
  visibility and use partial evidence with ground truth.
- [[zhang-2026-silo]]: N = 2 to 100 on sharded algorithmic inputs, no belief dynamics or polarisation
  endpoint.
- [[liu-2026-social]]: HiddenBench and Werewolf at n = 6 to 24 with a captured hub; herding floor at every
  size, no board persistence manipulation.
- [[gh-killy-netsphere-sealed-swarm-transcripts]]: board synchronisation, one condition. We add N and ground
  truth.

## Prediction

If true: at N = 32, wrong consensus on the board is at least 10% (pairwise near 0% per
[[pavlova-2026-flag]]); polarisation on the board stays under 30% up to N = 64; the crossover N (where
polarisation first exceeds wrong consensus) is at least 2x the pairwise crossover in our own pairwise arm.

If false: board and pairwise crossover N are within a factor of 1.5, or the board polarises earlier, meaning
persistence does not override local fragmentation at these sizes.

## Minimal experiment

- Task: private-crop identification in the Flag Game style (Flag Game code is not public; re-implement
  crops on public-domain flag renders), plus a text hidden-profile variant as a robustness check.
- Arms: pairwise (memory H = 8, as in [[pavlova-2026-flag]]) vs board (agents read the last V = 8 posts,
  persistent, append-only). One open model.
- N in {4, 8, 16, 32, 64}, 20 seeds per cell, 30 rounds or until consensus. Endpoint classes and thresholds
  copied from [[pavlova-2026-flag]].
- Prior-artefact control: country labels shuffled across renders for a 20% subset.
- Budget: the largest cost of the three proposals, around 2 x 20 x (4+8+16+32+64) x 30, about 150K calls.
  Run N <= 16 first and continue only if the board and pairwise curves already separate.

## Kill criteria

- Our own pairwise arm does not reproduce the qualitative [[pavlova-2026-flag]] shape (wrong consensus falling
  and polarisation rising with N): the task re-implementation is off; fix before comparing.
- Board and pairwise crossover N within 1.5x at N <= 64: claim refuted.
- The cost check at N <= 16 shows the full sweep exceeds the hackathon budget: park, keep the N <= 16 result
  as a pilot.
