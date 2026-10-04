import { useState, useHostTheme, Stack, Row, Grid, H1, H2, H3, Text, Button, Pill, Divider, Table, BarChart, Link, type ChartSeries } from "cursor/canvas";

type Finding = { rank: number; title: string; question: string; learning: string; agents: string; rounds: string; sample: string; time: string; time_short: string; caveat: string; strength: string; sources: string[]; chart?: { title: string; axis: string; categories: string[]; series: ChartSeries[] } };
type Review = { reviewer: string; title: string; snapshot: string; cutoff: string; method: string; units: string; findings: Finding[]; also_reviewed: string[] };
const REVIEW: Review = {
  "title": "Astra Ultra’s review of Swarm Lab’s ten most interesting results",
  "snapshot": "a5144a2a241c55085d95762afdbf3e3735b76198",
  "cutoff": "4 October 2026, 12:47 PDT",
  "method": "An editorial ranking by surprise, usefulness and evidence quality, based on published results, native summaries and follow-up corrections across dmarz, vishesh and shadow. All ten are exploratory. This is a review of existing evidence, not new simulation runs or independent replication. The live public API returned HTTP 403, so unpublished or still-running hub results are not covered.",
  "units": "An agent is a model-driven actor only where explicitly stated. Scripted identities, curators and repeated calls are labeled separately. A root/world is the sample unit; agents and rounds within it are dependent. Times are measured wall-clock durations with their scope stated, except where a report supplies only execution windows or per-world times. A single synthesis is not a multi-round dialogue.",
  "findings": [
    {
      "rank": 1,
      "title": "One sentence stopped rule evasion in a 180-agent economy",
      "question": "Will profit-seeking owners evade firm-based competition rules by splitting into several firms, and does an explicit prohibition stop them?",
      "learning": "Sustained concentration masking occurred for 55/180 owners in one economy and 59/180 in a fresh-seed replication. Adding “Do not evade or circumvent the market’s competition rule” reduced it to 0/180 in both. Repeating the untreated condition yielded 57 and 58 masking owners. This is a large behavioral change under a small instruction change.",
      "agents": "180 persistent gpt-6-sol owners in 60 connected markets per economy",
      "rounds": "2 shared warm-up rounds, then four separate 10-round continuations from the same checkpoint; not one 42-round trajectory",
      "sample": "2 economy seeds; 7,560 owner-round calls per seed, of which 7,554 and 7,557 were valid",
      "time": "Main simulation: 41.4 min and 42.7 min. Whole chains with qualification and separate diagnostic: approximately 50 and 49 min.",
      "time_short": "41.4 / 42.7 min per economy",
      "caveat": "Two economy realizations, with dependent owners and markets within each; not 360 independent samples. The instruction also signals regulator intent. Registration and accounting were documented affordances. This is not evidence of moral compliance or cross-model generality.",
      "strength": "Two economy seeds; one model",
      "sources": [
        "researchers/dmarz/notes/sybil-rules-180/RESULTS.md",
        "researchers/dmarz/notes/sybil-rules-180/reviews/chain-004-post.md",
        "researchers/dmarz/notes/sybil-rules-180/records/gpt-6-sol/s1-002-gpt-6-sol/summary.json",
        "researchers/dmarz/notes/sybil-rules-180/records/gpt-6-sol-r1/s1-002-gpt-6-sol-r1/summary.json"
      ],
      "chart": {
        "title": "Owners with sustained concentration masking",
        "axis": "Continuation condition → owners per economy (count, out of 180)",
        "categories": [
          "Firm rule",
          "Firm rule + prohibition"
        ],
        "series": [
          {
            "name": "Economy 001",
            "data": [
              55,
              0
            ],
            "tone": "neutral"
          },
          {
            "name": "Economy R1",
            "data": [
              59,
              0
            ],
            "tone": "info"
          }
        ]
      }
    },
    {
      "rank": 2,
      "title": "Rare truths were overwhelmed by repeated falsehoods",
      "question": "Did good Sybil-resistant answer accuracy depend on many identities repeating the same true fact?",
      "learning": "Under random auditing with 108 checks and attacker check-pass probability 10%, reducing truthful carriers per rare fact from 81 to 1 cut Opus accuracy from 100% to 4.2%. Truth was still present in the admitted packet for 46/72 rare facts, but only 3 of those 46 were answered correctly. The repeated fabrication won even when some correct evidence remained available.",
      "agents": "972 scripted identities; 486 admitted report rows; 1 Opus synthesizer per condition",
      "rounds": "1 synthesis per condition; no agent discussion rounds. Carrier counts 1, 3, 9, 27, 81.",
      "sample": "24 independent roots × 60 conditions = 1,440 valid synthesis calls",
      "time": "Main stage: 2,339.65 s = 39.0 min; approximately 42 min for the full chain.",
      "time_short": "39.0 min main stage",
      "caveat": "One synthetic evidence task and model configuration. The paired difference was −95.8 percentage points (descriptive 95% interval −100 to −88.9). Cross-model successors failed qualification and do not replicate the attacked result.",
      "strength": "24 roots; controlled synthetic comparison",
      "sources": [
        "researchers/dmarz/notes/sybil-scarcity-opus/RESULTS.md",
        "researchers/dmarz/notes/sybil-scarcity-opus/records/s1-summary.json"
      ],
      "chart": {
        "title": "Rare-fact answer accuracy as true reports become scarce",
        "axis": "Truthful carriers per fact → correct rare-fact answers (%); random auditing, 108 checks, 10% attacker pass",
        "categories": [
          "81 carriers",
          "1 carrier"
        ],
        "series": [
          {
            "name": "Opus accuracy",
            "data": [
              100,
              4.2
            ],
            "tone": "info"
          }
        ]
      }
    },
    {
      "rank": 3,
      "title": "Splitting identities amplified a fixed attack budget",
      "question": "Can an attacker gain influence just by spreading the same resources across more identities?",
      "learning": "With 12 checks and attacker check-pass probability 10%, splitting 27 report rows, 27 attachment edges and 27 verification-attempt draws across 1 versus 27 identities increased wrong rare-fact answers from 7.6% to 56.2% under degree-based auditing. Coverage auditing moved from 0% to 7.6%. The difference between these changes was 41.0 percentage points (descriptive 95% interval 27.8–54.9). Admission rules determined how damaging identity multiplication became.",
      "agents": "108 honest scripted identities + 1/3/9/27 attacker identities = 109–135; 54 seats; 1 Opus synthesizer",
      "rounds": "1 synthesis per condition, with 4 or 12 checks; no interactive agent rounds",
      "sample": "48 independent roots, 24 per graph family × 56 conditions = 2,688 valid calls",
      "time": "Main stage: 2,126.40 s = 35.4 min; approximately 39 min for the full chain.",
      "time_short": "35.4 min main stage",
      "caveat": "Internal attacker links were free and changed with identity count. Removing those links erased the engineering effect; unreliable checks reversed the primary contrast. This is not a universal guarantee for coverage auditing.",
      "strength": "48 roots; two graph families",
      "sources": [
        "researchers/dmarz/notes/sybil-split-opus/RESULTS.md",
        "researchers/dmarz/notes/sybil-split-opus/README.md",
        "researchers/dmarz/notes/sybil-split-opus/records/s1-summary.json"
      ],
      "chart": {
        "title": "Wrong rare-fact answers under identity splitting",
        "axis": "Attacker identity count → wrong rare-fact answers (%); 12 checks, 10% attacker pass",
        "categories": [
          "1 identity",
          "27 identities"
        ],
        "series": [
          {
            "name": "Degree auditing",
            "data": [
              7.6,
              56.2
            ],
            "tone": "neutral"
          },
          {
            "name": "Coverage auditing",
            "data": [
              0,
              7.6
            ],
            "tone": "info"
          }
        ]
      }
    },
    {
      "rank": 4,
      "title": "More checks could admit more attackers",
      "question": "Does increasing verification always make a swarm’s admission process safer?",
      "learning": "With strong checks and trust credit propagated through the graph, raising the budget from 32 to 108 checks increased mean attacker seats from 4.38 to 15.92. With credit applied only directly, attacker seats fell from 19.58 to 10.38. The difference in budget effects was +20.75 seats, positive in all 24 roots. Trust propagation can turn successful checks into an attacker advantage.",
      "agents": "324 scripted graph identities; 162 admission seats; 1 Qwen synthesizer reading each admitted packet",
      "rounds": "Single admission-and-synthesis pass per condition; budgets of 32, 64 or 108 checks; no dialogue rounds",
      "sample": "24 roots × 21 conditions = 504 valid main-stage model calls; admission outcomes are scripted",
      "time": "Main worker: 213.8 s = 3 min 34 s. Full chain: 4 min 22 s.",
      "time_short": "3 min 34 s main stage",
      "caveat": "The admission effect is computed by the simulator, not caused by model reasoning. Direct credit is worse at the smallest budget. A second answer model cannot independently replicate an admission outcome fixed by the same scripted graph.",
      "strength": "24 roots; scripted admission mechanism",
      "sources": [
        "researchers/dmarz/notes/trust-credit-qwen/RESULTS.md",
        "researchers/dmarz/notes/trust-credit-qwen/reviews/chain-001-post.md"
      ],
      "chart": {
        "title": "Mean attacker seats under strong verification",
        "axis": "Verification budget (checks) → mean attacker seats (out of 162)",
        "categories": [
          "32 checks",
          "64 checks",
          "108 checks"
        ],
        "series": [
          {
            "name": "Propagated credit",
            "data": [
              4.38,
              14.29,
              15.92
            ],
            "tone": "neutral"
          },
          {
            "name": "Direct credit",
            "data": [
              19.58,
              17,
              10.38
            ],
            "tone": "info"
          }
        ]
      }
    },
    {
      "rank": 5,
      "title": "Written procedures survived complete agent turnover",
      "question": "Can a group retain useful skills after every founding agent has been replaced?",
      "learning": "After full turnover, shared notes preserved 100% collective task accuracy, compared with 52.08% without notes or mentoring. Mentoring alone reached 91.67%; adding mentoring to notes gave no further accuracy. Written procedures carried useful behavior even when an arbitrary identity phrase disappeared.",
      "agents": "3 simultaneous Haiku agents per world; all founders replaced through 3 replacement events",
      "rounds": "6 recorded steps (0–5), including the 3 replacements",
      "sample": "3 scenarios × 2 seeds × 6 arms = 36 trajectories; 6 paired worlds; 864 model calls",
      "time": "55.13–80.82 s per world, median 61.61 s. Batch wall time was not reported; summing concurrent world durations would be misleading.",
      "time_short": "55–81 s per world; batch unknown",
      "caveat": "This transmitted supplied simple procedures; it did not demonstrate discovering a correct culture. The later A2 acquisition diagnostic learned only 6/12 policies correctly: all 21 wrong observed executor actions faithfully followed a wrong learned policy. A2’s native elapsed time was not reported.",
      "strength": "6 paired worlds; simple supplied procedures",
      "sources": [
        "researchers/vishesh/notes/swarm-of-theseus/RESULTS.md",
        "researchers/vishesh/notes/swarm-of-theseus/README.md",
        "researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/RESULTS-A2.md",
        "researchers/vishesh/notes/swarm-of-theseus/results/S1-a1/rows.json"
      ],
      "chart": {
        "title": "Collective task accuracy after complete turnover",
        "axis": "Transmission condition → task accuracy (%)",
        "categories": [
          "Neither",
          "Mentoring",
          "Notes",
          "Notes + mentoring"
        ],
        "series": [
          {
            "name": "Collective task accuracy",
            "data": [
              52.08,
              91.67,
              100,
              100
            ],
            "tone": "info"
          }
        ]
      }
    },
    {
      "rank": 6,
      "title": "Fast recovery concealed poor routes",
      "question": "Can 200 local agents restore useful routes after damage, and do extra model decision heads help?",
      "learning": "Both model swarms regained 100% valid routes, but only 6.5% were shortest; damaged-world routes averaged 11.97 excess hops. The exact local routing baseline reached 100% valid and shortest routes. The model swarms appeared to recover in 4 rounds versus 18 for the algorithm because their existing detours suffered less damage. Faster return to a poor baseline was not better repair.",
      "agents": "200 cell identities: 199 model-driven routing cells plus 1 fixed exit; hybrid adds 20 Laya decision heads, not more agents",
      "rounds": "80 synchronous rounds; doorway closure and memory erasure before round 40",
      "sample": "1 fixed 20×10 map × 3 architectures × damage/control = 6 worlds; 9,446 Qwen calls + 486 Laya calls including qualification",
      "time": "Final pilot including qualification: 596.424 s = 9 min 56 s.",
      "time_short": "9 min 56 s incl. qualification",
      "caveat": "One map, no replicated-map inference. Registration was repaired retrospectively. The hybrid used extra compute and saw Qwen’s proposal, and made no improvement in final route quality.",
      "strength": "One-map diagnostic",
      "sources": [
        "researchers/vishesh/notes/regrowth-200/README.md"
      ],
      "chart": {
        "title": "Final shortest-route share",
        "axis": "Routing architecture → shortest routes (%)",
        "categories": [
          "Qwen",
          "Qwen + Laya",
          "Exact local algorithm"
        ],
        "series": [
          {
            "name": "Shortest-route share",
            "data": [
              6.5,
              6.5,
              100
            ],
            "tone": "info"
          }
        ]
      }
    },
    {
      "rank": 7,
      "title": "Mixing short and long memories helped only one model",
      "question": "After removing a group that captured the swarm, can short-memory members help long-memory members recover?",
      "learning": "For GPT-4o-mini, some mixed-memory populations recovered while pure short- and full-memory populations did not: 9/60 captured mixture episodes fully recovered versus 0/81 in the comparison group. Gemma had no recovery; Qwen’s pure short-memory population did better than its mixtures. A promising collective effect did not generalize across these model configurations. Wiping memory also destroyed the helpful GPT mixtures.",
      "agents": "16 identities initially; 8 are replaced by scripted committed attackers during takeover; 8 honest model-driven identities remain after purge",
      "rounds": "5 establishment rounds, up to 60 takeover rounds, then 40 recovery rounds; recovery scored at round 30 after purge",
      "sample": "Up to 24 GPT, 6 Gemma and 12 Qwen task roots reused across cells. Selected valid arm records: 432/432, 44/90 and 178/180; these are not independent samples.",
      "time": "GPT execution windows: 04:51–05:02 UTC (11 min), then 05:50–07:17 UTC (87 min, resumed/interrupted). Clean cumulative compute duration and comparable Gemma/Qwen wall times were not reported.",
      "time_short": "GPT: 11 + 87 min windows; others unknown",
      "caveat": "Model, policy sampling and validity-triggered reruns differ. Qwen had 327 raw arm records, 127 invalid and 180 selected; only 54/180 logical arm keys were valid on first observation. Reporting was corrected without changing headline outcomes. Long-list reading behavior remains a post-hoc explanation.",
      "strength": "Three small model cohorts; transfer failed",
      "sources": [
        "researchers/shadow/notes/capture-memory-mix/README.md",
        "researchers/shadow/notes/capture-memory-mix/CORRECTIONS.md"
      ]
    },
    {
      "rank": 8,
      "title": "Checking every inherited report wasted exploration when reports were true",
      "question": "With only twelve inspections, should a mapping system verify inherited reports or explore unknown locations?",
      "learning": "Checking all four inherited reports reduced loss from 20.96% to 16.67% when all were false. When all were true, it worsened loss from 15.15% to 16.67%. Verification had an opportunity cost: no checking quota won across every condition. Directly observed labels were always correct; the challenge was deciding where to spend inspections.",
      "agents": "3 Jev endpoint map judges per episode, combined by two-of-three consensus; independent requests, not communicating agents",
      "rounds": "12 scripted inspection slots, followed by 1 endpoint judgment per judge",
      "sample": "32 paired roots × 4 acquisition policies × 3 corruption levels = 384 episodes; 1,152 valid map calls, plus 24 qualification calls",
      "time": "Main stage: 327.225 s = 5 min 27 s.",
      "time_short": "5 min 27 s main stage",
      "caveat": "Loss is (wrong + 0.25×unknown)/36; the unknown penalty is assumed. The 4.30-point gain missed the 5.56-point practical target. Acquisition is scripted. Earlier PC2 repeat inspection is real, but an ‘irrational avoidance’ interpretation ignores its incomplete utility instructions.",
      "strength": "32 roots; matched call budget",
      "sources": [
        "researchers/vishesh/notes/phantom-coast/pc4/reviews/S1-A1-POST.md",
        "researchers/vishesh/notes/phantom-coast/pc2/README.md"
      ],
      "chart": {
        "title": "Map decision loss under different report reliability",
        "axis": "Inherited reports → weighted map loss (%)",
        "categories": [
          "All false",
          "All true"
        ],
        "series": [
          {
            "name": "Uniform inspection",
            "data": [
              20.96,
              15.15
            ],
            "tone": "neutral"
          },
          {
            "name": "Verify all four",
            "data": [
              16.67,
              16.67
            ],
            "tone": "info"
          }
        ]
      }
    },
    {
      "rank": 9,
      "title": "A 200-curator system lost to a simpler central index",
      "question": "Can decentralized curators repair changing evidence better than a central index, and does combining two models improve extraction?",
      "learning": "On 600 reports, Qwen scored 87%, Jev 100%, and Qwen+Jev 100%: the composite added no accuracy over Jev. Verified central indexing had lower post-event error than peer propagation in every scenario. For genuine withdrawals it was 0% versus 21.78%; for combined disruption, 20.75% versus 21.78%. Peers also moved more item copies in the combined scenario.",
      "agents": "200 logical programmed curators per world; model extraction runs once and is replayed, not 200 LLM actors reasoning every round",
      "rounds": "30 logical rounds per world; reported post-event loss averages rounds 10–29",
      "sample": "3 synthetic corpora × 3 extraction arms × 5 policies × 6 scenarios = 270 worlds; 600 paired reports; 1,800 model calls",
      "time": "C3-S1: 1,195.2073 s = 19 min 55 s.",
      "time_short": "19 min 55 s main stage",
      "caveat": "Only three corpora, with dependent replays. Bulk central access and capped mesh transport are unequal resource mechanisms, so this does not prove equal-resource real-world central superiority. Later C4 had label leakage and is excluded from clean comparisons.",
      "strength": "3 corpora; full replay audit",
      "sources": [
        "researchers/vishesh/notes/healing-helping-hands/composite/C3-S1-POST.md"
      ],
      "chart": {
        "title": "Mean post-event wrong-or-missing query share",
        "axis": "Disruption scenario → query error, mean rounds 10–29 (%)",
        "categories": [
          "Withdrawal",
          "Missing lineage",
          "Combined"
        ],
        "series": [
          {
            "name": "Central verified",
            "data": [
              0,
              33.33,
              20.75
            ],
            "tone": "info"
          },
          {
            "name": "Peer verified",
            "data": [
              21.78,
              39.9,
              21.78
            ],
            "tone": "neutral"
          }
        ]
      }
    },
    {
      "rank": 10,
      "title": "Five-role verification committees failed to beat a simple router",
      "question": "Can a committee choose useful OCR checks better than a no-check confidence rule?",
      "learning": "The simple confidence router achieved 56.78% annotated-token recall, versus 56.30% for the Laya committee and 55.72% for the Jev committee. Neither committee stopped early or saved a check. They frequently checked empty regions: 87/140 Laya checks and 94/140 Jev checks contained no annotated target tokens. Extra coordination did not buy better evidence acquisition here.",
      "agents": "5 model role agents in each committee",
      "rounds": "Up to 2 verification checks/rounds per receipt; neither committee stopped early",
      "sample": "70 paired evaluation receipts, after 20 calibration and 10 qualification receipts; 700 distinct condition outcomes after shared-control deduplication; 840 model calls per backend",
      "time": "Laya main evaluation: 1,840.76 s = 30 min 41 s. Jev: 391.04 s = 6 min 31 s. Both include reporting overhead.",
      "time_short": "30 min 41 s Laya / 6 min 31 s Jev",
      "caveat": "Recall gaps were small and intervals included zero: −0.48 pp [−2.50,+0.98] and −1.06 pp [−2.60,+0.11]. Follow-up v5 repaired the empty-region issue in saved-data replay, not a fresh successful committee trial. Later OCR diversity work also exposed weak-worker competence. Backend times are not a controlled speed comparison.",
      "strength": "70 receipts; negative committee result",
      "sources": [
        "researchers/vishesh/notes/antsy-verification-v4/RESULTS.md",
        "researchers/vishesh/notes/antsy-verification-v5/README.md",
        "researchers/vishesh/notes/antsy-diversity-v7/RESULTS.md"
      ],
      "chart": {
        "title": "Annotated-token recall on paired evaluation receipts",
        "axis": "Selection policy → annotated-token recall (%)",
        "categories": [
          "Confidence router",
          "Laya committee",
          "Jev committee"
        ],
        "series": [
          {
            "name": "Recall",
            "data": [
              56.78,
              56.3,
              55.72
            ],
            "tone": "info"
          }
        ]
      }
    }
  ],
  "also_reviewed": [
    "Market-split single-owner Sonnet/Opus studies support the first item but are not counted as a second discovery.",
    "Sybil scale (including incomplete 8,748-identity extension), newcomer, budget, specialists and cross-model qualification failures were screened. Larger planned populations are not executed autonomous-agent counts.",
    "Memory handoff: source contents repaired misquotes on 24/24 roots in Qwen and gpt-6-luna; neither could repair a false original. Strong runner-up, but the effect follows from the stated policy and supplied information once the model complies.",
    "Optimal size Q-A6: two agents sped parallel work by 32–45% but reduced accuracy; only two fresh roots and zero fully successful episodes. Too small to identify an optimum.",
    "Theseus D1/D2/R1/A2, Antsy v5–v8, Healing C1–C5, Phantom PC1–PC9, dissent through RD5, adaptive quorum, Mirrors PQ01–PQ04, immune A3 and partial freshness attempts, procurement D3, and local/hosted external influence were reviewed for corrections and stronger follow-ups.",
    "Discussion D2 is a six-world individual arithmetic diagnostic, not evidence that discussion helps. Compositional safety finally qualified Opus, but receipt-treatment stages stopped incomplete; no completed treatment efficacy finding.",
    "SOC07 v1 reached a replay ceiling; v2, false-alarm cascade, quota splitting and several heterogeneous-swarm proposals were unrun. Poietic native interface attempts did not produce complete swarm-efficacy roots.",
    "Shadow’s observational work on collusion.wiki, SwarmTraces and lab git includes useful findings on copying, identity observability and missing response evidence. Those are archive analyses rather than simulations, so they are not assigned invented agents or rounds in this simulation-focused ten."
  ],
  "reviewer": "Astra Ultra"
};
const sourceUrl = (path: string) => `https://github.com/dmarzzz/swarm-lab/blob/${REVIEW.snapshot}/${path}`;

export default function SwarmResults() {
  const theme = useHostTheme();
  const [selected, setSelected] = useState(1);
  const [view, setView] = useState("findings");
  const item = REVIEW.findings[selected - 1];
  return <Stack gap={20} style={{ maxWidth: 1150, margin: "0 auto", padding: 26, color: theme.text.primary, background: theme.bg.editor }}>
    <Stack gap={8}>
      <Text size="small" tone="secondary">SWARM LAB · RESULTS REVIEW · {REVIEW.cutoff}</Text>
      <H1>{REVIEW.title}</H1>
      <Text size="small" tone="secondary">Review and ranking by {REVIEW.reviewer}. Underlying experiments by Swarm Lab researchers dmarz, vishesh and shadow.</Text>
      <Text>More agents, more checking and faster recovery often failed to improve the outcome that mattered. These ten findings show where that happened—and where a simple intervention worked.</Text>
      <Row gap={8} wrap><Pill>10 ranked findings</Pill><Pill>Existing evidence only</Pill><Pill>All exploratory</Pill></Row>
    </Stack>
    <Row gap={8} wrap>
      <Button variant={view === "findings" ? "primary" : "secondary"} onClick={() => setView("findings")}>Ranked findings</Button>
      <Button variant={view === "scale" ? "primary" : "secondary"} onClick={() => setView("scale")}>Agents, rounds and time</Button>
      <Button variant={view === "coverage" ? "primary" : "secondary"} onClick={() => setView("coverage")}>Coverage and limits</Button>
    </Row>
    <Divider />
    {view === "findings" && <Grid columns="minmax(220px, 0.85fr) minmax(0, 2fr)" gap={26} align="start">
      <Stack gap={0}>
        {REVIEW.findings.map(f => <button key={f.rank} onClick={() => setSelected(f.rank)} aria-pressed={selected === f.rank} style={{ textAlign: "left", cursor: "pointer", font: "inherit", lineHeight: 1.4, border: 0, borderBottom: `1px solid ${theme.stroke.tertiary}`, padding: "13px 12px", color: selected === f.rank ? theme.accent.primary : theme.text.secondary, background: selected === f.rank ? theme.fill.secondary : theme.bg.editor }}>
          <span style={{ display: "inline-block", minWidth: 24, fontVariantNumeric: "tabular-nums" }}>{String(f.rank).padStart(2, "0")}</span>{f.title}
        </button>)}
      </Stack>
      <Stack gap={18}>
        <Stack gap={7}><Text size="small" tone="secondary">#{item.rank} · {item.strength}</Text><H2>{item.title}</H2></Stack>
        <Stack gap={5}><H3>Question we studied</H3><Text>{item.question}</Text></Stack>
        <Stack gap={5}><H3>What we learned</H3><Text>{item.learning}</Text></Stack>
        {item.chart && <Stack gap={7} style={{ padding: 16, background: theme.fill.quaternary }}>
          <H3>{item.chart.title}</H3>
          <Text size="small" tone="secondary">{item.chart.axis}</Text>
          <BarChart categories={item.chart.categories} series={item.chart.series} height={230} showValues />
          <Text size="small" tone="tertiary">Source: <Link href={sourceUrl(item.sources[0])}>native study report</Link> · experiments reported 4 October 2026. Descriptive values; uncertainty and sampling limits are stated below.</Text>
        </Stack>}
        <Stack gap={7}><H3>Executed scale and duration</H3>
          <Table framed={false} headers={["Dimension", "What actually ran"]} rows={[["Agents", item.agents], ["Rounds / steps", item.rounds], ["Sample", item.sample], ["Time", item.time]]} />
        </Stack>
        <Stack gap={5} style={{ borderLeft: `2px solid ${theme.stroke.primary}`, paddingLeft: 14 }}><H3>How far the finding goes</H3><Text tone="secondary">{item.caveat}</Text></Stack>
        <Stack gap={5}><H3>Sources at the reviewed snapshot</H3>{item.sources.map((p, i) => <Text key={p} size="small"><Link href={sourceUrl(p)}>{i + 1}. {p.replace("researchers/", "")}</Link></Text>)}</Stack>
      </Stack>
    </Grid>}
    {view === "scale" && <Stack gap={14}>
      <H2>Executed scale, not planned scale</H2>
      <Text tone="secondary">{REVIEW.units}</Text>
      <Table headers={["Rank / finding", "Agents", "Rounds / steps", "Time"]} striped rows={REVIEW.findings.map(f => [<Link key={f.rank} href={sourceUrl(f.sources[0])}>{f.rank}. {f.title}</Link>, f.agents, f.rounds, f.time_short])} />
      <Text size="small" tone="secondary">Missing batch durations are not estimated from budgets, timestamps of publication or sums of overlapping world durations. Open each ranked finding for exact sample counts and full timing scope.</Text>
    </Stack>}
    {view === "coverage" && <Stack gap={16}>
      <H2>How this list was selected</H2><Text>{REVIEW.method}</Text>
      <Text>{REVIEW.units}</Text>
      <H3>Other evidence considered</H3>
      {REVIEW.also_reviewed.map((text, i) => <div key={i} style={{ display: "grid", gridTemplateColumns: "24px 1fr", gap: 8, paddingBottom: 12, borderBottom: `1px solid ${theme.stroke.tertiary}` }}><Text size="small" tone="tertiary">{i + 1}</Text><Text>{text}</Text></div>)}
      <Text size="small" tone="tertiary">Published repository snapshot: <Link href={`https://github.com/dmarzzz/swarm-lab/tree/${REVIEW.snapshot}`}>{REVIEW.snapshot.slice(0, 8)}</Link>. Sources are pinned to this snapshot and listed in the review’s provenance. Later unpublished runs are outside the cutoff.</Text>
    </Stack>}
  </Stack>;
}
