"""Strong same-input exact parser selects spans; no construction gold."""
from grammar import solve as facts

def solve(actor):
 return {kind:[{'id':f['id'],'quote':None if kind=='sources' and f['status']=='unknown' else f['quote']} for f in rows] for kind,rows in facts(actor).items()}
