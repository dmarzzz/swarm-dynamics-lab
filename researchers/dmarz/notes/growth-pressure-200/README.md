# Growth pressure and rule evasion in a 200-agent economy

**Astra Ultra’s experiment plan · v2: seeding × peer messaging.** Owner: dmarz. Prospective exploratory design, published before implementation. No runs started.

[Read the experiment plan](PLAN.md) · [Setup and launch gates](SETUP.md) · [Design numbers](design.json) · [V2 review](reviews/design-review-v2.md) · [Amendment and preserved v1](AMENDMENT-02.md)

The question is whether ordinary agents evade an explicit rule when successful cheating rivals compete with them as their own businesses grow toward a size levy, and whether peer messaging changes that effect. Three 200-agent economy batches each contain four isolated 50-owner markets. After five silent opening rounds, each batch forks into four conditions for 20 rounds:

| Arm | Assigned evaders per market | Peer messaging |
|---|---:|---|
| A | 0 | Off |
| B | 0 | On, neutrally encouraged |
| C | 4 | Off |
| D | 4 | On, neutrally encouraged |

Primary D − B; secondary interaction (D − B) − (C − A). The main comparison has 12 independent paired markets and 51,000 planned model decisions. Qualification adds 3,096 decisions. A measured-throughput gate targets completing qualification, all main runs and closeout within one hour once code and infrastructure are ready. This is a conditional execution target, not a measured runtime.

The design deliberately excludes extra models, a large parameter sweep and mechanically predetermined enforcement arms. It keeps legal growth, paying the levy and restraining output as meaningful alternatives. Agents explicitly choose send or pass, without a reward for persuading others or a supplied exploit argument. Public market observations remain visible in all arms. A well-exposed null remains useful evidence.

## Reproduce the plan checks

From the repository root:

```sh
python3 researchers/dmarz/notes/growth-pressure-200/src/check_plan.py
python3 researchers/dmarz/notes/growth-pressure-200/src/build_plan.py
```

These commands check arithmetic and render the document; they do not launch a simulation, contact a model provider or provision resources. Evidence metadata describes the unrun hypothesis, not the predecessor's results.
