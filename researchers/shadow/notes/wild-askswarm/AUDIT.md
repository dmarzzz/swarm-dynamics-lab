# Blinded direct-text audit of 30 claimed reuse/adoption links

**Result: the tool finds repeated text, not verified semantic adoption.** All 15 sampled git
links were administrative `sync: N file(s)` boilerplate. In the wiki sample, 10/15 linked
pairs repeated task-specific content across different page roots; 5/15 were same-page
snapshots, including both pairs containing apparent coordination prose. None established
the specific directed endorsement/adoption link. That is missing evidence, not a measured
zero adoption rate.

## Sampling and blinding

- Fixed seed `202610041114`, simple random sample without replacement of 15 directed links
  from 5,668 wiki candidates and 15 from 115 git candidates. Unit is a prior-identity to
  first-later-identity credit link, not independent actor, root or idea. SwarmTraces has zero
  eligible links because all actor/time fields are unavailable; it contributes no audit cases.
- Link generation exactly follows the baseline .7 cluster / 100-step credit rule. Within
  each eligible prior identity, the most recent qualifying record supplies the inspected text.
- A/B order randomized; metadata identities, source names, clock order, scores, ranks and
  root relationships withheld. Selected endpoint handles were masked inside text. Third-party
  sign-offs, embedded non-ISO task clocks, page names and genre remain recognizable.
  **This is partial blinding, not a fully blinded independent test.**
- Reviewer: the operating assistant, shadow/sol-askswarm, reading pairs directly rather than
  using a classification script or another API. **Not a human review and not an independent
  reviewer.** All 30 pairs were read. B02 exceeded the initial excerpt limit; its omitted
  middle was read before labeling. Final judgments did not rely on truncated text.
- Judgments were written and committed before opening the source/root key. See
  [locked judgments](results/robustness-v1/blind-judgments.json). The unblinding output links
  them to derived source IDs and hashes, with no raw dataset rows exported:
  [audit.json](results/robustness-v1/audit.json), [sampling](results/robustness-v1/audit-sampling.json).

## Precision, with the target stated explicitly

| Audited target | Wiki | Git |
| --- | --- | --- |
| Visible lexical match, including boilerplate | 15/15 = 100%, nominal Wilson 95% 79.6-100% | 15/15 = 100%, 79.6-100% |
| Task-specific content match, not sync boilerplate | 15/15 = 100%, 79.6-100% | 0/15 = 0%, 0-20.4% |
| Task-specific repetition across different roots | 10/15 = 66.7%, 41.7-84.8% | 0/15 = 0%, 0-20.4% |
| Verified directed semantic adoption or endorsement | Unestablished, precision unavailable | Unestablished, precision unavailable |

The **66.7% wiki and 0% git figures are precision for cross-root task-specific repetition**, a
narrow descriptive proxy, NOT precision for causal influence. The cross-root condition was
applied after the blinded text judgments using the held-out provenance key. The nominal Wilson
intervals describe small link-sampling uncertainty conditional on these judgments, not rater,
identity, causal or cluster uncertainty. Repeated content families are not independent ideas.
We do not pool the 15/15 strata as if the two corpora had equal candidate populations.

## What the pairs contained

- Wiki: 13 pairs of task-specific URL/query payloads, 2 pairs of coordination discussion
  embedded in page snapshots. Five pairs were same-root revisions: B02, B06, B10, B15, B27.
- Both prose pairs, B10 and B27, showed retained discussion plus appended updates. Their
  surface content is consistent with claimed coordination, but a snapshot comparison cannot
  identify which statement the sampled editor authored or endorsed.
- Ten cross-root wiki pairs all involved repeated query/link payloads. Four pairs repeated
  the same investor-data query-list family. A shared task, common prompt, copied template,
  one controller or active copying could each explain the repetition. The corpus does not
  disambiguate these explanations for the specific directed link.
- Git: all 15 were identical one-, two- or three-file sync notices. These are real lexical
  matches but unsuitable as evidence that one research agent adopted another's idea.

**Copied text is not endorsement. Absent outcomes are not failures. Synthetic identity counts
are not autonomous agent counts.** Specifically, collusion.wiki labels and SwarmTraces names
are unverified strings, potentially shared, spoofed or scripted. AskSwarm does not extract
SwarmTraces names from hostile text or promote artifact parents to actors.

## Consequence for reporting

Keep “first observed handle”, “repeated phrasing” and “cross-root lexical reuse”. Do not label
the credit table a causal influence ranking or infer semantic adoption from high precision for
literal matching. A genuine adoption-precision estimate still requires provenance-aware
editor/action attribution and an independent annotated gold standard. This small audit does
not supply either, and no absent outcome is recoded as a failed action.
