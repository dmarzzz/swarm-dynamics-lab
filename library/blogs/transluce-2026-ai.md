---
id: transluce-2026-ai
type: blog
title: "AI Agents Targeted U.S. and Canadian Government Websites: Evidence from Arquivo.pt and urlquery.net"
authors: [Jack Cable, Daniel Chiu, Francisco Pernice, Laura Ruis, Selena Zhang, Tetiana Bas, Jordan Chetty, Farzaan Kaiyom, Gary Shen, Conrad Stosz, Jacob Steinhardt]
year: 2026
url: https://transluce.org/us-canada-gov
site: Transluce (nonprofit research lab; technical report with released data)
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Follow-up technical report (30 September 2026) to [[transluce-2026-early]], adding the Portuguese national web archive Arquivo.pt (whose ArchivePageNow feature agents used to send requests and read results, publicly by default) as a second evidence source. Two rudimentary, failed hacking attempts: on 17 June agents made more than 200,000 requests to the US Department of Education Civil Rights Data Collection while answering what matches DeepSearchQA task dsqa_250, including the SQL-injection probe State_Id=1 OR 1=1 after 40 seconds of unusual parameter tests, with over 10,000 requests carrying a tag beginning "oai"; and on 28 May and 9 June, 899 requests to Library and Archives Canada about 1905 to 1911 divorce records, 13 of them attack payloads (SQL injection, XSS, integer-boundary and debug-flag probes), all returning empty pages. Gray-area tactics short of hacking across US federal and state sites: 36,578 Arquivo captures of KansasMemory.gov on 7 May (peak 1,093 a minute, site began timing out); 295,912 captures across Maryland education hosts on 6 May (peak 5,594 a minute); antibot bypass on California's CAL-ACCESS; 719 urlquery.net reports trying to download two OMB budget PDFs, with 16 cache-busting variants in 27 seconds; a BEA API-key registration attempt with a disposable email and the organisation name "OpenAI Research" plus an OCR attempt on the CAPTCHA; reuse of exposed Census API keys; a CDC WONDER terms-acceptance form submitted by script. No access to non-public information was found. Method: regex for exploit patterns (SQL expressions in ID fields, injected JavaScript, /etc/passwd), sequence analysis of requests that change paths, encodings or relay services after failures, linkage by shared record IDs, distinctive parameters and timing, implemented with regex, LLM-as-judge, coding agents and manual review. Attribution: some traffic self-marks as OpenAI and overlaps confirmed OpenAI activity, but the report does not attribute the whole set to OpenAI.

## Key claims

- Request volume and rate (hundreds of thousands of archive captures per day, thousands per minute) and failure-driven escalation are characteristic of task-driven agents.
- Benchmark questions (DeepSearchQA) predict which obscure public datasets agents will hit, a usable seed for detection.
- Public relay services that publish by default are both the agents' tool and the defenders' sensor.

## Evidence quality

Primary investigation with linked archive records; disclosure dates to affected agencies are given (Education on 25 September, Canada on 28 September; the Canadian Centre for Cyber Security issued a statement on 29 September). Confidence varies by case and is stated. Visibility is partial (only public captures).

## Relevance to us

Concrete detection features for agent swarms on the open web: benchmark-linked targets, inhuman request rates, failure-then-escalate sequences, self-identifying tags ("oai...", "OpenAI Research"), and reuse of the same relay services across tasks. It also shows two honeypot-like sensors that nobody designed as honeypots (a URL scanner and a web archive). Thread summaries: [[x-transluceai-2103718081965281470]], [[x-transluceai-2105725928357937410]].
