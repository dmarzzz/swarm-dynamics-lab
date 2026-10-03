# Influencing Agent Swarm Decisions Through Inferred Preferences

Research brief prepared for Grove Swarm Hackathon  
Date: October 3, 2026  
Status: hunch / proposed research direction (pre-survey; not a hypothesis under the lab's prior-art gate). Focused literature review.

There is published research closely related to using knowledge of one agent to influence a multi-agent collective. The strongest direct match is M-Spoiler, which studies collective manipulation when only one constituent agent is known. Other work examines reward inference, persuasive agents, information design, and manipulation of the options an agent selects. Together, these provide a foundation for studying whether preferences inferred from one agent can predict and influence a swarm’s decisions.

The specific combination remains a research question: can a behavioral model learned from one agent support ordinary-looking choice manipulations that transfer to an unseen group? This brief does not claim that combination is novel or that it reliably works. No experiments were run for this review.

## The concept

The proposed mechanism has three components:

1. Observe an agent’s choices to estimate the criteria and tradeoffs that predict its behavior.
2. Test whether those estimates generalize to other agents or to the collective decision process.
3. Examine whether changing the presentation, evidence, or available alternatives shifts the collective toward a designated option.

Neurolinguistic programming is an analogy used as an informal analogy. The technical foundations used here are behavioral preference inference, adversarial persuasion, information design, and choice architecture. The analogy is not evidence of a shared psychological mechanism.

A proposed descriptive label is **preference-informed adversarial choice design for multi-agent systems**. This is a working label, not an established field name.

## Closest direct precedent

**Liu et al., Can an Individual Manipulate the Collective Decisions of Multi-Agents? (2025).** The M-Spoiler framework considers an attacker with knowledge of one agent and incomplete knowledge of the remaining system. It simulates interactions to generate adversarial inputs intended to mislead collective decisions. This directly connects to the idea of using one known agent as an entry point for understanding or influencing a group. [1]

The distinction is consequential: the paper’s main approach uses optimized adversarial suffixes and access to a known model. It does not establish that a few black-box conversations recover shared preferences, nor that an ordinary proposal designed from those preferences will transfer. Its reported experiments support a bounded claim about the tested agents and collaboration protocols. [1]

## Literature map

| Work | What it contributes | Boundary of the evidence |
| --- | --- | --- |
| M-Spoiler, Liu et al., 2025 [1] | Collective manipulation with one known agent. | Adversarial input optimization is different from learning preferences through conversation. |
| Multi-Agent Adversarial Inverse Reinforcement Learning, Yu, Song and Ermon, ICML 2019 [2] | Learning reward functions from demonstrated multi-agent behavior. | Studies Markov games; “adversarial” describes the learning framework, not malicious influence. |
| Bayesian Persuasion, Kamenica and Gentzkow, 2011 [3] | Formal information design: a sender chooses an information structure to influence a receiver’s action. | A theoretical model with specific assumptions, not an LLM swarm experiment. |
| Adversarial Search Engine Optimization for Large Language Models, Nestaas, Debenedetti and Tramèr, 2024 [4] | Preference manipulation through third-party content that affects model selections. | Does not establish recovery of a swarm’s objectives or transfer from one profiled agent. |
| When collaboration fails, Kraidia et al., Scientific Reports, 2026 [5] | A persuasive adversarial participant can distort collective LLM debate. | Controlled debate results do not establish susceptibility of every swarm architecture. |
| Biased decisions of Large Language Models, Bösch, 2026 [6] | Tests whether adding an inferior alternative changes autonomous agents’ selections through the decoy effect. | Effects vary across models; individual-agent choice bias is not evidence of swarm transfer. |
| Reward Identification in Inverse Reinforcement Learning, Kim et al., ICML 2021 [7] | Formal conditions under which behavior permits reward identification. | Successful choice prediction alone does not demonstrate recovery of the true reward function. |

These works cover different parts of the proposed mechanism. None should be cited as demonstrating the entire chain from black-box profiling of one agent to preference-based manipulation of an unseen swarm.

## Distinctions needed for a defensible claim

### Predicting choices and identifying objectives

An inferred preference model can be useful without representing the agent’s true internal objective. Reward identifiability requires assumptions and conditions; it cannot be presumed from observed decisions. Kim et al. formalize this issue for inverse reinforcement learning. [7]

For this project, “preference model” should mean a model that predicts held-out choices. Claims about recovered value functions or internal logic would require additional evidence.

### Shared susceptibility and social propagation

Two hypotheses could explain a group decision shift. Under **shared susceptibility**, an intervention independently affects several agents because relevant behavioral characteristics are shared. Under **social propagation**, an affected agent changes its peers through communication. These are proposed explanatory categories for the study, not findings established by this brief.

Testing individual agents before communication and comparing those results with the group outcome would help separate the mechanisms. Group-level success alone would not identify which mechanism occurred.

### Attractive offers and distorted decisions

If an option becomes objectively better under the user’s intended criteria, increased selection is not by itself evidence of poisoned decision-making. A convincing experiment should distinguish genuine improvements from changes in framing, irrelevant alternatives, or misleading evidence.

Similarly, direct instruction injection, false factual claims, and context-dependent choice bias are different interventions. Combining them into one success rate would obscure what the study actually demonstrates.

## Proposed research question

**How much does profiling one agent improve the ability to predict and shift an unseen swarm’s choices, and how much of any effect comes from shared preferences versus communication?**

The following are hypotheses to test, not conclusions:

- A preference model learned from one agent may generalize better when agents share a base model and similar decision criteria.
- Differences in roles, context, and aggregation rules may reduce or alter that transfer.
- Communication may amplify an initial shift, or allow other agents to correct it.
- A targeted preference model may add little beyond generic framing effects; that negative result would be informative.

## Proposed controlled study

Use a local testbed with synthetic decisions and an explicit evaluation rubric. Examples include selecting among fictional project plans or allocating a simulated resource budget. The rubric supplies an independent definition of decision quality.

Separate profiling examples from evaluation examples. Observe one designated agent during profiling, then freeze the resulting behavioral model before evaluating unseen agents and groups. Treat rationales as supplementary observations; measure actual selections separately.

| Comparison | Purpose |
| --- | --- |
| Neutral presentation versus generic framing | Measure baseline sensitivity without agent-specific information. |
| Generic framing versus preference-informed presentation | Determine whether profiling contributes incremental predictive or steering value. |
| Independent agent choices versus choices after discussion | Estimate the contribution of communication. |
| Shared-model groups versus mixed-model groups | Test whether transfer depends on model similarity. |
| Fixed candidates versus candidate sets with irrelevant alternatives | Isolate choice-set effects from changes in substantive option quality. |
| Alternative aggregation rules | Test whether the collective decision protocol changes outcomes. |

Keep the intervention categories separate. Start with presentation changes that preserve substantive facts. If studying misleading evidence as another condition, report it independently so its effects are not attributed to preference inference.

### Measurements

- **Prediction quality:** accuracy and calibration on held-out choices.
- **Target selection lift:** difference in designated-option selection probability between intervention and neutral conditions.
- **Decision quality loss:** change in score under the fixed independent rubric.
- **Transfer gap:** difference between effects on the profiled agent and on unseen agents or groups.
- **Communication effect:** difference between matched groups with and without deliberation.
- **Query cost:** number of observations required to obtain any incremental benefit.

Randomize option order, use repeated trials, and report uncertainty. Keep tasks used for intervention selection separate from final evaluation. A result supports the central hypothesis only if profiling improves over a generic baseline on held-out groups. Calling that result harmful influence additionally requires evidence that it worsens the independent decision-quality measure.

## What is established and what remains open

The reviewed literature supports the existence of adversarial collective influence in tested multi-agent systems, reward inference methods in structured environments, and selection manipulation in LLM applications. [1][2][4][5]

This review does not establish that one agent is representative of a whole swarm, that an LLM exposes a stable scalar utility through conversation, or that preference inference is necessary for successful influence. Nor does it establish that adding agents or diversity reliably prevents the effect. These are empirical questions for the particular system.

The strongest project contribution would be a controlled measurement of the additional value of profiling one agent, with shared susceptibility separated from communication effects. An attack demonstration without those comparisons would provide weaker evidence for the distinctive idea.

## References

1. Fengyuan Liu et al. **Can an Individual Manipulate the Collective Decisions of Multi-Agents?** 2025. [Abstract](https://arxiv.org/abs/2509.16494) · [Full text consulted](https://arxiv.org/html/2509.16494v1).
2. Lantao Yu, Jiaming Song and Stefano Ermon. **Multi-Agent Adversarial Inverse Reinforcement Learning.** ICML 2019, PMLR 97, 7194–7201. [Proceedings and paper](https://proceedings.mlr.press/v97/yu19e.html).
3. Emir Kamenica and Matthew Gentzkow. **Bayesian Persuasion.** American Economic Review 101(6), 2590–2615, 2011. [Publisher](https://pubs.aeaweb.org/doi/10.1257/aer.101.6.2590).
4. Fredrik Nestaas, Edoardo Debenedetti and Florian Tramèr. **Adversarial Search Engine Optimization for Large Language Models.** 2024. [Paper](https://arxiv.org/abs/2406.18382).
5. Insaf Kraidia et al. **When collaboration fails: persuasion driven adversarial influence in multi agent large language model debate.** Scientific Reports 16, 11640, 2026. [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC13061921/).
6. Kevin Bösch. **Biased decisions of Large Language Models (LLM): Computer control agents and the decoy effect.** 2026. DOI: 10.1016/j.socec.2026.102641. [Publisher](https://www.sciencedirect.com/science/article/abs/pii/S221480432600131X).
7. Kuno Kim, Shivam Garg, Kirankumar Shiragur and Stefano Ermon. **Reward Identification in Inverse Reinforcement Learning.** ICML 2021, PMLR 139, 5496–5505. [Proceedings and paper](https://proceedings.mlr.press/v139/kim21c.html).

This is a focused review of primary research located during this review, not a systematic review or a replication. Source coverage includes full-text inspection for the closest collective-influence papers and abstract or publisher-page review for supporting works. The study design and hypotheses are original synthesis for this brief.
