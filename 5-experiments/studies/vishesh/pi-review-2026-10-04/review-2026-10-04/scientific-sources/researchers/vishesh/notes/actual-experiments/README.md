# Developed experiments: executable exploratory studies

Owner: vishesh/codex-experiments. Started 2026-10-03. These implementations turn the developed designs into bounded, auditable workers using the lab's distributed-worker contract. They are operational exploratory registrations, not accepted hypotheses or confirmatory studies.

| Study | Decision | Comparison | Fixed inputs | Outcomes |
|---|---|---|---|---|
| [External influence](external-influence/README.md) | Does checking decision-critical evidence improve fictional provider selection? | Independent assessments, discussion, same-source criticism, random checks, focused checks and a visible-root baseline | Provider truth, exposure packets, utility rule, final aggregation, five agents | Harmful target choice, correct choice, regret, abstention, eligibility and changed votes |
| [Immune response](immune-response/README.md) | Does shared-state restoration add value after private repair? | N, Q00, Q10, Q01, Q11 and clean reference | Eight actors, paired world/checkpoint, 24 rounds, incident window and recurrence/update timing | Useful completion, mock harm, recurrence, update acceptance, retained knowledge and recovery censoring |

The original sixteen briefs and 78 question extensions are not separate implementation commitments. Avalon is being published independently as [existing tooling](../../../../tooling/avalon-swarm/README.md); it will be integrated if included in the confirmed launch set.

## Run locally

From the repository root, Python 3.10+ standard library only:

```sh
python3 -m unittest discover -s researchers/vishesh/notes/actual-experiments/tests -v
python3 researchers/vishesh/notes/actual-experiments/src/runner.py external-influence local --stage S0 --out /tmp/influence-unique-run
python3 researchers/vishesh/notes/actual-experiments/src/runner.py immune-response local --stage S0 --out /tmp/immune-unique-run
```

Use a new output directory every time. `plan` prints the frozen assignment. `register`, `queue`, `work` and `status` use the preinstalled `swarm_report` module on the claimed fleet server. The bounded worker exits after one queued batch. Results include an assignment manifest written before execution, per-arm outcomes, policy request/response audit events, failures, summaries and a report. Uploads are compressed and split below the hub proxy limit, with hashes in `artifact-index.json`.

See [DEPLOYMENT.md](DEPLOYMENT.md) for the four completed hub runs and the blocked live-model handoff.

## Execution stages and spending

S0 qualifies the fixture and the real model interface. S1 is exploratory development and remains disabled for a live backend until its S0 results have been inspected and the qualification amendment is committed. S2 is unavailable. Existing source survey/hypothesis review gates remain intact.

The owner authorized **USD 50 total new spend**. API reservations share one transactional SQLite ledger, capped at USD 45 for all workers in this batch; USD 5 is reserved for possible new infrastructure. For new launches, the [dedicated-machine workflow](../experiment-machine-workflow.md) supersedes the earlier shared-server recommendation: claim an available machine from Dmarz's fleet exclusively for each experiment, or resolve authorized provisioning before launching. Existing runs finish in place. A new machine does not reset this batch's spending cap; enforce one budget authority or non-overlapping allocations before distributing paid workers across hosts. Reservations count failed and ambiguous requests and are never refunded. They are conservative cost bounds, not provider invoices. Model usage estimates are reported separately. Do not create a second ledger to evade the cap.

The native model is `claude-haiku-4-5-20251001`, matching dmarz's latest discussion-dose setup. [Official pricing](https://platform.claude.com/docs/en/about-claude/pricing), checked 2026-10-03, is USD 1/M input and USD 5/M output tokens. No caching or extended thinking is requested. Configuration is [model-config.json](model-config.json); model credentials remain in the fleet's private credential mechanism and never enter prompts, commands, logs, manifests or hub metadata. This price check does not itself qualify task performance.

## Provenance and limitations

Built from [the worker template](../../../../templates/experiment-worker/README.md), [the published methods toolkit](../../../../tooling/agent-experiments/README.md), and dmarz's [discussion-dose deployment](../../../dmarz/notes/discussion-dose/DEPLOYMENT.md). Study-specific amendments explicitly narrow the much larger proposed designs. The current external-influence fixture is a controlled-content experiment; it cannot establish organic search exposure or live SEO effectiveness. The immune study is Stage A oracle restoration, not a deployable detector or a biological claim. Scripted outputs describe deterministic policies; real model outputs are labeled separately.

All actions remain in fictional task worlds. Provider selection does not purchase or contact a provider. Deployment requests inside the immune world are mock ledger entries, separate from the real worker deployment.

