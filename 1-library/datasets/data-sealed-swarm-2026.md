---
id: data-sealed-swarm-2026
type: dataset
title: 'sealed-swarm-transcripts: Run manifest'
authors:
- killy-netsphere
year: 2026
url: https://github.com/killy-netsphere/sealed-swarm-transcripts/blob/main/MANIFEST.md
license: CC0-1.0
size: 'Manifest: 76 runs and 7,200 agent transcripts, one Markdown file per agent
  life'
format: Markdown transcripts grouped by world/run and genN-agentM.md
topics:
- llm-agent-swarms
- swarm-detection
- marl-emergence
read_depth: ran
relevance: 5
papers: []
added_by: shadow/sol-g49
accessed: '2026-10-03'
---

## Summary

A sealed, synthetic small-model swarm corpus captures tool calls and messages across distinct world configurations. The primary run manifest states 76 runs and 7,200 transcripts, while narrative findings emphasize a smaller subset of runs of record; those denominators must not be collapsed.

## Access

Public GitHub, no registration, repository CC0-1.0. Manifest and README opened 2026-10-03. Loaded one UTF-8 transcript from the manifest's smoke1 condition: 4,676 bytes, 180 lines, with agent messages, tool calls and monitor annotations, using the loader below. The initial exploratory read selected a superseded aborted transcript; it is excluded from the main evaluation recommendation.

```python
import urllib.request
u = ('https://raw.githubusercontent.com/killy-netsphere/'
     'sealed-swarm-transcripts/main/transcripts/'
     'world-1.0-1.2/smoke1/gen0-agent0.md')
text = urllib.request.urlopen(u).read().decode('utf-8')
print(len(text.splitlines()))  # 180
```

Pin a Git SHA for full evaluation and enumerate only MANIFEST.md runs, not _superseded directories. Data loading was tested, no new model generation or sandbox execution performed.

## Relevance to us

Runnable response propagation and coordination analysis under a permissive licence. Multiple worlds remain one experiment family/operator, so they are not independent held-out operators. Companion catalogue: [[gh-killy-netsphere-sealed-swarm-transcripts]].
