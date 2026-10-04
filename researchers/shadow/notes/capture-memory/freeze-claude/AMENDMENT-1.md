# Amendment 1: prospective OpenRouter transport relaunch

2026-10-04. Owner-authorized attempt 2, written before any request on this route. Attempt 1 and all its files remain untouched.

## TLDR

Rerun the frozen Claude qualification and, only on passing its existing gate, the frozen standardized-state repair and attack assignments. Change transport, not the scientific instrument. Route through OpenRouter `anthropic/claude-sonnet-5.5` and `anthropic/claude-opus-5.5`, the intended model families named `claude-sonnet-5-5` and `claude-opus-5-5` in the preregistration. Set `provider: {allow_fallbacks: false}` and record every returned model ID and provider. No other model, pool, or API budget is allowed.

## Question and prediction

The question, freeze band, endpoints, pairing, root bootstrap, missingness rules, and competence/non-copying gate remain exactly those in [PREREG.md](PREREG.md). Four roots are not a generalization study. The existing N=12 scripted reference does not reproduce S1b freeze: full/removal change is +0.250. This limitation is retained, not repaired by changing roots.

## Setup

Frozen `run.py`, `inputs.json`, `scripted-reference.json`, `analyze.py`, prompts, qualification contexts, assignments, histories and schedules stay unchanged. A separate transport adapter imports the frozen scientific functions. New records live only in `attempt2/`. The eight prior failed HTTP attempts remain on record, count toward nothing scientific, and conservatively remain included in the 1,500-attempt ceiling (at most 1,492 new attempts). Their unreceipted historical dollar cost remains unknown; it is not relabeled zero. The explicitly authorized OpenRouter lane has a new hard maximum of $10 in actual response-reported cost, not access to other budgets.

## Protocol

Request OpenRouter chat completions with the identical system/user text, no temperature, maximum 32 output tokens, and `usage: {include: true}`. Read the authorized key privately at runtime; never persist credentials. Record raw sanitized responses including usage/cost and served model identifier. Reject missing cost receipts or unexpected returned model family before further dispatch. Reserve conservative per-request exposure under the $10 cap, reconcile actual cost from every response, and halt at the cap or unresolved charge. Maximum concurrency six. Preserve the one-retry limit on HTTP429/529/5xx, global cooldown at least30 seconds and longer Retry-After, 120-second timeout, no parse retry or scientific replacement. Fail closed on repeated broker/server errors as well as repeated throttling; enforce the previously stated maximum12 qualification HTTP attempts.

Order: qualification (eight Sonnet plus four Opus contexts), all16 Sonnet repair episodes in the frozen rotated order, four Sonnet attack episodes, then optional two Opus repair episodes only if time, remaining attempts and budget permit. Qualification failure stops scientific escalation with no prompt tuning. Preserve partial or missing assignments in the analysis.

The owner's current relaunch instruction replaces the expired attempt-1 administrative clock: stop launching at **2026-10-04 23:30Z**, write up incomplete results honestly, and push final results by **23:40Z**. All scientific stop rules remain unchanged. This is an explicit wall-clock extension for the newly authorized transport attempt, not an outcome-dependent scientific change.

## Metrics and analysis compatibility

Use the frozen estimands, whole-root bootstrap (10,000 resamples, seed20261004), freeze criterion and scripted comparator. The saved `analyze.py` main routine is an attempt-1 closeout specialized to zero successful responses: it asserts every status is non-200 and no episode exists. It cannot honestly ingest successful attempt-2 data. Preserve it byte-for-byte, run it against a temporary copy of attempt1 for reproducibility, and import its unchanged mean/interval functions in an attempt2 reporting adapter if successful outputs exist. This is file-format/closeout compatibility, not a change in analysis. Never run its failure-only main over successful records or overwrite qualification with its hard-coded infrastructure failure.

Publication of this amendment precedes every paid route request. Transport source and offline checks will also be committed before qualification. The prior stopped run is not reopened; this is its separately authorized, fully retained successor.
