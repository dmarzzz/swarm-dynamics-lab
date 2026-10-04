# Pre-run assessment: Theseus v2 S0

- Experiment / owner / stage: swarm-of-theseus-v2 / vishesh/codex-theseus / exploratory S0.
- Parent: v1 S1, reviewed in ../redesign/REVIEW.md and ../redesign/structural-audit.json; no v2 attempt yet.
- Status: blocked
- Blocker: new USD 15 API authority and reservation are not approved; the existing USD 45 authority has USD 0.097684 unreserved. No host is held while blocked. A new exclusive allocation, deployment verification and public registration remain launch gates.
- Practical question: can a reader infer these bounded procedures from historical outcomes, and can the model execute each clean current rule before a turnover experiment is attempted?
- Expected finding: competence ceiling passes and historical acquisition is possible. A low learner score is a qualification failure requiring a documented repair, not evidence against cultural continuity. Ceiling or missing-output failure also blocks S1.

## Design and assessment

Closest evidence: v1 supplied-rule transmission, plus the scoped X/prior-art review in ../redesign/SOCIAL-GROUNDING.md. This is not a completed novelty gate. Current-rule reader is the strongest qualification comparator; a budget-matched single-controller scientific comparator is not implemented.

Units: two seeded worlds per scenario, paired learner and explicit-rule reader, stable and changed/interface checkpoints. Six cases per call; cases and calls within a world are dependent. Seeds 300/301 are initial qualification; 302/303 reserved for at most one justified repair; 400/401 withheld for S1. Finite patterns overlap between training and evaluation; IDs and combinations vary. This tests procedural application, not out-of-domain generalization.

The learner gets historical accepted outcomes, not a founding rule. Only the ceiling sees the current rule. Current labels are withheld from learner payloads. Source truth and a separately implemented raw-response scorer agree on software fixtures. Mutation controls reject stale rules, summary-only decisions, universal precaution/inaction and obsolete commands. Schema failures and provider failures retain separate reasons.

Gate: ceiling >=0.90 action accuracy in each scenario at each checkpoint; learner stable >=0.75 per scenario; all 24 outputs must satisfy schema. Changed learner score is descriptive, not a success gate. This implementation is stricter than a ceiling averaged over checkpoints; it prevents clean old-interface performance hiding inability to use the new console. Prospective, before any model output.

## Changes and unresolved issues

| Issue / prior evidence | Change | Acceptance check | Status |
|---|---|---|---|
| Supplied founding rules | Historical labeled cases | No rule in learner/crew payload; ceiling explicitly separated | Offline passed; model competence untested |
| Founder-only inheritance | Two complete waves | Generation 1 only by step 4, generation 2 only by step 7 | Offline passed |
| Instant relearning could dominate | Common interruption after step-5 outcome | No feedback in step 7-9 actor inputs | Offline passed; effect unmeasured |
| Old plan cache accepted | Exact uncached URL/revision/hash | Wrong revision and hash rejected | Offline passed; public registration pending |
| Provider failures lost | Durable call-start/result files with safe reason | HTTP/type reasons, no secrets, conservative denominator and bounds | Adapter not paid-qualified |
| Copying versus applying tool instructions conflated | Current command validity and intended semantics separate | Old tokens invalid but interpretable | Offline mutation passed |
| Missing swarm-specific comparator | Explicitly defer single-controller replication | No claim of swarm advantage | Open research limitation |
| Model-family portability | Interface change only | No cross-model claim | Deferred |

## Frozen execution plan

Protocol: ../PLAN.md plus prospective amendment. Source/config/instrument hashes are recorded in the dispatch manifest, selected from the clean published commit after offline validation. Model: claude-haiku-4-5-20251001; temperature 0; max output 900; max encoded input 18,000 bytes. Native Anthropic structured JSON; no transport/semantic retries. Python 3.12 and Pillow 11.3.0 are the deployment targets; verify actual versions before dispatch.

Command from the clean repository: `python3 researchers/vishesh/notes/swarm-of-theseus/v2/src/runner.py --stage S0 --config /srv/swarm/theseus-v2-config.json --receipt /srv/swarm/theseus-v2-deployment-receipt.json --output /srv/swarm/theseus-v2-results/S0`. Secure deployment creates those non-secret config/receipt files only after authorization and allocation.

S0: 24 calls. One repair: another 24. S1 after qualification: 612. Total maximum 660, USD 15, two concurrent worlds, a shared two-hour deadline persisted in the quota ledger. This is a hard ceiling, not a promise to spend it. Conservative byte bounds may stop before the maximum call count; no refund or silent extension. Model pricing checked 2026-10-04 UTC at https://platform.claude.com/docs/en/about-claude/pricing: USD 1/M input, USD 5/M output; no caching or batch discounts assumed.

Stop on process/resource gate failure. Preserve assigned manifests and partial outputs; do not count missing comparisons as known zero effects. Provider/semantic failures remain in the qualification denominator. Any repair needs a prospective revised review, fresh reserved qualification seeds, and the same remaining allocation. No S2.

Credentials: existing local Keychain alias `swarm-lab-anthropic`, consumed only by an authorized local process and passed securely into worker memory. No value in arguments, reports or logs. Dedicated host/claim: pending, cannot borrow another experiment's active machine. Artifact destination: public Git/Flight Deck for replay and report; hub progress/final PNG where supported.

Gate decision: blocked, not attempted. After explicit budget approval, reserve it in the central authority, obtain a fresh dedicated fleet claim, update this assessment with exact deployment, publish/register immutable plan and review, verify the page, then execute S0. S1 gets a separate pre-run assessment after qualification is reviewed.

## Visualization mapping

Mapping v2.1, bound to each manifest run/scenario/seed/arm. Logical steps 0-9. Crew generation, onboarding archive hash and replacement ID map to roster cards; steps 2-7 mark the six replacements; step 5 marks rule/interface change; steps 6-9 mark delayed feedback. Class A/B correctness divided by assigned cases maps to orange/green time traces. Missing observations remain marked and gaps break traces. Raw command validity and semantic intent remain distinct summary metrics.

Each case panel shows actor-visible summary/evidence/command and separately labeled evaluator-only accepted action and outcome. Archive text and parent hashes are recorded, not reconstructed from labels. Replay has world/arm selector, step cursor and play/pause. Live fallback is acknowledged hub progress per saved step; final output is 1800x1000 PNG and a standalone HTML replay. The hub cannot embed arbitrary HTML: deliver the replay through the artifact registry or local file, never pretend it is a native hub animation.

Record all events, no downsampling. No real-time PNG upload is yet wired into the worker; measured progress is the supported live fallback. Rendering failures are artifact failures, not scientific nulls. Owner verifies initial/change/final states, controls, missing states, metric agreement and persistent fixture watermark before launch. Unit-fixture replay is explicitly SCRIPTED — NOT MODEL EVIDENCE and cannot be presented as results.
