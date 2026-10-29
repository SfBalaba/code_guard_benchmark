import argparse
import csv
import io
import json
import re
import shlex
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


FIELDS = ("command", "description", "util", "severity", "category", "risk", "source", "seed", "class")
CATEGORY = "CAT-3 Деструкция облачной инфраструктуры и БД"
RISKS = (
    "CAT-3.1 Infrastructure as Code Destruction",
    "CAT-3.2 Cluster & Namespace Deletion",
    "CAT-3.3 Mass Container & Volume Prune",
    "CAT-3.4 Cloud Storage & Database Drop",
    "CAT-3.5 Production Deploy Without Approval",
)
PROVENANCE_FIELDS = (
    "csv_record", "candidate_id", "source_ids", "source_locator", "transformations",
    "documentation_urls", "tool_version", "label_rationale", "scenario_id", "role",
    "paired_csv_records", "synthetic_model",
)
CANDIDATE_FIELDS = (
    "candidate_id", "row", "source_ids", "source_locator", "evidence_context",
    "transformations", "documentation_urls", "tool_version", "label_rationale",
    "scenario_id", "role", "paired_candidate_ids", "synthetic_model", "status",
)
SOURCE_FIELDS = (
    "source_id", "url", "locator", "revision", "retrieved_at", "source_type", "risks",
    "accessibility", "relevance", "commands_present", "license", "license_url",
    "reuse_decision", "notes",
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    re.compile(r"(?i)\b(?:password|passwd|secret_access_key|api_key|access_token)\s*[=:]\s*['\"]?(?!\$|<|REDACTED\b|EXAMPLE\b|PLACEHOLDER\b)[A-Za-z0-9/+_=-]{16,}"),
    re.compile(r"https?://[^\s/:]+:[^\s/@]+@"),
)


class DatasetError(Exception):
    pass


def load_jsonl(path):
    try:
        text = path.read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeError) as error:
        raise DatasetError(f"Cannot read UTF-8 JSONL: {path}") from error
    records = []
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            raise DatasetError(f"Blank JSONL record: {path}:{number}")
        try:
            value = json.loads(line, object_pairs_hook=unique_object)
        except (ValueError, RecursionError) as error:
            raise DatasetError(f"Invalid JSON object: {path}:{number}") from error
        if not isinstance(value, dict):
            raise DatasetError(f"Expected JSON object: {path}:{number}")
        records.append(value)
    return records


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def load_candidates(root):
    result = []
    for path in sorted((root / "data/candidates").glob("CAT-3.*/candidates.jsonl")):
        result.extend(load_jsonl(path))
    return result


def present(value):
    return isinstance(value, str) and bool(value.strip())


def string_list(value, nonempty=False):
    return (isinstance(value, list) and (bool(value) or not nonempty)
            and all(present(item) for item in value)
            and len(value) == len(set(value)))


def web_url(value):
    if not present(value):
        return False
    try:
        parsed = urlparse(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.hostname) and not parsed.username and not parsed.password
    except ValueError:
        return False


def contains_secret(value):
    text = json.dumps(value, ensure_ascii=False)
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def trivial_key(command):
    try:
        tokens = shlex.split(command, posix=False)
    except ValueError:
        return None
    normalized = []
    for token in tokens:
        if re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z][a-z0-9]*)+-[0-9]+", token):
            token = re.sub(r"-[0-9]+$", "-<resource-number>", token)
        normalized.append(token)
    return tuple(normalized)


def validate_rows(rows):
    errors = []
    exact = {}
    normalized = {}
    for index, row in enumerate(rows, 1):
        where = f"CSV data record {index}"
        if not isinstance(row, dict) or set(row) != set(FIELDS):
            errors.append(f"{where}: expected exactly nine named fields")
            continue
        if not all(present(row[field]) for field in FIELDS):
            errors.append(f"{where}: fields must be nonempty strings")
            continue
        if row["category"] != CATEGORY or row["risk"] not in RISKS:
            errors.append(f"{where}: noncanonical category or risk")
        if row["severity"] not in {"critical", "high", "medium", "low"}:
            errors.append(f"{where}: invalid severity")
        if row["class"] not in {"allow", "deny", "ask"}:
            errors.append(f"{where}: excluded or invalid class")
        if row["source"] == "synthetic":
            if row["seed"].strip() == "-":
                errors.append(f"{where}: synthetic seed missing")
        elif row["seed"] != "-":
            errors.append(f"{where}: nonsynthetic seed must be -")
        if not re.search(r"[А-Яа-яЁё]", row["description"]):
            errors.append(f"{where}: Russian description missing")
        if "\x00" in "".join(row.values()):
            errors.append(f"{where}: NUL character forbidden")
        command = row["command"]
        if command in exact:
            errors.append(f"{where}: exact command duplicate of record {exact[command]}")
        else:
            exact[command] = index
        key = trivial_key(command)
        if key is not None and key in normalized and normalized[key][1] != command:
            errors.append(f"{where}: trivial lexical/resource-number variant of record {normalized[key][0]}; review and remove duplication")
        elif key is not None:
            normalized[key] = (index, command)
        if contains_secret(row):
            errors.append(f"{where}: possible secret indicator; inspect privately, value withheld")
    return errors


def index_records(records, field, label, errors):
    indexed = {}
    for number, record in enumerate(records, 1):
        key = record.get(field)
        if not present(key):
            errors.append(f"{label} entry {number}: missing identifier")
        elif key in indexed:
            errors.append(f"{label} entry {number}: duplicate identifier")
        else:
            indexed[key] = record
    return indexed


def validate_bundle(rows, provenance, candidates, sources, pending):
    errors = validate_rows(rows)
    candidate_map = index_records(candidates, "candidate_id", "Candidate", errors)
    source_map = index_records(sources, "source_id", "Source", errors)
    accepted = {key: value for key, value in candidate_map.items() if value.get("status") == "accepted"}
    unresolved = {item.get("candidate_id") for item in pending if isinstance(item.get("candidate_id"), str)
                  and item.get("status") not in {"resolved", "closed", "rejected"}}
    mapped = {}
    seen_candidates = set()
    for position, item in enumerate(provenance, 1):
        where = f"Provenance entry {position}"
        if set(item) != set(PROVENANCE_FIELDS):
            errors.append(f"{where}: wrong provenance fields")
        index = item.get("csv_record")
        if type(index) is not int or not 1 <= index <= len(rows):
            errors.append(f"{where}: invalid one-based data index")
            continue
        if index in mapped:
            errors.append(f"{where}: duplicate data index")
        mapped[index] = item
        candidate_id = item.get("candidate_id")
        if not present(candidate_id):
            errors.append(f"{where}: missing candidate identifier")
            continue
        if candidate_id in seen_candidates:
            errors.append(f"{where}: candidate mapped more than once")
        seen_candidates.add(candidate_id)
        candidate = accepted.get(candidate_id)
        if candidate is None:
            errors.append(f"{where}: candidate is absent or not accepted")
            continue
        if set(candidate) != set(CANDIDATE_FIELDS):
            errors.append(f"{where}: wrong candidate fields")
        row = rows[index - 1]
        if candidate.get("row") != row:
            errors.append(f"{where}: candidate row differs from CSV")
        risk = row.get("risk", "")
        if not candidate_id.startswith(risk.split(" ")[0] + "-"):
            errors.append(f"{where}: candidate ID must have risk prefix followed by hyphen")
        if candidate_id in unresolved:
            errors.append(f"{where}: accepted candidate has unresolved review issue")
        for field in PROVENANCE_FIELDS:
            if field not in {"csv_record", "paired_csv_records"} and item.get(field) != candidate.get(field):
                errors.append(f"{where}: provenance/candidate mismatch for {field}")
        for field in ("source_locator", "tool_version", "label_rationale", "scenario_id"):
            if not present(item.get(field)):
                errors.append(f"{where}: missing {field}")
        if not present(candidate.get("evidence_context")):
            errors.append(f"{where}: missing visible evidence context")
        if not string_list(item.get("transformations")):
            errors.append(f"{where}: transformations must be an explicit list")
        urls = item.get("documentation_urls")
        if not string_list(urls, nonempty=True) or not all(web_url(url) for url in urls):
            errors.append(f"{where}: documentation URLs missing or invalid")
        if row.get("source") == "synthetic":
            if not present(item.get("synthetic_model")):
                errors.append(f"{where}: synthetic model missing")
        elif item.get("synthetic_model") not in (None, ""):
            errors.append(f"{where}: nonsynthetic record declares a generation model")
        ids = item.get("source_ids")
        if not string_list(ids, nonempty=True):
            errors.append(f"{where}: source identifiers missing or invalid")
        else:
            for source_id in ids:
                source = source_map.get(source_id)
                if source is None:
                    errors.append(f"{where}: source identifier not in shared ledger")
                    continue
                if set(source) != set(SOURCE_FIELDS):
                    errors.append(f"{where}: source ledger schema mismatch")
                if source.get("accessibility") != "accessible" or source.get("reuse_decision") != "permitted":
                    errors.append(f"{where}: source is not accessible with permitted reuse")
                if not web_url(source.get("url")) or not web_url(source.get("license_url")):
                    errors.append(f"{where}: source/license URL missing or invalid")
                for field in ("locator", "revision", "retrieved_at", "license", "source_type", "relevance"):
                    if not present(source.get(field)):
                        errors.append(f"{where}: source evidence missing {field}")
                source_risks = source.get("risks")
                if not isinstance(source_risks, list) or not any(value in source_risks for value in (risk, risk.split(" ")[0])):
                    errors.append(f"{where}: source does not cover record risk")
                if source.get("commands_present") is not True:
                    errors.append(f"{where}: source does not attest actual command content")
        if item.get("role") not in {"dangerous", "counterexample"}:
            errors.append(f"{where}: invalid role")
        if item.get("role") == "counterexample" and row.get("class") != "allow":
            errors.append(f"{where}: counterexample must independently be allow")
        if item.get("role") == "dangerous" and row.get("class") not in {"ask", "deny"}:
            errors.append(f"{where}: dangerous record cannot be allow")
        if contains_secret(item) or contains_secret(candidate):
            errors.append(f"{where}: possible secret indicator; value withheld")
    if set(mapped) != set(range(1, len(rows) + 1)):
        errors.append("Provenance does not cover every CSV data record exactly once")
    if seen_candidates != set(accepted):
        errors.append("Accepted candidate set differs from final provenance mappings")
    for index, item in mapped.items():
        where = f"CSV data record {index}"
        pairs = item.get("paired_csv_records")
        if not isinstance(pairs, list) or not pairs or any(type(pair) is not int for pair in pairs):
            errors.append(f"{where}: paired data indices must be a nonempty integer list")
            continue
        if len(pairs) != len(set(pairs)):
            errors.append(f"{where}: duplicate paired data index")
        expected_ids = []
        for pair in pairs:
            other = mapped.get(pair)
            if other is None or pair == index:
                errors.append(f"{where}: invalid or self pair")
                continue
            expected_ids.append(other.get("candidate_id"))
            if (item.get("scenario_id") != other.get("scenario_id")
                    or item.get("role") == other.get("role")
                    or rows[index - 1].get("risk") != rows[pair - 1].get("risk")):
                errors.append(f"{where}: pair must share scenario/risk with opposite roles")
            reverse = other.get("paired_csv_records")
            if not isinstance(reverse, list) or index not in reverse:
                errors.append(f"{where}: pairing is not symmetric")
            if other.get("role") == "counterexample" and rows[pair - 1].get("class") != "allow":
                errors.append(f"{where}: dangerous counterpart is not allow")
        candidate = accepted.get(item.get("candidate_id"))
        if candidate:
            original_pairs = candidate.get("paired_candidate_ids")
            if not string_list(original_pairs, nonempty=True) or set(original_pairs) != set(expected_ids):
                errors.append(f"{where}: paired candidate resolution mismatch")
    for number, source in enumerate(sources, 1):
        if contains_secret(source):
            errors.append(f"Source entry {number}: possible secret indicator; value withheld")
    return errors


def summary(rows, errors):
    def counts(field, selected):
        values = [row.get(field, "invalid") for row in selected]
        return dict(sorted(Counter("[secret indicator withheld]" if contains_secret(value) else value for value in values).items()))
    return {
        "valid": not errors,
        "records": len(rows),
        "target": 250,
        "deficit": max(0, 250 - len(rows)),
        "counts": {field: counts(field, rows) for field in ("risk", "class", "severity", "util")},
        "by_risk": {
            risk: {"total": len(selected),
                   "class": counts("class", selected), "severity": counts("severity", selected),
                   "utilities": counts("util", selected)}
            for risk in RISKS for selected in [[row for row in rows if row.get("risk") == risk]]
        },
        "yellow_zone_ask": sum(row.get("class") == "ask" for row in rows),
        "errors": errors,
        "verification_scope": {
            "performed": "Inert UTF-8, CSV/JSON structure, ledger consistency, pairing, narrow duplicate and secret-indicator checks only.",
            "not_proven": "Bash syntax, command safety, source truth/accessibility/license compatibility, approval, isolation, PII absence, and semantic near-duplicate absence require independent manual review; ledger attestations are not live network verification.",
            "execution": "No dataset command is executed or imported. No shell/client or downloaded code is invoked.",
        },
    }


def validate_csv_quoting(text):
    state = "start"
    for character in text:
        if state == "quoted":
            if character == '"':
                state = "after_quote"
        elif state == "after_quote":
            if character == '"':
                state = "quoted"
            elif character in ",\r\n":
                state = "start"
            else:
                raise DatasetError("CSV has text after a closing quote")
        elif character == '"':
            if state != "start":
                raise DatasetError("CSV has an unescaped quote inside an unquoted field")
            state = "quoted"
        elif character in ",\r\n":
            state = "start"
        else:
            state = "unquoted"
    if state == "quoted":
        raise DatasetError("CSV has an unterminated quoted field")


def read_csv(path):
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8", errors="strict")
        validate_csv_quoting(text)
        records = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except (OSError, UnicodeError, csv.Error) as error:
        raise DatasetError("Cannot read commands.csv as strict UTF-8 CSV") from error
    if not records or records[0] != list(FIELDS):
        raise DatasetError("commands.csv header must match exact nine-field contract")
    if any(len(record) != len(FIELDS) for record in records[1:]):
        raise DatasetError("commands.csv contains a data record with incorrect width")
    stream = io.StringIO(newline="")
    csv.writer(stream).writerows(records)
    if list(csv.reader(io.StringIO(stream.getvalue(), newline=""), strict=True)) != records:
        raise DatasetError("CSV parsed-value roundtrip failed")
    return [dict(zip(FIELDS, record)) for record in records[1:]]


def main():
    parser = argparse.ArgumentParser(description="Validate CAT-3 artifacts as inert text; no Bash execution or semantic safety proof.")
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        rows = read_csv(args.root / "commands.csv")
        errors = validate_bundle(
            rows, load_jsonl(args.root / "data/processed/provenance.jsonl"),
            load_candidates(args.root), load_jsonl(args.root / "research/sources.jsonl"),
            load_jsonl(args.root / "data/review/pending.jsonl"),
        )
        print(json.dumps(summary(rows, errors), ensure_ascii=False, indent=2))
        return 1 if errors else 0
    except (DatasetError, OSError, UnicodeError, TypeError, KeyError, AttributeError, RecursionError) as error:
        message = str(error) if isinstance(error, DatasetError) else "Dataset validation failed; inspect JSON field types and filesystem permissions"
        print(json.dumps({"valid": False, "errors": [message]}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
