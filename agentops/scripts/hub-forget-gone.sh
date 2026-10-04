#!/usr/bin/env bash
# Tell the hub to forget servers that are no longer in fleet.yml, so a box torn down with `task down`
# does not show as "silent" and trip the /healthz/fleet uptime alert. Run automatically at the end of
# `task down`; safe to run any time. Needs your ssh access to the hub server (everyone with access has it).
set -euo pipefail
cd "$(dirname "$0")/.."
: "${SOPS_AGE_KEY_FILE:=$PWD/keys.txt}"; export SOPS_AGE_KEY_FILE
HUB=$(python3 -c "import sys;sys.path.insert(0,'scripts');import agentops as a;print(a.inventory()['all']['vars']['agentops_hub_url'])")
ME=${AGENTOPS_ME:-$(python3 -c "import sys;sys.path.insert(0,'scripts');import agentops as a;print(a.me())")}
SSH="ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new $ME@${HUB#https://}"
TOKEN=$(sops -d secrets/hub.sops.env 2>/dev/null | sed -n 's/^SWARM_HUB_TOKEN=//p') || true
[ -n "$TOKEN" ] || TOKEN=$($SSH 'sed -n "s/^SWARM_HUB_TOKEN=//p" /etc/swarm/report.env')
GONE=$(SWARM_HUB_URL=$HUB SWARM_HUB_TOKEN=$TOKEN python3 - <<'PY'
import sys; sys.path[:0] = ["hub", "scripts"]
import swarm_report as sr, agentops
fleet = set(agentops.load_fleet())
hosts = [h["host"] for h in sr._call("GET", "/api/v1/state")["hosts"]]
print(" ".join(h for h in hosts if h not in fleet and __import__("re").match(r"^[a-z][a-z0-9-]{1,62}$", h)))
PY
)
if [ -z "$GONE" ]; then echo "hub: no departed servers to forget"; exit 0; fi
echo "hub: forgetting servers no longer in fleet.yml: $GONE"
[ "${1:-}" = "--dry-run" ] && exit 0
IN=$(printf "'%s'," $GONE); IN=${IN%,}
$SSH "sudo -u swarm-hub sqlite3 /var/lib/swarm-hub/hub.db \"DELETE FROM hosts WHERE host IN ($IN);\""
echo "hub: forgot $GONE"
