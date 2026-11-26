# -*- coding: utf-8 -*-
"""v0.15.98 收口脚本：乡党 10.11–10.15（第 249–253 课）
生成页 → 抽十图 → 写五母本 → 串合稿 → 改索引 → 升站点 → 记 CHANGELOG → 推送
任一步断言失败即中止（不提交、不推送）。
"""
import os, re, json, subprocess, sys

ROOT = '/home/user/Doubao/chats/38450693190946306/daokedao-lunyu'
os.chdir(ROOT)
VER = open('VERSION', encoding='utf-8').read().strip()
assert VER == '0.15.98', VER


def sh(cmd, check=True):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise SystemExit('CMD FAIL: %s\n%s\n%s' % (cmd, r.stdout[-400:], r.stderr[-800:]))
    return r.stdout


# 1. 生成页
sh('python3 src/ke-249-253.py')

# 2. 校验页
SLUG = {249: ['ke249-ji-zhi-cheng', 'ke249-shu-yu-sheng'],
        250: ['ke250-xi-zheng', 'ke250-wei-yu-xin'],
        251: ['ke251-zhang-zhe-xian', 'ke251-xian-yu-hou'],
        252: ['ke252-nuo-yu-zhao-fu', 'ke252-jing-yu-an'],
        253: ['ke253-zai-bai', 'ke253-yuan-yu-jin']}
for n, (a, b) in SLUG.items():
    s = open('docs/ke/%d.html' % n, encoding='utf-8').read()
    han = len(re.findall(r'[\u4e00-\u9fa5]', re.sub(r'<[^>]+>', '', s)))
    assert s.count('class="h2"') == 20, (n, s.count('class="h2"'))
    assert s.count('class="figsvg"') == 2, n
    assert han > 1700, (n, han)
    assert 'v%s' % VER in s, n
    svgs = re.findall(r'<div class="figsvg">(<svg .*?</svg>)</div>', s, re.S)
    assert len(svgs) == 2
    for slug, sv in ((a, svgs[0]), (b, svgs[1])):
        x = sv.replace('\n', '').replace('  ', ' ')
        open('assets/%s.svg' % slug, 'w', encoding='utf-8').write(x)
        open('docs/fig/%s.svg' % slug, 'w', encoding='utf-8').write(x)
    print(n, han, a, b)

# 3. 五母本
FILES = {249: '249-shu-shi-cai-geng.md', 250: '250-xi-bu-zheng.md',
         251: '251-zhang-zhe-xian-chu.md', 252: '252-nuo-yu-zuo-jie.md',
         253: '253-wen-ren-yu-ta-bang.md'}
TITLES = {249: ('10.11', '虽疏食菜羹，瓜祭，必齐如也'),
          250: ('10.12', '席不正不坐'),
          251: ('10.13', '乡人饮酒，杖者出，斯出矣'),
          252: ('10.14', '乡人傩，朝服而立于阼阶'),
          253: ('10.15', '问人于他邦，再拜而送之')}

MD = {}
MD[249] = dict(
    yi='雖疏食，菜羹，瓜祭，必齊如也。',
    jiao='底本「瓜祭」，今传通行本多作「必祭」。朱子《集注》于「瓜」下自注「或作必」，是宋时两本并行。两存不改正文：一说「瓜祭」为祭瓜（郑注一路，谓祭五种菜蔬之属）；一说「瓜」为「必」之形讹，「凡食必祭」。正文从底本，异文入存疑。',
    zi='疏食：粗粮饭。菜羹：以菜为羹，无肉。瓜祭：祭瓜；一本作「必祭」。齊（斋）如：敬貌如斋戒之时。',
    du='「瓜祭」两读：祭瓜（本文主）／「瓜」作「必」之讹（校勘一路）。两存。「必齊如」之「齊」读斋，非「整齐」——敬由内发，不由外束。',
    zhi='食前必祭，祭必齐如：敬不以物之丰俭而改。饭薄、羹薄，而祭不薄、敬不薄。',
    ceng='一、雖疏食（饭之薄）；二、菜羹（羹之薄）；三、瓜祭（先祭而后食）；四、必齊如也（敬之厚）。',
    tu='图一：一簋粗饭、一豆菜羹，案前作揖，无牲无酒。图二：外（所祭不在鬼神）／内（所敬是这一口饭的分量）。',
    shu='疏食 3 见 3 章（7.16、10.11、14.9）；菜羹 1 见（孤例）；瓜 2 见 2 章（10.11；17.7 匏瓜义别）；齊如 1 见（孤例）；祭 14 见 10 章。',
    lun='上章记食寝之默（10.10），此章记食前之祭：一默于食时，一敬于食先。')
MD[250] = dict(
    yi='席不正不坐。',
    jiao='底本六字，字句与标点核对无误。内证：本篇 10.18「君賜食，必正席先嘗之」——「正席」再见，一为君赐而正，一为自坐而正。',
    zi='席：布地而居之席。正：布之合位，不偏斜。坐：跪坐，古人之坐。',
    du='「正」两读：布席合位（本文主）／席面整齐（义近而浅）。「不坐」两读：不坐此席（本文主）／先正而后坐（动作先后）。两读可合。',
    zhi='席有其位，布之必正；不正则不居。',
    ceng='一、席（有其位）；二、不正（失其位）；三、不坐（不居其位）。',
    tu='图一：两张蒲席并列，一正一偏，一人提席一角欲正之。图二：外（席之位）／内（心之位）。',
    shu='席 4 见 3 章（10.12、10.18、15.42）；本章 1 见；「席不正」1 见，「正席」1 见（10.18）。',
    lun='上章记食前之祭（10.11），此章记坐席之正：一敬于食，一敬于坐。')
MD[251] = dict(
    yi='鄉人飮酒，杖者出，斯出矣。',
    jiao='底本作「飮酒」，「飮」为「飲」之异体（底本「飮」5 见、「飲」0 见，全书一律作「飮」），非讹，不改。「斯出矣」句末「矣」无讹。',
    zi='鄉人：同乡之人。飮酒：乡饮酒之礼，乡党之会。杖者：老人，六十杖於鄉。斯：乃、才。',
    du='「杖者」两读：六十以上之老人（本文主）／泛称执杖者（义泛，不取）。朱子「未出不敢先，既出不敢後」十字，是此节之骨。',
    zhi='乡饮有序：杖者先出，己乃随出——未出不敢先，既出不敢後。',
    ceng='一、鄉人飮酒（与众同乐）；二、杖者出（长者先）；三、斯出矣（己随其后）。',
    tu='图一：乡饮散席，白发老人拄杖出门，一人垂手侧立于门内。图二：先（未出不敢先，让）／后（既出不敢後，随）。',
    shu='鄉人 5 见 3 章（10.13、10.14、13.24）；杖 4 见 3 章（本章指人；14.43、18.7 指杖本身）；飮 5 见 5 章（3.7、6.11、7.16、8.21、10.13）。',
    lun='上章记坐席之正（10.12），此章记乡饮之序：一正于己之位，一让于人之长。')
MD[252] = dict(
    yi='鄉人儺，朝服而立於阼階。',
    jiao='底本用正字「儺」，通行简作「傩」（底本「傩」0 见），字异义同，不改。「阼階」为东阶，主人之位。',
    zi='儺：驱疫之礼，戴面具、击鼓。朝服：君臣朝会之服，非祭服。阼階：东阶，主人之位。立：不敢坐。',
    du='「朝服」而非祭服：乡人傩非国祭，故不着祭服——敬其事而不僭其礼。「立於阼階」两义：敬其事（朱子前说）／安先祖之灵（朱子后说）。两义可合：敬与安，一事两面。',
    zhi='乡傩及门，朝服立阼阶：敬其事，安先祖。',
    ceng='一、鄉人儺（其事非常）；二、朝服（其服非常）；三、立於阼階（其位不移）。',
    tu='图一：夜门外傩队戴面具执戈盾而过，门内一人朝服立于东阶。图二：敬其事（对他）／安先祖（对己）。',
    shu='儺 1 见（孤例，底本正字；「傩」0 见）；阼 1 见（孤例）；階 5 见 4 章（10.4、10.14、15.42、19.25）；朝服 3 见 3 章（10.6、10.14、10.19）。',
    lun='上章记乡饮之序（10.13），此章记乡傩之敬：让是退，敬是立——退与立，皆不失其位。')
MD[253] = dict(
    yi='問人於他邦，再拜而送之。',
    jiao='底本字句与标点核对无误。「再拜」为礼之重者；「他邦」全书 2 见，一为陈文子去国（5.19），一即本章。',
    zi='問：问讯、问候（非问事）。他邦：他国。再拜：拜而再拜，重礼。送之：送使者之行。',
    du='朱子「拜送使者，如親見之，敬也」——所拜在远方，借使者一行其礼：形在使者，意在那人。「如亲见之」四字是全章钥匙：人不能亲至，礼可以代至。',
    zhi='问远必拜，拜如亲见：礼能代人到场。',
    ceng='一、問人於他邦（身不能至）；二、再拜（礼代其身）；三、而送之（礼及于行）。',
    tu='图一：门外土路，使者负简策执币帛欲行，一人俯身再拜于门内。图二：近（10.1–10.14 乡人）／远（10.15 他邦）。',
    shu='問人 1 见（孤例）；他邦 2 见 2 章（5.19、10.15）；拜 6 见 5 章（9.3、10.15、10.16、10.23、17.1）；送 1 见（孤例）。',
    lun='上章记乡傩之敬（10.14），此章记问远之敬。本篇始于「恂恂如也，似不能言者」（10.1），至此五节祭、坐、饮、傩、送，皆与乡人相处之分寸——敬无远近，皆是此人。')

os.makedirs('manuscript/xiang-dang', exist_ok=True)
for n, fn in FILES.items():
    ref, title = TITLES[n]
    d = MD[n]
    body = f"""# 乡党 {ref}　{title}

> 润泽说 · 道可道之论语 · 上论　第 {n} 课

## 原文

{d['yi']}

## 校记

{d['jiao']}

## 字义

{d['zi']}

## 两读

{d['du']}

## 章旨

{d['zhi']}

## 三层

{d['ceng']}

## 图

{d['tu']}

- **SVG**：见 `docs/ke/{n}.html` 页内，另见 `docs/fig/{SLUG[n][0]}.svg`
- **SVG**：见 `docs/ke/{n}.html` 页内，另见 `docs/fig/{SLUG[n][1]}.svg`

## 数证

{d['shu']}

## 连读

{d['lun']}
"""
    open('manuscript/xiang-dang/' + fn, 'w', encoding='utf-8').write(body)
    print('md', fn, len(body))

# 4. 串合稿：探测既有 10.x 标题式样，按同式追加
BOOK = 'book/润泽说 道可道之论语·上论（已刊）.md'
bk = open(BOOK, encoding='utf-8').read()
pats = [r'^## 10\.1[^0-9]', r'^# 10\.1[^0-9]', r'^### 10\.1[^0-9]']
hit = None
for p in pats:
    if re.search(p, bk, re.M):
        hit = p
        break
assert hit, '合稿内未找到 10.1 标题式样，停手'
print('合稿式样', hit)
prefix = hit.lstrip('^').split('10')[0].rstrip()
if not bk.endswith('\n'):
    bk += '\n'
for n in (249, 250, 251, 252, 253):
    ref, title = TITLES[n]
    d = MD[n]
    bk += f"\n{prefix} {ref}　{title}\n\n{d['yi']}\n\n{d['zhi']}\n\n{d['ceng']}\n\n{d['tu']}\n\n{d['shu']}\n"
open(BOOK, 'w', encoding='utf-8').write(bk)
print('合稿字数', len(bk))

# 5. 索引
s = open('scripts/build_site.py', encoding='utf-8').read()
NEW = [
    ('249', '第二百四十九课', TITLES[249][1], '食前之祭：物薄敬厚，祭必齐如。疏食 3 见、菜羹孤例、齊如孤例。'),
    ('250', '第二百五十课', TITLES[250][1], '席有其位，不正不居；先正后坐。席 4 见 3 章。'),
    ('251', '第二百五十一课', TITLES[251][1], '乡饮有序：杖者先出，己乃随出。鄉人 5 见、杖 4 见。'),
    ('252', '第二百五十二课', TITLES[252][1], '傩及门，朝服立阼阶：敬其事、安先祖。儺、阼各孤例。'),
    ('253', '第二百五十三课', TITLES[253][1], '问远必拜，拜如亲见。問人、送各孤例；他邦 2 见。'),
]
anchor = '''"八字两事：语（答人）默于食、言（自言）默于寝；范氏「存心不他」为正解。語 15 见／不言 6 见，本章各 1。字句标点核对无误。数证：不言 6。"),
]'''
assert anchor in s, '锚点不在'
add = '''"八字两事：语（答人）默于食、言（自言）默于寝；范氏「存心不他」为正解。語 15 见／不言 6 见，本章各 1。字句标点核对无误。数证：不言 6。"),
'''
for no, cn, title, gist in NEW:
    add += '    ("%s", "论语·%s·%s（乡党10.%s）（阅读版）.html", "%s", "%s",\n     "%s"),\n' % (
        no, cn, title.split('，')[0].replace('，', ''), no[1:].lstrip('0'), cn, title, gist)
add += ']'
s = s.replace(anchor, add, 1)
s = s.replace('乡党十节（10.1–10.10）', '乡党十五节（10.1–10.15）')
s = s.replace('已刊二百四十八课', '已刊二百五十三课')
s = s.replace('· 乡党十节', '· 乡党十五节')
s = s.replace('二百四十一件', '二百四十六件').replace('241 件', '246 件')
open('scripts/build_site.py', 'w', encoding='utf-8').write(s)

e = json.load(open('scripts/expected.json', encoding='utf-8'))
e['placeholders'] = 193
json.dump(e, open('scripts/expected.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('placeholders', e['placeholders'])

# 6. 站点
out = sh('python3 scripts/build_site.py')
print(out[-200:])

# 7. CHANGELOG
cl = open('CHANGELOG.md', encoding='utf-8').read()
entry = f"""## v{VER}　乡党 10.11–10.15（第 249–253 课）

- 五课：10.11 虽疏食菜羹瓜祭必齐如也｜10.12 席不正不坐｜10.13 乡人饮酒杖者出斯出矣｜10.14 乡人傩朝服而立于阼阶｜10.15 问人于他邦再拜而送之。
- 主线：由「食」转入「与人」——祭、坐、饮、傩、送五节，皆与乡人相处之分寸；末章以「再拜而送」回照 10.1「恂恂如也」。
- 校记四事：10.11「瓜祭」与通行「必祭」异文（朱子注「瓜，或作必」）两存不改；10.13「飮」为「飲」异体（全书写「飮」5 见、「飲」0 见）；10.14「儺」用正字（「傩」0 见）、「阼階」东阶主人位；10.12、10.15 无误。
- 十图：ke249-ji-zhi-cheng／ke249-shu-yu-sheng；ke250-xi-zheng／ke250-wei-yu-xin；ke251-zhang-zhe-xian／ke251-xian-yu-hou；ke252-nuo-yu-zhao-fu／ke252-jing-yu-an；ke253-zai-bai／ke253-yuan-yu-jin。
- 五母本：manuscript/xiang-dang/249–253。
- 站点：246 件、二百五十三课、乡党十五节；图位基线 193。

"""
open('CHANGELOG.md', 'w', encoding='utf-8').write(entry + cl)

# 8. README
rd = open('README.md', encoding='utf-8').read()
rd = rd.replace('v0.15.97', 'v0.15.98').replace('二百四十八课', '二百五十三课').replace('乡党十节', '乡党十五节')
open('README.md', 'w', encoding='utf-8').write(rd)

# 9. 校验
v = sh('python3 scripts/verify.py', check=False)
print('verify:', v[-300:])
assert 'OK' in v, v[-400:]
