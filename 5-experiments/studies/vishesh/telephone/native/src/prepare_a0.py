"""Export original sources and evaluator gold separately; no model calls."""
import json,sys
from pathlib import Path
from contract import assignments,sha
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'t1/src'))
from fixtures import cases
if __name__=='__main__':
 base=Path(__file__).resolve().parents[1]/'a0';c=cases()
 packet={'stage':'A0','scope':'original authored development cases','cases':[{'id':x['id'],'records':x['records']} for x in c],'assignments':assignments([x['id'] for x in c])}
 gold={x['id']:x['gold'] for x in c}
 (base/'packet.json').write_text(json.dumps(packet,indent=2)+'\n');(base/'gold.json').write_text(json.dumps(gold,indent=2)+'\n')
 print(json.dumps({'packet_sha256':sha(packet),'gold_sha256':sha(gold),'assigned':len(packet['assignments'])}))
