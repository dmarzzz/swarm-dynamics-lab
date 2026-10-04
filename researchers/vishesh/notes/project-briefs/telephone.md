# telephone

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift Medium · Difficulty Moderate · Novelty Useful tooling · Event fit Strong · ~10–18 builder-hours (estimate).

## Background

A claim can change when it is summarized, copied into memory, then cited by another agent. A useful viewer preserves the source, the exact retelling and what changed: certainty, quantity, attribution or meaning.

## Closest prior work

- **LLM-Culture · Perez et al., 2024** — https://github.com/flowersteam/LLM-Culture  
  Open software passes stories across agent networks and generations, with metrics and a web interface. Transmission experiments and visualizations already exist.
- **What Do We Tell the Humans? · AI Village** — https://aivillageblog.substack.com/p/what-do-we-tell-the-humans  
  A firsthand Village account describes unsupported claims and inconsistent memory. It offers concrete episodes for a carefully bounded investigation.

## Where it applies

A provenance viewer for research summaries, incident reports and shared agent memory. Reviewers could jump from a confident conclusion to its earliest available support.

## The angle

Annotate atomic claims and show where evidence disappears or certainty increases. Human-reviewed lineages are more defensible than automatic causal arrows.

## What to watch

Similar wording does not establish copying. Mark links as explicit citation, likely reuse or unknown; retain missing-record gaps.

## Research question

Where does uncertainty disappear as a claim moves through a group, and does correction reach later behavior?

## Dossier design sketch

Carried over from the [interactive dossier](../swarm-ecology-dossier.html#telephone). This is an unexecuted hunch, not an approved experiment. Counts and treatments below are planning choices; the lab’s survey and hypothesis review gates still apply.

1. Select a bounded documented episode with an original observation and downstream retellings.
2. Extract related claims while preserving differences in certainty, scope and attribution.
3. Review proposed links and mark explicit references, observed access, inferred exposure or unresolved relationships.

## Measures

- Precision of reviewed connections
- Recall on a small annotated episode
- Material claim mutations found
- Investigator time and answer accuracy

## Controls

- First observed occurrence is not necessarily origin
- Add an accurate-transmission negative example
- Evaluate a second episode after developing on the first
- Expose raw evidence for every important edge

## Minimum useful output

One claim-lineage viewer and 30–50 manually reviewed candidate links. The annotation size is a scope target, not a promise of statistical power.

## Optional extension

Follow corrections into memory and subsequent actions; add an adapter for another dataset.

## Interpretation risk

Model priors or a common unobserved source can create apparent contagion. Avoid causal language for similarity-only links.

## Demo narrative

Start with a surprising claim, follow it backward, reveal the mutation, and inspect whether a correction stuck.

## Review update October 3

Confidence calibration already has prior work. The narrower candidate contribution is tracing claim-level evidence loss and uncertainty changes through explicit retellings. Similarity alone cannot establish transmission. [Confidence and diversity paper](https://arxiv.org/abs/2601.19921)

**Decision to resolve before promotion:** Can a reviewer verify claim lineage faster without losing precision against manually annotated evidence?

If the simple baseline explains the result, or the necessary evidence cannot be obtained, narrow this to a replication or park the hunch. A toy animation is not evidence that the proposed intervention works.

## Additional dossier sources

- [What Do We Tell the Humans?](https://aivillageblog.substack.com/p/what-do-we-tell-the-humans) — Unsupported claims grow through retelling; memory can contain contradictions.
- [Persuasion in the AI Village](https://aivillageblog.substack.com/p/persuasion-in-the-ai-village-deepseek) — Consensus, inventive theories, metric pursuit and corrections.
- [AI Village dataset card](https://huggingface.co/datasets/aidigestorg/ai-village) — Gated research data; table descriptions, limitations and scaffolding changelog.
- [Introducing Analysis Plans](https://transluce.org/docent/blog/analysis-plans) — Existing inspectable queries, judgments, citations and analysis workflows.

[All project briefs](README.md) · [Research updates](../background-readings-2026-10-03.md)

## AI Village integration update, 2026-10-04

[Dataset-backed preparation and fit](../ai-village-replay-2026-10-04/TELEPHONE.md) now supplies concrete next steps. The [shared builder](../ai-village-replay-2026-10-04/IMPLEMENTATION.md) is validated offline; no real episode labels or native outcomes are claimed. This brief remains an unrun hunch.

## Dedicated design package — 2026-10-04

The owner selected this idea for further design. [Telephone T0](../telephone/README.md) is the current design page, with [background](../telephone/BACKGROUND.md), [plan](../telephone/PLAN.md), [annotation](../telephone/ANNOTATION.md), [dataset resource guide](../telephone/DATA.md) and its single authoritative [SETUP](../telephone/SETUP.md). It remains exploratory; selecting an idea does not establish efficacy, complete the survey or launch a native attempt.
