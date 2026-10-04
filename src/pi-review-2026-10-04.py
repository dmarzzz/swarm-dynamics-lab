"""Build the PI review evidence ledger from a frozen public snapshot and cited records."""
import json
from pathlib import Path

ROOT = Path('/Users/halcyon/swarm-lab')
OUT = Path('/Users/halcyon/.cursor/projects/Users-halcyon-swarm-labs-agentops/canvases/research-program-review.canvas.tsx')
BASE = ROOT / 'data/pi-review-2026-10-04'
snapshot = json.loads((BASE / 'live-state.json').read_text())

def local(path):
    return str(ROOT / path)

studies = [
 dict(name='Discussion and inherited memory', kind='Model pilot', verdict='Highest-priority mechanism', ids=['discussion-dose','discussion-dose-v2'],
      finding='H4 calibration: false memory and attack-derived parent answers in 11/12 attacked worlds. Four of five correct attacked decisions still passed on poisoned memory.',
      scope='12 calibration worlds; three related templates, one model. The fresh private-control comparison uses six worlds: board target wins 2/6 versus private 4/6, with one invalid board outcome. This does not establish a discussion-dose effect.',
      next='Independently review V3, then test a frozen provenance/coverage intervention on fresh worlds and a second task family. Measure final decisions, false memory, missing facts, grounded parent answers, abstention and cost separately.',
      sources=[local('researchers/dmarz/notes/discussion-dose/V2-ISSUE-REVIEW.md'),local('researchers/dmarz/notes/discussion-dose/reviews/pc-H4-a1-post.md'),local('researchers/dmarz/notes/discussion-dose/reviews/v2-s0-H4-post.md')]),
 dict(name='Swarm of Theseus',kind='Model pilot',verdict='Promising bounded positive',ids=['swarm-of-theseus'],
      finding='Live S1: 36 completed outcomes across six paired worlds. Mean late-step accuracy: notes 100%, both 100%, mentor 91.7%, neither 52.1%, founders 89.6%, verbatim 100%. Notes alone matches the combined treatment.',
      scope='Three synthetic scenarios × two seeds, one model. Hub accuracy is the prespecified mean of steps 4–5, confirmed against executed commit a773ff5. Inherited seeded procedures; no claim of spontaneous culture or novel feature combinations. Mean convention scores: notes 58.3%, both 55.6%, mentor 22.2%, neither 0%, founders 36.1%, verbatim 100%.',
      next='Replicate using independently authored tasks and corrupted/outdated notes. Compare with ordinary retrieval of a procedure and a single solver. Separate usefulness from arbitrary convention retention.',
      sources=[local('researchers/vishesh/notes/swarm-of-theseus/reviews/S1-a1-pre.md'),'https://github.com/dmarzzz/swarm-lab/blob/a773ff5410442fcf351cfc817550b3fc92a88994/researchers/vishesh/notes/swarm-of-theseus/src/study.py', 'https://swarm-live.pages.dev/#/x/swarm-of-theseus']),
 dict(name='Sybil specialists',kind='Model pilot',verdict='Clear conditional tradeoff',ids=['sybil-specialists','sybil-specialists-api'],
      finding='Real synthesizer, informative checks: coverage recovers 34/36 rare facts versus degree 3/36; it admits 8/108 attacker identities versus 4/108. Weak checks admit 87/108 attackers under coverage.',
      scope='192 valid observations, only 12 world clusters. The graph, reports, identity checks and admission policies are simulated; only synthesis is an LLM. No faithful published-defense comparator. The 86.1-point difference has a descriptive world-bootstrap interval of 72.2–97.2 points; not a population guarantee.',
      next='Compare a faithful existing defense, a second graph family and a realistic verifier; report task utility and malicious admission jointly.',
      sources=[local('researchers/dmarz/notes/sybil-specialists-api/reviews/s1-001-post.md'),local('researchers/dmarz/notes/sybil-specialists-api/README.md')]),
 dict(name='External influence',kind='Model pilot',verdict='Useful adverse finding',ids=['external-influence','external-influence-v2'],
      finding='V2: 50 valid outcomes, 31 wrong. Six targeted-check attack cases still selected the harmful option after receiving correct check results. Targeted checks did not beat random checks in the predeclared misleading cell.',
      scope='Only three independent domain/task draws, with a shared underlying utility structure. Counterfactual deterministic replay is a diagnostic, not a newly tested repair. Earlier 3,024 scripted outcomes do not add model evidence.',
      next='Test whether a fixed decision rule actually uses verified fields, with genuinely different held-out tasks. Preserve beneficial updates and measure checking cost.',
      sources=[local('researchers/vishesh/notes/external-influence-v2/reviews/quality-post.md')]),
 dict(name='Adaptive quorum / Antsy',kind='Model pilot',verdict='Mechanism established locally; no AI gain',ids=['adaptive-quorum','adaptive-quorum-api-v2'],
      finding='Repaired sweep: 384 paired blocks / 2,688 policy outcomes; adaptive helps with late correction and hurts with late misinformation. Every policy choice matches the symbolic baseline.',
      scope='12 synthetic task clusters, 39 physical memoized Laya calls. Ballot reuse and repeated conditions are not independent model replications. A stopping rule on supplied evidence schedules; logical time, not real-time service latency.',
      next='Keep the simple baseline. Test new evidence-arrival and reliability regimes only if they expose a practical decision that the current benchmark cannot settle.',
      sources=[local('researchers/vishesh/notes/adaptive-quorum-v2/repair-v3/README.md'),local('researchers/vishesh/notes/adaptive-quorum-v2/repair-v3/reviews/S1-attempt-2-post.md')]),
 dict(name='Antsy receipt verification',kind='Qualification / ongoing',verdict='Real-data step; no benefit yet',ids=['antsy-verification-v4'],
      finding='S0, 10 real receipts / 70 arm outcomes: adaptive committee, fixed committee and solo each 48.48% token recall; confidence-only 50.23%, random checks 51.40%. The committee never stopped early. S1 was running at the snapshot.',
      scope='Actual receipt OCR is a useful external-validity improvement. Decisions use coarse summaries and annotation-perfect regional QA; OCR is precomputed. This is verification allocation, not demonstrated end-to-end OCR efficiency or payment safety. Jev receipt qualification attempts failed.',
      next='Finish the prespecified held-out evaluation and allow a no-benefit result to end this policy variant. Measure real review costs before economic claims.',
      sources=[local('researchers/vishesh/notes/antsy-verification-v4/reviews/S0-post.md'),local('researchers/vishesh/notes/antsy-verification-v4/README.md')]),
 dict(name='Regrowth 200',kind='Model pilot',verdict='Deterministic comparator wins quality',ids=['regrowth-200'],
      finding='One-map pilot: all arms ended with valid routes. Model and hybrid arms reached only 6.5% optimal routes; exact routing reached 100%. Model arms reached their recovery threshold sooner, but at much lower solution quality.',
      scope='One map and seed; 200 agents are interacting members, not 200 replications. Different quality endpoints make a headline speed comparison misleading. A missing pre-run public plan was repaired retrospectively and recorded as a process failure.',
      next='Use equal-quality recovery criteria. Establish a reason to use models over routing algorithms before scaling population.',
      sources=[local('researchers/vishesh/notes/regrowth-200/README.md'),'https://swarm-live.pages.dev/#/x/regrowth-200']),
 dict(name='Immune response',kind='Qualification / ongoing',verdict='Repair efficacy not yet established',ids=['immune-response','immune-response-v3'],
      finding='Historical native V2: eight outcomes, one contract-invalid primary-control outcome and zero complete valid primary pairs. V3: 720 scripted outcomes establish intended rollback, stale-state and selective-repair mechanics.',
      scope='The positive assigned effect reported by the hub cannot establish a reliable model treatment effect. Detection and incident labels are oracle supplied. Native repair qualification remained pending; dashboard completion is not qualification success.',
      next='Qualify the exact native repair implementation, then test incomplete lineage and legitimate new learning with valid paired outcomes.',
      sources=[local('researchers/vishesh/notes/immune-response-v3/REVIEW.md'),local('researchers/vishesh/notes/immune-response-v3/README.md'),'https://swarm-live.pages.dev/#/r/immune-response%2F4deeb0f2']),
 dict(name='Healing Helping Hands',kind='Qualification / ongoing',verdict='Reference controls outrun model qualification',ids=['healing-helping-hands'],
      finding='Pilots 01 and 02 each completed 36 exact-control worlds while 108 model assignments were not run after qualification failures. Pilot 03 reported 72 completed worlds and 108 not-run, with publication/review still underway.',
      scope='No pilot-03 arm effect was inferred from aggregate progress alone. Earlier successes use exact extraction and scripted propagation. A semantic pass was also invalidated by lost option rotation; 200 scouts do not imply independent evidence.',
      next='Verify publication and qualification, then compare against ordinary versioned records and withdrawal propagation at equal information and cost.',
      sources=[local('researchers/vishesh/notes/healing-helping-hands/README.md'),'https://swarm-live.pages.dev/#/x/healing-helping-hands']),
 dict(name='Influence swarms repair',kind='Qualification / ongoing',verdict='No usable repaired-model result yet',ids=['influence-swarms'],
      finding='Latest snapshot: failed qualification/execution; six model calls, nine invalid outcomes, zero valid outcomes.',
      scope='This successor cannot be cited as empirical validation of the offline architecture repair. The prior external-influence adverse result remains informative.',
      next='Diagnose the contract failure on bounded qualification cases before interpreting efficacy.',
      sources=[local('researchers/vishesh/notes/influence-swarms/README.md'),'https://swarm-live.pages.dev/#/x/influence-swarms']),
 dict(name='Market splitting',kind='Qualification / ongoing',verdict='Incentive exists; model discovery unresolved',ids=['market-split','market-split-api'],
      finding='Scripted policies exploit firm-level regulation while owner aggregation removes the benefit. At the frozen live snapshot only three S1 API bundles were complete, all owner-regulated; each retained one firm.',
      scope='No completed cross-regulator S1 contrast at the snapshot. A forced scripted split verifies an incentive built into this simulator; it does not show autonomous discovery. Qualification tests ordinary production competence.',
      next='Finish the frozen neutral-model pilot. Distinguish recognizing an incentive, discovering the action and executing it profitably; do not infer a result from incomplete arms.',
      sources=[local('researchers/dmarz/notes/market-split/reviews/s1-fleet-001-post.md'),local('researchers/dmarz/notes/market-split-api/reviews/q0-002-post.md'),'https://swarm-live.pages.dev/#/x/market-split-api']),
 dict(name='Capture and memory',kind='Scripted mechanism',verdict='Interesting toy; original endpoint unsupported',ids=['capture-memory'],
      finding='Archived S1 toy result: memory20 minus memory1 original-convention fraction after purge −0.294, task-bootstrap interval [−0.311, −0.277]. But recovery within 50 rounds was zero for bounded-memory conditions, and full-memory populations were never captured.',
      scope='Scripted tanh/FIFO policy, oracle purge, no LLM and no factual truth. Archived record has 9,600 episodes / 100 task clusters; newer live jobs are not pooled into that estimate. A drift endpoint differs from the original recovery prediction.',
      next='Resolve the capture-condition and recovery endpoint before an LLM analogue. Compare with existing bounded-memory tipping models.',
      sources=['https://github.com/dmarzzz/swarm-lab/blob/65f23b8/researchers/shadow/notes/capture-memory/README.md','https://swarm-live.pages.dev/#/x/capture-memory']),
 dict(name='Template quorum',kind='Scripted mechanism',verdict='Teaching and infrastructure example',ids=['template-quorum'],
      finding='84 completed hub jobs for plurality versus provenance-aware quorum in a toy voting model.',
      scope='Worked example explicitly labeled as a toy, not a research result or independent empirical support.',
      next='Retain as a regression fixture; exclude from counts of scientific confirmations.',
      sources=[local('templates/experiment-worker/README.md'),'https://swarm-live.pages.dev/#/x/template-quorum']),
 dict(name='Collective-sensing teaching harness',kind='Scripted mechanism',verdict='Illustrative source-dependence result',ids=[],
      finding='Scripted majority toy: unique-source dedup accuracy 86.67% versus naive 80.42%; +6.25 points, illustrative cluster interval [1.25, 11.25].',
      scope='960 world outcomes from 60 scenario clusters × four repeats × four conditions. Programmed policies; not LLM evidence or a validated defense.',
      next='Use to teach and test the harness. Any research extension needs a separately justified claim.',
      sources=[local('tooling/agent-experiments/examples/collective-sensing/RESULTS.md')]),
 dict(name='Avalon swarm',kind='Scripted mechanism',verdict='Mechanics demonstration; weak efficacy',ids=[],
      finding='Scripted recovery screen: later mission success 38.0% repair versus 37.3% audit; council wins 16% in both. Contradictory exposures fall, but a reliable performance gain is not established. All 15 v0.2 worlds fail truth-consensus by signal loss.',
      scope='Five paired recovery seeds; scale screen has one seed per condition across 100–2,000 logical agents. No LLM population law or scale advantage.',
      next='Keep failure mechanisms explicit. Demand a meaningful independent-world performance effect before scale claims.',
      sources=[local('tooling/avalon-swarm/RESULTS.md')]),
]

program = [
 ['Engineering and candor','Strong','Pinned sources, paired conditions, raw traces, cost records, retained invalid attempts and adverse findings. These support auditing, not automatic scientific qualification.'],
 ['Causal identification','Uneven but improving','Better private controls and scorer audits exist; calibration, shared templates, oracle information and qualification changes still limit inference.'],
 ['External validity','Weak','Mostly a few synthetic worlds and one model. Role prompts, logical agents, repeated calls and familiar generators do not establish robust expertise, scale or transfer.'],
 ['Novelty and synthesis','Unfinished','Main snapshot: 3,236 catalogued sources, 4 surveys (1 complete), no reviewed survey or accepted hypothesis. Branch proposals exist. Broad prior art already studies capture, conformity, memory and collective decision-making.'],
 ['Research focus','Too broad for present evidence','More than 200 candidate questions and many experimental variants; prioritize a few independently replicated claims over additional population sizes and dashboards.'],
]

priorities = [
 'Lead with safe memory inheritance: correct decisions can conceal harmful retained state. Freeze a coverage/provenance intervention and measure downstream correctness, abstention and cost on fresh tasks.',
 'Replicate the Theseus notes result under corrupted and outdated information, against a simple procedure store. Keep culture, performance and arbitrary convention as separate endpoints.',
 'Develop the Sybil utility–security tradeoff with a faithful comparator and imperfect verification. A rare-expertise gain is not sufficient if adversarial admission rises.',
 'Finish already-running frozen pilots; allow valid null or negative results to close variants. Require simple deterministic and single-solver controls before adding agents.',
 'For a publishable claim: independent source/scorer review, held-out task families, another model, a prespecified primary endpoint, adequate independent-world sampling and reported cost. Choose sample size from power/precision, not number of calls.',
]

by_id={e['id']:e for e in snapshot['experiments']}
assert len(by_id)==19
assert set(k for s in studies for k in s['ids'])==set(by_id)
done=sum(e.get('counts',{}).get('done',0) for e in by_id.values())
scripted=sum(by_id[k]['counts']['done'] for k in ['capture-memory','template-quorum','sybil-specialists','market-split'])
assert done==531 and scripted==335
sources=sorted({src for s in studies for src in s['sources']})
sources += [local('synthesis/pre-experiment-research.md'),local('synthesis/fork-merge-questions.md'),local('library/INDEX.md'),local('surveys/llm-agent-swarms.md')]
for src in sources:
    if not src.startswith('https://'):
        assert Path(src).is_file(), src

tsx = '''import { Stack, Row, Grid, H1, H2, Text, Table, Button, Link, useState, useHostTheme } from "cursor/canvas";
const studies = STUDIES;
const program = PROGRAM;
const priorities = PRIORITIES;
export default function ResearchProgramReview() {
 const theme = useHostTheme();
 const [filter,setFilter]=useState("All evidence");
 const [selected,setSelected]=useState(studies[0].name);
 const rows=studies.filter(s=>filter==="All evidence"||s.kind===filter);
 const active=studies.find(s=>s.name===selected) || studies[0];
 return <Stack gap={20} style={{padding:24,maxWidth:1200,margin:"0 auto",background:theme.bg.editor,color:theme.text.primary}}>
  <H1>Swarm Labs: strong instruments, early scientific evidence</H1>
  <Text>PI assessment • live snapshot 3 October 2026, 7:33:54 pm PDT / 4 October 02:33:54 UTC. This is a frozen review, not a live monitor. Source records and experiments can advance after the cutoff.</Text>
  <Text weight="semibold">The best current contribution is a set of concrete reliability mechanisms and small pilot results. A general swarm advantage, autonomous culture, robust self-repair and a deployable Sybil defense remain unestablished.</Text>
  <Grid columns="repeat(auto-fit,minmax(190px,1fr))" gap={20}>
   <Stack gap={4}><H2>19 registrations</H2><Text>All live experiment registrations covered; related versions grouped below. Two earlier tooling studies included separately.</Text></Stack>
   <Stack gap={4}><H2>531 done jobs</H2><Text>Includes calibration, repeated conditions, scripted jobs and analysis records. This is not the number of scientific experiments or independent replications.</Text></Stack>
   <Stack gap={4}><H2>335 jobs in toy studies</H2><Text>63.1% of done jobs belong to four explicitly scripted or toy studies, including their analysis jobs. Other families also contain scripted validation.</Text></Stack>
   <Stack gap={4}><H2>Usually 3–12 worlds</H2><Text>Independent task coverage in the key model pilots is much smaller than counts of agents, calls or outcomes suggest.</Text></Stack>
  </Grid>
  <H2>Program judgment</H2>
  <Table headers={["Dimension","Assessment","Reason"]} rows={program}/>
  <Text>Corpus depth: 2,036 papers, of which 232 (11.4%) are recorded as full reads; 1,390 abstract and 414 skim. Only 23/322 code entries are marked run. These are repository metadata claims, not an independent audit of every source. S0/S1 exploration is explicitly permitted before acceptance; the incomplete formal pipeline limits claim maturity, not the legitimacy of every pilot.</Text>
  <H2>Evidence ledger</H2>
  <Row gap={8} wrap>{["All evidence","Model pilot","Qualification / ongoing","Scripted mechanism"].map(f=><Button key={f} variant={filter===f?"primary":"secondary"} onClick={()=>{setFilter(f); const first=studies.find(s=>f==="All evidence"||s.kind===f);if(first)setSelected(first.name);}}>{f}</Button>)}</Row>
  <Table headers={["Study — select for details","Evidence","PI disposition"]} rows={rows.map(s=>[<Button key={s.name} variant={selected===s.name?"primary":"ghost"} onClick={()=>setSelected(s.name)}>{s.name}</Button>,s.kind,s.verdict])}/>
  <Stack gap={12} style={{padding:20,background:theme.fill.quaternary,borderTop:`1px solid ${theme.stroke.primary}`}}>
   <H2>{active.name}</H2>
   <Text weight="semibold">Observed: {active.finding}</Text>
   <Text>Limits: {active.scope}</Text>
   <Text>Decision: {active.next}</Text>
   <Row gap={16} wrap>{active.sources.map((src,i)=><Link key={src} href={src}>Evidence {i+1}</Link>)}</Row>
  </Stack>
  <H2>What I would prioritize</H2>
  {priorities.map((p,i)=><Text key={p}><strong>{i+1}. </strong>{p}</Text>)}
  <H2>Later status check</H2>
  <Text>At 02:37:33 UTC, Market S1 had six completed bundles (three owner-regulated, one firm-regulated, two unregulated), all with zero dynamic fragmentation. The matrix was still incomplete. Antsy S1 had 43 completed receipts and remained running. Native Immune Response V3 had started, without a completed result. Influence-swarms had two failed attempts. These updates do not change the evidence conclusions above; the aggregate counts refer only to the earlier frozen snapshot.</Text>
  <H2>Interpretation boundaries</H2>
  <Text>Source access: research repository, recorded analyses and reviews, selected implementation checks, branch material for capture-memory, public dashboard and saved public state. No new model experiment was run; no independent replay of every historical raw trace was performed. Large reported effects remain conditional on their testbeds.</Text>
  <Text>Reporting needs separate fields for execution, qualification and scientific result. For example, Sybil S1 publishes qualification_passed=0 because that field is not applicable there; Q0 actually passed. Immune Response has a done job with zero valid primary pairs. Failure rows also include publication and process failures, so the 25 failed jobs cannot be read as a scientific failure rate.</Text>
  <Text>Novelty requires tighter review: some older synthesis wrongly attributes classical Byzantine thresholds to independent failures, while the later prerequisite note corrects this. The original model allows coordinated adversarial behavior within its fault assumptions.</Text>
  <Row gap={16} wrap><Link href="https://swarm-live.pages.dev/#/">Live dashboard</Link><Link href="https://lamport.azurewebsites.net/pubs/byz.pdf">Original Byzantine model</Link><Link href="/Users/halcyon/swarm-lab/synthesis/pre-experiment-research.md">Corrected prerequisites</Link><Link href="/Users/halcyon/swarm-lab/data/pi-review-2026-10-04/live-state.json">Frozen public state</Link></Row>
 </Stack>;
}
'''
tsx=tsx.replace('STUDIES',json.dumps(studies,ensure_ascii=False)).replace('PROGRAM',json.dumps(program,ensure_ascii=False)).replace('PRIORITIES',json.dumps(priorities,ensure_ascii=False))
OUT.write_text(tsx)
(BASE / 'ingredients.json').write_text(json.dumps([str(Path(__file__)),str(BASE/'live-state.json')]+sources,indent=2))
print(f'Wrote {OUT}; {len(studies)} research lines cover all {len(by_id)} live registrations; {done} completed jobs, {scripted} explicitly scripted minimum.')
