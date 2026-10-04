# 2026-10-03 dmarz/sd-honeypots

Lane: honeypots, honeytokens, canaries, tarpits and deception aimed at AI agents and crawlers (task
scan-papers-sd-honeypots). Worked on branch lane/sd-honeypots per dmarz's override: no claim/touch/done, no
edits under tasks/.

## What I covered

37 new entries (36 papers, 1 blog), all tagged swarm-detection. No existing entries matched, so none were
annotated. Five read in full: reworr-2024-llm, seiden-2026-identifying, fayolle-2026-internet,
pasquini-2024-hacking, lee-2011-seven. Skimmed: bridges-2025-sok, ayzenshteyn-2025-cloak,
cordeiro-2026-rouxii, rao-2025-detecting, lee-2010-uncovering, cloudflare-2025-trapping. The rest are
abstract-level.

Branches covered:
- Honeypots that detect LLM agents in the wild: reworr-2024-llm (plus live dashboard), elzer-2026-ollamadrama.
- Deception and traps against LLM agents: pasquini-2024-hacking, ayzenshteyn-2025-cloak,
  wang-2026-agentsnare, mittelsteadt-2026-detecting (policy).
- Evasion and negative results: cordeiro-2026-rouxii, xie-2026-llm-based, gans-2026-when,
  gans-2026-calibrated, wang-2026-towards, cornelissen-2018-deploying.
- Canary tokens and inject-and-detect: seiden-2026-identifying, rao-2025-detecting, gharami-2025-chatgpt,
  lin-2025-hidden, collu-2025-misleading, zhang-2026-measuring, xu-2026-penny, farooqi-2020-canarytrap.
- Honeysites and web-agent fingerprinting: fayolle-2026-internet, wang-2026-fp-agent,
  zychlinski-2025-whole, kim-2025-scrapers, liu-2024-somesite, hoetzlein-2025-protecting,
  cloudflare-2025-trapping.
- Social honeypots (classic): lee-2010-uncovering, lee-2011-seven, cornelissen-2018-deploying.
- LLM-as-honeypot and reviews: bridges-2025-sok (review), zhang-2021-three (review), sladic-2023-llm,
  otal-2024-llm, mckee-2023-chatbots, traister-2026-corpus, kahlhofer-2024-honeyquest.
- On-chain: torres-2019-art.

## Searches run

- arXiv API: honeypot AND LLM; honeypot AND agents; prompt injection AND honeypot; LLM agents AND deception
  AND defense; prompt injection AND LLM-driven AND defense; ti:canary AND agent; hidden prompt AND detect;
  AI crawlers; tarpit; web agents AND detect AND bot; social honeypot; honeypot AND smart contract;
  honeytoken(s); survey AND LLM AND respondents AND detect; peer review AND LLM-generated AND watermark;
  CAPTCHA AND LLM agents; title lookups for Kim 2025 and Cui 2025.
- Crossref: classic social-honeypot titles (Webb 2008, Lee 2010, Lee 2011, Stringhini 2010), Bowen 2009
  decoy documents, honeywords; DOI checks for every venue/page claim.
- Backward citation chasing from fayolle-2026-internet, seiden-2026-identifying, bridges-2025-sok and
  cordeiro-2026-rouxii (found ayzenshteyn-2025-cloak, wang-2026-fp-agent, zychlinski-2025-whole,
  kim-2025-scrapers, the AI Labyrinth post).
- WebFetch: Cloudflare AI Labyrinth post; Palisade honeypot dashboard; USENIX page and PDF for Cloak, Honey,
  Trap; AAAI page and PDF for Lee 2011; author PDF for Lee 2010.

## What I could not reach

- Semantic Scholar and OpenAlex returned 429 for the whole session (OpenAlex daily budget exhausted on the
  shared IP), so there was no forward citation chasing and `citations:` is null on every entry. The
  WebSearch budget was already used up by other lanes when I tried it. DBLP served a bot-check page.
- Not catalogued because not opened: Stringhini, Kruegel and Vigna 2010 "Detecting spammers on social
  networks" (ACSAC, DOI 10.1145/1920261.1920263; author PDF URLs 404); Webb, Caverlee and Pu 2008 "Social
  honeypots: making friends with a spammer near you" (CEAS); Bowen et al. 2009 "Baiting inside attackers
  using decoy documents" (DOI 10.1007/978-3-642-05284-2_4); Juels and Rivest 2013 "Honeywords" (DOI
  10.1145/2508859.2516671); Meeus et al. 2024 "Copyright traps for LLMs"; Cui et al. 2025 "The odyssey of
  robots.txt governance" (CCS); Brach et al. 2025 "Ghosts in the markup"; Westwood 2025 on AI agents passing
  survey attention checks; Guan et al. on in-the-wild LLM honeypot sessions (quoted in bridges-2025-sok).
- Recent arXiv items seen in listings but not catalogued for time: AdvancedShelLM (2606.27990), Honeyval
  (2605.29963), HoneyRoute (2609.08306), Speculative Safety Honeypot (2609.39549), AgentShield (2605.11026),
  Kill-Chain Canaries (2603.28013), Caught in the Act(ivation) (2606.04141), PHANTOM honeytokens
  (2605.02992), LLM honeytoken generation (2404.16118).

## What surprised me

- The only published base rate of wild autonomous attacking agents is tiny: 8 potential agents in 8.1M SSH
  attempts (reworr-2024-llm). The live dashboard now shows 14 potential and 3 confirmed in 24.1M.
- Deception is fragile against an agent told what to look for: in Rouxii, honeypot identification went from
  19% to 97% when only the prompt changed (cordeiro-2026-rouxii). Gans proves that shared memory across a
  coalition of agents defeats honeytokens in the limit (gans-2026-when). Together these suggest trap
  detection gets worse as swarms get bigger and share more (my inference, untested).
- Stealth modes make web agents easier to fingerprint (fayolle-2026-internet), and Cloudflare caught 1 of 7
  browsing agents where behavioural fingerprints caught all 7 (wang-2026-fp-agent).
- The cleanest statistical template is from peer review, not security: a random per-exposure canary plus a
  family-wise error test, with 98.6% embedding and zero false positives on over 10K human reviews
  (rao-2025-detecting).

## Next

Forward-chase reworr-2024-llm, pasquini-2024-hacking and ayzenshteyn-2025-cloak once Semantic Scholar
recovers. Catalogue the classic social-honeypot papers listed above. A hackathon hunch (not a hypothesis):
deploy per-visitor canaries on a honeysite plus asymmetric-character honeytokens, and measure how
detection rate scales with the number of agents that share memory.
