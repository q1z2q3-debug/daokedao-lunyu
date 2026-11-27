# 论语 · 应用图标（侧身授业）

作者于 2026-11-27 回传 `论语APK图标_侧身授业.zip`，此库为其入库版本。

## 设计定稿

- 形：米色纸底（`#F7F4EE`），双细朱环（`#A2503B`），环内为孔子侧身、右手前伸授业之墨黑剪影。
- 四稿曾并置比较（见 `论语图标_48px四稿对比.png`）：一为侧身授业，二为背影，三为正面抚坐，四为侧立细长。取第一稿——48px 下轮廓不塌、手势可辨。
- 与《礼记》同系列并置见 `礼记_论语_图标并排.png`：同纸底、同墨色，本篇独取圆环以别之。

## 水印处理

原 1024 图右下角带一行「元宝 AI 生成」，位在 x 847–996、y 946–1011。此处是纸地，非画面，故取上方同宽纹理覆盖补齐，未裁边、未缩放，图形与环分毫不损。`ic_launcher_foreground.png` 原为透明前景层，无水印，存原样。

## 文件用途

| 文件 | 用途 |
|---|---|
| `ic_launcher_1024.png` | 母图，1024 方，去水印后原像素 |
| `mipmap-mdpi/…` 至 `mipmap-xxxhdpi/` | Android 各密度 legacy 图标（48／72／96／144／192），由母图缩 |
| `mipmap-xxxhdpi/ic_launcher_foreground.png` | adaptive 前景层，1024 RGBA，含安全区留白 |
| `mipmap-anydpi-v26/ic_launcher.xml` | adaptive-icon 声明：底取 `@color/ic_launcher_background`，前景与单色层同用 foreground |
| `values/colors.xml` | 底色 `#F7F4EE` |

打包时把 `mipmap-*` 与 `values/colors.xml` 原样并入 `app/src/main/res/`，`ic_launcher.xml` 放 `res/mipmap-anydpi-v26/`。

## 站点对应件

- `docs/icon-192.png`、`docs/icon-512.png`、`docs/icon-1024.png`：由母图缩，manifest 三档（192 any／512 any＋maskable／1024 any）。
- `docs/apple-touch-icon.png`：180 方，iOS 主屏用。
- `docs/og.png`：1200×630，左书名右圆图，与站点同底同色。
- `docs/favicon.svg` 仍为朱底「论」字印——十六像素下剪影难辨，故标签页保留字印，安装图标用剪影，各司其职。
