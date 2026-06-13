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
