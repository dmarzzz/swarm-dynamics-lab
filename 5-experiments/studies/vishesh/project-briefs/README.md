# Project briefs: sixteen candidate directions (hunches, pre-survey)

Status: these are **hunches**, not hypotheses. None has passed the lab's prior-art gate; each names the prior work it would have to beat. The Lift / Difficulty / Novelty / Event-fit / hours columns are the author's own pre-survey triage, not a team ranking, and not measured; the order is the order they were written, not a recommendation.

| # | Brief | Lift | Difficulty | Novelty | Event fit | Hours |
|---|---|---|---|---|---|---|
| 01 | [collective-sensing](collective-sensing.md) | Medium | Moderate | Focused extension | Strong | 12–20 |
| 02 | [commons](commons.md) | Medium | Moderate | Focused extension | Strong | 12–20 |
| 03 | [regrowth](regrowth.md) | High | Hard | Focused extension | Strong | 18–28 |
| 04 | [quorum](quorum.md) | Low | Moderate | Focused extension | Strong | 6–12 |
| 05 | [diversity](diversity.md) | Medium | Hard | Focused extension | Strong | 14–24 |
| 06 | [telephone](telephone.md) | Medium | Moderate | Useful tooling | Strong | 10–18 |
| 07 | [whistleblowing](whistleblowing.md) | Medium | Hard | Focused extension | Strong | 14–22 |
| 08 | [memory](memory.md) | Medium | Hard | Focused extension | Strong | 12–22 |
| 09 | [casefile](casefile.md) | Medium | Moderate | Useful tooling | Strong | 10–18 |
| 10 | [leadership](leadership.md) | Medium | Hard | Focused extension | Strong | 14–24 |
| 11 | [dissent](dissent.md) | Low | Moderate | Focused extension | Strong | 8–14 |
| 12 | [culture](culture.md) | Medium | Hard | Focused extension | Strong | 14–24 |
| 13 | [coordination](coordination.md) | Low | Moderate | Useful tooling | Strong | 8–14 |
| 14 | [discovery](discovery.md) | High | Hard | Useful tooling | Strong | 18–28 |
| 15 | [institutions](institutions.md) | High | Hard | Focused extension | Strong | 18–28 |
| 16 | [nca-observatory](nca-observatory.md) | High | Hard | Established concept | Exploratory | 20–32+ |

## What each brief now includes

Every brief retains its original background, prior work, application, candidate contribution, and risk. The expanded sections preserve the dossier’s research question, design sketch, measures, controls, minimum output, optional extension, and demo narrative. A dated review update names a concrete decision to resolve before promoting the hunch.

The sketches describe possible future work. None records an experiment that was run or commits the team to a protocol. The [interactive dossier](../swarm-ecology-dossier.html) provides companion toy demonstrations; the [reading digest](../background-readings-2026-10-03.md) provides newer evidence and caveats.

## Selecting among the current candidates

| Direction | What would justify pursuing it | Main dependency or challenge |
| --- | --- | --- |
| Collective Sensing | An unanswered comparison after examining Silo-Bench and Proxifield. | Match evidence access and compute; avoid repeating a topology benchmark. |
| Quorum | A testable provenance-aware rule with a false-commit versus delay tradeoff. | Model common upstream sources; distinguish oracle provenance from inferred provenance. |
| Telephone | Useful, auditable claim lineage on held-out episodes. | Obtain trace coverage and manual labels; compare against existing investigation tools. |
| External influence | Measurable value from profiling over generic external contamination. | Establish normal retrieval exposure and separate acceptance from peer propagation. |

The external-influence hunch is documented [separately](../agent-swarm-influence-research.md); it is not one of the original sixteen briefs. Its [animated guide](../swarm-influence-guide.html) uses invented counts and must not be cited as evidence of attack reliability.

## Interpret the ratings cautiously

The ratings are rough planning categories, not quantitative scores. “Strong fit” applies to most candidates and is therefore a weak discriminator. Do not rank projects by counting favorable labels. Use access readiness, the closest prior implementation, an explicit unresolved question, and the smallest result that would change a decision.

The original hour estimates assume familiar tools and ready data. They exclude unknown access delays and do not substitute for an API or annotation budget. Record those costs before committing to a project.
