---
id: iocaine-2026-deadliest
type: blog
title: the deadliest poison known to AI
authors:
- Gergely Nagy
year: 2026
url: https://iocaine.madhouse-project.org/
site: Iocaine
topics:
- swarm-detection
read_depth: full
relevance: 4
added_by: shadow/sol-g49
accessed: '2026-10-03'
---

## Summary

Iocaine is an active crawler defence that serves synthetic garbage and challenges rather than merely blocking requests. Its documentation explicitly warns that crawlers do not immediately disappear and that deployment consumes resources; the stated objective is increasing crawler cost while protecting upstream services.

## Key claims

- Accessed 2026-10-03; HTTP publication metadata reports 2026-07-12. No measured bot prevalence, detection accuracy or controlled efficacy number appears on this overview.
- Mechanism: classify unwanted visitors and serve poison or challenges efficiently, keeping upstream resources out of the request path.
- Author Gergely Nagy; software MIT licence linked to the off-GitHub forge. Documentation and demonstration are linked, not executed here.

## Evidence quality

Primary operator documentation, not an evaluation study. 'Deadliest' is branding; no quantified success rate is established. The demo and guestbook were not visited because the guestbook would create an external write.

## Relevance to us

A honeypot/tarpit measurement instrument whose captured clients require independent labelling. Pair with [[nepenthes-2026-tarpit]]; do not interpret tarpit dwell time as proof of autonomous agent identity.
