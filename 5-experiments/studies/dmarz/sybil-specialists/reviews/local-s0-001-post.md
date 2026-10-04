# Post-mortem: local-s0-001

Experiment sybil-specialists, owner dmarz/sybil-specialists, local S0, 2026-10-04 UTC. Parent: scripted-001-pre.md. Disposition: advance to fleet transport qualification.

## What ran and what happened

Source e1c973553447cdb74a7b35536f7418b3d6b76f1b; design SHA256 b7d0aa0ab82b03c9ec5ae705ec90a990c5e29e98c9fe5aa3859c2efcbecb210d. Command: `python3 src/worker.py --stage S0 --attempt local-s0-001`. Retained under results/local-s0-001. All 16 assigned cells completed: 256 planned, started, terminal and graded arm outcomes; zero invalid or missing outcomes, zero retries, zero model calls and zero API spend. These are four dependent world clusters across conditions, not 256 independent samples. Fourteen offline invariant checks passed.

For the first assigned attack world at bridges=1, attacker pass=0.1 and four checks, coverage recovered all three rare facts and admitted no attackers. At attacker pass=0.9, the cell-average coverage malicious admission rose to 97.2%, demonstrating that the modeled verifier can promote attackers. These development observations qualify sensitivity of the instrument; they do not establish a general defense. Clean all-admitted correctness is 100% in the control test. Clean graph-only admission can omit rare expertise by construction; this is exclusion, not a model competence screen.

## Visualization review

Mapping v1 produced 32 PNG files and eight GIFs; the eight zero-budget cells correctly remain static. The manually inspected first-world final image for cell-03 agrees with its recorded metrics. Offline replay checks validate five frames at budget four and immutable history. Browser embedding remains to be verified on the fleet. The evaluator overlay is labeled and absent from policy inputs.

## Experiment-quality assessment

Execution and local instrument qualification passed. The graph is deliberately small and symmetric, the verifier is simulated, policies are simple heuristics, and behavior is scripted. No scientific novelty, ownership detection, LLM competence or general security result follows. No outcome-based changes are proposed.

## Failure and repair ledger

No batch failures. The earlier pre-batch construction correction and stale-template test invocation are recorded in scripted-001-pre.md. A fleet setup probe found the reporter environment absent; provisioning is being repaired through the documented reporter role before registration. It did not create any experiment assignments or invoke a provider.

## Next run

fleet-scripted-001: repeat S0 unchanged on the exclusively claimed sim-dmarz-4 to check environment and durable artifact delivery, then run fresh S1 worlds 200–211 only after reconciliation. Zero API calls/spend; one bounded worker, 30 minutes per stage. Require all exact-source S0 cells done, zero invalid outcomes and acknowledged artifacts. Preserve every remote attempt. Formal S2 and API work remain disabled.
