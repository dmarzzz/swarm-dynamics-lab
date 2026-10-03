#!/bin/sh
# fd-add: file an output into artifacts/ (see ../SKILL.md). Runs from anywhere inside the project.
set -eu
d="$(cd "$(dirname "$0")" && pwd)"
root="$d"
while [ "$root" != "/" ] && [ ! -f "$root/project.yaml" ]; do root="$(dirname "$root")"; done
exec python3 "$root/.flightdeck/fd.py" add "$@"
