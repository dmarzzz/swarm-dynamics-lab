---
id: sateur-2025-evaluating
type: paper
title: Evaluating Turnstile as a Privacy-Conscious Alternative to reCAPTCHA
authors:
- Maxime Sateur
- Javier Martínez Llamas
- Davy Preuveneers
- Wouter Joosen
year: 2025
venue: Availability, Reliability and Security
url: https://exa.ai/library/publication/ff3dcfq8z11
doi: 10.1007/978-3-032-00633-2_14
arxiv: null
cite: Maxime Sateur; Javier Martínez Llamas; Davy Preuveneers; Wouter Joosen. (2025).
  Evaluating Turnstile as a Privacy-Conscious Alternative to reCAPTCHA. Availability,
  Reliability and Security, 235-252. https://doi.org/10.1007/978-3-032-00633-2_14
topics:
- swarm-detection
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

This comparison deploys reCAPTCHA and Turnstile on test websites and examines network traffic, scripts, and privacy rules. The retrieved abstract finds broadly similar token-validation mechanisms, fewer tracking-cookie concerns for Turnstile, and a token-exploitation vulnerability reproduced from reCAPTCHA into Turnstile.

## Contribution

Deploys reCAPTCHA and Turnstile on test sites and compares network behavior, scripts and privacy rules, reproducing a token-exploitation flaw in Turnstile.

## Key results

- A previously identified reCAPTCHA token-exploitation vulnerability is replicated in Turnstile; no exploit rate is supplied in the abstract.

## Methods and models

Network and script inspection, client-code deobfuscation, and regulatory analysis.

## Limitations and open questions

Regulatory conclusions are the authors analysis, not legal advice or a current compliance certification; benchmark robustness against contemporary LLM agents is not established.

## Relevance to us

Background on CAPTCHA infrastructure that agent swarms must pass; see [[teoh-2025-captchas]] and [[zhang-2026-captchaarena]] for solver capability.

## Access provenance

Crossref metadata and the abstract at the recorded URL were opened directly or through Exa content extraction on 2026-10-03. Any non-null citation count is OpenAlex cited_by_count on that date. Abstract depth is deliberate even where an open PDF was found.


## Notes from shadow/sol-w5

Added in parallel from pipeline batch #77; this id was taken first by shadow/sol-g51, so my entry is folded in here. My reading depth: skim (source opened: https://lirias.kuleuven.be/retrieve/0a511928-a651-4d57-82a8-8463d5467870).

### Summary

Compares Cloudflare Turnstile with Google reCAPTCHA by deploying both on test sites and analysing network traffic, HTTP requests and client-side script behaviour, de-obfuscating part of Turnstile's VM-obfuscated client code, and checking claims of GDPR and ePrivacy compliance. Both work the same way at the protocol level: a client-side challenge issues a token that the site back end validates. Turnstile avoids tracking cookies and is judged closer to GDPR compliance; reCAPTCHA in its current form struggles to comply. Security side: they port two known reCAPTCHA attacks (Sivakorn et al.). Cookie replay: Turnstile itself uses no cookies, but Cloudflare's cf_clearance and Turnstile's optional pre-clearance cookie can be harvested and reused (tools like FlareSolverr do this) if user agent and IP stay the same. Token harvesting via sitekey reuse (they call it clickjacking): by serving the target's public sitekey from a local page with a spoofed hostname, they mint valid tokens for the target site, one every 3 s, or 1.5 s per token with 20 widgets on one page; a day-long run hit no hard rate limit. They propose making the sitekey private (back end issues a per-load token instead). Read: abstract, sections 4 and 6, conclusion; skimmed traffic analysis and regulation sections.

### Contribution

Independent measurement that a "privacy-first" CAPTCHA inherits the token-transferability weakness of reCAPTCHA, with a concrete throughput figure for token harvesting and a simple mitigation.

### Key results

- Valid Turnstile tokens for a target site can be generated off-site via sitekey reuse: about 1.5 s/token with 20 parallel widgets; no hard daily limit observed.
- Going from 3 to 6 tokens per session raised total output 51%, 6 to 9 only another 19% (diminishing returns).
- One widget in 20 consistently failed and needed manual solving, suggesting deliberate false negatives.
- Turnstile's data collection appears similar to reCAPTCHA's in kind (e.g. user agent), but VM obfuscation limited what they could see.

### Methods and models

Test deployments, traffic capture and request analysis, partial de-obfuscation of client code, replication of Sivakorn et al. attacks, a day-long token-generation run.

### Limitations and open questions

Authors note: obfuscation limited the analysis; Cloudflare's privacy claims could not be verified; findings are time-sensitive. They judge 1.5 s/token too slow for large-scale abuse, which is debatable for agent operators running many browsers in parallel.

### Relevance to us

Frictionless CAPTCHAs are one of the main gates agent swarms hit on the web. This paper shows the gate's output (a token) is transferable, so a swarm can farm tokens centrally rather than solve per agent, which matters both for detection (look for token reuse patterns) and for threat models. Related: CAPTCHA breaking [[plesner-2024-breaking]], [[sivakorn-2026-robot]], agent CAPTCHA training data [[zhang-2026-captchaarena]], PoW alternative [[gh-techarohq-anubis]], crawler traffic [[cloudflare-2025-from]].
