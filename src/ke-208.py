# -*- coding: utf-8 -*-
"""第 208 课（泰伯 8.21）阅读版生成器，泰伯篇收篇批（单课）。

- 页头取 docs/ke/207.html 的 head+CSS（<div class="wrap"> 之前部分）。
- 结构同上批；篇名泰伯第八 · 二十一章（收篇）。
- 本批校记二事（页内用通行字，原字入存疑）：
  (1) 底本「菲飮食」之「飮」为「飲」之异体。
  (2) 底本「溝恤」通行作「溝洫」，页内正之（同 8.15「睢／雎」例）。
"""
"""第 203–207 课（泰伯 8.16–8.20）阅读版生成器，泰伯篇第四批。

- 页头取 docs/ke/207.html 的 head+CSS（<div class="wrap"> 之前部分）。
- 结构与 198–202 课一致；篇名泰伯第八（二十一章）；本批接 8.16 起，至 8.20。
- 本批校记二事：
  (1) 8.19「堯之爲軍」之「軍」当为「君」，据通行本正。
  (2) 8.20「豫有亂臣十人」之「豫」当为「予」（同 5.10、6.28、7.23、8.3 例）；
      「不其然乎，」之逗当为「？」，页内正之。
"""
"""第 198–202 课（泰伯 8.11–8.15）阅读版生成器，泰伯篇第三批。

- 页头取 docs/ke/207.html 的 head+CSS（<div class="wrap"> 之前部分）。
- 结构与 193–197 课一致；篇名泰伯第八（二十一章）；本批接 8.11 起，至 8.15。
- 本批校记三事：
  (1) 8.13「危邦不人」之「人」当为「入」，据通行本正；「恥也，邦無道」逗，页内正作分号。
  (2) 8.15「關睢」之「睢」为「雎」之形讹（全书「睢」2 见、「雎」0 见）；页内用通行字，原字入存疑。
  (3) 8.14 与 14.26 重出，两处并存，不删不并。
"""
"""第 193–197 课（泰伯 8.6–8.10）阅读版生成器，泰伯篇第二批次。

- 页头取 docs/ke/207.html 的 head+CSS（<div class="wrap"> 之前部分）。
- 结构与 188–192 课一致；篇名泰伯第八（二十一章）；本批接 8.6 起，至 8.10。
- 本批校记三事：
  (1) 8.6「臨大節，而不可奪也，」逗误、又脱「？」，页内正作「臨大節而不可奪也。君子人與？君子人也。」
  (2) 8.7 两处「不亦重乎，死而後已」之「，」当为「？」，页内正作两反问。
  (3) 8.8 底本三句各作句号，通行本多作顿号并列；页内从句读，记而不改。
"""
"""第 188–192 课（泰伯 8.1–8.5）阅读版生成器，泰伯篇首五课。

- 页头取 docs/ke/207.html 的 head+CSS（<div class="wrap"> 之前部分）。
- 结构与 185–187 课一致；篇名泰伯第八（二十一章）；本批接 8.1 起，至 8.5。
- 本批校记三事：
  (1) 8.2 四句连书脱标点，页内补作四句各断（「恭而無禮則勞，愼而無禮則葸，勇而無禮則亂，直而無禮則絞。」）。
  (2) 8.3 两处「啟豫足」「啟豫手」之「豫」当为「予」，据通行本正。
  (3) 8.4「斯近信笑出辭氣」之「笑」当为「斯」、脱「矣；」，页内正作「斯近信矣；出辭氣」。
  (4) 8.5「實若處」之「處」当为「虛」，据通行本正。
"""
"""第 185–187 课（述而 7.36–7.38）阅读版生成器，述而篇收篇。

- 页头取 docs/ke/207.html 的 head+CSS（<div class="wrap"> 之前部分）。
- 结构与 180–184 课一致；篇名述而第七（三十八章）；本批接 7.36 起，至 7.38 收篇。
- 本批校记两事：
  (1) 7.36「孫」为「遜」之通假，底本如此，不改。
  (2) 7.36「甯」为「寧」之异体，底本如此，不改。
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = open(f'{ROOT}/VERSION', encoding='utf-8').read().strip()

MARK = '<div class="wrap">'
_tpl = open(f'{ROOT}/docs/ke/207.html', encoding='utf-8').read()
PREFIX = _tpl[:_tpl.find(MARK) + len(MARK)]

TOP = '''<div style="background:#FCFAF6;border-bottom:1px solid #DCD5C8;padding:9px 16px;
font-family:'Noto Sans SC','PingFang SC',sans-serif;font-size:12px;letter-spacing:.1em;
display:flex;justify-content:space-between;align-items:center;color:#7C6D5C">
<span>润泽说 · 道可道之论语 · 通释</span>
<a href="../index.html" style="color:#994433;text-decoration:none;border:0">← 目录</a></div>
'''


def tzg(items):
    return ('<div class="tzg" aria-label="四个关键字">' + ''.join(
        f'<div class="tzitem"><div class="cell">{k}</div><div class="tzcap">{v}</div></div>'
        for k, v in items) + '</div>')


def rows(items, wide=False):
    cls = 'rows wide' if wide else 'rows'
    return f'<div class="{cls}">' + ''.join(
        f'<div class="row"><div class="k k2">{k}</div><div class="v">{v}</div></div>'
        for k, v in items) + '</div>'


def scenes(items):
    return ''.join(f'<div class="scene">{x}</div>' for x in items)


def pairs(items):
    return '<div class="cards">' + ''.join(
        f'<div class="pair"><div class="a">{a}</div><div class="b">{b}</div></div>'
        for a, b in items) + '</div>'


def doubt(items):
    return '<div class="doubt">' + ''.join(f'<div class="q">{x}</div>' for x in items) + '</div>'


def fig_prompt(cap, ph, prompt):
    return (f'<div class="figs single"><div class="fig"><div class="cap">{cap}</div>'
            f'<div class="ph">{ph}</div></div></div>'
            f'<details class="prompt"><summary>提示词（存档）</summary><pre>{prompt}</pre></details>')


def svg(boxes, note, aria):
    out = [f'<div class="figsvg"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 220" role="img" aria-label="{aria}">']
    for x, w, t, s, c in boxes:
        out.append(f'  <rect x="{x}" y="56" width="{w}" height="86" fill="#FFFDF6" stroke="{c}"/>')
        out.append(f'  <text x="{x + w // 2}" y="88" text-anchor="middle" font-size="12" fill="{c}">{t}</text>')
        out.append(f'  <text x="{x + w // 2}" y="112" text-anchor="middle" font-size="9.5" fill="#8A8074">{s}</text>')
    out.append(f'  <text x="220" y="182" text-anchor="middle" font-size="10.5" fill="#2F2A24">{note}</text>')
    out.append('</svg></div>')
    return ''.join(out)






LESSONS = []

# ---------- 208 · 8.21 禹吾无间然矣 ----------
L = dict(
    lian_title='挑不出缝的那个人',
    no=208, ref='8.21', title='禹，吾无间然矣', safe='禹吾无间然矣',
    yi='子曰：「禹，吾無間然矣。菲飲食，而致孝乎鬼神；惡衣服，而致美乎黻冕；卑宮室，而盡力乎溝洫。禹，吾無間然矣。」',
    desc='《泰伯》8.21（收篇）：孔子言禹无可非间——菲饮食而致孝乎鬼神、恶衣服而致美乎黻冕、卑宫室而尽力乎沟洫，首尾复句以收。一课两页：少儿页讲他把自己的吃穿住压到最低，把该敬的、该办的抬到最高；成人辨「無間」为无可非间抑无隙可指、「菲」为薄抑假「匪」，附「菲」「致孝」「惡衣服」「黻冕」「卑宮室」「盡力」「溝洫」七孤例与「無間」二见同章之证；底本「飮」「恤」二处异体讹字页内用通行字、原字入存疑。',
    pianname='泰伯第八', pian='泰伯第八 · 二十一章（收篇）',
    kws=[('無間', '挑不出缝、无可非议'), ('菲', '薄、减省'), ('黻冕', '礼服礼冠'), ('溝洫', '田间水道')],
    one='孔子说：禹，我挑不出他一点缝来。他自己吃得省，祭鬼神却办得厚；自己穿得粗，礼服礼冠却做得美；自己住得低，田里的水道却修得尽。禹，我挑不出他一点缝来。',
    words=[('無間', '没有缝隙、挑不出毛病。'), ('菲', '薄、减省。'),
           ('致孝', '把敬意尽到。'), ('鬼神', '祭祀的对象。'),
           ('惡衣服', '穿得粗劣。'), ('黻冕', '礼服与礼冠。'),
           ('卑宮室', '住得低矮简陋。'), ('溝洫', '田间的沟渠水道。')],
    read=['第一句：禹，我挑不出缝来。',
          '第二句：自己吃得省，祭鬼神却厚。',
          '第三句：自己穿得粗，礼服却美。',
          '第四句：自己住得低，水道却修得尽。',
          '第五句：还是那句——挑不出缝来。'],
    life=['自己的那份可以省，大家的事不能省。',
          '省下来的，要花在该花的地方。'],
    ask=[('问一', '「无间」是什么意思？'), ('问二', '三件事各是「薄什么、厚什么」？'),
         ('问三', '为什么开头结尾说同一句话？')],
    grow=[('一', '对自己可以苛刻一点。'), ('二', '对大家的事要舍得。'),
          ('三', '一件事做到挑不出缝，才叫成。')],
    lian='上章论周之至德（8.20），此章论禹之无间：一以「服事」见其守分，一以「菲饮食、恶衣服、卑宫室」见其薄己。泰伯一篇以让始，以无间终——让是不争，无间是无隙。',
    adult_words=[('無間', '间，隙也；无间然，无可非间、无可指摘。'), ('菲', '薄也，减省。'),
                 ('致', '尽也、致之。'), ('鬼神', '祭所祀者，泛指神明。'),
                 ('黻冕', '黻，礼服之纹；冕，礼冠。'), ('卑', '低也、简陋。'),
                 ('溝洫', '田间水道；洫为田间之沟。')],
    reads=['「無間」两读：无可非间（本文主，朱子「间，罅隙也」）；一说无间隙可入（义近）。前读为长。',
           '「菲」两读：薄（本文主，朱子「菲，薄也」）；一说「菲」为「匪」之假（较弱，不取）。前读为长。',
           '「致孝乎鬼神」两读：致其孝于祭祀（本文主，谓祭尽其敬）；一说「孝」为「享」（较弱，不取）。前读为长。',
           '三组一例：薄于自奉而厚于所事——饮食／鬼神、衣服／黻冕、宫室／沟洫，一一对举。',
           '首尾复句：「禹，吾無間然矣」两见于本章，一头一尾，非重复而为收束。',
           '文本内证：「無間」2 见皆在本章；「菲」「致孝」「惡衣服」「黻冕」「卑宮室」「盡力」「溝洫」各 1 见，皆仅本章；「禹」5 见落 4 章。'],
    gist='薄于自奉，厚于所事，故无可非间。',
    layers=[('第一层', '禹，吾無間然矣——一句断。'), ('第二层', '菲飲食，而致孝乎鬼神——食与祭。'),
            ('第三层', '惡衣服，而致美乎黻冕——衣与礼。'), ('第四层', '卑宮室，而盡力乎溝洫——居与民。'),
            ('第五层', '禹，吾無間然矣——复句以收。')],
    layer_note='三组同一句法：先把自奉压低（菲、恶、卑），再把所事抬高（致孝、致美、尽力）。压低的是自己的吃穿住，抬高的是祭、礼、民田水利。末句复首句，不是又说一遍，是把三件事收进一个断语里。',
    doubts=['「無間」两读：无可非间（本文主）、无隙可指（义近）。',
            '「菲」两读：薄（本文主）、假「匪」（一说，较弱）。',
            '校勘：底本「菲飮食」之「飮」为「飲」之异体，页内用通行字「飲」，原字记此；底本「溝恤」通行作「溝洫」，页内正之（同 8.15「睢／雎」例，原字入存疑）。',
            '（底本 8.21 除上述二处外字句核对无误。）'],
    cards=[('菲饮食：薄己', '致孝鬼神：厚祭'), ('恶衣服：薄己', '致美黻冕：厚礼'),
           ('8.20 至德：守分', '8.21 无间：无隙'), ('薄于自奉', '厚于所事')],
    cross=[('《泰伯》8.18「舜禹有天下而不与」', '不与于天下，亦不厚于自奉。'),
           ('《泰伯》8.19「成功文章」', '尧以典章，禹以沟洫。'),
           ('《雍也》6.22「敬鬼神」', '「鬼神」之再见。'),
           ('《先进》11.12「事鬼神」', '「鬼神」之三见。')],
    cap='图一 · 低屋与长渠',
    ph='图位：竖幅 3:4 水墨。左侧一间低矮茅屋，檐低及眉、门仅容身；右侧一条长渠自田间蜿蜒远去，渠岸齐整、水光细亮；屋前一人（禹）着粗褐、手持耒耜，立于渠首，目光在渠不在屋。画面零文字。',
    prompt='竖幅中国古风淡彩水墨插图，暖米白纸本，墨色克制、留白充足，赭红与青灰点缀。左侧一间低矮茅屋，檐低及眉、门仅容身，屋顶茅草疏薄；右侧一条长渠自田间蜿蜒远去，渠岸齐整、水面一线细亮；屋前一人身着粗褐短衣、手持耒耜立于渠首，目光望向渠水而不望屋。田间阡陌浅赭，远山淡墨。整体低饱和，青灰用于水渠与褐衣，笔触淡墨渲染加少量赭石勾勒，纸面微纹理。画面不出现任何文字、屋上题字、渠边碑刻、题款或印章。',
    svg1=svg([(15, 92, '菲饮食', '薄己', '#4A5C55'), (120, 92, '致孝鬼神', '厚祭', '#4A5C55'),
              (225, 92, '恶衣服／卑宫室', '薄己', '#4A5C55'), (330, 92, '致美黻冕／尽力沟洫', '厚事', '#A2503B')],
             '压低自己的吃穿住，抬高祭、礼、民田', '三组薄厚四段'),
    svg1cap='义理图一 · 三组同句法',
    svg2=svg([(40, 150, '首句：一断', '禹吾无间', '#8A8074'), (250, 150, '末句：复句以收', '同一断语', '#4A5C55')],
             '不是又说一遍，是把三件事收进一个断语', '首与末两栏'),
    svg2cap='义理图二 · 首与末',
    extra1='三组同一句法：先把自奉压低（菲、恶、卑），再把所事抬高（致孝、致美、尽力）。压低的是自己的吃穿住，抬高的是祭、礼、民田水利——三者一落到「别人用得着」的地方。',
    extra2='首尾复句不是重复：头一句是开口就断，末一句是数完三事再断，中间三组就是这断语的凭据。与 8.18「舜禹之有天下也，而不与焉」对看：彼言不把天下算作己有，此言不把吃穿住留给自己——「不与」落到衣食住行，才看得见。泰伯一篇以「三让」始、以「无间」终：让是不争，无间是无隙，两字收尽一篇。',
    stats=[('無間', '全书 2 见，皆在本章（首尾复句）；「間」全书 5 见落 4 章。'),
           ('菲', '全书 1 见，仅本章；孤例。'),
           ('致孝', '全书 1 见，仅本章；孤例。'),
           ('惡衣服', '全书 1 见，仅本章；孤例。'),
           ('黻冕', '全书 1 见，仅本章；孤例（「冕」全书 7 见落 6 章）。'),
           ('卑宮室', '全书 1 见，仅本章；孤例（「宮室」全书 1 见）。'),
           ('盡力', '全书 1 见，仅本章；孤例。'),
           ('溝洫', '全书 1 见，仅本章；孤例（底本作「溝恤」）。'),
           ('孝', '全书 19 见，分落 14 章；本章 1 见。'),
           ('鬼神', '全书 3 见，分落 3 章（6.22、8.21、11.12）；本章 1 见。'),
           ('禹', '全书 5 见，分落 4 章（8.18、8.21、14.5、20.1）；本章 1 见（首尾各一，计 2）。'),
           ('命令', '要核：grep -o 無間 refs/lunyu-baiwen.txt | wc -l 应得 2；grep -o 溝恤 refs/lunyu-baiwen.txt | wc -l 应得 1（「溝洫」0 见）。')],
)
LESSONS.append(L)


def build(L):
    n, ref = L['no'], L['ref']
    teacher_child = rows(L['ask'])
    grow = rows(L['grow'])
    child = f'''<section class="page">
  <div class="leaf-tag">少儿页 · 第{n}课 · {ref}</div>
  <h1>{L['title']}</h1>
  <div class="h1-sub">{L.get("pianname", "里仁第四")} · {ref}　第 {n} 课</div>
  <div class="src">原文：{L['yi']}</div>
  <div class="h2" id="sc-1">四个关键字</div>{tzg(L['kws'])}
  <div class="h2" id="sc-2">一句话讲清</div><div class="scene">{L['one']}</div>
  <div class="h2" id="sc-3">字义小窗</div>{rows(L['words'], wide=True)}
  <div class="h2" id="sc-4">共读</div>{scenes(L['read'])}
  <div class="h2" id="sc-5">生活里的一天</div>{scenes(L['life'])}
  <div class="h2" id="sc-6">三个小问题</div>{teacher_child}
  <div class="h2" id="sc-7">成长小启示</div>{grow}
</section>'''

    adult = f'''<section class="page adult">
  <div class="leaf-tag">成人页 · 第{n}课 · {ref}</div>
  <h1>{L['title']}</h1>
  <div class="h1-sub">{L.get("pianname", "里仁第四")} · {ref}　第 {n} 课</div>
  <div class="src">原文：{L['yi']}</div>
  <div class="h2" id="sc-lian">连读</div><div class="scene">{L['lian']}</div>
  <div class="h2" id="sc-b">字义句读</div>{rows(L['adult_words'], wide=True)}
  <div class="h2" id="sc-c">两读</div>{scenes(L['reads'])}
  <div class="h2" id="sc-d">章旨</div><div class="scene">{L['gist']}</div>
  <div class="h2" id="sc-e">三层</div>{rows(L['layers'], wide=True)}
  <div class="scene">{L['layer_note']}</div>
  <div class="h2" id="sc-h">存疑</div>{doubt(L['doubts'])}
  <div class="h2" id="sc-i">双卡</div>{pairs(L['cards'])}
  <div class="h2" id="sc-j">跨典</div>{pairs(L['cross'])}
  <div class="h2" id="sc-19">图一　{L['cap'].split('· ', 1)[1]}</div>{fig_prompt(L['cap'], L['ph'], L['prompt'])}
  <div class="h2" id="sc-20">义理图一</div>{L['svg1']}<div class="figcap">{L['svg1cap']}</div>
  <div class="h2" id="sc-21">义理图二</div>{L['svg2']}<div class="figcap">{L['svg2cap']}</div>
  <div class="h2" id="sc-22">附论一</div><div class="scene">{L['extra1']}</div>
  <div class="h2" id="sc-23">附论二</div><div class="scene">{L['extra2']}</div>
  <div class="cardhint">数证（底本 refs/lunyu-baiwen.txt，白文全本繁简互校）</div>{rows(L['stats'])}
  <footer><div class="foot-l">润泽说 · 道可道之论语　v{VER}</div><div class="foot-r">第 {n} 课 / 498</div></footer>
</section>'''

    head = PREFIX
    head = re.sub(r'<div style="background:#FCFAF6;.*?</div>\n', '', head, flags=re.S)
    head = re.sub(r'<title>.*?</title>',
                  f'<title>润泽说 道可道之论语 · 第{n}课 {L["title"]}（{L.get("pianname", "里仁第四").split("第")[0]} {ref}）</title>', head, count=1)
    head = re.sub(r'(name="description" content=")[^"]*(")',
                  lambda m: m.group(1) + L['desc'] + m.group(2), head, count=1)

    html = head + TOP + f'''<div class="mast">
  <div class="series">润泽说 · 道可道之论语</div>
  <div class="crumb">上论　{L.get("pian", "里仁第四 · 二十六章")}　第 {n} 课 / 498</div>
</div>
''' + child + '\n\n' + adult + '''
</div>
</body>
</html>
'''
    open(f'{ROOT}/docs/ke/{n}.html', 'w', encoding='utf-8').write(html)
    print('ke', n, len(html))


if __name__ == '__main__':
    for L in LESSONS:
        build(L)
