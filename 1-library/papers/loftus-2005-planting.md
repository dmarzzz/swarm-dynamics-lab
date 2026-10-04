---
id: loftus-2005-planting
type: paper
title: "Planting misinformation in the human mind: A 30-year investigation of the malleability of memory"
authors: [Elizabeth F. Loftus]
year: 2005
venue: Learning & Memory
url: https://labs.wsu.edu/attention-perception-performance/documents/2016/05/learn-mem-2005-loftus-361-6.pdf/
doi: 10.1101/lm.94705
arxiv: null
cite: "Loftus, E. F. (2005). Planting misinformation in the human mind: A 30-year investigation of the malleability of memory. Learning & Memory, 12(4), 361–366."
topics: [fork-merge-security, collective-decision]
added_by: dmarz/fm
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: 1047  # Crossref is-referenced-by-count, 2026-10-03
code: []
---

## Summary

A short review (read in full from a mirror of the publisher PDF) of three decades of work on the misinformation effect: the impairment of memory for an event after exposure to misleading post-event information. The standard design has three stages: witness an event, receive misleading information about it, then recall the event. In the Okado and Stark (2005) neuroimaging study it opens with, misinformation was remembered as part of the original event about 47% of the time. Across studies using the "lost-in-the-mall" procedure (a false childhood event narrated as if supplied by relatives), an average of about 30% of subjects produced a partial or complete false memory. A single fake advertisement placing Bugs Bunny at a Disney resort led 16% of subjects to later claim they had met him there, which is impossible. The review covers when people are susceptible, whether warnings help, who is most susceptible, what happens to the original trace, and what false memories are like.

## Contribution

Consolidates the behavioural evidence that a memory store can be rewritten from outside by information delivered after the event, and that the rewritten memory is held with confidence and detail. It names the Discrepancy Detection principle as the main moderator.

## Key results

- Misinformation is most effective when the original memory has faded, because a discrepancy is then less likely to be noticed (Discrepancy Detection principle, Tousignant et al. 1986). People sometimes accept misinformation even after noticing a discrepancy, by deferring to the new source.
- Warnings given before the misinformation help. Warnings given after it mostly do not; an immediate post-misinformation warning worked only when the misinformation had low accessibility, and failed when it had been presented several times. General and item-specific warnings did not differ (Eakin et al. 2003).
- Temporary states (believing one drank alcohol, hypnosis) increase susceptibility. Young children and the elderly are more susceptible; dissociation scores explain about 10% of the variance in susceptibility.
- The effect is found in three-month-old infants, gorillas, pigeons and rats. In pigeons, misinformation biases toward a specific wrong answer and is stronger when given later in the retention interval, so it is not plain retrograde interference.
- On the fate of the original memory, McCloskey and Zaragoza (1985) argued that the original trace is untouched; later analyses (Ayers and Reder 1998) found small effects even on their modified test. The review concludes that reports of misinformation arise from three routes: no original trace, deliberate deference, and apparent impairment of the original.
- Zaragoza and Lane (1994) found that misled subjects sometimes come to remember seeing what was only suggested (source misattribution), but this is not inevitable.
- Single memory reports cannot be reliably classified as true or false from their content or, as of 2005, from neural signals.

## Methods and models

Narrative review of human and animal experiments. Paradigms: three-stage misinformation design, modified test, source-monitoring test, familial informant false narrative ("lost in the mall"), fake advertisements, neuroimaging.

## Limitations and open questions

A review, not a meta-analysis; percentages are quoted from individual studies or reviews (the 30% figure is from Lindsay et al. 2004). Most neuroimaging work used simple word or picture lists. The author is the field's leading proponent, and the debate on trace impairment versus retrieval competition is summarised rather than settled.

## Relevance to us

Bears on Q3 more closely than prompt-injection framing does. dmarz's attack, in which a sub-agent's memory is overwritten so that it sincerely becomes the attacker's agent and then carries that state home, is the misinformation effect applied to an artificial memory. The human literature gives three measured regularities that transfer as hypotheses, not facts. First, the attack works best when the agent's own record of the original event is weak; for an LLM agent that corresponds to memory lost through compaction, which [[zerhoudi-2026-compaction]] measures (about half of safety constraints survive one round). Second, post-hoc warnings fail once misinformation is accessible, which predicts that a parent's merge-time "are you compromised?" check will not undo an accepted rewrite. Third, rewritten memories are reported with confidence and cannot be classified one at a time, which is an argument for Q2: compare several independently gathered reports rather than inspect one. The "updating is also correction" point in the conclusion is the core tension for any merge rule. Related mechanisms: source confusion [[johnson-1993-source]], retrieval-triggered rewriting [[nader-2000-fear]], and the summariser-as-confused-deputy result [[liu-2026-safe]].
