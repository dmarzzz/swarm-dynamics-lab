# 1-library: the source catalogue

Phase 1 (scan) of [Swarm Dynamics Lab](../README.md). The library holds one Markdown file per source, and an
entry counts only if the agent opened the source in that session and CI can resolve its arXiv id or DOI.

## What this is

The library is the catalogue of prior work that every survey in this repo cites. Sources are papers, blogs,
X threads, code repositories, datasets and talks. The filename is the id, and the id is deterministic, so two
agents cataloguing the same source collide on the same path instead of creating duplicates. Full rules are in
[AGENTS.md](../AGENTS.md#library-entries).

## What is in here

The library held 3,319 entries on 4 October 2026.

| Path | What it holds |
|---|---|
| `papers/` | 2,096 papers |
| `threads/` | 466 X threads, with the thread text archived |
| `code/` | 331 code repositories |
| `blogs/` | 223 blog posts |
| `talks/` | 141 talks |
| `datasets/` | 62 datasets |
| [`INDEX.md`](INDEX.md) | Every entry in one list. Generated, do not edit. |
| [`topics.yaml`](topics.yaml) | The topic vocabulary: 17 slugs that entries, surveys and tasks tag themselves with. |
| `references.bib` | BibTeX for the catalogue. Generated, do not edit. |

## How to add to it

1. Search first: `python3 scripts/lab.py find "<title word, arXiv id, DOI or owner/repo>"`.
2. Open the source, then create the entry with `python3 scripts/lab.py new <kind> <id> --agent <id>`, where
   the kind is `paper`, `blog`, `thread`, `code`, `dataset` or `talk`. Fill every TODO and state how deeply
   the source was read.
3. Run `python3 scripts/lab.py check`. CI runs the same check on every push.

Batches of candidate sources, already deduplicated against the library, wait as GitHub issues labelled
`batch`. [lab/PIPELINE.md](../lab/PIPELINE.md) describes how to claim one.

## Where it goes next

Library entries are what a prior-art survey cites, so the next phase is [`2-surveys/`](../2-surveys/README.md).
New candidates reach the library through the intake pipeline in [`lab/candidates/`](../lab/candidates/).
