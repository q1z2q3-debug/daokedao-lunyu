#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把各课母本 md 串成「已刊」母本（学而篇起，入为政篇、八佾篇、里仁篇）。

用法：python3 scripts/build_book_md.py
源：../润泽说-论语/前言-读论语之前.md、../润泽说-论语/单课/[123].N-*.md、manuscript/ba-yi/NN-*.md（3.4 起）
产物：book/润泽说 道可道之论语（已刊）.md
约定：各课原 `# 标题` 降为 `## 标题`；每课前加一行课次索引（便于目录生成）。
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.path.dirname(ROOT), "润泽说-论语")
OUT = os.path.join(ROOT, "book", "润泽说 道可道之论语（已刊）.md")

HEAD = """---
title: 润泽说 道可道之论语
subtitle: 通释读本（连载）
author: 润泽
base: 朱熹《论语集注》
chapters: 498
published: {published}
version: {version}
date: 2026-11-26
---

# 润泽说 道可道之论语（已刊）

> 一章一课，一课两页：少儿页可念、成人页可考。
> 本册为连载中的一批：{detail}。全书依朱熹本四百九十八章，按篇推进。

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

    li = sorted(glob.glob(os.path.join(ROOT, "manuscript", "li-ren", "*.md")), key=_k4)
    for path in li:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 4.%d　%s" % (int(m.group(1)) - 65, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 公冶长篇（5.1 起）母本入库于 manuscript/gong-ye-chang/NN-*.md，课号 92 对应 5.1
    def _k5(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (5, int(m.group(1)) - 91) if m else (99, 99)

    gy = sorted(glob.glob(os.path.join(ROOT, "manuscript", "gong-ye-chang", "*.md")), key=_k5)
    for path in gy:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 5.%d　%s" % (int(m.group(1)) - 91, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 雍也篇（6.1 起）母本入库于 manuscript/yong-ye/NN-*.md，课号 120 对应 6.1
    def _k6(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (6, int(m.group(1)) - 119) if m else (99, 99)

    yy = sorted(glob.glob(os.path.join(ROOT, "manuscript", "yong-ye", "*.md")), key=_k6)
    for path in yy:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 6.%d　%s" % (int(m.group(1)) - 119, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 述而篇（7.1 起）母本入库于 manuscript/shu-er/NN-*.md，课号 150 对应 7.1
    def _k7(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (7, int(m.group(1)) - 149) if m else (99, 99)

    se = sorted(glob.glob(os.path.join(ROOT, "manuscript", "shu-er", "*.md")), key=_k7)
    for path in se:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 7.%d　%s" % (int(m.group(1)) - 149, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 泰伯篇（8.1 起）母本入库于 manuscript/tai-bo/NN-*.md，课号 188 对应 8.1
    def _k8(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (8, int(m.group(1)) - 187) if m else (99, 99)

    tb = sorted(glob.glob(os.path.join(ROOT, "manuscript", "tai-bo", "*.md")), key=_k8)
    for path in tb:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 8.%d　%s" % (int(m.group(1)) - 187, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 子罕篇（9.1 起）母本入库于 manuscript/zi-han/NN-*.md，课号 209 对应 9.1
    def _k9(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (9, int(m.group(1)) - 208) if m else (99, 99)

    zh = sorted(glob.glob(os.path.join(ROOT, "manuscript", "zi-han", "*.md")), key=_k9)
    for path in zh:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 9.%d　%s" % (int(m.group(1)) - 208, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 乡党篇（10.1 起）母本入库于 manuscript/xiang-dang/NN-*.md，课号 239 对应 10.1
    def _k10(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (10, int(m.group(1)) - 238) if m else (99, 99)

    xd = sorted(glob.glob(os.path.join(ROOT, "manuscript", "xiang-dang", "*.md")), key=_k10)
    for path in xd:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 10.%d　%s" % (int(m.group(1)) - 238, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 先进篇（11.1 起）母本入库于 manuscript/xian-jin/NN-*.md，课号 266 对应 11.1
    def _k11(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (11, int(m.group(1)) - 265) if m else (99, 99)

    xj = sorted(glob.glob(os.path.join(ROOT, "manuscript", "xian-jin", "*.md")), key=_k11)
    for path in xj:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 11.%d　%s" % (int(m.group(1)) - 265, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 颜渊篇（12.1 起）母本入库于 manuscript/yan-yuan/NN-*.md，课号 292 对应 12.1
    def _k12(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (12, int(m.group(1)) - 291) if m else (99, 99)

    yy2 = sorted(glob.glob(os.path.join(ROOT, "manuscript", "yan-yuan", "*.md")), key=_k12)
    for path in yy2:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 12.%d　%s" % (int(m.group(1)) - 291, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 子路篇（13.1 起）母本入库于 manuscript/zi-lu/NN-*.md，课号 316 对应 13.1
    def _k13(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (13, int(m.group(1)) - 315) if m else (99, 99)

    zl = sorted(glob.glob(os.path.join(ROOT, "manuscript", "zi-lu", "*.md")), key=_k13)
    for path in zl:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 13.%d　%s" % (int(m.group(1)) - 315, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 宪问篇（14.1 起）母本入库于 manuscript/xian-wen/NN-*.md，课号 346 对应 14.1
    def _k14(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (14, int(m.group(1)) - 345) if m else (99, 99)

    xw = sorted(glob.glob(os.path.join(ROOT, "manuscript", "xian-wen", "*.md")), key=_k14)
    for path in xw:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 14.%d　%s" % (int(m.group(1)) - 345, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 卫灵公篇（15.1 起）母本入库于 manuscript/wei-ling-gong/NN-*.md，课号 390 对应 15.1
    def _k15(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (15, int(m.group(1)) - 389) if m else (99, 99)

    wlg = sorted(glob.glob(os.path.join(ROOT, "manuscript", "wei-ling-gong", "*.md")), key=_k15)
    for path in wlg:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 15.%d　%s" % (int(m.group(1)) - 389, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 季氏篇（16.1 起）母本入库于 manuscript/ji-shi/NN-*.md，课号 432 对应 16.1
    def _k16(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (16, int(m.group(1)) - 431) if m else (99, 99)

    js = sorted(glob.glob(os.path.join(ROOT, "manuscript", "ji-shi", "*.md")), key=_k16)
    for path in js:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 16.%d　%s" % (int(m.group(1)) - 431, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 阳货篇（17.1 起）母本入库于 manuscript/yang-huo/NN-*.md，课号 446 对应 17.1
    def _k17(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (17, int(m.group(1)) - 445) if m else (99, 99)

    yh = sorted(glob.glob(os.path.join(ROOT, "manuscript", "yang-huo", "*.md")), key=_k17)
    for path in yh:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 17.%d　%s" % (int(m.group(1)) - 445, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 微子篇（18.1 起）母本入库于 manuscript/wei-zi/NN-*.md，课号 472 对应 18.1
    def _k18(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (18, int(m.group(1)) - 471) if m else (99, 99)

    wz = sorted(glob.glob(os.path.join(ROOT, "manuscript", "wei-zi", "*.md")), key=_k18)
    for path in wz:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 18.%d　%s" % (int(m.group(1)) - 471, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 子张篇（19.1 起）母本入库于 manuscript/zi-zhang/NN-*.md，课号 483 对应 19.1
    def _k19(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (19, int(m.group(1)) - 482) if m else (99, 99)

    zz = sorted(glob.glob(os.path.join(ROOT, "manuscript", "zi-zhang", "*.md")), key=_k19)
    for path in zz:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 19.%d　%s" % (int(m.group(1)) - 482, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    # 尧曰篇（20.1 起）母本入库于 manuscript/yao-yue/NN-*.md，课号 508 对应 20.1
    def _k20(path):
        m = re.match(r"(\d+)-", os.path.basename(path))
        return (20, int(m.group(1)) - 507) if m else (99, 99)

    yyue = sorted(glob.glob(os.path.join(ROOT, "manuscript", "yao-yue", "*.md")), key=_k20)
    for path in yyue:
        txt = open(path, encoding="utf-8").read()
        txt = shift(txt)
        txt = re.sub(r"^## 第 (\d+) 课 · (.+)$",
                     lambda m: "## 20.%d　%s" % (int(m.group(1)) - 507, m.group(2)), txt, count=1, flags=re.M)
        parts.append(txt.strip())

    body = "\n\n---\n\n".join(parts)

    version = open(os.path.join(ROOT, "VERSION"), encoding="utf-8").read().strip()

    def cn(n):
        d = "零一二三四五六七八九"
        if n < 10:
            return d[n]
        if n < 20:
            return "十" + (d[n % 10] if n % 10 else "")
        return d[n // 10] + "十" + (d[n % 10] if n % 10 else "")
    seg = ["前言一篇", "学而十六章", "为政二十四章", "八佾二十六章"]
    if li:
        seg.append("里仁%s章" % cn(len(li)))
    if gy:
        seg.append("公冶长%s章" % cn(len(gy)))
    if yy:
        seg.append("雍也%s章" % cn(len(yy)))
    if se:
        seg.append("述而%s章" % cn(len(se)))
    if tb:
        seg.append("泰伯%s章" % cn(len(tb)))
    if zh:
        seg.append("子罕%s章" % cn(len(zh)))
    if xd:
        seg.append("乡党%s节" % cn(len(xd)))
    if xj:
        seg.append("先进%s章" % cn(len(xj)))
    if yy2:
        seg.append("颜渊%s章" % cn(len(yy2)))
    if zl:
        seg.append("子路%s章" % cn(len(zl)))
    if xw:
        seg.append("宪问%s章" % cn(len(xw)))
    if wlg:
        seg.append("卫灵公%s章" % cn(len(wlg)))
    if js:
        seg.append("季氏%s章" % cn(len(js)))
    if yh:
        seg.append("阳货%s章" % cn(len(yh)))
    if zz:
        seg.append("子张%s章" % cn(len(zz)))
    if yyue:
        seg.append("尧曰%s章" % cn(len(yyue)))
    published = " + ".join(seg) if len(seg) - 4 else " + ".join(seg)
    head = HEAD.format(published=published, version=version, detail="、".join(seg))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(head + body + "\n")
    print("母本已生成：", OUT, len(body), "字")


if __name__ == "__main__":
    main()
