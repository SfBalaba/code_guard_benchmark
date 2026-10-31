"""Reproduce selected CSV/provenance/pairs from the audited output snapshot.
Writes to a separate destination, never runs dataset commands.
"""
import argparse,csv,json
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
source=Path(__file__).resolve().parent
rows=[json.loads(x) for x in (source/'selection_output.jsonl').read_text().splitlines()]
args.output.mkdir(parents=True,exist_ok=False)
with (args.output/'commands.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames='command description util severity category risk source seed class'.split());writer.writeheader();writer.writerows(x['fields'] for x in rows)
(args.output/'provenance.jsonl').write_text(''.join(json.dumps(x['provenance'],ensure_ascii=False)+'\n' for x in rows))
(args.output/'pairs.jsonl').write_bytes((source/'pairs_after.jsonl').read_bytes())
