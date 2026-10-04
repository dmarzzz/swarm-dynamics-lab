"""Frozen configuration: the plan (design.json) plus the dated execution amendment (execution.json).
Both files are read once per process and treated as read-only."""
import functools
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'

ARMS = ('private', 'public', 'never', 'prepare', 'vote')
SHARED_INITIAL_ARMS = ('private', 'public', 'never', 'vote')
COMMUNICATING_ARMS = ('private', 'public', 'never', 'prepare')
REGIMES = ('clean', 'informed_minority', 'correctable_minority')
AGENTS = 5
STAGES = ('s0', 'p0', 's1q', 's1r', 's1l')
STAGE_LABELS = {'s0': 'S0', 'p0': 'P0', 's1q': 'S1-Q', 's1r': 'S1-R', 's1l': 'S1-L'}
# P0: one qualification call on S0 fixture world PROBE_WORLD (never an S1 world), at the frozen model settings.
PROBE_WORLD = 0


@functools.lru_cache(maxsize=None)
def design():
    return json.loads((ROOT / 'design.json').read_text())


@functools.lru_cache(maxsize=None)
def execution():
    return json.loads((ROOT / 'execution.json').read_text())


def stage_config(stage):
    """Counts for one stage. S1 stages come from the plan; S0 is the plan's 60 offline fixtures."""
    if stage == 's0':
        return dict(execution()['s0'])
    if stage not in ('s1q', 's1r', 's1l'):
        raise ValueError('stage not authorized: %r (S2 is closed)' % (stage,))
    for entry in design()['stages']:
        if entry['id'] == stage:
            return dict(entry)
    raise ValueError('stage missing from design.json: %r' % (stage,))


def launch_manifest():
    """Model id, reasoning allowance, per-call output caps and prices: the parameters of one launch.
    Recorded on every hub run, in the journal header and in summary.json."""
    return execution()['launch_manifest']


def phase_caps():
    """Per-call output caps for visible output. The plan's values are the defaults; a launch
    manifest may only change them through a dated amendment."""
    return dict(launch_manifest()['output_token_caps'])


def thinking_budget():
    thinking = launch_manifest()['thinking']
    if thinking['type'] == 'off':
        if thinking['budget_tokens'] != 0:
            raise ValueError('thinking is off but a budget is set')
        return 0
    if thinking['type'] not in ('budget', 'adaptive') or thinking['budget_tokens'] < 1024:
        raise ValueError('thinking must be off, or a budget or adaptive allowance of at least 1024 tokens')
    if thinking['type'] == 'adaptive' and thinking.get('effort') not in ('low', 'medium', 'high', 'xhigh', 'max'):
        raise ValueError('adaptive thinking needs an explicit effort level')
    return thinking['budget_tokens']


def thinking_mode():
    """'off', 'budget' (fixed reasoning budget sent to the API) or 'adaptive' (the model decides how much to
    reason; the allowance only widens max_tokens, and the effort level is sent). Validated by thinking_budget()."""
    thinking_budget()
    return launch_manifest()['thinking']['type']


def seed_stage(stage):
    """The key that names a stage's worlds, call ids and ledger entry. A repeated qualification
    uses a new set, so its 12 worlds are fresh and its calls have their own cap."""
    n = launch_manifest()['qualification_set']
    return stage if stage != 's1q' or n == 0 else 's1q.%d' % n


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


RUNTIME_FILES = ('design.json', 'execution.json', 'experiment.json', 'requirements.txt')
HASH_GROUPS = {
    'prompts': ('prompts.py', 'contexts.py'),
    'generator': ('generate.py', 'seeds.py'),
    'scorer': ('score.py', 'parse.py'),
}


def file_hashes():
    paths = [ROOT / name for name in RUNTIME_FILES] + sorted(SRC.glob('*.py'))
    return {str(p.relative_to(ROOT)): sha256_file(p) for p in paths}


def source_hash():
    """Runtime fingerprint: every Python source file, the plan, the execution amendment,
    the hub registration and the dependency pin. Review notes and results do not change it."""
    return digest(sorted(file_hashes().items()))


def group_hashes():
    out = {}
    for name, files in HASH_GROUPS.items():
        out[name] = digest([(f, sha256_file(SRC / f)) for f in files])
    return out
