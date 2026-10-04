#!/bin/sh
# One finite worker only. The private claim-checked launcher supplies credentials and ledger.
set -eu
cd "$(dirname "$0")"
exec python3 src/worker.py --hub
