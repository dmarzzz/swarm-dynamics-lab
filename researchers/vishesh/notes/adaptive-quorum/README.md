# Adaptive quorum under urgency

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-pi-review; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — Fixed and adaptive quorum policies tied on the tested evidence tapes; the small fixture does not establish an adaptive stopping advantage. Basis: Fixed/adaptive policies tied; shared full tapes mean outcomes are paired. Source independence supplied, not detected. Small synthetic qualification does not establish adaptive advantage.
- **sample_size_summary:** Per backend:6 task clusters × 3 worlds × 2 deadlines × 4 policies =144 outcomes; scripted andLaya both complete.
<!-- experiment-evidence:end -->

## TLDR

When should five scouts commit to an API choice as a deadline approaches? Compare majority, fixed evidence quorum, a reduced final-round quorum and a central solver on shared recommendation tapes. Measure correctness, false commitment and delay. This tests a stopping rule on a fixed evidence schedule, not autonomous API research; a tied pilot does not show an adaptive advantage.

**Exploratory hunch and S0 instrument. Not an accepted hypothesis or a confirmatory experiment.**

Can a swarm lower its evidence quorum near a deadline to complete more useful decisions, without paying too much in false commitments? Five scouts choose a fictional API provider using distributed benchmark recommendations. The first version isolates the stopping rule; it does not simulate autonomous search or recruitment.

## Setup and protocol

Start from the lab's [worker template](../../../../templates/experiment-worker/README.md). This implementation retains its paired `run_episode` interface, evaluator separation, validity records and hub reporting, but bounds the worker to a single explicit qualification batch. See [preregistration](preregistration.md), [design](design.yaml), and [backend plan](BACKENDS.md).

The four policies are majority (three votes), fixed quorum (three votes and three distinct visible roots), adaptive quorum (three votes and three roots until the final round, then two roots), and a centralized solver. Scouts receive one private report per round and the preceding round's public reports; the central solver sees all reports available to scouts at that round. Each report recommends one provider for a fixed workload. This is a recommendation-integration task, not a validated end-to-end API procurement benchmark.

No independent decision-maker is presumed merely because it has another agent ID. Roots are fixture-provided labels, not detected independence. Copying and false reporting are controlled conditions; the code is not a detector of malicious intent.

## Research connections

- [Quorum](../project-briefs/quorum.md): deadline-dependent commitment.
- [Collective sensing](../project-briefs/collective-sensing.md): private versus common evidence.
- [Project brief index](../project-briefs/README.md): coordination, diversity and dissent connections remain exploratory.
- Dan's SOC-08 stopping-rule question in the [question atlas](../../../dmarz/notes/question-atlas/README.md): this is a bounded implementation, not a claim that stopping rules are a new research area.
- [[pratt-2006-tunable]]: biological motivation. Ant colonies alter decision parameters under urgency; our within-episode threshold schedule is an engineering analogy, not an exact biological replication.
- [Skeptical context](../skeptical-review/CONTEXT.md): coverage, accuracy, independent units and oracle leakage are reported separately.

## Reproduction

```
python3 src/selftest.py
python3 src/runner.py --backend scripted --out /tmp/quorum-scripted-S0
# With the pinned Laya environment and model installed:
python3 src/runner.py --backend laya --out /tmp/quorum-laya-S0
```

Output directories must be new; existing assignments are never overwritten or silently retried. Open `replay.html`, generated next to the append-only episode records. Scripted runs qualify plumbing only. Model qualification is a separate run, with backend identity and model revision in every record. Nothing provisions a server, invokes a real API provider, or launches S2.

## Results

[S0 completed](results/S0.md): 144 scripted and 144 local Laya outcomes; zero invalid; clean-task screen passed. Fixed and adaptive policies tied. [Live hub](https://swarm-live.pages.dev/#/x/adaptive-quorum) holds the reported runs and artifacts. This is qualification, not confirmation.

## Question and prediction

Can a reduced final-round quorum reduce delay or abstention without too many false commitments? The first pilot tests stopping policies on supplied recommendations, not research or evidence acquisition.

## Setup

Five scouts receive distributed, root-labelled benchmark recommendations for a fictional API choice. A centralized comparator sees the union of available reports.

## Protocol

Compare majority, fixed quorum, adaptive quorum and a central solver on a fixed evidence schedule. Fixed requires a majority and three visible roots; adaptive reduces the root floor to two at the deadline. Model qualification and scripted checks are separate.

## Metrics

Measure correct and false commitments, abstention, decision round and resources. Report fixed/adaptive ties directly. Root labels are fixture metadata, not independently discovered source trust.
