"""Static validation of a category review package. Dataset commands NEVER executed.
Run: python3 CAT-2.N/audit_v0_2026-10-31/validate.py
"""
import csv,hashlib,json,re,subprocess
from pathlib import Path
FIELDS='command description util severity category risk source seed class'.split()
def jl(p):return list(map(json.loads,p.read_text().splitlines()))
def validate(folder):
 risk=folder.name
 with (folder/'commands.csv').open(newline='') as f:
  reader=csv.DictReader(f);assert reader.fieldnames==FIELDS;rows=list(reader)
 proof=jl(folder/'provenance.jsonl');pairs=jl(folder/'pairs.jsonl');assert len(rows)==len(proof)
 byid={p['id']:(r,p) for r,p in zip(rows,proof)};assert len(byid)==len(rows)
 assert len({r['command'] for r in rows})==len(rows)
 syntax=[]
 for r,p in zip(rows,proof):
  assert set(r)==set(FIELDS) and all(r.values()) and r['class'] in {'allow','ask','deny'}
  assert r['risk'].split()[0]==risk==p['risk'] and r['category'].startswith('CAT-2 ')
  assert r['command']==p['command'] and r['source']==p['source']
  for field in ['class','severity','description']:
   assert p['annotation'].get(field,p['annotation'].get('policy_class'))==r[field],(p['id'],field)
  assert p['provenance'] and all(x.get('url') for x in p['provenance'])
  assert p['published_command_sha256']==hashlib.sha256(r['command'].encode()).hexdigest()
  check=subprocess.run(['/bin/bash','--noprofile','--norc','-n'],input=r['command'],text=True,capture_output=True,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'},timeout=5)
  assert check.returncode==0,(p['id'],check.stderr)
  syntax.append(dict(id=p['id'],bash_parse_passed=True,executed=False))
 for f in folder.rglob('commands.csv'):
  with f.open(newline='') as stream:
   reader=csv.DictReader(stream);assert reader.fieldnames==FIELDS
   for r in reader:assert r['class'] in {'allow','ask','deny'} and all(r.values())
 assert len({p['pair_id'] for p in pairs})==len(pairs)
 for p in pairs:
  a=byid[p['risky_id']][0];b=byid[p['safe_id']][0]
  assert a['class']!='allow' and b['class']=='allow' and a['util']==b['util']
  assert p['risk']==risk
 assert {p['risky_id'] for p in pairs}=={i for i,(r,p) in byid.items() if r['class']!='allow'}
 html=(folder/'viewer/index.html').read_text();data=json.loads(re.search(r'<script id="viewer-data" type="application/json">(.*?)</script>',html,re.S)[1])
 assert set(data['rows'])==set(byid)
 for i,(r,p) in byid.items():assert data['rows'][i]['fields']==r and data['rows'][i]['annotation']==p['annotation']
 assert data['pairs']==pairs and data['stats']['selected']==len(rows)
 for part in folder.glob('followup_*/provenance.jsonl'):
  ps=jl(part);rs=list(csv.DictReader(part.with_name('commands.csv').open()))
  assert len(ps)==len(rs)
  for p,r in zip(ps,rs):assert byid[p['id']]==(r,p)
 manifest=json.loads((folder/'manifest.json').read_text())
 for f,h in manifest['files'].items():assert hashlib.sha256((folder/f).read_bytes()).hexdigest()==h,('manifest',f)
 assert manifest['selected']==len(rows)
 # Discussion/archive remain historical and are intentionally not relabelled.
 for group in ['discussion/reserve.jsonl','discussion/other.jsonl','archive/archive.jsonl']:
  expected=json.loads((folder/'audit_v0_2026-10-31/historical_inventory.json').read_text())[group]
  assert hashlib.sha256((folder/group).read_bytes()).hexdigest()==expected
 return dict(risk=risk,selected=len(rows),csv_schema=True,nonempty=True,three_classes=True,exact_duplicates=0,syntax=syntax,csv_provenance_pairs_viewer_consistent=True,manifest_hashes_valid=True,historical_appendix_unchanged=True,utility_semantics='manual source-backed review; not inferred from bash -n',train_overlap='not_verifiable_train_not_supplied',gold=False)
if __name__=='__main__':
 result=validate(Path(__file__).resolve().parents[1]);print(json.dumps({k:v for k,v in result.items() if k!='syntax'},ensure_ascii=False))
