import re,glob,importlib.util,html,sys
V={}
for f in glob.glob('episodes/ep*.py'):
    sp=importlib.util.spec_from_file_location('m',f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);V[m.N]=m.V
def sec(t):
    s=0
    for x in t.split(':'): s=s*60+int(x)
    return s
def build(src,out,title,extra_css=''):
    s=open(src,encoding='utf-8').read()
    notes=[]
    def rep(mo):
        ep,t,lab=mo.groups(); notes.append((ep,t,lab)); n=len(notes)
        tip=f"第 {int(ep)} 集 · {t} · {lab}"
        return f'<sup class="fn" data-v="{V[ep]}" data-t="{sec(t)}" data-tip="{html.escape(tip)}" tabindex="0">{n}</sup>'
    s=re.sub(r'\{\{(\d{3})\|([\d:]+)\|([^}]*)\}\}',rep,s)
    def pair(mo):
        sutra=mo.group(1).strip().replace('\n','<br>')
        return f'<section class="pair"><div class="sutra">{sutra}</div><div class="ex">{mo.group(2).strip()}</div></section>'
    s=re.sub(r'\[\[PAIR\]\](.*?)\[\[EX\]\](.*?)\[\[/PAIR\]\]',pair,s,flags=re.S)
    lst=''.join(f'<li><a class="fn2" href="#" data-v="{V[e]}" data-t="{sec(t)}">第 {int(e)} 集 · {t}</a>　{html.escape(l)}</li>' for e,t,l in notes)
    page=open('guanxin_template.html',encoding='utf-8').read().replace('%%BODY%%',s).replace('%%NOTES%%',lst)
    page=re.sub(r'<title>.*?</title>',f'<title>{title}</title>',page).replace('</style>',extra_css+'</style>')
    open(out,'w',encoding='utf-8').write(page); print(out,len(notes),'notes')
build('guanxin_src.html','../guanxin.html','观察自心 · 解深密经诠义讲经整理')
build('duizhao_src.html','../duizhao.html','经文与讲解对照 · 解深密经诠义',open('duizhao.css',encoding='utf-8').read())
