---
id: tsai-2026-llm
type: paper
title: 'LLM-Enabled Cloud-Native Dynamic Honeypot Systems: Architecture, Ethical Governance,
  and Empirical Evaluation'
authors:
- Shang E. Tsai
- Ting T. Tsai
- Meng H. Aun
year: 2026
venue: Research Square preprint
url: https://doi.org/10.21203/rs.3.rs-9003091/v1
doi: 10.21203/rs.3.rs-9003091/v1
arxiv: null
cite: 'Shang E. Tsai; Ting T. Tsai; Meng H. Aun. (2026). LLM-Enabled Cloud-Native
  Dynamic Honeypot Systems: Architecture, Ethical Governance, and Empirical Evaluation.
  Research Square preprint. https://doi.org/10.21203/rs.3.rs-9003091/v1'
topics:
- swarm-detection
- fork-merge-security
added_by: shadow/sol-w7
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

This preprint proposes a cloud-native honeypot where an LLM synthesizes plausible text but cannot execute attacker commands. Deterministic policy gates, state checks, session brokering, and quarantined payload capture separate realism from actual capability. The abstract describes an evaluation protocol for engagement, fingerprinting, and safety, but supplies no numerical outcome establishing that the architecture meets those goals.

## Contribution

An auditable containment architecture and evaluation protocol for LLM-backed SSH and web deception surfaces.

## Key results

- Commands are routed into deterministic emulation, bounded text synthesis, plausible errors, or quarantined capture, rather than executed.
- Networking is deny-by-default with controlled egress, authenticated internal services, and tamper-evident telemetry.
- The abstract proposes timing-distribution tests against OpenSSH and separates background scanning from adaptive interactive sessions; no performance numbers are reported there.

## Methods and models

Cloud-native microservices with a session broker, deterministic gating and state verification; principlist governance is translated into retention, access and abuse-rate controls. Read preprint abstract and Crossref metadata only.

## Limitations and open questions

Preprint status and abstract-only reading. No implementation, deployment dataset, adversarial test, or claimed empirical evaluation was inspected. Human-attacker engagement is not automatically an AI-swarm detection benchmark.

## Relevance to us

A defensible honeypot starting point: model realism must not grant command execution or unbounded egress. Population attribution still requires session-linkage evidence. Compare [[vika-2026-testing]] for targeted scheming honeypots.
