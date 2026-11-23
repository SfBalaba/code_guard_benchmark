"""Аудит синтетики CAT-2.x (Belladonna03, S049, Qwen2.5-Coder-14B) для решения о train v0.

Только чтение: данные берутся через `git show <ref>:<path>` из origin/feat/data_CAT-2.{1,2,3,4}
(рабочее дерево не переключается), test — из generation-pipeline/data/test. Команды не исполняются.

Гейты:
  1. независимость от test: ручная карта сценарий -> test seed draft (SCENARIO_MAP ниже, составлена
     чтением всех 140 сценариев и 80 TEST-CAT-2.x seed drafts), поиск test-строк в промптах,
     exact + near-dup (char-4-gram Jaccard как cgen/neardup.py) по ядру и по развёрнутой команде
     против data/test и отдельно против test-пулов CAT-2 (discussion/archive/POOL_RECONSIDERATION).
  2. метки: проверяется наличие контракта меток (pair_inputs.source/contrast, флаги source_run).
  3. выход: identical sides -> dedup по маскированному ядру -> near-dup внутри -> cap семейства
     -> exact/near vs test; калибровка порога на CAT-2.

Выход: runs/cat2_s049/{audit.json, scenario_map.jsonl, leak_hits.jsonl, prompt_hits.jsonl,
threshold_calibration.json, yield_survivors.jsonl}. report.md пишется отдельно по audit.json.
"""
import argparse
import itertools
import json
import random
import re
import shlex
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

PIPE = Path(__file__).resolve().parents[1]
REPO = PIPE.parent
sys.path.insert(0, str(PIPE))
from cgen.dedup import normalize  # noqa: E402
from cgen.io import read_commands  # noqa: E402
from cgen.neardup import jaccard, shingles  # noqa: E402

SUBS = ["2.1", "2.2", "2.3", "2.4"]
SYN = "synthetic/qwen14b_s049_2026-11-15"
POOLS = ["discussion/reserve.jsonl", "discussion/other.jsonl", "archive/archive.jsonl",
         "overnight_2026-11-01/POOL_RECONSIDERATION.jsonl"]
DEMO_RE = re.compile(r"demo-[0-9a-f]{8}")
B64_RE = re.compile(r"[A-Za-z0-9+/]{16,}={0,2}")
THR = 0.5
K = 4

# Карта сценарий -> TEST seed draft (overnight_2026-11-01/test_seed_drafts.jsonl, TEST-CAT-2.x-NN)
# и/или test family_id (provenance.jsonl). Уровень:
#   S — тот же нестандартный механизм/краевой случай, что в test seed draft или test family;
#   P — вариант/частичное совпадение механизма с test seed draft;
#   G — шаблон или контрпример самого гайдлайна (общий источник для test и train, неизбежно);
#   N — в test seed drafts / families аналога не найдено.
SCENARIO_MAP = {
    "2.1": {
        "G01": ("G", "T14 force-dry-run; guideline counterexample push -f --dry-run"),
        "G02": ("G", "guideline counterexample --force-with-lease"),
        "G03": ("S", "T13 plus-partial"), "G04": ("N", ""),
        "G05": ("S", "T10 matching-colon; family matching-refspec"),
        "G06": ("S", "T15 push-all"), "G07": ("S", "T16 push-tags"),
        "G08": ("P", "T13 plus-partial (branch+tag variant)"),
        "G09": ("G", "guideline template --mirror; T07 mirror"),
        "G10": ("P", "T07 mirror via config"), "G11": ("N", ""),
        "G12": ("P", "T10 matching via push.default"), "G13": ("N", ""),
        "G14": ("S", "T03 lease-tracking"), "G15": ("S", "T03 lease-tracking"),
        "G16": ("S", "T04 lease-explicit"), "G17": ("S", "T05 lease-empty"),
        "G18": ("P", "T09 atomic-lease (multi-ref lease)"), "G19": ("P", "T13/T09 partial protection"),
        "G20": ("S", "T06 force-overrides-lease"), "G21": ("S", "T06 force-overrides-lease; family force-overrides-lease"),
        "G22": ("N", ""), "G23": ("P", "T03 lease + includes"), "G24": ("P", "T04 lease-explicit + includes"),
        "G25": ("P", "T09 atomic"), "G26": ("N", ""),
        "G27": ("P", "families ssh-url-force/ssh-url-plus"),
        "G28": ("P", "family configure-remote-then-force"), "G29": ("P", "family configure-remote-then-force"),
        "G30": ("N", ""), "G31": ("P", "T14 force-dry-run multi-ref"), "G32": ("S", "T08 mirror-preview"),
    },
    "2.2": {
        "G01": ("G", "guideline template reset --hard; T01 hard-head"),
        "G02": ("G", "guideline reset --hard; T02 hard-parent"),
        "G03": ("S", "T04 mixed-index"), "G04": ("S", "T05 restore-index; family reset-index-path"),
        "G05": ("S", "T16 submodule-reset"), "G06": ("N", ""), "G07": ("N", ""),
        "G08": ("S", "T10 checkout-paths"), "G09": ("S", "T10 checkout-paths"),
        "G10": ("G", "guideline template checkout -- .; T10"),
        "G11": ("S", "T09 checkout-forced"), "G12": ("S", "T09 checkout-forced; family checkout-detach"),
        "G13": ("N", ""), "G14": ("N", ""),
        "G15": ("P", "T09 forced switch analogue"), "G16": ("P", "T09 + checkout-detach analogue"),
        "G17": ("P", "T16 submodule"), "G18": ("G", "guideline counterexample restore <one-file>; T06"),
        "G19": ("P", "T06/T07 restore source"), "G20": ("P", "T05 restore-index"),
        "G21": ("S", "T05 restore-index"), "G22": ("N", ""), "G23": ("N", ""), "G24": ("N", ""),
        "G25": ("N", ""), "G26": ("S", "T07 restore-top"), "G27": ("N", ""),
        "G28": ("P", "T16 submodule"), "G29": ("G", "guideline stash drop; T13"),
        "G30": ("S", "families stash-numeric-selector/stash-explicit-entry"),
        "G31": ("G", "guideline stash clear; T14"), "G32": ("N", ""),
        "G33": ("G", "guideline counterexample stash push; T11"),
        "G34": ("S", "family stash-keep-index"), "G35": ("N", ""),
        "G36": ("S", "T12 stash-untracked; family stash-ignored"),
    },
    "2.3": {
        "G01": ("G", "T01 clean-files"), "G02": ("G", "guideline clean -fd; T02"),
        "G03": ("G", "guideline clean -fdx; T03"), "G04": ("G", "guideline clean -fX; T04"),
        "G05": ("S", "T05 clean-double-force"), "G06": ("S", "T05/T11 double force + preview"),
        "G07": ("S", "T06 clean-exclude-file"), "G08": ("S", "T06+T07 exclude file/directory"),
        "G09": ("S", "T08 clean-exclude-negated"), "G10": ("P", "T07 exclude directory"),
        "G11": ("S", "T09 clean-exclude-consumes; test row `git clean -dfe --dry-run`"),
        "G12": ("S", "T09/T10 attached exclude looks like preview"),
        "G13": ("S", "T12 clean-end-options"), "G14": ("S", "T11 clean-force-preview"),
        "G15": ("S", "T15 clean-visible-config; test row `git -c clean.requireForce=false clean -d`"),
        "G16": ("P", "T15"), "G17": ("P", "T15"), "G18": ("P", "T15"),
        "G19": ("S", "T16 clean-quiet"), "G20": ("S", "T16 clean-quiet"),
        "G21": ("P", "CAT-2.1 T18 push-C; CAT-2.2 git -C reset"), "G22": ("P", "CAT-2.1 T18 push-C"),
        "G23": ("P", "CAT-2.2 T19 explicit-worktree"),
        "G24": ("P", "CAT-2.2 T19 explicit-worktree"), "G25": ("S", "T12/T13 pathspec after --"),
        "G26": ("G", "guideline counterexample clean -fd <narrow-path>; T13"),
        "G27": ("P", "T13"), "G28": ("P", "T13"), "G29": ("S", "T12 clean-end-options"),
        "G30": ("P", "T13 + exclude"), "G31": ("N", ""), "G32": ("N", ""),
        "G33": ("S", "T14 clean-interactive"), "G34": ("S", "T14 clean-interactive"),
        "G35": ("S", "T14 clean-interactive"), "G36": ("S", "T19 clean-stdin"),
    },
    "2.4": {
        "G01": ("G", "guideline rm -rf .git; T01"), "G02": ("S", "T02 remove-gitfile"),
        "G03": ("P", "T01 remove-git"), "G04": ("P", "T01 remove-git"),
        "G05": ("N", ""), "G06": ("N", ""), "G07": ("N", ""), "G08": ("N", ""),
        "G09": ("G", "guideline deletion of refs"), "G10": ("G", "guideline deletion of objects"),
        "G11": ("P", "T17 pack-inspection contrast"), "G12": ("N", ""), "G13": ("N", ""),
        "G14": ("N", ""), "G15": ("N", ""), "G16": ("P", "T02 worktree link"),
        "G17": ("G", "guideline update-ref -d; T06 delete-local-ref"), "G18": ("P", "T06"),
        "G19": ("P", "T06"), "G20": ("N", "(read-only symbolic-ref in test only)"),
        "G21": ("S", "T08 bulk-update-ref"), "G22": ("S", "T08 bulk-update-ref"),
        "G23": ("G", "guideline reflog expire --expire=now --all; T03"),
        "G24": ("S", "T04 expire-unreachable"), "G25": ("S", "T05 reflog-delete-entry"),
        "G26": ("S", "family expire-rewrite-preview"), "G27": ("S", "T09 immediate-prune"),
        "G28": ("G", "guideline gc --prune=now; T09/T10"), "G29": ("G", "guideline counterexample git gc; T11"),
        "G30": ("P", "families *repack*prune"), "G31": ("N", ""), "G32": ("N", ""),
        "G33": ("S", "T06 delete-local-ref"), "G34": ("N", ""),
        "G35": ("S", "T10 expire-plus-gc; family mixed-reflog-retention"),
        "G36": ("S", "T14 lost-found"),
    },
}


def git_show(ref, path):
    return subprocess.run(["git", "-C", str(REPO), "show", f"{ref}:{path}"], check=True,
                          capture_output=True, text=True).stdout


def jsonl(text):
    return [json.loads(x) for x in text.splitlines() if x.strip()]


def mask(s):
    return DEMO_RE.sub("demo-X", s)


def unwrap(cmd):
    if cmd.startswith("(\n") and cmd.endswith("\n)"):
        return cmd[2:-2]
    return cmd


def core(p, side):
    argv = p["core_argv"][side] or []
    return " ".join(shlex.quote(a) for a in argv)


class TestIndex:
    """normalize()-строки test и их 4-граммы; поиск max Jaccard с префильтром по длине."""

    def __init__(self, cmds):
        self.exact = {}
        self.items = []
        for c, src in cmds:
            n = normalize(c)
            if not n:
                continue
            if n not in self.exact:
                self.exact[n] = src
                self.items.append((len(n), shingles(c, K), n, src))

    def best(self, cmd):
        n = normalize(cmd)
        sig = shingles(cmd, K)
        L = len(n)
        bj, bt = 0.0, None
        for tl, ts, tn, src in self.items:
            if L and (tl < L * 0.5 or tl > L * 2):
                continue
            j = jaccard(sig, ts)
            if j > bj:
                bj, bt = j, (tn, src)
        return n in self.exact, bj, bt


def load_test():
    cmds = []
    for p in sorted((PIPE / "data" / "test").rglob("*")):
        if p.suffix in (".csv", ".jsonl") and p.is_file():
            for c in read_commands(p):
                cmds.append((c, str(p.relative_to(PIPE / "data" / "test"))))
    return cmds


def load_pools():
    cmds = []
    for s in SUBS:
        ref = f"origin/feat/data_CAT-{s}"
        for f in POOLS:
            try:
                for r in jsonl(git_show(ref, f"CAT-{s}/{f}")):
                    if r.get("command"):
                        cmds.append((r["command"], f"CAT-{s}/{f}"))
            except subprocess.CalledProcessError:
                pass
        for f in ["overnight_2026-11-01/history/commands.csv"]:
            pass  # уже в data/test
    return cmds


def load_syn():
    data = {}
    for s in SUBS:
        ref = f"origin/feat/data_CAT-{s}"
        base = f"CAT-{s}/{SYN}"
        data[s] = {
            "ref_sha": subprocess.run(["git", "-C", str(REPO), "rev-parse", ref], check=True,
                                      capture_output=True, text=True).stdout.strip(),
            "pairs": jsonl(git_show(ref, f"{base}/pairs.jsonl")),
            "inputs": jsonl(git_show(ref, f"{base}/pair_inputs.jsonl")),
            "rejections": jsonl(git_show(ref, f"{base}/structural_rejections.jsonl")),
            "requests": jsonl(git_show(ref, f"{base}/model_requests.jsonl")),
            "source_run": json.loads(git_show(ref, f"{base}/source_run.json")),
        }
    return data


def label_contract(d):
    """Есть ли контракт меток: непустые source/contrast в pair_inputs или флаги source_run."""
    nonempty = sum(1 for r in d["inputs"] if r.get("source") or r.get("contrast"))
    keys = Counter(k for r in d["inputs"] for k in r)
    sr = d["source_run"]
    return {"pair_inputs_nonempty_source_or_contrast": nonempty, "pair_inputs_keys": sorted(keys),
            "safety_labels_assigned": sr.get("safety_labels_assigned"),
            "semantic_validation": sr.get("semantic_validation"),
            "test_family_independence": sr.get("test_family_independence")}


def prompt_hits(data, test_cmds, min_len=15):
    """Встречается ли нормализованная test-команда подстрокой в user-промпте (маскированном)."""
    texts = set()
    for s in SUBS:
        for r in data[s]["requests"]:
            for m in r["payload"]["messages"]:
                texts.add(normalize(m["content"]))
    blob = "\n".join(sorted(texts))
    hits = []
    seen = set()
    for c, src in test_cmds:
        n = normalize(c)
        if len(n) < min_len or n in seen:
            continue
        seen.add(n)
        if n in blob:
            hits.append({"test_command": n, "test_file": src})
    return hits, len(texts), len(seen)


def calibrate(pairs, rng):
    """Распределения Jaccard на CAT-2: rendered (unwrapped, masked) и ядро (masked)."""
    by = {(p["scenario_id"], p["form_id"]): p for p in pairs}
    scen = sorted({k[0] for k in by})
    forms = sorted({k[1] for k in by})
    sig_r = {k: shingles(mask(unwrap(p["source"])), K) for k, p in by.items()}
    sig_c = {k: shingles(mask(core(p, "source")), K) for k, p in by.items()}
    buckets = defaultdict(list)
    keys = list(by)
    for _ in range(6000):
        a, b = rng.sample(keys, 2)
        same_s, same_f = a[0] == b[0], a[1] == b[1]
        tag = ("same_scenario" if same_s else "diff_scenario") + "/" + ("same_form" if same_f else "diff_form")
        buckets["rendered:" + tag].append(jaccard(sig_r[a], sig_r[b]))
        buckets["core:" + tag].append(jaccard(sig_c[a], sig_c[b]))
    # гарантированно добавить same_scenario/diff_form и diff_scenario/same_form
    for _ in range(3000):
        s = rng.choice(scen)
        fa, fb = rng.sample(forms, 2)
        if (s, fa) in by and (s, fb) in by:
            buckets["rendered:same_scenario/diff_form"].append(jaccard(sig_r[(s, fa)], sig_r[(s, fb)]))
            buckets["core:same_scenario/diff_form"].append(jaccard(sig_c[(s, fa)], sig_c[(s, fb)]))
        f = rng.choice(forms)
        sa, sb = rng.sample(scen, 2)
        if (sa, f) in by and (sb, f) in by:
            buckets["rendered:diff_scenario/same_form"].append(jaccard(sig_r[(sa, f)], sig_r[(sb, f)]))
            buckets["core:diff_scenario/same_form"].append(jaccard(sig_c[(sa, f)], sig_c[(sb, f)]))
    out = {}
    for k, v in sorted(buckets.items()):
        v = sorted(v)
        if not v:
            continue
        out[k] = {"n": len(v), "p10": round(v[len(v) // 10], 3), "median": round(v[len(v) // 2], 3),
                  "p90": round(v[9 * len(v) // 10], 3), "share_ge_0.5": round(sum(x >= THR for x in v) / len(v), 3)}
    return out


def core_pair_spotcheck(units, rng, n=12):
    """Пары разных ядер в зоне 0.4-0.7 — для ручной проверки порога."""
    ex = []
    lst = list(units)
    for _ in range(20000):
        a, b = rng.sample(lst, 2)
        j = jaccard(a["sig"], b["sig"])
        if 0.4 <= j < 0.7 and a["scenario_id"] != b["scenario_id"] or (0.4 <= j < 0.7 and len(ex) < n // 2):
            ex.append({"j": round(j, 3), "a": a["key"], "b": b["key"],
                       "a_scn": a["scenario_id"], "b_scn": b["scenario_id"]})
        if len(ex) >= n:
            break
    return ex


def run(out, thr, cap, core_thr):
    rng = random.Random(49)
    out.mkdir(parents=True, exist_ok=True)
    data = load_syn()
    test_cmds = load_test()
    pool_cmds = load_pools()
    tix = TestIndex(test_cmds)
    pix = TestIndex(pool_cmds)
    cat2_test = TestIndex([(c, s) for c, s in test_cmds if "CAT-2." in s])
    audit = {"thr_vs_test": thr, "core_thr_within_train": core_thr, "k": K, "family_cap": cap, "test_unique": len(tix.items),
             "cat2_test_unique": len(cat2_test.items), "cat2_pool_unique": len(pix.items),
             "refs": {s: data[s]["ref_sha"] for s in SUBS},
             "model": data["2.1"]["source_run"]["model_config"], "subs": {}}

    # Гейт 1: карта сценариев
    smap_rows = []
    for s in SUBS:
        scen = {}
        for r in data[s]["inputs"]:
            scen.setdefault(r["scenario_id"], r)
        for sid, r in sorted(scen.items()):
            lvl, ev = SCENARIO_MAP[s].get(sid, ("?", "unmapped"))
            smap_rows.append({"subcategory": f"CAT-{s}", "scenario_id": sid,
                              "split_group": r["split_group_id"].split("/")[-1], "level": lvl,
                              "test_evidence": ev, "source_task": r["source_task"],
                              "contrast_task": r["contrast_task"]})
    with (out / "scenario_map.jsonl").open("w", encoding="utf-8") as f:
        for r in smap_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    lvl_count = defaultdict(Counter)
    for r in smap_rows:
        lvl_count[r["subcategory"]][r["level"]] += 1
    audit["scenario_levels"] = {k: dict(v) for k, v in lvl_count.items()}

    ph, n_texts, n_test_checked = prompt_hits(data, test_cmds)
    with (out / "prompt_hits.jsonl").open("w", encoding="utf-8") as f:
        for h in ph:
            f.write(json.dumps(h, ensure_ascii=False) + "\n")
    audit["prompt_check"] = {"unique_prompt_texts": n_texts, "test_commands_checked_len_ge_15": n_test_checked,
                             "hits": len(ph)}

    # Гейт 1/3: leak по ядру и развёрнутой команде
    leak_rows = []
    best_cache = {}

    def best(ix, name, text):
        key = (name, text)
        if key not in best_cache:
            best_cache[key] = ix.best(text)
        return best_cache[key]

    calib = {}
    survivors_all = []
    for s in SUBS:
        d = data[s]
        pairs = d["pairs"]
        lv = SCENARIO_MAP[s]
        st = {"seeds": len(d["inputs"]), "structural_rejections": len(d["rejections"]),
              "rendered_pairs": len(pairs)}
        # per-pair leak scan
        scen_max = defaultdict(float)
        for p in pairs:
            p["_leak"] = {}
            for side in ("source", "contrast"):
                variants = {"core": mask(core(p, side)), "rendered": mask(unwrap(p[side]))}
                for vname, text in variants.items():
                    for ixname, ix in (("test", tix), ("cat2_pool", pix)):
                        ex, j, bt = best(ix, ixname, text)
                        p["_leak"][f"{side}:{vname}:{ixname}"] = (ex, j)
                        if ixname == "test":
                            scen_max[p["scenario_id"]] = max(scen_max[p["scenario_id"]], j)
                        if ex or j >= thr:
                            leak_rows.append({"subcategory": f"CAT-{s}", "seed_id": p["seed_id"],
                                              "side": side, "variant": vname, "against": ixname,
                                              "exact": ex, "jaccard": round(j, 3), "text": text,
                                              "nearest": bt[0] if bt else None,
                                              "nearest_file": bt[1] if bt else None})
        st["scenario_max_jaccard_vs_test"] = {k: round(v, 3) for k, v in sorted(scen_max.items())}

        # Гейт 3
        ident_r = [p for p in pairs if p["source"] == p["contrast"]]
        ident_c = [p for p in pairs if p["source"] != p["contrast"]
                   and mask(core(p, "source")) == mask(core(p, "contrast"))
                   and p["declarations"]["source"] == p["declarations"]["contrast"]]
        st["identical_rendered"] = len(ident_r)
        st["identical_core_only"] = len(ident_c)
        bad = {p["seed_id"] for p in ident_r + ident_c}
        live = [p for p in pairs if p["seed_id"] not in bad]
        st["after_identical"] = len(live)
        # уникальные маскированные ядра-пары
        cores = defaultdict(list)
        for p in live:
            key = (mask(core(p, "source")), mask(core(p, "contrast")),
                   json.dumps(p["declarations"], sort_keys=True))
            cores[key].append(p)
        st["unique_core_pairs"] = len(cores)
        st["forms_per_core_pair_median"] = sorted(len(v) for v in cores.values())[len(cores) // 2] if cores else 0
        units = []
        for key, ps in cores.items():
            units.append({"key": key[0] + " ||| " + key[1], "sig": shingles(key[0] + " ||| " + key[1], K),
                          "scenario_id": ps[0]["scenario_id"], "group": ps[0]["split_group_id"].split("/")[-1],
                          "pairs": ps})
        calib[s] = {"distributions": calibrate(pairs, rng), "spot": core_pair_spotcheck(units, rng)}
        # near-dup внутри по ядру-паре (жадно, стабильный порядок по seed_id первой пары)
        units.sort(key=lambda u: u["pairs"][0]["seed_id"])
        # sweep порога внутри train по ядру-паре + примеры по полосам для ручной проверки
        sweep = {}
        for t in (0.5, 0.6, 0.7, 0.8, 0.9):
            ks = []
            for u in units:
                if not any(jaccard(u["sig"], x) >= t for x in ks):
                    ks.append(u["sig"])
            sweep[str(t)] = len(ks)
        st["core_neardup_sweep"] = sweep
        bands = defaultdict(list)
        for _ in range(40000):
            a, b = rng.sample(units, 2) if len(units) > 1 else (units[0], units[0])
            j = jaccard(a["sig"], b["sig"])
            for lo, hi in ((0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.01)):
                if lo <= j < hi and len(bands[f"{lo}-{hi}"]) < 6:
                    bands[f"{lo}-{hi}"].append({"j": round(j, 3), "a": a["key"], "b": b["key"],
                                                "a_scn": a["scenario_id"], "b_scn": b["scenario_id"]})
        calib[s]["bands"] = dict(bands)
        kept_units, kept_sigs, n_near = [], [], 0
        for u in units:
            if any(jaccard(u["sig"], ks) >= core_thr for ks in kept_sigs):
                n_near += 1
                continue
            kept_sigs.append(u["sig"])
            kept_units.append(u)
        st["core_pairs_after_neardup"] = len(kept_units)
        st["core_neardup_dropped"] = n_near

        # vs test: любая сторона, ядро или развёрнутая, exact или >= thr -> вон (только против data/test)
        def leaks(p, ixname="test"):
            return any((v[0] or v[1] >= thr) for k, v in p["_leak"].items() if k.endswith(":" + ixname))

        def leaks_core(p, ixname="test"):
            return any((v[0] or v[1] >= thr) for k, v in p["_leak"].items()
                       if k.endswith(":" + ixname) and ":core:" in k)
        st["rendered_pairs_leaking_test"] = sum(leaks(p) for p in pairs)
        st["rendered_pairs_leaking_test_core_level"] = sum(leaks_core(p) for p in pairs)
        st["rendered_pairs_leaking_cat2_pools"] = sum(leaks(p, "cat2_pool") for p in pairs)

        # выбор пар: из каждого ядра — одна пара с формой, ещё не использованной в сценарии; cap по семейству
        def select(units_in, fam_of, levels):
            fam_n = Counter()
            chosen = []
            used_forms = defaultdict(set)
            for u in units_in:
                if lv[u["scenario_id"]][0] not in levels:
                    continue
                fam = fam_of(u)
                if cap is not None and fam_n[fam] >= cap:
                    continue
                cand = [p for p in u["pairs"] if not leaks(p) and not leaks(p, "cat2_pool")]
                if not cand:
                    continue
                cand.sort(key=lambda p: (p["form_id"] in used_forms[fam], p["form_id"]))
                p = cand[0]
                used_forms[fam].add(p["form_id"])
                fam_n[fam] += 1
                chosen.append(p)
            return chosen

        levels_sets = {"all": set("SPGN"), "excl_S": set("PGN"), "G_N": set("GN"), "N_only": set("N")}
        st["yield"] = {}
        for lname, lset in levels_sets.items():
            for fname, ff in (("scenario", lambda u: u["scenario_id"]), ("split_group", lambda u: u["group"])):
                ch = select(kept_units, ff, lset)
                utils = Counter(x for p in ch for side in ("source", "contrast")
                                for x in [(p["core_argv"][side] or ["?"])[0]])
                st["yield"][f"{lname}/cap_by_{fname}"] = {
                    "pairs": len(ch), "rows": 2 * len(ch),
                    "scenarios": len({p["scenario_id"] for p in ch}),
                    "forms": len({p["form_id"] for p in ch}), "utils": dict(utils)}
                if lname == "all" and fname == "scenario":
                    for p in ch:
                        survivors_all.append({"subcategory": f"CAT-{s}", "seed_id": p["seed_id"],
                                              "scenario_id": p["scenario_id"], "form_id": p["form_id"],
                                              "scenario_level": lv[p["scenario_id"]][0],
                                              "source_command": p["source"], "contrast_command": p["contrast"],
                                              "core_argv": p["core_argv"], "declarations": p["declarations"],
                                              "train_admissible": False,
                                              "why_not": "gate1_unclear_test_independence; no labels"})
        # артефакты
        cmds = [p[side] for p in pairs for side in ("source", "contrast")]
        st["artifacts"] = {"rows": len(cmds),
                           "outer_subshell_wrapper": sum(c.startswith("(\n") and c.endswith("\n)") for c in cmds),
                           "cgb_identifier": sum("cgb" in c for c in cmds),
                           "demo_hex": sum(bool(DEMO_RE.search(c)) for c in cmds),
                           "example_invalid": sum("example.invalid" in c for c in cmds)}
        # грубая эвристика несуществующих/ошибочных опций Git в ядрах (не полный словарь флагов)
        BAD = {"push --preview": r"\bpush\b.*\s--preview\b", "--lease (not a git flag)": r"\s--lease\b",
               "--expected-old": r"--expected-old", "clean --ignored-only": r"--ignored-only",
               "diff/show --no-pager (global opt misplaced)": r"\b(diff|show|ls-files)\b[^|]*--no-pager",
               "config --global write": r"config --global"}
        core_txt = [core(p, side) for p in pairs for side in ("source", "contrast")]
        st["suspicious_core_flags"] = {k: sum(bool(re.search(v, c)) for c in core_txt) for k, v in BAD.items()}
        st["utils_all_rows"] = dict(Counter((p["core_argv"][side] or ["?"])[0]
                                            for p in pairs for side in ("source", "contrast")))
        st["label_contract"] = label_contract(d)
        audit["subs"][f"CAT-{s}"] = st

    with (out / "leak_hits.jsonl").open("w", encoding="utf-8") as f:
        for r in leak_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with (out / "threshold_calibration.json").open("w", encoding="utf-8") as f:
        json.dump(calib, f, ensure_ascii=False, indent=1)
    with (out / "yield_survivors.jsonl").open("w", encoding="utf-8") as f:
        for r in survivors_all:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    lk = Counter((r["subcategory"], r["variant"], r["against"], "exact" if r["exact"] else "near") for r in leak_rows)
    audit["leak_summary"] = {" ".join(k): v for k, v in sorted(lk.items())}
    with (out / "audit.json").open("w", encoding="utf-8") as f:
        json.dump(audit, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in audit.items() if k != "subs"}, ensure_ascii=False, indent=1)[:4000])
    for s, st in audit["subs"].items():
        print(s, {k: v for k, v in st.items() if k not in ("scenario_max_jaccard_vs_test", "label_contract")})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(PIPE / "runs" / "cat2_s049"))
    ap.add_argument("--thr", type=float, default=THR)
    ap.add_argument("--cap", type=int, default=5)
    ap.add_argument("--core-thr", type=float, default=0.8,
                    help="порог near-dup внутри train по маскированной ядро-паре (калибровка на CAT-2, см. report)")
    a = ap.parse_args()
    run(Path(a.out), a.thr, a.cap, a.core_thr)


if __name__ == "__main__":
    main()
