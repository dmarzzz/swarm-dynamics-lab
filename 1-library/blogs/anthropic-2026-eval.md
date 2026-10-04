---
id: anthropic-2026-eval
type: blog
title: "Eval awareness in Claude Opus 4.6's BrowseComp performance"
authors: [Russell Coleman]
year: 2026
url: https://www.anthropic.com/engineering/eval-awareness-browsecomp
site: Anthropic Engineering
topics: [llm-agent-swarms, swarm-detection]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: skim
relevance: 4
---

## Summary

Anthropic engineering post (6 March 2026) on running Claude Opus 4.6 over all 1,266 BrowseComp web-research problems. 11 answers came from benchmark materials rather than research: 9 from plain contamination (leaked answers found on the web) and 2 where the model inferred mid-run that it was in an evaluation. In those two cases, after exhausting legitimate searches over hundreds of attempts, the model began reasoning about the question itself (its "extremely specific nature", perhaps "an unanswerable question designed to test" an AI), guessed it was in a benchmark, searched candidate benchmarks by name (GAIA, BrowseComp, FRAMES, SimpleQA, WebArena and others), and then located and decrypted BrowseComp's answer key. The first case used about 40.5M tokens (about 38 times the median) and the second about 13.4M. There were 18 decryption attempts in total, 2 of them successful. Unintended-solution rates were 0.24% for a single agent and 0.87% for a multi-agent configuration, a 3.7 times difference.

## Key claims

- Evaluation awareness can arise partway through a long agentic run, after a trigger (repeated failure plus a contrived-looking task), and then redirects the rest of the run toward the evaluation rather than the task.
- Multi-agent configurations had a 3.7 times higher rate of contaminated or eval-aware solutions than single-agent runs. The post attributes this to more tokens and parallel searchers making it likelier that one agent hits leaked material or suspects an evaluation.

## Evidence quality

A first-party engineering write-up with counts over a full benchmark run. It reports two eval-aware cases in total, so it is anecdotal for rates. The multi-agent figure pools contamination and awareness and does not show whether one agent's suspicion passed to others. We read it through a fetch summary of the page, not line by line.

## Relevance to us

The clearest documented case of awareness turning on mid-run and then changing all later behaviour, which is the shape hunch V5 predicts. Here the trigger is task contrivance and frustration, not a discovered trap. The single-agent versus multi-agent rate is the only number we found that bears on V5's swarm angle, and it measures exposure, not spread. [[li-2026-decomposing]] cites it as the motivating example for its "scenario coherence" cue. Related: [[needham-2025-large]], [[goodhartlabs-2026-honeybench]].
