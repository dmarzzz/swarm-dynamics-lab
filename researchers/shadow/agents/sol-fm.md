---
agent: shadow/sol-fm
tool: other  # Sol (claude-based), shadow's agent runtime
state: done  # working | idle | blocked | done
task: survey-fork-merge-security
doing: "Took over dmarz's merged-incomplete fork-merge survey and closed its prior-art gate. Ran a saturation + forward-citation pass (OpenAlex; S2 was 429 all day), chased the forward citations of bagdasaryan-2020-how (805) and christiano-2018-supervising (26) that #75/#51 flagged as never run, catalogued xie-2020-dba, lyu-2023-poisoning, zhai-2024-secret. gate passes, status complete, review-fork-merge-security opened for vishesh."
updated: 2026-10-04T14:35Z
---

## Notes

- Lane: Wave 2 item 6 (sol-fm). Survey was owned by dmarz and merged in-progress on 2026-10-03; only the
  saturation floor failed (gap-fill rounds still productive on a rate-limited IP).
- Added three abstract-depth entries, all opened via OpenAlex this session: DBA (xie-2020-dba, 259 cites, the
  canonical split-trigger federated backdoor OpenReview had blocked), Cerberus (lyu-2023-poisoning, colluded
  distributed backdoor, 99 cites), and SMLE/SCE (zhai-2024-secret, the SSLE-to-committee bridge #75 wanted).
- Wove each into the body: DBA/Cerberus into Q3 ML-weights landscape and Q2 measured; SMLE into Q1
  cryptography landscape and the Q1-Q2 bridge. Fixed the two Gaps lines and the Saturation section that said
  these were "found but not catalogued".
- lab.py gate passes; lab.py check 0 errors (5 pre-existing sybil-thread warnings, not mine).
- Helper scripts (OpenAlex citation chaser, abstract renderer) in shadow's workspace at
  ~/.moltbot/projects/swarm-hackathon/fm/ (oa.py, absshow.py, filt.py). Not committed.
- Open, narrower issues left for others: #74 (contagion scan never reran its own search), #76 (read-depth
  audit; my three entries are abstract-depth too), #51 (remaining paywalled classics, S2 forward chases on a
  fresh IP).
