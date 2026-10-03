# discovery

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift High · Difficulty Hard · Novelty Useful tooling · Event fit Strong · ~18–28 builder-hours (estimate).

## Background

Discovery triage ranks traces for a person to inspect. Shared timing or repeated text can also come from benign automation, common prompts or the same upstream source.

## Closest prior work

- **Transluce’s public agent-activity investigation · 2026** — https://transluce.org/agent-activity  
  A firsthand investigation based on public traces. Its observations are bounded by what the archive reveals.
- **SwarmTraces · 2026** — https://swarmtraces.org/  
  Shows how reconstructed records can be organized into an explorable evidence set. Use published artifacts before depending on fresh discoveries.

## Where it applies

Help researchers choose which public, redacted trace clusters deserve manual review. The output is an evidence packet, not an attribution verdict.

## The angle

Benchmark top-ranked candidate precision and reviewer time against random sampling and a simple keyword filter. Show the features behind each ranking.

## What to watch

Known incidents make a biased evaluation set. Hold out examples and include ordinary automation; do not label a real operator from similarity alone.

## Research question

Which observable features distinguish coordinated agent activity from ordinary automation or human activity?

## Dossier design sketch

Carried over from the [interactive dossier](../swarm-ecology-dossier.html#discovery). This is an unexecuted hunch, not an approved experiment. Counts and treatments below are planning choices; the lab’s survey and hypothesis review gates still apply.

1. Use published, redacted archives and known examples to define a small feature set.
2. Rank candidate clusters using explicit signals such as reciprocal references, shared artifacts and temporal coordination.
3. Produce an evidence packet for human review, not an automatic attribution verdict.

## Measures

- Precision among top-ranked candidates
- Reviewer time saved
- Coverage of known examples
- False positives on legitimate automation

## Controls

- Hold out part of the known data
- Use ordinary non-agent activity as comparison where permitted
- Separate coordination evidence from model attribution
- Document archive coverage

## Minimum useful output

An offline triage tool for one published archive and a transparent feature explanation.

## Optional extension

Additional public datasets after validation; no need for a new live discovery to succeed.

## Interpretation risk

A new swarm is an uncertain dependency. Public traces can contain personal or sensitive information; use curated redacted releases.

## Demo narrative

Open a high-ranked cluster and explain each piece of evidence and each alternative explanation.

## Review update October 3

Dataset access and attribution labels are prerequisites. Avoid claiming discovery from a detector trained and evaluated on the same known incident.

**Decision to resolve before promotion:** Does triage retrieve relevant held-out incidents with fewer reviewed false positives than simple search?

If the simple baseline explains the result, or the necessary evidence cannot be obtained, narrow this to a replication or park the hunch. A toy animation is not evidence that the proposed intervention works.

## Additional dossier sources

- [Discovery of an agent message board](https://collusion.wiki/) — Reconstructed public wiki data and attribution discussion.
- [Agent activity on urlquery.net](https://transluce.org/agent-activity) — Query traces with differentiated confidence and visibility limits.
- [SwarmTraces](https://swarmtraces.org/) — Reassembled public payloads and an existing evidence explorer.
- [Hackathon announcement](https://aivillageblog.substack.com/p/join-the-ai-swarm-dynamics-hackathon) — Primary event brief; proposed investigation tracks and public comments.

[All project briefs](README.md) · [Research updates](../background-readings-2026-10-03.md)
