# 86 HUD · 安装与配置指南 (v5)

> Windows 端安装本主题、加载组件、接好音乐源的完整步骤。
> 本主题基于《86 -エイティシックス-》的视觉语言：**左侧竖直指挥栏 + 主视觉留白 + 成员纹章 Dock**，
> 一套透明 HUD 叠加皮肤，叠在任意 86 壁纸 / Wallpaper Engine 动态壁纸之上。
> 视觉基准：`@Resources/docs/preview/v5/index.html`（浏览器打开看目标效果）。

---

## 0. 前置：安装 Rainmeter

1. 到 [rainmeter.net](https://www.rainmeter.net/) 下载安装 Rainmeter（4.5+，建议最新版）。
2. 安装后会建立 `文档\Rainmeter\Skins\` 皮肤目录。

## 1. 部署本皮肤

把仓库里的 **`EightSix86`** 整个文件夹拷到：

```
C:\Users\<你>\Documents\Rainmeter\Skins\EightSix86\
```

> 让 `…\Skins\EightSix86\@Resources\Variables.inc` 路径存在。
> 拷完在 Rainmeter 托盘右键 → **Refresh All**。

## 2. 放入字体（要 100% 还原 v5 需要这步）

v5 用了 3 个开源字体，随包分发。按 `@Resources\Fonts\README.md` 把以下文件放进 `@Resources\Fonts\`：

- `Oxanium-Light.ttf` / `Oxanium-SemiBold.ttf`（时钟/标题/数值）
- `ChakraPetch-Medium.ttf` / `ChakraPetch-SemiBold.ttf`（标签/表格）
- `NotoSansSC-Regular.otf`（中文）

> 都在 [Google Fonts](https://fonts.google.com/) 免费下载（SIL OFL，可分发）。
> **不放也能用** —— 自动回退 Bahnschrift / YaHei（Win 自带），只是字形略有差异。

## 3. 加载组件（v5 三个核心 config）

打开 Rainmeter 管理器，在 `EightSix86` 下 **Load** 这三个，按下表锚点摆放（拖到位即记住）：

| 组件 | config | 画布 | 桌面锚点 |
|---|---|---|---|
| **左侧指挥栏**（86标识+花名册+音乐+日历） | `Rail\Rail.ini` | 312×1080 | **贴屏幕左上角 (0,0)**，竖直全高 |
| **中央时钟**（主视觉，纯白） | `Clock\Clock.ini` | 600×380 | 右侧留白区居中：X≈ 312+(屏宽−312)/2−300，Y 居中略偏上 |
| **成员纹章 Dock** | `Dock\Dock.ini` | 760×110 | 右侧留白区底部居中：X 同时钟居中，Y≈ 屏高−150 |

例：1920×1080 屏 →
- Rail: (0, 0)
- Clock: X = 312 + (1920−312)/2 − 300 = **816**，Y ≈ **307**
  （时钟大字中心落在屏幕约 46% 高度处，对齐 v5「主视觉居中略偏上」；
   画布 600×380，大字中心约在画布内 Y190，故 1080×0.46−190 ≈ 307）
- Dock: X ≈ 816 + 300 − 380 = **736**，Y ≈ **930**

> 经 ini 坐标 1:1 布局验证（`@Resources/docs/preview/v5-ini-verify/layout.png`），
> 以上锚点下整屏布局与 v5 预览一致。拖动时按住对齐即可，Rainmeter 记住坐标。

> 旧组件 `System` / `Calendar` / `Music` / `Search` / `Disk` / `Network` 等保留兼容，
> v5 下**不再单独加载**（功能已并入 `Rail.ini`）。

## 4. 音乐源接入（Rail 的 MEDIA 区需要）

Rail 的音乐/歌词走 **WebNowPlaying-Redux**：

1. 装 Rainmeter 插件 [WebNowPlaying-Redux](https://github.com/keifufu/WebNowPlaying-Redux)（`.rmskin` 双击装）。
2. 浏览器听歌装对应扩展；桌面网易云/QQ音乐装 [WNP-Redux SMTC adapter](https://github.com/keifufu/WebNowPlaying-Redux-SMTC)。

不想装？改 `Variables.inc` 的 `MusicSource`：`Spotify`（免装第三方）/ `TitleSniff`（退化）。
没装时不报错，显示占位曲目，进度 pin 停最左。

> 注：v5 的**实时歌词**当前是占位三行。Rainmeter 原生无歌词流，
> 落地实时歌词需 WNP 歌词扩展或外部 LRC 插件，见第 7 节路线。

## 5. 个性化 `@Resources\Variables.inc`

- **面板透明度**：`GlassAlpha`（0–255）控制左侧栏毛玻璃浓度。对应 v5 预览顶部的透明度滑块。
  默认 56（≈22%）。**改了它要同步改 `ColorGlass` 第 4 位**（或保持用动态引用）。
- **Dock 启动路径**：`DockUndertakerPath` / `DockBlackDogPath` / `DockGunSnakePath` /
  `DockLaughingFoxPath` / `DockSnowWitchPath` 改成你的程序/文件夹。
- **配色**：`Color*`（ice / steel / mist / crimson）一组定义冰蓝白军用色，统一生效。
- **网络带宽**：Rail.ini 的 `NetInSpeed` / `NetOutSpeed`（bit/s）按实际带宽调，百分比才准。

改完 Refresh 对应组件。

## 6. 毛玻璃模糊（可选增强）

Rail.ini 已开 `Blur=1`（Win10/11 DWM 模糊），让半透明底真正"毛玻璃"。
不支持/不想要就把 `[Rainmeter] Blur=1` 删掉，退化为纯半透明（视觉仍接近 v5）。
想要更强的 acrylic/mica，可装 [FrostedGlass 插件](https://forum.rainmeter.net/viewtopic.php?t=44887)。

## 7. 已知占位 / 落地后续（诚实清单）

以下在 macOS 无法验证，需在 Windows 实机调：

| 项 | 现状 | 落地补法 |
|---|---|---|
| GPU 温度 | 占位常量 54°C | 装 HWiNFO/CoreTemp 插件，把 `[mGpuTemp]` 换成对应 measure |
| 实时歌词 | 占位三行日文 | 接 WNP 歌词扩展或 LRC 插件 |
| 网络速率箭头 | 静态 ▲/— | 可接 Lua 对比上次值动态算趋势（旧 `Roster.lua` 有现成逻辑可移植） |
| 字体 | 需手动放入（见第 2 节） | 放入后 100% 还原；否则兜底 |
| 各组件坐标 | 需手动拖到锚点 | 按第 3 节表格摆放 |

## 8. 排错

| 现象 | 处理 |
|---|---|
| 字体显示成 Bahnschrift/方框 | 按第 2 节放入字体文件到 `@Resources\Fonts\` |
| 左侧栏不透明/太透 | 调 `Variables.inc` 的 `GlassAlpha` |
| 时钟 CPU 占用偏高 | Clock 用 125ms tick 驱动冒号呼吸；调 `[Rainmeter] Update=200` |
| 音乐进度 pin 不动 | 没装音乐源插件（第 4 节）或 player 不被 WNP 支持 |
| 日历日期不对 | `Calendar.lua` 按系统时间算；确认系统日期正确，Refresh Rail |
| 纹章 hover 无反应 | 确认加载的是 v5 `Dock.ini` |

---

各版浏览器预览稿见 `@Resources\docs\preview\v5\index.html`（双击看目标效果与动效）。
