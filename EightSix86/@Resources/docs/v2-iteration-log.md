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
