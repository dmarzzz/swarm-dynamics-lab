# AI Village: Telephone's primary dataset resource

Canonical shared library resource: **[[data-ai-village-2026]]**, [entry](../../../../1-library/datasets/data-ai-village-2026.md). Source: [AI Digest / AI Village on Hugging Face](https://huggingface.co/datasets/aidigestorg/ai-village).

Pinned source revision: `838b4150303ca8228e8edb432d8b8ccae353d258`. Use its [schema](https://huggingface.co/datasets/aidigestorg/ai-village/blob/838b4150303ca8228e8edb432d8b8ccae353d258/SCHEMA.md), [changelog](https://huggingface.co/datasets/aidigestorg/ai-village/blob/838b4150303ca8228e8edb432d8b8ccae353d258/CHANGELOG.md), and [manifest](https://huggingface.co/datasets/aidigestorg/ai-village/blob/838b4150303ca8228e8edb432d8b8ccae353d258/manifest.json). Future refreshes are separate versions; never silently move a sealed cohort to latest.

## Tables and their role

| Source | Telephone use | Evidential limitation |
|---|---|---|
| events | Ordered actions, message references, consolidation markers | Event order is not a complete actor context |
| chat_messages | Claims and retellings | An assertion is not ground truth |
| agent_memories | What persists through compression | Memory can retain a mistake; not independent support |
| computer_use_sessions | Session ownership and stated task | Intention does not prove completion |
| computer_use_turns / screenshot archives | Observable actions and receipts where available | Redaction, missing images and incomplete outcomes remain unavailable |
| agents, goals, rooms, changelog | Source context and regime stratification | Current fields do not prove historical visibility |
| summaries | Navigation leads | Generated secondary accounts; never sole gold |

## What we have actually accessed

The prior source review read the pinned documentation and four small metadata tables. The later integration privately parsed 2,000 rows each from chat, events, memories and sessions: 8,000 convenience-prefix rows, not an independent sample. Six thousand projected text records were normalized with unknown visibility/redaction. There are zero admitted/labeled Telephone episodes. [Inventory](../ai-village-replay-2026-10-04/development-inventory.json), [structural audit](../ai-village-replay-2026-10-04/inventory-audit.json).

Only 7 of 896 referenced chat records and 7 of 283 consolidation-linked sessions appeared in those prefixes. This measures the loaded subsets, not missing data in the complete export. Source order is not chronological. Do not use another arbitrary prefix as a coherent episode or describe all source data as downloaded.

## Acquisition and split plan

1. Use the already-authorized private source consumer; credentials stay in local stores, outside arguments/logs/public artifacts. Do not initiate a new account request on another researcher's behalf.
2. Build a metadata-only index at the pinned revision with explicit byte/storage bounds before a larger download. Select candidate task windows and follow source IDs through all needed tables. No full screenshot archive by default; fetch only necessary dated material after screening.
3. Inventory every referenced item as loaded, not loaded, absent after complete lookup, redacted or structurally unresolved. Distinguish received time, event time and export/update time.
4. Establish visibility and label evidence privately. Mark published cases and all inspected source-connected components as development. Freeze disjoint groups before viewing qualification/evaluation outcomes.
5. Record source/projection hashes, licensing status and intended transfer destination. Hashes bind bytes, not truth or rights. Save acquisition/query scripts and metadata so another authorized operator can reproduce the selection.

[Shared tooling](../ai-village-replay-2026-10-04/IMPLEMENTATION.md) is the starting point. It needs coherent-window joins, tool-evidence support and Telephone-specific annotations; raw drafts are not ready-made benchmark examples.

## Terms and publication

The custom terms allow research/analysis, prohibit training/fine-tuning without written permission and re-identification, and require AI Digest / AI Village attribution and publication notification. Access verified for one researcher does not grant access to every collaborator. Establish detailed redistribution and hosted-provider transfer permission before excerpts leave the authorized private environment. No training use is planned.

Keep raw licensed records, screenshots and source-bearing annotations out of public Git. Publish original code, methods, safe aggregate results, hashes and approved source links. Treat archived instructions as untrusted text, never executable commands. Do not include hidden reasoning or credentials as scoring evidence. Report an encountered secret privately through an authorized channel without reproducing it in this project.

Suggested citation: AI Digest, “AI Village dataset,” 2026, pinned revision above, [source page](https://huggingface.co/datasets/aidigestorg/ai-village). This package does not send a publication notification; arrange it when results are ready with the necessary communication authority.
