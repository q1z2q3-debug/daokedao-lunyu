# -*- coding: utf-8 -*-
"""修正：COURSES 节号、合稿去重、索引重生成、验校。可重复执行。"""
import os, re, subprocess, json

ROOT = '/home/user/Doubao/chats/38450693190946306/daokedao-lunyu'
os.chdir(ROOT)
REF = {'249': '10.11', '250': '10.12', '251': '10.13', '252': '10.14', '253': '10.15'}

s = open('scripts/build_site.py', encoding='utf-8').read()
for no, ref in REF.items():
    s = re.sub(r'(\("' + no + r'", "[^"]*?（乡党)10\.[0-9]+(\)（阅读版）\.html")',
               lambda m: m.group(1) + ref + m.group(2), s)
open('scripts/build_site.py', 'w', encoding='utf-8').write(s)

# 合稿去重：同一 10.x 标题只留最后一次
BOOK = 'book/润泽说 道可道之论语·上论（已刊）.md'
bk = open(BOOK, encoding='utf-8').read()
for ref in ('10.11', '10.12', '10.13', '10.14', '10.15'):
    parts = re.split(r'(?=^## ' + ref.replace('.', r'\.') + r'　)', bk, flags=re.M)
    if len(parts) > 2:
        bk = parts[0] + ''.join(parts[1:])
open(BOOK, 'w', encoding='utf-8').write(bk)

for cmd in ('python3 scripts/build_site.py', 'python3 scripts/verify.py'):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(cmd, r.returncode, r.stdout[-200:], r.stderr[-300:])
    if r.returncode != 0:
        raise SystemExit(1)
