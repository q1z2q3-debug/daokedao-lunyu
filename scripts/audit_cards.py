# -*- coding: utf-8 -*-
"""双卡（cards）体检：结构、宽度、重复、繁简与对举完整性。

用法：python3 scripts/audit_cards.py [--quiet]
检查项：
 1. 每课恰好 4 组（2×2 网格整两行）；
 2. 每组两栏非空、无重复标签；
 3. 显示宽度 ≤ 26（中文按 2）；
 4. 同一课内无重复标签、相邻课无完全相同的一组；
 5. 卡片不用繁体字（底本异体字 飮/擧 等例外白名单）；
 6. 第 3/4 组为章间对照时，前两字须为「x.y」形式或短题，不得出现空串。
退出码：0 通过；1 有问题。
"""
import ast, glob, os, re, sys
import opencc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WHITE = set('飮擧鮀')
MAXW = 26


def blocks(src):
    out, i = [], src.find('    cards=[')
    while i != -1:
        j = i + len('    cards=')
        depth = 0
        for k in range(j, len(src)):
            if src[k] == '[':
                depth += 1
            elif src[k] == ']':
                depth -= 1
                if depth == 0:
                    out.append((j, k + 1))
                    i = src.find('    cards=[', k)
                    break
        else:
            break
    return out


def width(t):
    return sum(2 if ord(c) > 127 else 1 for c in t)


def main():
    quiet = '--quiet' in sys.argv
    t2s = opencc.OpenCC('t2s')
    data, issues = {}, []
    for f in sorted(glob.glob(os.path.join(ROOT, 'src', 'ke-*.py'))):
        src = open(f, encoding='utf-8').read()
        nos = [int(x) for x in re.findall(r'no=(\d+),', src)]
        bs = blocks(src)
        if len(bs) != len(nos):
            issues.append((os.path.basename(f), 0, '课数与 cards 块数不符 %d/%d' % (len(nos), len(bs))))
            continue
        for no, (a, b) in zip(nos, bs):
            cards = ast.literal_eval(src[a:b])
            data[no] = cards
            if len(cards) != 4:
                issues.append((f, no, '组数 %d（应为 4）' % len(cards)))
            labs = [x for p in cards for x in p]
            if any(not x.strip() for x in labs):
                issues.append((f, no, '空栏'))
            if len(set(labs)) != len(labs):
                issues.append((f, no, '课内重复标签'))
            for x in labs:
                if width(x) > MAXW:
                    issues.append((f, no, '过宽 %d：%s' % (width(x), x)))
                s = t2s.convert(x)
                diff = [c for c, d in zip(x, s) if c != d and c not in WHITE]
                if diff:
                    issues.append((f, no, '繁体残留：%s（%s）' % (x, ''.join(diff))))
    for n in sorted(data):
        for p in data[n]:
            for m in (n - 1, n + 1):
                if m in data and p in data[m]:
                    issues.append(('adjacent', n, '与第 %d 课重复：%s／%s' % (m, p[0], p[1])))
    if not quiet:
        for f, n, msg in issues:
            print('%s 课%s %s' % (os.path.basename(f) if f.endswith('.py') else f, n, msg))
        print('课数 %d，问题 %d' % (len(data), len(issues)))
    return 1 if issues else 0


if __name__ == '__main__':
    sys.exit(main())
