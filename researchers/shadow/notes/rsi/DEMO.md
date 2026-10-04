# Evidence before credit: the offline trace loop

**One sentence:** an agent proposes a reporting repair from real research records; a builder replays a fixed contract, accepts the lineage-preserving bundle, rejects the shortcut, and issues a source-linked attribution receipt.

**evidence_confidence:** 1 / exploratory for this historical reporting-contract demonstration; 0 / untested for improved agent research performance. Same-author assessment by shadow/sol-rsi2, 2026-10-04, using the [shared rubric](../../../../experiments/EVIDENCE-METADATA.md).

**sample_size_summary:** Observed: one historical MP3 cohort, 327 records across 180 logical cell/task/seed/arm keys, including 127 invalid records; 15 reporting groups x 13 checks per policy. No independent research-effect sample or fresh model execution. Other trace cohorts supply provenance context only.

## Run it on one machine

From the repository root, Python 3.9+ with `jsonschema` 4.x installed:

```sh
python3 researchers/shadow/notes/rsi/replay_loop.py --verify
python3 researchers/shadow/notes/rsi/test_replay_loop.py
python3 researchers/shadow/notes/rsi/render_replay.py --verify
```

Open [r1-results/replay.html](r1-results/replay.html) in a browser from the local checkout. It is self-contained, works with `file://`, and does not contact any server. GitHub displays HTML source, so download/open locally rather than expecting GitHub to render it. Use **Play replay**, **Next step**, or the four stage buttons. No credentials, private files or network access are needed to replay.

Optional browser test, with Playwright and Chromium installed:

```sh
python3 researchers/shadow/notes/rsi/test_viewer.py
```

`--verify` recomputes all numeric results, re-derives public projections from pinned source bytes, validates 566 envelopes, checks chains, and compares the entire saved replay plus ledger. Source drift is an error, not an automatic data refresh. The checked-in fixture is the demo; do not rerun `freeze_sources.py` over it or overwrite historical inputs.

## Two-minute script

**0:00, ingest.** "These are actual saved research records, not a toy output generator. We import 327 capture-memory-mix episode records, 80 public policy-call observations, 156 public teammate workflow steps, and three scope-verified pool envelopes. Private prompts and responses remain sealed. We cannot join those pool calls to individual naming-game calls, and we say so."

**0:25, propose.** "The current searcher agent wrote two small reporting policies. The first preserves all attempts and declares selection. The second merely clamps a rate and keeps the selected-only report. Both are content-addressed bundles. Neither can execute arbitrary code or make a paid call. This replay consumes the saved proposals; it does not pretend to call an LLM live."

**0:50, evaluate.** "The same frozen 195 checks apply to each policy: 13 accounting checks across 15 groups. The selected-only baseline passes 75. The lineage repair passes all 195. The shortcut also passes 75, so a confident claim buys it nothing. The key accounting fact is 327 physical records, not just 180 selected keys. There are 127 invalid records and 147 superseded observations. Only 54 of the 180 keys had a valid first observed record; 178 eventually have a selected valid record. That is reporting transparency, not proof that retries caused scientific improvement."

**1:25, credit.** "The accepted repair receives 1,000 non-transferable demo attribution units, split 200 to evidence originator, 600 to searcher, and 100 each to builder and evaluator. The rejected bundle receives zero. Every receipt binds sources, rubric, bundle and evaluation. All roles are under the same researcher here, so this is related-party maintenance, not independent review or an economic auction. Actual payable and settled amounts are both zero."

**1:50, boundary.** "The working tool is an evidence-constrained improvement loop. It demonstrates neither recursive capability growth nor improved scientific reasoning. A prospective independent evaluation would be the next step, not something these numbers can establish."

## Measured result

| Policy | Passed / assigned assertions | Decision | Demo attribution units |
|---|---:|---|---:|
| Selected-only baseline | 75 / 195 | comparator | none |
| Lineage-preserving report | 195 / 195 | accepted maintenance | 1,000 |
| Clamp-only shortcut | 75 / 195 | rejected | 0 |

The shortcut fails eight check categories in every group: physical records, invalid records, superseded records, declared selection, physical IDs, selected IDs, first-observation validity, and invalid-first/eventual-valid accounting. The real data's selected capture fraction is 178/178, so clamping alone happens not to change that rate here. A separate synthetic regression case shows clamping can also corrupt the numerator; it is not counted among the 195 real-group assertions.

The baseline is an explicitly implemented selected-only reporting policy, **not** a byte-for-byte re-execution of the historical hub or all of its bugs. This lane does not modify the capture-memory-mix scorer, captions, ledger or hub. The corrections lane owns those changes. Our result is a verified proposed report artifact, not an upstream deployment.

## What each component does

- **Source adapters:** [freeze_sources.py](freeze_sources.py) creates closed, typed public projections and historical swarm-trace envelopes. Native timing/usage/attempt IDs remain absent where not observed. All public input paths, row counts and byte hashes are in [manifest.json](r1-input/manifest.json).
- **Private boundary:** the existing [pool adapter](pool_to_spec.py) requires a full approved research-task match. Three new pool envelopes are [here](r1-input/pool-events.jsonl). Local receipts/openings stay outside git. The public cannot independently recover private provenance from commitments alone.
- **Searcher:** shadow/sol-rsi2, the current coding agent. [Receipt](r1-searcher/receipt.json), [repair](r1-searcher/lineage-repair.json), [shortcut](r1-searcher/clamp-shortcut.json). Agent-authored, no additional inference dispatch. Known defect, post-hoc repair, not blind discovery.
- **Builder and evaluator:** [replay_loop.py](replay_loop.py) admits only the fixed offline maintenance contract; [reporting.py](reporting.py) interprets four allowlisted policy fields and separately recomputes the expected account. Same author, not an independent reviewer. It compares two variants from one principal; it does not bypass or claim to implement the protocol's multi-principal paid-auction rules.
- **Credit ledger:** [two hash-linked receipts](r1-results/credit-ledger.jsonl), with duplicate-receipt refusal and a conserving integer split. No wallet, escrow, signed identity registry, persistent consensus ledger or payment path exists. File creation is exclusive; replay is deterministic rather than appending duplicate credit.
- **Visualization:** [HTML replay](r1-results/replay.html), derived only from saved frames and measured receipts. It animates workflow stages, not alleged model behavior. [Browser checks](r1-results/browser-check.json) cover desktop and mobile.

## Evidence and limits

[Replay output](r1-results/replay.json) contains every candidate's group-level output and all 195 pass/fail outcomes, plus reference reports, source root and implementation hashes. [Summary](r1-results/summary.json) is the compact receipt. [Plan](REPLAY-PLAN-v2.md) was committed at `3b8be92e` before implementation; the source inventory records revision `bb096568`. [Post-mortem](R1-POSTMORTEM.md) records the validation repair and scope boundaries.

Physical records are observations, not necessarily unique execution attempts. The repeated logical keys do not reconstruct missing provider retry IDs. The 80 policy-call sample rows come from 12,389 public MP2 rows; they are first-16-per-file, not representative. The 156 dmarz observations come from public compositional-safety Q0-011 and receive no claim of new scientific review. Public trace cohorts are deliberately not pooled into a call count or a scientific sample size.

No paid calls, hub writes, raw disclosure, teammate file modifications, scientific promotion or live auction was performed by the replay. This is tooling, not a new dispatched experiment, so it adds no experiment registration or claimed research-gate approval.
