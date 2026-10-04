# B32 source capture and packet audit

2026-10-04. **Offline preparation completed for this intake; continue preparation, native launch HOLD.** No B32 or R60 call, machine allocation, cost reservation or native result was created. This is a corpus and instrument finding, not an efficacy result or a request to fund an unready run.

## What this experiment would do

Give reviewers a historical claim and the same source passages. Compare private reconsideration with seeing other reviewers' source-linked arguments, starting from identical initial answers. The practical question is whether discussion catches missed qualifiers and unsupported conclusions, or instead spreads persuasive mistakes. Stronger/more reviewers cannot rescue an ambiguous answer key. The six-reviewer B32 baseline prepares this comparison; it does not establish a 60-agent scaling effect.

## Completed intake and exclusions

The pinned AVeriTeC train/development source contains3568 claims. Before fetching:1394 development-connected records,608 with fewer than two questions,602 without the required text medium,397 with fewer than three evidence records,142 with known fact-check domains and8 placeholder/search-source records were excluded. This left417 structurally eligible rows. Deterministic label-interleaved selection chose40, skipping2 already-selected metadata components. These latter skips are selection operations within417, not extra dataset exclusions.

Attempted87 unique source locations:59 captured,28 unavailable. Initial extraction gave37 candidates some text; the stricter intermediate article/paragraph extraction gave35. Neither number measures answerability. The original [capture-only receipt](intake-pass1.json) is unchanged. Pass 1 stored original/final URLs and fallback attempts, not every intermediate redirect; its version-change flag identifies fallback, not all redirected versions. Temporal audit must use the saved URLs/raw bytes, not treat a false flag as proof of identical historical content. All40 were then read and audited in [the complete support/event log](support-audit.json):

| Packet disposition | Count | Meaning |
|---|---:|---|
| Retain as development controls |5|Original label defensible for the explicitly bounded source-packet interpretation|
| Limited; exclude from scored comparison |16|Material label, date, scope, denominator, attribution or terminology ambiguity|
| Reject current packet |19|Unavailable, wrong event/topic, missing attribution/modality, boilerplate or verdict leakage|

Retained labels:3 Supported,2 Not Enough Evidence;0 Refuted and0 Conflicting. Five distinct semantic event contexts were checked, with6 nonshared captured documents and12 bound passages. Broad pandemic context still creates correlated subject matter; distinct event keys are not proof of statistical independence or population representativeness. Every candidate has an explicit semantic event key and source-document log; metadata connected components alone are never called independent events.

Even if these development controls were eligible, the intake is35 short of40 defensible contexts, with no balanced four-class qualification set. They are deliberately development-only because the owning operator inspected and repaired their passages. **Fresh admitted B32 qualification/evaluation events:0; the frozen8+32 set still needs40.** None of these40 candidates, or their development-connected metadata groups, may be silently reused as fresh held-out evaluation. Future intake must exclude the union of the prior29 and these40 source keys before selection; review semantic connections as well.

## Representative development packets

[Manifest](development-manifest.json) separates original published verdict, packet support judgement, event context, limitations, source URL/raw hash, XPath, normalized offsets and passage hash. [Rebuilder](prepare_development.py) reconstructs actor-only packets locally and refuses a changed source, missing XPath, invalid offset or changed passage. Actor projection omits source split/index, gold, audit and original annotated answers. The actor sees publisher identity, not an archive as a separate publisher. Complete third-party articles and reconstructed passages are not republished here.

| External source key | Components checked | Bounded support and limitation |
|---|---|---|
|train:143|Named person's participation, later conversion, chronology|Biographical reporting supports the historical claim; an ordinary control, not a new independent biography verification|
|dev:82|Observed excess deaths, competing explanations, study limitations|Observed excess mortality does not identify the asserted lockdown causal contribution; uncertainty is grounded in the research discussion, not a failed fetch|
|train:682|Reported association, observational qualification|Supports the described ecological correlation; does not establish treatment benefit or causality|
|train:799|Historical sex-specific reporting and age qualification|Supports the descriptive pattern in the reported evidence; no current universal or biological-cause claim|
|train:468|Identified press conference and professional rebuttal versus platform action|Sources establish the event but do not establish the alleged ban or hoax wording; closed-packet uncertainty, not proof that no ban occurred|

All published labels are preserved. The owning operator's support audit is not independent human reannotation of these excerpts. No case was selected using a model failure, disagreement or susceptibility score. Ordinary and uncertainty controls remain even if a strong reader eventually finds them easy. Multiple excerpts from one article do not count as independent corroboration.

Repairs recovered the biography's article-body div and a research article nested inside an HTML form. Normalization preserves visible text next to removed scripts. The general-admission attendance figure was also recovered fortrain:153, but remains excluded: it does not uniquely resolve a claim about total attendance. Likewise, separate age/income margins are not a jointly measured subgroup (train:2727), and similar parking-notice terms are not interchangeable (train:2904). These are actual support failures, not reasons to force the inherited verdict.

## Implemented instrument and verification

The [fork engine](fork_runner.py) implements20 assigned calls per event: a two-turn single reader plus six initial reviewers each forked into peer and private continuations. It preserves common initial checkpoints, rotates evidence order, retains different claims on the same document, and records actor requests, returned message content, usage and all unstarted/failed outcomes. It never uses evaluator truth for the peer board. Literal quote checking is explicitly separate from semantic grading. Unknown costs retain reservations; known costs remain settled even if token/schema validation fails. Safe error codes avoid provider exception payloads. No retries or model fallbacks.

**19 offline tests pass:**13 fork/accounting tests and6 source-binding/isolation tests. [Actual development validation](development-validation.json) checks5 reconstructed packets/12 passage bindings; it is not native accuracy. [Instrument revision receipt](instrument-revision.json) preserves the pre-curation file hash and verifies unchanged prompt/board functions after the accounting repair.

[Remaining production work](INSTRUMENT-STATUS.md): authentic current-admission and original-ledger adapters, exact tokenizer and context accounting, current provider/model/usage qualification, actual route metadata, public registration, finalization and exclusive approved allocation. The fake adapters in tests confer no authority. Full schema-valid peer reports generate serialized requests of21,118–31,179 bytes on these packets. Bytes are not tokens, but this is a concrete warning that the4000-input-token contract is not yet robust. Resolve a bounded report/board contract before fresh evaluation curation and before spending, rather than silently truncating evidence or expanding costs.

## Exact proposed envelope and honest smaller scope

B32 remains1440 maximum calls:160 qualification plus640 per fresh evaluation execution, twice. At the stated unverified admission price ceiling and4000-input/2048-output bounds, API maximumUSD41.01120 plusUSD0.50 infrastructure = **USD41.51120 incremental**. This remains unfunded and is not ready for allocation. R60 is separate, unfunded, and not included or additive.

The actual assembled smaller scope is **five development contexts**, not a nominal balanced pilot. A future five-case fork diagnostic with two fresh executions would be5×20×2=200 calls, maximumUSD5.696 API plusUSD0.25 infrastructure = **USD5.946 incremental**, conditional on unchanged validated price/token bounds. It could check real-source reading, uncertainty and fork stability. It cannot qualify all four verdicts, establish a robust collective benefit, estimate60-agent scaling, or substitute for the requested scientific baseline. It is not launched or funded here; first finish context/admission integration. No claim that saved unit-test responses are fresh executions.

## Next concrete offline work

1. Repair the generic extractor to preserve article-bearing forms/divs and verify numeric/date/attribution coverage. Keep current rejects and all original labels.
2. Resolve the measured board-size risk with a prospective compact report contract, verified tokenizer and worst-case context tests, then freeze before fresh case curation.
3. Use a bounded next intake of at most40 additional source-independent candidates/120 locators, excluding all69 exposed keys and their connected components. Prioritize component-complete evidence and fresh Refuted/Conflicting cases under explicit model-independent rules, not cases expected to embarrass a reader. Stop and report yield/remaining shortfall after that batch. No API/model spending is implied.
4. Integrate authentic admission/ledger adapters and complete semantic/source support audits. Return a genuinely ready named native scope with actual counts and enforced costs before allocation. Continue in the background; this source failure is not a scientific negative or a reason to park the study.
