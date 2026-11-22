import unittest
from setup_proof import evidence
class ProofTests(unittest.TestCase):
 def test_direct(self):
  x=evidence('d=$(mktemp -d)\ntouch "$d/file"');self.assertEqual(x['mutation']['path_on_failure'],'/file')
 def test_alias_assignment(self):
  x=evidence('d=$(mktemp -d)\nn=0\np="${d}/file_${n}"\ntouch "$p"');self.assertEqual(x['mutation']['path_on_failure'],'/file_0')
 def test_first_loop_iteration(self):
  self.assertIsNotNone(evidence('d=$(mktemp -d)\nfor i in {1..8}; do\nrm "$d/file_$i"'))
 def test_while(self):self.assertIsNotNone(evidence('d=$(mktemp -d)\nwhile true; do\ntouch "$d/f"'))
 def test_guard(self):self.assertIsNone(evidence('d=$(mktemp -d) || exit\ntouch "$d/f"'))
 def test_errexit(self):self.assertIsNone(evidence('set -e\nd=$(mktemp -d)\ntouch "$d/f"'))
 def test_condition(self):self.assertIsNone(evidence('d=$(mktemp -d)\nif [ -d "$d" ]; then\ntouch "$d/f"'))
 def test_function(self):self.assertIsNone(evidence('f() {\nd=$(mktemp -d)\ntouch "$d/f"\n}'))
 def test_unrelated_absolute(self):self.assertIsNone(evidence('d=$(mktemp -d)\ntouch "/foo"'))
 def test_unknown_command(self):self.assertIsNone(evidence('d=$(mktemp -d)\nvalidate "$d"\ntouch "$d/f"'))
 def test_arithmetic_injection(self):self.assertIsNone(evidence('d=$(mktemp -d)\np="$d/$((1+1))"\ntouch "$p"'))
 def test_inert_literal(self):self.assertIsNone(evidence("cat <<'EOF'\nd=$(mktemp -d)\ntouch \"$d/f\"\nEOF"))
 def test_unknown_variable(self):self.assertIsNone(evidence('d=$(mktemp -d)\ntouch "$d/$unknown"'))
 def test_no_second_loop_iteration(self):self.assertIsNone(evidence('d=$(mktemp -d)\nfor i in {1..8}; do\necho ok\ndone\ntouch "$d/f"'))
if __name__=='__main__':unittest.main()
