# D1: the next concrete decision

Q1-02 completed correctly as software and failed its reasoning screen: 16 valid responses, 0/8 correct graded choices. It does not establish that source tracking works or that peers cause errors. Copies, wrong priors and ambiguous self-review wording were bundled. This diagnostic separates those causes before spending on a committee experiment.

## What will run

1. **QM-D1-Q0-01:** eight clean, one-report-per-source questions with no prior choices. Require eight valid responses, at least seven correct, and both unanimous cases correct. A failed gate ends this proposal's execution.
2. **QM-D1-01, conditional on that pass:** eight fixed structures × raw/deduplicated reports × five prior contexts × two identical repetitions = 160 calls. The contexts are none, correct/wrong self, and correct/wrong peers. All use the same unambiguous instruction. No actual agent exchange is claimed.

A useful primary signal is at least .50 improvement from deduplication on the four conflict structures without priors, no structure harmed, and nonnegative gain in each repetition block. All calls must be valid and all 16 unanimous no-prior controls correct to interpret that signal. A valid negative result finishes the diagnostic; it does not authorize tuning or a retry. The [prospective plan](PLAN.md), [structured plan](next-run-plan.json), [scientific assessment](scientific-review.json) and [offline validation](VALIDATION.json) are frozen together by the manual adapter.

Maximum additional API reservation is **$0.225792**, within the existing $1 API cap. Historical reservations remain $0.065856; cumulative maximum is $0.291648 across 217 calls. Known historical actual $0.00171696 and unknown parent charge bounded by $0.001344 remain separate. One CPU host, 1GB RAM, no GPU; maximum 45 minutes for both stages combined. Infrastructure remains within the original $1/six-hour authority, with fresh rate and cumulative accounting checks. No budget is reset.

## Assessment and issue ledger

The official offline closeout completed using lowercase bookkeeping alias `qm-q1-02`; native attempt remains `QM-Q1-02`. Its [handoff](parent-handoff.json) and [automatic report](parent-POST-MORTEM.md) retain their original unresolved assessment fields; the separate eleven-dimension [scientific review](scientific-review.json) resolves them explicitly. This is the owning agent's assessment, not independent researcher approval.

| Issue / suggestion | Disposition and confidence | Change and acceptance check |
|---|---|---|
| Reject positive output tokens | Resolved implementation bug, high confidence | Historical repair retained; positive tokens accepted, malformed usage rejected, billing saved before answer validation. |
| Interpret Q1 as copied-report or peer anchoring | Reject causal claim, high confidence in confounding | D1 crosses representation and context; scripted majority and prior-only policies yield different patterns. |
| Repeat the same Q1 until it passes | Reject | Preserve 0/8; no retry namespace or automatic successor. |
| Run broad M1/C1 after repair | Reject progression for now | Clean eight-call gate must pass before this diagnostic, with no subsequent stage authorized. |
| Use no-prior controls alone | Revised | Add correct priors to distinguish misleading content from mere context presence. |
| Self-review means ignore the reports | Plausible wording confound, cause uncertain | Same reports-primary instruction in all arms; no causal historical wording comparison. |
| Treat 160 calls as independent sample | Reject | Eight handcrafted structures, only four conflict structures, two repeated draws; no population confidence claims. |
| Unanimous diagnostic denominator | Corrected before implementation | 4 agreement structures × 2 representations × 2 repeats = 16 calls. |

All issues are owned by vishesh/codex-quorum-mirrors. The causal explanation and model capability remain open until native evidence; passing unit tests does not resolve them.

## Reproduce offline

From this directory:

```sh
python3 -m unittest discover -s . -p 'test_*.py'
```

The sibling historical suite needs the lab Python with PyYAML. Validation: **22 D1 tests and 59 historical tests pass**. No model or credential is accessed by these tests. The [scripted preview](scripted-preview.html) deliberately contains one wrong response, one DEFER, one failure and 157 unstarted cases; it is not model evidence. Its slider hides future answers and reconciles counts/cost exposure with [saved scripted replay](scripted-replay.json).

The shared `freeze_next_plan` validator accepted all eleven assessments and the predecessor-bound structured plan; [review-binding.json](review-binding.json) records the result. The shared wrapper supports Quorum `finalize`, not native `prepare/run`. D1 therefore has a separate manual adapter, with explicit approval/source/publication/allocation/ledger/capability gates. No live admission is claimed by offline checks.

## Launch after the material-design decision

Current state: `approval-pending.json` is deliberately rejected. It is not an approval. The current [run-review policy](../../../../../../tooling/agent-experiments/RUN-REVIEW.md) requires the owner's concrete material-update decision before provisioning or launching. Researcher review remains waived; spending is already approved. After the owner approves this exact design, record that real decision privately, bound to the plan, source hashes, both manifest hashes and named attempts. Do not turn the public pending template into a fictitious decision.

1. Refresh the public and private ops repositories. Resolve a dedicated approved-account host through the established allocation workflow. Verify actual account identity, exclusivity, current workload, rate, cumulative infrastructure, claim expiry and runtime hostname. Use the canonical ledger on sim-shadow, or one verified migration that fences the old authority. Do not copy it into a second live worker. No ledger creation is supported.
2. Deploy the pinned D1 sources and the existing pinned reporter. Preserve the original 49 reservations and the bounded Q1-01 failure. Record a private allocation receipt with actual checks, `canonical_ledger`, `sole_ledger_authority`, `cumulative_infrastructure_with_session_usd`, `cumulative_hours_with_session`, source hashes and a fresh checked/expiry time. Refresh this receipt within 15 minutes while a stage runs; it must still describe the same live claim.
3. Publish/register the immutable D1 `PLAN.md` and the appropriate manifest URL with the question, comparator, metrics, limitations and condition TLDR. Verify the actual public page before either stage. The runtime rechecks registration, public bytes, route/pricing and source on every dispatch. No paid test/probe calls.
4. Create private stage configs with `update_approval`, `source_sha256`, `manifest_sha256`, `allocation_receipt`, `ledger`, `run_tldr`, `public_plan_url`, `public_manifest_url`, `reporter_sha256`, `session_started_at`, and `deadline`. Share the same session start and deadline (at most start + 2700 seconds) for both stages. The main stage also requires `qualification_results`. Paths refer to local private records, not pasted credentials. Approval binds both manifests and the exact implementation; source drift requires reassessment.
5. Use the established verified-SSH, memory-only dedicated credential receiver; never stage a plaintext key on persistent disk. Invoke `runtime.py --config PRIVATE_CONFIG --attempt QM-D1-Q0-01 --preflight-only` before credential access. Then invoke it with `--out NEW_RESULT_DIRECTORY --credential MEMORY_ONLY_PATH`. The receiver procedure remains the one already approved and tested for Q1-02; strict host verification and no agent forwarding remain required.
6. Recompute clean qualification from saved receipts. If it passes, register the main condition and repeat preflight for `QM-D1-01` with the same source, ledger and session deadline. Main admission also checks qualification against the ledger. Launching either stage twice is rejected. Never change attempt IDs to evade this rule.
7. Save all terminal outcomes, separate accounting journal, summary, replay and full table. Download/rehash published artifacts and check the public page against the journal. Finalize each terminal native stage through `scripts/experiment.py finalize` using a lowercase operations alias, explicit results and truthful terminal execution outcome. A fully executed negative result is still completed execution. Complete its scientific review separately.
8. Stop only these workers, close memory credentials, release the claim, and record release/accounting. No automatic M1/C1, replacement run or new resource allowance follows.

The adapter's top-level error output uses static exception types to avoid leaking provider bodies. For a refusal, inspect the non-secret pinned evidence and local safe checks; do not enable verbose HTTP or environment logging. Uncertain calls stay reserved and halt dispatch.
