---
id: saucier-2026-content
type: paper
title: "Content camouflage: How diversified posting patterns influence human detection of AI-enabled social bots"
authors: [Camille J. Saucier, Darren L. Linvill, Amarachi H. Okoronkwo, Gayatri Tatineni, Aybuke Sezgin, Morgan Wack]
year: 2026
venue: Computers in Human Behavior, vol. 177, article 108881 (April 2026); SSRN preprint 2025
url: https://experts.umn.edu/en/publications/content-camouflage-how-diversified-posting-patterns-influence-hum/
doi: 10.1016/j.chb.2025.108881
arxiv: null
cite: "Saucier, C. J., Linvill, D. L., Okoronkwo, A. H., Tatineni, G., Sezgin, A., & Wack, M. (2026). Content camouflage: How diversified posting patterns influence human detection of AI-enabled social bots. Computers in Human Behavior, 177, 108881. https://doi.org/10.1016/j.chb.2025.108881 (SSRN preprint doi:10.2139/ssrn.5492309)"
topics: [swarm-detection]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null  # Semantic Scholar rate-limited at access time
code: []
---

## Summary

Two experiments on whether "content camouflage," mixing political posts with non-political material, changes humans' ability to spot AI-enabled social bots. The stimulus profiles were modelled on real bot accounts from the 2024 US election that used sports content to mask political messaging. Experiment 1 (N = 565 undergraduates) and Experiment 2 (N = 601 adults) compared reactions to profiles posting political-only content against mixed political-and-sports content. In both samples, diversification did not directly change bot-detection accuracy, but it reliably raised perceived trustworthiness, and higher trustworthiness in turn made participants more likely to classify the account as human; in the adult sample this trustworthiness pathway was moderated by political ideology. The authors frame this as a heuristic-cue credibility mechanism that AI-generated bots exploit, and call for interventions that account for strategic content blending. Only the abstract was read (the SSRN page and publisher page were blocked; abstract taken from the University of Minnesota experts page), so experimental details, effect sizes and the ideology interaction are not captured here.

## Contribution

Isolates one evasion tactic observed in the wild and shows experimentally that it works on humans through trust rather than through detection accuracy per se.

## Key results

- Two experiments, N = 565 (undergraduates) and N = 601 (adults).
- No direct effect of content diversification on bot-detection accuracy.
- Reliable indirect effect: diversification raises perceived trustworthiness, which raises "human" classification.
- Ideology moderates the trust pathway in adults.

## Methods and models

Between-subjects experiments with constructed social media profiles based on real 2024 election bot accounts; outcome measures of perceived trustworthiness and human-versus-bot classification; mediation analysis with moderation by political ideology (inferred from abstract).

## Limitations and open questions

Abstract-only read. Human judges, not algorithmic detectors; single camouflage tactic (sports content); US political context; unclear how profiles were presented (static screenshots versus interactive). Does not address coordinated populations of accounts.

## Relevance to us

Evidence that content-level camouflage defeats human heuristic detection by shifting trust, which supports the direction in [[guo-2026-text]] and [[lloyd-2025-there]] that behavioural and relational signals, not content plausibility, must carry the load against LLM-enabled bots. For swarm-detection it is a reminder that an agent population can trivially diversify content, so population-level signatures (timing, coordination structure, shared infrastructure) are the durable detection channel. Pre-LLM baseline for bot behaviour in political discourse: [[li-2024-social]].
