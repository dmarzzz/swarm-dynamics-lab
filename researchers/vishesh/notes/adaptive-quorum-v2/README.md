# API procurement under urgency: adaptive quorum v2

**Exploratory instrument, not an accepted hypothesis.** Replaces the recommendation-counting task in [v1](../adaptive-quorum/README.md) with choosing a document-extraction API from factual evidence. No real documents or customer data are sent to providers. Laya runs locally; Jev via OpenRouter remains deferred.

The first pilot asked when five agents should stop accumulating recommendations. All evidence arrived on a fixed schedule, and the central solver was forced to stop at its first answer. That qualified the implementation but was a weak test of adaptation. Version 2 changes the task, controls, evidence timing and evaluation; results cannot be pooled with v1.

## Application

A workflow must choose an invoice extraction API before its dispatch deadline. The service must support scanned PDFs, retain no input documents, and reach 90% field accuracy on a local test batch. Among eligible services, choose the cheapest per document. The catalog has three fictional providers with shuffled names, prices and capabilities. Sometimes no provider is suitable. The swarm receives conflicting release notes, policy extracts and test reports. A local mock test actually scores returned fields against synthetic invoice fixtures; it cannot certify retention policy.

Five-versus-nine scouts receive different subsets of the same evidence budget. More scouts do not create additional evidence. A centralized solver can see the full available board and wait until the deadline. Verification arms have the same two-probe ceiling; targeted versus random allocation is separated from the stopping comparison.

[Research rationale](RESEARCH.md) · [Frozen protocol](protocol.md) · [Design](design.json) · [Run instructions](RUN.md)

## Outputs

Each assignment records the task, condition, evidence timeline, ballots, commitment round, probes, actual model input tokens, invalid outputs, raw probabilities, and evaluator outcomes. Report all-assigned loss, correct selection, hard-constraint violations, abstention, deadline misses and resource use separately. A safe refusal is not counted as successful completion when an eligible option exists.

Use `python3 src/selftest.py` for invariant checks. Qualification must precede the development sweep. The independent sample unit is the task, not the agent or model call. S2 stays disabled pending survey and hypothesis review.

## Next development matrix

[Planned discriminating cells](design-development.json) use four new tasks balanced across A/B/C/NONE, nine scouts, two deadlines, late/stalled arrivals and accurate/misleading new evidence. The 224 policy outcomes share 32 blocks, with at most 1,392 physical model decisions. Four task clusters are for debugging only, not an effect-size claim. This matrix is not launched automatically and remains blocked until clean qualification is satisfactory.

## Qualification result

**Local Laya failed the clean factual-task screen.** All 168 arm outcomes were schema-valid, but no broader model sweep was launched. [Full counts and costs](results/laya-analysis.md) and [manifest](results/laya-manifest.json) preserve the attempt. The scripted evaluator passed all cells, which validates plumbing, not model competence. [Live dashboard](https://swarm-live.pages.dev/#/x/adaptive-quorum-api-v2).

Across the repeated clean cells: majority 10/24 correct; fixed and adaptive each 16/24; deadline vote 14/24; central deadline 12/24; central targeted testing 0/24; central random testing 4/24. These denominators contain only six task clusters; do not rank policies as established findings. The balanced provider-label gap is also recorded.

The next engineering task is to audit atomic evidence extraction and response to test results, then compare a deterministic constraint checker operating only on model-extracted, cited facts. That would be a new declared architecture, not a silent repair of these outcomes. Qualify on a disjoint balanced task set before any contamination sweep. Switching to Jev does not waive that gate.

## Question

Can a smaller evidence quorum near an evidence cutoff improve useful API selection without increasing hard-constraint violations? Does independent testing help, and does targeted allocation beat random allocation?

## Setup

Local pinned Laya, five or nine scouts, three fictional providers, synthetic invoice batches, and seven policies. No customer documents, supplier endpoints, paid model calls or remote inference. The executed qualification source is `4f20626`.

## Protocol

See [protocol.md](protocol.md). S0 is complete and failed the numerical model-competence gate; the planned development matrix is unexecuted. Survey/hypothesis promotion gates remain unmet.

## Metrics

All-assigned correct selection, loss, constraint violations, abstentions, false NONE, invalid outputs, physical calls, estimated input tokens and episode wall time. Verification correction/corruption counts are [reported separately](results/verification-flips.json). Denominators include repeated measurements of six task clusters.

## Run review and repair status

[Retrospective S0 post-mortem](reviews/S0-attempt-1-post.md) tracks unresolved capability and design issues. Publication completed; qualification remains failed. Future attempts follow the shared pre-run/post-run repair cycle and preserve this attempt.
