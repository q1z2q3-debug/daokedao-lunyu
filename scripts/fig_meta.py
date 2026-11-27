#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""旧版式课页的内联 SVG 元信息补齐：xmlns / role / aria-label，幂等可重跑。

- xmlns：早期页（第 26–31 课）的 <svg> 未声明命名空间，页内显示正常（HTML 解析隐含），
  但导出成独立 .svg 文件后打不开，故补齐。
- role/aria-label：第 20–25 课缺；取该图位所属 <div class="h2"> 标题为标签。
  页面内是图源（规矩），此脚本只补属性，不动图形与坐标。

用法：
    python3 scripts/fig_meta.py            # 20–31 课
    python3 scripts/fig_meta.py 26 29
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KE = os.path.join(ROOT, 'docs', 'ke')

SVG_OPEN = re.compile(r'<svg\b([^>]{0,400})>')
H2 = re.compile(r'<div class="h2"[^>]*>(.*?)</div>', re.S)
NS = 'xmlns="http://www.w3.org/2000/svg"'


def clean(t):
    t = re.sub(r'<[^>]+>', '', t)
    t = t.replace('　', ' ')
    t = re.sub(r'\s+', ' ', t).strip()
    return t.replace('"', '＂')


def patch(html):
    changed = []

    def repl(m):
        attrs = m.group(1)
        head = html[:m.start()]
        h2s = H2.findall(head)
        title = clean(h2s[-1]) if h2s else ''
        add = []
        if 'xmlns=' not in attrs:
            add.append(NS)
        if 'role=' not in attrs:
            add.append('role="img"')
        if 'aria-label=' not in attrs and title:
            add.append('aria-label="%s"' % title)
            changed.append(title)
        if not add:
            return m.group(0)
        # xmlns 紧跟 viewBox，其余续在其后，保持可读
        if NS in add:
            body = re.sub(r'(viewBox="[^"]*")', r'\1 ' + NS, attrs, count=1)
            if NS not in body:
                body = ' ' + NS + attrs
        else:
            body = attrs
        rest = [a for a in add if a != NS]
        if rest:
            body = body.rstrip() + ' ' + ' '.join(rest)
        return '<svg' + body + '>'

    return SVG_OPEN.sub(repl, html), changed


def main():
    args = sys.argv[1:]
    lessons = [int(a) for a in args] if args else list(range(20, 32))
    for n in lessons:
        p = os.path.join(KE, '%d.html' % n)
        with open(p, encoding='utf-8') as f:
            html = f.read()
        new, changed = patch(html)
        if new != html:
            with open(p, 'w', encoding='utf-8') as f:
                f.write(new)
            print('课%2d 已补 %d 处 %s' % (n, len(changed), '／'.join(zh[:12] for zh in changed[:2])))
        else:
            print('课%2d 无需改动' % n)


if __name__ == '__main__':
    main()
