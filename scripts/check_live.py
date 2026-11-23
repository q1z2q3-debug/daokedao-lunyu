# -*- coding: utf-8 -*-
"""论语线上站点核对（CI 定时任务与本地共用，零依赖）。

用法：
  python3 scripts/check_live.py          查入口、卷首
  python3 scripts/check_live.py --all    再加全部课页与专题页

判定：HTTP 200；入口与卷首另比对 content-length 与仓库内文件字节数。
Pages 有部署延迟，默认 6 次 × 30 秒重试。
"""
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://q1z2q3-debug.github.io/daokedao-lunyu/'
RETRY, INTERVAL = 6, 30


def head(url):
    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'lunyu-ci'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, int(r.headers.get('content-length') or 0)


def wait(path, expect=None):
    url = BASE + path + '?cb=%d' % int(time.time())
    last = None
    for i in range(RETRY):
        try:
            code, size = head(url)
            last = (code, size)
            if code == 200 and (expect is None or size == expect):
                return True, last
        except Exception as e:  # noqa: BLE001
            last = ('ERR', str(e)[:60])
        if i < RETRY - 1:
            time.sleep(INTERVAL)
            url = BASE + path + '?cb=%d' % int(time.time())
    return False, last


def main():
    fails = []
    for path, local in (('index.html', 'docs/index.html'), ('book.html', 'docs/book.html')):
        expect = os.path.getsize(os.path.join(ROOT, local))
        ok, info = wait(path, expect)
        print('%-13s' % path, 'OK' if ok else 'FAIL', info, '本地 %d' % expect)
        if not ok:
            fails.append(path)

    if '--all' in sys.argv:
        pages = ['ke/' + f for f in sorted(os.listdir(os.path.join(ROOT, 'docs', 'ke')))]
        pages += ['zt/' + f for f in sorted(os.listdir(os.path.join(ROOT, 'docs', 'zt')))]
        for p in pages:
            ok, info = wait(p)
            print('%-18s' % p, 'OK' if ok else 'FAIL', info)
            if not ok:
                fails.append(p)

    if fails:
        print('FAIL: %s' % '、'.join(fails))
        return 1
    print('OK 线上与仓库一致')
    return 0


if __name__ == '__main__':
    sys.exit(main())
