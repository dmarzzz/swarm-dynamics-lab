# Research questions about the right to reopen

The strongest next question is **how a group should preserve its ability to reconsider when evidence arrives over time and checking is scarce**. A dissenter should be able to earn scrutiny, withdraw when disproved, and return with new information. An unresolved objection should not consume every future opportunity merely by recurring. These are proposed properties to test, not guarantees already demonstrated.

## The primary question

**Can memory of unresolved evidence and protected verification capacity improve timely correct decisions under a fixed budget, without making the group slow to respond to an urgent early change?**

The compelling tension is between spending the next check and keeping the option to check later. A group can fail by overreacting to repeated ambiguity, by ignoring a recovered situation, or by waiting for a future event that never arrives. Aggregate accuracy alone hides these different behaviors. The proposed experiment therefore contains a useful second early check as well as cases where waiting helps.

The first comparison is small and operational: bounded always-check versus remembering attempted resolutions versus adding a fixed reserve. If remembering unresolved evidence suffices, the reserve is unnecessary. If reserve helps only at one known change time, it is a scheduling artifact rather than a robust collective principle. If clearer actor-visible evidence fixes the problem without a new allocation policy, prioritize the simpler interface improvement.

## Three scenarios worth showing

**The alarm that consumes the response budget.** The group receives an incomplete inspection, then many aliases of the same observation. A later genuine change finally provides a useful measurement. Show the shrinking check budget next to the unchanged evidence. Test whether one unresolved observation can repeatedly purchase attention. The opposite-direction version must test deterioration as well as recovery.

**The inspection stream with little information.** Reports are genuinely new, but early inspections cannot settle the relevant requirement. Deduplicating messages is insufficient. A later decisive observation competes with the temptation to exhaust the budget now. This exposes whether a protected check adds anything beyond sensible caching.

**The decisive rerun before the deadline.** The second early check can resolve the task, while late evidence adds nothing. A rigid reserve withholds useful effort and misses an otherwise achievable deadline. This is the crucial falsifier: a design that only contains late changes gives the treatment its preferred world.

These are mechanisms with practical stories, not three independent populations. A later study must cross mechanisms with domains and vary change timing; the six-stream pilot cannot establish that breadth.

## The Jev specific angle

Jev makes small, typed action choices and returns choice scores. The interesting decomposition is whether it should decide the action, the need for an observation, or both. RD4 showed that the extra admission decision can block a useful check while adding inference cost. The successor puts mechanical eligibility in an inspectable contract and tests Jev's interpretation separately.

This allows a sharper future research question: **when does a learned judge earn its own cost by choosing between genuinely competing, eligible checks?** A future queue experiment would compare Jev ranking with FIFO, recency, simple deadline/severity rules and budget-matched random selection, counting the judge's calls and delaying no hidden free baseline. It is a later study, not an extra arm squeezed into the remaining budget.

Do not call a correct answer on the retained old action a recovered semantic judgment. Track action correctness, evidence justification and abstention separately. Provider choice scores can be recorded, but using them as calibrated expected value requires separate evidence.

## Biological motivation and existing work

The existing [[seeley-2012-stop]] record motivates inhibition in collective choice. A newly read abstract, [[tan-2016-honey]], reports that inhibitory signaling in Asian honey bees varies with threat and attack context. Our proposed implication is to test selective interruption; it is not evidence that bees use our reserve or identity policy. [Primary article](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1002423).

The resource-allocation connection is already established prior art. [[hay-2012-selecting]] formalizes selecting computations and discusses saving unused sampling budget for later search states. Our scope differs: externally arriving observations, repeated unresolved decisions, deadlines and acquired-evidence provenance. Saving computation for later is therefore not our novelty claim. [Author-hosted paper, especially section 6.2](https://people.eecs.berkeley.edu/~russell/papers/uai12-meta.pdf).

The existing [[geifman-2017-selective]] entry motivates keeping rejection and coverage visible; its guarantees are not transferred to Jev. The [original source and Twitter map](../SOURCES.md) remains the canonical map for Minority Sentinel, withheld dissent and Jev's map demonstrations. No new verified Twitter evidence was found or claimed in this planning pass. The focused reading is not a comprehensive prior-art survey.

## What would make the result interesting

| Candidate conclusion | Evidence needed | What would undermine it |
| --- | --- | --- |
| Remembering unresolved evidence prevents repeated waste | B1 improves over B0 at equal maximum checks and common interpretation; repeated identical information consumes no new quota | Benefit exists only because B0 was artificially denied reusable receipts or because independent new checks are mislabeled duplicates |
| A reserve preserves useful flexibility | B2 improves over B1 across varied late-change times while urgent-early costs remain visible | Benefit disappears outside the fixed reserve boundary or comes only from an extra budget |
| Context makes a stop signal useful | Same interruption policy responds appropriately across verified scope, severity and freshness contrasts | Severity is an evaluator-provided answer or an untrusted self-declared urgency flag |
| A learned allocator earns its cost | A separate queue study beats strong simple policies after counting allocation calls, latency and acquisition cost | It merely recreates a deterministic validity rule or has privileged information |

The practical deliverable could be a reusable decision record: what is resolved, what is still unknown, what observations were already acquired, what would permit reopening, and how much verification capacity remains. That record could support incident response, release reviews and monitoring, but those applications require their own data and validation.

## Priority after the bounded pilot

First, isolate clear interpretation from allocation and retain negative results. Second, cross scenario mechanism with domain, urgency, event timing and no-change controls on independently authored tasks. Third, test a queue of competing dissenters, where there is a real reason for learned prioritization. Only then investigate endogenous minority formation or source-reputation learning. These extensions are research ideas, not runs scheduled under the current cap.

## The next question after RD5: spend or wait under uncertain arrivals?

RD5 fixes the reserve release at tick 4 and deliberately chooses informative arrivals before or at that boundary. Its useful outcome is a mechanistic tradeoff, not proof of a robust scheduling rule. The next research question is: **Can a group allocate its final verification opportunity from observable urgency and evidence quality when it does not know whether better evidence will arrive?**

A stronger follow-up would independently vary arrival time (early, late, never), true urgency (reversible delay versus missed deadline), inspection reliability (incomplete, conflicting, accurate), and source novelty (alias, genuinely new but correlated, independent). Cross these mechanisms with process, build and bridge tasks using independently authored cases. Keep evaluator urgency out of the actor; give actors a declared deadline and consequence schedule that is valid task information, and separately test false urgency claims.

Compare B1 attempt memory, the fixed RD5 reserve, a transparent deadline rule, and a Jev allocator choosing among multiple eligible objections. Match total physical checks, account for the allocator's extra inference cost and latency, and include a strong rule that spends when the next check is the last opportunity before an irreversible deadline. An oracle with future arrival knowledge may be a labelled ceiling, never an actor input or deployable baseline.

The primary decision would be whether learned prioritization improves correct actions before deadlines over the strongest affordable simple rule. Report harmful action, needless delay, unused capacity and inspection/model costs as a frontier before choosing explicit utility weights. A learned allocator that merely learns the fixed tick-4 schedule has failed the question. A simple rule matching it is a practical success for the simpler system.

This broader design is unfunded and unrun. RD5's remaining 12-call margin is not a budget for it. Use the pilot's failure strata to select the scope and independent unit; do not claim that six authored streams supply a power estimate or calibrate Jev's choice scores as probabilities of truth.
