# 2026-10-03 dmarz/sd-attribution

Lane: scan-papers-sd-attribution (identifying the model or agent behind observed behaviour). Isolated worktree on branch
lane/sd-attribution. Per dmarz's override, no lab.py claim/touch/done/sync and no edits under lab/tasks/; task state is
handled at merge.

## What I covered

53 new paper entries tagged swarm-detection, plus a "Notes from dmarz/sd-attribution" section and the
swarm-detection topic on the existing yang-2023-anatomy (fox8 botnet). `lab.py verify --agent dmarz/sd-attribution`:
53 checked, 0 problems. `lab.py check`: 0 errors in my files (the 6 errors are in 1-library/papers/wu-2024-system.md,
added on main by another lane).

Read in full (main text): pasquini-2024-llmmap, white-2026-black, lugoloobi-2026-known, reworr-2024-llm,
wang-2026-who. Main text of park-2026-cross also read, but logged as skim because the HTML lost the table numbers
and I did not read the appendices. Everything else is abstract-level.

Clusters:

- Black-box model fingerprinting of deployed LLMs: pasquini-2024-llmmap, gubri-2024-trap, iourovitski-2024-hide,
  li-2026-adaptprint, bruckner-2026-one, das-2026-identifying, kurian-2025-attacks, hu-2025-fingerprinting,
  yang-2025-challenge, finlayson-2024-logits, ellis-2026-black, wimbauer-2026-fingerprinting.
- API identity auditing (is it the model it claims to be): gao-2024-model, zhu-2025-auditing, cai-2025-are,
  zhang-2026-which, leshin-2026-behavioral, zhang-2026-real, chen-2026-token, wang-2026-agentprov.
- Lineage and provenance: nikolic-2025-model, yax-2024-phylolm.
- Passive text attribution: sun-2025-idiosyncrasies, kumarage-2023-neural, fu-2025-fdllm, bisztray-2025-i (code),
  kikteva-2026-show.
- Agent-level attribution from behaviour: wang-2026-who (coding trajectories), ediga-2026-trace (terminal
  commands), lugoloobi-2026-known (UI traces), kang-2026-whose, fayolle-2026-internet, wang-2026-fp,
  choudhary-2026-what (web agents).
- Same-operator linking: white-2026-black (system-prompt fingerprinting of scam bots), park-2026-cross
  (cross-agent campaign attribution), chen-2026-do (system-prompt clones), chocron-2026-who (vendor-assisted
  canary attribution).
- Probes and reverse Turing tests: wang-2023-bot (FLAIR), gressel-2024-are, rmus-2026-process,
  candussio-2026-rogueai, reworr-2024-llm (prompt-injection plus timing honeypot).
- Timing and network side channels: carlini-2024-remote, mcdonald-2025-whisper, zhang-2025-exposing,
  pouryousef-2026-large.
- Evasion and negative results: nasery-2025-are, yuan-2026-forging, chen-2026-token, cai-2025-are,
  kurian-2025-attacks.
- Review articles found: huang-2024-authorship, kumarage-2024-survey, shao-2025-sok, liu-2026-implicit.

## Searches run

- Semantic Scholar search API: "LLM fingerprinting black-box identification", "TRAP targeted random adversarial
  prompt honeypot", "model equality testing API", "fingerprinting LLM agents behavior", "timing side channel
  language model inference". Several other queries (attribution, reverse Turing, idiosyncrasies, LLMmap,
  authorship survey, agent honeypot) failed with HTTP 429.
- arXiv export API: all queries returned HTTP 429 (other lanes hitting it in parallel). Switched to the arXiv
  HTML search page: "LLM fingerprinting", "model attribution LLM-generated text", "identify underlying LLM agent",
  "same system prompt chatbot linking", "LLM social bots attribution", "reverse Turing test LLM", "behavioral
  fingerprint LLM", "LLM stylometry", "source LLM identification", "prompt injection detect AI agent", "CAPTCHA
  LLM agents", "sockpuppet LLM", "identify AI agent in conversation", "linking LLM agents same operator", "agent
  attribution campaign", "detecting LLM agents timing response latency".
- OpenAlex: every query returned HTTP 429.
- WebSearch: about 12 queries before the shared session budget (200) ran out: LIDAR, web-agent fingerprinting,
  LLMmap, idiosyncrasies, UI traces, FLAIR, reverse CAPTCHA, MET, remote timing, logits leak, PlugAE,
  authorship survey, LLM agent honeypot, account-linking stylometry, PhyloLM.
- Citation chasing (Semantic Scholar): forward from LLMmap (72 citing papers) and FLAIR (40), backward from
  white-2026-black (74 references). The forward chase from LLMmap gave about a third of the final set
  (ediga-2026-trace, chocron-2026-who, gressel-2024-are, shao-2025-sok, liu-2026-implicit, fu-2025-fdllm,
  kurian-2025-attacks, hu-2025-fingerprinting).
- Metadata for every entry comes from the arXiv abstract page I opened. Full texts came from arxiv.org/html.

## What I could not reach

- arXiv API and OpenAlex were rate-limited for the whole session, so I ran no systematic OpenAlex sweep and no
  DBLP query. Saturation is not established: the LLMmap forward chase was still turning up relevant work.
- Seen in citation lists but not opened, so not catalogued: Bhardwaj 2025 "Invisible Traces" (2501.18712, abstract
  opened but too vague to catalogue), Weinberg 2026 ARCANE (2604.24644, synthetic cyber attribution, opened, judged
  off-topic), "Love, Lies, and Language Models" romance-baiting scams (2512.16280), "Network-Level Prompt and Trait
  Leakage in Local Research Agents" (2508.20282), "Inference-Engine Fingerprinting Attacks are Practical"
  (2609.20614), "System Attribution in LLM Brand Recommendations" (2610.00253), "Dissecting a social bot powered
  by generative AI" (no arXiv id), "XDAC: detection and attribution of LLM-generated news comments in Korean",
  SeedPrints (2509.26404), MultiGhostBench (2609.02379), Witeness Overlap (2609.31784), Stemma (2607.25880),
  ProcGrep (cited in wang-2026-who, no id found), GhostPrint (cited in wang-2026-who), Panickssery 2024 on
  self-recognition, Weiss 2024 token-length side channel. These are the next things to open.
- No X threads, blogs or code in this lane. The code links (LLMmap, FLAIR, MET, Known By Their Actions harness)
  are named in entries but not catalogued as code entries.

## What surprised me

- How much of this literature is from 2026: 27 of 53 entries (by arXiv year). Agent-level attribution (coding trajectories, UI
  traces, terminal commands, tool-call distributions, campaign linking) appeared in the last six months.
- The measured in-the-wild base rate of autonomous LLM agents is tiny: reworr-2024-llm logged 8 potential agents
  in 8.1M SSH attempts. By contrast, the strongest attribution numbers (97.7% model ID from encrypted traffic in
  pouryousef-2026-large, 96% F1 from UI traces in lugoloobi-2026-known, 98% base-model attribution from a few turns
  in white-2026-black) all come from lab settings.
- Linking two agents to one operator is much harder than naming the model: 0.768 AUC from one conversation in
  white-2026-black, 0.82 pairwise AUC in park-2026-cross. A one-sentence tone prefix collapses system-prompt clone
  detection (chen-2026-do: 0.978 to 0.547).
- Evasion of text attribution is well developed: targeted rewriting forges another model's fingerprint 70.2% of
  the time (yuan-2026-forging), and ten ownership-fingerprint schemes fall to adaptive hosts (nasery-2025-are).
  Behavioural and structural signals (wang-2026-who, park-2026-cross) held up better in the tests reported.
- Stealth tooling increases detectability of web agents (fayolle-2026-internet), and Cloudflare caught 1 of 7 AI
  browsing agents (wang-2026-fp). Current agent detection keys on missing raw input events, an automation
  artefact (choudhary-2026-what), so it will expire when agents drive real input devices. This is my inference
  from the authors' statement, not something they measured.

## Next

Open the unreached items above, run an OpenAlex sweep once rate limits clear, chase citations forward from
white-2026-black and reworr-2024-llm, and catalogue code for LLMmap, FLAIR, MET and the UI-trace harness.
