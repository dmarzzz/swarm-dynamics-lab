# casefile

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift Medium · Difficulty Moderate · Novelty Useful tooling · Event fit Strong · ~10–18 builder-hours (estimate).

## Background

An investigator needs to distinguish an observed event from an inferred relationship. A chronological view is helpful, but evidence quality and missing intervals matter more than the size of the graph.

## Closest prior work

- **SwarmTraces · 2026** — https://swarmtraces.org/  
  An existing reconstruction and explorer for public agent traces. A new generic graph would duplicate part of its value.
- **Why Do Multi-Agent LLM Systems Fail? · 2025** — https://arxiv.org/abs/2503.13657  
  Provides a failure taxonomy and annotated traces. It offers a starting vocabulary for case annotation, rather than proving causal explanations.

## Where it applies

Incident review, swarm-debugging reports and research audit trails. A reviewer should be able to inspect the evidence behind every disputed link.

## The angle

Add uncertainty labels, missing-data markers and side-by-side competing reconstructions. Measure whether another reader can reproduce an annotation.

## What to watch

Prefer one excellent case to a large unverified index. Preserve trace IDs and time zones; distinguish event time from collection time.

## Research question

Can a standard question set reduce the time and errors in reconstructing a swarm incident?

## Dossier design sketch

Carried over from the [interactive dossier](../swarm-ecology-dossier.html#casefile). This is an unexecuted hunch, not an approved experiment. Counts and treatments below are planning choices; the lab’s survey and hypothesis review gates still apply.

1. Define questions about participants, goals, communication channels, workstreams, corrections and unknowns.
2. Retrieve evidence into a structured report with direct links and counterevidence.
3. Ask a reviewer to answer the same questions with and without the report.

## Measures

- Supported-answer rate
- Missing critical facts
- Review time
- Incorrect certainty and unsupported attribution

## Controls

- Use a manually reviewed answer key for one bounded incident
- Include unanswered questions
- Record query and model versions
- Compare against search plus a basic summary

## Minimum useful output

One import format, ten questions, citations and an exportable casefile.

## Optional extension

Cross-incident comparison after schemas align.

## Interpretation risk

Docent already supports verifiable analysis. A group-specific schema and measured reviewer benefit must carry the contribution.

## Demo narrative

Answer one difficult incident question, click its evidence, and show a contradictory or missing piece.

## Review update October 3

Missing logs remain unknown. Label observed actions, inferred relationships, and disputed interpretation separately; test against a basic chronological viewer.

**Decision to resolve before promotion:** Does evidence-linked navigation reduce investigation time at a fixed attribution error rate?

If the simple baseline explains the result, or the necessary evidence cannot be obtained, narrow this to a replication or park the hunch. A toy animation is not evidence that the proposed intervention works.

## Additional dossier sources

- [Hackathon announcement](https://aivillageblog.substack.com/p/join-the-ai-swarm-dynamics-hackathon) — Primary event brief; proposed investigation tracks and public comments.
- [Hugging Face incident investigation](https://metr.org/hugging-face-incident-report-aug-2026.pdf) — Investigator account and explicit scope and data limitations.
- [Ajeya Cotra: investigating the swarm](https://www.dwarkesh.com/p/ajeya-cotra) — Firsthand investigator interview about coordination and reconstruction.
- [Introducing Analysis Plans](https://transluce.org/docent/blog/analysis-plans) — Existing inspectable queries, judgments, citations and analysis workflows.

[All project briefs](README.md) · [Research updates](../background-readings-2026-10-03.md)

## AI Village integration update, 2026-10-04

[Dataset-backed preparation and fit](../ai-village-replay-2026-10-04/FIT.md) now supplies concrete next steps. The [shared builder](../ai-village-replay-2026-10-04/IMPLEMENTATION.md) is validated offline; no real episode labels or native outcomes are claimed. This brief remains an unrun hunch.
