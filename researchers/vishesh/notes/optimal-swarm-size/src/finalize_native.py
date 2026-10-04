"""Import completed native evidence into the shared finalizer's repository boundary."""
import hashlib,json,re,shutil
from pathlib import Path

def inventory(root):
    result=[]
    for path in sorted(Path(root).rglob('*')):
        if path.is_symlink():raise ValueError('evidence_symlink')
        if path.is_file():
            result.append({'path':path.relative_to(root).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    if not result:raise ValueError('evidence_empty')
    return result

def import_evidence(repo,output,attempt):
    repo=Path(repo).resolve();output=Path(output)
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*',attempt):raise ValueError('invalid_attempt')
    if output.is_symlink() or not output.is_dir():raise ValueError('invalid_evidence_root')
    before=inventory(output)
    identity=hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest()
    target=repo/'data/experiment-operations/native-imports/optimal-swarm-size'/attempt/identity
    if not target.exists():
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copytree(output,target)
    if inventory(target)!=before or inventory(output)!=before:raise ValueError('evidence_changed_during_import')
    return target.relative_to(repo).as_posix()
