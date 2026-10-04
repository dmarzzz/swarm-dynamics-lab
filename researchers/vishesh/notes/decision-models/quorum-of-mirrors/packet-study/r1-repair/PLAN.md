# Offline repair after R1: check normalized facts against their evidence

Prospective implementation note, after reviewing R1 native traces and before writing this guard. No new model run, allocation or change to R1's frozen instrument/outcomes.

R1-032 quoted “was operating” but returned running=0 for source s1; its final majority decision remained correct. R1-034 returned status unknown with value0 for a plan-only source, contradicting the null-value contract. This is a returned semantic/contract error, not HTTP400. The exact supplied text and output establish both divergences; whether attention, copying or sampling caused them is unknown.

Implement a read-only guard for the existing authored grammar: independently parse each input receipt/report, validate shape/status consistency, compare every extracted field and require a literal quotation containing the selected full proposition. Return rejection reasons; never silently rewrite a model answer or mark a historical failure passed. The guard uses actor inputs only, never construction gold. It is a software guard for a controlled grammar, not a native semantic-model repair or a free-form validator.

Acceptance: replay all35 saved responses; flag the two observed bad responses, accept the other33, and exercise known-value inversion, unknown/non-null contradiction and correct controls. Preserve native scores, aborted assignments and uncertain charges. Separately repair offline replay's assumption that an unordered runtime delta list has stable order; compare multiset values and reconstruct root-keyed outcomes. Future summaries should sort roots explicitly.

Next design option: for grammar-covered inputs use the exact parser directly. For free-form inputs, test evidence-span selection with deterministic normalization and explicit abstention rather than letting a model emit redundant status/value fields unchecked. Broaden qualification across positive/negative/unknown cases in every mechanism. A native successor would need its own fresh frozen cohort and prospective plan; no automatic rerun is part of this offline repair.
