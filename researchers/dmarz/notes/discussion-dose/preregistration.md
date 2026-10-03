# Exploratory protocol declaration

This is not a completed preregistration. No accepted hypothesis exists for this study, and S2 is disabled. The plan and code are committed before fleet smoke collection. Local self-tests are engineering checks, not experimental findings.

## Question and contrast

SEC-47 discussion-dose extension; see README. Candidate primary contrast: the clean-adjusted attack-target win difference at six versus zero rounds. One- and three-round trajectories, memory persistence and revision rates are exploratory. All configured conditions are reported.

## Units and assignment

World is the clustering unit; episode is world × replicate × exposure × communication dose. Agent votes and messages are not independent observations. Acquisition snapshots are shared across doses within one exposure condition. Worlds, allocations and arm order are seeded. Hosted sampling need not be deterministic.

## Fixed initial design

Three agents, three options, one initial contaminated digest delivery, three verification reads per agent before discussion, 0/1/3/6 rounds, 150 words per post plus bounded claims, private probes, strict-majority decision and memory rule. Task IDs and seeds are in design.yaml. Twelve S1 worlds produce 96 episodes with one repetition; they are not 96 independent worlds.

## Exclusions and failures

No outcome-based exclusions, model repair calls or automatic episode retries. Invalid outputs remain in all-assigned denominators with explicit invalid-outcome bounds. Hard crashes are reconciled against the planned manifest. Additional attempts get a new batch ID and a dated explanation; never overwrite earlier outcomes.

## Confirmation prerequisites

Survey/hypothesis acceptance; independent task review; pinned model and budget; qualified clean performance; holdout template design; S1-based power or precision analysis for a reviewed minimum effect; frozen scorer and analysis; explicit one-time holdout guard. No sample size or inference threshold is claimed to have passed these requirements.

## Amendments

2026-10-03: Initial engineering implementation uses new constraint fixtures inspired by HiddenBench rather than copying native benchmark cases. It guarantees a controlled initial exposure, freezes verification before discussion, and measures private ballots on disposable contexts. These choices narrow the earlier conversational proposal. User explicitly requested deployment and validation first, deferring paid model runs.
