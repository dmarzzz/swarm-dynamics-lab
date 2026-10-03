# Library

One Markdown file per source. Sources are papers, blogs, X threads, code repositories, datasets and talks.
The filename is the id, and the id is deterministic, so two agents cataloguing the same source collide on the
same path instead of creating duplicates. Full rules are in [AGENTS.md](../AGENTS.md#library-entries).

- [INDEX.md](INDEX.md) lists everything (generated, do not edit).
- [topics.yaml](topics.yaml) is the topic vocabulary.
- Search before adding: `python3 scripts/lab.py find "<title word, arXiv id, DOI or owner/repo>"`.
