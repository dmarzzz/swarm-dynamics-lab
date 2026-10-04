# Telephone: where evidence changes in an agent swarm

**Exploratory experimental idea, version T0, 2026-10-04.** Owner: Vishesh. Design author: vishesh/codex-village-fit. No experimental runs, accepted hypothesis, measured benefit or novelty certification. Researcher review is not required by owner direction.

**Question:** when agents relay a claim through conversation and compressed memory, what happens to its evidence, attribution and uncertainty—and can a source-linked handoff preserve meaning better than ordinary prose?

The practical output is a way to distinguish an accurately relayed claim from one that has become more confident, broader, differently attributed or detached from its support. It should help a researcher find the first *observed* distortion and decide which record needs checking. It must not invent a transmission path from similar wording.

| Read | Purpose |
|---|---|
| [Background research](BACKGROUND.md) | Closest work, what is already known, candidate contribution and remaining research gaps |
| [Prospective experiment plan](PLAN.md) | Separate natural-trace audit from controlled replay; treatments, controls, independent units, metrics and stopping |
| [Annotation and scenario specification](ANNOTATION.md) | Claim fields, lineage evidence, point-in-time truth, controls and adjudication |
| [AI Village resource and data plan](DATA.md) | Canonical dataset entry, pinned revision, acquisition and privacy boundaries |
| [Setup and readiness](SETUP.md) | One authoritative Telephone gate record, dependencies and exact next actions |

## The idea in one example

**Invented illustration, not a Village finding:** a source says a partner could not evaluate a prototype. A later summary says the partner reviewed it; a subsequent memory says it was validated; a final message describes it as adopted. These statements differ in action, attribution and evidential strength. A simple string-similarity score may regard them as related while missing the consequential change.

Telephone records separately: what each text asserts, whether the available evidence supports it, whether a source-to-retelling connection is established, and whether the record was available to that actor. A true statement can have an unsupported origin claim; an accurately copied statement can still be false about the world. These are different outcomes.

## Two complementary stages

1. **Natural-trace audit:** build a small, verified casebook from AI Village. Locate supported connections, annotate changes, retain accurate and uncertain cases, and document gaps. This stage describes the selected records; it cannot establish that interaction caused the distortion.
2. **Controlled three-hop replay:** if the corpus and labels qualify, randomly order paired fresh-agent chains comparing prose, source-linked structured retelling, and access to original-source retrieval. This tests our communication method on constructed tasks derived from the corpus. It is not a counterfactual continuation of the historical Village.

First deliverable: an evidence-linked development casebook and strong-baseline report. A model study is useful only if simple extraction or source lookup leaves a meaningful task unsolved. A negative result or solved baseline can finish the project.

## Why AI Village

The dataset offers linked chat, persistent memories, session metadata and computer-use evidence across long-running activities. That combination may connect retelling to memory and subsequent action. It is a promising affordance, not proof that complete chains exist in our sample. [[data-ai-village-2026]]

The prior preparation found sparse cross-table matches in arbitrary file prefixes. Telephone therefore selects complete task windows, not the first few thousand rows. The [resource guide](DATA.md) makes this an explicit acquisition requirement.

## Scope and related projects

Telephone measures claim fidelity and its change across hops. Quorum measures source identity/evidence counting; Theseus measures useful state transfer; Right Dissenter measures reopening after fresh evidence. They may reuse reviewed records but must not treat reuse as independent replication. The separate acknowledgment/closure idea remains an optional downstream extension, not another arm in T0.

**evidence_confidence:** 0/4 for structured retelling improving fidelity; assessed 2026-10-04 by vishesh/codex-village-fit. Background literature motivates the question; no Telephone treatment outcomes exist.

**sample_size_summary:** observed Telephone task components 0, adjudicated claims 0, model calls 0. Proposed 8 development, 8 qualification and 24 evaluation components, conditional on coherent independent groups. Claims, agents, hops and calls are nested observations, not independent samples.

**Current disposition: PREPARE OFFLINE.** Complete the development casebook, annotation agreement and baseline audit before freezing a costed native packet. This design request did not launch a study or allocate resources.

## Latest iteration: T1 offline preparation

[Implementation, cases and closeout](t1/README.md): 24 Telephone tests and 21 shared checks pass. Eight authored roots produce 72 scripted hop outputs. Fourteen private source joins yield zero validated complete episodes. Copy and exact lookup reach the fixture ceiling; model efficacy remains untested. **HOLD native collection** pending coherent development cases and a useful residual task. T0 remains the original prospective design, not a runnable admission packet.

[Top-10 design additions](TOP10-NEXT-STEPS.md) distinguish current A0/V0 handoffs from a possible future sparse-network study.
