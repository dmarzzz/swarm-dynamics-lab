# S0-repair-1 post-mortem

2026-10-04, vishesh/codex-methods; same-author review. [Full results and limitations](../RESULTS.md).

Execution: pass,100 started and100 valid native OCR invocations across20 assigned receipts. All20 analyzed;19 scorable,1 unknown reference;220 policy outcomes. Immediate call journals and a separate reconstruction audit reconcile all outputs.24 offline tests pass. Elapsed501.0s; no hosted language-model calls, no new infrastructure. The missing native library from the initial attempt is repaired and the initial attempt preserved.

Qualification: **fail**. Best worker R0 is11/19 correct, but the best Tesseract variant is1/19, below the predeclared minimum of2 for each family. Completeness, execution validity, reference coverage and best-worker threshold pass. S1 was not started; no new repairs or threshold relaxation.

Scientific interpretation: two perception paths are different but severely mismatched in competence. Same-wrong agreement survives in T0/T2; R1 adds errors without any correct candidate absent from R0. Majority of weak workers discards a useful strong singleton, and a blanket dissent veto loses one correct decision in the secondary team. This diagnoses the design weakness; it does not establish a diversity benefit, effective independence or an LLM-swarm result.

Response/extraction quality: Tesseract recognizes fewer total anchors and its outputs rarely meet the shared conservative field contract. Read-only saved-output replay locates the coverage loss without new inference. A future design should develop and qualify perception/field extraction separately, then test targeted verification against the strong singleton at matched compute. Fresh data and prospective admission are required for that successor.

Reporting: all numeric results, charts and18-frame trace replay are preserved. The public GitHub plan was actually browser-verified before both native attempts; the dashboard's local DNS failure is recorded separately. Durable hub artifact readback and final source links are in SETUP. Release the dedicated claim after uploads and verify no experiment workers remain.
