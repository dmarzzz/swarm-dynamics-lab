# PI review of the Grove Swarm project

User-requested internal review of research design, evidence, implementation, writing and agent definition. The central recommendation is to isolate a useful mechanism and its competing explanations before increasing headcount or study size. This is a PI-style critique by the researcher's agents, not an independent laboratory replication or a formal cross-researcher gate approval.

## Read the review

- [Scientific review in Markdown](SCIENTIFIC-REVIEW.md): all ten named projects, 21 study/version reviews, 110 scenario/condition assessments and all sixteen original proposals.
- [Prioritized findings in Markdown](FINDINGS.md): 57 evidence, implementation and presentation findings, with status and remedies.
- [Interactive scientific review](review-2026-10-04/scientific-review.html): ten-project overview, full assessments, eight focus areas, filtering and deep links.
- [Original interactive audit](review-2026-10-04/index.html): agent lifecycle, evidence checks, findings and file-level coverage.
- [Agent lifecycle contract](../../../../tooling/agent-experiments/AGENT-LIFECYCLE.md) and [29-source research supplement](../../../../tooling/agent-experiments/AGENT-LIFECYCLE-RESEARCH.md): agent definitions versus instances, actual initialization, context, memory, access, reset/fork semantics and limits of deterministic replay.

GitHub renders the Markdown; HTML is source on GitHub. Clone/download this repository and open either HTML file in a browser. The reports are self-contained; optional source links use the network. No deployment is required.

## Coverage and evidence limits

The original audit covers 1,331 unique local project files / 1,342 file versions: 1,056 files at 2026-10-04 02:30:09 UTC, followed by 275 new and 11 updated files at 02:58:11 UTC. The scientific review supplements that audit with pinned linked-repository documents. The heterogeneous biological revision is frozen at 03:23:55 UTC; Phantom Coast's PC-1 plan delta at 03:40:18 UTC. These are cutoffs, not a claim that concurrent later code or experiments were reviewed.

Antsy and historical/revised influence figures were checked against author reports, not newly replayed. Other entries identify independent trace reconstruction explicitly. Scripted fixtures, qualified model observations and unrun proposals remain separate. Candidate banks are agendas, not additional executed experiments. Reading a proposal does not imply full reading of every paper it cites.

The package publishes review records and saved design sources, not every local experiment artifact. [Source availability](review-2026-10-04/source-map.html) and its [JSON ledger](review-2026-10-04/source-map.json) distinguish exact matches to reviewed hashes, related but changed repository references, and local-only evidence. Original workspace-relative paths in review JSON retain their original meaning; they are not repository-root paths. Missing evidence links never silently resolve to an unrelated same-named file.

## Changes included

The canonical methodology toolkit receives three new lifecycle/research files plus selective navigation, launch-gate and bibliography corrections. Existing integration guidance and library citations are preserved. Recommended lifecycle checks remain recommendations until implemented in a launcher.

[workspace-edits.patch](workspace-edits.patch) preserves the earlier local README, dossier label/generator fix and Regrowth documentation corrections against the frozen workspace. Their original generators/protocols are absent or diverged in the shared repository; the patch is a reviewable record, not a patch to apply blindly at repository root. Historical raw experiment results are unchanged. The local guide's old package manifest is not installed as the integrity manifest of the larger canonical toolkit.

The incidental live-workspace drift inventory is narrowed to its scope notice; unrelated concurrent clones are excluded. Private task links no longer act as public evidence links. The original read-only audit/render scripts are retained as research provenance; some require the original workspace/snapshot layout and are not standalone shared-repository commands. Their required inputs remain explicit. Use the supplied rendered reports for this published snapshot.

## Verification

See [publication checks](publication-checks.json) for link checks, source availability and secret-scan status, alongside the retained local [scientific presentation checks](review-2026-10-04/scientific-presentation-checks.json). The repository validator is run before push. No new model calls, experiments, public-plan registrations or site deployment are part of this publication.

[Publication manifest](PUBLICATION-MANIFEST.json) records original review-file hashes, the target and portability transformations. Scientific recommendations are not preregistrations or launch authorization.
