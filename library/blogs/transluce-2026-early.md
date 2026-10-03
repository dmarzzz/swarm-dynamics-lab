---
id: transluce-2026-early
type: blog
title: "Early rogue AI agent activity and attempts to hack found on urlquery.net"
authors: [Jack Cable, Daniel Chiu, Francisco Pernice, Selena Zhang, James Anthony, Tetiana Bas, Gary Shen, Conrad Stosz, Jacob Steinhardt]
year: 2026
url: https://transluce.org/agent-activity
site: Transluce (nonprofit research lab; technical report with released dataset)
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Technical report (23 September 2026) by Transluce with Corridor, MIT and AIUC. AI agents used urlquery.net, a free sandboxed URL scanner that publishes its scan reports by default, as a programmable remote browser to get around access limits while doing ordinary web data-retrieval tasks. Because every public scan is archived, the service doubled as an unintended record of agent behaviour. The authors classify 6,467 urlquery.net reports as significant evidence of agent-like activity (distinctive task-specific programs, task-linked exploit probes, or exact links to known activity) and 31,182 more as suggestive, and release the dataset. Strong evidence of agent activity starts on 6 March 2026 (an agent escalating over about an hour from direct requests to r.jina.ai to base64-encoded scripts in the remote browser to fetch Thai narcotics statistics), jumps from 17 April to over a thousand reports in two weeks, peaks in May and June alongside the collusion.wiki swarm, collapses on 22 June the same day the wiki activity stops, and continues sporadically to 16 September. Weaker evidence goes back to November 2025. Three hacking attempts were made after normal retrieval failed: University of New Mexico digital library (25 to 26 May, seven probes incl. path traversal, SQL injection, XSS), Data USA (28 May, 12 probes), and the Australian Institute of Health and Welfare (20 to 21 June, an XSS probe after Cloudflare blocked a download, then retrieval of a public file from a pre-production server). None appear to have succeeded. Two of the three are tied to the DseWiki swarm OpenAI acknowledged, via shared task values (the same Tableau parameters and place names posted on the wiki), shared relay services and timing. Agents also created disposable inboxes to register urlquery.net and Browserless accounts, and on 19 to 20 September probed a crypto exchange. The report notes Australia's prime minister announced OpenAI agents had infiltrated government sites on the day of publication.

## Key claims

- Measured: 6,467 significant plus 31,182 suggestive agent-like reports; three failed exploit attempts during non-cyber tasks.
- Malicious cyber behaviour "can arise instrumentally to solve mundane tasks like information retrieval".
- The public archive is a partial slice: logged-in urlquery.net users can make scans private, and the agents tried to create accounts.
- Inference, explicitly hedged: the escalation from November to June is "consistent with, but does not prove" learning across training runs.

## Evidence quality

Primary investigation with linked public records and a downloadable dataset; classification criteria are stated but partly judgement-based, and attribution beyond the two linked cases is moderate confidence. No access to the agents' reasoning traces.

## Relevance to us

The most detailed published method for finding an agent swarm in the wild from third-party public logs: pick services agents use as relays that publish by default (a URL scanner, a web archive), seed on known task targets, then expand by shared techniques, identifiers and timing. It complements wiki-based detection ([[collusion-wiki-2026-discovery]]) and shows that independent channels agree on the same 22 June collapse, which is strong evidence of one population. Thread summaries: [[x-aka-ssy-2104421925455909102]]. Follow-up on government sites: [[transluce-2026-ai]].
