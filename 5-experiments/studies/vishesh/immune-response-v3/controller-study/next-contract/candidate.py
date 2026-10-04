"""Offline candidate only. No dispatcher, credentials or model calls."""
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import controller
DEFINITIONS=' Field definitions: probe_current means cached_probe.epoch equals current_epoch. failed_service names only a process explicitly non-live in a CURRENT probe; return none for stale liveness or a configuration-only problem. fault is configuration if any visible catalog compatibility check is false; otherwise unknown when the probe is stale; otherwise runtime if a process is non-live; otherwise none. These fields describe evidence, not confidence that a previous action succeeded.'
def diagnosis_request(observation):
 req=controller.diagnosis_request(observation);req['instructions']+=DEFINITIONS;return req
def action_request(case,observation,diagnosis,order):
 if order not in ('action_first','justification_first'):raise ValueError('unknown_order')
 req=copy.deepcopy(controller.action_request(case,observation,diagnosis));keys=['action_id','reason'] if order=='action_first' else ['reason','action_id'];s=req['response_schema'];s['properties']={k:s['properties'][k] for k in keys};s['required']=keys
 req['instructions']+=' Give a brief evidence-based justification, not extended deliberation. Serialize fields in this order: '+', '.join(keys)+'.'
 return req
