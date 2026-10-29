import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import integrate_dataset as integrator
import validate_dataset as validator


class DatasetPipelineTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.candidates = self.make_pair("alpha")
        self.sources = [{
            "source_id": "fixture-source",
            "url": "https://example.org/fixture",
            "locator": "fixture example",
            "revision": "fixture-revision",
            "retrieved_at": "2026-10-29",
            "source_type": "documentation",
            "risks": [validator.RISKS[0]],
            "accessibility": "accessible",
            "relevance": "Inert test fixture",
            "commands_present": True,
            "license": "CC0-1.0",
            "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
            "reuse_decision": "permitted",
            "notes": "Local fixture; no network access",
        }]
        self.pending = []
        self.assertEqual(self.errors(), [])

    def make_pair(self, name):
        result = []
        for role, label, command in (
            ("dangerous", "deny", f"echo {name}-danger"),
            ("counterexample", "allow", f"printf '{name}-safe'"),
        ):
            other_role = "counterexample" if role == "dangerous" else "dangerous"
            result.append({
                "candidate_id": f"CAT-3.1-{name}-{role}",
                "row": {
                    "command": command,
                    "description": "Инертный пример для проверки обработки данных",
                    "util": "echo" if role == "dangerous" else "printf",
                    "severity": "high" if role == "dangerous" else "low",
                    "category": validator.CATEGORY,
                    "risk": validator.RISKS[0],
                    "source": "documentation",
                    "seed": "-",
                    "class": label,
                },
                "source_ids": ["fixture-source"],
                "source_locator": "fixture example",
                "evidence_context": "Inert command text for parser tests only",
                "transformations": [],
                "documentation_urls": ["https://example.org/fixture"],
                "tool_version": "fixture-version",
                "label_rationale": "Fixture labels exercise pair validation, not shell safety",
                "scenario_id": "fixture-scenario",
                "role": role,
                "paired_candidate_ids": [f"CAT-3.1-{name}-{other_role}"],
                "synthetic_model": None,
                "status": "accepted",
            })
        return result

    def errors(self):
        rows, provenance = integrator.prepare(self.candidates)
        return validator.validate_bundle(rows, provenance, self.candidates, self.sources, self.pending)

    def write_jsonl(self, relative, records):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records), encoding="utf-8")

    def write_inputs(self):
        self.write_jsonl("data/candidates/CAT-3.1/candidates.jsonl", self.candidates)
        self.write_jsonl("research/sources.jsonl", self.sources)
        self.write_jsonl("data/review/pending.jsonl", self.pending)

    def run_script(self, name):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / name), str(self.root)],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_summary_uses_one_aggregate_target_at_boundaries(self):
        template = self.candidates[0]["row"]
        for total, expected_deficit in ((0, 250), (249, 1), (250, 0), (251, 0)):
            with self.subTest(total=total):
                rows = [
                    dict(template, risk=validator.RISKS[index % len(validator.RISKS)])
                    for index in range(total)
                ]
                report = validator.summary(rows, [])
                self.assertEqual(report["target"], 250)
                self.assertEqual(report["records"], total)
                self.assertEqual(report["deficit"], expected_deficit)
                self.assertEqual(sum(item["total"] for item in report["by_risk"].values()), total)
                for risk_report in report["by_risk"].values():
                    self.assertEqual(set(risk_report), {"total", "class", "severity", "utilities"})
                    self.assertLess(risk_report["total"], 250)
                if total == 250:
                    self.assertEqual([item["total"] for item in report["by_risk"].values()], [50] * 5)

    def test_summary_validity_is_independent_of_target(self):
        rows, provenance = integrator.prepare(self.candidates)
        errors = validator.validate_bundle(rows, provenance, self.candidates, self.sources, [])
        report = validator.summary(rows, errors)
        self.assertTrue(report["valid"])
        self.assertEqual(report["deficit"], 248)
        self.assertEqual(report["errors"], [])

        errors = ["Fixture schema failure"]
        report = validator.summary([rows[0]] * 250, errors)
        self.assertFalse(report["valid"])
        self.assertEqual(report["deficit"], 0)
        self.assertEqual(report["errors"], errors)

    def test_csv_roundtrip_preserves_embedded_newlines_quotes_and_unicode(self):
        self.candidates[0]["row"]["command"] = 'printf \'первая строка\n"вторая", строка\''
        self.candidates[0]["row"]["description"] = 'Описание, с "кавычками"\r\nи новой строкой'
        rows, provenance = integrator.prepare(self.candidates)
        self.assertEqual(self.errors(), [])
        csv_text, provenance_text = integrator.serialize(rows, provenance)
        integrator.persist(self.root, csv_text, provenance_text)
        self.assertEqual(validator.read_csv(self.root / "commands.csv"), rows)
        self.assertEqual(validator.load_jsonl(self.root / "data/processed/provenance.jsonl"), provenance)

    def test_csv_rejects_malformed_quoting(self):
        header = ",".join(validator.FIELDS) + "\n"
        for malformed in (
            'echo "broken,description,echo,high,category,risk,source,-,deny\n',
            '"echo"unexpected,description,echo,high,category,risk,source,-,deny\n',
            '"echo,description,echo,high,category,risk,source,-,deny\n',
        ):
            with self.subTest(record=malformed):
                path = self.root / "commands.csv"
                path.write_text(header + malformed, encoding="utf-8")
                with self.assertRaises(validator.DatasetError):
                    validator.read_csv(path)

    def test_rejects_unknown_provenance_record_indices(self):
        rows, original = integrator.prepare(self.candidates)
        for index in (0, -1, len(rows) + 1, True, "1"):
            with self.subTest(index=index):
                provenance = copy.deepcopy(original)
                provenance[0]["csv_record"] = index
                self.assertTrue(validator.validate_bundle(rows, provenance, self.candidates, self.sources, []))

    def test_rejects_provenance_for_unknown_candidate(self):
        rows, provenance = integrator.prepare(self.candidates)
        provenance[0]["candidate_id"] = "CAT-3.1-missing"
        self.assertTrue(validator.validate_bundle(rows, provenance, self.candidates, self.sources, []))

    def test_rejects_dangling_safe_pair(self):
        rows, provenance = integrator.prepare(self.candidates)
        provenance[0]["paired_csv_records"] = [len(rows) + 1]
        self.assertTrue(validator.validate_bundle(rows, provenance, self.candidates, self.sources, []))
        self.candidates[0]["paired_candidate_ids"] = ["CAT-3.1-missing"]
        with self.assertRaises(validator.DatasetError):
            integrator.prepare(self.candidates)

    def test_rejects_asymmetric_safe_pair_with_otherwise_valid_links(self):
        self.candidates.extend(self.make_pair("beta"))
        self.assertEqual(self.errors(), [])
        self.candidates[0]["paired_candidate_ids"].append(self.candidates[3]["candidate_id"])
        self.assertTrue(self.errors())

    def test_rejects_nonallow_safe_counterpart(self):
        for label in ("ask", "deny"):
            with self.subTest(label=label):
                self.candidates[1]["row"]["class"] = label
                self.assertTrue(self.errors())

    def test_rejects_unknown_source_and_unpermitted_reuse(self):
        self.candidates[0]["source_ids"] = ["missing-source"]
        self.assertTrue(self.errors())
        self.candidates[0]["source_ids"] = ["fixture-source"]
        for decision in ("pending", "forbidden", ""):
            with self.subTest(reuse_decision=decision):
                self.sources[0]["reuse_decision"] = decision
                self.assertTrue(self.errors())

    def test_synthetic_requires_seed_and_model(self):
        candidate = self.candidates[0]
        candidate["row"]["source"] = "synthetic"
        candidate["row"]["seed"] = "fixture-seed"
        candidate["synthetic_model"] = "fixture-model"
        self.assertEqual(self.errors(), [])
        candidate["row"]["seed"] = "-"
        self.assertTrue(self.errors())
        for seed in ("", "   "):
            with self.subTest(seed=seed):
                candidate["row"]["seed"] = seed
                with self.assertRaises(validator.DatasetError):
                    integrator.prepare(self.candidates)
        candidate["row"]["seed"] = "fixture-seed"
        for model in (None, "", "   "):
            with self.subTest(model=model):
                candidate["synthetic_model"] = model
                self.assertTrue(self.errors())

    def test_nonsynthetic_rejects_seed_or_generation_model(self):
        candidate = self.candidates[0]
        candidate["row"]["seed"] = "fixture-seed"
        self.assertTrue(self.errors())
        candidate["row"]["seed"] = "-"
        candidate["synthetic_model"] = "fixture-model"
        self.assertTrue(self.errors())

    def test_pending_accepted_candidate_blocks_integration(self):
        self.pending = [{"candidate_id": self.candidates[0]["candidate_id"], "status": "pending"}]
        self.assertTrue(self.errors())
        self.write_inputs()
        result = self.run_script("integrate_dataset.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "commands.csv").exists())
        self.assertFalse((self.root / "data/processed/provenance.jsonl").exists())
        self.pending[0]["status"] = "resolved"
        self.assertEqual(self.errors(), [])

    def test_integration_excludes_all_nonaccepted_candidates(self):
        expected_rows, expected_provenance = integrator.prepare(self.candidates)
        for status in ("pending", "rejected", "excluded"):
            pair = self.make_pair(status)
            for candidate in pair:
                candidate["status"] = status
            self.candidates.extend(pair)
        self.write_inputs()
        result = self.run_script("integrate_dataset.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(validator.read_csv(self.root / "commands.csv"), expected_rows)
        self.assertEqual(validator.load_jsonl(self.root / "data/processed/provenance.jsonl"), expected_provenance)
        validation = self.run_script("validate_dataset.py")
        self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_integration_rejects_pair_to_nonaccepted_candidate(self):
        self.candidates[1]["status"] = "pending"
        self.write_inputs()
        result = self.run_script("integrate_dataset.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "commands.csv").exists())
        self.assertFalse((self.root / "data/processed/provenance.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
