#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""早期版式课的图外置：以阅读版 HTML 为准，导出义理 SVG 与图一位图到 docs/fig 与 assets。

背景：第 20–31 课（《为政》2.5–2.16）用的是早期版式，义理图为页内内联 SVG、
图一为页内 base64 位图，二者都不落盘，故拿不到直链、母本也无从引用。

规矩（沿用 svg_sync.py 2026-11-19 定）：页面内嵌 SVG 是唯一源，外置文件只是副本；
改图先改页面，再跑本脚本，禁止两边各改一遍。

已在 docs/fig 中有语义名的同名图，按内容比对复用，不重复导出。

用法：
    python3 scripts/export_old_figs.py            # 20–31 课
    python3 scripts/export_old_figs.py 20 22 24
"""
import base64
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KE = os.path.join(ROOT, 'docs', 'ke')
FIG = os.path.join(ROOT, 'docs', 'fig')
ASSETS = os.path.join(ROOT, 'assets')

SVG_RE = re.compile(r'<svg\b.*?</svg>', re.S)
IMG_RE = re.compile(r'<img[^>]*src="data:image/(\w+);base64,([^"]+)"[^>]*>', re.S)


def norm(svg):
    """去掉 width/height 与空白差异，用于内容比对。"""
    s = re.sub(r'\s(width|height)="[^"]*"', '', svg)
    s = re.sub(r'>\s+<', '><', s)
    return re.sub(r'\s+', ' ', s).strip()


def load_existing():
    """docs/fig 现有 svg 的规范化内容 -> 文件名。"""
    out = {}
    for name in sorted(os.listdir(FIG)):
        if not name.endswith('.svg'):
            continue
        with open(os.path.join(FIG, name), encoding='utf-8') as f:
            out.setdefault(norm(f.read()), name)
    return out


def write_both(name, data):
    for d in (FIG, ASSETS):
        p = os.path.join(d, name)
        mode = 'wb' if isinstance(data, bytes) else 'w'
        with open(p, mode, **({} if mode == 'wb' else {'encoding': 'utf-8'})) as f:
            f.write(data)


def main():
    args = sys.argv[1:]
    lessons = [int(a) for a in args] if args else list(range(20, 32))
    existing = load_existing()
    report = []
    for n in lessons:
        src = os.path.join(KE, '%d.html' % n)
        with open(src, encoding='utf-8') as f:
            html = f.read()
        # 每幅 SVG 归属最近的图位标题：义理图 / 附论 / 研究，其余做配图 p
        seq = {}
        for m in SVG_RE.finditer(html):
            svg = m.group(0)
            head = html[:m.start()]
            h2s = re.findall(r'<div class="h2"[^>]*>(.*?)</div>', head)
            title = re.sub(r'<[^>]+>', '', h2s[-1]) if h2s else ''
            if '义理图' in title:
                kind = 'yi'
            elif '附论' in title:
                kind = 'fu'
            elif '研究' in title:
                kind = 'yan'
            else:
                kind = 'p'
            seq[kind] = seq.get(kind, 0) + 1
            nk = norm(svg)
            if nk in existing:
                report.append((n, existing[nk], 'reuse · ' + title[:20]))
                continue
            name = 'ke%d-%s%d.svg' % (n, kind, seq[kind])
            write_both(name, svg.rstrip() + '\n')
            existing[nk] = name
            report.append((n, name, 'new · ' + title[:20]))
        m = IMG_RE.search(html)
        if m:
            raw = base64.b64decode(m.group(2), validate=False)
            try:
                from PIL import Image
                im = Image.open(io.BytesIO(raw)).convert('RGB')
                buf = io.BytesIO()
                im.save(buf, 'PNG', optimize=True)
                data = buf.getvalue()
                note = '%dx%d' % im.size
            except Exception as e:
                data = raw
                note = 'raw %s' % e
            name = 'ke%d-tu1.png' % n
            write_both(name, data)
            report.append((n, name, 'bitmap ' + note))
    for r in report:
        print('课%2d  %-22s %s' % (r[0], r[1], r[2]))
    print('共 %d 项' % len(report))


if __name__ == '__main__':
    main()
