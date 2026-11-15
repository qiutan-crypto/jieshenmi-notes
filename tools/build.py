#!/usr/bin/env python3
"""Build ../index.html from template.html + episodes/epNNN.py.
Each episode module defines: N, V (YouTube id), DUR, SUB (bool), DATE, NOTE,
B = [(seconds, 'h'|'b', label, html)]  # handout pages / whiteboards
S = [(seconds, title, html)]            # lecture segments (empty if no subtitles)
"""
import glob, importlib.util, json, os
here=os.path.dirname(os.path.abspath(__file__))
def fmt(t): return '%d:%02d:%02d'%(t//3600,t%3600//60,t%60) if t>=3600 else '%02d:%02d'%(t//60,t%60)
secs=[]; done={}
for p in sorted(glob.glob(os.path.join(here,'episodes','ep*.py'))):
    sp=importlib.util.spec_from_file_location('ep',p); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    link=lambda t:f'<a class="t" data-v="{m.V}" data-t="{t}" href="https://www.youtube.com/watch?v={m.V}&t={t}s">{fmt(t)}</a>'
    o=[f'<section id="ep-{m.N}" data-v="{m.V}" data-n="{m.N}">\n<h2>第 {m.N} 集</h2>',
       f'<div class="meta">{m.DUR} · {"字幕版" if m.SUB else "无字幕（仅整理白板与讲义）"}{" · "+m.DATE if m.DATE else ""} · <a href="https://www.youtube.com/watch?v={m.V}">在 YouTube 打开</a></div>',
       f'<div class="note">{m.NOTE}</div>',
       '<h3>一、讲义与白板（书写内容）</h3>\n<p class="hint">点时间可跳到写这块板 / 放这页讲义的位置。黄底是印刷讲义，蓝底是白板手写。</p>\n<div class="grid">']
    for t,kind,label,html in m.B:
        o.append(f'<div class="b{" h" if kind=="h" else ""}"><small>{link(t)}{label}</small>{html}</div>')
    o.append('</div>')
    if m.S:
        o.append('<h3>二、讲解内容（按时间顺序）</h3>\n<p class="hint">小标题前的「起 / 承 / 转 / 合」标出法师讲解的衔接。</p>')
        for t,k,html in m.S:
            o.append(f'<div class="seg">{link(t)}<div>\n<b class="k">{k}</b>\n{html}</div></div>')
    o.append('</section>')
    secs.append('\n'.join(o)); done[m.N]='已整理' if m.S else '仅白板'
t=open(os.path.join(here,'template.html'),encoding='utf-8').read()
t=t.replace('%%SECTIONS%%','\n\n'.join(secs)).replace('%%DONE%%',str(len(done))).replace('%%DONESET%%',json.dumps(done))
open(os.path.join(here,'..','index.html'),'w',encoding='utf-8').write(t)
print('built',len(done),'episodes')
