# 86 HUD Rainmeter Skin — v1 设计定稿

> 基于动画《86 -エイティシックス-（86：不存在的战区）》视觉语言的 Rainmeter 桌面 HUD 皮肤组件库。
> 本文为 v1 锁定设计稿。后续视觉/交互调整请以 v2/v3 增量文档形式追加。

---

## 1. 设计哲学

**透明 HUD 叠加，drop-in 任意 86 壁纸。** 所有组件无背景填充，仅以线条 / 文字 / text-shadow / cyan glow 构造可读性，能完美兼容 Wallpaper Engine 任意 86 主题动态壁纸。

**不喧宾夺主。** Wallpaper 是主体，HUD 是参谋。颜色、构图、动画都为壁纸让位。

**86 美术语言保真。** 不是"赛博朋克 cyan UI"，而是动画里 main_desk / battle_field / system_status 截图所定义的具体语言：编号前缀 (001/002)、月相状态点、DESTROYED 红戳、scan stripe 高光条、菱形端点、Bahnschrift 等宽。

---

## 2. 调色板

| 用途 | 变量 | 值 |
|---|---|---|
| 主色 cyan | `--cyan` | `#7ee5f5` |
| cyan 亮边 | `--cyan-edge` | `rgba(126, 229, 245, 0.95)` |
| cyan 弱化 | `--cyan-dim` | `rgba(126, 229, 245, 0.45)` |
| cyan 极淡 | `--cyan-deep` | `rgba(126, 229, 245, 0.18)` |
| 警示红 | `--red` | `#ff5252` |
| 警示红弱化 | `--red-dim` | `rgba(255, 82, 82, 0.85)` |
| 主文字 | `--text` | `#f5fbff` |
| 弱文字 | `--text-dim` | `rgba(245, 251, 255, 0.7)` |
| 描边阴影 | `--shadow` | `0 0 4px rgba(0, 8, 18, 0.95), 0 0 1px rgba(0, 8, 18, 0.95)` |
| cyan 辉光 | `--glow` | `0 0 6px rgba(126, 229, 245, 0.7)` |

**色彩规则**
- 数据组件 (System/Clock/Calendar) 一律 cyan
- 警示状态 (NET DOWN / 磁盘满 / 回收站待清) 用 red，且仅在该行/该 launcher 上局部出现
- 不引入第二种"主题色"。蓝紫粉等仅作壁纸氛围，HUD 不响应

---

## 3. 字体与排版

**字体栈**
```
"Bahnschrift", "Eurostile Extended", "Consolas", "Trebuchet MS", monospace
```
Windows 10/11 自带 Bahnschrift，无需打包字体文件。

**排版规则**
- 所有数字必须 `font-variant-numeric: tabular-nums`（等宽）
- Header / column-head / label：全大写 + 大字距（3–4px）
- 数据值：紧字距（1–1.5px）
- 字号梯度：8 (label) / 9 (rate) / 10 (row val) / 11 (track) / 12 (date) / 14 (current month) / 92 (clock digits)

---

## 4. 视觉语法

### 4.1 边框系统
- **Corner brackets `[ ]`**：4 个 L 形角点，仅出现在交互组件 (Search rows, Music, System frame)。线宽 1px，10–12px 边长
- **Horizontal spine line**：贯穿屏幕中线的 cyan 渐变细线 (`linear-gradient(90deg, transparent 0%, var(--cyan-edge) 6%, var(--cyan-edge) 94%, transparent 100%)`)，两端各一个 7px 菱形端点
- **Diamond endpoint markers `◇`**：1px 边线 + 半透明深色填充 + cyan glow，用作 Clock 两侧装饰、spine 端点、Music 进度条 pin

### 4.2 状态符号
- **月相点** (PWR 列)：1px cyan 圆环，按使用率从空 (`q0`) → 半填 (`q1`) → 全填 (`q2`)
- **状态点** (STA 列)：纯 cyan 7px 圆 (正常) / red (warn) / 空心边框 (off)
- **DESTROYED 戳**：Impact / Arial Black 黑体，14px，倾斜 -2°，红色 + 红 glow，覆盖在异常 row 上
- **Scan stripe**：组件顶部 2px 高，cyan→透明渐变，Music / Clock / login 类组件出现

### 4.3 动画
- Clock 冒号 `:` 闪烁，1.6s `steps(2)`
- Search caret `▮` 闪烁，1.1s `steps(2)`
- Hover 过渡 0.15s `ease`
- Music 进度条连续填充 (Rainmeter 通过 ActionTimer/Update 驱动)
- **不引入** 复杂粒子 / 旋转 / 缩放循环

---

## 5. 整体布局

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌──────────────┐    ┌────────────────────┐    ┌────────────┐   │
│  │ S-1 SYSTEM   │    │ G GOOGLE  ▶  [  ] │    │ CHRONOS    │   │
│  │ ROSTER       │    │ B BING    ▶  [  ] │    │ MARCH  03  │   │
│  │ 001 CPU 62   │    └────────────────────┘    │ APRIL  30  │   │
│  │ 002 MEM 41   │                              │ MAY    05  │   │
│  │ 003 DSK 78   │                              └────────────┘   │
│  │ 004 NET XX D │                                               │
│  │ 005 NET UP 3 │                                               │
│  └──────────────┘                                               │
│                                                                 │
│                                                                 │
│         ◇──────────  1 3 : 4 2 : 0 8  ──────────◇   ← spine    │
│                       THU — 30 · APR · 2026                     │
│                       / T-001 ────────                          │
│                                                                 │
│                                                                 │
│              ┌──────── ▶ NOW PLAYING ────────┐                  │
│              │  86 ED「Avid」  01:24/03:47  │                  │
│              └────────────────────────────────┘                 │
│                                                                 │
│      [SVG] [SVG] [SVG] [SVG] [SVG]                              │
│       DEV   DOC  GAME  MEDIA  BIN                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 区域 | 组件 | 锚点 |
|---|---|---|
| TOP-LEFT | System Roster | top:22, left:24 |
| TOP-CENTER | Search · Google + Bing | top:22, x:50% center |
| TOP-RIGHT | Calendar | top:22, right:24 |
| CENTER | Clock (主视觉) | x/y:50% center |
| BOTTOM-CENTER | Music Player | bottom:130, x:50% center |
| BOTTOM | Folder Dock | bottom:22, x:50% center |
| MID | Horizontal spine line | y:50%, left:4%, right:4% |

---

## 6. 组件规格

### 6.1 Clock · 中央主视觉

**字段**
- 数字：`HH:MM:SS` 24h，92px Bahnschrift Light，letter-spacing 12px
- 副信息：`THU — 30 · APR · 2026`，12px，cyan-edge，居中
- 编号：`/ T-001 ────`，8px + 240px 渐变 scan，居中

**装饰**
- 左右各 14px 菱形端点 (`◇`)，垂直居中

**交互**
- 单击：打开 Windows 时钟应用
- 右击：打开 Rainmeter 配置菜单 (默认)

**Rainmeter measure**
```ini
[mTime]   Measure=Time   Format=%H:%M:%S
[mDate]   Measure=Time   Format=%d · %b · %Y
[mDay]    Measure=Time   Format=%a   StringCase=Upper
[mTNum]   Measure=Time   Format=%j   ; day-of-year for T-001 编号
```

### 6.2 System Roster · 左上

**结构** 6 列 × 5 行：
| 列 | 含义 | Rainmeter 数据源 |
|---|---|---|
| NO | 编号 (001-005) | 固定 |
| PERS | 指标名称 | 固定 |
| PWR | 月相 (用量比例) | 由 VAL 推导 |
| VAL | 当前值 | CPU / RAM / FreeDiskSpace / NetIn / NetOut |
| RATE | 趋势 (▲▼/--) | 用 ChangeAction + 内存上一次值差分 |
| ● | 状态点 | 阈值判定：< 80 cyan，>= 80 warn，0 off |

**5 行映射**
- 001 CPU LOAD ← `Measure=CPU Processor=0`
- 002 MEM USE ← `Measure=PhysicalMemory`
- 003 DSK C:\ ← `Measure=FreeDiskSpace Drive=C: InvertMeasure=1`
- 004 NET DOWN ← `Measure=NetIn` (`DESTROYED` 戳 = 速度 < 1KB/s 持续 > 30s)
- 005 NET UP ← `Measure=NetOut`

**头部**：`/ S-1 · SYSTEM ROSTER          ▼ ONLINE`
**框架**：4 角 corner brackets

**交互**
- Header 单击：打开任务管理器 (`taskmgr.exe`)
- 003 DSK row 单击：打开 `C:\`

### 6.3 Calendar · 右上

**结构**：3 行月份 stack
- 上月 (灰)：`MARCH  | 03`
- 当月 (高亮 + 加大)：`APRIL  | 30` (数字是当前日，月名加大字号到 14px)
- 下月 (灰)：`MAY    | 05`

**头部**：`/ CHRONOS · WK-18`
**底部**：`D-120 / 365  ▼ TODAY`

**Rainmeter measure**
```ini
[mWeek]  Measure=Time Format=%V    ; ISO week
[mDoY]   Measure=Time Format=%j    ; day of year
[mMonth] Measure=Time Format=%B
[mDay]   Measure=Time Format=%d
; 上下月通过 Lua 或 ActionTimer 计算
```

### 6.4 Search · Google + Bing · 顶部居中

**两行独立组件**：用户可以单独启用任一引擎

每行结构：`[corner]  [G glyph]  GOOGLE  ▶  search query placeholder ▮  [DISPATCH ⏎]`

- **glyph**：22×22 单字母方框 (G / B)，1px cyan border
- **engine name**：9px / 字距 3px
- **input**：InputText 插件，下划线 1px cyan，placeholder 灰色，caret cyan blink
- **DISPATCH 按钮**：3×7px padding 文字框，1px cyan border，字距 3px

**dispatch 行为**
- Google：`https://www.google.com/search?q=$UserInput$`
- Bing：`https://www.bing.com/search?q=$UserInput$`
- Enter 键 / 单击 DISPATCH 都触发

### 6.5 Music Player · 底部居中

**结构** 三栏 grid：
1. 左：track 信息块
   - 头部：`▶ NOW PLAYING ··· NETEASE / QQ MUSIC`
   - 主标：歌曲名 11px / 1px 字距
   - 副标：艺术家 9px / 弱化
2. 中：进度条
   - `00:48 ─────●─────── 04:12`
   - 菱形 pin 标当前位置
3. 右：3 个控件 `⏮ ⏵ ⏭`，hover 高亮

**装饰**：4 角 corner brackets + 顶部 cyan→透明 scan stripe

**音乐源接入策略**

Rainmeter 自带的 `Plugin=NowPlaying` 仅原生支持 Spotify / WMP / iTunes / foobar2000 / AIMP / WinAMP 等少数 player（[官方 PlayerType 列表](https://docs.rainmeter.net/manual/plugins/nowplaying/)）。**网易云音乐 / QQ 音乐没有原生 PlayerType。** 桥接方案：

- **方案 A · 推荐**：使用第三方 Rainmeter 插件 [`WebNowPlaying-Redux`](https://github.com/keifufu/WebNowPlaying-Redux)
  - 安装其 Rainmeter 端 `.rmskin` + 浏览器扩展（支持网页版网易云 / QQ 音乐 / Spotify / YouTube Music）
  - 桌面端 QQ 音乐 / 网易云：通过 [WNP-Redux 的 SMTC adapter](https://github.com/keifufu/WebNowPlaying-Redux-SMTC) 桥接 Windows 系统媒体传输控件
  - skin 中改用 `[mPlayer] Measure=Plugin Plugin=WebNowPlaying`
- **方案 B · 退化**：v1 默认配置成 `PlayerType=Spotify`（开箱即用）；用户切换至 QQ/网易云需自行装方案 A
- **方案 C · 最简**：仅显示当前焦点窗口标题（用 `Plugin=Process` + 窗口标题嗅探），无元数据 / 进度

`@Resources/Variables.inc` 中通过 `MusicSource=Spotify | WNP | TitleSniff` 切换三套测量配置。v1 默认 `WNP`，并在 `@Resources/docs/install.md`（v1 实现期补写）说明第三方插件安装步骤。

**交互**
- 单击主标：聚焦音乐应用窗口
- 左/右箭头：上一首 / 下一首 (`!CommandMeasure mPlayer "Previous"`)
- 中间：播放/暂停切换

### 6.6 Folder Dock · 5 个 Spearhead 个人 mark 启动器

**结构** 水平 5 项，无背景，`gap: 22px`：

每项 = SVG 个人 mark (52×52 cyan stroke) + label (8px 大写 cyan) + codename (7px 灰)

**5 个 Spearhead 个人 mark 映射**

| 启动器 | 角色 | 代号 | 设计要点 |
|---|---|---|---|
| DEV | Shin (辛) | UNDERTAKER 送葬人 | 骷髅 + 铲子 (你提供的参考图) |
| DOC | Raiden (莱登) | BLACK DOG 黑犬 | 狼头侧面 + 利齿 |
| GAME | Theo (西奥) | LAUGHING FOX 笑狐 | 露齿狐脸 (Theo 是队内画师，画了所有人的 mark) |
| MEDIA | Kurena (库蕾娜) | GUN SNAKE 银蛇 | 蛇盘绕 + 步枪 |
| BIN | Anju (杏祖) | SNOW WITCH 雪魔女 | 巫师帽 + 骷髅 (red 警示色) |

**Hover 反馈**：
- 整个 launcher 上移 3px
- mark 颜色从 `--cyan-edge` → `--text`，drop-shadow glow 加强
- 4 角 [ ] tick 浮现

**配置入口**：
每个 launcher 的目标路径在 `@Resources/Variables.inc` 中以变量定义：
```ini
[Variables]
DockDevPath=C:\Users\<user>\source
DockDocPath=C:\Users\<user>\Documents
DockGamePath=C:\Program Files\Steam
DockMediaPath=C:\Users\<user>\Videos
DockBinPath=::{645FF040-5081-101B-9F08-00AA002F954E}   ; 回收站 CLSID
```

**素材依赖**
v1 实现使用 Shape meter 复刻 5 个 mark 的简化版作为 placeholder。后续替换为精修矢量素材时，仅需更新对应 Shape meter 的路径或换为 Image meter + PNG。

---

## 7. Rainmeter 实现策略

### 7.1 文件组织

```
EightSix86/
├── @Resources/
│   ├── Variables.inc        # 全局色彩 / 字体 / dock 路径变量
│   ├── docs/
│   │   └── v1-design.md     # ← 本文件
│   ├── origin/              # 风格参考截图（不入皮肤逻辑）
│   ├── marks/               # SVG/PNG 个人 mark 素材（v1 用 Shape，v2 起可换 PNG）
│   │   ├── undertaker.png
│   │   ├── blackdog.png
│   │   ├── fox.png
│   │   ├── snake.png
│   │   └── witch.png
│   └── fonts/               # 可选 (Bahnschrift 已系统自带，预留)
├── Clock/Clock.ini          # 重写
├── System/System.ini        # 重写为 6 列 Roster
├── Calendar/Calendar.ini    # 新建
├── SearchGoogle/SearchGoogle.ini  # 在原 Google.ini 基础上重写
├── SearchBing/SearchBing.ini      # 新建（镜像 Google + 替 URL）
├── Music/Music.ini          # 新建
├── Dock/Dock.ini            # 新建（5 launcher 用 Group）
└── (旧组件保留以兼容，不在 v1 启用：Disk, Network, Recycle Bin, Google)
```

> 旧组件 (`Disk/`, `Network/`, `Recycle Bin/`, `Google/`) 在 v1 中**保留但不启用**，避免破坏现有用户配置；它们的功能被 System Roster + SearchGoogle + Dock 接管。

### 7.2 共享变量 `@Resources/Variables.inc`

```ini
[Variables]
; ===== 调色板 =====
ColorCyan=126,229,245,255
ColorCyanEdge=126,229,245,242
ColorCyanDim=126,229,245,115
ColorCyanDeep=126,229,245,46
ColorRed=255,82,82,255
ColorRedDim=255,82,82,217
ColorText=245,251,255,255
ColorTextDim=245,251,255,179
ColorShadow=0,8,18,242

; ===== 字体 =====
FontFace=Bahnschrift
FontFaceLight=Bahnschrift Light
FontMono=Consolas

; ===== Dock 启动路径 =====
DockDevPath=C:\Users\<user>\source
DockDocPath=C:\Users\<user>\Documents
DockGamePath=C:\Program Files (x86)\Steam
DockMediaPath=C:\Users\<user>\Videos
DockBinPath=::{645FF040-5081-101B-9F08-00AA002F954E}

; ===== 音乐源切换 =====
; 取值: WNP (WebNowPlaying-Redux) | Spotify | TitleSniff
MusicSource=WNP
```

每个 .ini 顶部用 `@include #@#Variables.inc` 复用。

### 7.3 矢量绘制：Shape Meter

Rainmeter Shape meter 支持 SVG-like 路径，能直接复刻 corner bracket / diamond endpoint / 月相点 / 星形 / 个人 mark 的简化版。

示例（corner bracket）：
```ini
[CornerTL]
Meter=Shape
Shape=Path tl | LineTo 12,0 | StrokeWidth 1 | Stroke Color #ColorCyanEdge#
Shape2=Path tl2 | LineTo 0,12 | StrokeWidth 1 | Stroke Color #ColorCyanEdge#
tl=0,0
tl2=0,0
X=0
Y=0
```

5 个个人 mark 在 v1 用 Shape 多 path 组合实现（参考 `hud-style-v7.html` 中的 SVG `<symbol>` 节点路径），保留 SVG 等效坐标，便于后续换为 Image meter + PNG。

### 7.4 输入 (InputText 插件)

Search 组件用 `Plugin=InputText`：
```ini
[mInputG]
Measure=Plugin
Plugin=InputText
SolidColor=0,0,0,1
StringStyle=Bold
FontFace=#FontFace#
FontSize=10
FontColor=#ColorText#
DefaultValue=""
FocusDismiss=1
Command1=["https://www.google.com/search?q=$UserInput$"]
```

### 7.5 NowPlaying

```ini
; v1 默认配置（WNP-Redux 模式）
[mPlayerStatus]
Measure=Plugin
Plugin=WebNowPlaying
PlayerType=Status

[mPlayerTitle]
Measure=Plugin
Plugin=WebNowPlaying
PlayerType=Title

[mPlayerArtist]
Measure=Plugin
Plugin=WebNowPlaying
PlayerType=Artist

[mPlayerProgress]
Measure=Plugin
Plugin=WebNowPlaying
PlayerType=Progress       ; 0-100
```

进度直接喂给 Bar 或 Shape 的宽度。Spotify 备用配置见 `Music/Music.ini` 注释。

---

## 8. 后续素材依赖

v1 范围内 **不依赖** 任何外部素材交付。所有视觉用 Shape meter 复刻可达成。

后续 v1.x / v2 替换路径：
- **Spearhead 5 个个人 mark 矢量精修版** (PNG / 直接替换 Shape)
- **Bahnschrift 替代字体** (如用户偏好其他几何无衬线，提供 .ttf 放 `@Resources/fonts/`)
- **Stride / Squadron 旅徽章** (Spearhead 旅徽，可作 Calendar / 月份装饰)

---

## 9. 路线图

### v1 范围（本文档）
- [x] Clock 中央主视觉
- [x] System Roster 6 列 5 行
- [x] Calendar 三月份 stack
- [x] SearchGoogle 长条
- [x] SearchBing 长条
- [x] Music NowPlaying（SMTC 默认源）
- [x] Dock 5 launcher（Shape 占位 mark）
- [x] @Resources/Variables.inc 全局变量

### v2 候选（不在本文档承诺）
- 左侧 vertical SCANNING / SYNC ticker
- Alert 浮窗（独立组件，DESTROYED 戳样式弹窗）
- 多套个人 mark 切换（用户选择把哪个角色的 mark 分给哪个 launcher）
- Wallpaper Engine 联动（壁纸切换时 HUD 微调对比度）
- Bilibili / 本地 .lrc 歌词 ticker

---

## 附录 A · 视觉来源溯源

每个核心元素都映射回一张 `@Resources/origin/` 截图：

| 元素 | 来源截图 |
|---|---|
| 编号前缀 001/002/003 + 月相点 | `system_status_1.png`, `system_status_2.png` |
| DESTROYED 红戳 | `system_status_2.png` |
| Cyan scan stripe（Music 顶部） | `main_desk.png` 控制台头部高光条 |
| Corner brackets 角括号 | `main_desk.png` 半透明面板边角 |
| 菱形端点 / 进度 pin | `battle_field.png` 标记 pin |
| Tabular 数字 + Eurostile 几何感 | 全部截图通用 UI |
| 笑狐 / 骷髅等个人 mark | 漫画 / 你提供的 Undertaker 参考图 |

## 附录 B · 设计稿渲染参考

完整的 v7 浏览器渲染版本保存在：
`/.superpowers/brainstorm/<session>/content/hud-style-v7.html`

可在浏览器直接打开预览所有组件叠加在两种壁纸场景的效果。
