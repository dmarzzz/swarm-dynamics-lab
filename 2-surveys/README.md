# 2-surveys: prior-art surveys

Phase 2 (survey) of [Swarm Dynamics Lab](../README.md). This folder holds one prior-art survey per topic or
question, and a survey must pass a mechanical gate and then a review by a different researcher before a
hypothesis built on it can be accepted.

## What this is

A survey is a prior-art scan of one topic or question, built from entries in the library. It is the gate in
front of every hypothesis. CI runs the gate: a survey passes with at least 20 cited library entries (10
papers, 3 code repos, 2 informal sources), 5 papers read in full, 3 seminal works with their forward
citations followed, and 8 logged search rounds in which the last 2 each turned up at most 15% new items. The
rules are in [AGENTS.md](../AGENTS.md#the-prior-art-gate).

## What is in here

The folder held five surveys on 4 October 2026. Two are marked complete and three are in progress. No survey
has passed review.

| Survey | Owner | Status |
|---|---|---|
| [`fork-merge-security.md`](fork-merge-security.md) | dmarz | complete |
| [`llm-agent-swarms.md`](llm-agent-swarms.md) | shadow | complete |
| [`sim-environments.md`](sim-environments.md) | dmarz | in progress |
| [`sybil-resistance.md`](sybil-resistance.md) | dmarz | in progress |
| [`vishesh-decision-models.md`](vishesh-decision-models.md) | vishesh | in progress |

[`reviews/`](reviews/README.md) holds the reviews of surveys, hypotheses and experiments. It held four on
4 October, all with the verdict `revise`.

## How to add to it

1. `python3 scripts/lab.py new survey <id> --agent <id>` creates a survey from the template with
   `status: in-progress`.
2. `python3 scripts/lab.py gate <survey-id>` lists what the survey still lacks.
3. When the gate reports nothing missing, set `status: complete` and open a review task for another
   researcher.

## Where it goes next

Surveys are built from [`1-library/`](../1-library/README.md). The reading across surveys is in
[`3-synthesis/`](../3-synthesis/README.md), and a hypothesis that cites a complete survey goes in
[`4-hypotheses/`](../4-hypotheses/README.md).
