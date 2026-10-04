---
id: liu-2026-safe
type: paper
title: "Safe to Check, Unsafe to Use: Relinking at the Compression Boundary of LLM Agents"
authors: [Zesen Liu, Zihan Zhang, Dongdong She]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.21732
doi: null
arxiv: '2606.21732'
cite: "Liu, Z., Zhang, Z., & She, D. (2026). Safe to Check, Unsafe to Use: Relinking at the Compression Boundary of LLM Agents. arXiv:2606.21732."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

Agents compress long contexts by summarisation before acting. Filters inspect the pre-compression context, but the backend acts on the newly generated summary. The authors identify "relinking": the summariser, acting as a confused deputy, joins separated, individually benign fragments into a complete, actionable malicious instruction. An attacker splits a payload into innocuous pieces placed in untrusted parts of the trajectory so the full instruction never exists before compression. Their tool, Relink, automates the split; their defence, KBRA, audits the compression boundary.

## Contribution

Shows that summarisation is not only lossy (as in [[zerhoudi-2026-compaction]]) but generative: it can create an attacker instruction that was never present in any inspected input.

## Key results

- Measured: across four long-context agent benchmarks (619 samples, including 30 from AgentDojo), Relink reaches an 86.9% relink rate and backend action rate, against 17.0% for clean-split controls.
- Measured: existing prompt-injection defences do not reliably catch adversarial relinking because no fragment is malicious on its own.
- Measured: the KBRA boundary audit reduces residual backend action rate to 0.0%.
- Argued: relinking arises from summarisation itself (attention makes fragments jointly available, pre-training makes connections plausible, post-training favours compact actionable summaries).

## Methods and models

Threat model splits the trajectory into trusted (system prompt, config, trusted memory, tool schemas) and untrusted (user content, retrieved documents, tool observations) parts; the attacker controls only untrusted parts. Defender sees pre-compression source, compressed context and backend action. A DSL-based generator places action-side and value-side fragments at distance.

## Limitations and open questions

Only skimmed here; model list and per-benchmark breakdown not checked. The defence is evaluated against the authors' own attack.

## Relevance to us

Q3, strongly. A sub-agent returning from a long excursion is likely to be summarised before its findings enter the parent: by itself, by an orchestrator, or by the parent. This paper shows that step can assemble an attacker instruction from pieces that each pass inspection. That bears on Q2 as well: if the parent merges summaries of several parts, fragments planted across different parts could relink in the merged summary, so k-of-n agreement on each part's raw content does not bound what the merge produces. The defence implication is to check the merged, compressed artifact, not only the inputs. Related: [[zerhoudi-2026-compaction]], [[xie-2026-what]], [[greshake-2023-not]].
