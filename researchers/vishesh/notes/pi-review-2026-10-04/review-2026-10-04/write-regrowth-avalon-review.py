import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];V=json.loads((R/'review-2026-10-04/regrowth-avalon-verification.json').read_text())
F=[]
def add(id,severity,title,project,evidence,impact,recommendation,confidence='high'):
 F.append(dict(id=id,severity=severity,title=title,project=project,evidence=[dict(path=p,line=l,detail=d) for p,l,d in evidence],impact=impact,recommendation=recommendation,confidence=confidence))
add('AV-01','P1','Avalon can still launch every condition without the required public design registration','avalon-swarm',[
('avalon-swarm/benchmark.py',496,'CLI proceeds directly to directory creation, config plan, and measure(); it has no public_plan import, immutable plan URL, run TLDR, registration receipt, or preflight.'),
('avalon-swarm/README.md',13,'The documented runnable commands launch unregistered worlds.')],
'Future launches violate the owner\'s explicit requirement. Existing JSON plans establish assignments, but cannot establish public preregistration; no saved immutable-plan receipt exists in these run folders.',
'Use the existing small public-plan helper (after fixing REG-01), require condition-specific registered descriptions, and fail before any world initialization. Mark historical registration status unknown/not evidenced separately from the 45 completed executions; do not relabel them as preregistered.')
add('REG-01','P1','Preflight validates a page shape, not registration of the actual planned worlds','regrowth-200',[
('regrowth-200/src/public_plan.py',5,'validate() checks URL shape, TLDR prefix, 40-character run text, and five nonempty headings; it requires no limitations section, condition assignments, execution hash, plan classification, or protocol identity.'),
('regrowth-200/src/run.py',65,'One receipt is checked before assignments are constructed; the same run_tldr authorizes all six arm×damage worlds.'),
('review-2026-10-04/regrowth-avalon-review.json',1,'Offline validation accepted headings containing only x and a run TLDR of forty x characters.')],
'A retrospective page or unrelated immutable page can authorize a new altered experiment, while individual worlds still lack the required condition-specific account of question/treatment/comparator/metrics/limits. This is not evidence that the existing numeric pilot was modified.',
'Keep a compact plan schema with experiment/version, prospective/retrospective status, protocol hash, assignment IDs, required per-assignment TLDR fields, and endpoints/limits. Validate those exact assignments before launch and attach their receipt to every terminal record. Rendered public-page verification should be a recorded publication step, not inferred from raw Markdown fetch.')
add('REG-02','P1','Laya provider failures bypass the documented three-error stop rule','regrowth-200',[
('regrowth-200/src/run.py',35,'Qwen success resets the single error counter; Laya exceptions at line42 increment invalid but never the failure streak.'),
('review-2026-10-04/regrowth-runner-faults.json',1,'Dummy-policy unit injection produced20 consecutive Laya ConnectionErrors without provider_failure_streak; execution stopped only at a synthetic wall deadline.')],
'A broken hybrid head can be silently converted into persistent WAIT actions while the experiment appears to exercise the intended model. Provider malfunction is mixed with policy behavior.',
'Track provider-specific failure streaks and terminal causes, including qualification. Separate invalid model choices, provider errors and defaults; halt according to the frozen rule. Cache successful decisions or explicitly label cached failure defaults. Add the isolated failure-injection regression test; no live model test is necessary.')
add('REG-03','P1','Claimed hard resource bounds are not enforced per dispatch','regrowth-200',[
('regrowth-200/src/run.py',19,'Wall and Laya budgets are checked only at round boundaries; a round can dispatch199 Qwen calls, whose90-second request timeout is independent of remaining pilot time.'),
('regrowth-200/src/run.py',41,'Every sentinel is allowed to call Laya without a remaining-cap reservation.'),
('regrowth-200/src/models.py',12,'Qwen timeout is fixed90s; ThreadPoolExecutor waits for submitted work when leaving its context.'),
('review-2026-10-04/regrowth-runner-faults.json',1,'Starting the dummy Laya counter at3999 executes20 calls and fails at4019, overshooting the4000 cap by19.')],
'A future run can exceed the promised call/wall limits. The Qwen expression calls+len(jobs) also counts already-started jobs twice and may stop early; failures during dispatch leave already-submitted calls without event receipts.',
'Reserve each call in a single synchronized ledger before dispatch, pass remaining deadline to each request, stop/cancel pending work on exhaustion, and write an attempted-call receipt even when the round aborts. A few functions and unit fault tests suffice; no scheduler service is needed.')
add('REG-04','P1','Publisher reuses historical pilot-v4 run IDs for any output directory','regrowth-200',[
('regrowth-200/src/publish_hub.py',4,'The command accepts an arbitrary output directory.'),
('regrowth-200/src/publish_hub.py',21,'Every uploaded world is named regrowth-200/pilot-v4-<world.id>.'),
('regrowth-200/src/publish_hub.py',23,'Existing IDs are reopened and artifacts/progress are written even when the existing run is already done.')],
'Publishing a later experiment through this helper can replace artifacts/progress attached to the original six pilot records, contradicting historical preservation and making provenance ambiguous.',
'Derive immutable run IDs from a manifest run ID, require a matching manifest digest when resuming, and refuse writes to a completed record with different source/input hashes. Build and validate a sanitized publication payload locally before upload. Do not run the existing publisher on new results.')
add('REG-05','P2','Advertised certificate validity and actual next-hop reachability are different outcomes','regrowth-200',[
('regrowth-200/src/world.py',39,'score() checks each stored full path from earlier neighbor states against current topology; it does not follow current next-hop pointers.'),
('regrowth-200/site/index.html',20,'The selected route overlay follows current f.next pointers, while the displayed validity and hop count describe the stored advertised certificate.'),
('review-2026-10-04/regrowth-avalon-verification.json',1,'Reanalysis found31 disagreement frames:15 algorithm-damage,8 qwen-damage,8 hybrid-damage. At round40, Qwen/hybrid certificate validity=.855 but current next-hop reachability=.97. At algorithm round52 the values are.79 and.975.')],
'The recorded primary metric is correctly implemented for the protocol, but it cannot by itself establish packet delivery or evacuating200 agents. The visualization may draw a route different from the certificate being scored, obscuring transient loops and recovery semantics.',
'Name the endpoint certificate validity throughout. Add a separately defined next-hop delivery metric (static forwarding or time-varying packet execution, explicitly chosen) and display the actual scored certificate on selection. Preserve original metrics; publish any reanalysis as retrospective.')
add('REG-06','P2','Development record misreports Laya qualification for pilot-v2','regrowth-200',[
('regrowth-200/DEVELOPMENT.md',9,'Table says both models scored5/10.'),
('regrowth-200/PROTOCOL.md',39,'V3 amendment says the preceding v2 attempt failed at5/10 Qwen and5/10 Laya.'),
('regrowth-200/results/pilot-v2/manifest.json',1,'Stored qualification is Qwen5/10 and Laya6/10; independently rescoring all10 fixture records confirms6 under both strict and any-shortest scoring.')],
'The narrative is inconsistent with preserved raw evidence and the correction changes the apparent effect of prompt revisions, though it does not change gate failure or any swarm outcome.',
'Correct both documents to Qwen5/10, Laya6/10; retain the original result JSON and add an explicit editorial correction note. Generate qualification tables from archived fixture records.')
add('REG-07','P2','Agent identity, context and reproducible model spin-up need an explicit executable contract','regrowth-200',[
('regrowth-200/src/models.py',9,'Qwen receives only a stateless route-length instruction; controller observation cell ID is omitted. There is no conversational history or per-identity model session.'),
('regrowth-200/src/models.py',24,'Laya likewise receives route sentences and the Qwen proposal, without identity or history; its revision is pinned.'),
('regrowth-200/src/run.py',11,'Identity-specific state is path plus memo; it resets per world. The map is hard-coded, not generated from manifest seed4100.'),
('regrowth-200/src/run.py',74,'Qwen metadata records a digest for the mutable qwen3:0.6b alias but does not enforce an expected digest or record Ollama/backend/hardware version.'),
('regrowth-200/README.md',17,'Runbook requires an existing Laya source/venv/cache via placeholder paths; there is no dependency lock or self-contained resolution step.')],
'The implementation does provide200 independent controller states, but readers cannot infer200 persistent model contexts, and another machine cannot reliably recreate the inference environment from the commands alone. A fixed seed does not make all serving backends bitwise deterministic.',
'Add one small versioned agent spec naming role, model artifact/digest, provider/runtime, initial prompt/schema bytes and hashes, observation allowlist, state ownership, reset/caching policy, context cap, legal actions, and hybrid assignment. Validate resolved model/dependency metadata before qualification. State199 decision agents plus one fixed exit, shared weights and stateless invocations; test initialization/input hashes separately from stochastic output reproducibility.')
add('REG-08','P2','Earlier development source hashes cannot be resolved from the retained project or archive','regrowth-200',[
('regrowth-200/results/pilot-v1/manifest.json',1,'Protocol/models/runner hashes identify prior bytes but those bytes are absent from the checked project and evidence archive.'),
('regrowth-200/results/pilot-v2/manifest.json',1,'The same gap affects pilot-v2, pilot-v3 and pilot-v1-attempt2.'),
('review-2026-10-04/regrowth-avalon-verification.json',1,'The v4 source is recoverable exactly from evidence.tar.gz. Archive checksum, member list, and71 members verified; all earlier attempts miss three source snapshots locally.')],
'Failed development outcomes remain inspectable, but exact prior prompt/scorer reconstruction requires another version-control artifact. Hashes prove identity only when the corresponding bytes can be retrieved.',
'Locate any existing Git objects matching these hashes before declaring evidence lost. For future runs save a small source bundle or immutable commit link before execution; keep qualification prompts/scorer version and exact inputs with each attempt. Do not rewrite earlier manifests to current hashes.')
add('REG-09','P2','Report regeneration silently erases hand-maintained publication context','regrowth-200',[
('regrowth-200/src/analyze.py',12,'The generator replaces the entire RESULTS.md.'),
('regrowth-200/RESULTS.md',35,'The publication-boundary section explaining what was uploaded is present in the current report but absent from the generator template.'),
('regrowth-200/src/analyze.py',11,'Date-specific test, diagnostic and deployment claims are hard-coded and reused for any input run.')],
'Regenerating the report removes relevant provenance and can carry stale facts into future results.',
'Render only a delimited generated table/metrics block or move immutable narrative into a separate linked note. Generate execution facts from the selected manifest and validation receipts; preserve publication/process-compliance status explicitly.')
add('REG-10','P2','The pilot cannot identify a diversity benefit and its stronger result should be surfaced','regrowth-200',[
('regrowth-200/results/pilot-v4/summary.json',1,'Qwen and hybrid have identical final validity, shortest fraction, excess hops and recovery; hybrid adds476 world Laya calls across two worlds.'),
('review-2026-10-04/regrowth-avalon-verification.json',1,'Only two distinct Laya overrides occur, repeated in control/damage. One chooses a tied nonminimum route; the other chooses33 hops instead of25 while23 is available. Neither corrects to minimum. Validity and optimal-fraction trajectories are identical; excess hops differ transiently by at most.23.'),
('regrowth-200/PROTOCOL.md',15,'Attachment cells are fixed, Laya sees Qwen, and additional compute is unmatched; the single map is developmental.')],
'The record supports a useful negative engineering finding: this hybrid mechanism did not improve measured endpoints, while the exact local algorithm dominates route quality. It does not establish that heterogeneity helps or never helps.',
'Write this negative finding plainly. Before any new model spending, define a mechanism-specific prediction and choose a task where the model contributes more than numeric argmin. For a routing continuation, use held-out maps/damage locations, randomized attachment assignments, blind Laya and second-Qwen controls, matched damage exposure, recovery-area/route-stretch endpoints, and paired world replicates.')
add('AV-02','P1','Interrupted or invalid-action runs have no terminal assignment ledger and freeze provenance too late','avalon-swarm',[
('avalon-swarm/benchmark.py',523,'Assignments are saved before execution, but source.sha256 is written only after every world finishes.'),
('avalon-swarm/benchmark.py',525,'measure() exceptions propagate out of the sweep with no failed/not_run outcome for the remaining assignments.'),
('avalon-swarm/PROTOCOL.md',79,'The limitations acknowledge incomplete plans on invalid actions; this is an implemented gap rather than an undisclosed historical failure.')],
'A partial future study can lack both source identity and terminal failure counts, inviting survivor-only reporting and making exact reconstruction harder. Current45 archived outcomes are complete and source hashes match.',
'Freeze code/config/agent-spec and environment metadata before world initialization. Wrap each assigned world in a small terminal-outcome recorder for completed, failed, timeout, canceled and not_run; record reason and preserve partial event-chain tail. Keep execution failure separate from consensus benchmark failure.')
add('AV-03','P2','Discussion randomness changes later decisions even when beliefs are unchanged','avalon-swarm',[
('avalon-swarm/benchmark.py',158,'One mutable RNG is shared by every policy phase.'),
('avalon-swarm/benchmark.py',200,'Discussion shuffles a treatment-dependent memory candidate list.'),
('avalon-swarm/benchmark.py',210,'Proposals shuffle with the same RNG; random votes and assassination also consume it.'),
('review-2026-10-04/regrowth-avalon-review.json',1,'Isolated policy test: deleting one audited contradiction leaves all beliefs equal, but after discuss() the RNG states and next tied proposals differ.')],
'Audit/repair and topology comparisons include changes to tie-breaking random streams caused by memory length. This is a legitimate total intervention effect, but a tiny mission-success change cannot be attributed specifically to improved belief correction without separating this mechanism; pairing is weaker than scenario_hash equality suggests.',
'Key independent random streams by world, identity, phase, mission and attempt; use deterministic/keyed random priorities for candidate items. Keep this change versioned. Add a unit test that irrelevant memory changes do not perturb proposal tie-breaking randomness when the legal options and scores are identical.')
add('AV-04','P2','Topology comparisons change access to task-relevant evidence, degree and RNG behavior together','avalon-swarm',[
('avalon-swarm/benchmark.py',282,'Every private signal targets the same seat in the next council; none targets the owner\'s own council.'),
('avalon-swarm/benchmark.py',180,'Belief computation ignores every nonlocal target.'),
('avalon-swarm/benchmark.py',329,'Local topology never moves evidence across councils; federated adds two useful cross-council links and increases degree9→11.'),
('avalon-swarm/PROTOCOL.md',25,'Each target has only one initial evidence source; adversaries reverse their80%-correct signal.')],
'Federated versus local estimates the combined effect of making useful evidence available, increasing communication and changing random-policy trajectories. Local versus none cannot deliver useful initial role evidence under these rules. At random source-role mixture, sent signal correctness is only.6×.8+.4×.2=.56; relays create repetition, not independent corroboration.',
'Present the existing results as a channel-access/mechanics check. For an information-topology claim, hold relevant evidence and delivered budget fixed, compare degree-matched overlays, vary independent source count/reliability and explicitly measure reach, delay, retained evidence and mission utility. Avoid interpreting more claims as more independent evidence.')
add('AV-05','P2','Consensus gate has a floor effect and measures acquisition failure as well as collapse','avalon-swarm',[
('avalon-swarm/results/consensus-v02/outcomes.jsonl',1,'All15 conditions fail signal_loss at round5; none passes.'),
('avalon-swarm/benchmark.py',176,'Uninformed prior=.4 and one positive.8 signal averages to.6, below confidence=.7 before mission/audit evidence. Provenance does not accumulate repeated signals.'),
('avalon-swarm/benchmark.py',90,'Self-exclusion leaves4 observers for ordinary-good targets; ceil(.8×4)=4 requires unanimity, versus4/5 for other targets.'),
('avalon-swarm/PROTOCOL.md',85,'The failure clock starts at the first discussion round; it does not require previously achieved truth consensus.')],
'These outcomes validate the mechanics of a chosen threshold, not a general law that swarms collapse. The same label conflates never acquiring knowledge, losing established knowledge and delayed recovery. Class thresholds and finite observer counts create additional asymmetric difficulty.',
'Calibrate on development cases with attainable oracle, unaided, single-agent, Bayesian/exact local and confidently wrong controls. Report continuous truth/agreement coverage and distinguish acquisition latency from loss after a predeclared stable baseline. Freeze thresholds on development seeds; retain the original15 failures unchanged. A post-audit window is a separate registered endpoint, not an after-the-fact rescue.')
add('AV-06','P2','Current recovery evidence is driven by one additional successful mission','avalon-swarm',[
('avalon-swarm/RESULTS.md',27,'Mean later-mission success is37.3% audit versus38.0% repair.'),
('review-2026-10-04/regrowth-avalon-verification.json',1,'Paired repair−audit mission differences across seeds0–4 are0,0,1/30,0,0; the pooled gain is one additional success in150 opportunities. Council win differences averagezero.'),
('avalon-swarm/report.py',48,'Report emits treatment means without paired world estimates or uncertainty; eligible-origin denominators remain unavailable.')],
'The cautious published prose is appropriate. The table alone can visually overstate a reproducible performance gain, and thousands of claim deliveries must not substitute for five independent worlds.',
'Add the five paired differences beside means and identify one extra mission explicitly. For a confirmatory continuation choose a minimum useful world-level improvement, pilot variance, held-out seed count and paired interval/analysis before launch. Report normalized exposure rate and eligible-source denominators, alongside raw counts. Do not claim significance from five-seed bootstrap behavior.')
add('AV-07','P2','Deterministic scripted initialization is strong but not yet a reusable real-agent lifecycle','avalon-swarm',[
('avalon-swarm/benchmark.py',28,'Roles, signals and policies are keyed by SCENARIO_VERSION, seed and identity; source snapshot preserves prior scenario streams.'),
('avalon-swarm/benchmark.py',291,'Observation explicitly constrains role knowledge, council membership, inbox, audited labels and mission history.'),
('avalon-swarm/benchmark.py',161,'Memory is a32-claim deque whose eviction order follows global sender ordering; context contains no individual vote history.'),
('avalon-swarm/ADAPTER.md',7,'Real structured provider adapter, context handling, isolation and cost reservation are described but not implemented.')],
'Identical scripted agents can be recreated today, and all13 tests pass. Replacing policies with LLMs without a frozen spec would introduce uncontrolled context exposure, memory selection, call scheduling and within-run adaptation. The trusted Python object boundary cannot enforce model/tool isolation.',
'Keep the current baseline lightweight. Before model execution add declarative initial agent specs and identity/role assignments; version an observation serializer, context budget/truncation and eviction policy, permitted tools, update/repair rules, allowed phase transitions and event-keyed randomness. Snapshot initial hashes, then log state/context deltas and policy-version changes. Make heterogeneity a preassigned treatment; learned changes must be named interventions. Verify identical initialization without requiring identical stochastic outputs.')
add('REG-11','P3','Replay emphasizes100% validity while the decisive6.5% shortest-path result is visually secondary','regrowth-200',[
('regrowth-200/site/index.html',5,'Headline panels say200×Qwen and show rounded valid percentages.'),
('regrowth-200/site/index.html',7,'Main table/chart omit final shortest fraction and excess hops; baseline has no grid panel.'),
('regrowth-200/src/check_replay.cjs',3,'A desktop/mobile smoke script exists but depends on a developer-specific absolute Playwright path and changes the screenshot while checking.')],
'The visual craft is already coherent, but a quick reader can infer model success and fail to notice that the exact algorithm produces optimal routes while model routes are poor. The headline multiplication can imply200 separately loaded models.',
'Use200 states /199 decision cells and shared-weight model labels. Put final validity, shortest fraction, route stretch, cost and registration/exploratory status together; give overlapping curves distinguishable markers/dashes, provide text summaries and keyboard cell selection, and show baseline on equal footing. Keep the existing restrained palette/layout; avoid a full UI rebuild. Make visual QA use resolved dependencies and write review screenshots to temporary output.')
# Explicit full inventory; machine logs receive batch audit rather than a false line-by-line claim.
coverage=[]
for x in V['file_inventory']:
 p=x['path'];s=pathlib.Path(p).suffix
 if s in ('.md','.py','.cjs','.html') or pathlib.Path(p).name=='.gitignore':mode='full substantive source/document review'
 elif p.endswith('agent-definition.json'):mode='full declarative agent specification review'
 elif p.endswith('site/data.js'):mode='entire embedded JSON parsed; exact equality checked against six world records and manifest'
 elif s=='.jsonl':mode='every event/outcome parsed; Regrowth decisions reconstructed; Avalon hash chains and terminal payloads verified; no raw log dumping'
 elif s=='.json':mode='every field parsed; assignments/qualifications/summary/manifests/receipt consistency checked'
 elif s=='.log':mode='all lines structurally checked, JSON status/progress parsed; raw diagnostics not disclosed'
 elif s=='.png':mode='visual inspection of full image and asset metadata'
 elif s=='.svg':mode='valid XML parsed; corresponding PNG visually inspected'
 elif s=='.gz':mode='archive checksum, every member and path index verified; all text source differences reviewed'
 elif s=='.sha256':mode='digest compared to corresponding current/archived source'
 else:mode='structural review'
 coverage.append({**x,'review_mode':mode})
O={
 'scope':'Principal-investigator audit of regrowth-200 and avalon-swarm; immutable audit snapshot,2026-10-04. Original files were not edited by this subreview.',
 'severity_scale':{'P1':'fix before next execution/publication','P2':'material validity, reproducibility or interpretation improvement','P3':'presentation/maintenance refinement'},
 'findings':F,
 'coverage':coverage,
 'coverage_summary':{'files':len(coverage),'regrowth_completed_worlds':6,'regrowth_failed_development_attempts':4,'regrowth_frames_reconstructed':486,'regrowth_model_events_reconstructed':9436,'avalon_worlds_validated':45,'avalon_event_chains':15,'avalon_events_verified':15393,'archive_members':len(V['regrowth']['archive']['members']),'exclusions':'Python __pycache__/*.pyc are generated derivatives; no credential files or arbitrary raw logs were printed; third-party source repositories were consulted only for cited scientific claims.'},
 'verified_statistics_and_tests':{
   'python':'3.14.5',
   'tests':[{'command':'python3 -m unittest discover -s regrowth-200/tests -v','result':'7/7 pass'},{'command':'cd avalon-swarm && python3 -m unittest discover -s tests -v','result':'13/13 pass'},{'command':'python3 review-2026-10-04/audit-regrowth-avalon.py','result':'all artifact assertions pass; no new worlds or inference'},{'command':'python3 review-2026-10-04/test-regrowth-runner-faults.py','result':'dummy-policy reproductions confirm Laya cap overshoot and missing provider-error halt; temporary outputs only'}],
   'regrowth_usage_recomputed':V['regrowth']['accounting'],
   'regrowth_data_replay_exact_match':True,
   'regrowth_archive_digest_and_index_match':True,
   'avalon_recovery_pair_differences':next(x for x in V['avalon']['validation'] if x['name']=='recovery-pilot')['paired_repair_minus_audit'],
   'avalon_consensus':'0/15 passes; every signal_loss failure first recorded at round5',
   'source_snapshot':'v4 Regrowth bytes available in evidence archive; v1/v1-attempt2/v2/v3 protocol/models/runner historical hashes unresolved within audited project and archive; Avalonv0.1 andv0.2 source hashes match45 outcomes.'},
 'positive_design_features':[
  'Honest scope: scripted Avalon is labeled scripted; Regrowth is labeled exploratory, one-map, shared weights,199 active decision cells, no NCA training; no claim that agent count equals sample size.',
  'Serious comparators: exact local path-vector algorithm and undamaged controls; Avalon separates none/audit/repair and treats complete worlds as experimental units.',
  'Failed attempts and tie-scoring amendment preserved; late public registration explicitly labeled retrospective with process failure separate from computational outcomes.',
  'Reconstructable v4 model decisions, per-identity memoization, explicit synchronous update order, reported token/call totals and model digest/revision; all486 frames and aggregate usage reproduced exactly.',
  'Avalon has deterministic role/signal streams, bounded sparse routing, role-authorized observation structure, exact scripted replay, immutable prior source snapshot and verified hash chains.',
  'Consensus failure is sticky, late recovery stays observable, class-specific truth and agreement remain distinct, and benchmark failure is not confused with crashed execution.',
  'Citations to AvalonBench\'s fifth-team convention, Strategist, Avalon-ToM, Growing NCA and model cards resolve to primary sources and are framed without false reproduction claims.',
  'Regrowth visual design is coherent and unusually clear for a pilot; outcome plot shows the model/algorithm route-quality gap directly.'],
 'prioritized_experiment_redesign':[
  {'priority':1,'action':'Freeze one falsifiable mechanism before any new run','detail':'Regrowth: does a specified blind decision head reduce downstream route stretch at matched compute and exposure? Avalon: does contradiction removal improve subsequent mission success beyond identical audited truth? Do not use general claims about swarm intelligence as endpoints.'},
  {'priority':2,'action':'Choose an agent contract and immutable initial state','detail':'Specify model/script hash, initial messages, role/skill assignment, observation access, state and context owners, memory cap/eviction, update policy, tool permissions, inference settings and expected initialization hash. Treat evolution of context as logged state progression; treat model/prompt changes as versioned interventions.'},
  {'priority':3,'action':'Repair launch/reporting correctness before paying for inference','detail':'Bind public plan and per-condition TLDRs to assignments; source snapshot before execution; terminal ledger for every assigned world; per-dispatch budgets; provider failure policy; non-overwriting publication IDs.'},
  {'priority':4,'action':'Use small calibrated scripted controls to establish identifiability','detail':'Regrowth: oracle greedy, persistent/random legal and matched error-rate controls to determine whether collective repair comes from the controller. Avalon: oracle and exact local inference controls, degree/budget-matched graphs, fixed relevant evidence and event-keyed random streams; calibrate consensus thresholds on development cases.'},
  {'priority':5,'action':'Register a compact paired held-out design','detail':'Separate development and held-out maps/seeds. Randomize head/role assignments with scenario blocks, distinguish fixed total compute from fixed per-agent compute, predeclare one primary endpoint and useful effect size, report whole-world paired differences with intervals and all failures. The existing pilots do not justify a universal seed count.'},
  {'priority':6,'action':'Report continuous mechanisms with task utility','detail':'Regrowth: certificate validity, defined packet forwarding success, route stretch, damage-at-t0 impact, area under post-damage loss, stability, costs. Avalon: local truth/ordinary agreement coverage, acquisition/loss/recovery separately, unaudited-target Brier, successful missions, useful evidence reach and contradiction exposures normalized by opportunity.'},
  {'priority':7,'action':'Make writing and aesthetics serve the strongest supported result','detail':'Lead the report with the actual negative or small effect, show baseline and cost together, label archival versus live/prospective status, use condition-specific captions, and generate numeric tables from evidence while preserving historical caveats.'}],
 'external_sources_checked':[
  {'url':'https://arxiv.org/html/2310.05036v2','checked':'AvalonBench authors, rules, fifth proposal executes after four rejections, role-deduction setting.'},
  {'url':'https://github.com/jonathanmli/Avalon-LLM','checked':'Official repository includes Strategist and identifies separate AvalonBench/Strategist work.'},
  {'url':'https://arxiv.org/abs/2608.09638','checked':'Avalon-ToM-Bench title and perspective/asymmetric-information diagnostic relevance.'},
  {'url':'https://distill.pub/2020/growing-ca/','checked':'Source exists; Regrowth correctly limits borrowing to presentation/local damage idea rather than claiming NCA training.'},
  {'url':'https://huggingface.co/Qwen/Qwen3-0.6B','checked':'Official model card exists; current local source uses the named small model with thinking disabled.'},
  {'url':'https://huggingface.co/convaiinnovations/laya','checked':'Named structured-prediction model card exists; pinned model revision recorded locally.'}],
 'limitations':['The saved Regrowth public-plan URL and raw immutable URL returned web cache-miss errors in this review; this is an inability to independently re-fetch here, not proof that the public page is unavailable. The local registration receipt was inspected.','Historical Regrowth source may exist in Git objects outside the project/archive comparison; no claim of irreversible loss is made.','No new scientific experiments, live inference, provider calls, public writes or historical artifact edits occurred. Existing unit tests and isolated dummy-policy failure injections were run.','All data files were structurally/semantically batch inspected, not manually read line by line. Full substantive documents and source were read; generated images were visually reviewed.']}
(R/'review-2026-10-04/regrowth-avalon-review.json').write_text(json.dumps(O,indent=2)+'\n')
print(json.dumps({'findings':len(F),'coverage_files':len(coverage),'path':'review-2026-10-04/regrowth-avalon-review.json','severity_counts':{s:sum(f['severity']==s for f in F) for s in ('P1','P2','P3')}},indent=2))
