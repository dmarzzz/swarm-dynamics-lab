---
id: heuer-1999-psychology
type: paper
title: "Psychology of Intelligence Analysis"
authors: [Richards J. Heuer Jr.]
year: 1999
venue: Center for the Study of Intelligence, Central Intelligence Agency (book)
url: https://www.cia.gov/resources/csi/static/Pyschology-of-Intelligence-Analysis.pdf
doi: null
arxiv: null
cite: "Heuer, R. J., Jr. (1999). Psychology of Intelligence Analysis. Washington, DC: Center for the Study of Intelligence, Central Intelligence Agency. ISBN 1-929667-00-0."
topics: [fork-merge-security, collective-decision]
added_by: dmarz/fm
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

A CIA book (about 67,000 words; chapters first published as articles between 1978 and 1986) that applies cognitive psychology to intelligence analysis. I read the table of contents, the introduction on denial and deception, Chapter 8 (Analysis of Competing Hypotheses, steps 1-3) and Chapter 10 (Biases in Evaluation of Evidence) in full, and skimmed Chapter 4. Chapter 10 argues that analysts are oversensitive to the consistency of evidence and insufficiently sensitive to its reliability, ignore missing evidence, treat uncertain reports as fully true or fully false, are not moved by caveats about a source's possible manipulation, and keep impressions after the evidence for them is discredited. Chapter 8 sets out Analysis of Competing Hypotheses (ACH): list all hypotheses, including deception, score each item of evidence for how well it discriminates between them, and try to disprove rather than confirm.

## Contribution

The standard text, inside the US intelligence community, linking known cognitive biases to the evaluation of reports from sources that may be under hostile control, with a concrete counter-procedure (ACH).

## Key results

- Consistency can mislead: "Information may be consistent only because it is highly correlated or redundant, in which case many related reports may be no more informative than a single report." Confidence from a small consistent sample "should be low regardless of the consistency of the information."
- Absence of evidence is under-weighted: in the Fischhoff, Slovic and Lichtenstein fault-tree study cited, mechanics shown a tree with three of seven branches removed raised "other problems" only half as much as they should have; non-mechanics did worse.
- Caveats do not attenuate: "Knowing that the information comes from an uncontrolled source who may be trying to manipulate us does not necessarily reduce the impact of the information."
- Perseverance: impressions survive full discrediting of their evidence (debriefing studies by Ross, Lepper and colleagues). Heuer applies this to learning that "a clandestine source who has been providing information for some time is actually under hostile control": analysts rationalise keeping the impressions.
- Best-guess strategy: analysts treat 70-80% reliable reports as 100% true; chained uncertain inferences should multiply (75% x 75% = 56%) but intuitive judgments do not.
- ACH rule on deception: do not reject the deception hypothesis for lack of evidence, because well-executed deception leaves little; keep it until disproved.

## Methods and models

Synthesis of experimental psychology (Tversky and Kahneman, Ross, Fischhoff and others) with the author's experience in the CIA Directorate of Operations and Intelligence; a few replications with military officers at the Naval Postgraduate School are mentioned. Not an empirical study itself.

## Limitations and open questions

Most cited experiments are 1970s laboratory studies; some have since been contested. ACH itself was not validated in this book, and later work questioned its benefits; I did not read that literature. Chapters 11-14 were not read.

## Relevance to us

For Q2 it states the independence condition that BFT thresholds silently need: correlated or redundant reports are worth one report, so k-of-n agreement among children that shared a source, a prompt, or a captor is not k confirmations. A fork-merge parent should weight agreement by independence of the paths that produced it, as the double-agent history in [[cowden-2014-pioneering]] shows the hard way. For Q3, the perseverance result predicts that once a corrupted child's report has been merged, learning later that the child was compromised will not cleanly undo its effect, which matches the post-warning failures in [[loftus-2005-planting]]; the agent-side implication is that merges must be reversible by construction (versioned, replayable patches as in [[loven-2026-meld]]) rather than relying on the parent to "forget". The ACH stance (keep "this child was turned" as a live hypothesis until disproved) is a merge-time procedure a parent agent could run explicitly. Related: [[kelly-2025-effect]], [[johnson-1993-source]].
