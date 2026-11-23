# 自动化（GitHub Actions）

三条流水线，均在 `.github/workflows/`：

| 工作流 | 触发 | 做什么 |
|---|---|---|
| `verify` | push / PR 涉及 `docs/**`、`scripts/**`、`VERSION`、`CHANGELOG.md` | `scripts/verify.py`：版本号一致、课页连续、每课双页标注、入口链接与 JSON-LD 顺序、全站死链、sitemap 覆盖、图位基线、`fig/*.svg` 引用 |
| `live-check` | 每天 09:00（UTC+8）+ 手动 | `scripts/check_live.py --all`：入口、卷首（字节比对）、全部课页与专题页 200 |
| `figs` | 每周一 09:00 + 手动 | 列出仍缺图的课次与合计，写入 Run Summary |

## 本地同款

```bash
python3 scripts/verify.py
python3 scripts/check_live.py --all
```

## 为什么没有 rebuild

`scripts/build_site.py` 的源目录 `../润泽说-论语` 不在仓库内（单课母本在本地工作区），CI 里没有源就无法重出站点。所以本站只做「校验 + 巡检」，重建仍在本地跑：

```bash
python3 scripts/build_site.py      # 需 ../润泽说-论语
python3 scripts/build_book_md.py
```

若哪天把母本收进仓库（如 `src/`），再把 `build_site.py` 的 `SRC` 指向它，就能接上「推送即重建」。

## 图位基线

`scripts/expected.json` 里 `placeholders` 为当前允许的最大图位数（现 22）。补图后若校验报「图位已减至 N」，把该值下调到 N 即可；若报「> 基线」，说明有新课带进了未登记的图位。

## 边界

- `verify` 只查结构与一致性，不判文案义理。
- 目录顺序、JSON-LD `hasPart` 顺序已纳入校验——v0.15.47 之前第 27–29 课曾逆序，现已改正（`scripts/build_site.py` 的 `COURSES` 同步调整）。
