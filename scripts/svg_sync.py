#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""义理图 SVG 同步：以阅读版 HTML 为准，导出独立 .svg 到 assets/。

用法：
    python3 scripts/svg_sync.py                 # 同步现有四课
    python3 scripts/svg_sync.py 论语·第四课*.html

规矩（2026-11-19 定）：页面内嵌 SVG 是唯一源；assets/*.svg 只是它的副本，
改图先改页面，再跑本脚本，禁止两边各改一遍。
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# aria-label 关键字 -> 文件名（不含目录与扩展名）。顺序不限，按关键字匹配。
MAP = {
    "pre": [
        ("五步读法", "论语-前言-五步读法"),
    ],
    "1.1": [
        ("有朋自远方来", "论语-1.1-朋来图"),
        ("认知的三重证明", "论语-1.1-三证图"),
        ("认知之圆", "论语-1.1-认知之圆"),
        ("学是移界", "论语-1.1-学教图"),
        ("一课之纲", "论语-1.1-总纲图"),
    ],
    "1.2": [
        ("本立道生", "论语-1.2-本立道生"),
        ("活根与死桩", "论语-1.2-活根死桩"),
    ],
    "1.3": [
        ("一力两途", "论语-1.3-一力两途"),
        ("粉饰之墙", "论语-1.3-粉饰之墙"),
        ("鲜不是零", "论语-1.3-鲜不是零"),
    ],
    "1.4": [
        ("三问三关", "论语-1.4-三问三关"),
        ("查事与定罪", "论语-1.4-查事定罪"),
    ],
    "1.5": [
        ("五事一条链", "论语-1.5-五事一条链"),
        ("不欺与不竭", "论语-1.5-不欺与不竭"),
    ],
    "1.6": [
        ("七事三层", "论语-1.6-七事三层"),
        ("文灭其质", "论语-1.6-两偏之间"),
    ],
}

STYLE_RE = re.compile(r'\s+style="width:100%;max-width:580px;display:block;margin:0 auto;height:auto"')


def clean(svg: str) -> str:
    svg = STYLE_RE.sub("", svg)
    if "xmlns=" not in svg.split(">")[0]:
        svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    return svg


def sync(html_path: str) -> int:
    base = os.path.basename(html_path)
    m = re.search(r"([0-9]+\.[0-9]+)", base)
    course = m.group(1) if m else None
    if course is None and "前言" in base:
        course = "pre"
    if course is None:
        for cn, cx in (("一", "1.1"), ("二", "1.2"), ("三", "1.3"), ("四", "1.4"), ("五", "1.5"), ("六", "1.6"), ("七", "1.7"), ("八", "1.8"), ("九", "1.9"), ("十", "1.10")):
            if f"第{cn}课" in base:
                course = cx
                break
    if course not in MAP:
        print(f"[skip] {base}：未登记第 {course} 课，先在 MAP 里加映射")
        return 0
    html = open(html_path, encoding="utf-8").read()
    svgs = re.findall(r"<svg viewBox.*?</svg>", html, re.S)
    written = 0
    for key, name in MAP[course]:
        hit = [s for s in svgs if key in s.split(">")[0]]
        if not hit:
            print(f"[warn] {course}：页面里找不到「{key}」")
            continue
        out = os.path.join(ROOT, "assets", name + ".svg")
        open(out, "w", encoding="utf-8").write(
            '<?xml version="1.0" encoding="UTF-8"?>\n' + clean(hit[0]) + "\n"
        )
        print(f"[ok] {name}.svg  {len(hit[0])} chars")
        written += 1
    return written


def main():
    args = sys.argv[1:]
    if args:
        paths = []
        for a in args:
            paths.extend(glob.glob(os.path.join(ROOT, a)))
    else:
        paths = sorted(glob.glob(os.path.join(ROOT, "论语·第*课*（阅读版）.html")))
    total = 0
    for p in paths:
        total += sync(p)
    print(f"共导出 {total} 张")


if __name__ == "__main__":
    main()
