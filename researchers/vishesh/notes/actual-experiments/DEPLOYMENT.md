# Deployment record and live qualification handoff

Deployed public source: `ef4a0d44d8b4ce2b5cbebce54939fe0627588925`. Shared existing server `sim-test-01`; dedicated checkout `/srv/swarm/vishesh-actual-experiments`; worker identity `vishesh/codex-experiments`. Fleet claim `vishesh-developed-experiments` was published through the private agentops claim workflow. No server was provisioned, no ports were opened and no existing worker was stopped.

## Completed hub runs

| Study | Stage | Hub run | Outcomes | Invalid | Backend |
|---|---|---|---:|---:|---|
| external-influence | S0 | external-influence/750034be | 84 | 0 | scripted |
| external-influence | S1 | external-influence/8a8174a7 | 3024 | 0 | scripted |
| immune-response | S0 | immune-response/8de9162d | 18 | 0 | scripted |
| immune-response | S1 | immune-response/4d83c625 | 36 | 0 | scripted |

Verified through the authenticated hub status API and the public live experiment list. Each run has its full assignment manifest, outcome records, policy-event journal, summary and report uploaded in compressed parts with an integrity index. All workers are bounded and have exited. **These are engineering measurements of programmed policies, not evidence about LLM behavior.** No API calls or new infrastructure charges were incurred by this batch.

- [External influence on Swarm Lab](https://swarm-live.pages.dev/#/x/external-influence)
- [Immune response on Swarm Lab](https://swarm-live.pages.dev/#/x/immune-response)

## Live model status

Native Haiku qualification is implemented and mock-tested but **not launched**. The preflight found no available model credential before enqueueing; no live runs or paid requests were created. During this session the team's model configuration moved from server environment storage to encrypted per-launch injection. The latest private agentops `scripts/run-discussion-dose.py` documents that mechanism. This machine has no SOPS executable or authorized age private key. Do not bypass that protection or copy plaintext credentials into this public repository.

Resume from an authorized credential-capable machine. Claim the server again; use the private repo's SOPS mechanism to load only the model key and workspace ID into a local process, then transmit them to the worker over SSH stdin/in-memory environment. Never print decrypted output, use secrets as command arguments or persist them to a launch script. Set these **nonsecret paths/settings** in the worker environment:

```text
PYTHONPATH=/usr/local/lib/swarm
SWARM_SOURCE=vishesh/codex-experiments
SWARM_MODEL_BASE_URL=https://api.anthropic.com/v1
SWARM_MODEL_CONFIG_FILE=<deployed-study-root>/model-config.json
SWARM_BUDGET_LEDGER=/srv/swarm/vishesh-actual-budget.sqlite
```

The same budget ledger must be used by both studies. Validate `AnthropicPolicy()` before enqueueing. Check the deployed revision, config hash and active claim. Then use `runner.py <study> queue --stage S0 --backend anthropic` followed by one bounded `work` process with the same backend. Do not enqueue S1 until S0 task validity is reviewed and the qualification amendment is committed. Do not automatically retry an assigned outcome.

The maximum S0 actor-slot bound is 67 for external influence and 960 for immune response. At the configured 24,000-byte input bound, 512-byte envelope allowance, 1,024 output-token cap and pinned prices, a conservative bound is `(67+960)*(24512*1+1024*5)/1e6 = USD 30.432064`, below the shared USD 45 API cap. Actual input sizes/slots are smaller. The original full live S1 is not authorized to run merely because it is listed: re-estimate its complete bound and amend its sample before opening it if it cannot fit the remaining ledger. USD 5 remains reserved for infrastructure; none was needed.

## Rerunning infrastructure checks

From the repository root on a freshly claimed server, set `PYTHONPATH` and `SWARM_SOURCE`, run the unit tests, register the study, and inspect `status`. A queue with the identical frozen parameters is deliberately rejected even if a previous run failed. New engineering batches require a documented design version/assignment, rather than silently replacing results. Repairing a failed artifact upload must reuse the existing outcomes and must not rerun the experiment.
