---
id: gh-floriangroetschla-agentsnet
type: code
title: "AgentsNet: benchmark of LLM agents on a graph solving distributed-computing tasks (colouring, matching, leader election, consensus, vertex cover) by synchronous message passing"
repo: floriangroetschla/AgentsNet
url: https://github.com/floriangroetschla/AgentsNet
authors: ["Florian Grötschla", "Luis Müller", "Jan Tönshoff", "Mikhail Galkin", "Bryan Perozzi"]
year: 2025
language: Python
license: "MIT"
stars: 38
last_commit: 2025-07-16
topics: [llm-agent-swarms, sync-consensus, collective-decision]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: ran
relevance: 5
papers: [grotschla-2025-agentsnet]
---

## Summary

Simulation model: one LLM per node of a graph (Watts-Strogatz, Barabasi-Albert, Delaunay instances from the HF dataset disco-eth/AgentsNet); each synchronous round every node sends a natural-language message to each neighbour (JSON keyed by neighbour name) and reads only its neighbours' messages; after the last round each node outputs an answer scored against the task (graph colouring, maximal matching, leader election, consensus, vertex cover). Scale: 4 to 16 nodes in the main benchmark, the paper reports up to 100. LLM-native: yes, LangGraph/LangChain with OpenAI, Anthropic, Gemini, Together and Ollama backends. Adversarial hooks: none built in, but the per-node `message_passing` coroutine in `LiteralMessagePassing.py` (558 lines) is the obvious place to swap in a Byzantine or sybil node. Weight: light, one Python file plus a dataset download.

## What it can do for us

Closest ready-made testbed for 'LLM swarm on a known topology' with ground-truth scoring from distributed computing. Adding k Byzantine nodes to consensus or leader election gives a clean Sybil/Byzantine-tolerance experiment with an exact success metric, and the graph generators let us vary topology. Transcripts are saved per node, which is useful for swarm-detection features.

## Run notes

Installed and ran on 2026-10-03 with local Ollama `llama3.1` 8B (no API key).

```
git clone --depth 1 https://github.com/floriangroetschla/AgentsNet
uv venv -p 3.11 venv-an
VIRTUAL_ENV=venv-an uv pip install datasets pandas scipy networkx numpy==1.26.4 \
  "langchain<0.4" "langchain-core<0.4" "langgraph<0.7" "langchain-ollama<0.4" \
  "langchain-openai<0.4" "langchain-anthropic<0.4" "langchain-google-genai<3"
OLLAMA_URI=http://localhost:11434 venv-an/bin/python main.py --model llama3.1 \
  --task coloring --graph_models ws --graph_size 4 --samples_per_graph_model 1 --rounds 4
```

Gotchas: Python 3.9 fails (`int | None` annotations); current langchain 1.x fails (`langchain.schema` removed), so pin 0.3; `OLLAMA_URI` must be set or it raises KeyError. Result: graph ws_4_0 (4 nodes, diameter 1, max degree 3), 4 rounds, score 0.833, no JSON or answer parse failures, 8 min 28 s wall time on the laptop. Answers ['Group 2', 'Group 3', 'Group 1', 'Group 3']. First-round messages were mostly questions about strategy rather than colour proposals.

## Limitations

Small research code (38 stars, last push July 2025) with a hard-coded model-to-provider table; adding a model means editing `MODEL_PROVIDER`. Synchronous rounds only; no asynchrony, message loss or identity layer. Local 8B models are slow (about 2 min per round on 4 nodes), so 16-node runs want an API model or a GPU server.
