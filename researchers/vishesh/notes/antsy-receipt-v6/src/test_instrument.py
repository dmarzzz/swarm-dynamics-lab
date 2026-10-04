import copy,json,tempfile,unittest
from pathlib import Path
from test_eval import record
from measure import lines_from_tsv
from study import evaluate
from audit import audit
from analyze import analyze

class InstrumentTests(unittest.TestCase):
 def test_tsv_quotes_are_literal_not_multiline_csv(self):
  raw='left\ttop\theight\tconf\ttext\n0\t0\t10\t80\t"\n0\t30\t10\t90\tTOTAL\n60\t30\t10\t90\t100\n'
  rows=lines_from_tsv(raw)
  self.assertEqual([r['text'] for r in rows],['"','TOTAL 100'])

 def fixture(self):
  p=Path(tempfile.mkdtemp(prefix='antsy6-eval-test-'));records=[record(0),record(1,'2.00'),record(2,None)]
  for r in records:r['image_sha256']=str(r['id'])
  rows,s=evaluate(records);(p/'records.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in records));(p/'manifest.json').write_text(json.dumps({'complete':True,'ids':[0,1,2],'ocr_calls':15,'invalid_ocr':0}));(p/'summary.json').write_text(json.dumps(s));(p/'outcomes.json').write_text(json.dumps(rows));return p
 def test_scoring_audit_passes(self):self.assertTrue(audit(self.fixture())['passed'])
 def test_score_mutation_rejected(self):
  p=self.fixture();s=json.loads((p/'summary.json').read_text());s['arms']['agreement']['correct']+=1;(p/'summary.json').write_text(json.dumps(s))
  with self.assertRaises(AssertionError):audit(p)
 def test_duplicate_assignment_rejected(self):
  p=self.fixture();rows=json.loads((p/'outcomes.json').read_text());rows[0]=rows[1];(p/'outcomes.json').write_text(json.dumps(rows))
  with self.assertRaises(AssertionError):audit(p)
 def test_missing_assignment_rejected(self):
  p=self.fixture();rows=json.loads((p/'outcomes.json').read_text());(p/'outcomes.json').write_text(json.dumps(rows[:-1]))
  with self.assertRaises(AssertionError):audit(p)
 def test_reference_unknown_bounds(self):
  r=analyze(self.fixture());self.assertEqual(r['uncertain_reference_bounds']['agreement']['error_rate_bounds'],[1/3,2/3])
 def test_spatial_rows_ignore_annotation(self):
  t='level\tleft\ttop\twidth\theight\tconf\ttext\n5\t0\t10\t30\t10\t90\tTOTAL\n5\t100\t11\t30\t10\t80\t100\n5\t0\t40\t30\t10\t70\tCASH\n'
  r=lines_from_tsv(t);self.assertEqual(r[0]['text'],'TOTAL 100');self.assertEqual(r[1]['text'],'CASH')
if __name__=='__main__':unittest.main()
