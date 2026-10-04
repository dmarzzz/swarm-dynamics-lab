#!/usr/bin/env python3
"""Attach a dated correction without overwriting the hub's earlier cohort artifacts."""
import json,os,sys,time
from pathlib import Path
import factory as f
sys.path.insert(0,os.environ.get('SWARM_REPORT_PATH',str(Path.home()/'projects/swarm-labs-agentops/hub')))
import swarm_report as sr
os.environ['SWARM_SOURCE']='shadow/sol-factory'
for file in sorted((f.ROOT/'hub').glob('*-closed.json')):
    receipt=json.loads(file.read_text());run=receipt['run']
    done=file.with_name(file.stem+'-correction.json')
    if done.exists():continue
    sr.upload(run,f.ROOT/'CORRECTIONS.md','CORRECTIONS-2026-10-04.md')
    f.dump(done,dict(run=run,correction_sha256=f.sha(f.ROOT/'CORRECTIONS.md'),uploaded_at=f.now()))
    time.sleep(.25)
print('correction attachments complete')
