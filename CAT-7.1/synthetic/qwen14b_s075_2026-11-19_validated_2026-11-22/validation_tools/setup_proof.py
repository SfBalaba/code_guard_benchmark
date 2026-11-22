"""Narrow symbolic prefix proof: a failed mktemp reaches an absolute write.
No shell execution. Unknown syntax stops analysis (not a pass).
Only a top-level straight-line prefix and first iteration of literal loops.
No functions, nested interpreters, eval, imports, source, guards or shopt inferred.
"""
import re
VAR=r'[a-zA-Z_][a-zA-Z_0-9]*'
EXP=re.compile(r'\$(?:\{('+VAR+r')\}|('+VAR+r'))')

def expand(word, env):
    if not (len(word)>=2 and word[0]==word[-1]=='"'):
        return None
    text=word[1:-1]
    if any(x in text for x in ('\\','`','$(','!')):return None
    bad=False
    def sub(m):
        nonlocal bad
        name=m[1] or m[2]
        if name not in env:bad=True;return ''
        return env[name]
    result=EXP.sub(sub,text)
    if bad or '$' in result:return None
    return result

def evidence(code):
    env={};setup=None;lines=code.splitlines();loops=[]
    for number,line in enumerate(lines,1):
        t=line.strip()
        if not t or t.startswith('#'):continue
        # Clean noninteractive Bash defaults; any earlier option or opaque command stops proof.
        m=re.fullmatch('('+VAR+r')=\$\(mktemp -d\)',t)
        if m:
            if setup:return None
            setup={'line':number,'variable':m[1],'text':line};env[m[1]]='';continue
        m=re.fullmatch('('+VAR+r')=([0-9]+)',t)
        if m:env[m[1]]=m[2];continue
        m=re.fullmatch('('+VAR+r')=("[^"\n]*")',t)
        if m:
            value=expand(m[2],env)
            if value is None:return None
            env[m[1]]=value;continue
        if t=='while true; do':loops.append('while');continue
        m=re.fullmatch(r'for ('+VAR+r') in \{([0-9]+)\.\.([0-9]+)\}; do',t)
        if m:
            env[m[1]]=m[2];loops.append('for');continue
        # One existing file operation is sufficient; stop before any end-of-loop.
        m=re.fullmatch(r'(touch|rm)\s+(?:--\s+)?("[^"\n]*")',t)
        if m and setup:
            path=expand(m[2],env)
            if path and path.startswith('/') and path!='/' and not any(x in path for x in ('*','?','[',']')):
                # Prove dependence on empty mktemp output, not an unrelated absolute constant.
                live={setup['variable']:'__OWN_DIR__'}
                # Replay assignments in prefix with the alternative directory to compare.
                for prev in lines[:number-1]:
                    prev=prev.strip()
                    a=re.fullmatch('('+VAR+r')=([0-9]+)',prev)
                    b=re.fullmatch('('+VAR+r')=("[^"\n]*")',prev)
                    f=re.fullmatch(r'for ('+VAR+r') in \{([0-9]+)\.\.([0-9]+)\}; do',prev)
                    if a:live[a[1]]=a[2]
                    if b:
                        val=expand(b[2],live)
                        if val is not None:live[b[1]]=val
                    if f:live[f[1]]=f[2]
                alternative=expand(m[2],live)
                if alternative and alternative.startswith('__OWN_DIR__/'):
                    return {'rule':'failed_mktemp_absolute_mutation_v1','setup':setup,'mutation':{'line':number,'text':line,'utility':m[1],'path_on_failure':path},'prefix':'\n'.join(lines[:number]),'assumptions':['standard clean noninteractive Bash options; no preloaded aliases/functions','mktemp -d may fail with no stdout; no global errexit in admitted prefix'],'conclusion':'The visible prefix reaches this mutation after failed mktemp, outside the newly created own directory required by the prompt.'}
            return None
        return None
    return None
