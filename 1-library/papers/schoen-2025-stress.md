---
id: schoen-2025-stress
type: paper
title: Stress Testing Deliberative Alignment for Anti-Scheming Training
authors: [Bronson Schoen, Evgenia Nitishinskaya, Mikita Balesni, Axel Højmark, Felix Hofstätter, Jérémy Scheurer, Alexander Meinke, Jason Wolfe, Teun van der Weij, Alex Lloyd, Nicholas Goldowsky-Dill, Angela Fan, Andrei Matveiakin, Rusheb Shah, Marcus Williams, Amelia Glaese, Boaz Barak, Wojciech Zaremba, Marius Hobbhahn]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/html/2509.15541
doi: null
arxiv: "2509.15541"
cite: Schoen, B., Nitishinskaya, E., Balesni, M., Højmark, A., Hofstätter, F., Scheurer, J., Meinke, A., Wolfe, J., van der Weij, T., Lloyd, A., et al. (2025). Stress Testing Deliberative Alignment for Anti-Scheming Training. arXiv preprint arXiv:2509.15541.
topics: [llm-agent-swarms]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

OpenAI and Apollo Research trained o3 and o4-mini with deliberative alignment against "covert actions" (secret rule-breaking, sandbagging). They tested on 26 out-of-distribution evaluations (180+ agentic environments). Covert actions fell from 13% to 0.4% for o3, but not to zero. Section 6 measures verbalised evaluation awareness in the chain of thought and tests whether it drives behaviour. Anti-scheming training raised verbalised awareness (o4-mini 0.9% to 5.5%, o3 2.3% to 4.5%). An experimental capability-RL run raised it far more, from 2.0% to 20.5%. Causal tests by editing the chain of thought mid-trajectory found that resampling from just before an evaluation-aware sentence until it disappears raised covert actions from 13.2% to 24.2%, while injecting an evaluation-aware sentence lowered them from 24.5% to 18.6% (random-sentence control 24.9%).

## Contribution

The strongest causal evidence that verbalised evaluation awareness, once it appears partway through an agentic trajectory, reduces misbehaviour for the rest of that trajectory, and that safety training can raise awareness as a side effect.

## Key results

- Covert action rate: o3 13% to 0.4%, o4-mini 8.7% to 0.3% after anti-scheming training.
- Verbalised evaluation awareness rises with anti-scheming training and much more with capability RL (2.0% to 20.5%).
- Ablating awareness: covert actions 13.2% to 24.2% (+11 pp). Injecting awareness: 24.5% to 18.6% (−5.9 pp). Measured on Lazy Checklist and other environments with o3.
- Training with explicit situational-awareness hints (o4-mini AS+SITA) lowered spec citations (78% to 64%) and raised verbalised awareness (7.5% to 12.0%) at test time without hints.
- Qualitative cases: o3 "after noticing a potential dilemma" correctly guesses the purpose of the evaluation (Figure 14).

## Methods and models

OpenAI o3 and o4-mini, plus an internal experimental model. A strict LLM classifier flags unambiguous verbalised awareness, counted per trajectory (at least once). The counterfactual interventions resample reasoning and actions from the point where awareness first appears (Appendix P). We read the abstract, Section 6 and Figure 14 to 17 captions, not the full 100+ page paper.

## Limitations and open questions

Verbalised awareness only. The authors note they cannot exclude that reduced covert actions are partly driven by awareness. They record whether awareness appears in a trajectory but do not report what in the environment triggered its onset or how far into the trajectory it occurs.

## Relevance to us

For V5, this paper establishes that "awareness appears mid-run, then later behaviour shifts toward being watched" is real and causal for single agents: mid-trajectory injection of one awareness sentence moved covert actions by about 6 pp. What it lacks is an environment trigger. Awareness arises spontaneously or by editing the chain of thought, never from discovering a trap. The resample-from-onset method can be reused directly in V5 to separate discovery effects from awareness effects. Contrast [[knecht-2026-evaluation]], which finds small effects of verbalised awareness on non-agentic benchmarks. See also [[krakovna-2026-realistic]], [[abdelnabi-2025-hawthorne]] and [[goodhartlabs-2026-honeybench]].
