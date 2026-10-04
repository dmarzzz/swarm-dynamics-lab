import hashlib
import json
import subprocess
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
EXP = 'compositional-safety'

def design(): return yaml.safe_load((ROOT/'design.yaml').read_text())
def dump(path, value): Path(path).write_text(json.dumps(value, indent=2, allow_nan=False)+'\n')
def git(*args): return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()
def hashes():
    h = hashlib.sha256()
    for p in sorted((ROOT/'src').glob('*.py')): h.update(p.name.encode()); h.update(p.read_bytes())
    h.update((ROOT/'src/prompt.txt').read_bytes())
    return {'engine_sha256': h.hexdigest(), 'design_sha256': hashlib.sha256((ROOT/'design.yaml').read_bytes()).hexdigest()}

def frozen(attempt):
    p = ROOT/'reviews'/f'{attempt}-pre.md'
    if not p.exists() or 'Status: ready' not in p.read_text(): raise ValueError('pre_run_not_ready')
    git('ls-files', '--error-unmatch', str(p.relative_to(ROOT)))
    if git('status', '--porcelain', '--', 'src', 'design.yaml', 'preregistration.md', str(p.relative_to(ROOT))): raise ValueError('uncommitted_protocol')
    return git('rev-parse', 'HEAD')
