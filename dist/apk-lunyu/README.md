# 道可道之论语 · Android APK 打包工程

WebView 宿主 + 全站 assets（首页、卷首、511 课、专题八篇、内嵌宋体）。包名 `com.runze.daokedaolunyu`，minSdk 21，targetSdk 35，零权限。

## 两条构建路径

| 路径 | 命令 | 说明 |
|---|---|---|
| 本地手工链（推荐，最快） | `SDK_ROOT=/path/to/sdk ./build.sh` | aapt2 → javac → d8 → zipalign → apksigner，不拉 gradle；产物 `../../dist/道可道之论语-v0.16.42.apk` |
| GitHub Actions | `.github/workflows/apk.yml` | 装 commandlinetools、platforms;android-35、build-tools;35.0.0、fonts-noto-cjk，先跑 `scripts/build_apk_assets.py` 再 `gradlew assembleDebug` |

SDK 只需三件：`build-tools/35.0.0`（aapt2、d8、zipalign、apksigner）、`platforms/android-35/android.jar`、JDK 17。
`build.sh` 以 `SDK_ROOT` 环境变量定位，缺省 `/home/user/apkbuild/sdk`。

## assets 从哪来

`scripts/build_apk_assets.py` 把 `docs/` 的离线可读部分灌进 `app/src/main/assets/`，可反复重跑：

- 收：`index.html`、`book.html`、`xing-e.html`、`ke/`（512 页）、`zt/`（8 页）、图标与 manifest。
- 不收：`fig/`（课页插图已是内嵌 `data:image/webp`）、`_shots/`、`fig/_history/`、sitemap、下载块。
- 改写：站内绝对地址（`https://q1z2q3-debug.github.io/daokedao-lunyu/`、`/daokedao-lunyu/`）→ 按页深补 `../` 的相对路径；裸 `index.html` 回链按层修正；`sitemap.xml` 链接与 `<!-- apk-dl:start -->` 下载块剥除；`ke/24`、`ke/25` 的外链字体样式表删除。
- 字体：取全部页面用字（约 3974 字）从系统 `NotoSerifCJK-Regular/Bold.ttc`（SC 为第 3 个 face，`--font-number=2`）子集化出两档 woff2，置于 `assets/fonts/`，并给每页注入 `@font-face`（家族名就叫 `"Noto Serif SC"`，页面原 CSS 无需改动即命中）。不嵌则安卓落回黑体，失纸墨味。

## 产物与签名

- 包内 `classes.dex` 只有宿主 Activity；签名走本地 `.debug.keystore`（不入库），v1/v2/v3 三签齐全。
- 版本：`versionCode 16041`、`versionName 0.16.41`，与 `VERSION` 同步。升版改 `app/build.gradle` 与 `build.sh` 的 `CODE`/`NAME` 两处。
- 发布：`cp dist/道可道之论语-vX.apk docs/dl/daokedao-lunyu-vX.apk`，在 `docs/dl/` 重算 `SHA256SUMS.txt`，首页下载块里的文件名与体积同步改。

## 已知边界

- 未做真机安装验证；本机只做 aapt2 badging、apksigner、zipalign 与 file:// 断链校验。
- debug 签名换机重装会冲突，需先卸载；稳定 release 签名未定。
