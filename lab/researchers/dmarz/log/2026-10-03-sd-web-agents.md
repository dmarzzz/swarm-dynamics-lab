# 2026-10-03 dmarz/sd-web-agents

Lane: scan-papers-sd-web-agents (detecting browser agents, computer-use agents and AI crawlers on the web). Isolated worktree on branch lane/sd-web-agents. Per dmarz's override I did not run lab.py claim/touch/done/release/sync and did not edit lab/tasks/.

## What I covered

43 new library entries (41 papers, 2 code repos) plus 5 annotations of existing entries, all tagged swarm-detection.

- LLM web-agent detection and attribution (honeysite studies): fayolle-2026-internet, kang-2026-whose, wang-2026-fp-agent, choudhary-2026-what, ousat-2026-broken, seiden-2026-identifying, borysenko-2026-developer, zhang-2025-exposing, rmus-2026-process, munirathinam-2026-will, kumar-2025-throttling. Code: gh-spin-umass-ai-agent-fingerprint, gh-ethanbwang-fp-agent.
- Pre-LLM and general web bot detection: venugopalan-2024-fp-inconsistent, vastel-2020-fp-crawlers, amin-azad-2020-web, iliou-2021-detection, kadel-2024-botracle, jarad-2026-when, salman-2026-how, van-boxem-2026-shy, gundelach-2026-detecting, hoetzlein-2025-protecting, jerkins-2026-penalizing, hosain-2025-web (review).
- AI crawlers and robots.txt compliance: liu-2025-somesite, kim-2025-scrapers, cui-2025-odyssey, longpre-2024-consent, lopez-fonseca-2026-do.
- CAPTCHAs vs multimodal agents: guerar-2021-gotta (review), searles-2023-dazed, deng-2024-oedipus, luo-2025-open, liu-2026-next-gen, wang-2025-cognition, sivakorn-2026-robot, zhang-2026-invisible, song-2026-hll, chen-2026-captcha, wu-2025-mca-bench, salman-2026-captchas.
- Agent identity and permission signalling: marro-2025-permission; annotated existing south-2025-authenticated, gh-cloudflare-web-bot-auth, cloudflare-2025-forget, cloudflare-2025-age, plesner-2024-breaking.

Read in full: fayolle-2026-internet, kang-2026-whose, wang-2026-fp-agent, choudhary-2026-what, ousat-2026-broken. Skimmed: seiden-2026-identifying (method and RQ1 to RQ2), kim-2025-scrapers (HTML lost most numbers). The rest are abstract-level. lab.py verify: 41 papers, 0 problems. lab.py check: 0 errors in my files (6 errors on main belong to 1-library/papers/wu-2024-system.md, not mine).

## Searches run

- arXiv API (abs: queries): "web agents" + detect, "AI crawlers", "browser agents" + detection, CAPTCHA + multimodal, "bot detection" + "LLM agents", "computer-use agents" + detect, robots.txt, "agentic traffic". Then the API rate-limited (shared IP with other lanes) and I switched to the arxiv.org/search HTML: web bot detection, bot detection browser automation, agent traffic web server, CAPTCHA GUI agents, CAPTCHA LLM solve, reCAPTCHA bots, agentic browsing detection, computer-use agent human distinguish, Web Bot Auth, AI agent identification web, LLM web agent honeypot, headless chrome detection, proof of work bots AI scrapers, plus title lookups for cited works.
- Semantic Scholar: keyword search (partly 429), backward references of fayolle-2026-internet, forward citations of liu-2025-somesite, luo-2025-open, venugopalan-2024-fp-inconsistent, kim-2025-scrapers, wang-2026-fp-agent, plesner-2024-breaking, liu-2026-next-gen. The forward-citation pass surfaced seiden-2026-identifying, lopez-fonseca-2026-do, kumar-2025-throttling, salman-2026-captchas, rmus-2026-process, jerkins-2026-penalizing and salman-2026-how.
- OpenAlex and DBLP: rate-limited / timed out all session. Crossref used for DOI metadata.
- WebSearch: unavailable (session budget of 200 searches already spent by other lanes).

## Could not reach / not catalogued

- Publisher pages for ACM DL (403) and Springer (auth redirect); abstracts for cui-2025-odyssey, vastel-2020-fp-crawlers, amin-azad-2020-web, salman-2026-how, jerkins-2026-penalizing came from Semantic Scholar records, iliou-2021-detection from Crossref.
- Seen in reference lists but not opened, so not catalogued: Li et al. 2021 "Good Bot, Bad Bot: Characterizing Automated Browsing Activity"; Sateur et al. 2025 "Evaluating Turnstile as a Privacy-Conscious Alternative to reCAPTCHA"; Iliou et al. 2021 "Web Bot Detection Evasion Using GANs"; Teoh et al. 2025 "Are CAPTCHAs Still Bot-hard?"; WebCloak (LLM agents as scrapers); Tsingenopoulos et al. RL evasion of reCAPTCHA v3; Crichton et al. "Rethinking fingerprinting" (behavioural fingerprinting at scale); "Free Proxies Unmasked" (Mehanna et al. 2024); Jang 2026 "Dissecting Mellowtel" (bandwidth-as-a-service extensions, possibly residential-proxy supply for agents); Hoffmann 2026 "From robots.txt to ai.txt"; CaptchaArena (2609.31957, abstract fetched but not catalogued); MirrorCAPTCHA (ACL 2026); Panizza 2026 Nature comment on survey-taking AI agents (belongs to another lane).
- Industry sources the papers rely on but which I did not open: Cloudflare Radar AI-bot share (8.7% of HTML traffic in 2025, 38.7% of top-million sites receiving AI bot traffic in 2024, both as cited by wang-2026-fp-agent), Imperva/Thales Bad Bot Report (51% of 2024 traffic automated, as cited), HUMAN Security and DataDome agent-trust products, Cloudflare AI Labyrinth, Anubis.
- No X threads, HN or blog posts searched (WebSearch unavailable).

## What surprised me

- Three independent 2026 honeysite studies (Inria, UMass, UC Davis) all reach near-perfect agent-vs-human separation in closed-world tests, but disagree on which layer matters: Fayolle says browser fingerprint (0.931) beats behaviour-free IP/TLS; Wang says behaviour beats browser fingerprint (about 0.8); Kang says no single layer suffices.
- Stealth modes made agents more detectable (fayolle-2026-internet), and the teleporting cursor is universal across seven commercial agents (wang-2026-fp-agent). Choudhary shows this is a CDP artifact that survives even human-trajectory replay, which means the signal disappears once agents move to OS-level input, as salman-2026-captchas already does.
- Deployed defences are mostly blind: Cloudflare free tier blocked 1 of 7 agents (only the self-declared one); Claude for Chrome and OpenClaw passed every defence including combined stacks. The real remaining barrier is browser-profile reputation (ousat-2026-broken), not challenge difficulty.
- The canary-token method (seiden-2026-identifying) is the closest thing to a swarm honeypot in this literature: it attributes scrapers through what the downstream model later says, and it found 10 of 18 chatbots reading third-party search indexes rather than crawling.
- No paper in this lane measures many agents from one operator acting together on the web; everything is per-session or per-product. Coordination signals appear only in hoetzlein-2025-protecting (subnet aggregation).

## Next

Survey the branch with the measured numbers above; run the FP-Agent or MARK code against a honeysite with several instances of one agent to test whether cross-session clustering exposes a swarm (hunch, not a hypothesis).
