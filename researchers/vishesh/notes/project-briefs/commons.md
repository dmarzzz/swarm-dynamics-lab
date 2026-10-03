# commons

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift Medium · Difficulty Moderate · Novelty Focused extension · Event fit Strong · ~12–20 builder-hours (estimate).

## Background

A public good costs its producer something while benefiting others. Bacterial siderophores make the cost-and-benefit structure concrete. In agent systems, verified shared notes can play a similar role: producing them takes budget, while everyone can reuse them.

## Closest prior work

- **Cooperation and competition in pathogenic bacteria · Griffin et al., 2004** — https://www.nature.com/articles/nature02744  
  Experiments connect bacterial cooperation to relatedness and the scale of competition. The lesson is to vary incentives and interaction structure explicitly.
- **Melting Pot · DeepMind** — https://github.com/google-deepmind/meltingpot  
  An existing suite tests cooperation, competition and other social interactions. Commons-style environments already have substantial benchmark history.
- **LLM agents in Melting Pot · 2024** — https://arxiv.org/abs/2403.11381  
  Adapts Melting Pot scenarios for language agents and evaluates cooperation in Commons Harvest. This is close prior art, not merely a biological analogy.

## Where it applies

Shared research caches, collective annotation and communal compute budgets. Useful output would identify a cheap rule that sustains verified contributions.

## The angle

Use shared artifacts with an objective quality check. Test whether attribution or contribution credit changes both useful output and free-riding.

## What to watch

A generic harvest game adds little. The contribution should come from verified knowledge, a new incentive comparison, or a well-measured failure.

## Research question

Does verification before sharing protect useful collective output when some shared results are unreliable?

## Dossier design sketch

Carried over from the [interactive dossier](../swarm-ecology-dossier.html#commons). This is an unexecuted hunch, not an approved experiment. Counts and treatments below are planning choices; the lab’s survey and hypothesis review gates still apply.

1. Agents spend a fixed budget testing small, objectively checkable hypotheses. Findings enter a shared library.
2. Compare immediate publication with evidence-required publication. Introduce a controlled fraction of unreliable contributions.
3. Track whether agents reuse, verify, dispute or ignore findings; keep the true validity of each finding available to the evaluator.

## Measures

- Verified useful findings per total budget
- Downstream work wasted on false findings
- Time until a bad artifact is challenged
- Honest work delayed by verification

## Controls

- Equal initial knowledge, test cost and total budget
- Separate non-contributors from false contributors
- Clean-library baseline
- If roles are programmed, report introduced rather than emergent cheating

## Minimum useful output

One hypothesis-testing task, two sharing policies, one contamination level and a clean condition; artifact lineage replay.

## Optional extension

Local versus global libraries, spatial assortment, or access earned through verified contributions.

## Interpretation risk

A hand-coded reward function can predetermine the result. Charge verification against the same budget and report its overhead.

## Demo narrative

Show one unreliable finding being reused. Switch to the evidence gate and reveal the benefit and cost over repeated runs.

## Review update October 3

Treat the biological analogy as motivation. Use objectively checked shared artifacts so increased contribution volume cannot masquerade as increased useful output.

**Decision to resolve before promotion:** Does the sharing rule improve verified output per unit cost over an uncredited shared cache?

If the simple baseline explains the result, or the necessary evidence cannot be obtained, narrow this to a replication or park the hunch. A toy animation is not evidence that the proposed intervention works.

## Additional dossier sources

- [Cooperation and conflict in quorum-sensing bacteria](https://www.nature.com/articles/nature06279) — Communication, cooperative behavior and exploitation.
- [Quorum sensing protects cooperation from cheats](https://www.nature.com/articles/ismej2015232) — Population composition and signaling influence cooperative investment.
- [Spatial-temporal dynamics of microbial cooperation](https://www.nature.com/articles/s41467-022-28321-9) — Spatial structure and cooperative behavior; inspiration for controlled comparisons.
- [Emergent cheating and whistleblowing in research swarms](https://arxiv.org/html/2609.04170v1) — Shared knowledge, exploit diffusion and ineffective enforcement in a research collective.
- [Welcome to Delvetown](https://groveresearch.com/blog/welcome-to-delvetown/) — Agent ecology, persistent identities, public interaction and institutions.

[All project briefs](README.md) · [Research updates](../background-readings-2026-10-03.md)
