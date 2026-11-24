# -*- coding: utf-8 -*-
"""第 47–48 课（八佾 3.8 绘事后素 / 3.9 夏礼能言）阅读版生成器。

- 模板前缀取 docs/ke/48.html 的 head+CSS（`<div class="wrap">` 之前的部分，含开标签）。
- 正文基准逐字取自 docs/ke/47.html、docs/ke/48.html；47 仅做两处定点替换
  （连读小标题、连读句），48 原样不动。
- 页脚版本号读站点根 VERSION 动态写入 `v{版本}`，不硬编码版本号。
- 每次都从 docs 参考页重新取文，重复运行幂等，不累积 CSS。
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = open(f'{ROOT}/VERSION', encoding='utf-8').read().strip()

MARK = '<div class="wrap">'

# 模板 PREFIX：48.html 的 head+CSS（含 wrap 开标签）
_tpl = open(f'{ROOT}/docs/ke/48.html', encoding='utf-8').read()
_i = _tpl.find(MARK)
PREFIX = _tpl[:_i + len(MARK)]

OLD_SENTENCE = '上一章讲射：标准要立对。此章讲绘：底色要先有。两章都在说「先后」——礼不是第一层，礼是第二层；第一层是人的质地。'
NEW_SENTENCE = '上一章讲争：争可入礼，争而不离让；此章讲绘：底色要先有。两章都在说先后——礼不是第一层，礼是第二层。'

LESSONS = [
    {
        'lesson': 47,
        'ref': 'docs/ke/47.html',
        'title': '润泽说 道可道之论语 · 第四十七课 绘事后素（八佾 3.8）',
        'repl': [
            ('连读：从射到绘', '连读：从争到绘'),
            (OLD_SENTENCE, NEW_SENTENCE),
        ],
    },
    {
        'lesson': 48,
        'ref': 'docs/ke/48.html',
        'title': '润泽说 道可道之论语 · 第四十八课 夏礼能言（八佾 3.9）',
        'repl': [],
    },
]

for cfg in LESSONS:
    ref = open(f'{ROOT}/{cfg["ref"]}', encoding='utf-8').read()
    j = ref.find(MARK)
    ref_prefix, body = ref[:j], ref[j + len(MARK):]

    # description 逐字取自参考页现成那一条
    m = re.search(r'name="description" content="([^"]*)"', ref_prefix)
    desc = m.group(1)

    html = PREFIX
    html = re.sub(r'<title>.*?</title>', f'<title>{cfg["title"]}</title>', html, count=1)
    html = re.sub(r'(name="description" content=")[^"]*(")',
                  lambda mm: mm.group(1) + desc + mm.group(2), html, count=1)

    for old, new in cfg['repl']:
        assert body.count(old) == 1, f'第 {cfg["lesson"]} 课待替换串出现 {body.count(old)} 次：{old[:20]}'
        body = body.replace(old, new)

    # 页脚版本：动态读 VERSION，不硬写版本号
    body = re.sub(r'v\d+\.\d+\.\d+', f'v{VER}', body)

    html += body
    os.makedirs(f'{ROOT}/src/html', exist_ok=True)
    out = f'{ROOT}/src/html/ke-{cfg["lesson"]}.html'
    open(out, 'w', encoding='utf-8').write(html)
    print(cfg['lesson'], len(html))
