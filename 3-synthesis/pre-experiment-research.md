# Research prerequisites for choosing swarm experiments

Owner: dmarz/preflight, holding `synthesis-pre-experiment-research`. Written 2026-10-03.

This is a bounded research synthesis, not a gate-passed survey, accepted hypothesis, or experimental result. It connects the team's existing quorum, memory, regrowth, external-influence, Sybil, detection and fork-merge work. The recommended next focus is **decisions and repair under incomplete evidence lineage**, with causal identification and attention accounting as shared requirements. This recommendation is an inference from the comparisons below, not a demonstrated novelty claim.

The research pass added eight missing source records after deduplication, inspected primary methods and limitations, and checked two associated repository READMEs. No models, attacks or experiments were run. The [search and evidence log](../researchers/dmarz/notes/preflight-evidence-log.md) records scope, access limitations and the self-audit.

## What the existing work already covers

The team's [quorum brief](../researchers/vishesh/notes/project-briefs/quorum.md) already distinguishes repeated messages from independent observations. The [memory brief](../researchers/vishesh/notes/project-briefs/memory.md) asks whether corrections survive retrieval and summaries. [Regrowth](../researchers/vishesh/notes/project-briefs/regrowth.md) separates restored connectivity from recovered knowledge. [External influence](../researchers/vishesh/notes/agent-swarm-influence-research.md) distinguishes direct exposure from peer propagation. These are starting points, not new proposals from this pass.

The [Sybil synthesis](sybil-flashbots.md), [fork-merge synthesis](fork-merge-questions.md) and [detection taxonomy](swarm-detection-methods.md) supply the security and measurement context. Their absence claims remain bounded by their searches. In particular, a recent counterexample can invalidate a broad statement that nobody studies agent-memory correction without settling the narrower fork-and-merge question.

## Evidence lineage and admission

Database provenance already offers a compositional representation of derivations under specified operators. It does not recover hidden semantic dependencies inside a model. [[green-2007-provenance]] MemLineage provides a closer agent-specific predecessor: trust propagation follows attributed derivation edges, and sensitive-action enforcement depends on that attribution. [[ouyang-2026-memlineage]]

CPB is an especially close overlap with the quorum brief. Its live instrument supplies authored input lineage but relies on declarations for generated derivations. Its tested policies do not exercise the store's correction operations. [[li-2026-benchmark]] This rules out treating duplicate-aware shared-memory admission as an untouched area.

**Research implication, inferred:** distinguish three settings before selecting a project: lineage supplied by the environment, lineage recorded by the runtime, and lineage inferred from text. A result in the first setting does not validate the third. A runtime retrieval record establishes access, not that the retrieved item caused a particular assertion.

The candidate opening is the degradation caused by missing or incorrect lineage, including what a system should do when it cannot determine independence. Useful boundaries include partial ancestry, summaries with omitted parents, and independently written documents that share an upstream observation. These remain hunches requiring a focused survey and review.

**Decision before implementation:** choose whether the target is dependency detection, admission under uncertain dependencies, or preservation of dependencies through transformation. Avoid combining all three into one score. An oracle lineage policy can be a diagnostic ceiling, but cannot be presented as a deployable baseline.

## Recovery and retained useful knowledge

MemTX already implements cascading repair through a recorded dependency graph. Its guarantee concerns recorded descendants; compensation bookkeeping is distinct from replaying external effects. [[li-2026-memtx]] Classical rollback recovery likewise distinguishes consistent restoration, logged nondeterminism and external output commitments. [[elnozahy-2002-survey]] Therefore, “add rollback to agent memory” is insufficient as a contribution claim.

**Research implication, inferred:** connect memory repair with regrowth. A copied record may preserve useful knowledge after worker loss, yet also reintroduce an obsolete claim after correction. The question worth retaining is whether useful state can survive while invalidated dependencies stop recurring when the dependency graph is imperfect.

Separate four objects in any later scope statement: the original record, derived summaries, other agents' retained state, and external effects. Specify which object is corrected and which is observable. Deleting a source file does not logically imply that already-derived records disappear. Conversely, labeling every subsequent error “reinfection” would require evidence that the old claim actually contributed.

**Decision before implementation:** choose a reversible setting and a definition of successful repair that includes task usefulness. Report wrong actions, legitimate completion, recurrence, and recovery cost separately. A system that refuses everything has not demonstrated useful recovery. A claim of repair should be checked on later relevant decisions, not only on the immediate acknowledgement of a correction.

## Causal interpretation of swarm traces

Shalizi and Thomas establish that latent homophily can confound observational contagion estimates. [[shalizi-2011-homophily]] Aronow and Samii provide an experimental framework that separates treatment assignment, exposure and the causal quantity being estimated; its exposure mapping must be justified, and its reduced-form effects do not automatically identify mediation. [[aronow-2013-estimating]]

**Research implication, inferred:** a detection result should name its target. AI authorship, common model family, common operator, coordinated behavior, and harmful intent are different labels. A classifier trained on one scaffold may learn that scaffold rather than a general property of swarms.

For the external-influence direction, distinguish publication, retrieval, acceptance, peer exposure and collective outcome. A shared retrieval can make peers agree even without transmission between them. A no-communication comparison is useful, but removing communication also changes available evidence and compute unless these are accounted for. Effects conditional on successful retrieval answer a different question from end-to-end effects across all assigned cases.

**Decision before implementation:** name the unit of assignment and the independent unit of analysis. Agents, messages and turns within one interacting episode are not automatically independent replicates. Any future causal study needs an explicit exposure model and a comparison with the same external information opportunities. Observational work should retain an “unresolved mechanism” category when the logs cannot separate common exposure from influence.

## Attention allocation and identity budgets

Fair queueing already discusses the incentive to create more processes when allocation is per process; equal packet counts also need not mean equal bandwidth. [[demers-1989-analysis]] AgentPrune studies communication pruning, while Fukushima studies message capacity and wording sensitivity in LLM populations; both primary abstracts were re-opened, but their full methods were not audited in this pass. [[zhang-2024-cut]] [[fukushima-2026-message]]

**Research implication, inferred:** separate available contributions from contributions actually read. Record attempted, admitted, delivered, retrieved and retained material. A nominal honest majority may have little influence if its messages never reach the decision context. This is a question about selection and resource allocation before it is a question about voting.

An allocation policy must state its accounting unit: identity, operator, parent lineage, source group, tokens or verified contribution. Per-operator quotas presuppose an operator mapping; they cannot quietly solve the identity problem by assuming the hidden answer. Token caps bound a resource but do not establish informational value. The comparison must retain legitimate throughput and correction access, since suppressing communication can suppress useful evidence too.

**Decision before implementation:** choose whether identities are fixed or cheap to mint, and what the scheduler observes. Keep total inference and communication budgets explicit. Equal message counts are not a substitute for equal token budgets, and neither implies equal quality of evidence.

## Clarify what a merge and a fault mean

The fork-merge line includes text reports, persistent memory, tool configuration, model weights and latent state. These need separate threat models: specify the merged object, write authority, validator and observable failure. A result about averaging parameter vectors cannot supply a text-summary threshold without another argument.

One correction to the broad framing is needed. Byzantine agreement tolerates arbitrary coordinated behavior within its fault bound and stated message model; it does not require independent coin-flip failures. Correlation matters when it causes more participants to violate the bound or when supposedly correct participants share bad inputs. Agreement also does not establish factual truth. [[lamport-1982-byzantine]] An appended note in that library entry records this distinction without rewriting its owner's original text.

**Research implication, inferred:** do not import a “one third” or majority threshold into free-text merging. First define what a correct participant does and what safety means. Signatures authenticate statements; they do not certify that observations are true or independent.

## Readiness and access

These are the access checks available at the end of this pass, not evidence that an experiment has been reproduced.

| Resource | Verified scope | Consequence for selection |
|---|---|---|
| [CPB repository](https://github.com/lxy1134/iclr_2027) | Public repository and README inspected; MIT repository metadata. Static data is a reconstruction recipe with external-source licensing. Some governance tests require an unreleased document. No install or execution. | Inspect the exact runnable subset and source terms before adopting it. |
| [MemTX repository](https://github.com/lxy1134/MEMTX_) | Public README inspected; GitHub API reports no recognized license. No execution. | Available for inspection; redistribution and reuse terms remain unconfirmed. |
| AI Village | Existing team access audit reports manual gating and research-specific terms. Access was not requested or re-tested here. [[data-ai-village-2026]] | Do not make an immediate implementation plan depend on approved access. |
| Sealed swarm transcripts | Team audit records loading one transcript and one experiment family. This pass did not repeat that load. [[data-sealed-swarm-2026]] | Useful for trace inspection; worlds from one operator do not supply operator-disjoint validation. |

## Recommended narrowing

This is a research recommendation, not an accepted experiment plan.

| Candidate | Closest overlap | Remaining decision | Reason to park or reframe |
|---|---|---|---|
| Admission with incomplete lineage | CPB, MemLineage, quorum brief | What ancestry is independently observable, and what is inferred? | The only improvement comes from privileged source labels. |
| Recovery through incomplete dependencies | MemTX, memory and regrowth briefs | Which descendants and later decisions can be observed? | The idea reproduces recorded-graph rollback, or succeeds only by erasing useful state. |
| Attention under cheap identities | Fair queueing, AgentPrune, Sybil synthesis | Which accounting unit is available without oracle identity? | Gains disappear when budget and identity assumptions are matched. |
| Causal trace analysis | External-influence brief, interference literature | Can common exposure and peer influence be separated? | The available trace cannot identify the proposed mechanism; report association instead. |

The next selection discussion can now use these boundaries rather than open a new broad scan. Before promoting one candidate, its closest-prior methods need full reads, its dataset or environment needs a small access check, and the corresponding survey and cross-researcher review requirements still apply. This pass does not close the existing [evidence-depth audit](https://github.com/dmarzzz/swarm-lab/issues/76), [fork-merge gate work](https://github.com/dmarzzz/swarm-lab/issues/75), or the LLM-survey's revise review.
