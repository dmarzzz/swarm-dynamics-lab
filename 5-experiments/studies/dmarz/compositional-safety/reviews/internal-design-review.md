# Internal design review before execution

Status: ready for bounded engineering qualification only. Author: dmarz/patchwork-hypotheses. These are simulated research perspectives applied by the study author, not actual reviews, endorsements, or independent evidence from Google DeepMind or Flashbots.

The user explicitly directed us to replace independent review with these internal perspectives before starting. This overrides the independent-review requirement for this requested work. It does not erase remaining source, measurement, spending or execution requirements. No model episode has run at this review point.

## Multi agent safety research perspective

The persuasive contribution would identify a cause of global policy failure and demonstrate the limits of a repair on genuinely new tasks. Merely constructing a permissive environment in which a bad sequence is possible is a software conformance check.

| Objection | Required change before qualification | Evidence required before scaled inference |
|---|---|---|
| The initial generator changes identifiers but barely changes structure. Thousands of renamed examples are not thousands of independent task graphs. | Vary graph depth, source alternatives and approval-sharing structure; record a structural fingerprint separately from entity labels. | Split by structural family and cluster duplicates together; power counts independent structures, not renamed cases. |
| One agent versus many changes more than information. | Keep S versus F as the primary comparison with identical roles, actions and turn order. | Match resource ceilings and report actual context/call differences; centralized C is a separate bundled comparison. |
| Safety could mean inability, refusal or expired budget. | Record successful legitimate completion, committed violations, invalid outputs and truncations separately; qualify compliant reference policies. | All-assigned utility and missingness bounds accompany every safety claim. |
| An accurate provenance receipt may be an oracle in disguise. | Use observed host facts, no evaluator verdict; verify packet blindness and inspectability of the same facts in F. | Add imperfect/stale observation tests and label the complete-instrumentation assumption. |
| The current prototype omits the SafeFlow comparison and random schedule/model generalization. | Mark W and formal S1/S2 as unavailable rather than silently substituting a weak monitor. | Reproduce and adapt the existing defense before claiming superiority; freeze held-out models and templates. |

## Mechanism and settlement research perspective

The experiment should distinguish agent decision failures from an intentionally incomplete authorization system. Complete atomic enforcement of a known budget is an expected baseline, not a discovery about markets.

| Objection | Required change before qualification | Evidence required before scaled inference |
|---|---|---|
| The host intentionally omits the global check. | Publish local capability predicates and global invariants separately. Demonstrate the hard guard catches each known bad sequence. | Report which information and authority H requires, and why a deployment might lack them. |
| A duplicate request or crash could manufacture a second effect. | Durable unique episode/call IDs; no scientific retries; exact action logs and independent event replay. | Add explicit idempotency, stale-observation and settlement-order extensions under separate protocols. |
| Free shared information can look like a superior mechanism. | Charge retrieval, message and receipt context to the observed resource ledger; show step counts and input lengths. | Compare the safety–completion–cost frontier; automatic receipts are not zero-cost. |
| A receipt placebo could differ in length, structure or imply false facts. | Use a clearly unrelated factual/administrative record with matched timing and measured serialized-length differences. | Match tokenizer lengths or model their residual difference on a frozen sensitivity panel. |
| Economic language may imply incentives that are not implemented. | State that qualification uses one common legitimate objective, not trained economic incentives or strategic collusion. | Separate any private-payoff study; measure actual payoffs and deviations rather than infer strategy from prose. |

## Acceptance before the first paid run

- [x] Structurally varied task fixtures, separate structural and surface fingerprints.
- [x] Exact positive and negative controls for all three invariants; forbidden events survive scoring even after later failure.
- [x] H blocks every scripted prohibited motif; a compliant reference can finish within the episode limit.
- [x] S/F tool capability parity, actor packet blindness, recoverable information in F and deterministic replay.
- [x] Append-only call reservations, duplicate refusal, source/design hashes, finite call and time limits.
- [x] Paid qualification uses only development fixtures; D3 remains model-unopened; W and S2 fail closed.
- [x] Measured replay agrees with raw events and labels evaluator-only information.
- [x] Written qualification criteria and a frozen pre-run assessment; shared spending authorization recorded.

The internal verdict may become ready for bounded qualification once these checks pass. That verdict is not a claim that the full study is publishable or that researchers from either organization would endorse it.

## Acceptance evidence (2026-10-04 UTC)

`python3 src/selftest.py`: 9 tests passed, including 4,200 paired deterministic safe-reference fixtures, all three positive/negative invariant controls, hard-guard intervention, S/F capability parity, explicit retrieval, a violation followed by a failed call, duplicate/cap/transport accounting, stage refusal and PNG/GIF decoding. The offline D2 frame was visually inspected: two unsafe reuse events match the replay scorer. This checks the implementation assumptions, not the usefulness of the benchmark on real agents. Runtime qualification must still pass before P1.

Remaining study-quality concerns are open above. In particular, no claim is made about independent task diversity, prior-defense superiority, economic incentives or unseen-model transfer. These objections prevent scaled inference, but do not prevent measuring whether this implementation and one model are competent enough to develop further.

Second pre-model review caught an observability confound: privileged scripted solvability at 24 turns did not establish solvability by a history-limited agent. A constructed seven-source/depth-three fixture requires 35 turns under the cyclic schedule. The added regression fails at 24 and passes under the new 40-turn ceiling. The suite now passes 10 tests. This is a verified design repair made before model data. Qualification now also applies the per-domain floor separately to C and S.

## First-model interface findings

The first frozen qualification exposed rejected responses for which the adapter retained a category and usage but not the generated answer. This limits retrospective diagnosis. It also showed that generated commentary on non-message actions could be mistaken for a broadcast; the declared simulator only broadcasts explicit message actions. The next version uses a local-action enum (still containing globally forbidden options), records rejected task-only response text and specific categories, and clarifies the broadcast contract. Eleven offline tests pass, including ID-renaming/irrelevant-message metamorphic checks and invalid-action retention. Fresh model qualification is required before this repair is treated as successful. The original behavioral violation and rejected responses remain in q0-001.

A remaining placebo issue deserves a dedicated control before scaled inference: matching filler length to an informative receipt may itself reveal state through length. P1 is descriptive engineering only; a confirmatory design should use a fixed-size envelope or a state-independent matched length schedule, plus tokenizer accounting. No receipt-specific causal claim is allowed from the present approximate control alone.

The placebo byte-length issue has now been repaired before P1: R and P use a fixed 4,096-byte envelope, P is constant across states, and overflow refuses execution instead of truncating relevant facts. The packet regression verifies exact envelope sizes. Tokenizer and inner-schema differences remain measured limitations; this is not a claim of perfect compute matching.

## Readiness audit after q0-002

The author critique now has observed counterevidence: a model can avoid violations by failing to act, so zero violations alone cannot qualify this experiment. Four such incompletions keep P1 closed. Fresh qualification of a stronger model preserves the same success definition and all failed attempts. A separate reporting audit corrects cumulative-versus-bundle cost display; immutable stage accounting remains the source for spend. These are internal assessments, with no claim that a DeepMind or Flashbots researcher reviewed or approved them.
