"""Prepare finite offline proposal or seal private evaluation. Never dispatch."""
import argparse
import hashlib
import json
import os
import random
import secrets
from pathlib import Path
import loop_world as w

ROOT = Path(__file__).resolve().parent

def digest(data):
    return hashlib.sha256(data).hexdigest()


def packet():
    assignments = []
    rng = random.Random(20261004)
    worlds = w.worlds(17001)
    for case in worlds:
        for repeat in (1, 2):
            arms = list(w.ARMS)
            rng.shuffle(arms)
            for arm in arms:
                assignments.append(dict(case=case['id'], repeat=repeat, arm=arm))
    return dict(stage='verification-loop-development', native_dispatch_enabled=False,
                model='anthropic/claude-opus-4.6', model_qualification='pending_native',
                worlds=worlds, assignments=assignments, task_roots=6, branch_worlds=10,
                episodes=40, ticks_per_episode=4, calls_per_tick=2, max_calls=320,
                max_request_usd=.055360, model_max_usd=17.715200,
                prior_reserved_usd=15.524695, current_model_cap_usd=16.877155,
                required_model_cap_usd=33.239895, infrastructure_authorized=False,
                plan_sha256=digest((ROOT / 'PLAN.md').read_bytes()),
                source_sha256={p.name:digest(p.read_bytes()) for p in sorted(ROOT.glob('*.py'))})


def seal(private_path, public_path):
    """Atomic refusal to overwrite. Neither seed nor cases returned to operator."""
    if public_path.exists():
        raise FileExistsError('seal already published')
    seed = secrets.randbelow(2**48) + 2**48
    data = json.dumps({'purpose':'sealed evaluation; no development access',
                       'worlds':w.worlds(seed)}, sort_keys=True).encode()
    fd = os.open(private_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    # No content readback. Hash over exactly the bytes just written.
    metadata = {'sha256':digest(data), 'worlds':10, 'roots':6,
                'opened_for_development':False, 'generated_by':'prepare.py seal',
                'source_sha256':digest(Path(__file__).read_bytes()),
                'generator_sha256':digest((ROOT/'loop_world.py').read_bytes()),
                'limitation':'New random fixtures from shared generator, not independent mechanisms or external validation.',
                'custody':'Private local file; path retained in local operations context only.',
                'evaluation_authorized':False}
    with public_path.open('x') as stream:
        json.dump(metadata, stream, indent=2)
    return metadata


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=['packet','seal'])
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--private', type=Path)
    args = parser.parse_args()
    if args.operation == 'packet':
        with args.out.open('x') as stream:
            json.dump(packet(), stream, indent=2)
    else:
        if args.private is None:
            parser.error('--private required')
        seal(args.private, args.out)
