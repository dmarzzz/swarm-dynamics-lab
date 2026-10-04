import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from candidates import build,TABLES

class CandidateTests(unittest.TestCase):
    def make(self,root,duplicate=False):
        data={name:[] for name in TABLES}
        data['events']=[{'id':'e','data':{'messageId':'m'}},{'id':'f','data':{'actionType':'CONSOLIDATE','computerUseSessionId':'s'}},{'id':'g','data':{'messageId':'absent'}}]
        data['chat_messages']=[{'id':'m','content':'PRIVATE CANARY\u2028inside JSON'}]
        data['computer_use_sessions']=[{'id':'s','session_goal':'PRIVATE CANARY'}]
        if duplicate:data['chat_messages']*=2
        for name,rows in data.items():
            (root/(name+'.development-prefix.jsonl')).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    def test_metadata_summary_and_private_bundles(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.make(p);result=build(p,p/'out')
            self.assertEqual(result['candidate_join_bundles'],2)
            self.assertEqual(result['joins']['chat_references'],2)
            self.assertEqual(result['validated_cases'],0)
            self.assertNotIn('PRIVATE CANARY',json.dumps(result))
            candidates=json.loads((p/'out/candidates.json').read_text())
            self.assertTrue(all(not c['complete_task'] and c['semantic_gold'] is None for c in candidates))
            self.assertEqual((p/'out/candidates.json').stat().st_mode&0o777,0o600)
    def test_existing_destination_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.make(p)
            with self.assertRaises(FileExistsError):build(p,p)
    def test_duplicate_input_ids_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.make(p,duplicate=True)
            with self.assertRaises(ValueError):build(p,p/'out')

if __name__=='__main__':unittest.main()
