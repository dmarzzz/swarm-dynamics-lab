# secrets/

Shared credentials for simulation runs (API keys for agent episodes, dataset tokens), encrypted with
SOPS to every active person's age key. Only `*.sops.*` files are tracked; anything else here is ignored.

```bash
task secrets:edit -- secrets/sim.sops.env    # create or edit
sops exec-env secrets/sim.sops.env '<command>'   # run a command with the values in its environment
```

When someone adds or changes `age:` in their people file, run `task secrets:sync` and push, so the
files are re-keyed for them. Put only what everyone may see in here. Your DigitalOcean token stays in
your own `.env`.
