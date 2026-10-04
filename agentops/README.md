# agentops (template)

This folder is a template of the fleet setup that ran the lab's multi-agent experiments. The original
lives in a private repo; this copy keeps the structure and the code and replaces every identifier with
a placeholder.

What it gave the team:

- Any researcher, or an agent working for them, could create a short-lived cloud server from one entry
  in a fleet file, and everyone on the team could ssh into it as themselves.
- Every run on every server reported to one hub: experiments, a run queue, events, metrics and
  artifacts, on one dashboard with backups.
- Servers were claimed with expiring claims recorded in git, so parallel agents did not run on the
  same box.
- Shared credentials were encrypted to each person's age key, so the repo held no plaintext secrets.

## What is here

| Path | Purpose |
|------|---------|
| `people/` | One file per person: GitHub login, ssh public keys, age public key. `alice.yml` and `bob.yml` are examples. |
| `fleet.example.yml` | Copy to `fleet.yml`. Every server: owner, blueprint, region, access, expiry. |
| `blueprints.yml` | What each kind of server is: droplet size, open ports, roles to install. |
| `tofu/` | One OpenTofu root module. Each owner applies only their own servers in their own workspace: droplet, root key, cloud-init accounts, firewall. Writes addresses to `generated/<owner>.json`. |
| `ansible/roles/base` | Packages, timezone, locale, swap. |
| `ansible/roles/access` | One Linux account per person with access, their keys, sudo, the shared `swarm` group and `/srv/swarm`. |
| `ansible/roles/security` | sshd locked to keys and the allowed users, ufw, fail2ban, unattended upgrades. |
| `ansible/roles/docker`, `python`, `node`, `agents` | Docker, Python with uv, Node 22, and the Claude Code and Codex CLIs. |
| `ansible/roles/reporter` | The `swarm-report` client, the hub address and token, and a heartbeat timer. Runs on every server. |
| `ansible/roles/hub` | The hub service, Caddy with HTTPS in front of it, backups to object storage, a daily restore check. |
| `hub/` | `hub.py` (standard library and SQLite), `swarm_report.py` (client and CLI), `dashboard.html`. |
| `claims/` | One file per claim: who is using which servers, until when. One example is included. |
| `secrets/` | Where sops-encrypted files go. Empty here except its README. |
| `scripts/agentops.py` | check, list, add-person, ssh-config, claim, release, claims, preflight, sops-sync, Ansible inventory. |
| `scripts/` (other) | `safe-deploy.sh`, `hub-forget-gone.sh`, `hub-claims-sync.py`, `deploy-pages.sh`, `example-launcher.py`. |
| `Taskfile.yml` | Wraps all of the above as `task <name>`. |
| `docs/REPORTING.md` | The contract between runs and the hub, including the HTTP API and restore steps. |

## What was left out on purpose

- Secrets (even encrypted ones), the real sops config, OpenTofu state and every key file.
- The real people files, fleet file, claims and generated server addresses.
- Agent traces and the tooling that collected them.
- Per-experiment launchers, credential delivery scripts, run records and planning notes. One generic
  launcher, `scripts/example-launcher.py`, shows the pattern.
- The experiment-specific controller role and its blueprint.
- The live public site that read the hub through a read-only proxy. The hub still has the read token
  and the public state endpoint it used.
- The CI workflow that ran `agentops.py check` on every pull request and rejected edits to another
  person's file. `agentops.py check --author` still has that logic.

All names, addresses, domains, account ids and keys were replaced with placeholders. This copy has not
been run end to end after scrubbing, so expect to fix small things.

## Recreate it

Copy this folder into a new private repo first. Once filled in, `fleet.yml`, `generated/` and
`people/` hold server addresses and public keys, which do not belong in a public repo.

1. Accounts and tools. You need a DigitalOcean account and API token, a GitHub repo with the `gh` CLI
   signed in (claims land as pull requests), and optionally an S3-compatible bucket for hub backups.
   Run `task setup` to install Ansible, OpenTofu, sops, age and PyYAML.
2. `cp .env.example .env` and set `AGENTOPS_ME=<handle>` and `DIGITALOCEAN_TOKEN`.
3. Make your age key with `task secrets:keygen`. It writes `keys.txt` and prints the public key.
4. Add yourself: `python3 scripts/agentops.py add-person <handle> --github <login>`, then put the age
   public key in the `age:` field of `people/<handle>.yml`. Delete `people/alice.yml`, `people/bob.yml`
   and `claims/alice-boids-sweep.yml`.
5. `task secrets:sync` writes `.sops.yaml` from everyone's age keys (`.sops.yaml.example` shows the
   shape). Then create the hub token: `task secrets:edit -- secrets/hub.sops.env` with a line
   `SWARM_HUB_TOKEN=<long random string>`. For backups add `SPACES_ACCESS_KEY`, `SPACES_SECRET_KEY`,
   `SPACES_ENDPOINT` and `SPACES_BUCKET` to the same file.
6. `cp fleet.example.yml fleet.yml` and describe your servers: one with `blueprint: hub`, one or more
   with `blueprint: sim`, each with your handle as `owner` and an `expires` date.
7. `task check`, then `task plan`, then `task up`. Commit `fleet.yml` and `generated/<handle>.json`.
8. After about a minute, `task provision HOST=hub-01`, then `task provision HOST=sim-01`. Use
   `task bootstrap HOST=<name>` first for a `provider: manual` machine.
9. Check the hub: `task hub:open` opens the dashboard, `task ping` reaches every server, `task list`
   shows addresses, and `task ssh-config >> ~/.ssh/config` lets you `ssh sim-01`.
10. Claim a box before using it:
    `python3 scripts/agentops.py claim <handle>-first-run --servers sim-01 --by <handle>/claude-1 --until 3h`.
    `task claims` shows current holders. Add `--no-pr` to write the file without a pull request.
11. Run something that reports to the hub (next section), or adapt `scripts/example-launcher.py`.
12. Release and tear down: `python3 scripts/agentops.py release <handle>-first-run --note "done"`,
    remove the server from `fleet.yml`, run `task down`, and commit.

When people join or leave, edit `people/` and run `task access`. After hub code changes, run
`task hub:safe-deploy`, which waits until no run is active. `task reporter:deploy` updates the client
on every server.

## How a run reports to the hub

Every provisioned server has `swarm_report` importable and the hub address and token in
`/etc/swarm/report.env`. Set `SWARM_SOURCE=<handle>/<tool>-<n>` and use the client:

```python
import swarm_report as sr

sr.register("boids-noise", title="Boids: order vs noise",
            params={"eta": {"type": "float"}, "seed": {"type": "int"}},
            metrics=["order"], primary_metric="order")                  # once per experiment
sr.enqueue("boids-noise", [{"eta": e / 10, "seed": 1} for e in range(11)])   # coordinator

def simulate(run):                                                      # worker
    for step in range(1, 101):
        run.progress(step, 100, order=0.5)
    run.artifact("out/order.png")
    run.done(order=0.91, message="transition near eta=0.4")

sr.work("boids-noise", simulate)    # takes queued runs until none are left
```

A run that returns is marked done and one that raises is marked failed. Reports are spooled locally
while the hub is unreachable and replayed later. `swarm-report pause -m "why"` stops the hub from
handing out new runs and `swarm-report resume` undoes it. The full contract is in `docs/REPORTING.md`.

## Costs and safety

- Every DigitalOcean server needs an `expires` date and `task check` warns once it has passed. Tear
  boxes down when a run is done. The owner of a server pays for it.
- Run `task up` for a server only from the machine that created it. State is local, and the preflight
  refuses to create a duplicate.
- Put a spend cap on every model API key before it goes into `secrets/`. Workers run unattended.
- Never commit `.env`, `keys.txt`, OpenTofu state or any private key. The `.gitignore` here covers them.
- Everyone with an account has sudo and can read the hub token on every box. Give access only to people
  and agents you would give the whole fleet to.
- The dashboard shows params, messages and artifacts to the whole team. Keep secrets out of them.
