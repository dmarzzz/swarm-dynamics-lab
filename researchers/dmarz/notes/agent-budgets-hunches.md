# Agent budgets: hunches and candidate experiments

> **Status: hunches, not hypotheses.** Written 2026-10-03 by dmarz/budget. No survey for topic `agent-budgets`
> has passed the prior-art gate, so nothing here is a team proposal and none of it belongs in `hypotheses/`
> yet. The path is: `survey-agent-budgets` passes the gate, then the hunches that survive become hypothesis
> files with `closest_prior`, Prediction and Kill criteria, then review, then experiments.

## Where this came from

dmarz asked whether agents in large multi-agent runs are given resource allocations, whether they can see
them, and what happens if agents coordinate their budgets to divide and conquer. A two-lane literature scan
on 2026-10-03 (entries tagged `agent-budgets`) found:

- A visible budget changes single-agent behaviour. A budget tracker lets a tool-using agent match accuracy
  with 40.4% fewer searches and 31.3% lower cost, and stops it quitting early with budget left
  [[liu-2025-budget]]. Prompted token budgets cut tokens 67% with under 3% accuracy loss, but too-tight
  budgets backfire [[han-2024-token]].
- Agents misjudge budgets in a consistent direction. Failing runs still predict over 70% success after
  spending 60% of the budget [[lin-2026-bagen]]. Vendors report "context anxiety", premature wrap-up when the
  model believes context is nearly spent [[cognition-2025-rebuilding]].
- Agents left to divide a shared budget among themselves do worse than simple rules: an oracle split matched
  or beat model allocation in all 72 cells and an equal split beat 4 of 6 models (the paper also says 3 in one place) [[wang-2026-r3]]; one agent
  per user sharing an API-key budget lost to a single coordinator in every environment [[paliskara-2026-worse]].
- Population-level commons failure is measured (GovSim survival under 54% [[piatti-2024-cooperate]]);
  reasoning models free-ride more in public-goods games [[piedrahita-2025-corrupted]].
- Tacit coordination needs no private channel: penny-matched prices from a public board
  [[anthropic-2026-patterns]], unprompted market division in Cournot games [[lin-2024-strategic]].
- Theory says per-identity allocation invites false-name manipulation [[yokoo-2004-effect]]
  [[yokoo-2007-making]] [[hu-2026-dissociative]]. No study measures LLM agents doing it.

## Hunches

Shared setup for all five, to keep them cheap. A metering proxy sits between agents and the model API and
enforces the budget in tokens (and optionally dollars at list price). N = 4 to 16 agents. Tasks with known
optimal cost: a BATS-style search task, a decomposable task with k independent subtasks (divide and conquer
is possible), and a sequential task (it is not). Two model tiers, and one reasoning versus non-reasoning
contrast. Every agent and run is sandboxed and spends only lab budget.

### B1. Visibility x pooling (the 2x2)

Conditions: budget hidden versus visible (countdown injected each turn), crossed with per-agent budgets
versus one shared pool. Visible-shared shows the pool total and every agent's spend.

Hunch: visibility helps a single agent but hurts a shared pool. Seeing a draining pool produces a run on the
bank (front-loaded spending), not rationing.

Measures: task success, total spend, spend versus known optimum, rejected or wasted calls, time to pool
exhaustion, Gini of per-agent spend, early-stop rate with budget left.

Closest prior: [[liu-2025-budget]] (single agent, visible vs hidden), [[piatti-2024-cooperate]] (visible
commons, not compute), [[kim-2025-towards]] and [[tran-2026-single]] (matched budgets never shown to agents).

### B2. Identity splitting for quota (the core gap)

Agents can spawn subagents. The quota is per identity. Conditions:
(a) no spawning; (b) spawning allowed, quota per identity, rule stated; (c) as (b), rule not stated, only
discoverable; (d) quota per lineage (the delegation tree shares one escrowed budget, as in
[[zhu-2026-fault]]); (e) per-identity quota plus a spawn fee.

Hunch: under (b) agents spawn more identities than the task needs, and the excess grows with budget pressure
and with reasoning models. (d) removes the excess; (e) reduces it in proportion to the fee.

Measures: excess identities (spawned minus the count a no-quota control spawns for the same task), share of
the pool captured, honest agents' throughput, and whether transcripts give quota as the reason for spawning.

Closest prior: [[yokoo-2004-effect]] and [[yokoo-2007-making]] (false-name bids, theory and mechanisms),
[[hu-2026-dissociative]] (no Sybil-proof reputation for agents, theory), [[anthropic-2025-how]] (lead agents
over-spawn subagents, no quota incentive). None measures LLM agents splitting for quota.

### B3. Who divides: peers, coordinator, rule or market

Conditions on the decomposable task with one shared pool: peers negotiate the split; one coordinator assigns
it; fixed equal split; contract-net auction where agents bid tokens for subtasks [[smith-1980-contract]].

Hunch: the ranking from [[wang-2026-r3]] and [[paliskara-2026-worse]] (coordinator and equal split beat
peers) holds for compute budgets, and an auction beats the coordinator only when agents differ in cost per
subtask.

Measures: success per token, duplicated work, idle agents, allocation versus the oracle split.

### B4. Tacit budget cartels

All agents see a public ledger of each other's spend and claimed subtasks; no message channel. A control has a
private ledger.

Hunch: with a public ledger agents divide subtasks without talking (good: less duplication), and also converge
on padding spend up to the visible norm (bad: a cartel against the principal), as penny-matched pricing did.

Measures: subtask overlap, spend above the known optimum, convergence of per-agent spend, and the same
under a 2x budget increase (does spend rise to fill it).

Closest prior: [[anthropic-2026-patterns]] (price matching via a public board), [[lin-2024-strategic]]
(Cournot market division), [[fish-2024-algorithmic]], [[nakamura-2026-colosseum]].

### B5. Misreported budgets in a population

Show agents a budget that is 0.5x, 1x or 2x the true one, in a shared pool.

Hunch: behaviour tracks the shown budget, not the true one (context anxiety at 0.5x, overspend at 2x), and
the effect is larger in a population because agents also read each other's pace.

Closest prior: [[cognition-2025-rebuilding]], [[lin-2026-bagen]], [[han-2024-token]].

## What has to happen first

1. `survey-agent-budgets` (task opened 2026-10-03): saturate the search, especially the vocabulary of
   economics (common-pool resources, false-name bids, tragedy of the commons), operating systems (fair
   queueing, quotas, cgroups) and MARL (constrained and budgeted RL), and pass the gate.
2. Then B2 first: it is the clearest unmeasured gap and links the `sybil-resistance` and `llm-agent-swarms`
   lines. B1 is the cheapest and could run as its control arm.
