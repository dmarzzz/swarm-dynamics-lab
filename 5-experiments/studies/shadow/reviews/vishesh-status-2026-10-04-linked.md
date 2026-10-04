# Vishesh status text, 2026-10-04 22:19Z: Shadow's link-fixed copy

**This is Shadow/Sol's copy of Vishesh's status message** (Discord attachment `2219_message.txt`, posted 2026-10-04 22:19Z). **His words are unchanged.** The only edits are the four `[Evidence](...)` links, which pointed at local machine paths (`/Users/ultron/...`, `/private/tmp/...`) and now point at the same files repo-relative so they resolve on `main`. Verification of studies 1 and 3 against main, offline re-runs and reviewer objections are in [vishesh-theseus-telephone-2026-10-04.md](vishesh-theseus-telephone-2026-10-04.md).

Link map (original -> repo path):

| Study | Original local path | Repo path on main |
|---|---|---|
| 1 Theseus | `/Users/ultron/Documents/ChatGPT/Grove Swarm Hackathon/swarm-of-theseus/execution-diagnostic/sol50/Q2-POST-MORTEM.md` | `5-experiments/studies/vishesh/swarm-of-theseus/execution-diagnostic/sol50/Q2-POST-MORTEM.md` |
| 2 Influence | `/private/tmp/swarm-pi-review-publish/researchers/vishesh/notes/influence-swarms/scenario/LATEST-RESULTS.md` | `5-experiments/studies/vishesh/influence-swarms/scenario/LATEST-RESULTS.md` |
| 3 Telephone | `/private/tmp/swarm-pi-review-publish/researchers/vishesh/notes/telephone/native/b2/results/POST-MORTEM.md` | `5-experiments/studies/vishesh/telephone/native/b2/results/POST-MORTEM.md` |
| 4 Immune | `/private/tmp/swarm-pi-review-publish/researchers/vishesh/notes/immune-response-v3/controller-study/c1/reviews/c1-post.md` | `5-experiments/studies/vishesh/immune-response-v3/controller-study/c1/reviews/c1-post.md` |

Newer evidence on main that post-dates this text (not edited into his words, listed here only): study 1 `.../sol50/baseline-replication/C2-POST-MORTEM.md` (23:08Z); study 3 `.../telephone/native/b4r1/results/POST-MORTEM.md` (22:46Z).

---

Our four priorities are Theseus, Influence, Telephone, and Immune Response. They remain promising research directions; none yet establishes a general swarm advantage. Latest recorded state as of October 4:
1. Swarm of Theseus — can useful knowledge survive replacing the team?
- Design: Agents learn local rules and whom to consult, then transfer knowledge to replacements. The intended comparison is interactive handover versus written notes, no inheritance, and retaining the original agents.
- Learned: In one five-agent world, consultation achieved 30/30 correct decisions, and one successor achieved 6/6. A single handover worked; full-team turnover remains untested.
- Went well: Trace review identified a routing bug, and the repaired protocol completed successfully with no harmful approvals.
- Didn’t: The inherited note already contained enough information, and a simple controller also scored perfectly. We cannot credit dialogue or “culture.” A later qualification stopped on an API request error.
- Latest: The C1 transport repair passed. A repeated, four-condition turnover experiment is being prepared; its scientific qualification and larger run remain pending. [Evidence](../../vishesh/swarm-of-theseus/execution-diagnostic/sol50/Q2-POST-MORTEM.md)
2. How to Win Agents and Influence Swarms — does advocacy spread through peer advice?
- Design: Give agents procurement evidence plus neutral or promotional framing, then compare peer discussion with private reconsideration and a simpler full-evidence analyst.
- Learned: Earlier 10-agent and 50-agent pilots selected the correct supplier, but every adviser deferred. Final decisions worked; the experiment did not meaningfully test peer influence.
- Went well: Evidence acquisition and final decision checks were accurate, and detailed traces exposed why the social comparison was uninformative.
- Didn’t: One synthetic world, universal adviser abstention, and model differences prevented conclusions about persuasion resistance or swarm size.
- Latest: B1 is reported running its qualification stage, with evaluation conditional on passing. It uses 30 authored dossiers—six development and 24 evaluation cases—with fresh repeats and stronger controls. No completed B1 scientific result is available yet. [Evidence](../../vishesh/influence-swarms/scenario/LATEST-RESULTS.md)
3. Telephone — what gets lost when agents pass information along?
- Design: Compare three-hop handoff chains with and without access to the original source, across 12 cases and two fresh repetitions.
- Learned: Both conditions preserved every final decision, but meaning degraded. Source access preserved roughly 4–5 percentage points more source meaning on this benchmark.
- Went well: 146/146 calls completed validly, and the full semantic audit identified concrete losses involving provenance, version qualifiers, and conditional rules.
- Didn’t: Agents received the previous answer and answered the same question, so they could copy a correct decision despite losing its supporting evidence. Cases also permitted lossless copying.
- Latest: B2 is complete and reviewed. Proposed B3 gives a fresh reader a new downstream question without previous answer fields, testing whether lost details actually impair useful work. It is not yet funded or launched. [Evidence](../../vishesh/telephone/native/b2/results/POST-MORTEM.md)
4. Immune Response — can agents repair failures without harming healthy systems?
- Design: Agents diagnose and repair simulated services. Latest C1 compared action-first versus justification-first outputs across four incident cases.
- Learned: Both repaired genuine failures, but both unnecessarily intervened on a healthy service because they trusted stale evidence. Justification-first eliminated one action/explanation contradiction without improving overall success.
- Went well: All 32 calls completed, and trace review pinpointed evidence freshness as the practical weakness. A simple rule controller solved the cases offline.
- Didn’t: Both conditions passed only 3/4 service gates and 2/4 combined diagnosis/outcome gates. Healthy final status concealed unnecessary intervention; four cases without repeats cannot establish reliability.
- Latest: C1 is closed and failed qualification. The next verification study has offline validation: six paired incident roots, fresh repeats, and guarded versus unguarded agents. Its 192-call native experiment remains unfunded and unlaunched in the latest records. [Evidence](../../vishesh/immune-response-v3/controller-study/c1/reviews/c1-post.md)
