# Antsy

When should a swarm commit to an API choice, and when should it wait for better evidence?

The current implementation is [repair v3](repair-v3/README.md). The review repaired evidence accounting, agent qualification, timing/cost claims, reproducibility and temporal visualization. The guarded local Laya architecture passed 22/22 qualification cases; 384 matched blocks produced 2,688 policy outcomes with zero actor/schema failures after recovery from a documented rendering bug.

[Quality assessment and results](repair-v3/reviews/S1-attempt-2-post.md) · [Specification](repair-v3/SPEC.md) · [Agent contract](repair-v3/agent-spec.json) · [Runbook](repair-v3/RUN.md) · [Live dashboard](https://swarm-live.pages.dev/#/x/adaptive-quorum-api-v2).

## Question

Does relaxing an evidence quorum near a deadline improve useful completion, and when does it instead admit misinformation? Compare constant-two and constant-three source requirements, adaptive stopping, majority voting and central controls.

## Setup

Five or nine scouts select among three fictional invoice APIs from delayed or misleading synthetic facts. Laya reads atomic predicates; explicit host code guards observed hard constraints and compares prices. This is an exploratory mechanism test, not independent AI expertise or real provider evaluation.

## Protocol

The frozen [v3 specification](repair-v3/SPEC.md) and [attempt reviews](repair-v3/reviews/) preserve every diagnostic, qualification and recovery. Twelve task clusters cross four evidence worlds, two arrival schedules, two populations and two cutoffs. Survey/hypothesis promotion gates remain unmet; S2 is disabled.

## Metrics

All-assigned correctness, constraint violations, abstention, loss, commitment ticks, logical invocations and actual physical inference costs. Adaptive helps when late information corrects earlier misinformation, but hurts when late information is false. In this study every learned-policy choice matched the symbolic baseline: no incremental AI benefit is established.

## Historical versions

[V2 original design and failed pilot](V2-HISTORICAL.md), [v2 protocol](protocol.md), [v2 results](results/laya-analysis.md), and [v1](../adaptive-quorum/README.md) remain intact. Stable experiment ID `adaptive-quorum-api-v2` retains old runs. Display name: Antsy. Jev through OpenRouter remains deferred pending secure setup and new qualification.

