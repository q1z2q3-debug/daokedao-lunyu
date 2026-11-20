#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把各课母本 md 串成「已刊」母本（学而篇起，入为政篇）。

用法：python3 scripts/build_book_md.py
源：../润泽说-论语/前言-读论语之前.md、../润泽说-论语/单课/[12].N-*.md
产物：book/润泽说 道可道之论语·学而篇（已刊）.md
约定：各课原 `# 标题` 降为 `## 标题`；每课前加一行课次索引（便于目录生成）。
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.path.dirname(ROOT), "润泽说-论语")
OUT = os.path.join(ROOT, "book", "润泽说 道可道之论语·学而篇（已刊）.md")

HEAD = """---
title: 润泽说 道可道之论语
subtitle: 学而篇 · 通释读本（连载）
author: 润泽
base: 朱熹《论语集注》
chapters: 498
published: 前言 + 学而十六章 + 为政四章
version: 0.15.17
date: 2026-11-20
---

# 润泽说 道可道之论语 · 学而篇（已刊）

> 一章一课，一课两页：少儿页可念、成人页可考。
> 本册为连载中的第一批：前言一篇、学而十六章、为政三章。全书依朱熹本四百九十八章，按篇推进。

"""


def demote(text: str) -> str:
    """一级标题降为二级；二级降为三级，保持层级不跳。"""
    text = re.sub(r"^# (.+)$", r"## \1", text, flags=re.M)
    text = re.sub(r"^## (.+)$", r"### \1", text, flags=re.M)
    # 上面两步会连降，先整体后移再补回：改为逐行判断
    return text


def shift(text: str) -> str:
    out = []
    for line in text.split("\n"):
        if line.startswith("# "):
            out.append("## " + line[2:])
        elif line.startswith("## "):
            out.append("### " + line[3:])
        elif line.startswith("### "):
            out.append("#### " + line[4:])
        else:
            out.append(line)
    return "\n".join(out)


def main():
    parts = []
    pre = os.path.join(SRC, "前言-读论语之前.md")
    if os.path.exists(pre):
        txt = open(pre, encoding="utf-8").read()
        parts.append(shift(txt).strip())

    for path in sorted(glob.glob(os.path.join(SRC, "单课", "[12].*.md"))):
        txt = open(path, encoding="utf-8").read()
        parts.append(shift(txt).strip())

    body = "\n\n---\n\n".join(parts)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(HEAD + body + "\n")
    print("母本已生成：", OUT, len(body), "字")


if __name__ == "__main__":
    main()
