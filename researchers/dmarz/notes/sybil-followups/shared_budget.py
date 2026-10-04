"""USD 60 owner-approved sub-budget shared by both follow-up workers.

Settled calls count actual charges. In-flight or unknown-cost requests retain their
entire conservative reservation. No credentials or transport metadata are stored.
"""
import fcntl
import json
import os
from pathlib import Path

CAP_MICRO_USD = 60_000_000
MAX_RESERVATIONS = 5_600


class SharedBudgetError(RuntimeError):
    pass


class SharedBudget:
    def __init__(self, path, study):
        if study not in ('sybil-budget-api', 'sybil-newcomer-api'):
            raise SharedBudgetError('unknown_followup')
        self.path = Path(path)
        self.study = study
        self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)

    def transact(self, event=None):
        with self.path.open('a+', encoding='utf-8') as stream:
            os.chmod(self.path, 0o600)
            fcntl.flock(stream, fcntl.LOCK_EX)
            stream.seek(0)
            events = [json.loads(line) for line in stream if line.strip()]
            reservations, settled = {}, {}
            for e in events:
                key = (e['study'], e['call_id'])
                if e['type'] == 'reserve':
                    if key in reservations:
                        raise SharedBudgetError('corrupt_duplicate_reservation')
                    reservations[key] = e['micro_usd']
                elif e['type'] == 'settle':
                    if key not in reservations or key in settled:
                        raise SharedBudgetError('corrupt_settlement')
                    settled[key] = e['micro_usd']
                else:
                    raise SharedBudgetError('corrupt_event')
            def status():
                actual = sum(settled.values())
                held = sum(v for k, v in reservations.items() if k not in settled)
                return {'actual_usd': actual / 1e6, 'held_usd': held / 1e6,
                        'committed_usd': (actual + held) / 1e6,
                        'reservations': len(reservations), 'settled': len(settled),
                        'cap_usd': CAP_MICRO_USD / 1e6}
            if event:
                event = dict(event, study=self.study)
                key = (self.study, event['call_id'])
                amount = event['micro_usd']
                if type(amount) is not int or amount < 0:
                    raise SharedBudgetError('invalid_budget_amount')
                if event['type'] == 'reserve':
                    if key in reservations:
                        raise SharedBudgetError('duplicate_shared_call')
                    committed = sum(settled.values()) + sum(v for k, v in reservations.items() if k not in settled)
                    if len(reservations) >= MAX_RESERVATIONS or committed + amount > CAP_MICRO_USD:
                        raise SharedBudgetError('shared_followup_budget_exhausted')
                    reservations[key] = amount
                elif event['type'] == 'settle':
                    if key not in reservations or key in settled:
                        raise SharedBudgetError('invalid_shared_settlement')
                    if amount > reservations[key]:
                        raise SharedBudgetError('shared_reservation_bound_breached')
                    settled[key] = amount
                else:
                    raise SharedBudgetError('invalid_shared_event')
                stream.seek(0, 2)
                stream.write(json.dumps(event, sort_keys=True) + '\n')
                stream.flush()
                os.fsync(stream.fileno())
            return status()

    def reserve(self, call_id, micro_usd):
        return self.transact({'type': 'reserve', 'call_id': call_id, 'micro_usd': int(micro_usd)})

    def settle(self, call_id, micro_usd):
        return self.transact({'type': 'settle', 'call_id': call_id, 'micro_usd': int(micro_usd)})
