---
id: owasp-2025-llm
type: blog
title: 'OWASP Top 10 for LLMs and Gen AI Apps 2025'
authors: [OWASP Gen AI Security Project]
year: 2025
url: https://genai.owasp.org/llm-top-10/
site: OWASP Gen AI Security Project
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: skim
relevance: 2
---

## Summary

The 2025 edition of OWASP's consensus list of the ten most critical risks for LLM applications. LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Supply Chain, LLM04 Data and Model Poisoning (pre-training, fine-tuning or embedding data), LLM05 Improper Output Handling, LLM06 Excessive Agency, LLM07 System Prompt Leakage, LLM08 Vector and Embedding Weaknesses, LLM09 Misinformation, LLM10 Unbounded Consumption. Read from the project's list page.

## Key claims

- Prompt injection is ranked first (LLM01).
- Poisoning appears at the data and model level (LLM04) and at the vector store level (LLM08). LLM08 is the label that SMSR [[sharma-2026-smsr]] uses for runtime memory poisoning.
- Excessive agency (LLM06) is listed as a separate risk.

## Evidence quality

Consensus taxonomy, no measurements. Item descriptions on the list page are one-liners.

## Relevance to us

Background for Q3. The 2025 LLM list has no item for persistent cross-session agent memory or for agent-to-agent propagation. Those appear only in the agentic list [[owasp-2025-agentic]] (ASI06, ASI07, ASI08, ASI10). The gap shows that fork-merge corruption is newer than the mainstream LLM threat models.
