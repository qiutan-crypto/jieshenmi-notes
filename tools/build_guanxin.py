import re,glob,importlib.util,html
V={}
for f in glob.glob('episodes/ep*.py'):
    sp=importlib.util.spec_from_file_location('m',f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);V[m.N]=m.V
src=open('guanxin_src.html',encoding='utf-8').read()
notes=[]
def sec(t):
    p=[int(x) for x in t.split(':')];s=0
    for x in p:s=s*60+x
    return s
def rep(mo):
    ep,t,lab=mo.group(1),mo.group(2),mo.group(3)
    notes.append((ep,t,lab));n=len(notes)
    tip=f"第 {int(ep)} 集 · {t} · {lab}"
    return f'<sup class="fn" data-v="{V[ep]}" data-t="{sec(t)}" data-tip="{html.escape(tip)}" tabindex="0">{n}</sup>'
body=re.sub(r'\{\{(\d{3})\|([\d:]+)\|([^}]*)\}\}',rep,src)
lst=''.join(f'<li><a class="fn2" href="#" data-v="{V[e]}" data-t="{sec(t)}">第 {int(e)} 集 · {t}</a>　{html.escape(l)}</li>' for e,t,l in notes)
page=open('guanxin_template.html',encoding='utf-8').read().replace('%%BODY%%',body).replace('%%NOTES%%',lst)
open('../guanxin.html','w',encoding='utf-8').write(page)
print(len(notes),'notes')
