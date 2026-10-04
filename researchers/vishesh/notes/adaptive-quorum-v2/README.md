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
