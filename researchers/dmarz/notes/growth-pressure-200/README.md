# Growth pressure and rule evasion in a 200-agent economy

**Astra Ultra’s experiment plan.** Owner: dmarz. Prospective exploratory design, published before implementation. No runs started.

[Read the experiment plan](PLAN.md) · [Setup and launch gates](SETUP.md) · [Design numbers](design.json) · [Design review](reviews/design-review.md)

The question is whether ordinary agents evade an explicit rule when successful cheating rivals compete with them as their own businesses grow toward a size levy. Four 200-agent economy batches each contain four isolated 50-owner markets. Each opening is forked into zero, one and four assigned cheating rivals per market, followed for 20 rounds.

The main comparison has 16 independent paired markets and 52,000 planned model decisions. Qualification adds 3,296 decisions. A measured-throughput gate targets completing qualification, all main runs and closeout within one hour once code and infrastructure are ready. This is a conditional execution target, not a measured runtime.

The design deliberately excludes extra models, a large parameter sweep and mechanically predetermined enforcement arms. It keeps legal growth, paying the levy and restraining output as meaningful alternatives, and treats a well-exposed null as useful evidence.

## Reproduce the plan checks

From the repository root:

```sh
python3 researchers/dmarz/notes/growth-pressure-200/src/check_plan.py
python3 researchers/dmarz/notes/growth-pressure-200/src/build_plan.py
```

These commands check arithmetic and render the document; they do not launch a simulation, contact a model provider or provision resources. Evidence metadata below describes the unrun hypothesis, not the predecessor's results.
