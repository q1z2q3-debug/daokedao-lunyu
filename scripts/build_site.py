#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 GitHub Pages 站点（docs/）。

来源：../润泽说-论语 下的各课阅读版 HTML（单文件自包含）。
产出：
  docs/index.html      入口页（书封、卷首语、目录、体例、五步读法、系列内链）
  docs/book.html       卷首（封面、扉页、前言全文、目录）
  docs/ke/*.html       各课阅读版（注入返回条）
  docs/favicon.svg     robots.txt  sitemap.xml  llms.txt
用法：python3 scripts/build_site.py
"""
import glob
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.path.dirname(ROOT), "润泽说-论语")
DOCS = os.path.join(ROOT, "docs")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import daokedao_book as kit  # noqa: E402

SITE = "https://q1z2q3-debug.github.io/daokedao-lunyu"
VERSION = open(os.path.join(ROOT, "VERSION"), encoding="utf-8").read().strip()

# 课次表：(文件名中的数字或 pre, 页名, 课次, 章句, 主旨)
COURSES = [
    ("00-pre", "论语·前言·读论语之前（阅读版）.html", "前言", "读法 · 总纲 · 体例",
     "先读它说什么，再谈它意味着什么。"),
    ("01", "论语·第一课·学而时习（阅读版）.html", "第一课", "学而时习之，不亦说乎",
     "学是受，习是发；一阴一阳，才是这一句的全部。"),
    ("02", "论语·第二课·其为人也孝弟（阅读版）.html", "第二课", "其为人也孝弟，而好犯上者，鲜矣",
     "本立而道生：孝弟是根，不是姿态。"),
    ("03", "论语·第三课·巧言令色（阅读版）.html", "第三课", "巧言令色，鲜矣仁",
     "饰在外，实在内；「鲜」不是零。"),
    ("04", "论语·第四课·吾日三省（阅读版）.html", "第四课", "吾日三省吾身",
     "「省」是查事，不是定罪。"),
    ("05", "论语·第五课·道千乘之国（阅读版）.html", "第五课", "道千乘之国，敬事而信，节用而爱人，使民以时",
     "五事归两路：不欺与不竭。"),
    ("06", "论语·第六课·弟子入则孝（阅读版）.html", "第六课", "弟子入则孝，出则弟，谨而信，泛爱众，而亲仁",
     "先事后文，是次序，不是轻重。"),
    ("07", "论语·第七课·父在观其志（阅读版）.html", "第七课", "父在，观其志；父没，观其行；三年无改于父之道",
     "三个时间点看同一个人；无改不是守旧，是不忍遽改。"),
    ("08", "论语·第八课·君子不重则不威（阅读版）.html", "第八课", "君子不重则不威，学则不固",
     "不重是病，学是药；无友不如己，是承认人人有一处胜我。"),
    ("09", "论语·第九课·慎终追远（阅读版）.html", "第九课", "慎终追远，民德归厚矣",
     "两件收不到回音的事，把一个人、一家、一地的壁练厚。"),
    ("10", "论语·第十课·夫子至于是邦也（阅读版）.html", "第十课", "夫子至于是邦也，必闻其政",
     "五德不是技巧，是可接近性；以得之，是德之得。"),
    ("11", "论语·第十一课·礼之用和为贵（阅读版）.html", "第十一课", "礼之用，和为贵",
     "礼是界，和是容，节是度：无礼则混，无和则僵，无节则散。"),
    ("12", "论语·第十二课·信近于义（阅读版）.html", "第十二课", "信近于义，言可复也",
     "三个「近」是三把尺：诺贴着义，恭贴着礼，托身贴着可亲。"),
]

SERIES = [
    ("道德经", "https://q1z2q3-debug.github.io/runze-daodejing/"),
    ("心经", "https://q1z2q3-debug.github.io/daokedao-xinjing/"),
    ("金刚经", "https://q1z2q3-debug.github.io/daokedao-jingang/"),
    ("坛经", "https://q1z2q3-debug.github.io/daokedao-tanjing/"),
    ("阴符经", "https://q1z2q3-debug.github.io/daokedao-yinfujing/"),
    ("易传", "https://q1z2q3-debug.github.io/daokedao-yijing/"),
    ("庄子", "https://q1z2q3-debug.github.io/daokedao-zhuangzi/"),
    ("千字文", "https://q1z2q3-debug.github.io/daokedao-qianziwen/"),
    ("三字经", "https://q1z2q3-debug.github.io/daokedao-sanzijing/"),
    ("甲骨文", "https://q1z2q3-debug.github.io/daokedao-jiaguwen/"),
]

CSS = """
:root{--paper:#F7F4EE;--paper2:#FCFAF6;--ink:#25211D;--ink2:#3B352F;
  --ochre:#994433;--brown:#7C6D5C;--line:#DCD5C8}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#F7F4EE;color:#25211D;
  font-family:"Noto Serif SC","Songti SC","Source Han Serif SC",serif;
  font-size:17px;line-height:1.95;letter-spacing:.01em}
a{color:#994433;text-decoration:none;border-bottom:1px solid rgba(153,68,51,.28)}
a:hover{border-bottom-color:#994433}
.wrap{max-width:780px;margin:0 auto;padding:38px 22px 72px}
.top{display:flex;justify-content:space-between;align-items:baseline;
  border-bottom:1px solid #DCD5C8;padding-bottom:10px;margin-bottom:34px;
  font-size:12.5px;letter-spacing:.18em;color:#7C6D5C;
  font-family:"Noto Sans SC","PingFang SC",sans-serif}
.top b{color:#994433;font-weight:500}
.hd{padding:6px 0 10px}
.series{font-size:12px;letter-spacing:.42em;color:#994433;margin-bottom:14px}
h1.title{font-size:40px;line-height:1.4;margin:0 0 10px;font-weight:600;letter-spacing:.1em}
.sub{font-size:15px;color:#7C6D5C;margin:0 0 18px;letter-spacing:.06em}
.stat{font-size:12.5px;color:#7C6D5C;font-family:"Noto Sans SC",sans-serif}
.stat span{display:inline-block;margin-right:16px}
.stat em{font-style:normal;color:#994433}
h2{font-size:23px;margin:46px 0 8px;letter-spacing:.14em;font-weight:600}
h2.ch{font-size:27px;letter-spacing:.16em;margin:44px 0 12px}
h2 small{font-size:12px;color:#7C6D5C;letter-spacing:.1em;margin-left:10px;font-weight:400}
.lead{font-size:13.5px;color:#7C6D5C;margin:0 0 16px;letter-spacing:.03em}
p{margin:0 0 1.05em;text-align:justify}
.list{border-top:1px solid #DCD5C8}
.item{padding:18px 0 16px;border-bottom:1px solid #E7E0D4}
.item .no{font-size:11.5px;letter-spacing:.22em;color:#994433;
  font-family:"Noto Sans SC",sans-serif;margin-bottom:5px}
.item .t{font-size:19px;letter-spacing:.03em;margin:0 0 4px}
.item .s{font-size:13px;color:#5C5348;margin:0 0 6px}
.item .k{font-size:12.5px;color:#7C6D5C}
.item .k a{font-size:12.5px}
.rows{border-top:1px solid #DCD5C8;margin-top:6px}
.row{display:grid;grid-template-columns:132px 1fr;gap:14px;padding:13px 0;
  border-bottom:1px solid #E7E0D4}
.row .kk{font-size:12.5px;color:#994433;letter-spacing:.12em;
  font-family:"Noto Sans SC",sans-serif;line-height:1.85}
.row .vv{font-size:15px}
.five{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:10px}
.five div{border:1px solid #DCD5C8;background:#FCFAF6;padding:12px 10px;text-align:center}
.five i{display:block;font-style:normal;font-size:20px;color:#994433;margin-bottom:4px}
.five small{font-size:11.5px;color:#7C6D5C;line-height:1.6;display:block}
.foot{margin-top:54px;padding-top:16px;border-top:1px solid #DCD5C8;
  font-size:12px;color:#7C6D5C;line-height:2}
.foot a{margin-right:12px}
.series-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
  gap:1px;margin-top:8px;border-top:1px solid #DCD5C8;border-left:1px solid #E7E0D4}
.series-grid a{display:block;padding:11px 12px;font-size:14px;border:0;
  border-right:1px solid #E7E0D4;border-bottom:1px solid #E7E0D4;background:#FCFAF6}
.series-grid a small{display:block;font-size:11px;color:#8E8071;letter-spacing:.08em;margin-top:2px}
.btn{display:inline-block;border:1px solid #994433;color:#994433;padding:6px 16px;
  font-size:13px;letter-spacing:.12em;margin-top:6px}
@media (max-width:640px){
  .wrap{padding:26px 16px 56px}
  h1.title{font-size:28px;letter-spacing:.06em}
  .row{grid-template-columns:1fr;gap:4px}
  .five{grid-template-columns:1fr 1fr}
  .top{font-size:11.5px;letter-spacing:.1em}
}
""" + kit.COVER_CSS + "@media (max-width:640px){" + kit.COVER_MQ + "}"


def shell(title, desc, body, canonical=""):
    can = '<link rel="canonical" href="%s">' % canonical if canonical else ""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="author" content="润泽">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="book">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:site_name" content="润泽说 道可道">
<meta property="og:image" content="https://q1z2q3-debug.github.io/daokedao-lunyu/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://q1z2q3-debug.github.io/daokedao-lunyu/og.png">
%s<link rel="icon" href="favicon.svg" type="image/svg+xml">
<style>%s</style>
</head>
<body>
%s
</body>
</html>
""" % (title, desc, title, desc, can, CSS, body)


def cover_block():
    return kit.cover(
        title="论语",
        tag="学 而 篇 · 连 载",
        seal="论",
        gatha_first=("学而时习之", "不亦说乎"),
        gatha_second=("人不知而不愠", "不亦君子乎"),
        meta=["底本　朱熹《论语集注》", "体例　一章一课 · 两页双读", "已刊　前言与学而一至十二章", "v" + VERSION + " · 二〇二六"],
    )


def frontis_block():
    return kit.frontis(
        title="润泽说 道可道之论语",
        sub="学而篇 · 通释读本（连载）",
        lines=[
            ("底本", "朱熹《论语集注》，参校何晏《集解》、刘宝楠《正义》"),
            ("体例", "一章一课；每课少儿页七块、成人页十三至十四节"),
            ("图", "典故图由作者供图；义理图手写 SVG，随课附文件"),
            ("进度", "全书四百九十八章，已刊前言与一至十章"),
            ("版本", "v" + VERSION),
        ],
        seal="论",
    )


def toc_items():
    out = []
    for slug, fname, no, verse, gist in COURSES:
        out.append(
            '<div class="item"><div class="no">%s</div>'
            '<div class="t">%s</div><div class="s">%s</div>'
            '<div class="k"><a href="ke/%s.html">进入阅读版 →</a></div></div>'
            % (no, verse, gist, slug)
        )
    return "".join(out)


def build_index():
    body = """<div class="wrap">
<div class="top"><div>润 泽 说 · 道 可 道 之 论 语</div><div><b>学而篇</b>　连载 · v%s</div></div>
<div class="hd">
  <div class="series">润 泽 说 · 道 可 道</div>
  <h1 class="title">论语 · 学而篇</h1>
  <p class="sub">一章一课，一课两页；少儿页可念，成人页可考。底本朱熹《论语集注》。</p>
  <div class="stat"><span>全书 <em>498</em> 章</span><span>已刊 <em>13</em> 件</span><span>版本 v%s</span></div>
</div>

<h2>卷首语<small>为什么这样读</small></h2>
<p>注了两千年的书，最容易被注遮住。这一部先做一件事：<b>把原文摆回它自己的时代，让它说自己的话；义理另开一节，标清是谁的引申。</b></p>
<p>贯穿全书一条总纲：<b>一阴一阳之谓道</b>——学是受（阴、向内收），习是发（阳、向外放）。只学不习，是替别人保管知识；只习不学，是自己摸黑走路。</p>
<p>所以每一课都问一句：这章说的是<b>哪件事、哪个字</b>？说不出，就退入存疑，不写成定论。</p>

<h2>已刊十三件<small>前言 · 学而一至十二章</small></h2>
<p class="lead">按课次顺序；每件都有少儿页与成人页，另附义理图。</p>
<div class="list">%s</div>
<a class="btn" href="book.html">从卷首读起（封面 · 扉页 · 前言）</a>

<h2>体例<small>一页两读</small></h2>
<div class="rows">
  <div class="row"><div class="kk">少儿页</div><div class="vv">字义小课堂、一句话讲清、共读、生活里的一天、三个小问题、成长小启示、家长栏（勘俗见、现代对照、常变主线、教与学二分、时代落点、融西、可做一件）。句子短，画面具体。</div></div>
  <div class="row"><div class="kk">成人页</div><div class="vv">连读、字义句读、时代背景、章旨、朱子注、分寸、反面、张力、脉络、跨典、存疑、双卡、阴阳五蕴；后附典故图与读图、义理图、附论。每节先一句断语，再出证据。</div></div>
  <div class="row"><div class="kk">图</div><div class="vv">典故图由作者供图，助手只写提示词、不擅自生图；义理图手写 SVG，页面内嵌为唯一源，导出独立文件随仓库留存。</div></div>
  <div class="row"><div class="kk">存疑</div><div class="vv">被否定的解读不销毁：撤出正文，另存并标「存疑」，不写成定论。</div></div>
</div>

<h2>五步读法<small>前三步求真，后两步求活</small></h2>
<div class="five">
  <div><i>校</i><small>校字<br>底本 · 异文 · 音读</small></div>
  <div><i>境</i><small>还境<br>制度 · 称谓 · 场景</small></div>
  <div><i>义</i><small>立义<br>须超出时代</small></div>
  <div><i>疑</i><small>存疑<br>说不清就写出来</small></div>
  <div><i>用</i><small>致用<br>在自己的世代做</small></div>
</div>

<h2>同系列<small>润泽说 · 道可道</small></h2>
<p class="lead">同一位作者、同一套义理（三才五蕴、阴阳和合）、同一种体例。</p>
<div class="series-grid">%s</div>

<div class="foot">
  <div>润泽说 道可道之论语 · 学而篇　v%s　（2026-11-19）</div>
  <div>底本：朱熹《论语集注》　参校：何晏《集解》、刘宝楠《正义》</div>
  <div>全书四百九十八章，按篇连载；本书为第一批七件。许可：CC BY-NC-SA 4.0</div>
  <div><a href="https://github.com/q1z2q3-debug/daokedao-lunyu">GitHub 仓库</a><a href="book.html">卷首</a><a href="sitemap.xml">站点地图</a></div>
</div>
</div>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Book","name":"润泽说 道可道之论语 · 学而篇",
"author":{"@type":"Person","name":"润泽"},"inLanguage":"zh-CN","bookEdition":"v%s",
"description":"《论语》学而篇通释读本，一章一课，少儿页与成人页双读；底本朱熹《论语集注》。全书四百九十八章，按篇连载。",
"publisher":{"@type":"Organization","name":"润泽说 道可道"},
"hasPart":[%s]}
</script>""" % (
        VERSION,
        VERSION,
        toc_items(),
        "".join('<a href="%s">%s<small>通释读本</small></a>' % (u, n) for n, u in SERIES),
        VERSION,
        VERSION,
        ",".join('{"@type":"Chapter","name":"%s","url":"%s/ke/%s.html"}' % (no, SITE, slug) for slug, _f, no, _v, _g in COURSES),
    )
    open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8").write(
        shell(
            "润泽说 道可道之论语 · 学而篇｜《论语》通释读本（连载）",
            "《论语》学而篇通释：一章一课，少儿页可念、成人页可考。已刊前言与学而一至十二章，底本朱熹《论语集注》，义理图手写、存疑另立。",
            body,
            SITE + "/",
        )
    )


def build_book():
    pre_md = os.path.join(SRC, "前言-读论语之前.md")
    txt = open(pre_md, encoding="utf-8").read()
    frag = subprocess.run(["pandoc", "-f", "markdown", "-t", "html5", "--no-highlight"],
                          input=txt.encode("utf-8"), stdout=subprocess.PIPE, check=True).stdout.decode()
    frag = frag.replace("<h1", "<h2 class=\"ch\"", 1)
    frag = frag.replace("</h1>", "</h2>", 1)

    body = """<div class="wrap">
<div class="top"><div><a href="index.html" style="border:0">← 目录</a></div><div>润 泽 说 · 道 可 道 之 论 语</div></div>
%s
%s
<div class="wrap" style="padding-top:0">
<h2 style="font-size:26px;letter-spacing:.16em;margin:44px 0 10px">读法、总纲与体例</h2>
<p class="lead">前言十节，全文如下；正文六课见目录，各附义理图。</p>
%s
<h2 style="font-size:26px;letter-spacing:.16em;margin:44px 0 10px">六课目录</h2>
<div class="list">%s</div>
<div class="foot">
  <div>润泽说 道可道之论语 · 学而篇　卷首　v%s　（2026-11-19）</div>
  <div>底本：朱熹《论语集注》　参校：何晏《集解》、刘宝楠《正义》</div>
</div>
</div>
</div>""" % (cover_block(), frontis_block(), frag, toc_items(), VERSION)

    open(os.path.join(DOCS, "book.html"), "w", encoding="utf-8").write(
        shell(
            "卷首：封面 · 扉页 · 前言｜润泽说 道可道之论语",
            "《论语》通释读本卷首：封面、扉页与前言十节（为什么从原文读起、一条总纲、君子不器、时的三层、认知之圆、朋来互享、五步读法、融西、体例、后续之路）。",
            body,
            SITE + "/book.html",
        )
    )


NAV = """<div style="background:#FCFAF6;border-bottom:1px solid #DCD5C8;padding:9px 16px;
font-family:'Noto Sans SC','PingFang SC',sans-serif;font-size:12px;letter-spacing:.1em;
display:flex;justify-content:space-between;align-items:center;color:#7C6D5C">
<span>润泽说 · 道可道之论语 · 学而篇</span>
<a href="../index.html" style="color:#994433;text-decoration:none;border:0">← 目录</a></div>
"""


def build_courses():
    outdir = os.path.join(DOCS, "ke")
    os.makedirs(outdir, exist_ok=True)
    n = 0
    for slug, fname, *_ in COURSES:
        src = os.path.join(SRC, fname)
        if not os.path.exists(src):
            print("[warn] 缺文件：", fname)
            continue
        html = open(src, encoding="utf-8").read()
        m = re.search(r"<body[^>]*>", html)
        if m:
            html = html[:m.end()] + "\n" + NAV + html[m.end():]
        open(os.path.join(outdir, slug + ".html"), "w", encoding="utf-8").write(html)
        n += 1
    print("已注入返回条并拷贝 %d 篇" % n)


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="10" fill="#994433"/>
<text x="32" y="45" font-size="40" text-anchor="middle" fill="#F7F4EE"
font-family="'Noto Serif SC','Songti SC',serif">论</text></svg>"""


def build_meta():
    open(os.path.join(DOCS, "favicon.svg"), "w", encoding="utf-8").write(FAVICON)
    urls = ["", "book.html"] + ["ke/%s.html" % c[0] for c in COURSES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sm += "<url><loc>%s/%s</loc><lastmod>2026-11-19</lastmod><changefreq>weekly</changefreq></url>\n" % (SITE, u)
    sm += "</urlset>\n"
    open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8").write(sm)

    open(os.path.join(DOCS, "robots.txt"), "w", encoding="utf-8").write(
        "User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\n"
        "Sitemap: %s/sitemap.xml\n" % SITE)

    llms = """# 润泽说 道可道之论语 · 学而篇

> 《论语》通释读本，连载中。底本朱熹《论语集注》，全书四百九十八章，一章一课。
> 每课两页：少儿页（可念、可见）与成人页（可考、可查）。义理图手写 SVG；被否定的解读撤出正文另立「存疑」。

## 已刊
"""
    for slug, _f, no, verse, gist in COURSES:
        llms += "- %s｜%s｜%s：%s/%s/ke/%s.html\n" % (no, verse, gist, SITE, "", slug)
    llms += """
## 引用
润泽《润泽说 道可道之论语 · 学而篇》v%s，%s/

## 义理口径
一阴一阳之谓道：学为受（阴）、习为发（阳）。君子不器：可器而不着于器（杯与管之模型）。
不新造名相；凡解读须指回原文的哪个字、哪一句；指不回者入「存疑」。
""" % (VERSION, SITE)
    open(os.path.join(DOCS, "llms.txt"), "w", encoding="utf-8").write(llms)


def main():
    os.makedirs(DOCS, exist_ok=True)
    build_index()
    build_book()
    build_courses()
    build_meta()
    print("站点已生成：" , DOCS)


if __name__ == "__main__":
    main()
