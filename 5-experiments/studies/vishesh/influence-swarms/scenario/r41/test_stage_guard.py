import unittest,sqlite3
from pathlib import Path
class StageGuardTest(unittest.TestCase):
 def setUp(self):
  self.db=sqlite3.connect(':memory:');self.addCleanup(self.db.close);self.db.executescript('CREATE TABLE r41_scope(grant_id TEXT PRIMARY KEY,source TEXT,manifest TEXT);CREATE TABLE r41_work(grant_id TEXT,stage TEXT,root TEXT,node TEXT,attempt TEXT,ordinal INTEGER);CREATE TABLE budget(reserved REAL);INSERT INTO budget VALUES(0);');self.db.executescript((Path(__file__).parent/'stage_guard.sql').read_text());self.db.execute('INSERT INTO r41_scope VALUES(?,?,?)',('R41-3744','source','manifest'));self.db.execute('INSERT INTO r41_stage_authority VALUES(?,?,?,?,?,?,?,?)',('R41-3744','R41-D1','test-authority','source','manifest',84,.478464,1));self.db.commit()
 def dispatch(self,stage,n):
  with self.db:self.db.execute('UPDATE budget SET reserved=reserved+0.005696');self.db.execute('INSERT INTO r41_work VALUES(?,?,?,?,?,?)',('R41-3744',stage,'root',str(n),'attempt',n))
 def test_only_84_diagnostic_and_atomic_rollback(self):
  for n in range(84):self.dispatch('R41-D1',n)
  for stage in ('R41-D1','R41-Q0','R41-E0'):
   with self.assertRaisesRegex(sqlite3.IntegrityError,'stage_not_allocated_or_exhausted'):self.dispatch(stage,85)
  self.assertEqual(self.db.execute('SELECT count(*) FROM r41_work').fetchone()[0],84);self.assertAlmostEqual(self.db.execute('SELECT reserved FROM budget').fetchone()[0],.478464)
 def test_wrong_source_manifest_and_excess_cost(self):
  for column,value in (('source','wrong'),('manifest','wrong'),('maximum_model',.005)):
   with self.db:self.db.execute('UPDATE r41_stage_authority SET source=?,manifest=?,maximum_model=?',('source','manifest',.478464));self.db.execute('UPDATE r41_stage_authority SET '+column+'=?',(value,))
   with self.assertRaisesRegex(sqlite3.IntegrityError,'stage_not_allocated_or_exhausted'):self.dispatch('R41-D1',1)
   self.assertEqual(self.db.execute('SELECT count(*) FROM r41_work').fetchone()[0],0);self.assertEqual(self.db.execute('SELECT reserved FROM budget').fetchone()[0],0)
if __name__=='__main__':unittest.main()
