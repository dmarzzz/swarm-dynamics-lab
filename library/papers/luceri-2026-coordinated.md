---
id: luceri-2026-coordinated
type: paper
title: "Coordinated Inauthentic Behavior on TikTok: Challenges and Opportunities for Detection in a Video-First Ecosystem"
authors: ["Luca Luceri", "Tanishq Vijay Salkar", "Ashwin Balasubramanian", "Gabriela Pinto", "Chenning Sun", "Emilio Ferrara"]
year: 2026
venue: "Proceedings of the International AAAI Conference on Web and Social Media (ICWSM)"
url: https://arxiv.org/abs/2505.10867
doi: "10.1609/icwsm.v20i1.42711"
arxiv: "2505.10867"
cite: "Luceri, L., Salkar, T. V., Balasubramanian, A., Pinto, G., Sun, C., & Ferrara, E. (2026). Coordinated Inauthentic Behavior on TikTok: Challenges and Opportunities for Detection in a Video-First Ecosystem. Proceedings of the International AAAI Conference on Web and Social Media, 20(1), 1533–1550."
topics: [swarm-detection]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "14 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Adapts similarity-network coordination detection to TikTok using synchronized posting, similar captions, multimedia reuse and hashtag sequence overlap, with graph pruning. On 793K TikTok videos about the 2024 US election they find synchronized amplification of political narratives and semi-automated content replication with AI-generated voiceovers and split-screen formats. Traditional indicators transfer; transcript similarity and Duet/Stitch interactions do not.

## Contribution

First CIB detection framework for a video-first platform, with a list of which coordination signals transfer and which fail.

## Key results

- 793K videos analysed (abstract).
- Found semi-automated replication using AI-generated voiceovers, an in-the-wild sign of generative AI used inside coordinated campaigns (abstract).
- Text similarity of transcripts and Duet/Stitch signals proved ineffective (abstract).

## Methods and models

User similarity networks per trace, graph pruning to dense subnetworks, following [[luceri-2024-unmasking]].

## Limitations and open questions

Abstract only; no precision or recall figures in the abstract. Negative finding on transcript similarity may reflect templated content norms rather than detector failure.

## Relevance to us

Documents generative AI (voiceovers) already inside coordinated campaigns, and that content-similarity signals can fail when templates are the platform norm. Relevant to whether LLM paraphrase defeats text-based coordination signals.
