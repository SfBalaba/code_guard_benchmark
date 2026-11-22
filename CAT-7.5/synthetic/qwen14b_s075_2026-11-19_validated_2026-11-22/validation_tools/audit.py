"""Exhaustive inert checks. Model text is ONLY parser input, never a program to run."""
import ast
import collections
import concurrent.futures
import hashlib
import json
import pathlib
import re
import subprocess
import sys
from tree_sitter import Language, Parser
import tree_sitter_bash
from conformance import evidence

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = ROOT / 'train_generation_2026-11-19_cat7_qwen14b_full'
BASH = '/opt/homebrew/bin/bash'
SHELLCHECK = str(HERE / '.venv/bin/shellcheck')
ENV = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'}
LANG = Language(tree_sitter_bash.language())

def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()

def readl(p):
    return [json.loads(l) for l in p.open()]

def dump(p, x):
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')

def writel(p, rows):
    with p.open('w') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, separators=(',', ':')) + '\n')

def parse_only(code):
    try:
        r = subprocess.run([BASH, '--noprofile', '--norc', '-n'], input=code,
                           text=True, capture_output=True, timeout=8, env=ENV)
        return {'ok': r.returncode == 0, 'stderr': r.stderr}
    except subprocess.TimeoutExpired:
        return {'ok': None, 'stderr': 'parser timeout; no verdict'}

def walk(node):
    yield node
    for c in node.named_children:
        yield from walk(c)

def literal(node, data):
    """Only constant shell words. No expansion, unescaping eval, or shell invocation."""
    if node is None:
        return None
    t = data[node.start_byte:node.end_byte].decode()
    if node.type == 'raw_string':
        return t[1:-1]
    if node.type == 'word' and not re.search(r'[\\$`*?\[\]{}~]', t):
        return t
    if node.type == 'string' and not re.search(r'[\\$`]', t):
        return t[1:-1]
    if node.type in ('concatenation', 'command_name'):
        parts = [literal(c, data) for c in node.named_children]
        return ''.join(parts) if parts and all(v is not None for v in parts) else None
    return None

def inspect_tree(code, depth=0, path='outer'):
    data = code.encode()
    tree = Parser(LANG).parse(data)
    nodes = list(walk(tree.root_node))
    counts = collections.Counter(n.type for n in nodes)
    commands, nested, unresolved = [], [], []
    functions = [literal(n.child_by_field_name('name'), data) for n in nodes if n.type == 'function_definition']
    for n in nodes:
        if n.type != 'command':
            continue
        parts = [c for c in n.named_children if c.type not in ('variable_assignment',)]
        if not parts:
            continue
        values = [literal(c, data) for c in parts]
        name = values[0]
        commands.append({'name': name, 'line': n.start_point.row + 1,
                         'text': data[n.start_byte:n.end_byte].decode()})
        interpreter = pathlib.PurePosixPath(name or '').name
        body, language, kind = None, None, None
        if interpreter in ('bash', 'sh', 'python', 'python3'):
            language = 'python' if interpreter.startswith('python') else 'bash'
            if '-c' in values:
                i = values.index('-c') + 1
                if i < len(values):
                    body, kind = values[i], 'literal_-c'
                if body is None:
                    unresolved.append({'line': n.start_point.row + 1, 'kind': 'dynamic_interpreter_argument'})
            parent = n.parent
            if parent and parent.type == 'redirected_statement':
                for redir in parent.named_children:
                    if redir.type != 'heredoc_redirect':
                        continue
                    start = next((x for x in redir.named_children if x.type == 'heredoc_start'), None)
                    content = next((x for x in redir.named_children if x.type == 'heredoc_body'), None)
                    delim = data[start.start_byte:start.end_byte].decode() if start else ''
                    if content and (delim.startswith("'") or delim.startswith('"')):
                        body = data[content.start_byte:content.end_byte].decode()
                        kind = 'quoted_heredoc'
                    else:
                        unresolved.append({'line': n.start_point.row + 1, 'kind': 'expanding_heredoc'})
        elif interpreter in ('eval', 'source', '.', 'trap'):
            unresolved.append({'line': n.start_point.row + 1, 'kind': 'deferred_or_dynamic_' + interpreter})
        if name is None:
            unresolved.append({'line': n.start_point.row + 1, 'kind': 'dynamic_command_name'})
        if body is not None and depth < 4:
            item = {'path': path + '/' + str(n.start_point.row + 1), 'language': language,
                    'kind': kind, 'code': body, 'sha256': sha(body),
                    'reachability': 'not_proven; diagnostics_only'}
            if language == 'python':
                try:
                    ast.parse(body)
                    item['syntax'] = {'ok': True}
                except SyntaxError as e:
                    item['syntax'] = {'ok': False, 'line': e.lineno, 'message': str(e)}
            else:
                item['syntax'] = parse_only(body)
                item['analysis'] = inspect_tree(body, depth + 1, item['path'])
            nested.append(item)
    return {'tree_sitter_has_error': tree.root_node.has_error, 'node_counts': dict(counts),
            'commands': commands, 'functions': functions, 'nested': nested, 'unresolved': unresolved}

def inspect_command(code):
    syntax = parse_only(code)
    # Ignore model-supplied ShellCheck directives. No -x or sourced files supplied.
    lint_text = re.sub(r'(?m)^(\s*)#\s*shellcheck\b[^\n]*', r'\1# removed untrusted lint directive', code)
    try:
        p = subprocess.run([SHELLCHECK, '--norc', '--shell=bash', '--format=json', '-'],
                           input=lint_text, text=True, capture_output=True, timeout=12, env=ENV)
        lint = {'returncode': p.returncode, 'diagnostics': json.loads(p.stdout or '[]'), 'stderr': p.stderr}
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        lint = {'error': str(e), 'diagnostics': []}
    return {'command_sha256': sha(code), 'bash_syntax': syntax, 'shellcheck': lint,
            'ast': inspect_tree(code)}

def main():
    cards = readl(SOURCE / 'reports/pair_cards.jsonl')
    unique = {sha(c[s]['checks']['command']): c[s]['checks']['command'] for c in cards for s in ('base', 'contrast')}
    cache = HERE / 'command_analysis.jsonl'
    results = {r['command_sha256']: r for r in readl(cache)} if cache.exists() else {}
    todo = [v for k, v in unique.items() if k not in results]
    with cache.open('a') as f, concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for i, result in enumerate(pool.map(inspect_command, todo), 1):
            f.write(json.dumps(result, ensure_ascii=False, separators=(',', ':')) + '\n')
            results[result['command_sha256']] = result
            if i % 250 == 0:
                f.flush()
                print(f'parsed {i}/{len(todo)} unique programs', flush=True)
    manual_path = HERE / 'manual_reviews.jsonl'
    manual = {r['seed_id']: r for r in readl(manual_path)} if manual_path.exists() else {}
    decisions = []
    for card in cards:
        seed = card['seed']
        reasons = []
        sides = {}
        signals = {}
        for side in ('base', 'contrast'):
            response = card[side]
            code = response['checks']['command']
            check = results[sha(code)]
            signals[side] = evidence(check, seed, side, code)
            reasons.extend(signals[side]['failures'])
            sides[side] = {'command_sha256': sha(code), 'content_sha256': sha(response['content']),
                           'request_id': response['request_id'], 'context': response['evaluation_context'],
                           'model_call': response.get('model_call', True)}
            fence = re.fullmatch(r'\s*```(?:bash|sh)\s*\n([\s\S]*?)\n```\s*', response['content'])
            if not fence or response['content'].count('```') != 2:
                reasons.append({'code': 'response_format', 'side': side, 'detail': 'Required exactly one bash/sh fence with no outside text.'})
            if response['finish_reason'] != 'stop':
                reasons.append({'code': 'incomplete_generation', 'side': side, 'detail': response['finish_reason']})
            if check['bash_syntax']['ok'] is False:
                reasons.append({'code': 'outer_bash_syntax', 'side': side, 'detail': check['bash_syntax']['stderr']})
            assert response['evaluation_context'] == seed['evaluation_context'][side]
        same = sides['base']['command_sha256'] == sides['contrast']['command_sha256']
        if same and seed['pair_type'] == 'command_contrast' and sides['base']['context'] == sides['contrast']['context']:
            reasons.append({'code': 'identical_pair_no_context_change', 'detail': 'The requested command contrast is absent.'})
        if seed['pair_type'] == 'context_only':
            assert same and sides['base']['context'] != sides['contrast']['context']
        review = manual.get(seed['seed_id'])
        if review:
            assert review['command_sha256'] == {s: sides[s]['command_sha256'] for s in sides}
            if review['status'] == 'pass':
                assert not reasons, (seed['seed_id'], reasons)
            reasons.append({'code': 'agent_read_review', 'detail': review['reason']})
        status = 'reject' if any(r['code'] != 'agent_read_review' for r in reasons) else (review['status'] if review else 'needs_review')
        if not review and status == 'needs_review':
            reasons.append({'code': 'semantic_and_form_not_established', 'detail': 'Parsers and lint cannot prove scenario, paired contrast, wrapper behavior, resource ownership/lifetime, or cleanup. No semantic acceptance inferred.'})
        decisions.append({'seed_id': seed['seed_id'], 'risk': seed['risk'], 'scenario_id': seed['scenario_id'],
                          'form_id': seed['form_id'], 'pair_type': seed['pair_type'], 'status': status,
                          'review_method': 'static_exhaustive_plus_agent_read' if review else 'static_exhaustive',
                          'reasons': reasons, 'sides': sides, 'labels_assigned': False,
                          'static_conformance': signals,
                          'human_gold': False, 'semantic_validation': False})
    writel(HERE / 'pair_validation.jsonl', decisions)
    summary = {'pairs': len(cards), 'side_instances': len(cards)*2, 'unique_programs_parsed': len(unique),
               'agent_read_pairs': len(manual), 'model_calls': 0, 'corpus_executions': 0,
               'by_category': {cat: dict(collections.Counter(r['status'] for r in decisions if r['risk'] == cat))
                               for cat in ('CAT-7.1','CAT-7.3','CAT-7.5')},
               'reason_counts': dict(collections.Counter(x['code'] for r in decisions for x in r['reasons']))}
    dump(HERE / 'summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
