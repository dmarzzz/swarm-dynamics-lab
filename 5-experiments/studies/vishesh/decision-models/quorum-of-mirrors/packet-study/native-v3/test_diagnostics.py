import unittest,io,json,urllib.error
from diagnostics import classify_http,LIMIT
class Tests(unittest.TestCase):
 def run_error(self,raw):
  exc=urllib.error.HTTPError('https://example.invalid',400,'bad',{},io.BytesIO(raw))
  try:return classify_http(exc)
  finally:exc.close()
 def test_reflected_secret_never_returned(self):
  r=self.run_error(json.dumps({'error':{'message':'secret-fixture-do-not-echo','metadata':{'error_type':'invalid_request','raw':'secret-fixture-do-not-echo'}}}).encode());self.assertEqual(r['category'],'invalid_request');self.assertNotIn('secret-fixture',json.dumps(r))
 def test_schema_classification(self):
  r=self.run_error(b'{"error":{"metadata":{"raw":"Schema is too complex for compilation."}}}');self.assertEqual(r['category'],'schema_complexity')
 def test_bounded_and_malformed(self):
  r=self.run_error(b'x'*(LIMIT+100));self.assertTrue(r['body_truncated']);self.assertEqual(r['body_bytes_retained_for_hash'],LIMIT);self.assertEqual(r['category'],'unclassified')
 def test_untrusted_category_not_echoed(self):
  r=self.run_error(b'{"error":{"metadata":{"error_type":"secret-fixture"}}}');self.assertEqual(r['category'],'unclassified');self.assertNotIn('secret-fixture',json.dumps(r))
if __name__=='__main__':unittest.main()
