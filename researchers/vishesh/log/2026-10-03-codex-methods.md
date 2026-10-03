# 2026-10-03 — vishesh/codex-methods

Human request: contribute the experiment guide as general tooling for whichever project the team chooses; check repository fit, documentation and secret exposure before publication.

The toolkit lives in `tooling/agent-experiments/`, with a root navigation link and an explicit integration map. No formal survey, hypothesis, experiment or cross-researcher review is introduced. The existing research gates and researcher directives remain unchanged. The repository's direct-main workflow is followed.

Privacy review removed standalone-machine context and excluded generated traces, local source paths, original package manifests and unrelated workspace material. A selected-file Gitleaks scan with complete redaction returned zero findings across 57 files before publication preparation. A separate path/credential-pattern/context scan returned zero flags. No credentials were read or printed. Only public source metadata and synthetic examples are included. Scanner results are bounded checks, not proof that all possible secrets are detectable.

Validation: the offline harness validator passed twice-per-check replay for 960 worlds and 12,480 events per run, with pairing, reset isolation, known-answer behavior, corruption detection and overwrite rejection. `lab.py check` reported zero errors and the same five pre-existing unresolved-reference warnings. `fd.py check --strict .` passed with zero errors/warnings in a checkout named `swarm-lab`; a first check in a differently named scratch checkout correctly reported its folder-name invariant. No project metadata was changed to evade that rule.

Source integration: reused three canonical paper records and added 26. `lab.py verify` checked 24 resolvable arXiv/DOI records with zero problems; the JMLR and PMLR publication pages were checked directly and remain explicitly URL-only. No full-paper reads or empirical replication are claimed by the new source entries.

Workflow choice: automatic sync was deferred until the requested publication/privacy review was complete, so unreviewed imported files could not be pushed by a timer. Manual checkpoints are used in this isolated contribution checkout. The user request to audit before contribution takes precedence over starting a broad automatic sync immediately. Registration and task claiming use the repository tools; claim fields are never edited by hand.

Next: projects should adapt the toolkit only after their own survey and hypothesis gates, validate production adapters independently, and keep paid collection separate from this offline teaching example.

## Publication result

Published toolkit commit: [4d8eadde6b26f6299d67ba2af90fde7427bba6ac](https://github.com/dmarzzz/swarm-lab/commit/4d8eadde6b26f6299d67ba2af90fde7427bba6ac). The final exact-staged-file Gitleaks review covered 57 files / 210,591 bytes with zero findings. All 34 canonical source links in the toolkit resolve.

GitHub Actions passed: [offline toolkit validation](https://github.com/dmarzzz/swarm-lab/actions/runs/37152506049) and [repository check, source verification and generated index](https://github.com/dmarzzz/swarm-lab/actions/runs/37152505912). The contribution is general tooling; no paid experiment was launched and no project hypothesis was selected. The build task is closed through `lab.py done` after publication.
