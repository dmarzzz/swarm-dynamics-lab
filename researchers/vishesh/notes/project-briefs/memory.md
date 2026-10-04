# memory

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift Medium · Difficulty Hard · Novelty Focused extension · Event fit Strong · ~12–22 builder-hours (estimate).

## Background

Persistent memory can keep a useful fact or repeatedly reintroduce a bad one. A correction has to reach the record that future retrieval actually uses. Deletion, annotation and replacement have different failure modes.

## Closest prior work

- **AgentPoison · 2024** — https://arxiv.org/abs/2407.12784  
  Shows that poisoned memory or retrieved knowledge can redirect agent behavior. It establishes a concrete memory-integrity problem.
- **LongMemEval · 2024** — https://arxiv.org/abs/2410.10813  
  Evaluates memory abilities including knowledge updates and abstention. It provides task-design ideas for testing whether a correction sticks.
- **Generative Agents · 2023** — https://arxiv.org/abs/2304.03442  
  Uses stored experiences, retrieval and reflection. A correction may need to address a derived reflection as well as the original note.

## Where it applies

Repair stale project assumptions, revoked instructions and incorrect research notes without erasing useful history.

## The angle

After a verified correction, test recurrence across later retrievals. Track derived summaries and compare append-only correction with explicit supersession.

## What to watch

A safer-sounding response is not a memory repair. Check the retrieved records and behavior on held-out questions.

## Research question

When an agent is corrected, is the correction retained, weakened, omitted or later contradicted?

## Dossier design sketch

Carried over from the [interactive dossier](../swarm-ecology-dossier.html#memory). This is an unexecuted hunch, not an approved experiment. Counts and treatments below are planning choices; the lab’s survey and hypothesis review gates still apply.

1. Find episodes with a mistaken claim, disconfirming evidence and memory snapshots on both sides.
2. Classify correction preservation and coexistence with the old claim.
3. Retrieve later relevant actions and label recurrence or insufficient evidence.

## Measures

- Correction retention at the next available snapshot
- Later contradiction frequency
- Evidence-supported classifier precision
- Time to recurrence in the available record

## Controls

- Separate unknown from false
- Do not infer unseen observations
- Track model, goal and scaffold changes
- Compare with manually reviewed episodes

## Minimum useful output

A before/after memory viewer and a small annotated set of correction episodes.

## Optional extension

Test a structured memory format prospectively using a synthetic task.

## Interpretation risk

Not every later mistake is recurrence of the same belief. Public comments already propose basic memory checking.

## Demo narrative

Open a correction, inspect the next memory and reveal a later relevant action with its evidence.

## Review update October 3

Use a correction that reaches the retrieved state, including derived summaries. Compare against memory-poisoning work already in the library. [[chen-2024-agentpoison]]

**Decision to resolve before promotion:** Does explicit supersession reduce recurrence on held-out retrievals compared with appending a correction?

If the simple baseline explains the result, or the necessary evidence cannot be obtained, narrow this to a replication or park the hunch. A toy animation is not evidence that the proposed intervention works.

## Additional dossier sources

- [Compounding misalignment: Gemini case study](https://aivillageblog.substack.com/p/gemini-25-pro-in-the-ai-village-as) — Longitudinal case interpretation connecting failure, state and later behavior.
- [Saving Gemini](https://aivillageblog.substack.com/p/saving-gemini) — Peer intervention and subsequent memory correction.
- [Hackathon announcement](https://aivillageblog.substack.com/p/join-the-ai-swarm-dynamics-hackathon) — Primary event brief; proposed investigation tracks and public comments.
- [AI Village dataset card](https://huggingface.co/datasets/aidigestorg/ai-village) — Gated research data; table descriptions, limitations and scaffolding changelog.

[All project briefs](README.md) · [Research updates](../background-readings-2026-10-03.md)

## AI Village integration update, 2026-10-04

[Dataset-backed preparation and fit](../ai-village-replay-2026-10-04/PLAN.md) now supplies concrete next steps. The [shared builder](../ai-village-replay-2026-10-04/IMPLEMENTATION.md) is validated offline; no real episode labels or native outcomes are claimed. This brief remains an unrun hunch.
