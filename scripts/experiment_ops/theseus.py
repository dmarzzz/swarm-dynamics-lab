"""Small adapter over the unchanged Theseus v2 instrument. No automatic resume.

Metadata is allowlisted. Operator context is never part of an experimental request.
Native network/credential use occurs only inside run(), after native admission.
"""
from contextlib import ExitStack, closing, contextmanager, redirect_stderr, redirect_stdout
import hashlib
import importlib
import json
import math
import os
import platform
import re
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time

STUDY = 'researchers/vishesh/notes/swarm-of-theseus/v2'
STAGES = ('S0', 'S0-repair', 'S1')
MODULES = ('analyze', 'domain', 'engine', 'preflight', 'presentation', 'provider', 'runner', 'render')
CONFIG_KEYS = {'model', 'input_rate', 'output_rate', 'max_output_tokens', 'max_input_bytes',
               'pricing_verified_epoch', 'source_commit', 'plan_url', 'plan_sha256',
               'pre_run_review_url', 'pre_run_review_sha256', 'prospective_repair_review_url'}
NATIVE_RECEIPT_KEYS = {'experiment', 'source_commit', 'exclusive_claim_verified', 'claim_id', 'host',
                'verified_epoch', 'claim_until_epoch', 'reserved_usd', 'max_calls',
                'authority_allocation_id', 'owner_authorization_ref'}

RECEIPT_KEYS = NATIVE_RECEIPT_KEYS | {'approved_account_verified',
    'native_budget_ledger', 'minimum_prior_reserved_calls', 'minimum_prior_reserved_usd'}
# Owner waived researcher review for this Vishesh-owned study. Retain truthful
# historical fields when supplied; neither absence nor a failed historical review
# creates a researcher approval gate. Owner approval of an updated run is separate.
OPTIONAL_RECEIPT_KEYS = {'researcher_review_passed', 'researcher_review_ref'}

NATIVE_SAFE_CODES = frozenset({
    'clean_source_required', 'allocation_experiment_mismatch', 'allocation_source_mismatch',
    'fresh_exclusive_claim_required', 'stale_deployment_verification', 'claim_too_short',
    'new_fifteen_dollar_reservation_required', 'owner_budget_authority_required',
    'config_source_mismatch', 'matching_source_qualification_required', 'prospective_repair_review_required',
    'wrong_experiment', 'immutable_v2_plan_required', 'registered_plan_revision_mismatch',
    'public_plan_hash_mismatch', 'registered_tldr_missing', 'condition_tldr_missing',
    'required_plan_section_missing', 'immutable_pre_run_review_required', 'pre_run_review_hash_mismatch',
    'pre_run_review_blocked', 'public_document_too_large', 'unqualified_model_or_price',
    'prompt_bounds_mismatch', 'pricing_verification_expired', 'credential_missing',
    'allocation_ledger_mismatch', 'allocation_exhausted', 'wall_or_claim_limit',
    'input_bound_exceeded', 'stage_already_attempted_no_invisible_reruns', 'hub_event_not_acknowledged',
})


class AdapterError(ValueError):
    """Only fixed, public-safe codes may be used as messages."""


def _fail(code):
    raise AdapterError(code)


def _hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def _path(root, path):
    root = Path(root).resolve()
    value = Path(path)
    value = root / value if not value.is_absolute() else value
    for candidate in (value, *value.parents):
        if candidate == root: break
        if candidate.is_symlink(): _fail('symlink_input_refused')
    value = value.resolve()
    try:
        value.relative_to(root)
    except ValueError:
        _fail('path_outside_repository')
    return value


def _study(root, entry):
    if entry.get('study_path') != STUDY or entry.get('adapter') != 'theseus-v2':
        _fail('study_adapter_mismatch')
    return _path(root, STUDY)


def _json(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        _fail('invalid_json_input')


def _head(root):
    result = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True)
    head = result.stdout.strip()
    if result.returncode or len(head) != 40 or any(c not in '0123456789abcdef' for c in head):
        _fail('source_revision_unavailable')
    return head


@contextmanager
def _native(root, entry, module='runner'):
    """Isolate legacy bare imports; never import a different study's provider."""
    base = _study(root, entry)
    _files(root, entry)
    old = {name: sys.modules.pop(name, None) for name in MODULES}
    before = list(sys.path)
    sys.path.insert(0, str(base / 'src'))
    try:
        yield importlib.import_module(module)
    finally:
        sys.path[:] = before
        for name in MODULES:
            sys.modules.pop(name, None)
            if old[name] is not None:
                sys.modules[name] = old[name]


def _files(root, entry):
    base = _study(root, entry)
    paths = sorted((base / 'src').glob('*.py')) + [base / 'PLAN.md']
    if not paths or not all(p.is_file() for p in paths):
        _fail('instrument_missing')
    return {str(p.relative_to(Path(root).resolve())): _hash(_path(root, p)) for p in paths}


def _instrument(root, entry):
    base = _study(root, entry)
    paths = sorted((base / 'src').glob('*.py')) + [base / 'PLAN.md']
    return hashlib.sha256(b''.join(str(p.relative_to(base)).encode() + p.read_bytes() for p in paths)).hexdigest()


def _config(root, path):
    config = _json(_path(root, path))
    if not isinstance(config, dict) or set(config) - CONFIG_KEYS or not CONFIG_KEYS.difference({'prospective_repair_review_url'}).issubset(config):
        _fail('config_fields_not_allowlisted')
    expected = {'model': 'claude-haiku-4-5-20251001', 'input_rate': 1, 'output_rate': 5,
                'max_output_tokens': 900, 'max_input_bytes': 18000}
    if any(config.get(k) != v for k, v in expected.items()):
        _fail('native_model_or_bounds_mismatch')
    prefix = r'https://github\.com/dmarzzz/swarm-lab/blob/[0-9a-f]{40}/' + re.escape(STUDY)
    for name, suffix in (('plan_url', r'/PLAN\.md'), ('pre_run_review_url', r'/reviews/[A-Za-z0-9_-]+-pre\.md'), ('prospective_repair_review_url', r'/reviews/[A-Za-z0-9_-]+-pre\.md')):
        if name in config and (not isinstance(config[name], str) or not re.fullmatch(prefix + suffix, config[name])):
            _fail('immutable_native_document_required')
    for name in ('plan_sha256', 'pre_run_review_sha256'):
        if not isinstance(config[name], str) or not re.fullmatch(r'[0-9a-f]{64}', config[name]):
            _fail('native_document_hash_required')
    epoch = config['pricing_verified_epoch']
    if type(epoch) not in (int, float) or not math.isfinite(epoch) or epoch < 0:
        _fail('pricing_timestamp_invalid')
    if config['source_commit'] != _head(root):
        _fail('config_source_mismatch')
    return config


def _contract(stage):
    return {'status': 'intended_not_observed', 'operator_context_injected': False,
            'model': 'claude-haiku-4-5-20251001', 'temperature': 0,
            'request_fields': ['instructions', 'observation'],
            'context_renderer': 'src/presentation.py',
            'initialization': 'fresh world and empty private notebook/feedback; scenario history or explicit-rule ceiling',
            'memory': 'private notebook <=700 characters; inherited archive <=2400 characters; native scheduled feedback',
            'pairing': 'shared world seeds; S1 conditions fork the same acquisition checkpoint',
            'stage': stage, 'resume_supported': False,
            'determinism': 'world, schedule and context assembly are seeded; hosted responses are not guaranteed deterministic'}


def describe(root, entry):
    _study(root, entry)
    return {'adapter': 'theseus-v2', 'stages': list(STAGES), 'native_dispatch_available': True,
            'resume_supported': False, 'qualification_required_for': ['S1'],
            'initialization_contract': _contract('S0'),
            'budget': {'native_ledger_env': 'THESEUS_V2_LEDGER', 'existing_ledger_required': True,
                       'cap_usd': 15, 'max_calls': 660, 'unknown_usage': 'full reservation retained'},
            'researcher_review': 'not required by owner direction; historical reviews are not relabeled as passed',
            'trust_boundary': 'Account evidence is an external private attestation; native checks retain the owning agent pre-run assessment, public plan, source and receipt freshness. Owner approval of an updated run is checked separately by the operations layer. The adapter does not inspect the provisioner.'}


def analysis_fingerprint(root, entry):
    """Hash the analysis instrument without constructing future stage assignments."""
    _study(root, entry)
    _files(root, entry)
    return {"instrument_sha256": _instrument(root, entry)}


def validate(root, entry):
    files = _files(root, entry)
    with _native(root, entry) as native:
        counts = {stage: len(native.assignments(stage)) for stage in STAGES}
    return {'status': 'validated_offline', 'native_dispatch_available': True,
            'input_files': files, 'assignment_counts': counts, 'live_admission_checked': False, 'software_tests_executed': False,
            'instrument_sha256': _instrument(root, entry)}


def _evidence_files(source):
    if source.is_symlink() or not source.is_dir(): _fail('invalid_evidence_directory')
    manifest = source / 'manifest.json'
    if manifest.is_symlink() or not manifest.is_file(): _fail('manifest_missing_or_symlinked')
    paths = [manifest]
    for name in ('events', 'calls', 'outcomes'):
        directory = source / name
        if directory.is_symlink(): _fail('symlink_evidence_refused')
        if directory.exists() and not directory.is_dir(): _fail('invalid_evidence_directory')
        for child in directory.rglob('*') if directory.exists() else []:
            if child.is_symlink(): _fail('symlink_evidence_refused')
        for path in sorted(directory.glob('*.json')):
            if not path.is_file() or not path.resolve().is_relative_to(source.resolve()): _fail('invalid_evidence_file')
            paths.append(path)
    return paths


def _copy_evidence(source, target):
    for path in _evidence_files(source):
        output = target / path.relative_to(source)
        output.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        shutil.copyfile(path, output)


def _qualification_files(root, path):
    source = _path(root, path)
    return {str(p.relative_to(Path(root).resolve())): _hash(p) for p in _evidence_files(source)}


def prepare(root, entry, stage, config_path=None, qualification_path=None):
    root = Path(root).resolve()
    if stage not in STAGES:
        _fail('unsupported_stage')
    if config_path is None:
        _fail('native_config_required')
    config_path = _path(root, config_path)
    config = _config(root, config_path)
    if stage == 'S0-repair' and not config.get('prospective_repair_review_url'):
        _fail('prospective_repair_review_required')
    inputs = _files(root, entry)
    inputs[str(config_path.relative_to(root))] = _hash(config_path)
    qualification = None
    if stage == 'S1':
        if qualification_path is None:
            _fail('qualification_required')
        qualification = str(_path(root, qualification_path).relative_to(root))
        inputs.update(_qualification_files(root, qualification))
        q = _recompute(root, entry, _path(root, qualification))
        qm = _json(_path(root, qualification) / 'manifest.json')
        if not q.get('qualification_passed') or qm.get('instrument_sha256') != _instrument(root, entry):
            _fail('matching_source_qualification_required')
    with _native(root, entry) as native:
        assigned = native.assignments(stage)
    calls = sum(len(a['steps']) * (1 if stage.startswith('S0') else 3) for a in assigned)
    worlds = {(a['scenario'], a['seed']) for a in assigned}
    return {'stage': stage, 'config_path': str(config_path.relative_to(root)),
            'config_sha256': _hash(config_path), 'qualification_path': qualification,
            'source_commit': config['source_commit'], 'instrument_sha256': _instrument(root, entry),
            'input_files': inputs, 'assignments': assigned, 'assignment_sha256': _digest(assigned),
            'sample_size_summary': {'independent_unit': 'scenario × world seed', 'worlds': len(worlds),
                                    'scenario_families': 3, 'trajectories': len(assigned),
                                    'primary_worlds': 4 if stage == 'S1' else None, 'planned_calls': calls},
            'cost_envelope': {'maximum_calls': calls, 'maximum_input_bytes_per_call': 18000,
                              'maximum_output_tokens_per_call': 900,
                              'maximum_reserved_usd': round(calls * (18000 + 512 + 900 * 5) / 1e6, 6),
                              'native_study_cap_usd': 15, 'native_study_call_cap': 660,
                              'concurrency': 2, 'automatic_retries': 0,
                              'price_basis': 'native pinned rates; fresh native pricing check still required',
                              'replay_is_new_replication': False},
            'initialization_contract': _contract(stage), 'live_admission_checked': False,
            'resume_supported': False,
            'adapter_runtime': {'python_implementation': platform.python_implementation(), 'python_version': platform.python_version()},
            'dependency_limitation': 'Native src and PLAN are hashed; external swarm_report installation is not independently fingerprinted. Deployment verification remains an operator responsibility.'}


def _ledger(root, receipt, stage):
    # No fallback and no minting a fresh allowance. Native reserve() remains authoritative.
    value = os.environ.get('THESEUS_V2_LEDGER')
    if not value or not Path(value).is_file():
        _fail('existing_native_budget_ledger_required')
    path = Path(value)
    declared = Path(receipt.get('native_budget_ledger', ''))
    declared = declared if declared.is_absolute() else Path(root) / declared
    if not path.is_absolute() or any(p.is_symlink() for p in (path, *path.parents, declared, *declared.parents)):
        _fail('canonical_native_ledger_path_required')
    path = path.resolve()
    if path != declared.resolve():
        _fail('native_budget_ledger_binding_mismatch')
    minimum_calls = receipt.get('minimum_prior_reserved_calls')
    minimum_usd = receipt.get('minimum_prior_reserved_usd')
    if type(minimum_calls) is not int or minimum_calls < 0 or type(minimum_usd) not in (int, float) or not math.isfinite(minimum_usd) or minimum_usd < 0:
        _fail('budget_continuity_floors_required')
    try:
        with closing(sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)) as db:
            row = db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
            deadline = db.execute('SELECT deadline FROM study_limit WHERE id=1').fetchone()
            has_attempts = db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='attempts'").fetchone()
            attempted = db.execute('SELECT 1 FROM attempts WHERE stage=?', (stage,)).fetchone() if has_attempts else None
        if attempted:
            _fail('native_stage_already_attempted')
        if not deadline or type(deadline[0]) not in (int, float) or not math.isfinite(deadline[0]) or deadline[0] <= time.time():
            _fail('native_study_deadline_expired')
        if not row or row[0] != 15 or type(row[1]) not in (int, float) or not math.isfinite(row[1]) or not 0 <= row[1] <= 15 or type(row[2]) is not int or not 0 <= row[2] <= 660:
            _fail('native_budget_ledger_mismatch')
        if row[1] < minimum_usd or row[2] < minimum_calls:
            _fail('native_budget_history_missing')
        if row[1] >= 15 or row[2] >= 660:
            _fail('native_budget_exhausted')
    except AdapterError:
        raise
    except Exception:
        _fail('native_budget_ledger_unreadable')
    return {'reserved_usd': row[1], 'reserved_calls': row[2], 'unknown_usage_policy': 'no refund'}


def _verify_prepared(root, entry, packet):
    if packet.get('stage') not in STAGES or packet.get('source_commit') != _head(root):
        _fail('prepared_source_or_stage_drift')
    for name, digest in packet.get('input_files', {}).items():
        path = _path(root, name)
        if not path.is_file() or _hash(path) != digest:
            _fail('prepared_input_drift')
    current = prepare(root, entry, packet['stage'], packet['config_path'], packet.get('qualification_path'))
    if current != packet:
        _fail('prepared_packet_drift')
    return _config(root, packet['config_path'])


def _observed_contexts(result_path):
    _evidence_files(result_path)
    rows = []
    finishes = {p.name.replace('-finished.json', '') for p in (result_path / 'calls').glob('*-finished.json')}
    for path in sorted((result_path / 'calls').glob('*-started.json')):
        record = _json(path)
        request = record.get('request', {})
        if set(request) != {'instructions', 'observation'} or not isinstance(request['observation'], dict):
            _fail('context_receipt_shape_invalid')
        if type(record.get('call')) is not int or record['call'] < 1 or type(record.get('input_bytes')) is not int or not 0 <= record['input_bytes'] <= 18000 or not isinstance(record.get('exact_user_text'), str) or not isinstance(request['instructions'], str):
            _fail('context_receipt_scalar_invalid')
        rows.append({'call': record['call'], 'request_sha256': _digest(request),
                     'system_sha256': _digest(request['instructions']),
                     'rendered_user_sha256': _digest(record['exact_user_text']),
                     'input_bytes': record['input_bytes'],
                     'finished_receipt_present': path.name.replace('-started.json', '') in finishes})
    return {'status': 'observed_native_predispatch_journal',
            'limitation': 'Records serialized context before transport; a started journal alone does not prove provider delivery.',
            'operator_context_injected_by_adapter': False, 'calls': rows}


def _write(path, value):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'w') as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')


def run(root, entry, packet, receipt_path, output_path):
    root = Path(root).resolve()
    config = _verify_prepared(root, entry, packet)
    receipt = _json(_path(root, receipt_path))
    if not isinstance(receipt, dict) or not RECEIPT_KEYS.issubset(receipt) or set(receipt) - (RECEIPT_KEYS | OPTIONAL_RECEIPT_KEYS):
        _fail('receipt_fields_not_allowlisted')
    if receipt.get('approved_account_verified') is not True:
        _fail('external_account_attestation_missing')
    for name in ('authority_allocation_id', 'owner_authorization_ref'):
        if not isinstance(receipt.get(name), str) or not receipt[name].strip():
            _fail('allocation_authority_reference_missing')
    for name in ('verified_epoch', 'claim_until_epoch', 'reserved_usd'):
        if type(receipt.get(name)) not in (int, float) or not math.isfinite(receipt[name]) or receipt[name] < 0:
            _fail('receipt_numeric_field_invalid')
    if type(receipt.get('max_calls')) is not int or receipt['max_calls'] < 0:
        _fail('receipt_numeric_field_invalid')
    _ledger(root, receipt, packet['stage'])
    native_receipt = {k: receipt[k] for k in NATIVE_RECEIPT_KEYS}
    output = _path(root, output_path)
    if output.exists():
        _fail('fresh_output_required')
    output.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    previous_cwd = Path.cwd()
    previous_umask = os.umask(0o077)
    try:
        os.chdir(root)
        # Suppress legacy transport/library diagnostics before they can enter transcripts.
        with ExitStack() as stack:
            qualification = None
            if packet.get('qualification_path'):
                qualification = Path(stack.enter_context(tempfile.TemporaryDirectory(prefix='theseus-qualification-')))
                original = _path(root, packet['qualification_path'])
                _copy_evidence(original, qualification)
                for path in _evidence_files(original):
                    if _hash(qualification / path.relative_to(original)) != packet['input_files'][str(path.relative_to(root))]:
                        _fail('qualification_snapshot_drift')
            with open(os.devnull, 'w') as sink, redirect_stdout(sink), redirect_stderr(sink):
                with _native(root, entry) as native:
                    result = native.run(config, native_receipt, packet['stage'], output, qualification)
        _write(output / 'ops-initialization-contract.json', packet['initialization_contract'])
        _write(output / 'ops-observed-contexts.json', _observed_contexts(output))
        return {'status': 'completed', 'exit_code': 0,
                'qualification_passed': result.get('qualification_passed'),
                'scientific_status': 'consult_saved_analysis', 'resume_supported': False}
    except Exception as error:
        # Only literal native codes are exported, never arbitrary transport/provider text.
        code = str(error)
        reason = code if code in NATIVE_SAFE_CODES else 'native_admission_or_execution_failed'
        return {'status': 'ambiguous' if output.exists() else 'blocked', 'exit_code': 1,
                'reason': reason, 'resume_supported': False}
    finally:
        os.umask(previous_umask)
        if output.is_dir():
            output.chmod(0o700)
            for filename, value in (('ops-initialization-contract.json', packet['initialization_contract']),):
                if not (output / filename).exists():
                    try: _write(output / filename, value)
                    except Exception: pass
            if not (output / 'ops-observed-contexts.json').exists():
                try: _write(output / 'ops-observed-contexts.json', _observed_contexts(output))
                except Exception: pass
        os.chdir(previous_cwd)


def _recompute(root, entry, source):
    """Native summarizer writes summary.json; use scratch so source evidence is immutable."""
    with tempfile.TemporaryDirectory(prefix='theseus-report-') as tmp:
        target = Path(tmp)
        _evidence_files(source)
        manifest = _json(source / 'manifest.json')
        if manifest.get('stage') not in STAGES:
            _fail('unsupported_saved_stage')
        _write(target / 'manifest.json', {'stage': manifest['stage'], 'assignments': manifest['assignments']})
        for name in ('events', 'calls', 'outcomes'):
            (target / name).mkdir()
            for path in (source / name).glob('*.json'):
                shutil.copyfile(path, target / name / path.name)
        with _native(root, entry, 'analyze') as analyzer:
            return analyzer.summarize(target)


def report(root, entry, result_path, output_path):
    source = _path(root, result_path)
    target = _path(root, output_path)
    if target.exists():
        _fail('fresh_report_output_required')
    summary = _recompute(root, entry, source)
    manifest = _json(source / 'manifest.json')
    # Never export raw manifest config/receipt, provider errors, prompts or arbitrary keys.
    safe = {'stage': manifest['stage'], 'evidence_type': 'saved_native_evidence',
            'report_recomputed_without_model_calls': True, 'source_evidence_modified': False,
            'recorded_events': summary['recorded_events'], 'expected_events': summary['expected_events'],
            'audit_mismatch_count': len(summary['audit_mismatches']),
            'qualification_passed': summary.get('qualification_passed'),
            'call_accounting': summary['call_accounting'],
            'primary_conservative_difference': summary.get('primary_conservative_difference'),
            'primary_bounds': summary.get('primary_bounds'),
            'useful_signal_threshold_met': summary.get('useful_signal_threshold_met')}
    def finite(value):
        if isinstance(value, dict): return all(finite(v) for v in value.values())
        if isinstance(value, list): return all(finite(v) for v in value)
        return not isinstance(value, float) or math.isfinite(value)
    if not finite(safe):
        _fail('nonfinite_saved_summary')
    observed = _observed_contexts(source)
    target.mkdir(mode=0o700, parents=True)
    _write(target / 'summary.json', safe)
    _write(target / 'observed-contexts.json', observed)
    return {'status': 'reported', 'exit_code': 0, 'model_calls': 0,
            'qualification_passed': safe['qualification_passed'],
            'audit_mismatch_count': safe['audit_mismatch_count']}
