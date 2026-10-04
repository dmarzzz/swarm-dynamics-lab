"""Make the hub's claim list match claims/ on origin/main.

agentops.py mirrors a claim or release to the hub only as a best effort; when the shell has no hub token
(no SOPS_AGE_KEY_FILE, no .env) the registry changes and the hub keeps the old picture.

Usage, from an agentops checkout with SOPS_AGE_KEY_FILE set:
    git fetch origin && python3 scripts/hub-claims-sync.py <hub state URL>           # dry run, prints differences
    git fetch origin && python3 scripts/hub-claims-sync.py <hub state URL> --apply   # sends claim/release events
"""
import sys, subprocess, yaml, importlib.util, json, urllib.request, datetime as dt
spec = importlib.util.spec_from_file_location("agentops", "scripts/agentops.py"); a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
STATE = sys.argv[1]
dry = "--apply" not in sys.argv
now = dt.datetime.now(dt.timezone.utc)
def git(*x): return subprocess.run(["git", *x], capture_output=True, text=True)
reg = {}
for f in git("ls-tree", "--name-only", "origin/main", "claims/").stdout.split():
    if f.endswith(".yml"):
        reg[f.split("/")[-1][:-4]] = yaml.safe_load(git("show", "origin/main:" + f).stdout) or {}
def live(d):
    if d.get("status") not in a.CLAIM_ACTIVE: return False
    u = d.get("until")
    return (not u) or dt.datetime.fromisoformat(str(u).replace("Z", "+00:00")) > now
hub = {c["id"]: c for c in json.load(urllib.request.urlopen(urllib.request.Request(STATE, headers={"User-Agent": "curl/8"}), timeout=30))["claims"]}
for cid, d in sorted(reg.items()):
    d.pop("_file", None)
    if live(d) and (cid not in hub or hub[cid].get("servers") != d.get("servers") or hub[cid].get("until") != d.get("until") or hub[cid].get("status") != d.get("status")):
        print("ADD/UPDATE on hub:", cid, d.get("servers"), d.get("by"), d.get("status"), d.get("until"))
        if not dry: a._hub_event("claim", cid, d)
for cid, c in sorted(hub.items()):
    d = reg.get(cid)
    if d is None:
        print("REMOVE from hub (no file in registry):", cid, c.get("servers"), c.get("by"))
        if not dry: a._hub_event("release", cid, {**c, "status": "done", "note": "Removed from the hub by a registry sync: no claim file on agentops main."})
    elif not live(d):
        print("REMOVE from hub (registry:", d.get("status"), "until", d.get("until"), "):", cid, d.get("servers"), d.get("by"))
        if not dry: a._hub_event("release", cid, {**d, "status": d.get("status") if d.get("status") not in a.CLAIM_ACTIVE else "done"})
print("dry run" if dry else "applied")
