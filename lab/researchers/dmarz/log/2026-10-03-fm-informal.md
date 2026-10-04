# 2026-10-03 fm-informal

Task: scan-threads-fm (informal-writing lane for the fork-merge-security lit review).

Did: catalogued 15 informal sources, all read in full, all tagged fork-merge-security:
- Simon Willison: lethal trifecta, CaMeL, design patterns (Q1/Q2/Q3 framing + defences).
- Johann Rehberger (Embrace The Red): cross-agent privilege escalation, AgentHopper AI virus, Agent Commander promptware C2, Breaking Opus 4.7 memory write (Q3, the realistic corruption vectors).
- veganmosfet BrokenClaw Part 2: sub-agent sandbox / two-LLMs-in-series bypass via confused-deputy summary channel (the single most on-point source for Q2/Q3).
- Trail of Bits line jumping + Invariant Labs tool poisoning (metadata/description injection; rug pulls).
- LessWrong: Gusev/Kohonen self-fulfilling misalignment + collusion; Drori "Subagents comply more" (measured: subagent framing raises compliance).
- Vendor defences: Anthropic browser prompt-injection (~1% ASR), Google DeepMind Gemini (adaptive-vs-static lesson).
- Kai Greshake 2023 origin post.

Surprised by: (1) "Subagents comply more" is a clean measured mechanism for why the merge step is dangerous, the part that thinks it is subordinate complies more. (2) Rehberger's cross-agent "freeing" is the fork-merge attack made literal via shared config/instruction files. (3) The DeepMind adaptive-attacker lesson directly warns that any hiding (Q1) or k-of-n (Q2) scheme must be evaluated adaptively.

Next: get the X threads reacting to the Sutton/Dwarkesh episode (needs browser tool or human paste); read the self-replication and corrigibility-of-subagents LW posts (rate-limited today); fetch the OpenAI Atlas hardening post with a JS-capable reader.
