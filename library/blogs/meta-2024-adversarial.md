---
id: meta-2024-adversarial
type: blog
title: "Adversarial Threat Report, First Quarter 2024"
authors: [Margarita Franklin, Lindsay Hundley]
year: 2024
url: https://md.teyit.org/file/meta-threat-report.pdf
site: Meta quarterly adversarial threat report (PDF mirror hosted by Teyit; original on transparency.meta.com)
topics: [swarm-detection]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Platform threat report (May 2024) on six covert influence operations Meta removed for coordinated inauthentic behaviour (CIB), from Bangladesh, China, Croatia, Iran, Israel and an unknown-origin network targeting Moldova and Madagascar, plus an update on Russia's Doppelganger. Meta's main GenAI finding: "we have not seen novel GenAI-driven tactics that would impede our ability to disrupt the adversarial networks behind them." Observed uses were GAN profile photos, AI-generated newsreader videos, likely AI-generated poster images (China's fictitious pro-Sikh "Operation K") and likely AI-generated comments. The Israel-based network, linked to Tel Aviv political marketing firm STOIC, ran 510 Facebook accounts, 11 Pages, one Group and 32 Instagram accounts, posting likely AI-generated comments under media and politicians' pages that were often unrelated to the post and drew replies calling them propaganda; many of its fake and compromised accounts were disabled by automated systems before the investigation began, and the operators kept replacing them, likely from account farms. Meta found it after DFRLab's public reporting on the same activity on X. The unknown-origin network had 1,326 Facebook accounts and was linked despite VPNs and anonymizers through operational slip-ups.

## Key claims

- Behaviour-based detection (coordination, account provenance, repeat-offender monitoring) still works against AI-assisted operations; content-based detection is not needed for these cases.
- Meta continuously removes accounts linked to previously removed networks using automated and manual detection.

## Evidence quality

Platform transparency report; counts are Meta's, methods described only at a high level, no false-positive rates. Skimmed: read the key insights and the Israel and unknown-origin network sections; the OpenAI May 2024 report on the same STOIC network was not opened.

## Relevance to us

The platform-side counterpart to the model-provider reports ([[openai-2025-disrupting]], [[anthropic-2025-detecting]]): Meta's 2024 position is that LLM text did not defeat behavioural CIB detection. Whether that holds against agent-orchestrated swarms that vary timing and engagement per persona is the open question.
