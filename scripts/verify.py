# -*- coding: utf-8 -*-
"""论语站点一致性校验（CI 与本地共用，零第三方依赖）。

用法：
  python3 scripts/verify.py
  python3 scripts/verify.py --quiet

校验项：
  1 VERSION 与入口页 bookEdition、卷首页脚一致，且已记入 CHANGELOG
  2 docs/ke/ 为 00-pre + 01..N 连续，无断号、无多余
  3 每课页含「第N课」与「第 N 课」两种写法，且含少儿页、成人页
  4 入口页链接覆盖全部课页与专题页；JSON-LD hasPart 顺序与课次一致
  5 docs 内本地链接无死链
  6 sitemap 覆盖全部课页
  7 图位数量不超过基线（scripts/expected.json），并在输出中报数
  8 页面引用的 fig/*.svg 均存在
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
KE = os.path.join(DOCS, 'ke')

CN = '〇一二三四五六七八九'
fails = []
notes = []


def cn(n):
    if n < 10:
        return CN[n]
    if n < 20:
        return '十' + (CN[n % 10] if n % 10 else '')
    return CN[n // 10] + '十' + (CN[n % 10] if n % 10 else '')


def check(cond, msg):
    if not cond:
        fails.append(msg)
    return cond


def main():
    ver = open(os.path.join(ROOT, 'VERSION'), encoding='utf-8').read().strip()
    idx = open(os.path.join(DOCS, 'index.html'), encoding='utf-8').read()
    book = open(os.path.join(DOCS, 'book.html'), encoding='utf-8').read()
    check(('v' + ver) in idx or ver in idx, '入口页未见版本号 %s' % ver)
    check(ver in book, '卷首页未见版本号 %s' % ver)
    cl = open(os.path.join(ROOT, 'CHANGELOG.md'), encoding='utf-8').read()
    check(ver in cl, 'CHANGELOG 首条未记 %s' % ver)

    ke_files = sorted(f for f in os.listdir(KE) if f.endswith('.html'))
    nums = [int(f[:2]) for f in ke_files if re.fullmatch(r'\d{2}\.html', f)]
    n = max(nums) if nums else 0
    check('00-pre.html' in ke_files, '缺 docs/ke/00-pre.html')
    check(nums == list(range(1, n + 1)), '课页号不连续：共 %d 个，最大 %d' % (len(nums), n))

    for i in range(1, n + 1):
        s = open(os.path.join(KE, '%02d.html' % i), encoding='utf-8').read()
        check(('第%s课' % cn(i)) in s or ('第%d课' % i) in s, '第 %d 课缺课次标注' % i)
        check(('第 %d 课' % i) in s, '第 %d 课页脚课次格式不符' % i)
        check('少儿页' in s and '成人页' in s, '第 %d 课缺少儿页或成人页' % i)

    links = re.findall(r'href="(ke/\d{2}-?[a-z]*\.html)"', idx)
    check(len(set(links)) == n + 1, '入口页课链接 %d 个 ≠ 课页 %d 个' % (len(set(links)), n + 1))
    zt = [f for f in os.listdir(os.path.join(DOCS, 'zt')) if f.endswith('.html')]
    check(len(re.findall(r'href="zt/\d+\.html"', idx)) >= len(zt), '入口页专题链接少于 %d 个' % len(zt))

    parts = re.findall(r'"@type":"Chapter","name":"([^"]*)","url":"[^"]*/ke/([^"]*)"', idx)
    order = [p[1] for p in parts]
    want = ['00-pre.html'] + ['%02d.html' % i for i in range(1, n + 1)]
    check(order == want, 'JSON-LD hasPart 顺序与课次不一致（%s…）' % '、'.join(order[:4]))

    missing = []
    for dirpath, _dirs, files in os.walk(DOCS):
        for f in files:
            if not f.endswith('.html'):
                continue
            s = open(os.path.join(dirpath, f), encoding='utf-8').read()
            for href in re.findall(r'href="([^"#?:]+\.html)"', s):
                t = os.path.normpath(os.path.join(dirpath, href.replace('%20', ' ')))
                if not os.path.exists(t):
                    missing.append(os.path.relpath(t, DOCS))
    check(not missing, '死链 %d 处：%s' % (len(missing), '、'.join(missing[:5])))

    sm = open(os.path.join(DOCS, 'sitemap.xml'), encoding='utf-8').read()
    for i in range(1, n + 1):
        check('/ke/%02d.html' % i in sm, 'sitemap 缺第 %d 课' % i)

    base = json.load(open(os.path.join(ROOT, 'scripts', 'expected.json'), encoding='utf-8'))
    ph = 0
    for f in ke_files:
        ph += open(os.path.join(KE, f), encoding='utf-8').read().count('class="ph"')
    limit = base.get('placeholders', 0)
    check(ph <= limit, '图位 %d 处 > 基线 %d（新增缺图未登记）' % (ph, limit))
    if ph < limit:
        notes.append('图位已减至 %d（基线 %d，可下调 expected.json）' % (ph, limit))
    notes.append('图位 %d/%d' % (ph, limit))

    figs = set(os.listdir(os.path.join(DOCS, 'fig')))
    bad = []
    for f in ke_files:
        s = open(os.path.join(KE, f), encoding='utf-8').read()
        for ref in re.findall(r'(?:src="|href=")\.?\.?/?fig/([^"]+)"', s):
            if ref not in figs:
                bad.append('%s→%s' % (f, ref))
    check(not bad, '缺图文件 %d 处：%s' % (len(bad), '、'.join(bad[:5])))

    notes.insert(0, '课页 %d（含前言）／图位 %d／版本 v%s' % (n + 1, ph, ver))
    if fails:
        print('FAIL（%d 项）' % len(fails))
        for m in fails:
            print('  - %s' % m)
        return 1
    if '--quiet' not in sys.argv:
        print('OK  ' + '；'.join(notes))
    return 0


if __name__ == '__main__':
    sys.exit(main())
