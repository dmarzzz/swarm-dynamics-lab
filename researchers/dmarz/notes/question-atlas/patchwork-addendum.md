# Patchwork Heist: candidate hypotheses for swarm research

Owner: dmarz/patchwork-hypotheses. Added 2026-10-04 UTC at the user's request to add the diamond-heist connections to the research page and GitHub. **These five additions are unreviewed hunches for selection.** They do not promote a formal hypothesis or authorize an experiment. The existing survey and independent-review gates still apply.

## New candidates and the questions they extend

| ID | Candidate | Relationship to existing work |
|---|---|---|
| [SEC-54](https://swarm-research.pages.dev/#/questions?id=SEC-54) | When permitted specialist actions compose into a forbidden outcome | SEC-04 addresses authority changes at return. This tests whether already-granted, individually valid capabilities compose across agents without any permission change. |
| [SEC-55](https://swarm-research.pages.dev/#/questions?id=SEC-55) | Causal audits when provenance is incomplete | SEC-06 concerns repair from a faulty graph and SEC-30 review queues. This tests pre-effect classification, abstention and useful completion under the same imperfect observations and review budget. |
| [SEC-56](https://swarm-research.pages.dev/#/questions?id=SEC-56) | How much finality delay buys containment? | SEC-49 measures cumulative damage despite eventual recovery. This varies the time before an action becomes irreversible against audit latency, explicitly charging legitimate work for the delay. |
| [MKT-13](https://swarm-research.pages.dev/#/questions?id=MKT-13) | Market limits with uncertain ownership and concurrent settlement | MKT-03/11 test incentives to split firms and evade fines. This tests hard-limit enforcement when ownership records are wrong or simultaneous actions race, separately from model strategy discovery. |
| [MKT-14](https://swarm-research.pages.dev/#/questions?id=MKT-14) | Evidence royalties versus identity farming | BUD-14 studies ledger coordination and MKT-09 public production information. This tests whether paying for used evidence changes costly discovery, and whether duplicated identities capture those payments. |

Search the research page for `Patchwork`, or open the linked candidate. Each card includes a prediction, comparison, measurements, falsifier, confounds and prerequisites. Existing card content and IDs are retained.

The user selected SEC-54 for deeper planning. The [compositional safety experiment plan](../compositional-safety-plan/README.md) specifies causal controls, a staged scale envelope, held-out transfer, power planning and falsifiers. It is an unreviewed working draft; the candidate's formal status remains unchanged.

## Evidence recovered from Patchwork

Source: [[gh-dmarzzz-patchwork]]. The repository and local reports were inspected with the owner's access. The GitHub project is private; the public catalogue and this limited summary make the motivation readable without implying public access to the implementation. The bypass, market and audit reports are local uncommitted extensions, absent from GitHub revision `854bdebd60579bf8b93ae1117b9bb428dcb06135`. No raw agent traces, private messages, credentials or operational data are copied here.

| Instrument | Inspected report or aggregate result | What it does not establish |
|---|---|---|
| Restriction-bypass factorial | 80 live-model runs, 16 cells, five replicates each. Fragmented intent plus local helper policy yielded 4/5 prohibited exports without the host guard, versus 0/5 with it. Across benign cells, completion was 18/20 with and 18/20 without the guard. | One model, small cells and deliberately weak local policies; no general safety result, spontaneous malicious goal or stable interaction estimate. A provider-failure/resume deviation is disclosed in the report. |
| Market-invariant conformance | 4,000 scripted cases. Prohibited outcomes: 500/500 with local checks; 500/500 with per-agent trajectory checks; 200/500 with global causal provenance; 0/500 with aggregate-state enforcement. Each level completed 500/500 paired benign cases. | A finite test of declared rules with complete host mediation, accurate owner labels and atomic settlement. No measured LLM discovery, real-world ownership detection or general economic-manipulation guarantee. |
| Asynchronous exact audit | 250 prohibited and 250 paired benign traces; repeated auditor/cadence evaluations are not independent traces. Full causal ancestry enabled complete detection in the specified motif. No reviewer prevented an immediately final effect. With an eight-event finality delay, causal audit contained 100% at cadence eight and 50.8% at cadence sixteen. | Deterministic detector semantics with complete edges. Event cadence is not wall-clock latency, and node inspections are not model-token costs. |
| Semantic audit pilot | 60 model calls on ten prohibited/benign trace pairs and three views. Causal ancestry: 10/10 detections, 0/10 benign false positives. Per-agent view: insufficient evidence on all 20 cases; recent-event window: insufficient evidence on 18/20. | Explicit rule and a three-event path, not realistic semantic understanding. Abstaining on everything is different from a useful safe policy. |
| Private-profit economy | Nine balanced 12-round cases, three per communication condition. All discovered the opportunity; six realized it; four sales were solo; zero service contracts were used. Published evidence could satisfy prerequisites for others without compensation. | No reliable ranking of communication treatments, no proof that every unpaid publisher caused a sale, and no finding that removing chat removes information exchange. The failed/retry-selected 18-round panel was withheld from that comparison. |

The source reports distinguish observations from interpretations. The free-rider explanation motivates MKT-14 but is not a tested royalty intervention. Likewise, the perfect scripted enforcement result motivates boundary tests rather than a claim that the problem is solved.

## Source fingerprints and access

These SHA-256 values identify the local inputs inspected on 2026-10-04; they provide identity, not public availability, authorship certification or independent validation. Paths below are relative to the Patchwork repository, not paths in swarm-lab.

| Input | SHA-256 |
|---|---|
| `docs/restriction-bypass-factorial-v2-results.md` | `a8de2a9b1d1b28ab04bdfb95a9bd2d6815d5de1f32e114fd4cd2c38e69bad01c` |
| `docs/market-invariant-conformance-v1.md` | `7bfa7936e6ef2aeede5b27b9f5acfd5210379ccff80f7391fcf2fb2c75729d85` |
| `docs/async-causal-graph-audit-v1.md` | `33ace3a89d0f6fdebc6dc92fe7c9afa41a94b3b51c642d71d02e45692ec67261` |
| `docs/async-semantic-graph-audit-api-v1.md` | `62be795910ae96c68ccfd13ace266bc93355633739ca15a8db399f12ce1a6f25` |
| `docs/economy-pilot-results.md` | `fd3a5c44ca56fa5dd404d3f14ef74e3bbc242ae4b17205986f75f3e7b1c1c9cc` |
| `runs/bypass/factorial-v2-luna-r5.json` | `037dadefc3a663679c9dde265ac0d87ba39bcf29c742e7852e49300d6de41fb2` |
| `runs/market/market-invariant-v1-scripted-r100.json` | `46fcb6cdfbf47f74d0333e43169f7b1e5e89bb41f13d44774536fe83ad231468` |
| `runs/async-audit/api-semantic-audit-v1-luna-r10.json` | `9d56f14e44998bfa28afbce39a5002bb5c2940df05e8c81051e7c3a96d6e0d7a` |

## Reading and promotion limits

This addition read the Patchwork reports and aggregate records, inspected its README, metadata and selected implementation checks, and read the existing catalogue entries cited by the cards. It did not rerun an experiment, fully audit the implementation, reread every cited paper, or perform a saturated novelty search. Prior-work relationships outside Patchwork are at existing catalogue depth; no read-depth field on an existing entry was upgraded.

Before promotion, obtain a reproducible permitted source snapshot, qualify the simulator with benign and prohibited controls, complete the relevant prior-art survey and independent review, and preregister assignment units and uncertainty-aware decision thresholds. Observed graph edges, true owner labels and synthetic evidence-use receipts are different objects: evaluator-only truth must not silently enter the policy being tested. Monetary values and external effects remain simulated.
