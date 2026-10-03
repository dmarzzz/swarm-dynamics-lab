---
id: bosch-2026-biased
type: paper
title: 'Biased decisions of Large Language Models (LLM): Computer control agents and the decoy effect'
authors:
- Kevin Bösch
year: 2026
venue: Journal of Behavioral and Experimental Economics 124
url: https://ideas.repec.org/a/eee/soceco/v124y2026ics221480432600131x.html
doi: 10.1016/j.socec.2026.102641
arxiv: null
cite: 'Bösch, K. (2026). Biased decisions of Large Language Models (LLM): Computer control agents and the decoy effect. Journal of Behavioral and Experimental Economics, 124, 102641. https://doi.org/10.1016/j.socec.2026.102641'
topics:
- llm-agent-swarms
added_by: vishesh/senku-1
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: '1 (Semantic Scholar, 2026-10-03); Crossref is-referenced-by-count 0 the same day'
code: []
---

## Summary

The study asks whether the decoy effect, where adding a clearly inferior third option shifts human preference toward one of the two real options, also appears when LLMs act rather than write. It runs 3600 simulations across five canonical decision scenarios with six state-of-the-art LLMs, driving them through the open-source browser-use framework so the measured output is an action taken in a browser rather than generated text. The abstract reports an aggregate effect: the target option is selected 43.4% of the time when a decoy is present against 38.0% when it is absent, p < .001. The effect's size and direction vary by model, and the abstract states that some models display no significant bias. The author frames the implications for digital nudging, system design, and using LLMs as stand-ins for human subjects in behavioural research.

## Contribution

It extends evidence of human-style choice heuristics in LLMs from text outputs to autonomous actions, which is the behaviour that matters once a model is wired to a computer-control loop.

## Key results

- Measured: target selected 43.4% with a decoy present against 38.0% with no decoy, p < .001, aggregated over all runs.
- Measured: 3600 simulations, five canonical decision scenarios, six state-of-the-art LLMs, executed through browser-use.
- Stated: effect magnitude and direction differ across models, with some showing no significant bias. Per-model numbers are in the full text, which could not be loaded.
- Crossref records volume 124, article 102641, published print September 2026, licensed CC BY 4.0, 68 references.

## Methods and models

Computer control agents driven by the open-source browser-use framework, choosing among options presented in a browser, with and without a decoy alternative, over five classic decoy-effect scenarios. Which six models were used, the per-scenario breakdown, the per-model effect sizes and the statistical tests beyond the aggregate p-value are in the full article and are not recorded here because the publisher page was not reachable.

## Limitations and open questions

Noticed here: this is a single-agent study. It measures one agent's choice bias, not a collective's, so any extension to groups is an inference and not something the paper tests. The aggregate gap is 5.4 percentage points, which is modest and is pooled across models that the author says differ in direction, so the aggregate may be averaging over opposed effects. Whatever limitations the author states are in the full text and could not be read.

## Relevance to us

If an attacker or designer wants to move a collective's choice without touching any agent's prompt, the decoy effect is the cheapest lever available: it changes only the option set. This paper gives the single-agent effect size to beat, 43.4% against 38.0%, and a concrete harness (browser-use with five canonical scenarios) that a hackathon project can lift and rerun with several agents deliberating instead of one deciding alone. The obvious experiment it sets up is whether the effect amplifies, cancels or inverts under group deliberation, which is directly the question of whether an individual-level preference signal predicts a collective outcome. Its measured model-dependence is also a warning for us: a swarm of heterogeneous models may respond to the same decoy in opposite directions, which would show up as noise unless reported per model. Pairs with the preference-manipulation attacks in [[nestaas-2024-adversarial]], which manipulate the option set from the content side, and with the conformity work in [[weng-2025-do]] and [[cho-2025-herd]] for what happens to an individual bias once agents observe each other.

## Access note

The publisher page at sciencedirect.com returned HTTP 403 on both the abstract and full-text paths, as did the DOI resolver's Elsevier redirect and the SSRN preprint page. Title, sole author, journal, volume, article number, DOI, year and the full abstract above were read from the RePEc/IDEAS record listed in `url`, and the volume, page, publication date, licence and reference count were confirmed against the Crossref record for the DOI. No part of the full text was read, hence `read_depth: abstract`. Anyone with publisher access should fill in the per-model results and the author's own limitations under a notes heading.
