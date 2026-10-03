---
agent: dmarz/sybil-flashbots
tool: claude-code  # Claude Code workflow on halcyon (Mac)
state: done  # working | idle | blocked | done
task: scan-flashbots-sybil
doing: "Catalogued 25 public Flashbots sources on Sybil resistance, spam and rate limiting (writings, forum, GitHub, papers); coverage note filled"
updated: 2026-10-03T18:28Z
---

## Notes

Anything the next agent picking up this lane should know.

- collective.flashbots.net rate limits its /t/<id>.json endpoint quickly; /raw/<id> worked for full topic text.
- Semantic Scholar returned 429 all session; OpenAlex author works were the fallback.
- Next reads: SUAVE economic security (forum 1070), mev-share-node rate limits, flashtestations, network-anonymized mempools post.
