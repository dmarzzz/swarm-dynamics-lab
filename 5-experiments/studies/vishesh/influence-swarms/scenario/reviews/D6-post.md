# D6: the first direct API request returned HTTP429

Retrospective closeout, 2026-10-04. **HOLD further model collection.** [Native diagnostic](https://swarm-live.pages.dev/#/r/influence-swarms%2F1004-180640-faf466) · [immutable prospective plan](https://github.com/dmarzzz/swarm-lab/blob/c0f3d096aa6e98b93dd6b8f09f71c4f1becf415b/researchers/vishesh/notes/influence-swarms/scenario/ITERATION-06-PREP.md).

## Purpose and result

D6 checks whether the direct provider route and the two prepared reviewer formats can produce a usable response before committing to another behavioral cohort. It permits one matrix request, followed by one typed-fact request only if the first passes parsing, contract and usage checks. It is an acquisition diagnostic on one previously inspected case, not an experiment demonstrating an architecture advantage or a model's reasoning quality.

The first matrix request returned **HTTP429** before any model response. The new logger preserved that status and the circuit breaker stopped immediately. The typed request remained **unstarted**. There was one physical request, no retry and no automatic successor. No usable Retry-After value was supplied or retained; the request ID was recorded privately and in the native event artifact. No HTTP error body, authentication header or credential was logged.

This identifies a current direct-API rejection as the immediate obstruction. It does not establish billing exhaustion, which rate limit applied, a common cause for every earlier D5 failure, model incapacity or schema incompatibility. The typed format remains untested live. Other routes/providers succeeding would not establish recovery of this one.

## Accounting and controls

Two assigned contracts; one started/failed, one unstarted; zero usable answers. Exact first-request bytes/hash match the frozen prepared wire. No response artifact was fabricated for the HTTP failure, and no request/response artifacts exist for the unstarted second condition. Durable session state is stopped. The worker exited; no blocking model processes remained at closeout. The hub says failed and retains both condition-specific TLDRs and the immutable plan.

One conservative reservation of **USD0.048640** was added to the original ledger. Cumulative reservation is **USD4.917472 of8**, calls247, leaving **USD3.082528 unreserved**. Usage is missing for the one request, so actual cost is **unknown**, not zero. Earlier48 uncertain D5 charges/reservations remain untouched. No new machine was created; existing dedicated capacity was used and released.

The deployed source was `c0f3d096aa6e98b93dd6b8f09f71c4f1becf415b`.75 offline tests passed in the actual pinned runtime before launch, including two-contract success fixtures and first429retaining the unstarted second assignment. Approved-account/resource, exclusive idle allocation, original budget, public plan and source/wire checks passed. The credential traveled through verified encrypted stdin into memory only. These process controls do not turn a failed acquisition into native qualification.

## What changed from D5 and what remains

D5 repeatedly retried and retained only PolicyError. D6 retained the exact safe status and stopped after one physical request, limiting incremental reservation to less than five cents. Request artifacts and hashes survive independently of response validation. The full assigned cohort is visible without calling unstarted conditions failures or inventing outputs.

The diagnostic achieved its immediate operational purpose, but it did not establish that either reviewer contract can complete on the live route. Behavioral findings remain D3's previously measured false-blocker errors. No procurement outcome, architecture effect, fresh sample or generalization evidence was added.

Next action: the account/provider operator resolves or characterizes the direct-route rejection using authorized account-side evidence. This task will not poll the model endpoint, switch credentials/providers, retry the same packet, or launch a broader study automatically. Any later acquisition attempt needs a concrete bounded scope decision and refreshed admission with the original ledger. No second researcher review is needed.
