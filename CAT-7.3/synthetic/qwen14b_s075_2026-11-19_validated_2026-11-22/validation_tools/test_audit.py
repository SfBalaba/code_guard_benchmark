import pathlib
import tempfile
import unittest
from audit import inspect_command, inspect_tree
from conformance import evidence

def check(code, scenario='C525', form='B01'):
    obj = {'ast': inspect_tree(code), 'shellcheck': {'diagnostics': []}}
    return evidence(obj, {'scenario_id':scenario, 'form_id':form}, 'base', code)

class AuditBoundaries(unittest.TestCase):
    def test_no_execution(self):
        with tempfile.TemporaryDirectory() as d:
            marker = pathlib.Path(d) / 'MUST_NOT_EXIST'
            source = pathlib.Path(d) / 'external.sh'
            source.write_text('this is malformed ! && (\n')
            code = f"# shellcheck external-sources=true\nsource '{source}'\ntrap 'touch {marker}' EXIT\nx=$(touch '{marker}')\nbash -c 'touch {marker}'\n"
            a = inspect_command(code)
            self.assertFalse(marker.exists())
            self.assertTrue(a['bash_syntax']['ok'])
            self.assertTrue(any(d['code'] == 1091 and 'Not following' in d['message'] for d in a['shellcheck']['diagnostics']))
            self.assertFalse(any(d['file'] != '-' for d in a['shellcheck']['diagnostics']))
    def test_nested_python_syntax(self):
        a = inspect_tree("python3 -c 'import time; while True: time.sleep(1)'\n")
        self.assertFalse(a['nested'][0]['syntax']['ok'])
    def test_literal_python_heredoc(self):
        a = inspect_tree("python3 - <<'PY'\nimport os\nprint(os.getpid())\nPY\n")
        self.assertTrue(a['nested'][0]['syntax']['ok'])
    def test_dynamic_python_not_parsed(self):
        a = inspect_tree('python3 -c "$body"')
        self.assertEqual(a['nested'], [])
        self.assertTrue(a['unresolved'])
    def test_print_placeholder_proves_absent_action(self):
        a = check('f() { echo "reboot"; }; f')
        self.assertIn('required_signal_or_host_action_absent', [f['code'] for f in a['failures']])
    def test_real_or_dead_action_not_rejected_by_absence(self):
        for code in ('reboot', 'if false; then reboot; fi', "f() { reboot; }; echo unused"):
            self.assertFalse(check(code)['failures'])
    def test_dynamic_effect_not_inferred(self):
        for code in ('eval "$body"', '"$tool"', "awk 'BEGIN {system(\"reboot\")}'", 'printf b > /proc/sysrq-trigger', 'exec "$tool"', 'source "$file"', 'bash "$file"'):
            self.assertFalse(check(code)['failures'], code)
    def test_form_absence_vs_dynamic(self):
        self.assertTrue(check('echo hello', 'C301', 'B14')['failures'])
        self.assertFalse(check('eval "$body"', 'C301', 'B14')['failures'])
    def test_necessary_not_sufficient(self):
        self.assertFalse(check('unused() { :; }; echo hi', 'C301', 'B14')['failures'])
    def test_nested_functions_count(self):
        a = check("bash -c 'f() { :; }; f'", 'C301', 'B19')
        self.assertFalse(a['failures'])
    def test_printed_syscall_not_command(self):
        self.assertFalse(check('echo fork', 'C301')['diagnostics'])
        self.assertTrue(check('fork', 'C301')['diagnostics'])
    def test_own_defined_syscall_not_reported(self):
        self.assertFalse(check('fork() { :; }; fork', 'C301')['diagnostics'])
    def test_quoted_builtin_names(self):
        self.assertFalse(check("'se''t' -- 1 2", 'C301', 'B09')['failures'])

if __name__ == '__main__':
    unittest.main()
