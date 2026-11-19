"""Validate publication integrity without executing any corpus command."""
import hashlib
import json
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def validate(root):
    manifest = json.loads((root / 'manifest.json').read_text())
    for name, expected in manifest['files_sha256'].items():
        assert sha((root / name).read_bytes()) == expected, name
    category = manifest['subcategory']
    pairs = load(root / 'pairs.jsonl')
    commands = load(root / 'commands.jsonl')
    rejected = load(root / 'structural_rejections.jsonl')
    contexts = load(root / 'pair_inputs.jsonl')
    records = load(root / 'model_records.jsonl')
    requests = load(root / 'model_requests.jsonl')
    assert all(p['subcategory'] == category for p in pairs + rejected + contexts)
    pm = {p['seed_id']: p for p in pairs}
    rm = {r['request_id']: r for r in records}
    qm = {r['request_id']: r for r in requests}
    im = {p['seed_id']: p for p in contexts}
    assert len(pm) == len(pairs) and len(rm) == len(records) and len(qm) == len(requests)
    assert set(rm) == set(qm) == {sid+'-'+s for sid in im for s in ('source', 'contrast')}
    rejected_ids = {p['seed_id'] for p in rejected}
    assert not set(pm) & rejected_ids
    assert set(pm) | rejected_ids == set(im)
    for rid, record in rm.items():
        request = qm[rid]
        assert record['seed_id'] in im
        assert record['request_sha256'] == request['request_sha256']
        payload_sha = sha(json.dumps(request['payload'], ensure_ascii=False, sort_keys=True).encode())
        assert payload_sha == request['request_sha256']
    cm = {c['id']: c for c in commands}
    assert len(cm) == len(commands) == 2*len(pairs)
    for sid, pair in pm.items():
        for side in ('source', 'contrast'):
            command = cm[sid+'-'+side]
            assert command['subcategory'] == category and command['side'] == side
            assert command['command'] == pair[side]
            assert command['command_sha256'] == sha(pair[side].encode())
            assert command['request_sha256'] == pair['request_sha256'][side] == rm[command['id']]['request_sha256']
            assert command['model_output_sha256'] == sha(rm[command['id']]['content'].encode())
            assert command['status'] == 'draft' and command['semantic_validation'] is False
            assert command['human_gold'] is False and command['labels_assigned'] is False
            assert not {'class', 'severity', 'label'} & set(command)
    unique_pairs = {(p['source'], p['contrast']) for p in pairs}
    counts = dict(seeds=len(contexts), model_responses=len(records), rendered_pairs=len(pairs),
                  command_rows=len(commands), rejected_pairs=len(rejected),
                  identical_side_pairs=sum(p['source'] == p['contrast'] for p in pairs),
                  duplicate_pairs=len(pairs)-len(unique_pairs),
                  unique_distinct_side_pairs=sum(a != b for a,b in unique_pairs))
    assert counts == manifest['counts'], (counts, manifest['counts'])
    return dict(status='pass', subcategory=category, counts=counts,
                files_sha256_verified=len(manifest['files_sha256']), commands_executed=0)


if __name__ == '__main__':
    print(json.dumps(validate(Path(__file__).resolve().parent), ensure_ascii=False))
