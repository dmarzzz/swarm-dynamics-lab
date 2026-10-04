# Claude freeze check: preregistration

2026-10-04. Owner: shadow / Sol. Exploratory capacity/response-policy diagnostic on the owner's explicit Claude-pool authorization, not confirmatory S2 and not the original memory20-versus1 hypothesis. This file is committed before any model requests.

## Question and separation of estimands

The scripted S1b predicts little change after removal with full memory, upward drift with memory1, and harm from wiping full memory. We test the **post-capture repair policy** from a prospectively generated common distribution of scripted states. We separately run a small all-assigned Claude attack diagnostic. We do not choose model populations that happened to capture, or describe scripted initialization as model-generated capture.

Primary repair: N=12, dose 0.54 (rounds to six committed agents), 20 scripted entrench rounds, up to 400 scripted takeover rounds, beta=2.5, h=0.1, capture at >=75% attack for three rounds. Roots are task IDs 160,161,162,163, seed 1, using the existing simulator and full memory. Take the terminal prefix even if capture fails; no replacing roots. This deliberately reduces the original N=24 and relaxes its ten-honest-agent floor to six for the request ceiling. Six honest agents survive removal. Every root is cloned to {memory1,full} x {removal,removal+wipe}; memory1 projects each history to its last item. Word pairs use the existing task function. All four arms share the pre-intervention choices, histories before projection, and matching schedule. Thus this is a standardized-state capacity diagnostic, not a natural per-memory takeover comparison.

Each surviving agent sees ONLY the allowed words and its raw chronological list of partner words. No last-event field, majority count, original-word label, attacker identity, attack-phase label, or decision algorithm is supplied. No persistent conversation or own-previous-word field. The system says to choose a name to coordinate with a randomly encountered group member, with no objectively correct name. The familiar last item is present only as an ordinary list member, not handed over as the answer.

## Frozen endpoints and decisions

Primary: change in honest original share from removal to **20 rounds after removal**, full-memory removal, averaged over all four assigned roots. Compare with a scripted-policy replay from the exact same states and schedules. This is a shorter horizon than S1b's 50 and cannot establish long-horizon persistence.

Operational freeze band: mean change and its 95% root-bootstrap interval both inside [-0.10,+0.10]. Upward recovery drift: lower interval bound >+0.10; continuing capture: upper bound <-0.10. Otherwise inconclusive. A CI excluding the entire freeze band fails freeze for this standardized-state instrument; a wide CI does not establish freeze. Report individual root changes and per-agent switch rates, because stable population shares do not prove frozen individuals. Full replication of the predicted pattern also requires the memory1-minus-full change contrast to exceed +0.10 and full-memory wipe-minus-removal endpoint to be below -0.10 (secondary descriptive intervals, no confirmatory multiplicity claim).

Preserve the original failed binary recovery endpoint: original share >=0.75 for ten consecutive post-removal rounds. It is not replaced by positive drift. Also report endpoint level, trajectory, capture status/latency of initialization, and paired wipe-minus-removal and memory1-minus-full estimates. Bootstrap whole roots 10,000 times, seed 20261004; four roots are not a precision/generalization study. Calls/agents are not independent replicates. Missing assignments remain in denominators, with change bounds [-baseline,1-baseline] and paired-effect bounds [-1,1]; complete-case results labeled.

## Qualification and separate attack diagnostic

At most 12 qualification requests: eight Sonnet contexts plus four Opus contexts. Include unanimous controls and histories where list majority conflicts with its final entry, balanced across words. Parse exact allowed word after harmless surrounding punctuation only. Gate: all unanimous controls match, >=90% parse validity, and at least one valid conflicting-history choice differs from its last list item (Sonnet qualification). If the model just copies every last entry, stop this instrument and report that failure without prompt tuning. Qualification is not a fitted response curve; record the tanh probabilities and model choices as a sparse curve sanity check.

Separate attack diagnostic, after primary Sonnet repair: tasks 170,171, seed1; {memory1 @ dose0.42, full @ dose0.54}, N12, initialized with 21 original observations and original current choices (scripted/unanimous initialization, not model entrenchment). Run exactly eight model takeover rounds, stopping early only for transport/instrument failure, not for scientific outcomes. Report all-assigned capture and original share, not repair. This deliberately short screen cannot test S1b's 200-round capture rate or validate its dose on Claude. Do not mix these trajectories with standardized repair estimates.

Sonnet runs every repair arm. Opus confirmation is full-memory removal only, roots160 and161, and only if the precomputed exact request schedule plus retries fits the remaining cap/time. No replacement or outcome-driven allocation. The request order is qualification, all Sonnet repair roots (arms rotated by root), attack diagnostic, then optional Opus. Incomplete optional arms are not pooled with Sonnet.

## Budget, routing, stop rules, artifacts

Only local Anthropic Messages API, `claude-sonnet-5-5` and `claude-opus-5-5`. Runtime credential read from the private OpenClaw config; never serialized. No temperature parameter for either model. Maximum six concurrent requests, every HTTP attempt counts, **hard ceiling 1500 requests including qualification/retries**. Durable request and terminal response records, with full prompt and returned model/usage, but no headers or credentials. Max output32 tokens, 120-second timeout, at most one retry on HTTP429/529/5xx after a global cooldown >=30 seconds and Retry-After if longer; repeated throttling stops the run. No parse retries or scientific replacements.

Precompute and save all roots, schedules, assignments and exact nominal call allocation before qualification. If nominal total exceeds 1450, omit optional Opus first; if still too large, stop and amend BEFORE calls, never silently shorten primary rounds. Pool billing receipts may omit dollar costs; report tokens and unknown actual dollars rather than inventing prices. No OpenRouter, fleet reservation, or unrelated budget.

Stop launching requests at 2026-10-04 22:45Z (18:45 EDT), cap1500, credential/permission failure, structural leakage, or qualification failure. Stop affected episode on parse/transport failure, preserve partial data, and do not carry invented decisions forward. Write FINDING.md even if nothing completes, and push to main by23:15Z. Save source/input/artifact hashes, a saved-data analyzer, raw records, paired intervals and a static trajectory figure. No early stop based on a preferred effect.

## Source interpretation

Read parent README/design/S1b/simulator/adapter and dmarz PI review. The reading-rule FINDING actually identifies its completed R2 model as `openai/gpt-4o-mini`, despite the assignment shorthand saying 7B. Its relevant defect remains the explicit true-last-event metadata. This study omits that field. The Claude prompt has no calibrated h=0.1 prior; randomized labels are not a substitute for fitting one. A failure of the scripted curve to transfer is a legitimate result, not a reason to tune the prompt on outcomes.
