# Theseus R1: one bounded atomic-contract and conditional-rule repair

Status: prospective, written after D2 postmortem and before repair implementation or native responses. The current owner-directed review/change/run/postmortem cycle authorizes this bounded repair within the existing cumulative USD5. This is the single targeted repair allowed after D2, not a new budget or an automatic culture experiment.

## TLDR

Can a tightened atomic output contract and explicit incident conditional remove the residual failures exposed by D2? Compare unchanged atomic E with repaired F on six fresh fixed worlds, two task families, eight cases and two identical native repetitions. Measure assigned strict accuracy, full contract validity, release recall, false releases/activations, repeat consistency and cost. Exactly 384 calls/decisions, 192 per arm, 96 distinct case/family pairs. This bundled engineering qualification cannot isolate its two components or establish cultural preservation.

## Question and prediction

Prediction: requiring exactly one supplied ID will remove ID-copy failures; spelling out both incident branches will reduce false activation. The fixed primary contrast is world-level F minus E strict accuracy, with equal world and task-family weighting. Report every world difference and the mean. A material improvement requires at least 3 percentage points and gains in at least four of six worlds, separate from qualification. No significance or population reliability claim; six fixed worlds and repeated calls have weak generality.

## Setup

Pinned model claude-haiku-4-5-20251001, temperature zero, max_tokens 1200, no notebook/history/feedback and one case per call. E uses the exact D2 atomic request constructor. F keeps the same observations, mappings, commands and release instructions, but tightens the output schema to one decision whose ID enum contains only the supplied ID. For incident only, append: select the source from the supplied class mapping, read that source's signal, and use the explicit conditional table (false => console1/none; true => console1/<selected source>). Freshness, other sources, summary and queue do not enter the predicate. No per-case truth is calculated or inserted into actor context. This changes instruction salience and schema constraints, not evidence.

Use D2's generator with fresh seeds 7200–7205 and all six ordered mappings in the same order as D2. The inherited named RNG streams use those new seeds. Eight cases per world cover all four signal/freshness pairs per class, independently permuted irrelevant columns. Require challenge coverage for all governing sources before calls; if it fails, amend prospectively rather than silently resample. Development seeds 7000–7005 and D2 failures are offline regressions only. No D2 response is reused as a fresh sample.

## Protocol

Six worlds × two task families × eight cases × two repetitions × two arms = 384 calls. Each case is presented independently; remove the redundant atomic order factor. Each arm receives 192 decisions, 96 per family, 32 per world and 24 eligible-release presentations representing 12 distinct positive cases. Randomize all assignments once with R1-dispatch-v1. Save assignments and request hashes before dispatch. Identical repetitions must have identical request bytes. Do not adapt scheduling or prompts to results.

One worker, two hours, zero retries or excluded probes. Save starts, raw text, served model, outcomes and usage before reporting. Stop on transport ambiguity, served-model mismatch, missing usage, admission/reporting failure, claim expiry, deadline or budget cap. Preserve completed, invalid and unstarted rows. No second repair is authorized by this protocol, even if near a gate.

## Metrics

Retain D2's full-response strict scoring and independent raw-text audit. Invalid identities remain strict failures; do not retroactively credit D2's three ID mistakes. Report response presence, schema, ID uniqueness, command validity, semantic correctness and strict correctness separately. Report useful-release recall, false releases, incident false activations, per-world/family accuracy, repeat disagreement, tokens, cost and wall time. Compare matched F/E outcomes within world; do not count 384 independent tasks.

Qualification per arm: full completion and reconciled usage; 100% valid response contracts; at least 189/192 strict correct (98%), 92/96 in each family (95%), 31/32 in every world (95%), 23/24 valid releases (95%), zero false releases, and zero false incident activations. The last gate is stricter than D2 and directly targets the remaining harmful action failure. Thresholds are engineering gates, not statistical guarantees.

If F passes and E fails, freeze F as a candidate executor; describe a material repair benefit only when the separate primary contrast criterion is met. If both pass, prefer the cheaper qualifying interface. If E passes and F fails, retain E provisionally and report the adverse repair. If neither passes or execution is incomplete, close the repair line and do not start a culture run. All outcomes get a postmortem. Passing still does not establish acquisition or selective inheritance.

## Budget and launch gates

Carry forward D1+D2 estimated cumulative spend USD0.5433070437, leaving approximately USD4.4566929563. Reserve R1 once: USD3.70 model and USD0.10 infrastructure, total USD3.80 within remaining authority. With each encoded request bounded at 2500 bytes and 512 overhead tokens, a full max-output reserve at USD1/M input and USD5/M output is 384×(2500+512+1200×5)/1e6 = USD3.460608. Verify request sizes and current pricing; stop rather than exceed these bounds. Expected spend is roughly USD0.26–0.35 using D2 atomic usage, not a guarantee.

Retain the same experiment's current exclusive sim-dmarz-3 allocation only while claim and actual workload remain valid. No new cloud machine purchase. Pin clean revised source, pass offline checks on worker, bind current cumulative authority and immutable public-plan/assessment hashes, register the R1 experiment and condition TLDRs, and verify the actual public page before dispatch. Researcher review remains not required. Credentials and exact user prompts remain private.

## Closeout

Reconcile every assigned call, full scorer agreement, model route, hashes, usage and charge. Upload and read back raw evidence, CSV, summary and figure. Stop only this experiment's worker; release the existing fleet allocation after transport. Write the postmortem whether qualification passes or fails. Any later change of model, learning or culture design needs its own prospective scope and remaining-budget assessment.
