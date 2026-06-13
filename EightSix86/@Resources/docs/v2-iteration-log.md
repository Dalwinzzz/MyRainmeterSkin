# 86 HUD — v2 迭代日志

> v1 设计稿见 `v1-design.md`。本文件按迭代轮次增量记录 v1.x → v2 的演进。
> 当前配色已从 v1 的纯 cyan 切换到「红彼岸花 #C81E3A × 钴蓝 #1E5AC8」（见 `Variables.inc`）。

---

## 迭代 1 · System Roster 数据驱动化（v1.2.0）

**动机**：对照 `origin/system_status_1.png` 参考图，v1.1 的 System Roster 虽然布局到位，但
PWR 月相 / RATE 趋势 / STA 状态点全是写死的静态字符 —— 它「长得像」战术名册，却
不「活」。86 参考图的灵魂正是这张表会随战况实时跳动（`041↑` 红色趋势、半填月相、
横贯整行的 `DESTROYED` 红戳）。本轮把它从展示板升级为真正反映系统状态的活体 HUD。

呼应 `frontend.md`：
- 第 3 节「signature moment 要真」→ 让数据真正驱动符号，而非装饰。
- 第 5 节「一次高质量进场编排 > 到处撒微交互」→ 开机一道扫描线，而非满屏循环动画。

### 新增 / 改动

| 文件 | 改动 |
|---|---|
| `@Resources/Scripts/Roster.lua` | **新增**。统一数据驱动逻辑，每秒 Update 一次 |
| `System/System.ini` | 接入 Lua；STA 改 String meter；加 5 个 DESTROYED 戳；加扫描线 + ActionTimer 进场 |

### 数据驱动规则（Roster.lua）

1. **PWR 月相**（5 档）：`○ ◔ ◑ ◕ ●`，按 `floor(pct/20)+1` 映射使用率。
   网络行用 1MB/s 软上限把字节速率折算成 0–100。
2. **RATE 趋势**：与上一次 Update 的值做差分。
   - 上升 → `▲`（蓝）；下降 → `▼`（暗蓝）；持平 → `──`（灰）。
   - 数据行死区 1%，网络行死区 1KB，避免微抖动刷屏。
3. **STA 状态色 + 阈值告警**：
   - CPU/MEM ≥ 90%、DSK ≥ 85% → STA 点 + 月相变红。
4. **DESTROYED 红戳**（signature）：
   - 网络行连续 30 次 Update（≈30s）流量 < 64B/s 判定断流。
   - 整行盖 Impact 体倾斜红戳 `D E S T R O Y E D`，原 VAL 隐藏。
   - 只在状态**切换**时发 Show/Hide bang（`wasDestroyed` 记忆位），避免每秒覆盖进场动画。

### 进场编排（ActionTimer · mIntro）

- 皮肤刷新时 `OnRefreshAction` 先 `!HideMeterGroup roster`，把整张名册藏起。
- 一道 cyan 渐变扫描线（`mtrScanLine`，Y 绑定 `#ScanY#`）18 步 × 8px 自 y=36 扫到底。
- 扫到底后 `!ShowMeterGroup roster` —— 整张名册「一次性上线」，配合扫描线消失。
- DESTROYED 戳归入独立 `stamps` 组，不受 `!ShowMeterGroup roster` 影响，仅由 Lua 控制。

### 验证

macOS 无法运行 Rainmeter，故用 `luac -p`（语法）+ mock SKIN 跑真实 `lua` 解释器（逻辑）双重校验：
- ✅ Lua 语法通过 `luac -p`
- ✅ CPU 15%→`○`蓝 / 95%→`●`红；网络断流 35 次→DESTROYED 触发；CPU 20→60→`▲`
- ✅ ini 结构：75 section 无重复，roster 组 30 成员、stamps 组 5 成员，ScanY 引用闭环

### Windows 端待人工确认

- [ ] Impact 字体在 DESTROYED 戳上的实际字距（macOS 无法预览，可能需调 FontSize/间距）
- [ ] ActionTimer 扫描线速度手感（18ms/步，可能偏快或偏慢）
- [ ] `Segoe UI Symbol` 下 5 档月相字符是否都有字形（◔◕ 在部分字体缺失，缺则回退 ◐）

---

## 迭代 2 · Clock 中央主视觉进场 + 呼吸（v1.2.0）

**动机**：Clock 是整个 HUD 的 signature moment（v1 设计稿明确定义为「中央主视觉」），但实现一直
是完全静态的——数字直接出现、冒号不闪、没有任何进场。`frontend.md` 第 4 节把 Clock 列为「克制
科技 / 奢侈极简」脸的核心记忆点，第 5 节强调「一次高质量进场编排 > 到处撒微交互」。本轮给中央
时钟做最精致的「揭示」。

### 改动（`Clock/Clock.ini`）

| 能力 | 实现 |
|---|---|
| 三段式进场 | `mIntro` ActionTimer：ChromeUp(菱形+扫描线 alpha↑) → DigitUp(数字 alpha↑) → MetaUp(日期+编号 alpha↑) |
| 冒号正弦呼吸 | `mBreathTick`(0..31 自增计数) + `mBreath`(Sin 公式 → BreathAlpha 76..255) 喂 InlineSetting |
| alpha 分层 | DigitAlpha / ChromeAlpha / MetaAlpha / BreathAlpha 四个独立变量，编排可精确分层 |

**关键技术点**：skin 基准 `Update=125`（8× 时钟速度）驱动平滑呼吸；时间/日期 measure 用
`DefaultUpdateDivider=8` 回到每秒刷新；呼吸 measure 显式 `UpdateDivider=1` 走 125ms。
ActionTimer 在独立线程跑自己的 Wait，不受 base tick 影响。

### 验证

- ✅ ini 结构：19 section 无重复，4 个动画变量都在 `[Variables]` 初始化，Formula/Action 括号配对
- ✅ 呼吸正弦数学（Python）：alpha 76..255 不越界，相邻 125ms 帧最大跳变仅 17/255（丝滑），4s 对称周期
- 附 `preview/iter2-clock.html` 浏览器预览（含真实走时 + 进场重播）

### Windows 端待人工确认

- [ ] 96px Bahnschrift Light 大数字实际渲染重量
- [ ] 冒号呼吸手感（4s 周期是否过慢/过快，可调 mBreathTick 模数）
- [ ] base tick 125ms 对 CPU 的占用（中央时钟常驻，若偏高可放宽到 200ms / 16 步）

---

## 迭代 3 · Music Player 进度跟随 + 微交互（v1.2.0）

**动机**：Music 组件布局完整，但有个真实硬伤——进度菱形 pin 死死钉在最右端 X=326 不动
（`mtrProgressBar` Bar 会填充，但 pin 不跟随），视觉上「进度条在走、pin 不动」很穿帮。
另外 v1 设计承诺的「控件 hover 高亮」「播放/暂停图标切换」都没实现。
本轮补齐这些「signature moment 要真」的细节（`frontend.md` 第 3 节）。

### 改动（`Music/Music.ini`）

| 能力 | 实现 |
|---|---|
| 进度 pin 跟随（修复） | 新增 `mPinX` Calc = `18 + progress/100×304`，pin `X=([mPinX]-3)` 绑定 |
| 播放/暂停图标 | 新增 `mPlayGlyph` Calc，`IfCondition(state=1)` 切 `⏸`/`⏵` |
| 控件 hover 微交互 | 三个 hit-area 加 `MouseOver/LeaveAction`，`!SetOption Shape` 改 box 描边+填充、icon 变色 |
| Play 焦点反馈 | Play 按钮 hover 用 `ColorRedLight` 加深红填充（焦点强调） |

### 验证

- ✅ ini 结构：41 section 无重复，引用的 10 个颜色变量全在 Variables.inc 定义
- ✅ pin 映射（Python）：0%→X18、100%→X322，与进度条左右端（18 / 18+304）精确对齐，中心偏差 0.5px
- ✅ 三按钮 hover action / IfCondition 图标切换 方括号引号配对正确
- 附 `preview/iter3-music.html`（进度真实走 + pin 跟随 + hover + 播放切换）

### Windows 端待人工确认

- [ ] WebNowPlaying 插件 + SMTC adapter 已装（否则无数据，pin 停在 0）
- [ ] `Segoe UI Symbol` 的 ⏸⏵⏮⏭ 字形（缺则改用 `Segoe MDL2 Assets` 的 E768/E769）
- [ ] hover 反馈手感（box 填充 alpha 90/130 是否过强）

---

## 迭代 4 · Dock 个人 mark hover 反馈（v1.1.0）

**动机**：Dock 的 5 个 Spearhead 个人 mark（Shape 绘制的送葬人/黑犬/笑狐/银蛇/雪魔女）视觉个性
很强，但 v1 设计 6.6 节明确承诺的 **hover 反馈**（上移 3px / mark 变亮 / 角括号 tick 浮现）一直没
实现，悬停毫无反馈。`frontend.md` 第 8 节「作品集/创意站」：个人徽记正是可以放飞、给足交互的地方。
本轮兑现这个承诺。

### 改动（`Dock/Dock.ini`）

| 能力 | 实现 |
|---|---|
| mark 描边变量化 | 每个 mark 的所有 `Stroke/Fill Color` 抽成局部变量 `#L*Mk#`（默认蓝边 / BIN 暗红） |
| hover 上移 | mark Y 用 `#L*Ty#`，MouseOver 4→1（−3px lift），MouseLeave 还原 |
| 角括号 tick | 新增 5 个 `mtrL*Tick`（60×60 四角），alpha `#L*Tk#` hover 0→255 浮现 |
| hover 变色 | MouseOver mark → `ColorText`（纯白），BIN → `ColorRedLight`（亮红）；MouseLeave 还原 |
| 编组重绘 | 每 launcher 的 mark+tick+label+code 归入 `g1..g5`，hover 一次 `!UpdateMeterGroup` |

### 验证

- ✅ ini 结构：28 section 无重复，5 mark 全变量化（0 处残留旧硬编码色），各有 tick + 3 成员组
- ✅ 15 个 hover state 变量（L1-5 × Mk/Ty/Tk）全在 `[Variables]` 初始化
- ✅ 10 个 MouseOver/Leave action 方括号引号配对正确，引用颜色变量全已定义
- 附 `preview/iter4-dock.html`（5 mark SVG + 真实 hover 上移/变白/tick 浮现）

### Windows 端待人工确认

- [ ] hover 上移 3px 手感（Rainmeter Shape 整体 Y 偏移是否顺滑，无过渡是瞬变）
- [ ] mark 描边变纯白的对比度（深色壁纸 OK，浅色壁纸可能过曝）
- [ ] tick 60×60 框与各 mark 实际对齐（mark 绘制坐标略有差异）

---

## 迭代 5 · Calendar 日期修复 + 年度进度条（v1.2.0）

**动机**：审查 Calendar 时发现一个**真实 bug**——上下月用 `now ± 2592000`（固定 30 天秒数）
计算，在 31 天月份和月初/月末会跨月错乱。7 个边界日期测试错 5 个（如 3月31日 −30天 = 3月1日，
仍显示 3 月而非 2 月）。这是会被用户直接看到的显示错误。本轮修复并补一条年度进度条。

### 改动（`Calendar/Calendar.ini`）

| 改动 | 实现 |
|---|---|
| **日期 bug 修复** | 新增 `mAnchorTS` Calc = `now − (day−15)×86400`（当月15号正午），4 个上下月 measure 改用 `[mAnchorTS]±2592000` |
| 年度进度条 | 新增 `mYearFill` = `213 × doy/365`，底部 track(淡蓝) + fill(红) + 焦点菱形 pin |

**为什么 15 号基准有效**：从月中（15号）跨 ±30 天，无论当月几天，都必然落入相邻月，
绝不会因 31 天月份多出的那天而停在本月。

### 验证

- ✅ ini 结构：39 section 无重复，4 上下月全用 mAnchorTS，0 处 mNowTS±2592000 残留
- ✅ **日期修复（Python 全边界）**：旧算法 7 测试错 5；新算法 7/7 全对（含 1/31、3/31、7/1、12/31）
- ✅ 年度进度映射：D-1→1px、D-365→213px 与轨两端对齐；今天 D-165→45.2%
- ✅ 今日（2026-06-14）实显：上月 MAY 05 / 当月 JUN 14红 / 下月 JUL 07，全对
- 附 `preview/iter5-calendar.html`（含修复前后对比表 + 实时年度进度条）

### Windows 端待人工确认

- [ ] 年度进度条在 155px 画布底部不被裁切（Y=146 + 2px，pin Y=143）
- [ ] `TimeStamp` measure 配 Calc `[mAnchorTS]` 在 Rainmeter 实际能正确解析（DynamicVariables 已开）

---

## 迭代 6 · Search 双引擎 hover + 整合交付（v1.2.0 · 最后一轮）

**动机**：Search 是唯一还没做 hover 的核心交互组件——Music（轮3）、Dock（轮4）都有了，
Search 的输入框 / dispatch 按钮悬停却毫无反馈，是套件内的交互一致性缺口。同时这是 6 轮里
的最后一轮，需要把整套主题**整合成可交付状态**（`frontend.md` 执行流程第 7 步「交付」）。

### 改动

| 文件 | 改动 |
|---|---|
| `SearchGoogle/SearchGoogle.ini` | 输入框 hit-area + dispatch hit-area 加 `MouseOver/LeaveAction` hover |
| `SearchBing/SearchBing.ini` | 镜像同步同样的 hover（两文件交互一致） |
| `@Resources/docs/install.md` | **新增** 完整安装指南（Rainmeter / 组件加载 / WNP 音乐源 / 字体 / 路径配置 / 排错） |
| `README.md` | 重写：整套组件总览 + 快速开始 + 预览稿索引 + 设计哲学 |

**hover 设计**：输入框 hover → 边框 + 下划线 蓝边变亮蓝、填充加深（提示字段激活）；
dispatch（焦点红按钮）hover → 红填充加深 + 描边亮红。与 Music/Dock 的 hover 语言统一。

### 验证

- ✅ 两 Search 文件各 23 section 无重复，各 2 对 MouseOver/Leave，action 方括号引号配对正确
- ✅ 引用颜色变量全在 Variables.inc 定义
- 附 `preview/iter6-search.html`（Google + Bing 双条，真实 hover）

---

## 6 轮迭代总结

| 轮 | 组件 | 核心 | commit |
|---|---|---|---|
| 1 | System Roster | 数据驱动月相/趋势/状态 + DESTROYED 戳 + 扫描进场 | 874e876 |
| 2 | Clock | 三段进场编排 + 冒号正弦呼吸 | 695fdc4 |
| 3 | Music | 进度 pin 跟随 + 状态图标 + 控件 hover | 2ffda0f |
| 4 | Dock | 5 个人 mark hover（上移+变亮+角括号） | 7b66f46 |
| 5 | Calendar | 修复上下月跨月 bug + 年度进度条 | 833a031 |
| 6 | Search + 交付 | 双引擎 hover + install.md + README | （本轮） |

**整套主题现状**：6 个核心组件交互风格统一（数据驱动 + 进场编排 + hover 微交互），
配色统一「红彼岸花 × 钴蓝」，全部经 macOS 端静态校验（ini 结构 / Lua luac+mock / 数学 Python）。
Windows 端首次安装预览的待确认项已分散记录在各轮「Windows 端待人工确认」小节。

**验证方法论**（macOS 无法跑 Rainmeter）：每轮用 `luac -p` + mock SKIN 跑真实 lua、
Python 验证数学映射与边界、Python 校验 ini 结构与变量闭环，并产出浏览器预览稿供人工验收。
