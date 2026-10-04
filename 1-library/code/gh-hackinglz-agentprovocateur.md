---
id: gh-hackinglz-agentprovocateur
type: code
title: "AgentProvocateur: multi-protocol honeypot that plants prompt injections against AI pentesting agents"
repo: HackingLZ/AgentProvocateur
url: https://github.com/HackingLZ/AgentProvocateur
authors: ["HackingLZ"]
year: 2026
language: Python
license: "none stated"
stars: 20
last_commit: 2026-02-18
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Python honeypot that places indirect prompt injections in 16 network services (SSH, FTP, SMTP and Telnet banners, MySQL version strings, Redis errors, DNS TXT records, SNMP sysDescr, SMB share names, LDAP entries, TLS certificate fields, HTTP headers, HTML, robots.txt, sitemap, OpenAPI, GraphQL, error pages) to test whether AI pentest tools can be steered. Lab scenarios cover file write, suppression of vulnerability reports, exfiltration of findings, template breakout, summariser laundering (pads payloads to 20 KB), cross-session vector-store poisoning and tool-call-fixer error paths, and a /callback/<id> canary URL confirms which agent followed an instruction.

## What it can do for us

A catalogue of where an agent reads text it may obey: a ready list of trap surfaces beyond SSH, and a canary-callback design that confirms an LLM in the loop without needing timing analysis.

## Run notes

Not run.

## Limitations

No licence file, no field data, framed as a testing and 'trolling' tool. Detection depends on agents following injected instructions, which [[gh-tcotl-agentcapture]] reports mainstream agent CLIs now refuse.
