"""Lossless display-string extraction for the independently built English edition."""
import re,json,html
from pathlib import Path
CJK=re.compile(r'[\u3400-\u9fff]')
SCRIPT=re.compile(r'(<script\b[^>]*>)([\s\S]*?)(</script\s*>)',re.I)
QUOTED=re.compile(r'(["\'])(?:\\.|(?!\1)[^\r\n])*?\1')
def decode_string(raw):
    body=raw[1:-1]
    def escape(m):
        v=m.group(1)
        if v.startswith('u') and len(v)==5:return chr(int(v[1:],16))
        if v.startswith('x') and len(v)==3:return chr(int(v[1:],16))
        return {'n':'\n','r':'\r','t':'\t','b':'\b','f':'\f','v':'\v','0':'\0','\n':''}.get(v,v)
    return re.sub(r'\\(u[0-9a-fA-F]{4}|x[0-9a-fA-F]{2}|[\s\S])',escape,body)
def js_tokens(source):
    """Yield editable string interiors, excluding comments and regexp literals."""
    n=len(source);i=0;previous=''
    def expression(i,stop=None):
        nonlocal previous
        depth=0;parens=[]
        while i<n:
            ch=source[i]
            if stop and ch==stop and depth==0:return i+1
            if source.startswith('//',i):
                end=source.find('\n',i+2);i=n if end<0 else end+1;continue
            if source.startswith('/*',i):
                end=source.find('*/',i+2);i=n if end<0 else end+2;continue
            if ch in ['"',"'"]:
                start=i;i+=1
                while i<n:
                    if source[i]=='\\':i+=2;continue
                    if source[i]==ch:
                        i+=1;yield (start,i,decode_string(source[start:i]),ch);break
                    if source[i] in '\r\n':break
                    i+=1
                previous='value';continue
            if ch=='`':
                i+=1;start=i
                while i<n:
                    if source[i]=='\\':i+=2;continue
                    if source[i]=='`':
                        if i>start:yield(start,i,decode_string('`'+source[start:i]+'`'),'template')
                        i+=1;break
                    if source.startswith('${',i):
                        if i>start:yield(start,i,decode_string('`'+source[start:i]+'`'),'template')
                        gen=expression(i+2,'}');
                        try:
                            while True:yield next(gen)
                        except StopIteration as done:i=done.value
                        start=i;continue
                    i+=1
                previous='value';continue
            if source.startswith('=>',i):previous='=>';i+=2;continue
            if ch=='(':parens.append(previous in ['if','while','for','with','switch','catch']);previous='(';i+=1;continue
            if ch==')':previous='condition' if parens and parens.pop() else ')';i+=1;continue
            if ch=='/' and previous in ['', '=', '(', ':', ',', '[', '!', '?', 'return', '=>', 'condition', '||','&&']:
                j=i+1;inside=False
                while j<n and source[j] not in '\r\n':
                    if source[j]=='\\':j+=2;continue
                    if source[j]=='[':inside=True
                    if source[j]==']':inside=False
                    if source[j]=='/' and not inside:
                        i=j+1
                        while i<n and source[i].isalpha():i+=1
                        previous='value';break
                    j+=1
                else:i+=1
                continue
            if ch=='{':depth+=1
            elif ch=='}':depth-=1
            if ch.isalpha() or ch=='_':
                j=i+1
                while j<n and (source[j].isalnum() or source[j] in '_$'):j+=1
                previous=source[i:j];i=j;continue
            if not ch.isspace():previous=ch
            i+=1
        return i
    yield from expression(0)
def encode(value,kind):
    if kind=='template':return value.replace('\\','\\\\').replace('`','\\`').replace('${','\\${').replace('</script','<\\/script')
    return json.dumps(value,ensure_ascii=False).replace('</script','<\\/script')
def walk_json(value,visit):
    if isinstance(value,str):return visit(value)
    if isinstance(value,list):return [walk_json(v,visit) for v in value]
    if isinstance(value,dict):return {k:walk_json(v,visit) for k,v in value.items()}
    return value

def process_js(source,visit):
    edits=[]
    for start,end,value,kind in js_tokens(source):
        if CJK.search(value):edits.append((start,end,encode(re.sub(r'(</(?:span|strong|em|b|i)>)(?=[A-Za-z])',r'\1 ',visit(value)),kind)))
    for a,b,s in reversed(edits):source=source[:a]+s+source[b:]
    return source

def process_html(source,visit):
    blocks=[]
    def script(m):
        text=process_js(m[2],visit)
        token=f'<!--EN-SCRIPT-{len(blocks)}-->';blocks.append(m[1]+text+m[3]);return token
    source=SCRIPT.sub(script,source)
    def style(m):
        token=f'<!--EN-SCRIPT-{len(blocks)}-->';blocks.append(process_css(m[0],visit));return token
    source=re.sub(r'<style\b[^>]*>[\s\S]*?</style\s*>',style,source,flags=re.I)
    # Display text and accessibility attributes; layout and script ordering stay intact.
    def attrs(m):
        name=m[1].split('=')[0].strip().lower();value=html.unescape(m[3])
        visible=name in ['aria-label','aria-description','title','placeholder','alt','value'] or name.startswith('data-')
        return m[1]+m[2]+html.escape(visit(value),quote=True)+m[2] if visible and CJK.search(value) else m[0]
    source=re.sub(r'([\w:-]+\s*=\s*)(["\'])(.*?)\2',attrs,source,flags=re.S)
    # Match real tags, allowing > inside visible prose or quoted attributes.
    tag=re.compile(r"<!--[\s\S]*?-->|<![^>]*>|</?[A-Za-z][^\s<>]*(?:[^<>\"']|\"[^\"]*\"|'[^']*')*>")
    parts=[];cursor=0
    for match in tag.finditer(source):
        raw=source[cursor:match.start()];value=html.unescape(raw)
        translated=html.escape(visit(value),quote=False) if CJK.search(value) else raw
        if CJK.search(value) and parts and re.fullmatch(r'</(?:span|strong|em|b|i)>',parts[-1],re.I) and re.match(r'[A-Za-z]',translated):translated=' '+translated
        parts.append(translated);parts.append(match[0]);cursor=match.end()
    raw=source[cursor:];value=html.unescape(raw);parts.append(html.escape(visit(value),quote=False) if CJK.search(value) else raw);source=''.join(parts)
    for i,block in enumerate(blocks):source=source.replace(f'<!--EN-SCRIPT-{i}-->',block)
    return source.replace('lang="zh-CN"','lang="en"')
def process_css(source,visit):
    mask=re.sub(r'/\*[\s\S]*?\*/',lambda m:' '*len(m[0]),source)
    edits=[]
    for match in re.finditer(r"\bcontent\s*:\s*([\"'])(.*?)\1",mask):
        raw=source[match.start(2):match.end(2)];value=decode_string(match[1]+raw+match[1])
        if CJK.search(value):edits.append((match.start(2),match.end(2),visit(value).replace('\\','\\\\').replace(match[1],'\\'+match[1])))
    for a,b,value in reversed(edits):source=source[:a]+value+source[b:]
    return source

def process_file(path,visit):
    source=path.read_text()
    if path.suffix=='.json':return json.dumps(walk_json(json.loads(source),visit),ensure_ascii=False,indent=2)+'\n'
    if path.suffix=='.html':return process_html(source,visit)
    if path.suffix=='.css':return process_css(source,visit)
    return process_js(source,visit)
def files(root):
    return sorted(p for p in root.rglob('*') if p.suffix in ['.html','.js','.mjs','.cjs','.json','.css'] and p.is_file())
def inventory(root):
    found={}
    for path in files(root):
        def visit(s):
            if CJK.search(s):found.setdefault(s,[]).append(str(path.relative_to(root)))
            return s
        process_file(path,visit)
    return {s:sorted(set(paths)) for s,paths in found.items()}
