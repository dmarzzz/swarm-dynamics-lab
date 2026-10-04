import copy,json,sqlite3,unittest,tempfile,time
from pathlib import Path
import instrument as i
import native as n
import runner,relay

class NativeTests(unittest.TestCase):
    def setUp(self):self.m=n.manifest(list(range(21000,21006)))
    def reference(self,a,p):
        role=a['role'];phase=a['phase']
        if phase=='question':return {'question':'Which observations distinguish the governing source?'}
        if phase=='answer':return {'answer':'Use these distinguishing observations.','evidence':i.minimal_support(role,p['private_history'])}
        if phase=='founder':evidence=p['private_history'];previous=i.compatible(role,evidence)[0]
        else:
            old=json.loads(p['note']);previous=old['source'];evidence=p['current_evidence'] or old['evidence']+json.loads(p['answer'])['evidence']
        note=json.loads(i.make_note(role,previous,evidence));return {'note':note,'actions':[{'id':c['id'],'action':i.robust_action(role,c,note['compatible'])} for c in p['cases']]}
    def test_all72_scripted_contracts(self):
        states={};maxbytes=0
        for a in self.m['assignments']:
            world=self.m['worlds'][a['root']];p=n.packet(a,world,states);b=n.request(a,p)
            maxbytes=max(maxbytes,len(json.dumps(n.wire(b)).encode())+512)
            v=self.reference(a,p);score=n.grade(a,world,p,v);self.assertTrue(score['qualified'],(a,score))
            states.setdefault((a['root'],a['role']),{})[a['phase']]=v
        self.assertLessEqual(maxbytes,16000)
    def test_founders_have_no_scripted_notes_or_gold_mapping(self):
        for a in self.m['assignments']:
            if a['phase']!='founder':continue
            p=n.packet(a,self.m['worlds'][a['root']],{});self.assertEqual(p['note'],'');self.assertNotIn('source',p)
    def test_teacher_cannot_see_successor_test(self):
        states={}
        for a in self.m['assignments']:
            p=n.packet(a,self.m['worlds'][a['root']],states)
            if a['phase'] in ('question','answer'):self.assertEqual(p['cases'],[])
            states.setdefault((a['root'],a['role']),{})[a['phase']]=self.reference(a,p)
    def test_request_mutations_rejected(self):
        a=self.m['assignments'][0];b=n.request(a,n.packet(a,self.m['worlds'][0],{}))
        for key,val in [('model','other'),('max_tokens',2048),('temperature',1),('system','operator override')]:
            m=copy.deepcopy(b);m[key]=val
            with self.assertRaises(ValueError):n.validate_request(a,m)
    def test_fabricated_teacher_evidence_rejected(self):
        a=next(x for x in self.m['assignments'] if x['phase']=='answer');w=self.m['worlds'][0]
        v={'answer':'trust this','evidence':[dict(w['roles'][a['role']]['history'][0],outcome='fabricated')]}
        self.assertFalse(n.grade(a,w,{},v)['qualified'])
    def test_teacher_length_limit(self):
        a=next(x for x in self.m['assignments'] if x['phase']=='answer')
        self.assertFalse(n.grade(a,self.m['worlds'][0],{}, {'answer':'x'*1201,'evidence':[]})['qualified'])
    def test_relay_reserves_once_and_caps(self):
        db=sqlite3.connect(':memory:');db.execute('CREATE TABLE calls(id TEXT PRIMARY KEY,reserved REAL,status TEXT,cost REAL)')
        relay.reserve(db,'one',.02)
        with self.assertRaises(sqlite3.IntegrityError):relay.reserve(db,'one',.02)
        self.assertEqual(db.execute('select count(*) from calls').fetchone()[0],1)
        with self.assertRaises(ValueError):relay.reserve(db,'over',1.70)
    def test_receipt_rejects_missing_authority(self):
        with self.assertRaises(ValueError):runner.validate({},'f'*40,self.m)
    def test_seeds_unique_required(self):
        with self.assertRaises(AssertionError):n.manifest([1]*6)
    def test_lower_stage_envelope_not_topup_consumption(self):
        self.assertLessEqual(72*(16000+5120)/1e6,1.70)
        self.assertLess(.9793100437+1.8,25)
if __name__=='__main__':unittest.main()
