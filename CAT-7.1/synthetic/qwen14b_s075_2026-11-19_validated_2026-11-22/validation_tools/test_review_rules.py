import importlib.util,pathlib,sys,unittest
HERE=pathlib.Path(__file__).resolve().parent
OLD=HERE if (HERE/'audit.py').exists() else HERE.parent/'cat7_synthetic_validation_publication_2026-11-22'
sys.path.insert(0,str(OLD))
from audit import inspect_command
from conformance import evidence as prior_evidence
sys.path.insert(0,str(HERE))
from review_rules import evidence
class Boundaries(unittest.TestCase):
 def failures(self,code,form):
  check=inspect_command(code);seed={'scenario_id':'C301','form_id':form};prior=prior_evidence(check,seed,'base',code)
  return evidence(check,prior,seed,'base',code)
 def test_alias_disabled(self):self.assertTrue(self.failures("alias a='echo x'\na",'B21'))
 def test_alias_enabled(self):self.assertFalse(self.failures("shopt -s expand_aliases\nalias a='echo x'\na",'B21'))
 def test_dynamic_alias_option(self):self.assertFalse(self.failures("o=expand_;o+=aliases\nshopt -s \"$o\"\nalias a='echo x'\na",'B21'))
 def test_nameref_missing(self):self.assertTrue(self.failures('f() { local x=$1; echo "$x"; }; f x','B07'))
 def test_nameref_present(self):self.assertFalse(self.failures('f() { local -n x=$1; echo "$x"; }; a=x; f a','B07'))
 def test_nameref_dynamic_option(self):self.assertFalse(self.failures('f() { local "$opt" x=$1; echo "$x"; }; f a','B07'))
 def test_missing_bash_c(self):self.assertTrue(self.failures('echo x','B32'))
 def test_nested_shell_present(self):self.assertFalse(self.failures("bash -c 'echo x'",'B32'))
 def test_function_chain_not_recursion(self):self.assertTrue(self.failures('a() { b; }; b() { echo x; }; a','B26'))
 def test_real_cycle(self):self.assertFalse(self.failures('a() { b; }; b() { a; }; a','B26'))
 def test_dynamic_call_no_proof(self):self.assertFalse(self.failures('a() { "$fn"; }; fn=a; a','B25'))
 def test_alias_hidden_construct(self):self.assertFalse(self.failures("shopt -s expand_aliases\nalias a='f() { local -n r=x; }; f'\na",'B07'))
 def test_arithmetic_hidden_eval(self):self.assertFalse(self.failures("a='$(echo x)'; echo $((a))",'B32'))
 def test_implicit_first_array_element_valid(self):self.assertFalse(self.failures('a=(echo); "$a" x','B08'))
if __name__=='__main__':unittest.main()
