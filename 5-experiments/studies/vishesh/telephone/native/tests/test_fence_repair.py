import sys,json,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from contract import response,MODEL
class FenceRepair(unittest.TestCase):
 def raw(self,text):return {'model':MODEL,'role':'assistant','stop_reason':'end_turn','content':[{'type':'text','text':text}],'usage':{'input_tokens':200,'output_tokens':160}}
 def test_single_wrapper_preserves_returned_text(self):
  obj={'claims':[{'claim':'A prototype may work','status':'unverified','uncertainty':'no test performed','source_ids':['r00-0']}]}
  text=json.dumps(obj)
  for x in (text,'```json\n'+text+'\n```','```\n'+text+'\n```'):
   self.assertEqual(response(self.raw(x),'S')['text'],x)
 def test_no_repair_of_prose_or_malformed_schema(self):
  for text in ('before\n```json\n{}\n```','```json\n{}\n```\nafter','```json\n{}\n```\n```json\n{}\n```','```json\n{"claims":[]}\n```','```python\n{}\n```','```json\n{bad}\n```'):
   with self.assertRaises(ValueError):response(self.raw(text),'S')
if __name__=='__main__':unittest.main()
