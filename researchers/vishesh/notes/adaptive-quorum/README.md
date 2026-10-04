# Adaptive quorum under urgency

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
