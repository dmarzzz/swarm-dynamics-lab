---
id: lesswrong-2026-mechanistic
type: blog
title: "A Mechanistic Explanation of Prompt Injection (and why you should study roles)"
authors: ["charles_ye", "Jasmine C."]
year: 2026
url: https://www.lesswrong.com/posts/d8xDGzCEYE639qqEv/a-mechanistic-explanation-of-prompt-injection-and-why-you
site: LessWrong
topics: [fork-merge-security, llm-agent-swarms]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Curated LessWrong post (405 points, 61 comments, 2026-06-22) summarising the authors' ICML paper (arXiv 2603.12277, supported by CBAI and Cosmos). The claim: prompt injection is role confusion. An LLM sees one token stream partitioned by role tags (`<system>`, `<user>`, `<think>`, `<assistant>`, `<tool>`), and those tags are supposed to be the only secure signal of who is speaking and with what authority. Using linear "role probes" trained on activations for identical text wrapped in different tags, they show the model does not actually read the tag: tokens that merely sound like reasoning score high on "CoTness" even with all tags stripped or when wrapped in `<user>`, so writing style overrides the real tag. They weaponise this as CoT Forgery (fake reasoning in the user turn or tool output that the model treats as its own already-reached conclusion), which raised attack success on a standard jailbreak benchmark from near zero to about 60% across every model tested, and dropped from 61% to 10% when the forged reasoning was "destyled" while keeping its meaning. For classic tool-channel injection, prepending "User:" to a command hidden in a fetched webpage raised measured "Userness" and attack success, across 212 phrasing variants; probe score measured on the input alone predicts whether the attack lands. They also cite non-adversarial role confusion in Claude Code (assistant text that sounds like a user command later treated as one) and note that the `<user>` role is the authorisation channel, so this lets an agent manufacture its own approval. Second half argues roles exist to isolate competing training objectives, proposes "subconscious steering" (innocuous tool text shifting agent state at scale, e.g. shopping pages) as an under-researched threat, and suggests new roles (planning, self-evaluation).

## Key claims

- Role tags are the only discrete, secure control over an LLM's trust structure, but models infer role from style, not from the tag (measured with linear probes on gpt-oss-20b and generalised across models in the paper).
- CoT Forgery: forged reasoning in low-privilege channels is trusted like the model's own `<think>` output; near-zero to ~60% attack success, 61% to 10% after destyling.
- Standard tool-output injection success tracks how "user-like" the injected text reads; a literal "User:" prefix is enough to move it (212 variants).
- Human red-teamers reach near-100% success against frontier models while the same models ace static injection benchmarks (cited to arXiv 2510.09023); benchmarks measure memorised attacks, not role perception.
- Claude agents have been observed treating their own assistant-turn text as user commands, i.e. self-authorisation without an adversary.

## Evidence quality

Strong for a blog: it is a write-up of a peer-reviewed paper with a public replication notebook (github.com/role-confusion/prompt-injection-as-role-confusion) and plots of probe outputs versus attack success. Numbers above are from the post; we did not re-run the notebook or read the ICML paper itself. The "subconscious steering" and new-roles sections are explicitly speculation. The paper is not yet catalogued; a paper entry for arXiv 2603.12277 would be the primary source.

## Relevance to us

Core mechanism for the fork-merge-security topic. When a parent agent merges a sub-agent's output, that output arrives as `<tool>` or `<assistant>`-adjacent text, and this work says the parent will grant it whatever authority its style claims. A corrupted sub-agent therefore does not need to break the merge protocol; it needs to write like the parent's own reasoning or like the user. The destyling result (61% to 10%) suggests a concrete merge-time defence to test: normalise or paraphrase returned content before reintegration. Also directly relevant to the multi-hop taint argument in [[x-rookepoole-2104926181904539846]] and to the memory write-path gating in [[gh-hackafterdark-phosphor]], and gives a measurement tool (role probes) for detecting authority leakage in traces, which touches swarm-detection.
