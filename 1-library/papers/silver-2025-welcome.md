---
id: silver-2025-welcome
type: paper
title: Welcome to the Era of Experience
authors: [David Silver, Richard S. Sutton]
year: 2025
venue: Preprint of a chapter in the book Designing an Intelligence (MIT Press)
url: https://storage.googleapis.com/deepmind-media/Era-of-Experience%20/The%20Era%20of%20Experience%20Paper.pdf
doi: null
arxiv: null
cite: Silver, D., & Sutton, R. S. (2025). Welcome to the Era of Experience. Preprint of a chapter to appear in Designing an Intelligence, MIT Press. Google DeepMind.
topics: [fork-merge-security, meta]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

A position chapter arguing that AI will move from an era of human data to an era of experience, in which agents learn predominantly from data they generate by acting. Agents will "inhabit streams of experience" lasting months or years, act autonomously through rich actions and observations, take rewards grounded in the environment, and plan and reason about experience rather than in human terms. The chapter cites AlphaProof as an early example. Its Consequences section names risks: fewer opportunities for humans to intervene in long autonomous runs and harder interpretability once agents move away from human modes of thought. It names three claimed safety benefits: adaptation to a changing environment, reward functions corrected over time by bilevel optimisation, and the natural brake of real-world experiment time.

## Contribution

States the Silver and Sutton research programme in which the knowledge an agent gains lives in its continually updated weights, which is the regime where Sutton's fork-merge question in [[sutton-2025-father]] arises.

## Key results

- No experiments of its own; it is a position paper.
- It does not discuss spawning copies, merging experience across instances, or adversaries corrupting an agent's experience stream (checked by searching the full text for copy, merge, parallel and instances).

## Methods and models

Argument by example (AlphaZero, AlphaProof, DeepSeek-R1) and reference to reinforcement-learning concepts: value functions, world models, bilevel reward optimisation.

## Limitations and open questions

The safety section is short and considers misuse and loss of oversight, not adversarial manipulation of what the agent experiences. Reward correction "based upon indications of human concern" assumes the signal is not itself corrupted.

## Relevance to us

Background for all three questions. If experience goes into weights continually, then a forked copy that explores a hostile domain returns as a weight delta or a distilled policy, not as a report, so Q3 attacks are closer to data poisoning and model-merge backdoors than to prompt injection. The chapter's own listed safety benefit (reward adapted by experience) is also an attack surface: a child whose reward has been reshaped by its environment carries that reshaping back. Read alongside [[sutton-2025-father]] and [[sutton-2022-alberta]].
