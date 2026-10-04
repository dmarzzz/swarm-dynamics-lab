#!/usr/bin/env python3
# Ansible dynamic inventory: hosts come from fleet.yml + generated/*.json.
import os
import sys

script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts", "agentops.py")
os.execv(sys.executable, [sys.executable, script, "inventory"] + sys.argv[1:])
