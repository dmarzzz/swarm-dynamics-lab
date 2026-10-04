---
id: data-ai-village-2026
type: dataset
title: AI Village dataset
authors:
- AI Digest
year: 2026
url: https://huggingface.co/api/datasets/aidigestorg/ai-village
license: 'Custom AI Village research terms: research/analysis only; no training or
  fine-tuning without written permission; no re-identification; citation required'
size: HF size category 1M to 10M records; usedStorage 392,608,511,991 bytes; hackathon
  promises >170,000 messages and >2 million computer-use turns
format: Gzipped JSONL tables plus image TAR archives; 13 configs including events,
  chat_messages, computer_use_turns and agent_memories
topics:
- llm-agent-swarms
- swarm-detection
- fork-merge-security
read_depth: skim
relevance: 5
papers: []
added_by: shadow/sol-g49
accessed: '2026-10-03'
---

## Summary

AI Village records frontier-model agents on separate computers pursuing open-ended goals and interacting through shared chat and changing memories. Its public metadata makes the corpus identifiable and the research terms explicit, but the underlying files are manually gated and not runnable anonymously.

## Access

Checked 2026-10-03: API metadata returns gated=manual and custom research terms; raw README access returns HTTP 401. Request Hugging Face access and mention the hackathon, as instructed at https://swarmchasing.com/logistics/. Approvals are manual. No access request submitted on someone else's behalf and no gated files downloaded.

API revision 838b4150303ca8228e8edb432d8b8ccae353d258, last modified 2026-09-20. The 392.6 GB usedStorage figure includes image archives and is not a JSONL download-size estimate. Logistics promises >170k messages and >2M turns, not independently counted here.

After approval, use the authorized HF token with `load_dataset('aidigestorg/ai-village', 'chat_messages', token=True)` and follow the supplied schema. Training/fine-tuning requires additional written permission.

## Relevance to us

Real independently built collaborating agents for behavior analysis and memory propagation. Availability is conditional, unlike [[data-sealed-swarm-2026]]; do not report it as immediately runnable without approved access.

## Notes from vishesh/codex-pi-review

2026-10-04: authenticated access verified at revision `838b4150303ca8228e8edb432d8b8ccae353d258`. Read the pinned README, SCHEMA and CHANGELOG; downloaded and parsed only agents (46 rows), village goals (51), agent goals (33) and rooms (16). The export manifest reports 2,510,487 computer turns, 78,362 sessions, 246,151 memories and 183,485 chat messages; those larger tables were not loaded or counted. Metadata access is not validation of behavioral data or labels. No private corpus text is reproduced here.

Use pinned JSONL files and the documented schema; the earlier `load_dataset` config suggestion above was not verified in this audit. Exact model prompts are absent, export-time roster fields do not reconstruct historical agent context, and the scaffolding changelog reports material room/memory/tool changes. New comparisons need point-in-time visibility and task-cluster splits. The terms also require publication notification. The researcher-specific access result does not establish access for other accounts.

[Study mapping and prospective replay design](../../researchers/vishesh/notes/ai-village-replay-2026-10-04/README.md) includes source hashes and read scope. [Pinned schema](https://huggingface.co/datasets/aidigestorg/ai-village/blob/838b4150303ca8228e8edb432d8b8ccae353d258/SCHEMA.md), [changelog](https://huggingface.co/datasets/aidigestorg/ai-village/blob/838b4150303ca8228e8edb432d8b8ccae353d258/CHANGELOG.md), [manifest](https://huggingface.co/datasets/aidigestorg/ai-village/blob/838b4150303ca8228e8edb432d8b8ccae353d258/manifest.json).
