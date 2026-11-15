# 维护流程（每周更新用）

播放清单：https://www.youtube.com/playlist?list=PLAB59o9Lpy0oNGie02HwJGkfYCvMWsQFS
（译经院 abtemplorg 官方清单「講經16_解深密經詮義」；标题含「字幕版」的有烧录字幕，否则只有白板）

网站：https://qiutan-crypto.github.io/jieshenmi-notes/ （GitHub Pages，main 分支根目录）

## 文件
- `episodes/epNNN.py`：每集一个文件，字段 N, V(视频ID), DUR, SUB(True/False), DATE, NOTE(本集概述), B=[(秒,'h'|'b',标签,html)] 讲义/白板，S=[(秒,标题,html)] 讲解分段（无字幕集 S=[]）。
  写法照 ep024.py（有字幕）和 ep040.py（无字幕）。
- `build.py` + `template.html` → `../index.html`。template 里的「共 N 集（…缺 …）」「已整理 %%DONE%% / N」要随集数手动改。
- `duizhao_src.html` → `../duizhao.html`（经文与讲解对照）；`guanxin_src.html` → `../guanxin.html`。由 `build_reports.py` 生成。
  对照页语法：`[[PAIR]]经文（繁体，照讲义投影）[[EX]]<h4>串讲</h4>…<h4>名词</h4><dl>…</dl><h4>义贯</h4>…[[/PAIR]]`；
  出处角标：`{{集号|分:秒|标签}}`，例如 `{{040|38:50|板 27}}`（集号必须已有 episodes 文件）。
- `pub.sh "说明"`：重建三页并 commit + push。

## 抓取（在 Chrome 的 YouTube 播放页，用 javascript 工具）
YouTube 有 Trusted Types，不能 eval 文件，要把 `capture.js` 的函数内容直接贴进 javascript 工具执行。
- 字幕：`__startJob(1.5)` 逐 1.5 秒取画面底部字幕，二值化后去重成 strips；用 `__showR(a,b)` 把一批 strips 画成覆盖层截图来读（每屏约 100 条，分 4 栏即可）。
- 白板：`__boards(3)` 找出大面积白色的画面区间；用 `__grid([秒,...],4)` 一次截 12–16 张缩图来读。
- 长时间的 await 会让工具超时：把任务放到后台跑，再用短调用（≤40 秒）轮询进度；视频若被卸载（duration=null）要重新播放后继续。
- 先读完字幕再写 S（保留起承转合、法师补字；与他宗/时人相关的激烈批评只概述为“法师个人看法”），再读白板写 B。

## 对照页更新
新集若讲到经文：在 duizhao_src.html 相应位置加/补 [[PAIR]]；原来标「没有讲解」的 gap（041、042、045 的经文）一旦有了对应集，就补上经文与串讲/名词/义贯，删去 gap 说明；总结段落如有新内容也顺带更新。只收对经文本身的解释，不收题外话。
