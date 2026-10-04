import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
STUDY=HERE.parents[1]
REPO=HERE.parents[5]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

original=load('comparison_original',STUDY/'src/fields.py')
repaired=load('comparison_repaired',STUDY/'trace-repair-v2/fields.py')

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write(path,value):
    import os
    path=Path(path)
    # Snapshot publication is exclusive. Mutable native journal is separate.
    with path.open('x') as f:
        json.dump(value,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
