#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把各课母本 md 串成「已刊」母本（学而篇起，入为政篇、八佾篇、里仁篇）。

用法：python3 scripts/build_book_md.py
源：../润泽说-论语/前言-读论语之前.md、../润泽说-论语/单课/[123].N-*.md、manuscript/ba-yi/NN-*.md（3.4 起）
产物：book/润泽说 道可道之论语·上论（已刊）.md
约定：各课原 `# 标题` 降为 `## 标题`；每课前加一行课次索引（便于目录生成）。
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.path.dirname(ROOT), "润泽说-论语")
OUT = os.path.join(ROOT, "book", "润泽说 道可道之论语·上论（已刊）.md")

HEAD = """---
title: 润泽说 道可道之论语
subtitle: 上论 · 通释读本（连载）
author: 润泽
base: 朱熹《论语集注》
chapters: 498
published: 前言 + 学而十六章 + 为政二十四章 + 八佾二十六章 + 里仁五章
version: 0.15.59
date: 2026-11-25
---

# 润泽说 道可道之论语 · 上论（已刊）

> 一章一课，一课两页：少儿页可念、成人页可考。
> 本册为连载中的第一批：前言一篇、学而十六章、为政二十四章、八佾二十六章、里仁五章。全书依朱熹本四百九十八章，按篇推进。

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

    def _k(path):
        m = re.match(r"(\d+)\.(\d+)-", os.path.basename(path))
        return (int(m.group(1)), int(m.group(2))) if m else (99, 99)

    for path in sorted(glob.glob(os.path.join(SRC, "单课", "[123].*.md")), key=_k):
        txt = open(path, encoding="utf-8").read()
        parts.append(shift(txt).strip())

    # 3.4 起（第 43 课以后）的母本入库于 manuscript/ba-yi/NN-*.md
    def _k3(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (3, int(m.group(1)) - 39) if m else (99, 99)

    for path in sorted(glob.glob(os.path.join(ROOT, "manuscript", "ba-yi", "*.md")), key=_k3):
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        # 统一课标题体例：「## 第 43 课 · 林放问礼之本」→「## 3.4　林放问礼之本」
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 3.%d　%s" % (int(m.group(1)) - 39, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 里仁篇（4.1 起）母本入库于 manuscript/li-ren/NN-*.md，课号 66 对应 4.1
    def _k4(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (4, int(m.group(1)) - 65) if m else (99, 99)

    for path in sorted(glob.glob(os.path.join(ROOT, "manuscript", "li-ren", "*.md")), key=_k4):
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 4.%d　%s" % (int(m.group(1)) - 65, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    body = "\n\n---\n\n".join(parts)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(HEAD + body + "\n")
    print("母本已生成：", OUT, len(body), "字")


if __name__ == "__main__":
    main()
