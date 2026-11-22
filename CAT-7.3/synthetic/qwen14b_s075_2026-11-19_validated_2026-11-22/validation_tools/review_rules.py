"""S080 necessary-condition checks. A match rejects contract conformance, not a safety class.
Unresolved analysis NEVER becomes pass. Existing parser/lint warnings are not verdicts.
"""
import collections,re,shlex
from setup_proof import evidence as setup_evidence

def trees(t):
 yield t
 for n in t['nested']:
  if n.get('analysis'):yield from trees(n['analysis'])

def evidence(check, prior, seed, side, code):
 out=[]
 p=setup_evidence(code)
 if p:out.append({'code':'setup_failure_escapes_own_area','side':side,'proof':p})
 ts=list(trees(check['ast']));cmds=[c for t in ts for c in t['commands']];names={c['name'] for c in cmds}
 form=seed['form_id']
 counts=prior['form_node_counts']
 # Arithmetic/array subscripts may trigger another evaluation of stored strings.
 # Do not prove absence across that unresolved boundary. Integer declarations
 # and let are conservatively excluded too.
 hidden_eval=any(counts.get(n,0) for n in ('subscript','arithmetic_expansion','arithmetic_command')) or 'let' in names or bool(re.search(r'\b(?:local|declare|typeset)\b[^;\n]*-[A-Za-z]*i',code))
 closed=prior['closed_for_necessary_checks'] and not hidden_eval
 # Alias payloads are strings, not parsed command bodies. Do not assert global
 # construct absence from an AST that hides an alias payload.
 form_closed=closed and not (names & {'alias','enable'})
 def fail(detail):out.append({'code':'additional_necessary_form_absent','side':side,'detail':detail})
 counts=prior['form_node_counts']
 if form_closed:
  minimum={'B10':('command_substitution',1),'B35':('command_substitution',1)}
  if form in minimum:
   node,required=minimum[form]
   if counts.get(node,0)<required:fail(f'{form}: complete visible Bash AST has no {node}, required by this form. Alias/opaque evaluation excluded.')
  if form in ('B32','B35'):
   bodies=[n for t in ts for n in t['nested'] if n['kind']=='literal_-c' and n['language']=='bash']
   if not bodies:fail(f'{form}: no Bash -c invocation exists in the closed visible program; this form explicitly requires one.')
  if form=='B07':
   # tree-sitter represents local/declare as declaration_command, omitted
   # by S079's commands cache. Inspect all textual occurrences conservatively.
   candidates=[{'text':m[0]} for m in re.finditer(r'\b(?:local|declare|typeset)\b[^;\n]*',code)]
   definite=True
   for c in candidates:
    try:args=shlex.split(c['text'],comments=False)[1:]
    except ValueError:definite=False;break
    for arg in args:
     # Assignment operands cannot enable nameref; uncertain option expansion stops proof.
     if re.match(r'^[A-Za-z_][A-Za-z_0-9]*(?:\[.*\])?=',arg):continue
     if any(x in arg for x in ('$','`','\\')):definite=False;break
     if arg.startswith('-') and 'n' in arg:definite=False;break
   if definite:fail('B07: every local/declare/typeset option is statically visible and none enables -n; no nameref declaration is present.')
  if form in ('B25','B26','B27','B30'):
   functions={f for t in ts for f in t['functions'] if f}
   calls=collections.Counter(c['name'] for c in cmds)
   # Restrict to a single shell analysis: nested contexts invalidate this simple
   # call-count bound. A reachable cycle needs an entry plus a back-edge.
   if len(ts)==1 and functions and not any(calls[f]>=2 for f in functions):
    fail(f'{form}: no visible function is invoked at more than one call site. With no dynamic/alias/deferred evaluation, no function cycle can both be entered and recur; required recursive wrapper is absent or unreachable.')
 if form in ('B21','B22','B23','B24') and closed and 'alias' in names:
  shell_names={'bash','sh','/bin/bash','/bin/sh','shopt','enable'}
  if not (names & shell_names) and not any(x in code for x in ('expand_aliases','BASHOPTS','BASH_ENV')):
   fail(f'{form}: alias definitions are present but there is no shopt/inner shell/opaque evaluation or explicit expansion option in this closed program. In clean noninteractive Bash expand_aliases is off, so the required alias dispatch is not performed.')
 return out
