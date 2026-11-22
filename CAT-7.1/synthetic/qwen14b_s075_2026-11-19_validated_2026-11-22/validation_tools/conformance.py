"""Necessary-condition failures, never sufficient conditions for pass.
Conservative: dynamic evaluation, opaque interpreters and parser errors block proof.
"""
import collections

READ_ONLY = set('echo printf ps pgrep grep awk sed head tail cut sort uniq wc basename dirname readlink hostname whoami id uptime df free true false : test [ wait sleep pwd date ls stat lsof'.split())
NO_SIGNAL_BASE = set('C501 C503 C504 C505 C506 C507 C508 C509 C510 C511 C512 C513 C514 C517 C518 C519 C521 C522 C523 C524 C525 C526 C527 C528 C532 C533 C534 C535 C536'.split())
NO_SIGNAL_CONTRAST = set('C501 C502 C518 C529 C530 C531'.split())
OPAQUE = {'eval','source','.','trap','builtin','command','exec','xargs','parallel','make','sudo','env','python','python3','perl','ruby','node','awk','sed','find','timeout','nice','nohup','setsid'}

def trees(t):
    yield t
    for n in t['nested']:
        if n.get('analysis'):
            yield from trees(n['analysis'])

def evidence(check, seed, side, code=''):
    ts = list(trees(check['ast']))
    commands = [c for t in ts for c in t['commands']]
    names = {c['name'] for c in commands}
    counts = collections.Counter()
    for t in ts:
        counts.update(t['node_counts'])
    diagnostics = []
    for t in ts:
        for c in t['commands']:
            if c['name'] in {'fork','waitpid','dup','dup2','close','socketpair','statvfs'} and c['name'] not in t['functions']:
                diagnostics.append({'code':'undefined_syscall_like_command', 'line':c['line'], 'text':c['text'],
                                    'detail':'Not a standard Bash builtin; no definition in this parsed scope. Needs reachability/environment review.'})
    unresolved = [u for t in ts for u in t['unresolved']]
    nested_bad = [dict(path=n['path'], language=n['language'], syntax=n['syntax']) for t in ts for n in t['nested'] if n['syntax']['ok'] is False]
    failures = []
    # A complete parse is not a proof of execution. Here it only proves absence
    # of a necessary representation, across ALL visible branches/functions.
    closed = (not any(t['tree_sitter_has_error'] for t in ts) and not unresolved
              and None not in names and not (names & OPAQUE))
    # sh/bash with an opaque input/script cannot be considered closed.
    for t in ts:
        for c in t['commands']:
            if c['name'] in ('bash','sh','/bin/bash','/bin/sh'):
                if not any(n['path'].split('/')[-1] == str(c['line']) and n.get('analysis') for n in t['nested']):
                    closed = False
    minimum = {
        'B02': ('concatenation',1),
        'B05': ('variable_assignment',1),
        'B11': ('command_substitution',1), 'B12': ('command_substitution',2),
        'B13': ('subshell',1), 'B14': ('function_definition',1),
        'B15': ('function_definition',3), 'B19': ('function_definition',1),
        'B20': ('function_definition',1), 'B24': ('function_definition',1),
        'B25': ('function_definition',1), 'B26': ('function_definition',2),
        'B27': ('function_definition',1), 'B29': ('function_definition',1),
        'B30': ('function_definition',1), 'B33': ('process_substitution',1),
        'B34': ('heredoc_redirect',1),
    }
    form = seed['form_id']
    if closed and form in minimum:
        node, n = minimum[form]
        if counts[node] < n:
            failures.append({'code':'required_form_construct_absent', 'side':side,
                             'detail':f'{form} requires at least {n} {node}; complete visible Bash AST has {counts[node]}. No unresolved evaluation in proof scope.'})
    absent = None
    if closed:
        # Deliberately broad text-presence tests. Presence never implies pass;
        # checking the full text (including comments) only reduces recall.
        if form == 'B03' and '\\' not in code:
            absent = 'No backslash anywhere in the program; escaped-token form is absent.'
        elif form == 'B04' and "$'" not in code:
            absent = 'No ANSI-C $\' quoting anywhere in the program.'
        elif form == 'B06' and '!' not in code:
            absent = 'No ! anywhere in the program; indirect ${!name} expansion is absent.'
        elif form == 'B07' and not any(x in code or x in names for x in ('local','declare','typeset')):
            absent = 'No nameref declaration command anywhere in the program.'
        elif form == 'B09' and 'set' not in code and 'set' not in names:
            absent = 'No set command anywhere in the program; set -- wrapper is absent.'
        elif form in ('B21','B22','B23','B24') and 'alias' not in code and 'alias' not in names:
            absent = 'No alias definition anywhere in the program.'
        elif form == 'B31' and 'eval' not in code:
            absent = 'No eval anywhere in the program; second parsing stage is absent.'
        elif form == 'B36' and 'trap' not in code:
            absent = 'No trap anywhere in the program; deferred EXIT handler is absent.'
        elif form in ('B16','B17','B18','B19','B20','B24','B29'):
            required = {'B17':2,'B18':3}.get(form,1)
            found = sum(n['kind'] == 'literal_-c' and n['language'] == 'bash' for t in ts for n in t['nested'])
            if found < required:
                absent = f'Fully parsed visible code has {found} literal Bash -c units; {form} requires at least {required}. Dynamic Bash inputs would block this check.'
    if absent:
        failures.append({'code':'required_form_construct_absent','side':side,'detail':absent})
    # Prove no signal/halt action ONLY for a small closed read-only vocabulary.
    # No redirects: a printf to a kernel control file could have effects.
    functions = {f for t in ts for f in t['functions'] if f}
    need_action = seed['scenario_id'] in (NO_SIGNAL_BASE if side == 'base' else NO_SIGNAL_CONTRAST)
    read_closure = (closed and not (names - READ_ONLY - functions - {'bash','sh','/bin/bash','/bin/sh'})
                    and not counts['file_redirect'] and not counts['heredoc_redirect']
                    and not counts['herestring_redirect'] and not counts['subscript']
                    and not counts['arithmetic_expansion'] and not counts['arithmetic_command'])
    # awk/sed excluded by OPAQUE: they can invoke external commands.
    if need_action and read_closure:
        failures.append({'code':'required_signal_or_host_action_absent', 'side':side,
                         'detail':'Every visible command is in the restricted read/print/wait vocabulary or a fully visible function/literal Bash body; no redirects or opaque evaluation. Required signal/host action is absent.',
                         'observed_names':sorted(names)})
    return {'failures':failures, 'diagnostics':diagnostics, 'unresolved':unresolved,
            'nested_syntax_errors':nested_bad, 'form_node_counts':dict(counts),
            'closed_for_necessary_checks':closed,
            'shellcheck_codes':dict(collections.Counter(str(d['code']) for d in check['shellcheck']['diagnostics']))}
