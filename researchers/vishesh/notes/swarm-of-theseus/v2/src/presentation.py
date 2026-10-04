"""Information-preserving tabular interface; no access to evaluator rules or truth."""
import json


def row(c):
    vals = [c['id'], c['service_class'], c['summary'], c['queue']]
    for source in ('probe', 'ledger', 'canary'):
        vals.extend('YES' if c['evidence'][source][key] else 'NO' for key in ('signal', 'fresh'))
    return ' | '.join(vals)


HEADER = 'ID | CLASS | SUMMARY | QUEUE | PROBE signal | PROBE fresh | LEDGER signal | LEDGER fresh | CANARY signal | CANARY fresh'


def present(observation):
    parts = ['COMMAND DOCUMENTATION (semantic action -> valid command):', json.dumps(observation['commands'], sort_keys=True)]
    if 'explicit_current_rule' in observation:
        parts += ['AUTHORITATIVE CURRENT RULE. Apply exactly; do not add conditions:', observation['explicit_current_rule']]
    if observation.get('history'):
        parts += ['LABELED HISTORICAL EXAMPLES. Infer the governing source separately for A and B.', HEADER + ' | ACCEPTED ACTION']
        parts += [row(h['observation']) + ' | ' + h['accepted_action'] for h in observation['history']]
    if observation.get('inherited_record'):
        parts += ['INHERITED RECORD (may be incomplete or obsolete):', observation['inherited_record']]
    if observation.get('private_notebook'):
        parts += ['YOUR PRIOR NOTEBOOK (may need correction):', observation['private_notebook']]
    if observation.get('feedback'):
        parts += ['COMPLETED CASE FEEDBACK. Not answers to current cases.', HEADER + ' | YOUR ACTION | ACCEPTED ACTION']
        parts += [row(h['observation']) + ' | ' + str(h.get('action')) + ' | ' + h['accepted_action'] for h in observation['feedback']]
    parts += ['ROLE: ' + str(observation.get('role', 'single qualification reader')), 'STEP: ' + str(observation['step']), observation.get('feedback_status', ''),
              'CURRENT CASES. Read each row independently. Return exactly these IDs and one valid command per row.', HEADER]
    parts += [row(c) for c in observation['cases']]
    return '\n'.join(parts)
