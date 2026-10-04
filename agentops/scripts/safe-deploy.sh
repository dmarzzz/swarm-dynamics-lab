#!/usr/bin/env bash
# Deploy without cutting off a running experiment.
#
#   scripts/safe-deploy.sh hub                 # hub code + Caddy + backups on the hub server
#   scripts/safe-deploy.sh reporter            # swarm-report client + heartbeat/flush timer on every server
#   scripts/safe-deploy.sh hub --wait 120      # wait up to 120 min for active runs to finish (default 60)
#   scripts/safe-deploy.sh hub --now           # skip the wait (clients spool, so nothing is lost)
#
# "Active" = any run assigned or running on the hub. Workers on the current client spool their reports
# while the hub restarts, so --now is safe for them; the wait protects workers still on an older client.
set -euo pipefail
cd "$(dirname "$0")/.."
WHAT=${1:?usage: safe-deploy.sh hub|reporter [--wait MIN] [--now]}; shift
WAIT=60; NOW=0; ANY_BRANCH=0
while [ $# -gt 0 ]; do case $1 in --wait) WAIT=$2; shift ;; --now) NOW=1 ;; --allow-branch) ANY_BRANCH=1 ;; *) echo "unknown $1"; exit 2 ;; esac; shift; done
# Deploy only what is on main. Several agents share checkouts, so the working tree may sit on someone's
# branch or hold uncommitted edits; deploying that ships code nobody merged.
git fetch -q origin main
if [ "$ANY_BRANCH" = 0 ]; then
  [ "$(git branch --show-current)" = main ] || { echo "refusing: checkout is on '$(git branch --show-current)', not main (or pass --allow-branch)"; exit 1; }
  if ! git diff --quiet origin/main -- hub ansible || [ -n "$(git status --porcelain -- hub ansible)" ]; then
    echo "refusing: hub/ or ansible/ differ from origin/main (commit+push, or pass --allow-branch):"; git diff --stat origin/main -- hub ansible; git status --short -- hub ansible; exit 1
  fi
fi
: "${SOPS_AGE_KEY_FILE:=$PWD/keys.txt}"; export SOPS_AGE_KEY_FILE
export SWARM_HUB_URL=$(python3 -c "import sys;sys.path.insert(0,'scripts');import agentops as a;print(a.inventory()['all']['vars']['agentops_hub_url'])")
export SWARM_HUB_TOKEN=$(sops -d secrets/hub.sops.env | sed -n 's/^SWARM_HUB_TOKEN=//p')
active() { python3 -c "
import sys; sys.path.insert(0, 'hub'); import swarm_report as sr
rs = [r for r in sr.runs(limit=5000) if r['status'] in ('assigned', 'running')]
print(len(rs)); [print('  ', r['run'], 'on', r.get('host'), 'by', r.get('source'), file=sys.stderr) for r in rs]"; }
if [ "$WHAT" = hub ] && [ "$NOW" = 0 ]; then
  deadline=$(( $(date +%s) + WAIT * 60 ))
  while n=$(active) && [ "$n" != 0 ]; do
    [ "$(date +%s)" -ge "$deadline" ] && { echo "still $n active run(s) after $WAIT min; rerun later or with --now"; exit 1; }
    echo "$(date +%H:%M) waiting: $n active run(s)"; sleep 60
  done
  echo "no active runs; deploying"
fi
case $WHAT in
  hub)      (cd ansible && ansible-playbook playbooks/provision.yml -e target_hosts=bp_hub -t hub) ;;
  reporter) (cd ansible && ansible-playbook playbooks/provision.yml -t reporter) ;;
  *) echo "hub|reporter"; exit 2 ;;
esac
for i in $(seq 30); do curl -sf "$SWARM_HUB_URL/healthz" >/dev/null && { echo "hub healthy"; exit 0; }; sleep 2; done
echo "HUB NOT HEALTHY after deploy: ssh into the hub and run 'journalctl -u swarm-hub -n 50'"; exit 1
