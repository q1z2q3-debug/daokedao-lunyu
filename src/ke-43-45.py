# -*- coding: utf-8 -*-
import re, os

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = open(f'{ROOT}/VERSION', encoding='utf-8').read().strip()
src = open(f'{ROOT}/docs/ke/42.html', encoding='utf-8').read()
i = src.find('<div class="wrap">')
PREFIX = src[:i+len('<div class="wrap">')]
SUFFIX = '</footer>\n</div>\n</body>\n</html>\n'

def tzg(items):
    out = '<div class="tzg" aria-label="四个关键字">'
    for z, cap in items:
        out += f'<div class="tzitem"><div class="cell">{z}</div><div class="tzcap">{cap}</div></div>'
    return out + '</div>'

def rows(pairs, k2=False):
    out = '<div class="rows">'
    for k, v in pairs:
        cls = 'k k2' if len(k) > 4 else 'k'
        out += f'<div class="row"><div class="{cls}">{k}</div><div class="v">{v}</div></div>'
    return out + '</div>'

def scene(t):
    return f'<div class="scene">{t}</div>'

def cards(pairs):
    out = '<div class="cards"><div class="pair"><div class="a">左</div><div class="b">右</div></div>' if False else '<div class="cards">'
    for a, b in pairs:
        out += f'<div class="pair"><div class="a">{a}</div><div class="b">{b}</div></div>'
    return out + '</div>'

def qs(items):
    return '<div class="doubt">' + ''.join(f'<div class="q">{q}</div>' for q in items) + '</div>'

def h2(id_, t):
    return f'<div class="h2" id="{id_}">{t}</div>'

def figph(cap, prompt):
    return (f'<div class="figs single"><div class="fig"><div class="cap">{cap}</div>'
            f'<div class="ph">图位：竖幅 3:4 水墨。{prompt}</div></div></div>'
            f'<details class="prompt"><summary>提示词（存档）</summary><pre>{prompt}</pre></details>')

def figsvg(svg, cap):
    return f'<div class="figsvg">{svg}</div><div class="figcap">{cap}</div>'

def page(lesson, section, h1, sub, src_txt, kid, adult):
    return f'''<div class="mast">
  <div class="series">润泽说 · 道可道之论语</div>
  <div class="crumb">上论　八佾第三 · 二十六章　第 {lesson} 课 / 498</div>
</div>

<section class="page">
  <div class="leaf-tag">少儿页 · 第{lesson}课 · {section}</div>
  <h1>{h1}</h1>
  <div class="h1-sub">八佾第三 · {section}　第 {lesson} 课</div>
  <div class="src">{src_txt}</div>
  {kid}
</section>

<section class="page adult">
  <div class="leaf-tag">成人页 · 第{lesson}课 · {section}</div>
  <h1>{h1}</h1>
  <div class="h1-sub">八佾第三 · {section}　第 {lesson} 课</div>
  <div class="src">{src_txt}</div>
  {adult}
  <footer><div class="foot-l">润泽说 · 道可道之论语　v{VER}</div><div class="foot-r">第 {lesson} 课 / 498</div></footer>
</section>
'''

# ---------- 3.4 ----------
L43_kid = ''.join([
 h2('sc-1','四个关键字'),
 tzg([('本','礼从哪里长出来'),('奢','排场过头'),('俭','简而不薄'),('戚','哀在心里')]),
 h2('sc-2','一句话讲清'),
 scene('有人问孔子：礼的根本是什么？夫子先说这问题问得好，然后给了两个对比：办礼，与其铺张，不如朴素；办丧事，与其只是把事办得顺溜，不如心里真的难过。'),
 h2('sc-3','字义小窗'),
 rows([('林放','鲁国人，好礼而问其本。'),('本','树根。礼的根，不在器物，在心。'),
       ('易','把事情办得轻省、顺当，却少了那份郑重。'),('戚','哀戚，心里的难过。')]),
 h2('sc-4','共读'),
 scene('「大哉问！」——夫子不是在夸人，是在夸这个问题。礼被办成一套流程以后，很少有人再回头问：这一套究竟为了什么。'),
 scene('「与其奢也，宁俭」——两个都不完美，但奢离本更远。俭是少，不是薄；是把多余的东西去掉，留下要紧的。'),
 h2('sc-5','生活里的一天'),
 scene('奶奶过生日，家里订了很大的蛋糕、请了很多人，可奶奶一直坐在角落里没说话。后来小辈们围过来，一人说一句小时候的事，她才笑起来——那天最像「过生日」的，是后面那半小时。'),
 scene('同学的爷爷走了。灵堂布置得很体面，司仪的话一句接一句，可同学一直低着头。散场时他说：其实我只想再安静坐一会儿。'),
 h2('sc-6','三个小问题'),
 rows([('问题一','「与其奢也，宁俭」，是不是说越省越好？'),
       ('问题二','丧事里「易」和「戚」差在哪里？'),
       ('问题三','你参加过的那场婚礼或葬礼，哪一刻让你觉得「这才是真的」？')]),
 h2('sc-7','成长小启示'),
 rows([('一','做事先把「为谁做」想清楚，再想「做多大」。'),
       ('二','少一点，但每一样都用上心——这叫俭，不叫省。'),
       ('三','难过的时候不必装镇定，那是礼允许的。')]),
])

L43_adult = ''.join([
 h2('sc-lian','连读：从僭到本'),
 scene('3.1 八佾舞于庭，僭在数；3.2 三家以雍彻，僭在位；3.3 人而不仁如礼何，点出礼乐无所附丽。三章连着讲「礼失」，3.4 忽然掉头问「礼之本」——失其本，才处处只剩形式。'),
 h2('sc-b','字义句读'),
 rows([('林放','鲁人。《论语》中仅此一见，因一问而留名。'),
       ('本','与本末相对。朱子：「礼之本，在于俭戚。」'),
       ('奢 / 俭','奢，过也；俭，约也。二者皆非中，而奢去本远。'),
       ('易','朱子训「慢易」，谓治丧轻慢、徒具其事；郑玄一路训「治」，亦通。'),
       ('戚','哀戚。丧礼之本在哀，不在仪节之备。')], k2=True),
 h2('sc-c','两读：「易」字怎么讲'),
 scene('一读：易＝慢易。丧事办得顺溜、轻省，仪节不缺而哀情不足。此读与「戚」正相对，朱子取之。'),
 scene('二读：易＝治。郑玄「易谓治也」，谓料理丧事周全。若作此读，则「与其易也，宁戚」是说：与其把事办得周全，不如心里真有哀——朱子其实也承此意，只是把「易」的贬义说得更明。'),
 scene('两读不冲突：都指向「事办得好，心不到」。差别只在「易」是轻慢，还是仅仅「办得周全」。'),
 h2('sc-d','章旨'),
 scene('礼有本有文。文是器物、仪节、排场；本是敬与哀。夫子不否认文，只说：两个方向都偏时，宁可往本那边偏。这是给「礼」定优先级，不是否定礼。'),
 h2('sc-e','三层'),
 rows([('第一层','问得对：先把问题问对，答案才可能对。'),
       ('第二层','奢不如俭：多在物上用力，少在心上用力，礼就越办越空。'),
       ('第三层','易不如戚：丧礼最不能省的，是那份难过。')], k2=True),
 h2('sc-h','存疑'),
 qs(['「易」训「慢易」还是「治」，汉宋两读；本文两存，以「心不到」为共义。',
     '「与其…宁…」是比较句式，非取舍定论：夫子未说奢可废，只说二者相权。',
     '林放其人，一说是鲁人，一说为孔子弟子；《史记·弟子列传》不载，本文取「鲁人」而不列入门人。',
     '此章是否专对鲁国当时僭奢之风而发，无确证，只能看作通则。']),
 h2('sc-i','双卡'),
 cards([('奢：物有余','俭：物不足而心足'),('易：事办得顺','戚：心跟得上'),
        ('本：敬与哀','文：器与仪'),('礼之用：和','礼之失：空转')]),
 h2('sc-j','跨典'),
 cards([('《礼记·檀弓》','丧礼主哀，与其哀不足而礼有余，不若礼不足而哀有余。'),
        ('《八佾》3.3','人而不仁如礼何——本亡则文无所附。'),
        ('《学而》1.13','礼之用，和为贵——本立而后文行。'),
        ('《阳货》17.8','礼云礼云，玉帛云乎哉——同一声问。')]),
 h2('sc-19','图一　林放问本'),
 figph('图一 · 一问之下，满庭陈设忽然显得轻',
      '庭中陈设齐备而无人用心：一侧几案上礼器罗列、锦帛堆叠；另一侧一位士人空手立着，只向夫子发问。夫子坐着，手未指器物，只微向前倾。远处两三个仆役还在搬抬器物，动作忙碌而神情空。重心在「物多而心少」的反差，画面零文字。'),
 h2('sc-20','义理图一　四对坐标'),
 figsvg("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 260" role="img" aria-label="礼的四个坐标：奢与俭、易与戚">
  <line x1="60" y1="130" x2="380" y2="130" stroke="#DED2B9"/>
  <circle cx="60" cy="130" r="5" fill="#A2503B"/><circle cx="380" cy="130" r="5" fill="#4A5C55"/>
  <text x="60" y="112" text-anchor="middle" font-size="12" fill="#A2503B">奢</text>
  <text x="60" y="152" text-anchor="middle" font-size="10.5" fill="#8A8074">物有余</text>
  <text x="380" y="112" text-anchor="middle" font-size="12" fill="#4A5C55">俭</text>
  <text x="380" y="152" text-anchor="middle" font-size="10.5" fill="#8A8074">物不足</text>
  <text x="220" y="78" text-anchor="middle" font-size="11" fill="#2F2A24">礼：与其奢也，宁俭</text>
  <line x1="60" y1="212" x2="380" y2="212" stroke="#DED2B9"/>
  <circle cx="60" cy="212" r="5" fill="#A2503B"/><circle cx="380" cy="212" r="5" fill="#4A5C55"/>
  <text x="60" y="238" text-anchor="middle" font-size="12" fill="#A2503B">易</text>
  <text x="60" y="196" text-anchor="middle" font-size="10.5" fill="#8A8074">事办得顺</text>
  <text x="380" y="238" text-anchor="middle" font-size="12" fill="#4A5C55">戚</text>
  <text x="380" y="196" text-anchor="middle" font-size="10.5" fill="#8A8074">心跟得上</text>
  <text x="220" y="196" text-anchor="middle" font-size="11" fill="#2F2A24">丧：与其易也，宁戚</text>
</svg>""",'义理图一 · 两条轴，四端：偏于物者退半步，偏于心者进一步。'),
 h2('sc-21','义理图二　本与文'),
 figsvg("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 240" role="img" aria-label="本在情，文在物；本文相须">
  <circle cx="150" cy="120" r="44" fill="#FFFDF6" stroke="#A2503B"/>
  <text x="150" y="118" text-anchor="middle" font-size="19" font-weight="600" fill="#A2503B">本</text>
  <text x="150" y="140" text-anchor="middle" font-size="10.5" fill="#8A8074">敬 · 哀</text>
  <rect x="270" y="86" width="126" height="68" fill="#FFFDF6" stroke="#DED2B9"/>
  <text x="333" y="114" text-anchor="middle" font-size="16" fill="#2F2A24">文</text>
  <text x="333" y="134" text-anchor="middle" font-size="10.5" fill="#8A8074">器 · 仪 · 排场</text>
  <line x1="194" y1="120" x2="270" y2="120" stroke="#4A5C55" stroke-width="1.5"/>
  <polygon points="270,120 261,116 261,124" fill="#4A5C55"/>
  <text x="232" y="108" text-anchor="middle" font-size="10" fill="#4A5C55">附丽</text>
  <text x="220" y="210" text-anchor="middle" font-size="11" fill="#2F2A24">本亡则文空转：礼云礼云，玉帛云乎哉</text>
</svg>""",'义理图二 · 文依本立；本去，文只剩动作。'),
 h2('sc-22','附论一　俭不是寒酸'),
 scene('俭的反面不是体面，是「用力用错了地方」。一场婚礼，把预算花在灯光和车队，还是花在让每位长辈坐得舒服、说得上话——前者是奢，后者未必贵。俭的判准不在花多少钱，在每一分钱是否落在人身上。'),
 h2('sc-23','附论二　丧礼允许你难过'),
 scene('今天很多丧事被办成一场「流程管理」：时间、路线、致辞、答谢，样样周全，唯独没有留给哀伤的位置。夫子这句话像是替活着的人争一个权利：你可以不周全，但你不必不难过。'),
])

# ---------- 3.5 ----------
L44_kid = ''.join([
 h2('sc-1','四个关键字'),
 tzg([('夷狄','远处未化之人'),('诸夏','中原诸国'),('有君','名分还在'),('亡','同「无」，没有了')]),
 h2('sc-2','一句话讲清'),
 scene('夫子说：夷狄那样远处的地方，好歹还有自己的君长；中原这些礼乐之国，反倒常常君不君、臣不臣，名分空着。'),
 h2('sc-3','字义小窗'),
 rows([('夷狄','古人对四方未通礼乐者的称呼，此处不必当贬词读死。'),('诸夏','中原华夏诸国，礼乐之所在。'),
       ('有君','有君长，有上下之分。'),('亡','读作「无」。不是国家亡了，是「没有」了。')]),
 h2('sc-4','共读'),
 scene('这句话听上去像在贬低自己人。夫子偏偏这么说——他不是看不起诸夏，是着急：礼乐之地，反而不守礼乐之实。'),
 scene('「有君」不只是有个人坐在位上，是有名分、有秩序、有人守。位子在而分不在，就等于没有。'),
 h2('sc-5','生活里的一天'),
 scene('班里选出了班长，可收作业、排值日、调座位，全是另一个同学在张罗，班长只在名单上。大家都说「我们班有班长」，其实那阵子班里是「无班长」的。'),
 scene('一个球队，教练在场边站着，队员各打各的，谁也叫不动谁——场上有人，队里无主。'),
 h2('sc-6','三个小问题'),
 rows([('问题一','「有君」的「有」，是有个人，还是有秩序？'),
       ('问题二','如果名分在、事情却没人做，算「有」还是「无」？'),
       ('问题三','你们家、你们班，有没有「有位子没人管」的地方？')]),
 h2('sc-7','成长小启示'),
 rows([('一','头衔不等于在管；被认，是因为有人在做事。'),
       ('二','规矩没人守的时候，最先塌的是最小的事：值日、作业、集合。'),
       ('三','别用「我们一向如此」替空位子遮羞。')]),
])

L44_adult = ''.join([
 h2('sc-lian','连读：僭与亡'),
 scene('前三章讲僭：数僭、位僭、礼乐空转。本章换一个方向说：僭的尽头是「亡」——不是国亡，是名分亡。有君之名而无君之实，与无君无异。'),
 h2('sc-b','字义句读'),
 rows([('夷狄','《论语》中与「诸夏」对举，多指礼乐未及之地，非血统论。'),
       ('诸夏','中原列国，自称礼乐之邦。'),
       ('亡','同「无」。朱子：「亡，无也。」'),
       ('不如','一读「比不上」，一读「不像」；两读方向相反，见下。')], k2=True),
 h2('sc-c','两读：谁不如谁'),
 scene('甲读（朱子一路）：夷狄尚有君长，诸夏反无君长——「不如」是「比不上」，语气是伤病。此读把矛头指向诸夏的僭乱。'),
 scene('乙读：夷狄虽有君，仍不如诸夏之无君——因为诸夏纵一时无君，礼乐之统还在。此读把话读成对「礼」的自信。'),
 scene('甲读合于《八佾》上下文：上一章刚骂完僭，这一章接着叹「名分亡」。故本文取甲读，乙读入存疑。'),
 h2('sc-d','章旨'),
 scene('君之为君，不在位，在分。分在，则虽乱可复；分亡，则虽安亦危。夫子这句话，是把「礼」看成一套名分秩序：秩序在，国才是国。'),
 h2('sc-e','三层'),
 rows([('第一层','有君：位与分相称。'),('第二层','有君之名：位在而分不在——僭者当道。'),
       ('第三层','亡：名分整体失效，虽有人君，等于无君。')], k2=True),
 h2('sc-h','存疑'),
 qs(['「不如」两读方向相反，本文取「比不上」；若取「不像」，全章语气转褒，与上章不接。',
     '「夷狄」在此是礼乐地理概念，非种族优劣；引用时不宜作民族论解。',
     '此章是否针对某国具体之事（如鲁之三家、卫之出公），无确证。',
     '「亡」通「无」，汉石经以下无异说；唯「亡」亦可读「灭亡」，则语气更重，今不取。']),
 h2('sc-i','双卡'),
 cards([('有君：分在位在','有君之名：位在分亡'),('诸夏：礼乐之地','夷狄：礼乐未及'),
        ('僭：越过名分','亡：名分空转'),('秩序：可复','空位：难救')]),
 h2('sc-j','跨典'),
 cards([('《颜渊》12.11','君君臣臣父父子子——名分是秩序的第一层。'),
        ('《子路》13.3','名不正则言不顺——名亡则事不成。'),
        ('《季氏》16.2','天下有道，则礼乐征伐自天子出——僭之极。'),
        ('《春秋》','夷狄进于中国则中国之——华夷以礼分，不以血分。')]),
 h2('sc-19','图一　有位无主'),
 figph('图一 · 堂上有位，堂下无主',
      '厅堂正中设一空座，座前几案陈设整齐；两侧各立数人，各自朝向不同，无一人向座行礼，也无一人主事。地上散着几卷未收的简册。门外一名小吏探头，似在等吩咐而无人吩咐。画面只画「位」与「无人」，零文字。'),
 h2('sc-20','义理图一　有君的三层'),
 figsvg("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 250" role="img" aria-label="有君的三层：位、分、事">
  <rect x="40" y="40" width="110" height="46" fill="#FFFDF6" stroke="#DED2B9"/>
  <text x="95" y="69" text-anchor="middle" font-size="13" fill="#2F2A24">位</text>
  <rect x="165" y="40" width="110" height="46" fill="#FFFDF6" stroke="#DED2B9"/>
  <text x="220" y="69" text-anchor="middle" font-size="13" fill="#2F2A24">分</text>
  <rect x="290" y="40" width="110" height="46" fill="#FFFDF6" stroke="#A2503B"/>
  <text x="345" y="69" text-anchor="middle" font-size="13" fill="#A2503B">事</text>
  <line x1="150" y1="63" x2="165" y2="63" stroke="#4A5C55"/><polygon points="165,63 157,59 157,67" fill="#4A5C55"/>
  <line x1="275" y1="63" x2="290" y2="63" stroke="#4A5C55"/><polygon points="290,63 282,59 282,67" fill="#4A5C55"/>
  <text x="220" y="120" text-anchor="middle" font-size="11" fill="#8A8074">三者相须：缺一则「有君」落空</text>
  <rect x="40" y="150" width="360" height="1" fill="#DED2B9"/>
  <text x="220" y="182" text-anchor="middle" font-size="11.5" fill="#2F2A24">名分在，虽乱可复；名分亡，虽安亦危</text>
  <text x="220" y="212" text-anchor="middle" font-size="10.5" fill="#8A8074">夷狄有君，不如诸夏之亡也</text>
</svg>""",'义理图一 · 位、分、事三足；一足不立，名存实亡。'),
 h2('sc-21','义理图二　僭到亡'),
 figsvg("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 230" role="img" aria-label="僭越累积导致名分空转">
  <line x1="50" y1="120" x2="390" y2="120" stroke="#DED2B9"/>
  <circle cx="90" cy="120" r="7" fill="#4A5C55"/><circle cx="210" cy="120" r="7" fill="#A2503B"/><circle cx="330" cy="120" r="7" fill="#2F2A24"/>
  <text x="90" y="100" text-anchor="middle" font-size="11.5" fill="#4A5C55">数僭</text>
  <text x="210" y="100" text-anchor="middle" font-size="11.5" fill="#A2503B">位僭</text>
  <text x="330" y="100" text-anchor="middle" font-size="11.5" fill="#2F2A24">名亡</text>
  <text x="90" y="146" text-anchor="middle" font-size="10" fill="#8A8074">八佾舞庭</text>
  <text x="210" y="146" text-anchor="middle" font-size="10" fill="#8A8074">三家雍彻</text>
  <text x="330" y="146" text-anchor="middle" font-size="10" fill="#8A8074">有君如无</text>
</svg>""",'义理图二 · 僭不是一次越界，是一路把名分磨空。'),
 h2('sc-22','附论一　「有君」是动词'),
 scene('现代组织里最不缺的是「位」：职务、群公告、名册。最缺的是「事」：谁在收尾、谁在拍板、谁在被认。夫子的判准很直白：看有没有人在做事，而不是看名单上有没有名字。'),
 h2('sc-23','附论二　华夷之辨的读法'),
 scene('这句话最容易被读成自贬或自傲，两者都不对。它讲的是礼乐秩序的有无，不是人的高下。礼乐在地理上有先后，在人心上没有贵贱——这也是后来「夷狄进于中国则中国之」的根据。'),
])

# ---------- 3.6 ----------
L45_kid = ''.join([
 h2('sc-1','四个关键字'),
 tzg([('旅','祭名，祭山川'),('泰山','五岳之首'),('冉有','季氏的家臣'),('救','阻止、纠正')]),
 h2('sc-2','一句话讲清'),
 scene('季氏是大夫，却去祭泰山。夫子问做他家臣的冉有：你不能拦一拦吗？冉有说不能。夫子叹：难道泰山的神，还不如林放懂礼吗？'),
 h2('sc-3','字义小窗'),
 rows([('旅','祭名。祭名山大川叫「旅」。'),('泰山','天子祭天下名山，诸侯祭境内山川；大夫不在其列。'),
       ('冉有','名求，孔子弟子，时任季氏家宰。'),('救','止也。不是吵架，是设法让它停下来。')]),
 h2('sc-4','共读'),
 scene('夫子没有骂季氏，先问冉有：你在那儿做事，能不能拦？——把话问给「有能力阻止却未阻止」的人。'),
 scene('「曾谓泰山不如林放乎」——林放一个普通人尚且知道问礼之本，泰山之神难道反而分不清谁该来祭？这是反问，不是骂神。'),
 h2('sc-5','生活里的一天'),
 scene('班里规定值周生才能开教室的广播。有同学图方便自己去开了，班长在场，看见了，没说话。事后老师说：我不是问他为什么开，我是问你在场为什么不管。'),
 scene('小区里有人把车停在消防通道，物业看见了只说「没办法」。业主群里有人说：你们不是没办法，是不想得罪人。'),
 h2('sc-6','三个小问题'),
 rows([('问题一','季氏祭泰山，错在哪一步：想去、去了、还是没人拦？'),
       ('问题二','夫子为什么先问冉有，而不是先骂季氏？'),
       ('问题三','你身边有没有「看见了、能管、却没管」的时刻？')]),
 h2('sc-7','成长小启示'),
 rows([('一','看见不对而能说话，沉默也是一种参与。'),
       ('二','拦人之前先想清楚依据：不是「我看不惯」，是「这不合规矩」。'),
       ('三','别用「我人微言轻」提前替自己免责。')]),
])

L45_adult = ''.join([
 h2('sc-lian','连读：僭的第三案'),
 scene('3.1 僭在数，3.2 僭在位，3.6 僭在祭。三章一案比一案重：数可以争，位可以夺，祭则是直接向神冒领名分。夫子这一次不问当事人，问的是「在场而能止者」。'),
 h2('sc-b','字义句读'),
 rows([('旅','祭名。《礼记·王制》：天子祭天下名山大川，诸侯祭名山大川之在其地者。'),
       ('泰山','鲁之望山，在鲁境内，然唯天子与鲁君得祭；大夫祭之，僭。'),
       ('冉有','冉求，字子有，孔子弟子，时为季氏宰。'),
       ('救','止也、匡也。朱子：「救，谓救其陷于僭窃之罪。」'),
       ('曾谓','岂谓、难道说。反问语气。')], k2=True),
 h2('sc-c','三读：谁该被责'),
 scene('一读（朱子）：责冉有。家臣之职在匡正，不能救则当去；既不能救，又不去，是失职。'),
 scene('二读：责季氏。全章以「旅」字立罪，冉有只是引子，重点在僭本身。'),
 scene('三读：责制度。季氏所以敢旅，是因为鲁君失权、礼制无人执行；冉有不能救，是因为他背后没有可依的分。'),
 scene('三读可以并立：罪在季氏，责在冉有，病在制度。夫子一句「曾谓泰山不如林放乎」，把三层都收在里面。'),
 h2('sc-d','章旨'),
 scene('礼之所以能约束人，靠两样：一是名分，二是执行。名分给了「不该」，执行者给了「不许」。季氏越名分，冉有不执行，两样一起失效——于是祭还在做，礼已经不在。'),
 h2('sc-e','三层递进'),
 rows([('事实层','季氏旅于泰山：大夫祭名山，僭。'),('责任层','冉有弗能救：在场而不止，失职。'),
       ('义理层','泰山不如林放乎：神不歆非礼，礼不因势而改。')], k2=True),
 h2('sc-h','存疑'),
 qs(['「旅」一说是「陈设祭品而祭」，一说是「僭祭之专名」；本文取祭名之说。',
     '泰山之祭，鲁君是否得祭，诸家略有异说；大夫不得祭则无异说。',
     '冉有此时是否已为季氏宰，前人多从《论语》本文推定；其年岁与仕历，别无可考。',
     '「曾谓泰山不如林放乎」是反问还是感叹，文章语气有别，义无大异。']),
 h2('sc-i','双卡'),
 cards([('名分：不该','执行：不许'),('季氏：越界者','冉有：在场者'),
        ('救：止之','不救：去之'),('神：不歆非礼','礼：不因势改')]),
 h2('sc-j','跨典'),
 cards([('《八佾》3.1','八佾舞于庭——数之僭。'),
        ('《八佾》3.2','三家以雍彻——位之僭。'),
        ('《先进》11.17','季氏富于周公，而求也为之聚敛——冉有之失，前后一贯。'),
        ('《礼记·曲礼》','临财毋苟得，临难毋苟免——在场者的最低义务。')]),
 h2('sc-19','图一　旅于泰山'),
 figph('图一 · 山道上的一列祭器',
      '山道蜿蜒向上，一列人抬着祭器与牲币行进，为首者衣冠逾制，神情自若；道旁一株古松，松下立一人（冉有）低头不语，手垂着未举。远处山巅有旧祭坛的残石。重心在「人往上走、旁观者不动」，画面零文字。'),
 h2('sc-20','义理图一　祭权的层级'),
 figsvg("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 250" role="img" aria-label="祭权层级：天子、诸侯、大夫">
  <rect x="170" y="30" width="100" height="40" fill="#FFFDF6" stroke="#2F2A24"/>
  <text x="220" y="56" text-anchor="middle" font-size="13" fill="#2F2A24">天子</text>
  <rect x="120" y="96" width="200" height="40" fill="#FFFDF6" stroke="#4A5C55"/>
  <text x="220" y="122" text-anchor="middle" font-size="13" fill="#4A5C55">诸侯 · 祭境内山川</text>
  <rect x="120" y="162" width="200" height="40" fill="#FFFDF6" stroke="#A2503B"/>
  <text x="220" y="188" text-anchor="middle" font-size="13" fill="#A2503B">大夫 · 不得祭名山</text>
  <line x1="220" y1="70" x2="220" y2="96" stroke="#DED2B9"/>
  <line x1="220" y1="136" x2="220" y2="162" stroke="#DED2B9"/>
  <text x="360" y="188" text-anchor="end" font-size="10.5" fill="#8A8074">季氏在此越界</text>
  <text x="220" y="228" text-anchor="middle" font-size="10.5" fill="#8A8074">祭权随分而止：上得下不得，非关诚心</text>
</svg>""",'义理图一 · 祭权是名分的一部分；心再诚，越分即僭。'),
 h2('sc-21','义理图二　三个在场者'),
 figsvg("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 230" role="img" aria-label="季氏、冉有、泰山：越界、失守、不受">
  <circle cx="100" cy="105" r="38" fill="#FFFDF6" stroke="#A2503B"/>
  <text x="100" y="102" text-anchor="middle" font-size="14" fill="#A2503B">季氏</text>
  <text x="100" y="122" text-anchor="middle" font-size="9.5" fill="#8A8074">越界</text>
  <circle cx="220" cy="105" r="38" fill="#FFFDF6" stroke="#2F2A24"/>
  <text x="220" y="102" text-anchor="middle" font-size="14" fill="#2F2A24">冉有</text>
  <text x="220" y="122" text-anchor="middle" font-size="9.5" fill="#8A8074">失守</text>
  <circle cx="340" cy="105" r="38" fill="#FFFDF6" stroke="#4A5C55"/>
  <text x="340" y="102" text-anchor="middle" font-size="14" fill="#4A5C55">泰山</text>
  <text x="340" y="122" text-anchor="middle" font-size="9.5" fill="#8A8074">不受</text>
  <text x="220" y="185" text-anchor="middle" font-size="11" fill="#2F2A24">越界者有人拦，拦不住；受祭者不认，礼才没落地</text>
</svg>""",'义理图二 · 三环断了任何一环，僭都成不了事实——偏偏三环全断。'),
 h2('sc-22','附论一　在场者的责任'),
 scene('「女弗能救与」问得很轻，落到今天却很重：一件事不合规矩，你在场、你有位置、你说得上话——你有没有说？制度不是靠文件运行的，是靠一个个在场者把「不许」说出口。'),
 h2('sc-23','附论二　神不歆非礼'),
 scene('「曾谓泰山不如林放乎」不是神话，是逻辑：如果神真有其神，必不享非分之祭；如果神只是山，那这场祭从头到尾只是人在自我加冕。两种读法指向同一句结论——僭祭，祭的是自己。'),
])

LESSONS = [
 (43,'3.4','林放问礼之本','原文：林放问礼之本。子曰：「大哉问！礼，与其奢也，宁俭；丧，与其易也，宁戚。」',L43_kid,L43_adult),
 (44,'3.5','夷狄之有君','原文：子曰：「夷狄之有君，不如诸夏之亡也。」',L44_kid,L44_adult),
 (45,'3.6','季氏旅于泰山','原文：季氏旅于泰山。子谓冉有曰：「女弗能救与？」对曰：「不能。」子曰：「呜呼！曾谓泰山不如林放乎？」',L45_kid,L45_adult),
]

NO = {'43': '第四十三课', '44': '第四十四课', '45': '第四十五课', '46': '第四十六课', '47': '第四十七课', '48': '第四十八课'}
DESC = {'43': '《论语·八佾》3.4 林放问礼之本。一课两页：少儿页讲礼有本有文，本在敬与哀，偏时宁往本偏；成人页辨「易」字两读（变易／治办）、奢俭与丧易丧戚的取舍，立「宁俭宁戚」的优先级，附存疑一条。', '44': '《论语·八佾》3.5 夷狄之有君，不如诸夏之亡也。一课两页：少儿页讲君在分不在位；成人页辨「亡」两读（无／亡失）与「谁不如谁」两解，三层递到「位在分不在、名存而分亡」，附存疑。', '45': '《论语·八佾》3.6 季氏旅于泰山。一课两页：少儿页讲名分与执行两道；成人页论大夫祭名山之僭、冉有「弗能救」之失职，与 3.1、3.2 合为礼崩三证，附存疑与句读辨。', '46': '《论语·八佾》3.7 射不主皮，为力不同科。一课两页：少儿页讲比的是容仪不是力气，尽力而量力；成人页辨「主皮」与「贯革」、古之道何指，附存疑与双卡。', '47': '《论语·八佾》3.8 绘事后素。一课两页：少儿页讲底子先于花样；成人页辨「素」为白底还是素功、「礼后乎」是先后还是轻重，子夏由诗悟礼，孔子许其可与言诗。', '48': '《论语·八佾》3.9 夏礼吾能言之，杞宋不足征。一课两页：少儿页讲「记得」不等于「有据」；成人页辨「文献」二字（文与献）、能言与能征之别，断在证据不在理解。'}
for lesson, sec, title, srctxt, kid, ad in LESSONS:
    html = PREFIX + '\n' + page(lesson, sec, title, sec, srctxt, kid, ad) + SUFFIX
    html = re.sub(r'<title>.*?</title>', '<title>润泽说 道可道之论语 · ' + NO[str(lesson)] + ' ' + title + '（八佾 ' + sec + '）</title>', html, count=1)
    html = re.sub(r'(name="description" content=")[^"]*(")', lambda m: m.group(1) + DESC[str(lesson)] + m.group(2), html, count=1)
    html = html.replace('</style>', '.fig .ph{height:auto;min-height:88px;padding:10px 14px;align-items:flex-start;line-height:1.85;font-size:13px}\n' + '</style>', 1)
    html = html.replace('</style>', 'pre{white-space:pre-wrap;word-break:break-word;font-family:inherit;font-size:14.5px;line-height:1.9;margin:0}\n' + '</style>', 1)
    html = html.replace('</style>', '.doubt .q:not(:has(span)){grid-template-columns:1fr}\n' + '</style>', 1)
    os.makedirs(f'{ROOT}/src/html', exist_ok=True)
    open(f'{ROOT}/src/html/ke-{lesson}.html','w',encoding='utf-8').write(html)
    print(lesson, len(html))
