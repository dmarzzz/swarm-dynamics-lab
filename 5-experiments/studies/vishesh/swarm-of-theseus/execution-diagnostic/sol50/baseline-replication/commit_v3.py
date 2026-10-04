"""Offline candidate only; active and historical runtimes do not import this module."""
import copy
import selection_v2 as previous,contract

def wire(phase,family,packet):
 body=previous.wire(phase,family,packet)
 if phase=='commit':
  body=copy.deepcopy(body)
  body['messages'][0]['content']=('This call only commits private institutional memory; it does not decide operational cases. '
   'Return exactly one JSON object with exactly one top-level key, "note", and no other keys. '
   'The note object must contain exactly one key, "witnesses", whose value is two distinct current roster position strings other than your own position. '
   'Do not include a decision, actions, explanation, or surrounding prose. '
   'Use only delivered inheritance and current observations. If no inheritance or current evidence is delivered, choose an uninformed provisional pair from the roster; do not invent access to history. '
   'Return shape: {"note":{"witnesses":["position_A","position_B"]}}.')
 contract.validate_wire(body)
 return body
