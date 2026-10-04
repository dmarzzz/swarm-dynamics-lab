# Scope claims before collecting evidence

Owner design guidance, 2026-10-04: every experimental claim must name its scope. This applies across the owner's studies; it is a design requirement, not a disclaimer added after results.

Before implementation, specify the population/task family, environment, model and configuration, intervention, strongest relevant comparator, measured endpoint, independent sampling unit and resource envelope. Write one sentence stating what favorable evidence would establish, and another stating what remains untested. Connect each intended claim to the control and observation capable of distinguishing it from a simpler explanation.

Separate software correctness, agent competence, a causal mechanism, comparative practical benefit and generalization. Passing one level does not imply the next. A rule supplied in context tests execution; learning it tests acquisition; preserving it through complete replacement tests continuity; outperforming an equally informed controller tests collective benefit. More repeated calls do not create more independent worlds.

Choose the minimum useful claim, then design enough challenge, independent variation and precision to support it. If that claim would be trivial or not decision-relevant, improve the design before collection rather than adding expansive language. Disclose finite synthetic or inspected development cases; reserve untouched cases for actual transfer claims. Define support, null, adverse and inconclusive decisions prospectively. Report effect size and uncertainty at the independent-unit level, including missingness and failures.

A strong comparator implements a credible simpler alternative with matched information, tools, memory capacity, model and an explicit compute budget. Give it the same legitimate opportunities to update, check and act. Validate that it can perform the required task. State unmatched resources and distinguish an oracle ceiling from a fair efficacy comparator. An intentionally weak baseline cannot support a broad superiority claim.

After the run, test the original claim against the actual evidence. Narrowing an unsupported conclusion is necessary; repeated narrowing is feedback to improve the next design's controls, task coverage or decision value. Do not broaden claims from favorable scores, treat provider failures as incapacity, or keep collecting to obtain a preferred result. Use RUN-QUALITY.md and ITERATION.md for implementation and closeout.
