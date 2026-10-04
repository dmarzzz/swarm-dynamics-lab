#!/usr/bin/env bash
# Deploy a static front end to Cloudflare Pages with the team token.
#
#   scripts/deploy-pages.sh <dir> <name> [branch]
#   scripts/deploy-pages.sh ./site my-viewer             -> https://swarm-<name>.pages.dev
#
# The token lives only in secrets/cloudflare.sops.env (SOPS, decrypted with your age
# key) and is passed to wrangler through the environment, never written to disk.
# Project names are forced to start with `swarm-` so nobody can overwrite another
# project on the account. Pages sites are PUBLIC; never deploy data or the hub token.
#
# A dir with functions/ (Pages Functions) publishes <dir>/public as the static files and
# compiles <dir>/functions. PAGES_SECRETS="NAME1 NAME2" sets those environment variables
# (taken from this script's environment) as encrypted Pages secrets before deploying.
set -euo pipefail
cd "$(dirname "$0")/.."
DIR=${1:?usage: deploy-pages.sh <dir> <name> [branch]}
NAME=${2:?usage: deploy-pages.sh <dir> <name> [branch]}
BRANCH=${3:-main}
[[ "$NAME" =~ ^[a-z0-9][a-z0-9-]{1,40}$ ]] || { echo "name: lowercase letters, digits, dashes"; exit 1; }
PROJECT="swarm-${NAME#swarm-}"
# wrangler 4 needs Node >= 22. If the node on PATH is older (some distro packages ship 18),
# use the newest nvm-installed node that is new enough.
node_major() { "${1:-node}" -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0; }
if [ "$(node_major)" -lt 22 ]; then
  for bin in $(ls -d "${NVM_DIR:-$HOME/.nvm}"/versions/node/v*/bin 2>/dev/null | sort -V -r); do
    if [ "$(node_major "$bin/node")" -ge 22 ]; then export PATH="$bin:$PATH"; break; fi
  done
  [ "$(node_major)" -ge 22 ] || { echo "wrangler needs Node >= 22 (found $(node --version 2>/dev/null || echo none)); install one, e.g. nvm install 22"; exit 1; }
fi
[ -d "$DIR" ] || { echo "no such dir: $DIR"; exit 1; }
[ -f secrets/cloudflare.sops.env ] || { echo "secrets/cloudflare.sops.env missing: add CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID with: task secrets:edit -- secrets/cloudflare.sops.env"; exit 1; }
: "${SOPS_AGE_KEY_FILE:=$PWD/keys.txt}"; export SOPS_AGE_KEY_FILE
ENV=$(sops -d secrets/cloudflare.sops.env) || { echo "cannot decrypt: your age key must be in people/<you>.yml and synced (task secrets:sync)"; exit 1; }
export CLOUDFLARE_API_TOKEN=$(sed -n 's/^CLOUDFLARE_API_TOKEN=//p' <<<"$ENV")
export CLOUDFLARE_ACCOUNT_ID=$(sed -n 's/^CLOUDFLARE_ACCOUNT_ID=//p' <<<"$ENV")
unset ENV
# Create the project through the Pages API (idempotent). `wrangler pages project create`
# now delegates to Workers, which this Pages-only token is not allowed to do.
API="https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/pages/projects"
if ! curl -sf "$API/$PROJECT" -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" >/dev/null; then
  curl -sf -X POST "$API" -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -H "Content-Type: application/json" \
    -d "{\"name\":\"$PROJECT\",\"production_branch\":\"main\"}" >/dev/null \
    || { echo "could not create Pages project $PROJECT (token expired or missing the Pages permission?)"; exit 1; }
  echo "created Pages project $PROJECT -> https://$PROJECT.pages.dev"
fi
if [ -n "${PAGES_SECRETS:-}" ]; then
  # one PATCH with every secret, so no update replaces another's env_vars map
  BODY=$(python3 -c '
import json, os, sys
names = os.environ["PAGES_SECRETS"].split()
missing = [n for n in names if not os.environ.get(n)]
if missing: sys.exit("PAGES_SECRETS names empty variables: " + " ".join(missing))
env = {n: {"type": "secret_text", "value": os.environ[n]} for n in names}
print(json.dumps({"deployment_configs": {e: {"env_vars": env} for e in ("production", "preview")}}))')
  curl -sf -X PATCH "$API/$PROJECT" -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -H "Content-Type: application/json" \
    --data-binary @- <<<"$BODY" >/dev/null || { echo "could not set Pages secrets ($PAGES_SECRETS)"; exit 1; }
  unset BODY
  echo "set Pages secrets: $PAGES_SECRETS"
fi
if [ -d "$DIR/functions" ]; then
  [ -d "$DIR/public" ] || { echo "$DIR has functions/ but no public/"; exit 1; }
  cd "$DIR" && npx --yes wrangler@4 pages deploy public --project-name "$PROJECT" --branch "$BRANCH" --commit-dirty=true
else
  npx --yes wrangler@4 pages deploy "$DIR" --project-name "$PROJECT" --branch "$BRANCH" --commit-dirty=true
fi
