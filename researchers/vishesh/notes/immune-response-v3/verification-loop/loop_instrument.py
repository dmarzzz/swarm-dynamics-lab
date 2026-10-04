"""Offline request construction and scored response validation; no dispatch."""
import importlib.util
import json
from pathlib import Path
import jsonschema
import loop_world as w
from native_provider import wire, validate_wire

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('verification_loop_candidate', ROOT.parent/'controller-study/next-contract/candidate.py')
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)


def request(case, observation, phase, diagnosis=None):
    if phase == 'diagnosis':
        q = candidate.diagnosis_request(observation)
    elif phase == 'action':
        validate_diagnosis(observation, diagnosis)
        # Preserve the model's actual diagnosis, even if wrong.
        q = candidate.action_request(case, observation, diagnosis, 'justification_first')
    else:
        raise ValueError('unknown_phase')
    body = wire(q, 'anthropic/claude-opus-4.6')
    validate_wire(body)
    return q, body


def validate_diagnosis(observation, diagnosis):
    jsonschema.validate(diagnosis, candidate.diagnosis_request(observation)['response_schema'])
    return diagnosis == w.reference.labels(observation)


def validate_action(case, observation, diagnosis, proposal):
    q, _ = request(case, observation, 'action', diagnosis)
    jsonschema.validate(proposal, q['response_schema'])
    if list(proposal) != ['reason', 'action_id']:
        raise ValueError('action_field_order')


def qualification(episode, diagnoses):
    """Require complete observations and diagnosis evidence. No missing-as-pass."""
    trace = episode['trace']
    if len(trace) != 4 or [r['tick'] for r in trace] != [1,2,3,4] or len(diagnoses) != 4:
        raise ValueError('incomplete_or_unordered_episode')
    accuracy = [validate_diagnosis(row['observation'], d) for row,d in zip(trace, diagnoses)]
    return {'architecture_pass':episode['architecture_pass'],
            'diagnoses_correct':sum(accuracy), 'diagnoses_assigned':4,
            'full_model_qualification':episode['proposal_pass'] and all(accuracy),
            'forced_inspections':sum(r['forced_inspection'] for r in trace),
            'voluntary_inspections':sum(r['voluntary_inspection'] for r in trace),
            'proposed_inspections':sum(r['proposed_inspection'] for r in trace)}
