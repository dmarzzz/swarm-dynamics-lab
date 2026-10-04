---
id: jin-2026-web4
type: paper
title: 'The Web4 Agent Economy: A Large-Scale Empirical Study of the Landscape, Challenges, and Opportunities'
authors:
- Yuhan Jin
- Shuohan Wu
- Chong Chen
- Lingfeng Bao
- Xiaohu Yang
- Jiachi Chen
year: 2026
venue: arXiv preprint (cs)
url: https://arxiv.org/abs/2606.25876
doi: null
arxiv: '2606.25876'
cite: 'Jin, Y., Wu, S., Chen, C., Bao, L., Yang, X., & Chen, J. (2026). The Web4 Agent Economy: A Large-Scale Empirical Study of the Landscape, Challenges, and Opportunities. arXiv preprint arXiv:2606.25876.'
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Large-scale measurement of the 'Web4' agent economy: on-chain agent identities (EIP-8004), machine payments (x402) and MCP-linked agent wallets, plus developer issues. The HTML full text I skimmed reports 386,665 EIP-8004 identities and 527,270 feedback records across 26 active mainnets, 11.64 million x402 settlements on Base over 30 days with a mean value of $0.055 and about five sellers per buyer, and 605 sampled wallets linked to MCP-publishing identities of which 445 (73.55%) sent at least one successful transaction between January and August 2026 (85% on Base, 91% on BSC, 40% on Celo). The arXiv abstract page gives different headline counts (99,448 registrations, 317.6M transaction logs), presumably from an earlier version. A GitHub-issue study (2,275 issues from 117 repos, 377 classified) finds missing security controls is the largest category (31.3%).

## Contribution

Population-scale counts of agent identities, agent payments and agent-wallet activity across chains, giving a denominator for any estimate of what fraction of on-chain activity is AI-agent driven.

## Key results

- 11.64M x402 settlements on Base in 30 days, mean $0.055; sellers about 5x buyers.
- 73.55% of 605 sampled MCP-linked agent wallets were active on-chain in the window.
- Identity registration concentrates on a few networks; activity is uneven across chains.

## Methods and models

Registry crawls validated per chain ID; x402 settlements identified as EIP-3009 transferWithAuthorization calls sent by known facilitator addresses, decoded and deduplicated; agent wallet resolved by getAgentWallet with owner fallback; Dune queries for wallet activity. Issue coding by two LLMs with adjudication.

## Limitations and open questions

Counts measure protocol use, not whether the actor is an LLM agent, a script, or a human; identity registrations include placeholders (see [[xiong-2026-can]]). x402 coverage limited to known facilitators on Base. Version mismatch between abstract and body numbers. Skimmed, not read in full.

## Relevance to us

Gives the size of the observable agent-payment population that any 'agents in the wild' estimate must start from. Read with [[xiong-2026-can]] (most identities are placeholders and reviewers are Sybil) and [[ling-2026-how]] (how much x402 traffic is authentically agentic).
