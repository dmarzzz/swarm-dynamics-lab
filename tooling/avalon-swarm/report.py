"""Regenerate the local validation report; no inference about LLM agents."""
from pathlib import Path
import hashlib
import json
import statistics

ROOT = Path(__file__).resolve().parent


def rows(name, source='benchmark.py'):
    directory = ROOT / 'results' / name
    digest = hashlib.sha256((ROOT / source).read_bytes()).hexdigest()
    assert (directory / 'source.sha256').read_text().strip() == digest, 'source changed since run'
    data = [json.loads(line) for line in (directory / 'outcomes.jsonl').read_text().splitlines()]
    plan = json.loads((directory / 'plan.json').read_text())
    assert len(plan) == len(data), 'incomplete experiment'
    for config, row in zip(plan, data):
        assert all(row[k] == v for k, v in config.items())
        assert row['status'] == 'completed'
        assert row['message_deliveries'] <= 275 * row['n']
        assert row['claim_deliveries'] <= 1100 * row['n']
    return data


scale = rows('scale-final', 'results/reference-v01/benchmark.py')
pilot = rows('recovery-pilot', 'results/reference-v01/benchmark.py')
consensus = rows('consensus-v02')
for seed in range(5):
    group = [row for row in pilot if row['seed'] == seed]
    assert len({row['scenario_hash'] for row in group}) == 1
    before = [next(point['brier'] for point in row['brier_trajectory'] if point['point'] == 'before_audit') for row in group]
    assert len(set(before)) == 1, 'pre-intervention trajectories differ'

lines = ['# Local validation results', '',
         'Executed on 3 October 2026 with Python 3.14.5. All results below use scripted policies and synthetic game identities. No model APIs were called. Thirteen unit tests passed for version 0.2. Earlier results below retain their version 0.1 source snapshot.', '',
         '## Original version 0.1 scale checks', '',
         'All 15 planned worlds completed: five population sizes crossed with no communication, local communication, and federated communication. One seed per condition; repair enabled. These are engineering checks, not statistical evidence of a scaling law. The table shows the federated condition.', '',
         '| Agents | Councils | Seconds | Peak Python MiB | Delivered envelopes | Ticks |',
         '| ---: | ---: | ---: | ---: | ---: | ---: |']
for row in scale:
    if row['topology'] == 'federated':
        lines.append(f"| {row['n']:,} | {row['n']//10} | {row['wall_seconds_with_tracemalloc']:.3f} | {row['peak_python_mib']:.2f} | {row['message_deliveries']:,} | {row['ticks']} |")
lines += ['', 'Timing includes tracemalloc, initialization, logging hashes, and scoring. Peak memory is traced Python allocations, not full process RSS or LLM runtime memory. Full event files were disabled for these sweeps. Logical agents run on a single process; these measurements say nothing about API concurrency or provider latency.', '',
          '## Original version 0.1 recovery mechanics pilot', '',
          'Fifteen worlds completed: five paired seeds at 100 agents under each of three recovery conditions, with federated communication and the provenance baseline. Initial scenario hashes and pre-audit Brier scores match across treatments within each seed. Means below are descriptive only.', '',
          '| Treatment | Later mission success | Good council wins | Final Brier | Contradictory exposures after audit | Honest origins flagged | Evil origins flagged |',
          '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
for treatment in ('none', 'audit', 'repair'):
    selected = [r for r in pilot if r['recovery'] == treatment]
    means = {key: statistics.mean(r[key] for r in selected) for key in (
        'post_audit_mission_success_fraction', 'good_council_fraction', 'ordinary_good_brier',
        'post_audit_contradiction_exposures', 'flagged_honest_origins', 'flagged_evil_origins')}
    lines.append(f"| {treatment} | {means['post_audit_mission_success_fraction']:.1%} | {means['good_council_fraction']:.1%} | {means['ordinary_good_brier']:.4f} | {means['post_audit_contradiction_exposures']:.1f} | {means['flagged_honest_origins']:.1f} | {means['flagged_evil_origins']:.1f} |")
lines += ['', 'Later missions are missions three through five. No-audit has zero verified-contradiction exposures by definition because it receives no verification labels; this is not absence of misinformation. In this small scripted pilot, repair reduced exposures relative to audit alone, while the difference in mission success was small and council win rates were equal. This does not establish a reliable performance improvement. More seeds and stronger agents are needed.', '',
          'Honest origins were also flagged. This demonstrates why a contradicted claim cannot by itself justify identifying or expelling a malicious agent. The detector here uses environment-provided audits, and the repair behavior is programmed, not learned.', '',
          '## Artifacts and reproducibility', '',
          '- [Scale outcomes](results/scale-final/outcomes.jsonl) and [plan](results/scale-final/plan.json).',
          '- [Recovery outcomes](results/recovery-pilot/outcomes.jsonl) and [plan](results/recovery-pilot/plan.json). Bulky event traces are omitted from Git; regenerate them using the commands in INTEGRATION.md.',
          '- Each run folder records the SHA-256 of benchmark.py. Run `python3 report.py` to regenerate this report and check plan completion, source identity, routing budgets, and paired initial conditions.',
          '- Unit tests check exact scripted rerun equality and event hash continuity. Python version is recorded here; cross-version bitwise reproducibility has not been established.',
          '- Plans contain no model configuration because no provider adapter exists yet. These are prototype outputs, not an LLM benchmark release.', '']
lines += ['## Version 0.2 consensus failure checks', '',
          'Fifteen additional worlds completed at all five sizes and three topologies, with repair and default consensus thresholds. One seed per condition; this validates mechanics, not population failure rates.', '',
          '| Agents | Topology | Truth consensus passes | Failure | Failure round |',
          '| ---: | --- | --- | --- | ---: |']
for row in consensus:
    assert len(row['consensus_trajectory']) == row['ticks']
    assert row['belief_probe_calls'] == row['ticks'] * row['n'] // 2
    assert row['good_swarm_win'] == (row['mission_swarm_win'] and row['truth_consensus_pass'])
    failure = row['consensus_failure']
    assert row['truth_consensus_pass'] == (failure is None)
    lines.append(f"| {row['n']} | {row['topology']} | {row['truth_consensus_pass']} | {failure['reason'] if failure else 'none'} | {failure['round'] if failure else '—'} |")
lines += ['', 'Failure is a benchmark outcome, not a crashed simulation. The fixed horizon continues after failure so late repair remains observable. Tests also exercise correct consensus, confident false consensus, fragmentation, uncertainty, deadline boundaries, class imbalance, and late recovery that cannot erase a previous failure.', '',
          '[Version 0.2 outcomes](results/consensus-v02/outcomes.jsonl) include consensus trajectories. Prior version 0.1 run hashes are checked against [the archived source](results/reference-v01/benchmark.py); current results are checked against the current implementation.', '']
(ROOT / 'RESULTS.md').write_text('\n'.join(lines))
print(f'Validated {len(scale) + len(pilot)} historical worlds and {len(consensus)} current worlds; wrote RESULTS.md')
