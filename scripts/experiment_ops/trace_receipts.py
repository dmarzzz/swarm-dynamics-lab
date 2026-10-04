"""Offline trace coverage and byte integrity; never a scientific verdict or dispatcher."""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

KINDS = ('input', 'context', 'response', 'parsed', 'transition', 'grade', 'usage', 'phases', 'stdout', 'stderr')
STATUSES = ('unstarted', 'started', 'valid', 'failed', 'interrupted')
REASONS = ('not_collected', 'not_applicable', 'not_reached', 'legacy_missing')
SHA = re.compile(r'[0-9a-f]{64}')
ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,95}')


class InvalidReceipt(ValueError):
    """Messages are fixed categories, never source data."""


def require(condition):
    if not condition:
        raise InvalidReceipt('invalid_trace_manifest')


def file_digest(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def contained(root, relative):
    require(isinstance(relative, str))
    p = Path(relative)
    require(bool(p.parts) and not p.is_absolute() and '..' not in p.parts)
    current = root
    require(root.is_dir() and not root.is_symlink())
    for part in p.parts:
        current = current / part
        require(not current.is_symlink())
    require(current.resolve().is_relative_to(root.resolve()))
    return current


def retain(directory, content):
    """Store caller-selected experimental bytes privately and durably, without overwrite.

    The caller must exclude credentials/headers/operator history before calling. This
    is retention, not redaction. Call before parsing; retain timeout streams natively.
    """
    directory = Path(directory)
    require(isinstance(content, bytes) and not directory.is_symlink())
    require(not any(p.is_symlink() for p in (directory, *directory.parents)))
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    digest = hashlib.sha256(content).hexdigest()
    destination = directory / digest
    fd, temporary = tempfile.mkstemp(prefix='.receipt-', dir=directory)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, destination)
        except FileExistsError:
            require(not destination.is_symlink() and destination.is_file() and file_digest(destination) == digest)
        dfd = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    finally:
        os.unlink(temporary)
    return {'path': digest, 'sha256': digest, 'bytes': len(content)}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result)
        result[key] = value
    return result


def audit(root, study=None, attempt=None):
    """No paths, raw payloads, arbitrary labels, or exception strings in output.

    An absent/invalid manifest never becomes complete. Requirements are assertions
    by the native adapter; integrity is not an independent completeness attestation.
    """
    root = Path(root)
    try:
        manifest_path = contained(root, 'trace-manifest.json')
        if not manifest_path.exists():
            return {'status': 'unavailable', 'reason': 'trace_manifest_absent'}
        require(manifest_path.is_file() and manifest_path.stat().st_size <= 16 * 1024 * 1024)
        raw = manifest_path.read_bytes()
        m = json.loads(raw, object_pairs_hook=unique_object)
        require(set(m) == {'schema_version', 'study', 'attempt', 'source_sha256', 'config_sha256', 'assignments', 'calls'})
        require(type(m['schema_version']) is int and m['schema_version'] == 1)
        for field in ('study', 'attempt'):
            require(isinstance(m[field], str) and ID.fullmatch(m[field]))
        require(study is None or m['study'] == study)
        require(attempt is None or m['attempt'].lower() == attempt.lower())
        for field in ('source_sha256', 'config_sha256'):
            require(isinstance(m[field], str) and SHA.fullmatch(m[field]))
        require(isinstance(m['assignments'], list) and bool(m['assignments']) and isinstance(m['calls'], list))
        assignments = set()
        for a in m['assignments']:
            require(isinstance(a, dict) and set(a) == {'id', 'unit', 'arm'})
            require(all(isinstance(v, str) and ID.fullmatch(v) for v in a.values()))
            require(a['id'] not in assignments)
            assignments.add(a['id'])
        observed, call_ids = set(), set()
        counts = dict.fromkeys(STATUSES, 0)
        coverage = {k: {'verified': 0, 'missing': 0, 'mismatch': 0, 'not_collected': 0,
                        'not_applicable': 0, 'not_reached': 0, 'legacy_missing': 0} for k in KINDS}
        for c in m['calls']:
            require(isinstance(c, dict) and set(c) == {'assignment', 'call_id', 'status', 'artifacts'})
            require(isinstance(c['assignment'], str) and c['assignment'] in assignments and c['assignment'] not in observed)
            observed.add(c['assignment'])
            require(isinstance(c['status'], str) and c['status'] in STATUSES)
            status = c['status']; counts[status] += 1
            if status == 'unstarted':
                require(c['call_id'] is None and c['artifacts'] == {})
                continue
            require(isinstance(c['call_id'], str) and ID.fullmatch(c['call_id']) and c['call_id'] not in call_ids)
            call_ids.add(c['call_id'])
            require(isinstance(c['artifacts'], dict) and set(c['artifacts']) == set(KINDS))
            for kind, ref in c['artifacts'].items():
                require(isinstance(ref, dict))
                if set(ref) == {'absent'}:
                    require(isinstance(ref['absent'], str) and ref['absent'] in REASONS)
                    # Started calls always need their effective input; valid outputs
                    # cannot opt out of response retention using not-applicable.
                    require(not (ref['absent'] in ('not_applicable', 'not_reached') and
                                 (kind == 'input' or kind == 'response' and status == 'valid')))
                    coverage[kind][ref['absent']] += 1
                    continue
                require(set(ref) == {'path', 'sha256', 'bytes'})
                require(isinstance(ref['sha256'], str) and SHA.fullmatch(ref['sha256']))
                require(type(ref['bytes']) is int and ref['bytes'] >= 0)
                p = contained(root, ref['path'])
                if not p.is_file():
                    coverage[kind]['missing'] += 1
                elif p.stat().st_size != ref['bytes'] or file_digest(p) != ref['sha256']:
                    coverage[kind]['mismatch'] += 1
                else:
                    coverage[kind]['verified'] += 1
        require(observed == assignments)
        missing = sum(v['missing'] + v['not_collected'] + v['legacy_missing'] for v in coverage.values())
        mismatches = sum(v['mismatch'] for v in coverage.values())
        return {'status': 'gaps' if missing or mismatches or counts['started'] else 'verified_declared_coverage',
                'manifest_sha256': hashlib.sha256(raw).hexdigest(), 'assignment_count': len(assignments),
                'distinct_unit_labels': len({a['unit'] for a in m['assignments']}),
                'counts': counts, 'started_count': len(call_ids), 'coverage': coverage,
                'unresolved_started': counts['started'], 'missing_artifacts': missing, 'mismatched_artifacts': mismatches,
                'scope': 'declared_local_bytes_only_not_provider_delivery_or_scientific_validation'}
    except (ValueError, TypeError, KeyError, OSError, RecursionError):
        return {'status': 'invalid', 'reason': 'trace_manifest_or_artifacts_invalid'}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('results', type=Path)
    parser.add_argument('--study', required=True)
    parser.add_argument('--attempt', required=True)
    args = parser.parse_args()
    result = audit(args.results, args.study, args.attempt)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result['status'] == 'verified_declared_coverage' else 1)
