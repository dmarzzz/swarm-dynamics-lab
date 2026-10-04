---
id: sotala-2019-subagents
type: blog
title: "Subagents, neural Turing machines, thought selection, and blindspots"
authors: ["Kaj Sotala"]
year: 2019
url: https://www.lesswrong.com/posts/7zQPYQB5EeaqLrhBh/subagents-neural-turing-machines-thought-selection-and
site: LessWrong
topics: [fork-merge-security, collective-decision]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 1
---

## Summary

Curated 2019 post (87 points, 3 comments) in Sotala's Multiagent Models of Mind sequence, building a mechanistic picture of how sub-agents compete to set the contents of consciousness. It starts from sequential sampling models in mathematical psychology, specifically the drift diffusion model (four parameters: decision threshold, starting-point bias, drift rate, non-decision time) which fits a wide range of reaction-time experiments and has neural correlates in MT/V5 and LIP firing rates (citing Forstmann et al. 2016, Ratcliff et al. 2016, Shadlen and Shohamy 2016). Shadlen and Shohamy's extension to value-based choice has evidence accumulated by retrieving memories through a limited number of "pipes", which is why subjective decisions take time. Sotala then lays out Dehaene's model (Zylberberg et al. 2011; Dehaene and Sigman 2012) of consciousness as a production system or virtual Turing machine: contents of working memory activate competing production rules held by different neuron groups, the first to cross threshold fires and rewrites working memory, and this is applied one level down from action selection to selecting which thoughts to think. In his framing each production rule is a sub-agent voting to modify consciousness, which connects back to his Internal Family Systems toy model. The remainder (emotion suppression, internal conflict, blind spots as rules that suppress certain content) was not read in this pass.

## Key claims

- Decision-making is well described by threshold-crossing evidence accumulators, with measurable parameters and neural correlates.
- Consciousness can be modelled as a production system where sub-agents are competing rules and the winner edits shared working memory.
- The same accumulate-and-threshold mechanism plausibly selects thoughts, not just actions.

## Evidence quality

Literature synthesis with real citations to the psychology and neuroscience of sequential sampling and to Dehaene's published model; the sub-agent interpretation is the author's gloss on top. No new data.

## Relevance to us

Background. The shared-working-memory-edited-by-whichever-rule-fires-first architecture is a concrete model of a multi-agent system with a single mutable shared state, which is the setting where one corrupted sub-agent can rewrite what every other sub-agent sees. That is the fork-merge-security memory-hijack concern in a cognitive-science costume. The DDM's threshold parameter is also a tidy analogue of a merge threshold. Low priority as a citation.
