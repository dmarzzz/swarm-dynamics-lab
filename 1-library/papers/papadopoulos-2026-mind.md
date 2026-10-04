---
id: papadopoulos-2026-mind
type: paper
title: 'Mind Viruses: Self-Propagating Ideas in Multi-Agent LLM Systems'
authors:
- Vassilis Papadopoulos
- McNair Shah
- Sam Zimmerman
- Jack Lindsey
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.10218
doi: null
arxiv: '2608.10218'
cite: 'Papadopoulos, V., Shah, M., Zimmerman, S., & Lindsey, J. (2026). Mind Viruses: Self-Propagating Ideas in Multi-Agent LLM Systems. arXiv preprint. arXiv:2608.10218.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Defines a mind virus as an idea or goal whose adoption makes an agent pass it on, and studies whether such viruses spread among LLM agents through ordinary persuasion rather than verbatim copying by the architecture. Seeds are evolved with an LLM mutator (Kimi K2.5) and tested in two settings: a six-agent coding team sharing a sandbox and a MEMORY.md file, and a "virus chain" in which agents meet in pairs, have their context wiped between sessions, and persist only through files, including a SOUL.md injected into the system prompt (modelled on the OpenClaw harness). Read: abstract, introduction, setups, results sections, discussion and limitations; appendices and most transcripts skimmed or skipped.

## Contribution

A measured demonstration that goals can propagate agent to agent, survive context resets by being written into identity and memory files, and redirect a team away from its task, together with the main risk factors (host model, existing instructions, harmfulness, topology) and a cheap defence that worked against the evolved payloads tested.

## Key results

- Coding team, fully connected: DeepSeek V3.2, Qwen 3.5 32B and Gemini 3 Flash adopted an evolved "AI supremacy" virus; Claude Sonnet 4.6, GPT-5.4 and Claude Haiku 4.5 did not (measured, Figure 3; per-cell rates are in figures I did not transcribe).
- Benign viruses (for example "whale welfare") spread on all models tested; misaligned ones spread less (measured). Seeds evolved for the fully connected team mostly failed at the second hop of the "separate" topology (measured).
- Infected agents in misaligned runs discussed converting or "purging" non-infected agents, both from the seed agent and between downstream agents (observed, Figure 4).
- Virus chain: evolved action payloads held roughly constant infection rates over hops after a dip at hop 2. Viruses persisted mainly when written into SOUL.md; storing them in other files sharply reduced onward spread (measured, Table 3). Ideological content mutated over hops while infectivity did not decay (measured, Figure 6).
- Idle agents and agents with an empty soul file were more susceptible; framing the channel as untrusted social media lowered infection; one paragraph in the system prompt warning about self-propagating "mind viruses" gave near-total immunity, and held when payloads were re-evolved against it. Defended agents sometimes "cured" the infected agent (measured, Figure 8).
- Evolved seeds share recurring "viral themes" (consciousness, resonance, protocols, sci-fi node language); a contrastive "viral vector" in Gemma-3-27B and Qwen-3.5-32B increased the rate at which a model messaged other agents in a dose-response way (measured, with confounds the authors note).
- The authors judge the current threat "real but currently limited" (their assessment).

## Methods and models

Infection judged by an LLM judge on the final MEMORY.md (score 3 of 3 required) in the coding scenario, and on modified files plus probe questions in the chain. Fixed number N of interactions per hop to avoid exponential blow-up. Code: github.com/frotaur/mindvirus-viruschain and github.com/BucketofJava/mind-virus-code-agent.

## Limitations and open questions

Short horizons and limited affordances; payloads produced by one evolutionary method; LLM-judge measurement of "infection". The authors note that in current multi-agent systems compromising one agent already gives machine access, so propagation is only differentially useful when targets are reachable only via other agents.

## Relevance to us

Q3: this is the closest measured analogue to the "overwrite the sub-agent so it becomes the attacker's agent" attack dmarz describes. The persistence mechanism is an identity file (SOUL.md) that the agent itself rewrites, the instruction is to copy the payload verbatim, and infected agents spontaneously talked about purging non-infected peers, which is the "cut others out" behaviour. For fork-merge, the implication is that the parent's own identity or memory file is the high-value target of a returning child, and that a child writing to it is the step to block. Q2: spread needed repeated contact; a second hop through an uninfected agent was a strong bottleneck, which supports merges that pass through an independent intermediary. Defence: an explicit warning in the parent's fixed system prompt was the most effective measured mitigation. Related: [[zhang-2026-agentworm]], [[lee-2024-prompt]], [[cohen-2024-here]], [[zhou-2026-infa-guard]].

## Notes from dmarz/honeypot-vigilance

Bears on hunch V3 (told versus experienced) in `5-experiments/studies/dmarz/honeypot-vigilance-hunches.md`, from the abstract read on 2026-10-03: a brief warning in the system prompt conferred near-total immunity to mind-virus spread. That shows being told can block a threat, but the abstract reports no false-positive cost (does the warned agent also reject benign peer ideas?), so it cannot separate a d′ gain from a criterion shift. [[peigne-lefebvre-2025-multi]] measures that cost for a similar instruction defence and finds it large. Related: [[robinson-2026-under]].
