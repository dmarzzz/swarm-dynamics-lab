# Qualification build and launch status

Updated 2026-10-04 UTC by vishesh/codex-idea-scores.

## Implemented

- `src/tasks.py`: deterministic 16-item evidence/repository fixtures, strict JSON parsing, restricted-AST repair evaluation, operational scoring and an 80-assignment manifest. Transfer generation is deliberately unavailable.
- `src/engine.py`: stateful contexts, one planning-repair allowance for malformed model plans, dependency scheduling, charged-context interfaces and final integration. Ready jobs use the least-used idle actor (ties by actor ID), so a four-slot limit does not silently make N=16 use only the same four contexts. Model-call transport failures are not retried as planning repairs.
- `src/budget.py`: durable SQLite reservations at episode and shared-stage scope; unfinished provider charges retain their reservation. Concurrent reservation tests exercise overspend prevention. This is single-host accounting; do not copy its database to independent hosts.
- `src/provider.py`: an isolated-process OpenRouter transport, parent-enforced request deadline, no credential logging, no route fallback, conservative full-context reservations and actual-cost settlement. Provider execution has not been tested with a real call; served model/provider fields remain unset.
- `src/run_qualification.py`: Q-A-only execution entry point, source/public-plan checks, assigned manifest, local condition-specific TLDRs and durable event/outcome files. It uses `reporting.py` to register each run with a condition-specific TLDR and verify that TLDR through the public proxy before actor calls. `register.py` publishes experiment-plan metadata separately. Local JSON events/outcomes and a standalone interval replay are uploaded through the installed hub client. It does not allocate a machine or manufacture a review verdict. Reporting/transport integration still needs validation on the selected host. Q-B requires the Q-A assessment and frozen calibration configuration; it is not automatically launched.

The actual first implementation narrows repository repair to an explicitly described arithmetic expression grammar. It is a qualification benchmark, not a general software repair study. All actors receive the complete small public task at context initialization; replicated prompt tokens must be charged. This avoids unequal information access but does not implement the large-corpus retrieval extension yet. Dependencies are explicitly visible in these fixtures; latent-structure inference is not being tested.

## Offline verification

Command from repository root:

```
python3 -m unittest discover -s researchers/vishesh/notes/optimal-swarm-size/src -p 'test_*.py' -v
```

Eighteen test methods cover 80 reference-task variations, all five rosters under scripted transport, malformed and adversarial submissions, equivalent valid repairs, split/input invariants, concurrency/overspending, operational boundaries and refusal of the incomplete launch configuration. Scripted reference answers prove plumbing only; they are not model performance observations. No experimental/model run has occurred.

Read [PRIOR-ART-REVIEW.md](PRIOR-ART-REVIEW.md) for the completed focused author review and its limits. The independent review is requested in `tasks/review-swarm-size-qualification.md` for Shadow; no passing verdict has been received. The focused review does not complete the formal survey/hypothesis gates for a confirmatory study.

## Remaining launch work

1. Obtain the user's total API cap (asked in the task); choose an episode cap within it. User intent to launch is recorded, but no numeric spending allowance was supplied.
2. Review and pin the served model/provider route and the price/accounting bound. Public OpenRouter model metadata on 2026-10-04 listed `openai/gpt-4.1-mini` with input $0.40/M tokens and output $1.60/M tokens. These are observed quotes, not a contract or spending authorization. The draft conservatively reserves 1,047,576 context tokens plus 4,096 output tokens per call: $0.425585 rounded upward. Nineteen calls per episode gives a very loose upper bound of $8.086115 per episode, $129.37784 for Q-A and $646.8892 for all 80. Actual prompt/output usage would normally be much smaller, but it is unmeasured. A smaller authorized cap may stop execution early; tighter reservations need verified tokenization rather than optimistic guesses.
3. Obtain independent package review and address findings. Confirm the permitted exploratory S0/S1 route; keep core/transfer locked behind the research gates.
4. Validate the implemented hub reporting/transport and standalone replay on the selected host; register and verify an immutable public plan and condition-specific TLDR before model execution. Existing public proxy problems must not be treated as a successful public preflight.
5. Verify a fresh exclusive eligible fleet allocation and non-secret credential availability. No machine was claimed or provisioned during this build.
6. Freeze source/config, verify every launch requirement, start Q-A, reconcile all 16 assignments, assess qualification and calibration, then freeze Q-B. Keep failed/cancelled/not-started records visible and retain unknown billing reservations.

The launch check currently exits 2 with missing fields. This is an explicit not-ready result, not an attempted model run or a successful launch.

## Visualization delivery

Live qualification uses textual progress and measured item counts. Final `replay.html` displays recorded service intervals with a scrubber and static table; it is a downloadable hub artifact because the public proxy does not serve arbitrary HTML. `trace.jsonl` preserves event history. There is no flock animation or manufactured physical trajectory, and no claim that an interval plot measures provider GPU activity. Browser validation and transport integration are outstanding review checks; offline replay checks cover interval lengths, missing ends and HTML escaping.
