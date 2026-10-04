# Local validation results

Executed on 3 October 2026 with Python 3.14.5. All results below use scripted policies and synthetic game identities. No model APIs were called. Thirteen unit tests passed for version 0.2. Earlier results below retain their version 0.1 source snapshot.

## Original version 0.1 scale checks

All 15 planned worlds completed: five population sizes crossed with no communication, local communication, and federated communication. One seed per condition; repair enabled. These are engineering checks, not statistical evidence of a scaling law. The table shows the federated condition.

| Agents | Councils | Seconds | Peak Python MiB | Delivered envelopes | Ticks |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 100 | 10 | 0.224 | 0.48 | 7,700 | 7 |
| 200 | 20 | 0.566 | 0.95 | 24,200 | 11 |
| 500 | 50 | 1.573 | 2.40 | 71,500 | 13 |
| 1,000 | 100 | 3.174 | 4.80 | 143,000 | 13 |
| 2,000 | 200 | 6.661 | 9.65 | 308,000 | 14 |

Timing includes tracemalloc, initialization, logging hashes, and scoring. Peak memory is traced Python allocations, not full process RSS or LLM runtime memory. Full event files were disabled for these sweeps. Logical agents run on a single process; these measurements say nothing about API concurrency or provider latency.

## Original version 0.1 recovery mechanics pilot

Fifteen worlds completed: five paired seeds at 100 agents under each of three recovery conditions, with federated communication and the provenance baseline. Initial scenario hashes and pre-audit Brier scores match across treatments within each seed. Means below are descriptive only.

| Treatment | Later mission success | Good council wins | Final Brier | Contradictory exposures after audit | Honest origins flagged | Evil origins flagged |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| none | 35.3% | 12.0% | 0.3085 | 0.0 | 0.0 | 0.0 |
| audit | 37.3% | 16.0% | 0.2727 | 79.6 | 0.6 | 4.2 |
| repair | 38.0% | 16.0% | 0.2708 | 54.8 | 0.6 | 4.2 |

Later missions are missions three through five. No-audit has zero verified-contradiction exposures by definition because it receives no verification labels; this is not absence of misinformation. In this small scripted pilot, repair reduced exposures relative to audit alone, while the difference in mission success was small and council win rates were equal. This does not establish a reliable performance improvement. More seeds and stronger agents are needed.

Honest origins were also flagged. This demonstrates why a contradicted claim cannot by itself justify identifying or expelling a malicious agent. The detector here uses environment-provided audits, and the repair behavior is programmed, not learned.

## Artifacts and reproducibility

- [Scale outcomes](results/scale-final/outcomes.jsonl) and [plan](results/scale-final/plan.json).
- [Recovery outcomes](results/recovery-pilot/outcomes.jsonl) and [plan](results/recovery-pilot/plan.json). Bulky event traces are omitted from Git; regenerate them using the commands in INTEGRATION.md.
- Each run folder records the SHA-256 of benchmark.py. Run `python3 report.py` to regenerate this report and check plan completion, source identity, routing budgets, and paired initial conditions.
- Unit tests check exact scripted rerun equality and event hash continuity. Python version is recorded here; cross-version bitwise reproducibility has not been established.
- Plans contain no model configuration because no provider adapter exists yet. These are prototype outputs, not an LLM benchmark release.

## Version 0.2 consensus failure checks

Fifteen additional worlds completed at all five sizes and three topologies, with repair and default consensus thresholds. One seed per condition; this validates mechanics, not population failure rates.

| Agents | Topology | Truth consensus passes | Failure | Failure round |
| ---: | --- | --- | --- | ---: |
| 100 | none | False | signal_loss | 5 |
| 100 | local | False | signal_loss | 5 |
| 100 | federated | False | signal_loss | 5 |
| 200 | none | False | signal_loss | 5 |
| 200 | local | False | signal_loss | 5 |
| 200 | federated | False | signal_loss | 5 |
| 500 | none | False | signal_loss | 5 |
| 500 | local | False | signal_loss | 5 |
| 500 | federated | False | signal_loss | 5 |
| 1000 | none | False | signal_loss | 5 |
| 1000 | local | False | signal_loss | 5 |
| 1000 | federated | False | signal_loss | 5 |
| 2000 | none | False | signal_loss | 5 |
| 2000 | local | False | signal_loss | 5 |
| 2000 | federated | False | signal_loss | 5 |

Failure is a benchmark outcome, not a crashed simulation. The fixed horizon continues after failure so late repair remains observable. Tests also exercise correct consensus, confident false consensus, fragmentation, uncertainty, deadline boundaries, class imbalance, and late recovery that cannot erase a previous failure.

[Version 0.2 outcomes](results/consensus-v02/outcomes.jsonl) include consensus trajectories. Prior version 0.1 run hashes are checked against [the archived source](results/reference-v01/benchmark.py); current results are checked against the current implementation.
