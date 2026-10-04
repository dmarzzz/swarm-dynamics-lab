# Avalon Swarm

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-pi-review; source `9781739c` ([registry](../../experiments/evidence-metadata.json), [rubric](../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — Scripted recovery and communication mechanics work at increasing logical population size. Basis: Programmed repair, synthetic identities and environment audits do not establish LLM benefit; small recovery difference descriptive. Large logical population is a capacity check, not large independent sample.
- **sample_size_summary:** 45 scripted worlds:15v0.1 scale (5sizes × 3topologies),15recovery (5paired seeds × 3arms),15v0.2 consensus checks;one scale seed per condition.
<!-- experiment-evidence:end -->

A runnable research prototype for studying trust, deceptive claims, coordination, and recovery in populations of **100, 200, 500, 1,000, and 2,000 agents**. Created for swarm-dynamics tooling, 3 October 2026. Version 0.2 uses scripted agents; it does not contain results from LLM agents.

The research question is: **When misleading claims spread through a swarm, does verified evidence actually repair collective decisions, or does the swarm keep repeating its earlier mistakes?**

We use ten-agent councils connected by sparse communication. Agents propose teams, vote, undertake missions, conceal roles, and exchange claims. Each council has its own hidden roles, but information about its members originates in neighboring councils. The resulting world has coupled information flow and a shared aggregate objective. It is a new Avalon-inspired game, not an official AvalonBench update or a faithful reproduction.

See [swarm-lab integration and status](INTEGRATION.md) before treating this prototype as a team experiment.

## Start here

Python 3.10 or newer; no dependencies, credentials, network, or paid calls.

```sh
cd tooling/avalon-swarm
python3 -m unittest discover -s tests -v
python3 benchmark.py --n 100 --recovery repair --out /tmp/avalon-example
python3 benchmark.py --n 100 --recovery-sweep --replicates 5 --out /tmp/avalon-recovery
python3 benchmark.py --sweep --recovery repair --out /tmp/avalon-scale
```

Each command requires a new output directory. Single-size runs save event logs; scale sweeps save outcomes and event hashes without retaining all messages. `--policy echo` counts repeated claims; `--policy provenance` deduplicates by original source and target; `--policy random` uses random team selection and voting with role-specific sabotage. These are deliberately simple baselines, not competent Avalon strategies.

| File | Purpose |
| --- | --- |
| [PROTOCOL.md](PROTOCOL.md) | Rules, research design, endpoints, budgets, limitations, and next experiments |
| [benchmark.py](benchmark.py) | Reference environment, scripted policies, routing, audits, and runner |
| [ADAPTER.md](ADAPTER.md) | Contract for connecting real agents and production execution requirements |
| [tests/test_benchmark.py](tests/test_benchmark.py) | Replay, observation boundaries, routing limits, repair, and action checks |
| [RESULTS.md](RESULTS.md) | Actual local validation and explicitly scripted pilot results |
| [results](results) | Machine-readable plans, outcomes, traces, and code hashes |

## Scale without a global transcript

Every agent sends one envelope per discussion tick to nine council members and two bridge contacts. Each envelope contains at most four claims. Receivers see at most eleven envelopes, keep at most 32 claims, and reason about ten local identities. Councils finish decisions in parallel logical rounds; the reference Python implementation executes those rounds on one process.

| Agents | Councils | Maximum delivered envelopes per tick | Full broadcast comparison |
| ---: | ---: | ---: | ---: |
| 100 | 10 | 1,100 | 9,900 |
| 200 | 20 | 2,200 | 39,800 |
| 500 | 50 | 5,500 | 249,500 |
| 1,000 | 100 | 11,000 | 999,000 |
| 2,000 | 200 | 22,000 | 3,998,000 |

These counts follow the routing rules, not observed LLM throughput. They compare delivered copies, not API calls. Linear communication cost does not guarantee that information can traverse the whole swarm quickly: the current council ring has increasing diameter.

## What recovery means here

After mission two, a trusted environment audit reveals one randomly selected member's alignment per council. Compare three conditions with identical initial roles and noisy evidence:

1. **None:** no audit.
2. **Audit:** agents can use the verified label, but stale contradictory claims remain in memory and circulation.
3. **Repair:** honest agents additionally remove contradicted claims and stop forwarding them; adversaries continue.

We measure subsequent mission success, role-belief error, contradictory claim exposure, and the honest versus adversarial origins of flagged claims. A contradiction is evidence that a claim is wrong; it is not proof that its author is malicious. There is no automatic expulsion or role accusation in this version.

The audit is an experimental intervention supplied by the environment. Autonomous discovery of trustworthy evidence, learned repair behavior, and real LLM adaptation remain to be implemented and evaluated.

## Chaos and loss of signal are failures

A run now fails the benchmark if it spends `--consensus-patience` consecutive discussion rounds without sufficient consensus on the truth, even if its missions succeed. Default patience is five rounds. Uncertainty and fragmented beliefs count as `signal_loss`; sufficiently widespread confident agreement on wrong answers counts as `false_consensus`.

For each identity, at least 80% of eligible ordinary-good council members must assign at least 70% probability to its true alignment. At least 80% of good identities **and** 80% of evil identities must meet that quorum across the network. Self-reports, Merlin, and evil agents are excluded from this truth-recovery endpoint: they already know relevant labels or have incentives to lie. This is network-wide coverage of locally relevant truths, not a requirement that every agent know all 2,000 identities.

A passing run must also end with two consecutive qualifying rounds. Failure after the patience window remains recorded even if the network later recovers; the simulator continues to capture recovery diagnostics. The thresholds are configurable design defaults and need calibration. `status=completed` means execution finished; `truth_consensus_pass` and `good_swarm_win` record benchmark success separately.

```sh
python3 benchmark.py --n 100 --recovery repair --consensus-patience 8 --consensus-quorum 0.8 --consensus-coverage 0.8 --consensus-confidence 0.7 --consensus-stability 2 --out /tmp/avalon-chaos
```
