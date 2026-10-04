# Saved-data reporting supplement

`saved_diagnostics.py ROOT OUT` reads retained traces and summaries only. It never dispatches a model. It separates paid collection from counterfactual cascade selection, reports both Qwen passes, observed component time/tokens and served models, and draws all family error strata. Local Qwen has no dollar price assigned; zero recorded API charge is not zero compute cost. Observed summed call time is not a randomized production-latency benchmark.

Browser review of the original renderer found that tiles were grouped by family despite wording suggesting curator grouping/recorded chronological replay. `replay-reviewed.html` corrects those labels to family grouping and tile reveal; the original artifact remains retained, and all model outcomes are unchanged. The tile inspector was checked against a saved SUPPORT case with two wrong REFUTE answers and a correct Jev answer. The running scientific source is unchanged.

Qualification diagnostics:120 Qwen calls consumed141.3284 observed seconds;60 Jev calls15.2151 seconds. The counterfactual cascade would use both Qwen passes plus one Jev referral (141.5949 summed observed seconds). It detected0/23 Qwen-A errors. API-only savings therefore cannot support a speed or total-resource improvement claim.
