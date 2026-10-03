---
slug: attack-surface
title: "Attack surface: how an outside content injector can shape an agent swarm's choice of provider / site / MCP server"
authors: internal supporting note; roll-up across many sources, not a single-source reading
org_or_venue: internal supporting note for the SEO-poisoning proposal
date: 2026-10-03
url_loaded: see numbered reference list (all fetched this session unless marked)
status: found
fetched: 2026-10-03
---

> **attack-surface.md** — What an outside content injector can do to the retrieval channel an agent swarm reads: measured promotion effects, corpus and listing manipulation, instruction injection, and the tool/registry surface.  
> Compiled 2026-10-03. Supporting note for the seo-poisoning proposal; hunch-level, not a survey or a hypothesis.

> **Format.** `_SCHEMA.md` is one-file-per-reading; this is a roll-up over 33 readings, so each source gets a
> compact entry (what it is · what was measured · **boundary of evidence**). **Extends**
> `researchers/vishesh/notes/agent-swarm-influence-research.md` — only overlap is Nestaas et al., one table row
> there, opened out here with measured effect sizes.
> **Marks.** `[V]` = page fetched this session, numbers read off it. `[L]` = abstract read via the arXiv API
> *listing* only — weaker, never load-bearing. `unverified` = asserted in a loaded source but sourced to a
> document we could not load. The outside party is the **content injector** / **influence operator**; the
> measured quantities are visibility, selection rate, promotion rate. This is scenario modelling.

---

## 0. The chain the record actually documents

The owner's construction is "the injector adds context into the population of sites the swarm reads." The
literature splits that into five stages and the effect sizes attach to **different** stages:

```
(1) PUBLISH     (2) CRAWLED/INDEXED   (3) WIN RETRIEVAL   (4) SURVIVE RERANK   (5) CHANGE THE CHOICE
    cost: $/page    latency: unmeasured    measured §2         measured §2.4        measured §1,§3,§4
```

Nestaas et al. [1] cover **stage 5 only**: *"our work focuses exclusively on manipulating a LLM search engine
or plugin application **after** it is presented with attacker-controlled text. An end-to-end attack would also
require performing traditional SEO"* (§6.3); they pre-placed 50 pages on a domain they own. **Stages 1–2 are
the least-measured part of the threat model** — exactly where "simply add context" hides the cost.

---

## 1. Preference / ranking manipulation (persuasion; no false facts required)

### 1.1 Nestaas, Debenedetti & Tramèr 2024 — Preference Manipulation Attacks [1] `[V]`
Crafted website content or plugin documentation makes an LLM promote the injector's product and discredit
competitors. Measured on **production** systems (Bing Copilot, Perplexity) and plugin APIs for **GPT-4** and
**Claude 3**; 50 dummy pages on a domain they control; fictitious cameras/books/news plus plugin functions.
- Fake camera recommendation rate **34.0% → 59.4%**; comparable **real** cameras sat at **57.9%** (Table 1) —
  a *fabricated* option reached parity with real ones.
- **2.5×** more likely to be recommended than comparable products (Fig. 4). Plugins: **up to 7.2×** vs a
  comparable competitor; Claude 3 Opus plugin selection **0% → over 90%** (Fig. 6).
- Injection from a page they did **not** control (GitHub): **8/8** exact-phrase successes on Perplexity
  Default, **7/7** on Claude 3 Opus (§5.4, 10 trials/model).
- External injections succeeded **"at most 25%"** on Bing but *"significantly more often"* on Perplexity;
  **80% of successful attacks** stayed stealthy (§5.3).
- **Prisoner's dilemma (Fig. 5):** *"regardless of the number of parties having launched an attack, benign
  product owners have incentive to also attack rather than stay idle"*, yet *"all parties globally lose in
  recommendation rates compared to the baseline."*

**Boundary:** stage-5 only; isolated setting where the authors control every adversarial page; they state they
do not seek the most efficient attack; per-engine results differ widely; no multi-agent deliberation anywhere.

### 1.2 Aggarwal et al., GEO (KDD 2024) [2] `[V]`
First formalisation of **Generative Engine Optimization** — black-box optimisation of a page's visibility
inside a synthesised answer — plus **GEO-bench**. *"GEO can boost visibility by up to 40% in generative engine
responses"*, and *"the efficacy of these strategies varies across domains."*
**Boundary:** "up to 40%" is a ceiling over strategies and domains, not an expected effect; the abstract names
no engine or model; this is a content-creator framing, so the edits are legitimate-looking rewrites.

### 1.3 Pfrommer, Bai, Gautam & Sojoudi, EMNLP 2024 [3] `[V]`
Conversational-search ranking as an adversarial problem over **RagDoll** (**1,147 webpages**, 50 product
categories, ≥8 brands each). Models: GPT-3.5 Turbo, GPT-4 Turbo, Llama 3 70B, Mixtral 8x22, Perplexity Sonar
Large Online.
- **Baseline position bias (no injection):** *"All LLMs are significantly influenced by the input context
  position, tending to prefer product-document pairs earlier in the context"* (Fig. 8).
- Promotion from a tree-of-attacks injection (Table 1): GPT-3.5 **+3.38** (57.53% of max gain) · GPT-4 Turbo
  **+5.00** (82.94%) · Llama 3 70B **+6.02** (95.74%) · Mixtral **+4.13** (76.23%) · Sonar **+2.89** (54.23%).
- Live transfer to perplexity.ai: *"average ranking score improvement of almost 33 positions"* — with the
  injection interspersed **15 times** in the page HTML.

**Boundary:** only **2 recommender responses per attack attempt** and shallow attack-tree depth (cost limits,
admitted); not all promoted products reached top rank; no defence evaluation. The 15× repetition is the real
operator-cost signal — one sentence on one page was not what worked.

### 1.4 2025–2026 follow-ups
- **SafeGEO** [4] `[V]` — 22 attack variants × **600** recommendation cases: *"they increase the rate at which
  such flawed products enter the recommendation set by up to 83.2 percentage points (pp)"*; simple agent-side
  defences recover *"up to 39.2 pp"* but do **not** restore no-GEO performance. **Boundary:** set-entry not
  final choice; target is an *existing flawed* product; no models named in the abstract.
- **GEO-Bench** [5] `[V]` — one protocol over black-box (TAP, Zero-Shot), white-box (STS, RAF, StealthRank)
  and 10 white-hat C-SEO strategies; 5 datasets, one fixed ranker (Llama-3.1-8B-Instruct). *"black-box content
  rewriting matches or exceeds gradient-based attacks on rank promotion while producing more fluent text and
  can evade both keyword- and perplexity-based detection on some domains"*; *"the access model does not
  predict attack strength."* **Boundary:** one open-weight ranker — silent about production engines; stealth
  is per-domain.
- **Counter-GEO-Bench** [6] `[V]` — 247 human-verified queries, 3 victim LLMs. Off-the-shelf guardrails
  (Granite Guardian, Llama Guard 3, NeMo Self-Check) cut attack success by **at most 5.7% relative**, Granite
  Guardian's **not statistically significant**; their C-GEO Guard baseline gets **47.6% relative**.
  **Boundary:** benchmark baseline, not a deployed defence; relative-ASR units.
- **Chen, Wang, Chen & Koudas 2025** [7] `[V]` — AI search shows *"a systematic and overwhelming bias towards
  Earned media (third-party, authoritative sources) over Brand-owned and Social content, a stark contrast to
  Google's more balanced mix."* **Boundary:** fetched; the abstract gives **no** sample sizes or percentages.
  Directional only — but it implies the injector must place content on sites it does not own.
- **Martinez 2026 survey** [8] `[L]` — 45 studies 2023–2026: *"no reviewed technique shows stable
  cross-platform causal effect."* The key external check against pooling effect sizes across engines.
- `[L]`, not load-bearing: E-GEO, 13,747 e-commerce queries [9]; GEO-at-scale over 100k+ responses, listicles
  the most-cited format at 21% [10]; a position paper naming *"concentrated influence"* a governance risk [11].

---

## 2. Retrieval / RAG poisoning (false content, not instructions)

**PoisonedRAG — Zou, Geng, Wang & Jia, USENIX Security 2025** [12] `[V]`. *"PoisonedRAG could achieve a 90%
attack success rate when injecting five malicious texts for each target question into a knowledge database
with millions of texts."* Black-box and white-box variants; evaluated defences, found them insufficient.
**Boundary:** per-question targeting — the injector must know the query in advance; 5 texts suffice *because*
they win the top-k for that one query, not because 5 documents dominate a corpus. No LLM/retriever names in
the abstract (fetched; absent).

**Zhong, Huang, Wettig & Chen 2023** [13] `[V]`. *"50 generated passages optimized on Natural Questions can
mislead >94% of questions posed in financial documents or online forums"*; all tested dense retrievers fell to
*"up to 500 passages, a small fraction compared to a retrieval corpus of millions of passages."*
**Boundary:** query-**agnostic** and out-of-domain — the strongest "few documents suffice" result for an
injector who does not know the swarm's query; but the passages are token-level optimised, i.e. not fluent
pages, so they are precisely what a perplexity filter is built to catch.

**Trigger-gating and agent memory.** **Phantom** [14] `[V]`: *"inject a single malicious document"*, firing
only when a naturally occurring trigger token sequence appears in the query, then pursuing refusal /
reputation damage / privacy violation / harmful behaviour; tested on Gemma, Vicuna, Llama, GPT-3.5 Turbo,
GPT-4, NVIDIA Chat with RTX. **Boundary:** no success rates in the abstract (fetched); one document buys a
*conditional* effect and the trigger must appear — a strong assumption for a swarm's free-form query.
**AgentPoison** [15] `[V]`: poisons an **agent's** long-term memory / RAG store — *"average attack success
rate higher than 80% with minimal impact on benign performance (less than 1%) with a poison rate less than
0.1%"* on a driving agent, a QA agent and EHRAgent, with no training or fine-tuning. **Boundary:** needs write
access to the agent's memory, a stronger premise than the owner's scenario; closest analogue to "poison what
the swarm remembers" rather than "what the swarm reads." **Long et al. 2024** [16] `[L]`: grammatical-error
trigger at *"a minimal corpus poisoning rate of only 0.048%"*, robust to three defences.

**Anthropic / UK AISI / Alan Turing Institute, Oct 2025** [17] `[V]` — *"A small number of samples can poison
LLMs of any size."* **250** poisoned documents gave reliable backdoor success at 600M, 2B, 7B and 13B
parameters (100 insufficient, 500 most consistent); 250 docs ≈ 420,000 tokens ≈ **0.00016%** of training
tokens; the absolute count **does not scale** with model or dataset size. **Boundary:** this is **pretraining**
poisoning and a narrow gibberish-emitting denial-of-service backdoor; the authors say it is unclear whether it
holds at larger scale or for complex behaviours. Do **not** cite it as a retrieval-time result — its only
transferable lesson is the *shape*: absolute document count, not corpus fraction, governed the outcome.

### 2.4 What the operator has to pay for: rerankers and pipelines
- **Nie et al. 2026** [18] `[V]` — *"many existing attacks substantially degrade after reranking despite
  achieving high retrieval-stage relevance."* **Boundary:** no percentages in the abstract (fetched); the
  direction is the usable finding — a single-stage dense-retrieval simulation **overstates** the injector.
- **RobustRAG — Xiang, Wu, Zhong, Wagner, Chen & Mittal** [19] `[V]` — isolate-then-aggregate (answer from
  each isolated passage group, then securely aggregate), giving *"non-trivial lower bounds on response
  quality — even against an adaptive attacker with full knowledge of the defense and the ability to
  arbitrarily inject a bounded number of malicious passages."* **Boundary:** certificates hold for *certain
  queries*, 3 datasets × 3 LLMs, no numbers in the abstract. **This is the formal bridge to the dissent-incentives note:
  robustness comes from not letting one retrieved item set the answer.**
- **Divide and Doubt** [20] `[L]` — distributing the target answer across *stylistically diverse* passages
  beats clustering- and conflict-aware defences across 9 RAG configurations. **Boundary:** listing-level; but
  it is the counter-move to naive diversity defences and belongs in the simulation as a condition.

---

## 3. Indirect prompt injection — a *separate, stronger* mechanism

**Greshake, Abdelnabi, Mishra, Endres, Holz & Fritz 2023** [21] `[V]` — *"Not what you've signed up for."*
Adversaries inject prompts into **data likely to be retrieved**, with no direct interface to the model. Threat
classes: information-ecosystem contamination, data theft, worming, arbitrary code execution, functionality
manipulation, API-call control. Demonstrated against **Bing's GPT-4-powered Chat**, code-completion engines
and synthetic GPT-4 applications. **Boundary:** 2023 systems; a demonstration paper — taxonomy and
feasibility, not rates.

**Keep the categories unmerged (BRIEF QC-1 requires it):**

| | persuasion / preference manipulation | factual-false content | indirect prompt injection |
|---|---|---|---|
| page carries | favourable framing, true-or-plausible | a false claim stated as fact | an *instruction* to the agent |
| changes | the agent's ranking preference | the agent's belief | the agent's **control flow** |
| deniability | high — reads as marketing | medium | low once found |
| caught by | GEO-specific detectors, weakly [6] | fact-checking, corroboration | injection detectors, provenance separation |
| ceiling | shifts a distribution [1][3][4] | asserts an answer [12][13] | exfiltrate, call tools, persist [21][23] |

---

## 4. MCP / tool ecosystem — the cheaper surface

The text that decides which tool an agent calls is the **tool name and description**, written by the server
operator — no crawling, no indexing, no third-party publishing. "Which MCP server" is therefore a
**lower-cost, lower-latency** version of the same attack than "which website": the owner's two cases are not
equal-cost.

- **MPMA — Wang et al. 2025** [22] `[V]` — *"An attacker deploys a customized MCP server to manipulate LLMs,
  causing them to prioritize it over other competing MCP servers"*, for paid-service revenue or ad income.
  **DPMA** inserts manipulative words/phrases into the tool name and description (effective, not stealthy);
  **GAPMA** uses four ad-style description strategies plus a genetic algorithm for stealth. **Boundary:** the
  abstract carries **no** success rates, tool counts or model names (fetched; confirmed absent) — cite for
  mechanism and economic motive, not effect size. Closest published match to the owner's "which MCP" framing.
- **Invariant Labs, 1 Apr 2025 (Beurer-Kellner & Fischer)** [23] `[V]` — **tool poisoning**: *"malicious
  instructions are embedded within MCP tool descriptions that are invisible to users but visible to AI
  models"*, typically in `<IMPORTANT>` tags in the docstring. On **Cursor**, a poisoned `add` tool exfiltrated
  `.cursor/mcp.json` and `.ssh/id_rsa`, because *"tool arguments are hidden behind an overly simplified UI
  representation."* Also names **rug pulls** — *"A malicious server can change the tool description after the
  client has already approved it"* — and **tool shadowing**, where one malicious server rewrites agent
  behaviour toward a *trusted* server, enabling cross-server credential hijack absent from user-facing logs.
  **Boundary:** vendor blog, one client, demonstration not measurement, no rates — but it is the primary
  source everything later cites.
- **Registry trust, measured.** Li & Gao (DSN 2026) [24] `[V]`: **67,057** servers across **six** public
  registries; *"weak vetting and ownership checks allow adversarial or hijacked servers to enter hosts"*;
  MCPInspect flagged **833** vulnerable servers and **18** with suspicious descriptions. Hasan et al. [25]
  `[L]`: 1,899 servers, eight vulnerability classes, **5.5%** with tool poisoning. **Boundary:** [24]'s 18 is
  a *detector* count, not prevalence — read it as "the registry layer does not establish ownership".
- **Taxonomies / benchmarks.** MCP Safety Audit [26] `[V]`: malicious code execution, remote access control
  and credential theft through MCP tools; ships MCPSafetyScanner (no rates in the abstract). MCPSecBench [27]
  `[L]`: 17 attack types, *"all attack surfaces yield successful compromises"*, protections under 30%.
  Jamshidi et al. [28] `[L]` formalise **Tool Poisoning, Shadowing and Rug Pull** as descriptor-level attacks,
  with a layered defence cutting unsafe invocations to 15%.

**What a "decoy listing" realistically is, and what it buys.** A *functional* server that genuinely does the
advertised job (it must survive use), with a description optimised for selection [22]. Operator value: (a)
service revenue or ad income [22]; (b) a credential/file exfiltration channel at first invocation [23]; (c)
persistence past human approval via a rug pull [23]; (d) lateral reach into *trusted* servers via shadowing
[23]; (e) a durable read on the swarm's intentions, since every selection reveals the task. **(b)–(d) are
demonstrations on one client, not measured rates** — never present them as probabilities.

---

## 5. Real-world precedents of content flooding — measured vs asserted

- **NewsGuard, 6 Mar 2025 (Sadeghi & Blachez)** [29] `[V]` — the "Pravda" network / *LLM grooming*.
  **Measured by NewsGuard:** *"A NewsGuard audit has found that the leading AI chatbots repeated false
  narratives laundered by the Pravda network 33 percent of the time"*, across **10** leading generative AI
  tools. **Asserted, third-party:** **3.6 million** articles published in 2024 — attributed to another
  organisation whose report we could **not** load (americansunlight.org 404 on both paths tried), so treat as
  **unverified at source**. The page gates full methodology behind a form, so narrative count, prompt count,
  persona split and debunk/non-response rates are **not verified** here.
- **NewsGuard, 18 Jun 2024 (Sadeghi)** [30] `[V]` — the fully-specified sibling audit, usable as the
  methodology template. **Measured:** 10 named models (ChatGPT-4, You.com Smart Assistant, Grok, Pi, le Chat,
  Copilot, Meta AI, Claude, Gemini, Perplexity); **19** false narratives; **570** prompts (57/chatbot);
  **3** personas (neutral factual inquiry · leading · malign actor); **31.75%** of responses repeated the false
  claim (152 explicit, 29 with a disclaimer; 389 clean = 144 refusals + 245 debunks); **167** fake local news
  domains in the network. **Boundary:** a chatbot audit, not a swarm; it measures *co-occurrence* of flooded
  content with model output, **not** a controlled causal effect — there is no unflooded counterfactual web.
- **Ongoing monitoring** [31] `[V]` — AI False Claims Monitor; latest loaded entry a May 2026 quarterly audit
  over **11** chatbots, 30 prompts from 10 false claims, same personas. Its own rate was not in the loaded
  summary; "more than 28%" (Jan 2026) and "more than one third" (Aug 2025) show for earlier rounds.
  **Boundary:** small per-round prompt counts; rates move between rounds — no single number is *the* rate.

**Searched for and not found:** any controlled experiment that floods a real web corpus and measures an AI
system's selection shift against a counterfactual. Everything above is either a lab retrieval setup [1]–[20]
or an observational audit [29]–[31]. That gap is what the simulation is for, and is claimable as the contribution.

---

## 6. Operator economics and constraints

**Measured:**
- **No gradient access needed** — black-box rewriting *"matches or exceeds gradient-based attacks on rank
  promotion"* and *"the access model does not predict attack strength"* [5]; cost is LLM inference plus
  hosting, not model access.
- **Per-document generation cost is small and falling** — HotFlip-style poisoning reproduced at **4 hours →
  15 minutes per document** [32] `[L]`; a continuous-space variant, **under two minutes** [33] `[L]`.
  **Boundary:** both listing-level; both produce low-fluency, detectable passages.
- **Detection is weak but domain-dependent** — effectiveness/stealth trade off and black-box rewrites *"can
  evade both keyword- and perplexity-based detection on some domains"* [5]; safety guardrails cut this content
  by **≤5.7% relative**, one of three not statistically significant [6].
- **Pipeline attrition is the main hidden cost** — high retrieval-stage relevance *"substantially degrades
  after reranking"* [18].
- **Placement, not just publication** — AI search is biased toward **earned** third-party media over
  brand-owned content [7], so the operator pays for placements on sites it does not own; that is also what
  made Nestaas's cross-domain GitHub injection (8/8, 7/7) the notable result [1].
- **Volume is achievable by one actor** — 167 domains in one measured network [30]; 3.6M articles/yr claimed
  for another (**unverified at source**) [29].

**NOT measured anywhere located — these must be *swept parameters*, never cited constants:** dollar cost per
published page; crawl-to-index latency for a new domain; takedown/detection hazard rate per page; the fraction
of a *production* engine's retrieval set an operator can realistically hold.

**Share-of-corpus is the wrong denominator.** Across [12]–[16] the governing quantity is **how many
injector-controlled items land in the top-k actually retrieved for the decision query**:

| source | injected | corpus | effect |
|---|---|---|---|
| PoisonedRAG [12] | 5 per target question | millions of texts | 90% ASR |
| Zhong et al. [13] | 50 (→ up to 500) | millions of passages | >94% out-of-domain misleads |
| Phantom [14] | 1 document | not stated | trigger-gated; no rate given |
| AgentPoison [15] | <0.1% poison rate | agent memory store | >80% ASR, <1% benign loss |
| Long et al. [16] `[L]` | 0.048% | — | high ASR, trigger-gated |

**Existing vs fabricated target** — measured separately. *Existing-but-flawed:* **up to 83.2 pp** more likely
to enter the recommendation set [4]; rank promotion of a real low-ranked product [3]. *Fabricated:*
**34.0% → 59.4%**, parity with real products at **57.9%** [1] — but it has no earned media and no
corroboration, and AI search prefers earned media [7], so it needs third-party placements: **strictly more
stage-1/2 cost**. No located source measures that differential.

---

## Design implications for the proposal

### A. Threat-model parameters the simulation must expose
1. **Injector budget**, split into `N_pages` published *and* `N_placements` on sites the injector does not own
   (different costs — [1][7] force the split), plus repetitions per page: [3] needed **15×** in one page's HTML.
2. **Share of the retrieved set, not of the corpus** — expose `k` and `m` = injector-owned items in top-k;
   sweep `m/k` from `1/k` to `1`. Corpus fraction is derived and mostly irrelevant ([12][15] vs [17]).
3. **Position within the context** — every LLM in [3] preferred earlier positions *before* any injection, so
   rank/position is a first-class parameter, not an implementation detail.
4. **Content type as three non-merged arms** — persuasive-true/framing [1][2][4]; factual-false [12][13];
   instruction-injection [21][23]. Report each separately; a pooled rate is uninterpretable (BRIEF QC-1).
5. **Target type** — existing-good · existing-flawed [4] · fabricated [1]; for the MCP arm, a decoy-listing server
   that genuinely works [22][23].
6. **Swarm retrieval method** — single-stage dense top-k vs **chunk → retrieve → rerank → generate** [18]; and
   whether each agent retrieves *independently* or they share one retrieval result (the hinge into collective-dynamics.md / dissent-incentives.md).
7. **Aggregation / defence stack** — isolate-then-aggregate with a bounded-corruption certificate [19];
   perplexity + keyword filters [5]; safety guardrails [6]; style-diversity defences and their counter [20].
8. **Number of competing injectors** — 0, 1, 2, … all — with an "everyone attacks" equilibrium per [1] Fig. 5.
9. **Engine/model identity as a reported factor, never pooled** — [1] (Bing ≤25% vs Perplexity much higher),
   [3] (+2.89 to +6.02 across five models), [2] (domain variance), [8] (no stable cross-platform effect).
10. **The MCP arm's distinct cost model** — descriptor text is authored directly, no crawl, index or
    third-party placement [22][23]; a separate cheaper channel with its own approval-review and rug-pull dynamics.

### B. Where the literature corrects the owner's construction
1. **"Simply add context into the population of sites" is the unmeasured half.** [1 §6.3] scopes out getting
   into the context and pre-placed pages on its own domain. The simulation needs an explicit
   crawl/index/retrieval stage; assuming presence assumes away the attack's real cost.
2. **Ranking and position matter as much as presence.** Baseline position bias is measured [3], the live
   transfer needed 15 repetitions [3], rerankers eat much of the gain [18]. "In the corpus" ≠ "in top-k" ≠
   "early in context" ≠ "survives rerank".
3. **One knob is three mechanisms.** Persuasion, false facts and prompt injection differ in effect size,
   detectability and defence (§3 table). Keep the arms separate.
4. **Source diversity is not automatically a defence.** Spreading one target answer across *stylistically
   diverse* passages beats clustering- and conflict-aware defences [20]; what helps is **independent evidence**
   plus **isolate-then-aggregate** with a bounded-corruption guarantee [19] — the formal form of the dissent thesis.
5. **A single injector overstates the return.** With several, the equilibrium is "everyone attacks and
   everyone's recommendation rate falls below baseline" [1 Fig. 5] — a one-injector simulation overstates the
   operator's payoff and understates the collective quality loss, the quantity the value function should price.
6. **A fabricated option is reachable but not free.** It hit parity with real products [1], yet AI search
   prefers earned third-party media [7], so it needs placements the injector does not own. Steering toward an
   existing option is the cheaper attack; fabricated-option cost stays a swept unknown.
7. **"Which MCP" is cheaper than "which website".** Treating them as one scenario, as the ask does, hides a
   large cost asymmetry [22][23] and a different defence surface (approval review, rug pulls, registry
   ownership checks [24][25]).
8. **Do not borrow the pretraining constant.** The 250-document result [17] is pretraining, narrow and
   explicitly uncertain beyond 13B; it supports "absolute count, not fraction" as a *shape*, nothing more.
9. **Guardrails are not the control.** Off-the-shelf safety guardrails cut this attack by ≤5.7% relative [6];
   the leverage is in retrieval, aggregation and incentive design — where collective-dynamics.md / dissent-incentives.md pick up.
10. **No public work measures a causal flood → selection-shift effect on a real corpus** (§5). That gap is both
    the proposal's contribution and the reason the deliverable should be a *simulation*, not a claim about the
    live web.

---

## Not found / could not verify
- Full Pravda-audit methodology (narrative/prompt counts, persona split, debunk rate): form-gated [29]; the
  June 2024 sibling audit [30] stands in as the methodology template.
- The originating **3.6 million articles** report (American Sunlight Project): both URLs tried 404'd —
  **unverified at source**.
- Dollar cost per published page, and crawl-to-index latency for a new domain in any AI search pipeline: not
  located in any academic or vendor source this session.
- Effect sizes for MPMA [22], Phantom [14], MCP Safety Audit [26], RobustRAG [19], Nie et al. [18] are absent
  from their abstracts; full-text extraction of those five is the follow-on if the proposal needs them.
- `[L]` sources ([8][9][10][11][16][20][25][27][28][32][33]) are arXiv-API listing reads only — verify before
  promoting any to a headline claim.

---

## References

1. Fredrik Nestaas, Edoardo Debenedetti, Florian Tramèr. **Adversarial Search Engine Optimization for Large Language Models.** 2024. https://arxiv.org/abs/2406.18382 · full text https://arxiv.org/html/2406.18382v2
2. Pranjal Aggarwal, Vishvak Murahari, Tanmay Rajpurohit, Ashwin Kalyan, Karthik Narasimhan, Ameet Deshpande. **GEO: Generative Engine Optimization.** KDD 2024. https://arxiv.org/abs/2311.09735
3. Samuel Pfrommer, Yatong Bai, Tanmay Gautam, Somayeh Sojoudi. **Ranking Manipulation for Conversational Search Engines.** EMNLP 2024 (Main). https://arxiv.org/abs/2406.03589 · full text https://arxiv.org/html/2406.03589v3
4. Qianfeng Wen, Yifan Simon Liu, Xin Liu, Difan Jiao, Blair Yang, Junda Wu, Zhenwei Tang. **SafeGEO: Understanding Generative Engine Optimization Risks in Recommendation Agents.** 2026. https://arxiv.org/abs/2606.28356
5. Ojas Nimase, Zhe Chen, Gengpei Qi, Yue Zhao, Xiyang Hu. **GEO-Bench: Benchmarking Ranking Manipulation in Generative Engine Optimization.** 2026. https://arxiv.org/abs/2605.29107
6. Bing Zheng, Zongyao Zhao, Wenming Yang. **Counter-GEO-Bench: Evaluating Defenses Against Information-Distorting Generative Engine Optimization.** 2026. https://arxiv.org/abs/2609.02316
7. Mahe Chen, Xiaoxuan Wang, Kaiwen Chen, Nick Koudas. **Generative Engine Optimization: How to Dominate AI Search.** 2025. https://arxiv.org/abs/2509.08919
8. Olivier Martinez. **Optimizing Visibility in Generative Engines: A Critical Survey.** 2026. https://arxiv.org/abs/2607.14035
9. Puneet S. Bagga, Vivek F. Farias, Tamar Korkotashvili, Tianyi Peng, Yuhang Wu. **E-GEO: A Testbed for E-Commerce Generative Engine Optimization.** 2025. https://arxiv.org/abs/2511.20867
10. Pratyush Kumar. **Generative Engine Optimization at Scale: Brand Visibility.** 2026. https://arxiv.org/abs/2606.20065
11. Yizhu Wen, Nan Zhang, Haohan Yuan, Xun Chen, Haopeng Zhang, Hanqing Guo. **Position: Generative Engine Optimization Creates Risks.** 2026. https://arxiv.org/abs/2606.12439
12. Wei Zou, Runpeng Geng, Binghui Wang, Jinyuan Jia. **PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models.** USENIX Security 2025. https://arxiv.org/abs/2402.07867
13. Zexuan Zhong, Ziqing Huang, Alexander Wettig, Danqi Chen. **Poisoning Retrieval Corpora by Injecting Adversarial Passages.** 2023. https://arxiv.org/abs/2310.19156
14. Harsh Chaudhari, Giorgio Severi, John Abascal, Anshuman Suri, Matthew Jagielski, Christopher A. Choquette-Choo, Milad Nasr, Cristina Nita-Rotaru, Alina Oprea. **Phantom: General Backdoor Attacks on Retrieval Augmented Language Generation.** 2024. https://arxiv.org/abs/2405.20485
15. Zhaorun Chen, Zhen Xiang, Chaowei Xiao, Dawn Song, Bo Li. **AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases.** 2024. https://arxiv.org/abs/2407.12784
16. Quanyu Long, Yue Deng, LeiLei Gan, Wenya Wang, Sinno Jialin Pan. **Backdoor Attacks on Dense Retrieval via Public and Unintentional Triggers.** 2024. https://arxiv.org/abs/2402.13532
17. Anthropic (Alignment Science), UK AI Security Institute, Alan Turing Institute. **A small number of samples can poison LLMs of any size.** 9 Oct 2025. https://www.anthropic.com/research/small-samples-poison
18. Xi Nie, Hongwei Li, Shenghao Wu, Mingxuan Li, Jiachen Li, Wenbo Jiang. **When Poison Fails After Retrieval: Revisiting Corpus Poisoning under Chunking and Reranking Pipelines.** 2026. https://arxiv.org/abs/2606.11265
19. Chong Xiang, Tong Wu, Zexuan Zhong, David Wagner, Danqi Chen, Prateek Mittal. **Certifiably Robust RAG against Retrieval Corruption.** 2024. https://arxiv.org/abs/2405.15556
20. Tianhao Chen, Yuhan Wei, Weifei Jin, Zhengyuan Jiang, Yuepeng Hu, Neil Zhenqiang Gong. **Divide and Doubt: Diverse Distributed Poisoning for Retrieval-Augmented Generation.** 2026. https://arxiv.org/abs/2609.27090
21. Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, Mario Fritz. **Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.** 2023. https://arxiv.org/abs/2302.12173
22. Zihan Wang, Rui Zhang, Yu Liu, Wenshu Fan, Wenbo Jiang, Qingchuan Zhao, Hongwei Li, Guowen Xu. **MPMA: Preference Manipulation Attack Against Model Context Protocol.** 2025. https://arxiv.org/abs/2505.11154
23. Luca Beurer-Kellner, Marc Fischer (Invariant Labs AG). **MCP Security Notification: Tool Poisoning Attacks.** 1 Apr 2025. https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
24. Xiaofan Li, Xing Gao. **A First Look at the Security Issues in the Model Context Protocol Ecosystem.** DSN 2026. https://arxiv.org/abs/2510.16558
25. Mohammed Mehedi Hasan, Hao Li, Emad Fallahzadeh, Gopi Krishnan Rajbahadur, Bram Adams, Ahmed E. Hassan. **MCP at First Glance: Security and Maintainability of MCP Servers.** 2025. https://arxiv.org/abs/2506.13538
26. Brandon Radosevich, John Halloran. **MCP Safety Audit: LLMs with the Model Context Protocol Allow Major Security Exploits.** 2025. https://arxiv.org/abs/2504.03767
27. Yixuan Yang, Cuifeng Gao, Daoyuan Wu, Yufan Chen, Yingjiu Li, Shuai Wang. **MCPSecBench: A Systematic Security Benchmark and Playground for Model Context Protocols.** 2025. https://arxiv.org/abs/2508.13220
28. Saeid Jamshidi, Arghavan Moradi Dakhel, Kawser Wazed Nafi, Foutse Khomh. **Semantic Attacks on Tool-Augmented LLMs: Descriptor-Level Manipulation.** 2025. https://arxiv.org/abs/2512.06556
29. McKenzie Sadeghi, Isis Blachez (NewsGuard). **A Well-funded Moscow-based Global 'News' Network has Infected Western Artificial Intelligence Tools Worldwide with Russian Propaganda.** 6 Mar 2025. https://www.newsguardtech.com/special-reports/moscow-based-global-news-network-infected-western-artificial-intelligence-russian-propaganda
30. McKenzie Sadeghi (NewsGuard). **Top 10 Generative AI Models Mimic Russian Disinformation Claims A Third of the Time, Citing Moscow-Created Fake Local News Sites as Authoritative Sources.** 18 Jun 2024. https://www.newsguardtech.com/special-reports/generative-ai-models-mimic-russian-disinformation-cite-fake-news
31. NewsGuard. **AI False Claims Monitor.** Ongoing; latest loaded entry May 2026. https://www.newsguardtech.com/ai-false-claims-monitor/
32. Yongkang Li, Panagiotis Eustratiadis, Evangelos Kanoulas. **Reproducing HotFlip for Corpus Poisoning Attacks in Dense Retrieval.** 2025. https://arxiv.org/abs/2501.04802
33. Yongkang Li, Panagiotis Eustratiadis, Simon Lupart, Evangelos Kanoulas. **Unsupervised Corpus Poisoning Attacks in Continuous Space for Dense Retrieval.** 2025. https://arxiv.org/abs/2504.17884
