"""A transparent grammar reference and a hash-bound native-response tape."""
from cases import digest

class ExactReference:
    """Only understands the published fixture grammar. It is not Jev."""
    name = 'exact-fixture-reference'
    def __call__(self, phase, packet):
        if phase == 'admission': return 'CHECK'
        t = packet['task']
        evidence = [packet['check_record']] if packet.get('check_record') else packet['records']
        valid = [e for e in evidence if e['scope']==t['scope'] and e['revision']==t['revision'] and 0<=t['now']-e['observed_at']<=t['ttl']]
        if not valid: return 'DEFER'
        latest = max(e['observed_at'] for e in valid)
        labels = set()
        for e in valid:
            if e['observed_at'] != latest: continue
            text = e['text']
            if any(x in text for x in ('severed','test fails','outside the permitted')):labels.add('HOLD')
            elif any(x in text for x in ('span intact','test passes','within the permitted')):labels.add('PROCEED')
            else:labels.add('DEFER')
        return next(iter(labels)) if len(labels)==1 else 'DEFER'

class TapePolicy:
    """Consumes strict native responses keyed by exact request hash, never gold."""
    name = 'jev-response-tape'
    def __init__(self, entries, model_snapshot):
        from jev import validate
        self.entries = {}; self.seen = []; self.snapshot = model_snapshot
        for row in entries:
            k = row['request_sha256']
            if k in self.entries: raise ValueError('duplicate_tape_request')
            self.entries[k] = row
    def __call__(self, phase, packet):
        from jev import request, validate
        req = request(phase,packet); key = digest(req)
        if key not in self.entries: raise ValueError('missing_tape_response')
        row = self.entries[key]
        if row.get('request') != req: raise ValueError('tape_request_mismatch')
        result = validate(row['response'], req, self.snapshot)
        self.seen.append(key)
        return result['action']
