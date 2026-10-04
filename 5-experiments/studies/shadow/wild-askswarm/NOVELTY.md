# Novelty and measurement boundary

Checked 2026-10-04 before interpreting results. This is an exploratory tool demonstration,
not a hypothesis submitted around the repository's survey/review gates.

## Closest work actually inspected

1. [[de-marzo-2026-copying]], De Marzo, Alboré and Garcia, arXiv 2609.09150.
   Opened https://arxiv.org/abs/2609.09150 (abstract and metadata), and read the local library
   entry. The abstract explicitly studies where agents write, what they name themselves,
   and their wording; frequency-dependent copying explains the three. We do not claim
   discovery of wiki copying, first-writer effects or wording adoption. We do not reproduce
   that paper's exposure reconstruction or fitted copying models. Our full revision census
   is not its filtered 1,201-handle, 5,929-edit population.
2. [[gh-kmad-agent-swarm-forensics]], opened https://github.com/kmad/agent-swarm-forensics
   (README, including results and caveats). Already reports a failover protocol in 44
   revisions by 35 labels over 99 minutes: 3 revisions introduce the provider name and 41
   inherit it. This directly precedes any claim about protocol adoption. The distinction
   between inherited snapshot text and an editor introducing text is especially important.
   AskSwarm's snapshot clusters do **not** resolve it. The source also reports a verified
   UTF-8/Latin-1 export-layer issue in 250 wiki bodies; our adapter uses the supplied text
   unchanged, followed by documented Unicode normalization, not a byte reconstruction.
3. [[collusion-wiki-2026-discovery]] and [[swarmtraces-2026-revealing]], read the local
   library entries. The former already establishes the public coordination channel; the
   latter already reconstructs attack payload chains and explicitly discusses redactions.
   Our local schema census is a coverage check, not a new incident or attribution claim.
4. [[aidigest-2025-season]], read the local library entry. Village collaboration and failure
   narratives are prior work, not our outcomes. This lane does not analyze village data or
   reassert its persuasion/cascade stories as new.

## What is added

A reusable, deterministic measurement interface that runs without model calls, adapters for
three heterogeneous sources, explicit denominators and missingness, tests against synthetic
edge cases, and the self-application to swarm-lab's own git/task history. The honest headline
is portability **with visible limits**, not a matched cross-swarm causal comparison.

## What remains unvalidated

- Clusters approximate lexical resemblance, not idea units. No human semantic gold set.
- Snapshot inheritance, common tool output, response decoding and commit boilerplate can all
  look like cross-identity adoption. First observed occurrence does not establish source.
- Self-chosen labels, shared labels, operator identity and model identity are not equivalent.
  We do not exclude purported humans without an independently checked rule.
- Clock precision differs; source clock uncertainty is retained in wiki Event metadata but
  not propagated into time-to-k intervals. Exact ties are retained and receive no causal order.
- Administrative first-use/reuse rankings are not productivity, quality or social power.
- Threshold sensitivity is descriptive. At threshold .5 the fixed LSH configuration has
  lower theoretical candidate recall than at .7; a threshold sweep is not a recall audit.
- Input corpora are selected, overlapping/dependent artifacts, not random independent
  samples. No claim of population uncertainty from naive record-wise confidence intervals.
