"""PC6 is parked. Only offline assignment preparation remains supported."""
import argparse,json
from pathlib import Path
from admission import fingerprint
from design import schedule
from wire import digest

def prepare(stage):
    return dict(design='PC-6',stage=stage,assignments=schedule(stage),assignment_sha256=digest(schedule(stage)),instrument=fingerprint(),native_calls=0,admission='parked_no_decision_value')
def run(config,out,credential):
    raise ValueError('pc6_parked_no_decision_value')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('operation',choices=['prepare','run']);p.add_argument('--stage',default='Q0',choices=['Q0']);p.add_argument('--output',type=Path);a=p.parse_args()
    if a.operation=='run':raise SystemExit('PC6 parked: no native dispatch is supported.')
    if a.output is None:p.error('--output required for offline preparation')
    with a.output.open('x') as f:json.dump(prepare(a.stage),f,indent=2)
    print('Offline assignments prepared; PC6 remains parked, zero native calls.')
