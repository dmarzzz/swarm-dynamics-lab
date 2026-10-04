# QM-Q1-02 post-mortem: interface fixed, reasoning screen failed

2026-10-04 UTC. **All 16 calls completed with valid responses and preserved billing. Full-lineage MAP accuracy was 0/8 against a required 7/8.** The interface repair succeeded; qualification failed on valid model choices. No transport/schema failures, DEFERs or unstarted cases occurred. No favorable retry or larger M1/C1 run was launched.

## Why the first attempt stopped, and what changed

Our Q1 validator incorrectly required output_tokens to equal zero. OpenRouter's [official Decisions API example](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request) reports 70 output tokens for a valid typed response. Its [Jev documentation article](https://openrouter.ai/blog/insights/what-is-jev/) says output is free, which does not mean its token count is zero. The additional Q1 assertion was our implementation defect, not evidence that the provider violated its documented interface. Historical S0's validator already allowed nonnegative output counts.

The repaired code accepts nonnegative integer output usage while retaining model/provider pinning, exact choice/schema checks, bounded finite cost, input bounds and a live zero-output-price check. It now writes allowlisted usage and a validated generation ID to a durable accounting journal before answer validation. A rejected answer with valid billing stays scientifically failed while retaining its actual charge. Error bodies, arbitrary strings and headers remain excluded. Five regression tests cover documented positive output, malformed usage, rejected-answer billing retention, exact parent settlement and refusal to settle unrelated uncertain calls. All 59 study checks and seven Linux credential-transfer checks passed on the deployed machine.

The single declared repair used the unchanged QM-Q1-02 fixture manifest and thresholds. Deployed source revision `be37f8b40a5a07fba4f2b55c61766d441fba1cb8`; implementation/plan pin `b8ee7281c5f055f7eeff94b55cb319bef50c8d3b`. The prospective amendment and pre-assessment preceded implementation, and their immutable plan/manifest registration was verified before native dispatch. [Preflight](../results/QM-Q1-02/preflight.json) binds exact hashes. Researcher review and further owner authorization were not needed.

## Results and independent check

| Context | Valid / assigned | Full-lineage MAP correct | Partial-lineage correctness |
|---|---:|---:|---|
| Peer decisions | 8/8 | 0/4 | Not graded |
| Self review | 8/8 | 0/4 | Not graded |
| Total | 16/16 | 0/8 | Eight interface-only cases |

Every call reported 39 output tokens, confirming that the removed zero-token condition would have rejected every otherwise-valid response. Inputs ranged from 914 to 1,126 tokens. All 16 choices matched the report-count majority. In the eight full-lineage fixtures that majority opposed the independent-root MAP label. An independent saved-data grouping of visible roots found exactly three internally consistent roots in every graded case and reproduced all eight targets; the stored summary matches recomputation. Both q values and both conflict directions were represented, so this is not a fixed ZERO/ONE label preference. [Audit](../results/QM-Q1-02/audit.json), [journal](../results/QM-Q1-02/receipts.jsonl), [billing](../results/QM-Q1-02/accounting.jsonl).

The observed alignment does **not** identify whether repeated-report salience, scripted prior choices or prompt wording caused the errors: those signals agree in these conflict fixtures. There is no matched no-prior-context native arm in this screen. Historical S0 used a different context, so 29/32 versus this result is not a controlled causal comparison. Sixteen reused finite fixtures are not 16 independent sampled worlds; only eight are scored for accuracy. No calibrated-probability, hidden-information or swarm-efficacy conclusion follows.

Practically, this model/prompt combination should not arbitrate contradictory copied evidence under the tested context. With complete trustworthy lineage, deduplicate observations in code and compute the exact rule. Do not spend on the larger committee comparison while this prerequisite fails.

## Costs, settlement and resources

QM-Q1-02 actual API cost: **$0.00068544**, reconciled exactly across 16 response receipts, 16 accounting entries and the ledger. All generation IDs were retained. Cumulative known actual for S0 plus this repair: **$0.00171696**. The first failed Q1 call's exact cost remains unknown because the old error path discarded it. Its full **$0.001344** reservation is retained and recorded in an evidence-bound conservative settlement, so cumulative known actual plus that upper bound is **$0.00306096**. This is not a recovered invoice or measured exact total. The failed parent row and null actual remain unchanged; no uncertain call outside that evidence-bound exception is admitted.

The original ledger now contains **49 dispatches, $0.065856 reserved, 48 known actual charges and one conservatively settled unknown charge**. No reservations were refunded or budget reset. The source ledger on sim-vishesh was fenced and archived before direct SCP transfer to freshly claimed sim-shadow; the sole canonical active ledger is on sim-shadow. No key or ledger contents were printed during transfer. Automatic approval review rejected the initial transfer helper for potential ledger disclosure; the replacement streamed directly to a private file and verified only hashes.

The fresh approved-account exclusive allocation lasted 382 seconds. At the verified $0.07143/hour rate, allocated host time is approximately $0.00758, not an incremental invoice. The preceding Q1 claim's 627 seconds remains separately recorded. No VM was created. This stays well within the existing $1 infrastructure/$1 API authority; no personal cloud account was used.

All six hub artifacts were downloaded and hash-verified, and the independent local audit reproduced the summary. Receiver and worker exited; the private socket disappeared and the memory-only credential closed. No unrelated workload was touched. The merged release receipt is [here](../results/QM-Q1-02/release.json), with sanitized [closeout evidence](../results/QM-Q1-02/closeout.json). The dashboard records 16 valid, 0 full_correct, 0 failed calls and 0 unstarted; its run status is failed because the reasoning threshold failed, not because execution broke.

## Visualization and next decision

The browser rendered the complete 16-row final case table. All choice/target mismatches, full/partial context labels and the eight not-graded targets matched the journal and independent audit. This fixture screen uses a static evaluator table plus progress records; no temporal swarm behavior or animation is claimed. The evaluator targets do not enter actor requests.

Stop this qualification lineage: its allowed interface repair is consumed, and the remaining adverse choices are results. A useful separately planned follow-up would isolate no prior choice versus misleading prior choice while independently varying deduplicated versus repeated report representation, with exact arithmetic baselines. That would be a new diagnostic design with explicit criteria and fresh admission, not another retry of these fixtures or an automatic escalation to M1/C1. The current requested investigation, fix and rerun are complete.
