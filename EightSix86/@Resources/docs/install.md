# 86 HUD · 安装与配置指南

> Windows 端安装本主题、加载各组件、接好音乐源的完整步骤。
> 本主题基于动画《86 -エイティシックス-》的视觉语言，是一套**透明 HUD 叠加**皮肤，
> 可直接覆盖在任意 86 壁纸 / Wallpaper Engine 动态壁纸之上。

---

## 0. 前置：安装 Rainmeter

1. 到 [rainmeter.net](https://www.rainmeter.net/) 下载并安装 Rainmeter（4.5+，建议最新版）。
2. 安装后 Rainmeter 会在 `文档\Rainmeter\Skins\` 建立皮肤目录。

## 1. 部署本皮肤

把仓库里的 **`EightSix86`** 整个文件夹拷到：

```
C:\Users\<你>\Documents\Rainmeter\Skins\EightSix86\
```

> 即让 `…\Skins\EightSix86\@Resources\Variables.inc` 这个路径存在。
> 拷贝后在 Rainmeter 托盘图标右键 → **Refresh All**，皮肤就会出现在管理器里。

## 2. 加载组件（建议顺序与锚点）

打开 Rainmeter 管理器（双击托盘图标），在 `EightSix86` 下逐个 **Load** 以下 config，
按 v1 设计的布局摆放（拖动到位即可，位置会被记住）：

| 组件 | config | 建议位置 |
|---|---|---|
| 中央时钟（主视觉） | `Clock\Clock.ini` | 屏幕正中 |
| 系统名册 | `System\System.ini` | 左上 |
| 日历 Chronos | `Calendar\Calendar.ini` | 右上 |
| 搜索 · Google | `SearchGoogle\SearchGoogle.ini` | 顶部居中 |
| 搜索 · Bing | `SearchBing\SearchBing.ini` | Google 下方（可选，二选一也行） |
| 音乐播放器 | `Music\Music.ini` | 底部居中偏上 |
| 启动器 Dock | `Dock\Dock.ini` | 底部居中 |

> 旧组件 `Disk` / `Network` / `Recycle Bin` / `Google` 仍保留以兼容，但其功能已被
> System Roster + Search + Dock 接管，无需再加载。

## 3. 字体（多数无需手动装）

主题字体栈全部使用 **Windows 10/11 自带字体**，正常情况开箱即用：

- `Bahnschrift`（几何无衬线，HUD 主字）— Win10/11 自带
- `Microsoft YaHei UI`（中文）— 自带
- `Segoe UI Symbol` / `Segoe MDL2 Assets`（图标 / 月相 / 播放控件）— 自带
- `Impact`（System Roster 的 DESTROYED 红戳）— 自带

若某些符号显示成方框（如 System 月相 ◔◕、Music 控件 ⏸⏵），多半是该字体在你机器上缺字形，
见第 6 节「排错」。

## 4. 音乐源接入（Music 组件需要）

Music 默认走 **WebNowPlaying-Redux**（支持网页版 / 桌面版网易云、QQ 音乐、Spotify、YTM 等）：

1. 装 Rainmeter 端插件：[WebNowPlaying-Redux](https://github.com/keifufu/WebNowPlaying-Redux)（下载 `.rmskin` 双击安装）。
2. 浏览器搜索听歌：装对应浏览器扩展。
3. 桌面客户端（网易云 / QQ 音乐）听歌：装 [WNP-Redux SMTC adapter](https://github.com/keifufu/WebNowPlaying-Redux-SMTC) 桥接系统媒体控件。

不想装插件？编辑 `@Resources\Variables.inc` 把 `MusicSource` 改成：
- `Spotify` — 用 Rainmeter 自带 NowPlaying 插件（仅 Spotify，免装第三方）
- `TitleSniff` — 退化模式，只读焦点窗口标题（无进度 / 封面）

> 没装音乐源时 Music 组件不会报错，只是显示"未在播放"、进度 pin 停在最左。

## 5. 个性化配置 `@Resources\Variables.inc`

用记事本 / VS Code 打开，按需改：

- **Dock 启动路径**：`DockDevPath` / `DockDocPath` / `DockGamePath` / `DockMediaPath`
  改成你自己的文件夹或程序（`DockBinPath` 是回收站，勿动）。
- **配色**：`Color*` 一组变量定义了「红彼岸花 × 钴蓝」主题色，想微调整体色调改这里即可，
  全部组件统一生效。
- **网络带宽**：System Roster 的 `NetInSpeed` / `NetOutSpeed`（在 `System\System.ini`）
  按你的实际带宽（bit/s）调，百分比才准。

改完在 Rainmeter 里 Refresh 对应组件。

## 6. 排错

| 现象 | 原因 / 处理 |
|---|---|
| 月相 / 控件显示成 □ 方框 | `Segoe UI Symbol` 缺该字形：把对应组件的该 meter `FontFace` 换成 `Segoe MDL2 Assets`，或退化用 `◐` |
| DESTROYED 戳字距怪异 | `Impact` 渲染差异：调 `[stDestroyed]` 的 `FontSize` 或去掉字母间空格 |
| 中央时钟 CPU 占用偏高 | Clock 用 125ms tick 驱动冒号呼吸；嫌高就把 `[Rainmeter] Update` 调到 200、`mBreathTick` 模数改 16 |
| Music 进度 pin 不动 | 没装音乐源插件（见第 4 节），或当前 player 不被 WNP 支持 |
| Dock 图标 hover 无反应 | 确认加载的是本仓库 v1.1+ 的 `Dock.ini` |

## 7. 当前版本组件能力速览（v1.2）

- **System Roster**：月相/趋势/状态点全部数据驱动；网络断流盖 DESTROYED 红戳；开机扫描进场。
- **Clock**：三段进场揭示；冒号正弦呼吸。
- **Music**：进度 pin 跟随；播放/暂停图标切换；控件 hover 微交互。
- **Dock**：5 个 Spearhead 个人 mark；hover 上移 + 变亮 + 角括号浮现。
- **Calendar**：上下月跨月 bug 已修；年度进度条。
- **Search**：Google / Bing 双引擎；输入框 + dispatch 按钮 hover 高亮。

各组件的浏览器预览稿见 `@Resources\docs\preview\iter*.html`（双击用浏览器打开，可直接看动效）。
迭代细节见 `@Resources\docs\v2-iteration-log.md`。
