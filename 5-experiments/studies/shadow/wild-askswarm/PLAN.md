# AskSwarm analysis plan, 2026-10-04

Status: exploratory descriptive tooling, specified after schema inspection, before computing outcomes.
Agent: shadow/sol-askswarm. No model calls or paid API use.

## Questions and scope

Given records (agent_id, time, text[, thread]), report lexical first occurrence and distinct
observed adopters per text cluster, time to k observed identities, lexical dissent/revert
marker fractions, near-term reuse credit, participation Gini, and observed identity span.
These are measurement proxies, not causal influence, verified agent identities, semantic ideas,
or organism lifetimes. Do not convert missing times to sequence numbers or unknown actors to
unique row ids. All unavailable quantities must be null, with coverage denominators.

## Inputs

- collusion.wiki revisions.jsonl.gz: full revision snapshots; label is a claimed handle, time is
  the publisher-selected clock, page_id is thread. Retained old text can look like adoption.
- SwarmTraces redacted.jsonl.gz: payload, response and recovered_text artifacts. Schema inspection
  found no top-level actor field and null time_utc. Do not extract unverified names or embedded
  dates from hostile payload text. Cluster content, but report identity/time questions unavailable.
  The artifact kinds are not three classes of agent, and parent_id is not an actor.
- swarm-lab git history frozen at 4959a80b2e48050066630c5d22ea5d1fa1b0beb2: non-merge commits;
  explicit bracketed researcher/agent prefix only, exclude bot from actor analysis. Git author
  time is an observed timestamp, not guaranteed event order. Claim/done subject events form
  a separate table, not additional commits in the participation denominator.

## Method fixed before run

Normalize Unicode, lowercase, word tokens; compare word-trigram sets with deterministic 64-permutation
MinHash LSH (16 bands of 4) to propose candidates, verify Jaccard >=0.7. Assign to one fixed
representative, not unrestricted transitive components. Exact normalized duplicates always match.
Fewer than 6 tokens do not cluster except exact duplicates. Long texts use at most 512 evenly
spaced word trigrams (a documented approximation). Run sensitivity at Jaccard 0.5 and 0.9 if time permits.
First movers are earliest dated known identities, ties retained; never a claimed source of invention.
Time to k includes the first identity, k=2,3,5,10, and is null when unreached; right censoring is explicit.
Influence proxy: each newly observed identity in a cluster contributes fractional credit to prior
known distinct identities within 100 intervening globally sorted, dated records; ties do not create
causal ordering. Participation Gini includes observed nonmissing identities only. Identity span is
last minus first recorded activity, including zero for singletons. Dissent/revert are separate
lexical regex flags, not validated behavioral labels.

## Outputs and checks

Synthetic fixtures for adapters, temporal ties, repeated same-identity posts, censoring, missing
coverage, determinism, HTML escaping and known Gini. Commit code, source checksums, aggregate JSON,
HTML reports and a one-page FINDING.md, never raw records/text from source datasets. No inferential
claim or significance test is planned. Full-corpus descriptive fractions get no IID confidence
interval; naive row bootstrap would misstate uncertainty under clustered selection.

## Novelty boundary

Do not claim a new finding of copying on collusion.wiki (arXiv 2609.09150), nor village persuasion
or cascade results. The deliverable is one honest measurement interface applied to two public
artifact corpora and our own research swarm, with missingness visible rather than filled in.
