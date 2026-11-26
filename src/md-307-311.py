# -*- coding: utf-8 -*-
"""把第 307–311 课的 L 数据落成母本 markdown（manuscript/yan-yuan/NN-*.md）。"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = open(os.path.join(ROOT, 'VERSION'), encoding='utf-8').read().strip()

p = os.path.join(ROOT, 'src', 'ke-307-311.py')
NS = {'__name__': 'gen', '__file__': p}
exec(compile(open(p, encoding='utf-8').read(), p, 'exec'), NS)
LESSONS = NS['LESSONS']

SLUG = {307: 'cheng-ren-zhi-mei', 308: 'zheng-zhe-zheng-ye', 309: 'huan-dao', 310: 'yan-yong-sha', 311: 'wen-yu-da'}
FIG = {307: ('ke307-yi-fu-yi-tui','ke307-fen-shui-ling'),
        308: ('ke308-yi-shuai-yi-sui','ke308-shuai-zi-shi-yan'),
        309: ('ke309-yi-cang-yi-gou','ke309-ben-mo'),
        310: ('ke310-feng-guo-cao-yan','ke310-ge-yu-chui'),
        311: ('ke311-liang-fu-hua-xiang','ke311-ming-shi')}



def kv(items):
    return [('- **%s**：%s' % (a, b)) for a, b in items]


def bullets(items):
    return ['- ' + x for x in items]


def build_md(L):
    no = L['no']
    f1, f2 = FIG[no]
    lines = []
    lines.append('# 第 %d 课 · %s' % (no, L['title']))
    lines.append('')
    lines.append('> %s　%s　第 %d 课' % (L['pian'], L['ref'], no))
    lines.append('>')
    lines.append('> 原文：%s' % L['yi'])
    lines.append('')
    lines.append('## 少儿页')
    lines.append('')
    lines.append('### 四个关键字')
    lines.append('')
    lines.append('\n'.join(kv(L['kws'])))
    lines.append('')
    lines.append('### 一句话讲清')
    lines.append('')
    lines.append(L['one'])
    lines.append('')
    lines.append('### 字义小窗')
    lines.append('')
    lines.append('\n'.join(kv(L['words'])))
    lines.append('')
    lines.append('### 共读')
    lines.append('')
    lines.extend(L['read'])
    lines.append('')
    lines.append('### 生活里的一天')
    lines.append('')
    lines.extend(bullets(L['life']))
    lines.append('')
    lines.append('### 三个小问题')
    lines.append('')
    lines.append('\n'.join(kv(L['ask'])))
    lines.append('')
    lines.append('### 成长小启示')
    lines.append('')
    lines.append('\n'.join(kv(L['grow'])))
    lines.append('')
    lines.append('## 成人页')
    lines.append('')
    lines.append('### 连读')
    lines.append('')
    lines.append(L['lian'])
    lines.append('')
    lines.append('### 字义句读')
    lines.append('')
    lines.append('\n'.join(kv(L['adult_words'])))
    lines.append('')
    lines.append('### 两读')
    lines.append('')
    lines.append('\n\n'.join('- ' + x for x in L['reads']))
    lines.append('')
    lines.append('### 章旨')
    lines.append('')
    lines.append(L['gist'])
    lines.append('')
    lines.append('### 三层')
    lines.append('')
    lines.append('\n'.join(kv(L['layers'])))
    lines.append('')
    lines.append(L['layer_note'])
    lines.append('')
    lines.append('### 存疑')
    lines.append('')
    lines.append('\n\n'.join('- ' + x for x in L['doubts']))
    lines.append('')
    lines.append('### 双卡')
    lines.append('')
    lines.append('\n\n'.join('- %s ↔ %s' % (a, b) for a, b in L['cards']))
    lines.append('')
    lines.append('### 跨典')
    lines.append('')
    lines.append('\n\n'.join('- %s ↔ %s' % (a, b) for a, b in L['cross']))
    lines.append('')
    capname = L['cap'].split(' · ', 1)[1]
    lines.append('### 图一　%s' % capname)
    lines.append('')
    lines.append('- **图注**：%s' % L['cap'])
    lines.append('- **画面**：%s' % L['ph'])
    lines.append('- **提示词**：见 `docs/ke/%d.html` 页内「提示词（存档）」。' % no)
    lines.append('')
    lines.append('### 义理图一')
    lines.append('')
    lines.append('- **图**：%s' % L['svg1cap'].split(' · ', 1)[1])
    lines.append('- **SVG**：见 `docs/ke/%d.html` 页内，另见 `docs/fig/%s.svg`' % (no, f1))
    lines.append('')
    lines.append('### 义理图二')
    lines.append('')
    lines.append('- **图**：%s' % L['svg2cap'].split(' · ', 1)[1])
    lines.append('- **SVG**：见 `docs/ke/%d.html` 页内，另见 `docs/fig/%s.svg`' % (no, f2))
    lines.append('')
    lines.append('### 附论一')
    lines.append('')
    lines.append(L['extra1'])
    lines.append('')
    lines.append('### 附论二')
    lines.append('')
    lines.append(L['extra2'])
    lines.append('')
    st = [s for s in L['stats'] if s[0] not in ('命令', '要核')]
    if st:
        lines.append('**数证**（底本 refs/lunyu-baiwen.txt，白文全本繁简互校）：')
        lines.append('')
        lines.append('\n'.join(kv(st)))
        lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('润泽说 · 道可道之论语 · v%s　底本：朱熹《论语集注》' % VER)
    lines.append('')
    return '\n'.join(lines)


for L in LESSONS:
    out = os.path.join(ROOT, 'manuscript', 'yan-yuan', '%d-%s.md' % (L['no'], SLUG[L['no']]))
    open(out, 'w', encoding='utf-8').write(build_md(L))
    print('写', os.path.relpath(out, ROOT), os.path.getsize(out))
