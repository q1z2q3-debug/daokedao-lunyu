#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""专题五《孝与道：药与饭》线上 HTML → 统一 Markdown 母本（DOM 解析，规避嵌套 div 边界问题）。"""
import re, html, pathlib
from html.parser import HTMLParser

BASE = "https://q1z2q3-debug.github.io/daokedao-lunyu"
FIG = {
    "图一 · 药与饭（第十八章次序）": f"{BASE}/fig/zt5-yao-yu-fan.svg",
    "图二 · 三器：敬留空、继使通、顺有度（本文引申示意）": f"{BASE}/fig/zt5-san-qi.svg",
}

src = pathlib.Path("/tmp/lunyu5.html").read_text(encoding="utf-8", errors="ignore")
s = src.find('<div class="leaf">')
e = src.find('<div class="foot">')
seg = src[s:e]
seg = re.sub(r'<div class="toc">.*?(?=<h2|<p|<div class="rows"|<div class="quote")', '', seg, flags=re.S)
seg = re.sub(r'<div class="crumb">.*?</div>', '', seg, flags=re.S)

# ---------- 极简 DOM ----------
class Node:
    __slots__ = ("tag", "attrs", "children", "text")
    def __init__(self, tag, attrs=None):
        self.tag = tag; self.attrs = dict(attrs or []); self.children = []; self.text = ""

VOID = {"br", "hr", "meta", "link", "img", "input", "rect", "path", "line", "text"}

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root"); self.stack = [self.root]
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs)
        self.stack[-1].children.append(n)
        if tag not in VOID:
            self.stack.append(n)
    def handle_startendtag(self, tag, attrs):
        n = Node(tag, attrs); self.stack[-1].children.append(n)
    def handle_endtag(self, tag):
        if tag in VOID: return
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]; break
    def handle_data(self, data):
        self.stack[-1].text += data

p = P(); p.feed(seg)

def cls(n): return n.attrs.get("class", "")

def inline(node):
    """提取节点内联文本，b/strong 加粗，br 换行，a 转链接；按文档顺序拼接。"""
    parts = []
    def walk(n, bold=False):
        if n.text:
            parts.append(("**" + n.text + "**") if bold else n.text)
        for c in n.children:
            if c.tag in ("b", "strong"):
                walk(c, True)
            elif c.tag == "br":
                parts.append("\n")
            elif c.tag == "a":
                href = c.attrs.get("href", "")
                t = "".join(x.text for x in c.children).strip()
                parts.append(f"[{t}]({href})" if href else t)
            else:
                walk(c, bold)
    walk(node)
    s = html.unescape("".join(parts))
    s = re.sub(r"\s+", " ", s).strip()
    s = s.replace("****", "** **")
    return s

out = []

def render(node):
    if node.tag in ("h2",):
        out.append("\n## " + inline(node) + "\n")
    elif node.tag == "h3":
        out.append("\n### " + inline(node) + "\n")
    elif node.tag == "p":
        t = inline(node)
        if t: out.append(t)
    elif node.tag == "div" and "rows" in cls(node):
        for row in node.children:
            if row.tag != "div" or "row" not in cls(row): continue
            k = v = ""
            for cell in row.children:
                if "k" in cls(cell): k = inline(cell)
                elif "v" in cls(cell): v = inline(cell)
            out.append(f"- **{k}**　{v}" if k else f"- {v}")
    elif node.tag == "div" and "quote" in cls(node):
        t = inline(node)
        out.append("\n> " + t.replace("\n", "\n> ") + "\n")
    elif node.tag == "div" and "figs" in cls(node):
        cap = ""
        def alltext(n):
            t = n.text
            for c in n.children: t += alltext(c)
            return t
        for f in node.children:
            if "fig" in cls(f):
                for c in f.children:
                    if "figcap" in cls(c): cap = html.unescape(alltext(c)).strip()
        url = FIG.get(cap, "")
        if url:
            out.append(f"\n![{cap}]({url})\n*{cap} · [SVG 直链]({url})*\n")
        elif cap:
            out.append(f"\n*{cap}*\n")
    elif node.tag == "table":
        rows = [c for c in node.children if c.tag == "tr"]
        md_rows = []
        for r in rows:
            cells = [inline(c) for c in r.children if c.tag in ("th", "td")]
            md_rows.append(cells)
        if md_rows:
            ncol = len(md_rows[0])
            md = ["| " + " | ".join(md_rows[0]) + " |", "|" + "---|" * ncol]
            for r in md_rows[1:]:
                md.append("| " + " | ".join(r) + " |")
            out.append("\n" + "\n".join(md) + "\n")
    elif node.tag == "hr":
        out.append("\n---\n")
    else:
        for c in node.children:
            render(c)

for n in p.root.children:
    render(n)

md = "\n\n".join(x.strip() for x in out if x.strip())
md = re.sub(r"\n{3,}", "\n\n", md)
pathlib.Path("/home/user/Doubao/chats/38450693190946306/daokedao-lunyu/dist").mkdir(exist_ok=True)
pathlib.Path("/home/user/Doubao/chats/38450693190946306/daokedao-lunyu/dist/zt5-xiaoyu-dao.md").write_text(md, encoding="utf-8")
print("md chars:", len(md), "| h2:", md.count("\n## "), "| h3:", md.count("\n### "),
      "| table:", md.count("\n|---"), "| fig:", md.count("!["), "| li:", md.count("\n- **"))
