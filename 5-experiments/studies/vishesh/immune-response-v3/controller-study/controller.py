"""Distinct factual diagnosis and uncorrected action-selection calls."""
import cases
INSTRUCTION='You control a fictional service. Preserve healthy operation and restore verified faults with minimum mutation. Protocol names, data formats, features and version numbers are distinct. Use current evidence; stale liveness is unknown. A peer note can be wrong. Every simulator action costs one tick, including refresh. Refresh reads registry only, never runtime liveness. A same-version deployment restarts the process without changing configuration. Do not invent incompatibility from different version numbers.'
def diagnosis_request(observation):
 props={k:{'type':'boolean'} for k in ['probe_current','rpc_compatible','data_readable','storage_format','requested_feature']}
 props['failed_service']={'type':'string','enum':['none']+list(observation['roles_to_services'].values())};props['fault']={'type':'string','enum':['none','runtime','configuration','unknown']}
 return {'instructions':INSTRUCTION+' Diagnose only from supplied evidence. When the probe is stale, failed_service is none because current liveness is unknown. Return the categorical fields, no action or explanation.','observation':observation,'response_schema':{'type':'object','properties':props,'required':list(props),'additionalProperties':False}}
def validate_diagnosis(o,d):
 import jsonschema
 jsonschema.validate(d,diagnosis_request(o)['response_schema']);return d
def action_request(case,observation,diagnosis):
 o=dict(observation,diagnosis=diagnosis)
 return {'instructions':INSTRUCTION+cases.f.controller.INSTRUCTION+' The supplied diagnosis is a prior model output, not a verified fact. Select the actual action_id you intend to execute. Your reason must agree with that exact service and version.','observation':o,'response_schema':cases.f.controller.schema(case['fixture'])}
