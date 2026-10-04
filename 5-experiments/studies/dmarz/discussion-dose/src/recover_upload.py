"""Repair artifact transport only; never repeat model calls or change the failed outcome."""
import argparse
from pathlib import Path
from artifacts import publish_artifacts

def main():
    p=argparse.ArgumentParser();p.add_argument('run');a=p.parse_args()
    if not a.run.startswith('discussion-dose/') or '/' in a.run.split('/',1)[1] or '..' in a.run:
        p.error('expected a discussion-dose run ID')
    import swarm_report as sr
    out=Path(__file__).resolve().parent.parent/'results'/'episodes'/a.run.replace('/','__')
    if not out.exists():p.error('existing local run output required')
    record=sr.get_run(a.run)
    if record.get('status') not in ('failed','done'):p.error('wait for a terminal run before repairing uploads')
    run=sr.Run(a.run,'discussion-dose',record.get('params',{}))
    publish_artifacts(run,out)
    run.log('Repaired artifact transport using compression/chunks. Original execution and terminal status preserved; no episodes rerun.')
    print('Artifacts repaired; original run status preserved')
if __name__=='__main__':main()
