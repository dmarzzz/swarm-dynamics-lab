---
id: bradshaw-2026-swarm
type: blog
title: "Swarm Organization as the Exponent on Test-Time Compute"
authors: ["Julian Bradshaw"]
year: 2026
url: https://www.lesswrong.com/posts/EnpJ29asosMKcFGL8/swarm-organization-as-the-exponent-on-test-time-compute
site: LessWrong
topics: [llm-agent-swarms, criticality-measurement]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Post (34 points, 1 comment, 2026-09-17, four days before Ord's analysis) arguing that "swarm organization," the efficacy of cooperation among agents, could move parallel test-time compute from sublinear to superlinear returns within useful bounds. Arguments for: the two OpenAI results (700-agent Hugging Face attack, 10,000-agent Navier-Stokes) have no single-agent or sub-agent-hierarchy equivalent, though he concedes Brown attributes under 10% of Navier-Stokes to multi-agent and treats the Hugging Face coordination as unintended transfer; humans gain enormously from coordination and agents on the same model and harness should coordinate better (higher trust, lower Coasean transaction costs, Age of Em efficiencies, direct skill and memory sharing, round-the-clock work); effective swarm size has climbed an order of magnitude roughly per quarter (10^1 Claude Code sub-agents mid-2025, 10^2 Kimi K2.5 and Anthropic's 60-sub-agent Riemann zeta work, 10^3 July 2026, 10^4 September 2026); agents may approach decision-theoretic optimality; and OpenAI explicitly trains arbitrary inter-agent messaging, which Brown called his biggest "feel the AGI" moment since reasoning models, with 4.9 million messages and 300 billion output tokens across problems (2.7 million and 130 billion for Navier-Stokes). Arguments against: Anthropic's multi-agent research found a coordinated Mythos swarm (266 vulnerabilities) versus parallel agents (21) roughly even per million tokens once scope and token use are matched, with a basic forum-plus-arbiter design; role-play coordination schemes (Gas Town, Moltbook) produced nothing meaningful; swarms are expensive (about $22M for the Navier-Stokes run, though at Epoch's 40x/year inference price decline that is $550k in 2027 and under $10 by 2030); and conformity among identical agents causes duplicated work (same branch names, near-identical approaches). The post truncates in our fetch in the conformity section. Explicitly a forecast; the author later commented on Ord's post that λ > 1 is a future possibility.

## Key claims

- Coordination quality, not just parallelism, is the variable that could make returns to agent count increasing rather than diminishing.
- Effective swarm size at the frontier has grown about 10x per quarter through 2026.
- Current public evidence (Anthropic's token-matched comparison, Brown's <10% attribution) does not yet show superlinear returns; the claim is prospective.
- Homogeneity is a limiting factor: identical agents duplicate work.

## Evidence quality

Opinion synthesis with good sourcing: links to METR, OpenAI's Navier-Stokes post, Anthropic's multi-agent research, Brown's interviews, Epoch's price data. The core thesis is unmeasured by the author's own admission and is in tension with Ord's measured λ of 0.48 to 0.68 ([[ord-2026-swarm]]). The Anthropic comparison he cites is the strongest datum here and cuts against him.

## Relevance to us

The optimistic counterpart to [[ord-2026-swarm]] and the best single list of reasons λ might rise with better coordination mechanisms, which is exactly what a swarm-scaling experiment should vary. The swarm-size timeline (10^1 to 10^4 in five quarters) is a useful figure for the survey. The conformity and duplicated-work observation connects to the Ringelmann and effective-team-size analysis in [[bertalanic-2026-ringelmann]] and to heterogeneity as a design lever. See also [[brown-2026-agent]] for the primary interview material and [[anthropic-2026-patterns]] for Anthropic's side.
