"""Export only public assignment metadata; never materialize transfer roots."""
import argparse
import json
from pathlib import Path
from tasks import qualification_manifest

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    with args.output.open('x') as handle:
        json.dump({'status':'planned; not executed','assignments':qualification_manifest()},handle,indent=2)
        handle.write('\n')
    print('Wrote 80 planned assignments (16 Q-A / 64 Q-B); no model calls.')
