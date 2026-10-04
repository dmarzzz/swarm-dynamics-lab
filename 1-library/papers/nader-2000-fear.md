---
id: nader-2000-fear
type: paper
title: "Fear memories require protein synthesis in the amygdala for reconsolidation after retrieval"
authors: [Karim Nader, Glenn E. Schafe, Joseph E. LeDoux]
year: 2000
venue: Nature
url: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=10963596&rettype=abstract&retmode=text
doi: 10.1038/35021052
arxiv: null
cite: "Nader, K., Schafe, G. E., & LeDoux, J. E. (2000). Fear memories require protein synthesis in the amygdala for reconsolidation after retrieval. Nature, 406(6797), 722–726."
topics: [fork-merge-security]
added_by: dmarz/fm
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

A rat fear-conditioning study (read from the PubMed abstract only) showing that a consolidated memory becomes unstable again when it is retrieved. The protein synthesis inhibitor anisomycin was infused into the lateral and basal amygdala, the presumed storage site for conditioned fear. Infusion shortly after a reactivation trial produced amnesia on later tests, whether the reactivation came 1 or 14 days after conditioning. The same infusion without reactivation left the memory intact, and infusion delayed to six hours after reactivation produced no amnesia. The authors conclude that a reactivated memory returns to a labile state and must be "reconsolidated" through new protein synthesis.

## Contribution

Revived and established the reconsolidation hypothesis: memories are not fixed once consolidated, and each retrieval opens a time-limited window in which the stored trace can be disrupted (and, by later work, modified). The abstract states the result is "not predicted by traditional theories of memory consolidation".

## Key results

- Post-reactivation anisomycin caused amnesia at both 1-day-old and 14-day-old memories (measured).
- No amnesia without reactivation, and none when the infusion was delayed six hours after reactivation (measured).
- Interpretation that retrieval itself makes the trace labile (the authors' inference from the pattern).

## Methods and models

Auditory fear conditioning in rats; intra-amygdala infusion of anisomycin after a reactivation (retrieval) trial; freezing measured at later tests. Details beyond the abstract not checked.

## Limitations and open questions

Read at abstract depth; group sizes, effect sizes and controls not checked. The result concerns disruption of a fear memory by a drug in rodents, not the insertion of new content; that the reopened window also admits new information comes from later work in humans and is not in this paper. Boundary conditions on reconsolidation (memory age, strength) were debated in later literature I did not open.

## Relevance to us

A biological precedent for a specific Q3 timing claim: a memory is most open to rewriting at the moment it is recalled, not while it sits unused. For an LLM agent the analogue is that a stored belief is re-read into context, reasoned over and written back (summarised, compacted, merged); that read-modify-write step is where an attacker's content can be fused into the old record, which is the mechanism [[liu-2026-safe]] measures at the compression boundary and [[zerhoudi-2026-compaction]] measures as constraint loss. For the merge itself, the parent's act of reading a returning child's memory to integrate it is a reactivation of its own related memories, so the parent's records are in their most rewritable state exactly when the possibly corrupted child is speaking. A defence implied by the analogy (not tested anywhere I found) is to integrate a child's report against a frozen, read-only snapshot of the parent's memory rather than the live store. Related: [[loftus-2005-planting]], [[johnson-1993-source]].
