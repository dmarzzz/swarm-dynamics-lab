# Prospective offline repair: separate memory commitment from operational decisions

C2's first invalid commit returned the correct inherited witness pair plus an unsolicited `decision:"defer"` field. The strict instrument expected exactly one top-level `note` field. Preserve that failure and all raw responses. No extra field was stripped and no score is upgraded.

The observed cause of termination is the extra field. A plausible contributor is that the commit system message combined general allow/hold/defer rules with a memory-only output request. That causal explanation is unproven:three other observed commits complied under the same interface. The prompt gave the expected shape, but did not explicitly say that additional keys were forbidden; the parser did.

Implement an unused candidate commit prompt that states its sole task, exact allowed keys and explicit prohibition on actions/decisions. Remove operational-decision instructions from this memory-only phase. Preserve native witness choice and the strict parser:wrong pairs remain wrong, missing/malformed fields still fail, and no automatic correction is added. All six other phase bodies must remain byte-identical to selector-v2. This is an interface clarification, not evidence of a native reliability gain.

Offline checks must verify phase isolation, unchanged model/provider/output budgets and exact-key rejection of the saved invalid answer. Retain a golden conforming commit and a semantically wrong but syntactically valid note to distinguish schema from policy competence. These checks do not require paid calls.

No new native stage is allocated here. A later explicitly admitted bounded diagnostic could compare the scoped prompt on inspected commit contexts and uninformed/changed-note controls, recording every raw output and semantic choice. It must be labeled development qualification and cannot retrospectively pass C2 or establish full-turnover culture. Do not launch a review-led successor from historical reviews:the newly requested external Theseus review was not yet pushed, and that review pass has been redirected to another study.
