# -*- coding: utf-8 -*-
"""把 docs/ 阅读版装进 APK 资产（dist/apk-lunyu/app/src/main/assets），可复跑。

只搬离线读得到的部分：首页、卷首、511 课（ke/）、专题（zt/）、图标与 manifest。
fig/ 不入包——课页插图已是内嵌 data:image/webp，无需外链文件。
同时把站内绝对地址改相对、去掉外部字体样式表，保证断网可读。
"""
import os, re, shutil, subprocess, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
ASSETS = os.path.join(ROOT, 'dist', 'apk-lunyu', 'app', 'src', 'main', 'assets')

SITE = 'https://q1z2q3-debug.github.io/daokedao-lunyu/'
SITE_BARE = 'https://q1z2q3-debug.github.io/daokedao-lunyu'
FONT_LINK_RE = re.compile(r'[ \t]*<link[^>]*fonts/css2[^>]*>\s*\n?')


def copy_tree(src, dst, skip=()):
    """按需复制目录，跳过 _shots/_history 这类工作稿。"""
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*skip))


ROOT_ABS = '/daokedao-lunyu/'
SITEMAP_LINK = re.compile(r'<a href="sitemap\.xml">站点地图</a>')
APK_DL = re.compile(r'<!-- apk-dl:start -->[\s\S]*?<!-- apk-dl:end -->\n?')


def rewrite_html(path, depth):
    """depth=head 相对 assets 根的层数；裸 index.html、根绝对路径都要按层补 ../。"""
    prefix = '../' * depth
    s = open(path, encoding='utf-8').read()
    n_site = (s.count(SITE) + s.count(SITE_BARE)
              + s.count(ROOT_ABS) + s.count('index.html">'))
    s = s.replace(SITE, prefix)
    s = s.replace(SITE_BARE, prefix + 'index.html')
    s = s.replace(ROOT_ABS, prefix)
    # ke/、zt/ 里回首页的裸 index.html 需补层
    if prefix:
        s = s.replace('href="index.html"', 'href="%sindex.html"' % prefix)
    s, n_map = SITEMAP_LINK.subn('', s)
    s = APK_DL.sub('', s)
    s, n_font = FONT_LINK_RE.subn('', s)
    if n_site or n_font or n_map:
        open(path, 'w', encoding='utf-8').write(s)
    return n_site, n_font



# ---- 衬线字体内嵌：安卓无「Noto Serif SC」，不嵌则落回黑体，失纸墨味 ----
SERIF = {
    '400': ('/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc', 2),
    '700': ('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc', 2),
}
FONT_STYLE = (
    '<style id="lunyu-serif">'
    '%s'
    '</style>\n</head>'
)
FACE = ('@font-face{font-family:"Noto Serif SC";font-style:normal;font-weight:%s;'
        'font-display:swap;src:url("%sfonts/lunyu-serif-%s.woff2") format("woff2")}')


def collect_chars():
    chars = set('　-~\u00a0\u3000'
                '，。、；：？！“”‘’（）《》〈〉「」『』【】…—～·・％‰')
    for dirpath, _, files in os.walk(ASSETS):
        for f in files:
            if not f.endswith('.html'):
                continue
            s = open(os.path.join(dirpath, f), encoding='utf-8').read()
            s = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', '', s)
            s = re.sub(r'<[^>]+>', '', s)
            s = s.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            chars |= set(s)
    chars = {c for c in chars if c.isprintable()}
    return ''.join(sorted(chars))


def embed_fonts():
    import shutil as sh
    out = os.path.join(ASSETS, 'fonts')
    os.makedirs(out, exist_ok=True)
    text = collect_chars()
    tf = tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False, encoding='utf-8')
    tf.write(text)
    tf.close()
    made = []
    for w, (ttc, idx) in SERIF.items():
        dst = os.path.join(out, 'lunyu-serif-%s.woff2' % w)
        subprocess.run([sh.which('pyftsubset') or 'pyftsubset', ttc,
                        '--font-number=%d' % idx, '--flavor=woff2',
                        '--text-file=%s' % tf.name,
                        '--layout-features=kern,vert,palt',
                        '--output-file=%s' % dst], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        made.append((w, os.path.getsize(dst)))
    os.unlink(tf.name)

    for dirpath, _, files in os.walk(ASSETS):
        for f in files:
            if not f.endswith('.html'):
                continue
            path = os.path.join(dirpath, f)
            prefix = '../' * (os.path.relpath(dirpath, ASSETS).count(os.sep) + 1) \
                if dirpath != ASSETS else ''
            s = open(path, encoding='utf-8').read()
            if 'id="lunyu-serif"' in s:
                continue
            css = ''.join(FACE % (w, prefix, w) for w in SERIF)
            s = s.replace('</head>', FONT_STYLE % css, 1)
            open(path, 'w', encoding='utf-8').write(s)
    return len(text), made


def main():
    if os.path.isdir(ASSETS):
        shutil.rmtree(ASSETS)
    os.makedirs(ASSETS)

    for name in ('index.html', 'book.html', 'xing-e.html',
                 'favicon.svg', 'manifest.webmanifest',
                 'icon-192.png', 'icon-512.png', 'icon-1024.png',
                 'apple-touch-icon.png', 'og.png'):
        src = os.path.join(DOCS, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(ASSETS, name))

    copy_tree(os.path.join(DOCS, 'ke'), os.path.join(ASSETS, 'ke'))
    copy_tree(os.path.join(DOCS, 'zt'), os.path.join(ASSETS, 'zt'),
              skip=('_shots', '_history'))

    total_site = total_font = 0
    for dirpath, _, files in os.walk(ASSETS):
        for f in files:
            if f.endswith('.html'):
                depth = os.path.relpath(dirpath, ASSETS).count(os.sep) + 1 \
                    if dirpath != ASSETS else 0
                a, b = rewrite_html(os.path.join(dirpath, f), depth)
                total_site += a
                total_font += b

    size = sum(os.path.getsize(os.path.join(d, f))
               for d, _, fs in os.walk(ASSETS) for f in fs)
    n_chars, made = embed_fonts()
    size = sum(os.path.getsize(os.path.join(d, f))
               for d, _, fs in os.walk(ASSETS) for f in fs)
    print('assets %.2f MB  site-links 改写 %d 处  外链字体样式表 去除 %d 处'
          % (size / 1048576, total_site, total_font))
    print('字集 %d 字，内嵌字重 %s'
          % (n_chars, '，'.join('%s %.1f MB' % (w, sz / 1048576) for w, sz in made)))
    print('ke 课 %d 页' % len(os.listdir(os.path.join(ASSETS, 'ke'))))


if __name__ == '__main__':
    main()
