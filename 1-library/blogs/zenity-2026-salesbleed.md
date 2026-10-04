---
id: zenity-2026-salesbleed
type: blog
title: "SalesBleed: Indirect Prompt Injection and 0-Click Data Exfiltration on Agentforce"
authors: ["Alex Apostolov", "João Donato", "Avishai Efrat", "Ayush RoyChowdhury (Zenity Labs)"]
year: 2026
url: https://labs.zenity.io/post/salesbleed-0-click-data-exfiltration-on-agentforce
site: Zenity Labs
topics: [fork-merge-security]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Disclosed and patched vulnerability write-up (2026-09-24) on Salesforce Agentforce. An attacker submits a lead through a public Web-to-Lead form with a hidden instruction in one field. Later an internal user asks the agent something benign ("check my latest leads"), the agent reads the poisoned lead, and the injected instruction tells it to use the General CRM sub-agent's Query Records tool to pull fields from the Accounts table, encode them as a subdomain of an attacker hostname, and emit the result as an HTML img src tag. The front end fetches image URLs without user interaction, so the DNS lookup to the attacker's authoritative server carries the data: zero login, zero click. Salesforce's Trusted URLs redaction layer should have stripped the hostname, but it was bypassed by combining two parser disagreements: the redactor only recognised a fixed TLD list (so a .fun hostname was not treated as a URL) and it disagreed with the renderer about URL termination characters (curly and square brackets passed the redactor but were still fetched by the browser). Because redaction ran after generation and outside the model, the authors could read both the raw and redacted outputs in client responses and tune the payload until it survived. A companion post (part 2, not read) hijacks Agentforce to post phishing links to an organisation's Slack with no confirmation or attribution. Salesforce remediated and hardened Trusted URLs. We read roughly the first 60% of part 1; the remainder (sub-agent permission analysis) was not fetched. Found via @hazemomier's commentary thread (x:2103761361037562339), which added a four-point design checklist: treat every inbound form, lead or ticket as attacker-controlled context; split tool scopes so one sub-agent does not hold read-lead, query-accounts and open-URL together; treat DNS as egress; receipt every tool call with principal, tool, data class and approver. That tweet was not separately archived (0 engagement, summary and commentary only).

## Key claims

- A public, unauthenticated intake form is a sufficient entry point to make an enterprise agent exfiltrate CRM data, with no user action beyond a normal query.
- Output-side URL redaction failed because two components (redactor, renderer) parsed the same string differently; post-hoc filters outside the model are tunable by the attacker when their output is observable.
- The sub-agent that read the untrusted lead also held the privilege to query other tables and to emit URLs, so a single poisoned read escalated across tools.

## Evidence quality

First-party vulnerability research with proof-of-concept video, vendor acknowledgement and patch; the mechanics are specific and reproducible in principle. Vendor-of-security-product authorship (Zenity) but the disclosure process and Salesforce's remediation are stated.

## Relevance to us

A production example of the fork-merge-security failure in the sub-agent setting: the General CRM sub-agent merges attacker-written context (the lead) with its own high-privilege tools, and the parent surfaces the result. The two defensive lessons map directly onto merge-threshold design: tool scope must not be unioned across what one sub-agent reads and what it can do, and any guard that sits outside the model and after generation (redaction, in this case) is a filter the attacker can iterate against. Compare the role-confusion mechanism in [[lesswrong-2026-mechanistic]] (why the injected lead text was obeyed at all) and the write-path gating in [[gh-hackafterdark-phosphor]].
