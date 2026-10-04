import unittest
from corpus import score

def line(text,x=10,y=10,category='menu.nm'):
    return {'category':category,'words':[{'text':text,'quad':{'x1':x,'x2':x+60,'x3':x+60,'x4':x,'y1':y,'y2':y,'y3':y+10,'y4':y+10}}]}
def word(text,y=10):return {'text':text,'left':10,'top':y,'width':50,'height':10}
class Scoring(unittest.TestCase):
    def test_token_multiplicity(self):
        r=score([line('rice rice soup')],[word('rice soup')],90)
        self.assertAlmostEqual(r['recall'],2/3);self.assertEqual(r['regions'],[2/3,None,None])
    def test_spatial_mismatch(self):
        self.assertEqual(score([line('rice')],[word('rice',50)],90)['recall'],0)
    def test_no_double_assignment(self):
        r=score([line('rice'),line('rice',y=11)],[word('rice')],90)
        self.assertEqual(r['recall'],.5)
    def test_total_exact_and_extra_tokens(self):
        r=score([line('10.000',category='total.total_price')],[word('10.000 extra')],90)
        self.assertEqual(r['recall'],1);self.assertFalse(r['total_field_exact'])
if __name__=='__main__':unittest.main()
