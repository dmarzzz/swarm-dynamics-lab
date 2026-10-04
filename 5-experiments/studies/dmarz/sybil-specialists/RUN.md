# Run the exploratory instrument

Use Python 3.9+ with requirements.txt. Start from the experiment-worker template and follow the root AGENTS.md and 5-experiments/toolkit/agent-experiments/RUN-REVIEW.md. This directory stays in researcher notes until formal gates pass.

1. Read the last post-mortem and commit the next pre-run assessment and configuration.
2. Run `python3 src/selftest.py`. It performs no provider calls.
3. Run a fresh local rehearsal: `python3 src/worker.py --stage S0 --attempt local-s0-001`. Existing outputs are never overwritten.
4. Refresh agentops fleet and claims, exclusively claim an available authorized host, and verify the merged claim. Use a dedicated checkout pinned to the committed public source revision.
5. On the claimed host set SWARM_SOURCE=dmarz/sybil-specialists and use the preinstalled swarm-report module. Register with `python3 src/coordinator.py register`, queue with `python3 src/coordinator.py stage S0`, and run `python3 src/worker.py --hub`. The worker ends when the queue is empty.
6. Check every S0 cell is done with zero invalid episodes and durable images/traces. Then queue S1 and run the same bounded worker. Exact-source S0 completion is enforced by the coordinator. Repeated queue commands retain existing assignments, including failures.
7. Review the live UI, record all run IDs and a post-mortem. Keep outputs until uploads and checksums have been verified. Stop all experiment workers, then release the agentops claim.

The deployment wrapper is in the private swarm-labs-agentops repository. Only server names appear here. Hub credentials are resolved on the server through its protected reporting environment; they are never copied into this repository. Scripted operation never needs a model API key.

S2 and model calls remain disabled. To enable a paid exploratory follow-up, first specify and review its model role, frozen prompt, clean qualification, resource cap and credential alias. Do not change this worker to interpret an unreviewed backend parameter as permission to spend.
# Aggregate analysis

Install analysis-requirements.txt in the analysis environment. After copying the authenticated raw run directories into a fresh results directory, run `python3 src/analyze.py results/REMOTE_DIRECTORY --output results/analysis.json` and `python3 src/plot_results.py results/REMOTE_DIRECTORY results/tradeoff.png`. Both output paths must be new. The plot requires all 18 S1 cells and refuses duplicate condition tuples. It shows descriptive means for all four arms; the main dashboard's scalar metrics describe the coverage arm. Record the analysis source revision and dependency versions separately from the frozen simulation revision.
