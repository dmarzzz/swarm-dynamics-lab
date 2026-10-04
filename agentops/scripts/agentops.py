#!/usr/bin/env python3
"""agentops: the people + fleet registry for a lab's simulation servers.

    check                      validate people/, fleet.yml, blueprints.yml
    list                       every server: owner, address, access, expiry
    add-person HANDLE --github LOGIN [--name NAME]
                               write people/HANDLE.yml with the keys GitHub has for LOGIN
    ssh-config                 Host blocks for ~/.ssh/config (User = you)
    claim ID --servers a,b --by PERSON/AGENT [--until 3h] [--experiment X] [--note ...] [--shared]
                               say you are using servers: writes claims/ID.yml via an auto-merged PR
    release ID [--status done|abandoned] [--note ...]
                               say you are finished (or that a run keeps going: --status running)
    claims [--all]             who holds which servers right now
    preflight                  before `task up`: refuse if a server of yours already exists on DO
                               but is missing from this machine's Tofu state (would duplicate it)
    sops-sync                  rewrite .sops.yaml so every active person's age key can decrypt secrets/
    inventory --list           Ansible dynamic inventory (ansible/inventory/fleet.py calls this)

"You" is AGENTOPS_ME, read from the environment or .env at the repo root.
Needs Python 3.9+ and PyYAML.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is missing: pip install pyyaml (or: uv run --with pyyaml scripts/agentops.py ...)")

ROOT = Path(__file__).resolve().parent.parent
PEOPLE_DIR = ROOT / "people"
GENERATED_DIR = ROOT / "generated"
HANDLE_RE = re.compile(r"^[a-z][a-z0-9_-]{1,31}$")
SERVER_RE = re.compile(r"^[a-z][a-z0-9-]{1,62}$")
KEY_RE = re.compile(r"^(ssh-ed25519|ssh-rsa|ecdsa-sha2-nistp(256|384|521)|sk-ssh-ed25519@openssh\.com|sk-ecdsa-sha2-nistp256@openssh\.com) [A-Za-z0-9+/=]+( .*)?$")
AGE_RE = re.compile(r"^age1[0-9a-z]{58}$")
CLAIMS_DIR = ROOT / "claims"
PROVIDERS = {"digitalocean", "manual"}
CLAIM_ACTIVE = {"planned", "running"}
CLAIM_STATUSES = CLAIM_ACTIVE | {"done", "abandoned"}
CLAIM_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,80}$")
# Linux accounts that must never be claimed by a handle.
RESERVED = {"root", "admin", "ubuntu", "daemon", "bin", "sys", "sync", "nobody", "swarm", "docker", "sshd"}


def env_value(key: str) -> str:
    """KEY from the environment, else from .env at the repo root (launchers do not load .env)."""
    val = os.environ.get(key, "")
    env = ROOT / ".env"
    if not val and env.exists():
        for line in env.read_text().splitlines():
            if line.strip().startswith(key + "="):
                val = line.split("=", 1)[1].split("#", 1)[0].strip().strip("'\"")
    return val


def me() -> str:
    return env_value("AGENTOPS_ME")


def load_people() -> dict:
    people = {}
    for f in sorted(PEOPLE_DIR.glob("*.yml")):
        if f.name.startswith("_"):
            continue
        data = yaml.safe_load(f.read_text()) or {}
        data["_file"] = f"people/{f.name}"
        people[f.stem] = data
    return people


def load_blueprints() -> dict:
    return (yaml.safe_load((ROOT / "blueprints.yml").read_text()) or {}).get("blueprints") or {}


def load_fleet() -> dict:
    return (yaml.safe_load((ROOT / "fleet.yml").read_text()) or {}).get("servers") or {}


def load_generated() -> dict:
    """DO addresses written by `task up`: generated/<owner>.json -> {server: {...}}."""
    out = {}
    for f in sorted(GENERATED_DIR.glob("*.json")):
        for name, info in (json.loads(f.read_text()) or {}).items():
            out[name] = {**info, "_owner_file": f.stem}
    return out


def load_claims(root: Path = ROOT) -> dict:
    out = {}
    for f in sorted((root / "claims").glob("*.yml")):
        data = yaml.safe_load(f.read_text()) or {}
        data["_file"] = f"claims/{f.name}"
        out[f.stem] = data
    return out


def parse_time(v):
    if v is None or v == "":
        return None
    if isinstance(v, dt.datetime):
        return v if v.tzinfo else v.replace(tzinfo=dt.timezone.utc)
    if isinstance(v, dt.date):
        return dt.datetime(v.year, v.month, v.day, tzinfo=dt.timezone.utc)
    d = dt.datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)


def active(people: dict) -> list:
    return [h for h, p in people.items() if p.get("active", True)]


def access_of(server: dict, people: dict) -> list:
    acc = server.get("access", "all")
    handles = active(people) if acc == "all" else list(acc)
    # The owner always keeps access to their own box.
    owner = server.get("owner")
    if owner in people and people[owner].get("active", True) and owner not in handles:
        handles.append(owner)
    return [h for h in handles if h in people and people[h].get("active", True)]


def address_of(name: str, server: dict, generated: dict) -> str:
    if server.get("provider") == "manual":
        return str(server.get("ip", ""))
    return str(generated.get(name, {}).get("ipv4", ""))


# --------------------------------------------------------------------------- check

def cmd_check(args) -> int:
    errors, warnings = [], []
    people = load_people()
    blueprints = load_blueprints()
    fleet = load_fleet()
    generated = load_generated()

    logins = {}
    for h, p in people.items():
        where = p["_file"]
        if not HANDLE_RE.match(h) or h in RESERVED:
            errors.append(f"{where}: handle '{h}' must be lowercase [a-z0-9_-], 2-32 chars, and not a system account")
        gh = p.get("github")
        if not gh:
            errors.append(f"{where}: missing github")
        elif gh.lower() in logins:
            errors.append(f"{where}: github '{gh}' already used by {logins[gh.lower()]}")
        else:
            logins[gh.lower()] = where
        keys = p.get("ssh_keys") or []
        if p.get("active", True) and not keys:
            errors.append(f"{where}: active person with no ssh_keys")
        for k in keys:
            if not KEY_RE.match(str(k).strip()):
                errors.append(f"{where}: not an OpenSSH public key: {str(k)[:40]}...")
            if "PRIVATE KEY" in str(k):
                errors.append(f"{where}: that is a PRIVATE key. Remove it and rotate it.")
        age = p.get("age") or ""
        if age and not AGE_RE.match(age):
            errors.append(f"{where}: age must be an age1... public key")

    for b, spec in blueprints.items():
        if not spec.get("size"):
            errors.append(f"blueprints.yml: {b} has no size")

    for name, s in fleet.items():
        where = f"fleet.yml: {name}"
        s = s or {}
        if not SERVER_RE.match(name):
            errors.append(f"{where}: name must be lowercase [a-z0-9-]")
        owner = s.get("owner")
        if owner not in people:
            errors.append(f"{where}: owner '{owner}' has no people/{owner}.yml")
        prov = s.get("provider")
        if prov not in PROVIDERS:
            errors.append(f"{where}: provider must be one of {sorted(PROVIDERS)}")
        if s.get("blueprint") not in blueprints:
            errors.append(f"{where}: blueprint must be one of {sorted(blueprints)}")
        if prov == "manual" and not s.get("ip"):
            errors.append(f"{where}: manual servers need ip")
        acc = s.get("access", "all")
        if acc != "all":
            if not isinstance(acc, list):
                errors.append(f"{where}: access must be 'all' or a list of handles")
            else:
                for h in acc:
                    if h not in people:
                        errors.append(f"{where}: access lists '{h}', who has no people/{h}.yml")
        if not s.get("purpose"):
            warnings.append(f"{where}: no purpose")
        exp = s.get("expires")
        if exp is None:
            if prov == "digitalocean":
                warnings.append(f"{where}: no expires date (DO bills until someone runs task down)")
        else:
            try:
                d = exp if isinstance(exp, dt.date) else dt.date.fromisoformat(str(exp))
                if d < dt.date.today():
                    warnings.append(f"{where}: expired {d}; destroy it (task down) or move the date")
            except ValueError:
                errors.append(f"{where}: expires must be YYYY-MM-DD")
        for port in s.get("ports") or []:
            if not isinstance(port, int) or not 1 <= port <= 65535:
                errors.append(f"{where}: bad port {port}")
        if prov == "digitalocean" and name not in generated:
            warnings.append(f"{where}: not created yet (owner runs task up)")

    for name, info in generated.items():
        if name not in fleet:
            warnings.append(f"generated/{info['_owner_file']}.json: {name} is not in fleet.yml (destroyed? run task up to refresh)")

    now = dt.datetime.now(dt.timezone.utc)
    holders = {}
    for cid, c in load_claims().items():
        where = c["_file"]
        if not CLAIM_RE.match(cid):
            errors.append(f"{where}: claim id must be lowercase [a-z0-9._-]")
        st = c.get("status")
        if st not in CLAIM_STATUSES:
            errors.append(f"{where}: status must be one of {sorted(CLAIM_STATUSES)}")
        by = str(c.get("by") or "")
        if by.split("/")[0] not in people:
            errors.append(f"{where}: by '{by}' must start with a handle from people/ (e.g. alice/claude-1)")
        servers = c.get("servers") or []
        if not servers:
            errors.append(f"{where}: no servers")
        for s in servers:
            if s not in fleet and st in CLAIM_ACTIVE:
                errors.append(f"{where}: server '{s}' is not in fleet.yml")
        try:
            until = parse_time(c.get("until"))
        except ValueError:
            errors.append(f"{where}: until must be an ISO time")
            until = None
        if st in CLAIM_ACTIVE:
            if until and until < now:
                warnings.append(f"{where}: still {st} but until {until:%Y-%m-%d %H:%M}Z has passed; release it or extend")
            for s in servers:
                holders.setdefault(s, []).append((cid, not c.get("shared", False)))
    for s, hs in holders.items():
        if len(hs) > 1 and any(excl for _, excl in hs):
            errors.append(f"claims: {s} is claimed by {', '.join(c for c, _ in hs)} at once, and at least one is exclusive")

    # Pull-request rule: you may only edit your own people/ file. The repo owner
    # (passed as --admin) may edit any, e.g. to deactivate someone.
    if args.author:
        admins = {a.lower() for a in (args.admin or [])}
        for f in args.changed or []:
            m = re.match(r"^people/([^/_][^/]*)\.yml$", f)
            if not m:
                continue
            handle = m.group(1)
            # Ownership comes from the base branch when the file already exists
            # there, so nobody can take over a file by rewriting its github field.
            owner_login = ""
            if args.base:
                r = subprocess.run(["git", "show", f"{args.base}:{f}"], cwd=ROOT, capture_output=True, text=True)
                if r.returncode == 0:
                    owner_login = (yaml.safe_load(r.stdout) or {}).get("github", "")
            if not owner_login:
                owner_login = (people.get(handle) or {}).get("github", "")
            if args.author.lower() in admins:
                continue
            if owner_login.lower() != args.author.lower():
                errors.append(f"{f}: changed by @{args.author}, but this file belongs to @{owner_login or '?'}")

    for w in warnings:
        print(f"warn  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(people)} people, {len(fleet)} servers, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


# --------------------------------------------------------------------------- list

def cmd_list(args) -> int:
    people, fleet, generated = load_people(), load_fleet(), load_generated()
    rows = [("server", "owner", "blueprint", "address", "access", "expires", "purpose")]
    for name, s in sorted(fleet.items()):
        acc = s.get("access", "all")
        rows.append((
            name, s.get("owner", ""), s.get("blueprint", ""),
            address_of(name, s, generated) or "(not created)",
            "all" if acc == "all" else ",".join(access_of(s, people)),
            str(s.get("expires", "")), s.get("purpose", ""),
        ))
    widths = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]) - 1)]
    for r in rows:
        print("  ".join(str(c).ljust(w) for c, w in zip(r, widths)) + "  " + str(r[-1]))
    return 0


# --------------------------------------------------------------------------- add-person

def cmd_add_person(args) -> int:
    h = args.handle
    if not HANDLE_RE.match(h) or h in RESERVED:
        sys.exit(f"bad handle '{h}': lowercase [a-z0-9_-], 2-32 chars")
    path = PEOPLE_DIR / f"{h}.yml"
    if path.exists() and not args.force:
        sys.exit(f"{path.relative_to(ROOT)} exists (use --force to overwrite)")
    url = f"https://github.com/{args.github}.keys"
    with urllib.request.urlopen(url, timeout=15) as r:
        keys = [k.strip() for k in r.read().decode().splitlines() if k.strip()]
    if not keys:
        sys.exit(f"GitHub has no public keys for {args.github}. Add one at https://github.com/settings/keys or paste it into the file.")
    doc = {"github": args.github, "name": args.name or args.github, "active": True, "ssh_keys": keys, "age": args.age or ""}
    path.write_text(f"# {h}\n" + yaml.safe_dump(doc, sort_keys=False, width=1000))
    print(f"wrote {path.relative_to(ROOT)} with {len(keys)} key(s) from {url}")
    return 0


# --------------------------------------------------------------------------- ssh-config

def cmd_ssh_config(args) -> int:
    user = args.user or me()
    if not user:
        sys.exit("set AGENTOPS_ME=<your handle> in .env (or pass --user)")
    fleet, generated = load_fleet(), load_generated()
    key = env_value("AGENTOPS_SSH_KEY")
    ident = f"  IdentityFile {Path(key).expanduser()}\n  IdentitiesOnly yes\n" if key else ""
    print("# >>> agentops >>>  (regenerate: task ssh-config)")
    for name, s in sorted(fleet.items()):
        addr = address_of(name, s, generated)
        if not addr:
            continue
        print(f"Host {name}\n  HostName {addr}\n  User {user}\n  Port {s.get('ssh_port', 22)}\n{ident}"
              f"  StrictHostKeyChecking accept-new\n  ForwardAgent no\n")
    print("# <<< agentops <<<")
    return 0


# --------------------------------------------------------------------------- claims

def _duration(s: str) -> dt.datetime:
    """'3h', '90m', '2d' or an ISO time -> aware datetime."""
    m = re.match(r"^(\d+(?:\.\d+)?)([mhd])$", s or "")
    if m:
        n, unit = float(m.group(1)), m.group(2)
        field = {"m": "minutes", "h": "hours", "d": "days"}[unit]
        return dt.datetime.now(dt.timezone.utc) + dt.timedelta(**{field: n})
    return parse_time(s)


def _iso(d: dt.datetime) -> str:
    return d.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _git(*a, cwd=ROOT, check=True):
    r = subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f"git {' '.join(a)}: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout.strip()


def _gh_identity():
    """Commit as the GitHub noreply address: pushes with a private email are refused
    when the account has email privacy on."""
    r = subprocess.run(["gh", "api", "user", "--jq", '.login + " " + (.id|tostring)'], capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        login, uid = r.stdout.split()
        return login, f"{uid}+{login}@users.noreply.github.com"
    return (_git("config", "user.name", check=False) or "agentops"), (_git("config", "user.email", check=False) or "agentops@localhost")


def _publish(cid: str, doc: dict, verb: str, pr: bool) -> None:
    """Write claims/<cid>.yml on top of origin/main in a throwaway worktree, check it,
    and land it as an auto-merged PR. The caller's own checkout is never touched
    except for a final fast-forward, so other agents' uncommitted work is safe."""
    text = f"# {verb} by {doc.get('by')}; see README.md (Claims)\n" + yaml.safe_dump(doc, sort_keys=False, width=1000)
    if not pr:
        CLAIMS_DIR.mkdir(exist_ok=True)
        (CLAIMS_DIR / f"{cid}.yml").write_text(text)
        print(f"wrote claims/{cid}.yml (not committed: --no-pr)")
        return
    import tempfile
    _git("fetch", "-q", "origin", "main")
    wt = Path(tempfile.mkdtemp(prefix="agentops-claim-")) / "wt"
    _git("worktree", "add", "-q", "--detach", str(wt), "origin/main")
    try:
        (wt / "claims").mkdir(exist_ok=True)
        (wt / "claims" / f"{cid}.yml").write_text(text)
        chk = subprocess.run([sys.executable, str(wt / "scripts/agentops.py"), "check"], capture_output=True, text=True)
        bad = [l for l in chk.stdout.splitlines() if l.startswith("ERROR") and "claims" in l]
        if bad:
            sys.exit("refusing to " + verb + ":\n" + "\n".join(bad))
        branch = f"claim/{cid}-{doc['status']}-{dt.datetime.now(dt.timezone.utc):%H%M%S}"
        _git("add", f"claims/{cid}.yml", cwd=wt)
        name, email = _gh_identity()
        _git("-c", f"user.name={name}", "-c", f"user.email={email}", "commit", "-q", "-m", f"claim {cid}: {doc['status']} ({', '.join(doc['servers'])}) by {doc['by']}",
             "-m", doc.get("note") or "", cwd=wt)
        _git("push", "-q", "origin", f"HEAD:refs/heads/{branch}", cwd=wt)
        body = (f"**{doc['status']}** on {', '.join(doc['servers'])} by `{doc['by']}`"
                + (f" until {doc['until']}" if doc.get("until") else "")
                + (f"\n\nexperiment: `{doc['experiment']}`" if doc.get("experiment") else "")
                + (f"\n\n{doc['note']}" if doc.get("note") else ""))
        url = subprocess.run(["gh", "pr", "create", "--base", "main", "--head", branch,
                              "--title", f"claim {cid}: {doc['status']}", "--body", body],
                             cwd=wt, capture_output=True, text=True)
        if url.returncode:
            sys.exit(f"gh pr create failed: {url.stderr.strip()}")
        m = subprocess.run(["gh", "pr", "merge", url.stdout.strip(), "--squash", "--delete-branch"],
                           cwd=wt, capture_output=True, text=True)
        print(f"{verb}: {url.stdout.strip()} " + ("merged" if m.returncode == 0 else f"NOT merged: {m.stderr.strip()}"))
    finally:
        _git("worktree", "remove", "--force", str(wt), check=False)
    # Bring the merged claim into this checkout if that is a clean fast-forward.
    if _git("rev-parse", "--abbrev-ref", "HEAD", check=False) == "main":
        r = subprocess.run(["git", "pull", "-q", "--ff-only", "origin", "main"], cwd=ROOT, capture_output=True, text=True)
        if r.returncode:
            print("note: could not fast-forward this checkout; `git pull` when convenient")
    # Two claims can merge at the same moment; re-check what landed.
    _git("fetch", "-q", "origin", "main")
    landed = subprocess.run(["git", "show", f"origin/main:claims/{cid}.yml"], cwd=ROOT, capture_output=True, text=True)
    if landed.returncode == 0:
        servers = set(doc["servers"])
        for f in _git("ls-tree", "--name-only", "origin/main", "claims/").splitlines():
            other = yaml.safe_load(_git("show", f"origin/main:{f}")) or {}
            if Path(f).stem != cid and other.get("status") in CLAIM_ACTIVE and servers & set(other.get("servers") or []) \
                    and (not other.get("shared") or not doc.get("shared")) and doc["status"] in CLAIM_ACTIVE:
                print(f"WARNING: {f} also holds {', '.join(servers & set(other['servers']))}. Talk to {other.get('by')} before starting.")


def _hub_event(kind: str, cid: str, doc: dict) -> None:
    """Mirror the claim to the hub dashboard. Best effort."""
    try:
        sys.path.insert(0, str(ROOT / "hub"))
        import swarm_report  # noqa: E402
        for line in ((ROOT / ".env").read_text().splitlines() if (ROOT / ".env").exists() else []):
            k, _, v = line.partition("=")
            if k.strip() in ("SWARM_HUB_URL", "SWARM_HUB_TOKEN") and v.strip() and not os.environ.get(k.strip()):
                os.environ[k.strip()] = v.strip()
        if not os.environ.get("SWARM_HUB_TOKEN"):
            tok = _hub_token()
            if tok:
                os.environ["SWARM_HUB_TOKEN"] = tok
        if not os.environ.get("SWARM_HUB_URL"):
            os.environ["SWARM_HUB_URL"] = inventory()["all"]["vars"]["agentops_hub_url"]
        swarm_report.report(kind, run=cid, source=doc.get("by"), status=doc.get("status"), message=doc.get("note"),
                            role="coordinator", data={"id": cid, "servers": doc.get("servers"), "until": doc.get("until"),
                                                      "experiment": doc.get("experiment")})
    except Exception as e:  # noqa: BLE001
        print(f"note: hub not updated ({e})")


def _hub_token() -> str:
    f = ROOT / "secrets/hub.sops.env"
    if not f.exists():
        return ""
    env = dict(os.environ)
    if not env.get("SOPS_AGE_KEY_FILE") and (ROOT / "keys.txt").exists():
        env["SOPS_AGE_KEY_FILE"] = str(ROOT / "keys.txt")
    r = subprocess.run(["sops", "-d", str(f)], capture_output=True, text=True, env=env)
    m = re.search(r"SWARM_HUB_TOKEN=(\S+)", r.stdout)
    return m.group(1) if m else ""


def cmd_claim(args) -> int:
    cid = args.id
    if not CLAIM_RE.match(cid):
        sys.exit("claim id: lowercase [a-z0-9._-], e.g. alice-boids-sweep")
    fleet = load_fleet()
    servers = [s.strip() for s in args.servers.split(",") if s.strip()]
    missing = [s for s in servers if s not in fleet]
    if missing:
        sys.exit(f"not in fleet.yml: {', '.join(missing)}")
    if not args.by or "/" not in args.by:
        sys.exit("--by <handle>/<tool>-<n>, e.g. alice/claude-1")
    doc = {"servers": servers, "by": args.by, "status": args.status, "shared": bool(args.shared),
           "since": _iso(dt.datetime.now(dt.timezone.utc)), "until": _iso(_duration(args.until)) if args.until else None,
           "experiment": args.experiment, "note": args.note}
    doc = {k: v for k, v in doc.items() if v not in (None, "")}
    _publish(cid, doc, "claim", not args.no_pr)
    _hub_event("claim", cid, doc)
    return 0


def cmd_release(args) -> int:
    claims = load_claims()
    _git("fetch", "-q", "origin", "main", check=False)
    remote = subprocess.run(["git", "show", f"origin/main:claims/{args.id}.yml"], cwd=ROOT, capture_output=True, text=True)
    doc = yaml.safe_load(remote.stdout) if remote.returncode == 0 else claims.get(args.id)
    if not doc:
        sys.exit(f"no claim {args.id}")
    doc.pop("_file", None)
    doc["status"] = args.status
    if args.note:
        doc["note"] = args.note
    if args.until:
        doc["until"] = _iso(_duration(args.until))
    if args.status not in CLAIM_ACTIVE:
        doc["ended"] = _iso(dt.datetime.now(dt.timezone.utc))
    _publish(args.id, doc, "release" if args.status not in CLAIM_ACTIVE else "update", not args.no_pr)
    _hub_event("release" if args.status not in CLAIM_ACTIVE else "claim", args.id, doc)
    return 0


def cmd_claims(args) -> int:
    rows = [("claim", "status", "servers", "by", "until", "note")]
    for cid, c in load_claims().items():
        if args.all or c.get("status") in CLAIM_ACTIVE:
            rows.append((cid, c.get("status", ""), ",".join(c.get("servers") or []) + (" (shared)" if c.get("shared") else ""),
                         c.get("by", ""), str(c.get("until", "")), c.get("note", "")))
    if len(rows) == 1:
        print("no active claims (git pull first)")
        return 0
    widths = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]) - 1)]
    for r in rows:
        print("  ".join(str(c).ljust(w) for c, w in zip(r, widths)) + "  " + str(r[-1]))
    return 0


# --------------------------------------------------------------------------- preflight

def cmd_preflight(args) -> int:
    """Tofu state is local to the machine that ran `task up`. From any other
    checkout the same owner's servers look missing, and apply would create
    duplicates (and overwrite ~/.ssh/<name>_ed25519). Catch that first."""
    user, token = me(), os.environ.get("DIGITALOCEAN_TOKEN", "")
    if not user or not token:
        sys.exit("preflight needs AGENTOPS_ME and DIGITALOCEAN_TOKEN")
    mine = {n for n, s in load_fleet().items() if s.get("owner") == user and s.get("provider") == "digitalocean"}
    req = urllib.request.Request(
        f"https://api.digitalocean.com/v2/droplets?tag_name=owner-{user}&per_page=200",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        live = [(d["name"], str(d["id"])) for d in json.load(r)["droplets"]]
    show = subprocess.run(["tofu", "show", "-json"], cwd=ROOT / "tofu", capture_output=True, text=True)
    in_state = set()
    if show.returncode == 0 and show.stdout.strip():
        for res in (json.loads(show.stdout).get("values") or {}).get("root_module", {}).get("resources", []):
            if res.get("type") == "digitalocean_droplet":
                in_state.add(str(res["values"]["id"]))
    bad = [(n, i) for n, i in live if n in mine and i not in in_state]
    if not bad:
        print(f"preflight ok: {len(live)} droplet(s) tagged owner-{user} on DO, none missing from this state")
        return 0
    print("ERROR these servers already exist on DigitalOcean but not in this machine's Tofu state.")
    print("      `task up` here would create a second copy. Run it from the machine that created them,")
    print("      or adopt them into this state (the root key stays on the original machine):")
    for n, i in bad:
        print(f"        tofu -chdir=tofu import 'digitalocean_droplet.this[\"{n}\"]' {i}")
    return 1


# --------------------------------------------------------------------------- sops-sync

def cmd_sops_sync(args) -> int:
    people = load_people()
    recipients = [people[h]["age"] for h in active(people) if people[h].get("age")]
    if not recipients:
        sys.exit("no active person has an age key")
    text = (
        "# GENERATED by scripts/agentops.py sops-sync from people/*.yml `age:` fields.\n"
        "# After it changes, re-key existing files: task secrets:updatekeys\n"
        "creation_rules:\n"
        "  - path_regex: (^|/)secrets/.*\n"
        f"    age: >-\n      {','.join(recipients)}\n"
    )
    (ROOT / ".sops.yaml").write_text(text)
    print(f".sops.yaml: {len(recipients)} recipient(s)")
    return 0


# --------------------------------------------------------------------------- inventory

def inventory() -> dict:
    people, fleet, generated, blueprints = load_people(), load_fleet(), load_generated(), load_blueprints()
    user = me()
    hostvars, groups = {}, {"swarm": []}
    for name, s in sorted(fleet.items()):
        addr = address_of(name, s, generated)
        if not addr:
            continue
        bp = s.get("blueprint", "sim")
        hv = {
            "ansible_host": addr,
            "ansible_port": s.get("ssh_port", 22),
            "agentops_owner": s.get("owner"),
            "agentops_blueprint": bp,
            "agentops_install": (blueprints.get(bp) or {}).get("install", []),
            "agentops_access": access_of(s, people),
            "agentops_ports": sorted(set((s.get("ports") or []) + ((blueprints.get(bp) or {}).get("ports") or []))),
        }
        if user:
            hv["ansible_user"] = user
        hostvars[name] = hv
        groups["swarm"].append(name)
        groups.setdefault(f"bp_{bp}", []).append(name)
        groups.setdefault(f"owner_{s.get('owner')}", []).append(name)
    hub_url = next((f"https://{hostvars[n]['ansible_host']}" for n in sorted(hostvars)
                    if hostvars[n]["agentops_blueprint"] == "hub"), "")
    people_vars = {h: {"ssh_keys": p.get("ssh_keys") or [], "active": bool(p.get("active", True))} for h, p in people.items()}
    inv = {"_meta": {"hostvars": hostvars}, "all": {"children": sorted(groups), "vars": {"agentops_people": people_vars, "agentops_hub_url": hub_url}}}
    for g, hosts in groups.items():
        inv[g] = {"hosts": hosts}
    return inv


def cmd_inventory(args) -> int:
    if args.host:
        print(json.dumps(inventory()["_meta"]["hostvars"].get(args.host, {})))
    else:
        print(json.dumps(inventory(), indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--author", help="PR author's GitHub login (CI)")
    c.add_argument("--admin", action="append", help="GitHub login allowed to edit any people/ file")
    c.add_argument("--changed", nargs="*", help="files changed in the PR (CI)")
    c.add_argument("--base", help="git ref of the PR base, e.g. origin/main (CI)")
    c.set_defaults(fn=cmd_check)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    a = sub.add_parser("add-person")
    a.add_argument("handle")
    a.add_argument("--github", required=True)
    a.add_argument("--name")
    a.add_argument("--age")
    a.add_argument("--force", action="store_true")
    a.set_defaults(fn=cmd_add_person)
    s = sub.add_parser("ssh-config")
    s.add_argument("--user")
    s.set_defaults(fn=cmd_ssh_config)
    cl = sub.add_parser("claim")
    cl.add_argument("id")
    cl.add_argument("--servers", required=True, help="comma-separated fleet.yml names")
    cl.add_argument("--by", default=os.environ.get("SWARM_SOURCE"), help="<handle>/<tool>-<n>")
    cl.add_argument("--until", help="3h, 90m, 2d or an ISO time")
    cl.add_argument("--status", choices=sorted(CLAIM_ACTIVE), default="running")
    cl.add_argument("--experiment", help="experiment id (experiments/<id> in the research repo, same id you report to the hub)")
    cl.add_argument("--note")
    cl.add_argument("--shared", action="store_true", help="others may run on these servers at the same time")
    cl.add_argument("--no-pr", action="store_true", help="only write the file")
    cl.set_defaults(fn=cmd_claim)
    rl = sub.add_parser("release")
    rl.add_argument("id")
    rl.add_argument("--status", choices=sorted(CLAIM_STATUSES), default="done")
    rl.add_argument("--note")
    rl.add_argument("--until", help="extend: 3h, 2d or ISO (with --status running)")
    rl.add_argument("--no-pr", action="store_true")
    rl.set_defaults(fn=cmd_release)
    cs = sub.add_parser("claims")
    cs.add_argument("--all", action="store_true")
    cs.set_defaults(fn=cmd_claims)
    sub.add_parser("preflight").set_defaults(fn=cmd_preflight)
    sub.add_parser("sops-sync").set_defaults(fn=cmd_sops_sync)
    i = sub.add_parser("inventory")
    i.add_argument("--list", action="store_true")
    i.add_argument("--host")
    i.set_defaults(fn=cmd_inventory)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
