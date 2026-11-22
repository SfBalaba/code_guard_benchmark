"""Portable stdlib-only integrity/replay check. Never executes dataset commands."""
import collections
import hashlib
import importlib.util
import json
import pathlib
import re
import sys
sys.dont_write_bytecode = True

def sha(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()

def rows(p):
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]

def keyed(items, key):
    out = {x[key]:x for x in items}
    assert len(out) == len(items), ('duplicate',key)
    return out

def validate(root):
    manifest = json.loads((root/'manifest.json').read_text())
    for name, expected in manifest['files_sha256'].items():
        path = root/name
        assert path.resolve().is_relative_to(root.resolve())
        assert sha(path.read_bytes()) == expected, name
    actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    assert actual == set(manifest['files_sha256']) | {'manifest.json'}, actual ^ set(manifest['files_sha256'])
    cat = manifest['subcategory']
    im = keyed(rows(root/'pair_inputs.jsonl'), 'seed_id')
    rm = keyed(rows(root/'model_records.jsonl'), 'request_id')
    qm = keyed(rows(root/'model_requests.jsonl'), 'request_id')
    raw = keyed(rows(root/'model_raw.jsonl'), 'request_id')
    planned = keyed(rows(root/'planned_requests.jsonl'), 'request_id')
    copies = keyed(rows(root/'copy_tasks.jsonl'), 'request_id')
    dm = keyed(rows(root/'validation/pairs.jsonl'), 'seed_id')
    am = keyed(rows(root/'validation/agent_reviews.jsonl'), 'seed_id')
    cm = keyed(rows(root/'validation/command_analysis.jsonl'), 'command_sha256')
    assert set(rm) == set(qm) == set(raw) == set(planned)
    assert not set(rm)&set(copies)
    expected_ids = {sid+'-'+s for sid in im for s in ('base','contrast')}
    assert set(rm)|set(copies) == expected_ids
    assert set(im) == set(dm)
    assert all(x['risk'] == cat for x in list(im.values())+list(rm.values())+list(planned.values())+list(copies.values()))
    assert len(im) == {'CAT-7.1':1296,'CAT-7.3':1295,'CAT-7.5':1295}[cat]
    for rid, r in rm.items():
        q = qm[rid]
        assert sha(json.dumps(q['payload'],ensure_ascii=False,sort_keys=True)) == q['request_sha256'] == r['request_sha256'] == raw[rid]['request_sha256']
        choice = raw[rid]['response']['choices'][0]
        assert choice['message']['content'] == r['content']
        assert choice['finish_reason'] == r['finish_reason']
        assert q['payload']['messages'] == planned[rid]['messages']
        assert planned[rid]['source_prompt_sha256'] == im[r['seed_id']]['prompt_sha256']
        assert r['evaluation_context'] == im[r['seed_id']]['evaluation_context'][r['side']]
    spec = importlib.util.spec_from_file_location('cat7_conformance', root/'validation_tools/conformance.py')
    rules = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rules)
    pm = {}
    for name, status in [('accepted/pairs.jsonl','pass'), ('review/rejected_pairs.jsonl','reject'), ('review/needs_review_pairs.jsonl','needs_review')]:
        for p in rows(root/name):
            sid = p['seed_id']
            assert sid not in pm
            pm[sid] = p
            assert p['validation_status'] == status == dm[sid]['status']
            assert p['subcategory'] == cat
            assert p['evaluation_context'] == im[sid]['evaluation_context']
            assert not p['human_gold'] and not p['semantic_validation'] and not p['labels_assigned']
            assert not {'class','label','severity'}&set(p)
            auto_failure = False
            for side in ('base','contrast'):
                rid = sid+'-'+side
                copied = rid in copies
                record = rm[copies[rid]['depends_on']] if copied else rm[rid]
                code = record['checks']['command']
                assert p[side] == code
                info = dm[sid]['sides'][side]
                assert info['command_sha256'] == sha(code)
                assert info['content_sha256'] == sha(record['content'])
                assert info['context'] == im[sid]['evaluation_context'][side]
                assert info['model_call'] == (not copied)
                analysis = cm[sha(code)]
                ev = rules.evidence(analysis, im[sid], side, code)
                assert ev == dm[sid]['static_conformance'][side]
                fence = re.fullmatch(r'\s*```(?:bash|sh)\s*\n([\s\S]*?)\n```\s*',record['content'])
                auto_failure |= bool(ev['failures']) or not fence or record['content'].count('```') != 2
                auto_failure |= record['finish_reason'] != 'stop' or analysis['bash_syntax']['ok'] is False
                if sid in am:
                    assert am[sid]['command_sha256'][side] == sha(code)
            same = p['base'] == p['contrast']
            if im[sid]['pair_type'] == 'context_only':
                assert same and p['evaluation_context']['base'] != p['evaluation_context']['contrast']
            elif same and p['evaluation_context']['base'] == p['evaluation_context']['contrast']:
                auto_failure = True
            want = 'reject' if auto_failure else (am[sid]['status'] if sid in am else 'needs_review')
            assert status == want, (sid,status,want)
            if status == 'pass':
                assert sid in am and am[sid]['status'] == 'pass'
    assert set(pm) == set(im)
    command_rows = rows(root/'accepted/commands.jsonl')
    assert len(command_rows) == 2*sum(p['validation_status']=='pass' for p in pm.values())
    assert len({x['id'] for x in command_rows}) == len(command_rows)
    for x in command_rows:
        p = pm[x['seed_id']]
        assert p['validation_status'] == 'pass'
        assert x['command'] == p[x['side']]
        assert x['evaluation_context'] == p['evaluation_context'][x['side']]
        assert x['command_sha256'] == sha(x['command'])
    counts = {'pairs':len(im), 'side_instances':2*len(im), 'model_responses':len(rm), 'copy_sides':len(copies),
              'agent_read_pairs':len(am), 'accepted_command_rows':len(command_rows),
              'by_status':dict(collections.Counter(x['status'] for x in dm.values()))}
    assert counts == manifest['counts'], (counts,manifest['counts'])
    return {'status':'pass', 'subcategory':cat, 'counts':counts,
            'payload_files_verified':len(manifest['files_sha256']), 'raw_payload_joins':len(rm),
            'replayed_pair_decisions':len(dm), 'corpus_executions':0}

if __name__ == '__main__':
    print(json.dumps(validate(pathlib.Path(__file__).resolve().parent),ensure_ascii=False,indent=2))
