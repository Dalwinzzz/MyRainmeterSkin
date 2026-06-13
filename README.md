# 86 HUD — 「不存在的战区」Rainmeter 主题

> 基于动画《86 -エイティシックス-》视觉语言的桌面 HUD 皮肤组件库。
> 一套**透明叠加**的战术 HUD，可直接覆盖在任意 86 壁纸 / Wallpaper Engine 动态壁纸之上。

配色取自「彼岸花鲜红 `#C81E3A` × 共和国钴蓝 `#1E5AC8`」：
**蓝是 HUD 结构 / 分隔线，红是焦点 / 告警 / 当下**，中性白承载数据值。

## 组件

| 组件 | 位置 | 说明 |
|---|---|---|
| **Clock** 中央时钟 | 屏幕正中 | 主视觉。三段进场揭示 + 冒号正弦呼吸 + 中文日期 |
| **System Roster** 系统名册 | 左上 | 战术名册式监控：月相/趋势/状态全数据驱动，断网盖 DESTROYED 红戳 |
| **Calendar** Chronos | 右上 | 三月份 stack + 当日红高亮 + 年度进度条 |
| **Search** 双引擎 | 顶部居中 | Google / Bing 快搜，输入框 + dispatch hover 高亮 |
| **Music** 播放器 | 底部居中 | NowPlaying，进度 pin 跟随 + 状态图标 + 控件 hover |
| **Dock** 启动器 | 底部 | 5 个 Spearhead 个人 mark（送葬人/黑犬/笑狐/银蛇/雪魔女），hover 上移+变亮 |

## 快速开始

把 `EightSix86/` 拷到 `文档\Rainmeter\Skins\`，Refresh All，逐个 Load 组件即可。
完整步骤（含音乐源插件、字体、路径配置、排错）见
**[安装指南](EightSix86/@Resources/docs/install.md)**。

## 预览

macOS 无法运行 Rainmeter，每个组件配了**浏览器预览稿**（双击打开看动效）：

- [`iter1-roster.html`](EightSix86/@Resources/docs/preview/iter1-roster.html) — System 数据驱动 + DESTROYED
- [`iter2-clock.html`](EightSix86/@Resources/docs/preview/iter2-clock.html) — Clock 进场 + 冒号呼吸
- [`iter3-music.html`](EightSix86/@Resources/docs/preview/iter3-music.html) — Music 进度跟随 + 微交互
- [`iter4-dock.html`](EightSix86/@Resources/docs/preview/iter4-dock.html) — Dock 个人 mark hover
- [`iter5-calendar.html`](EightSix86/@Resources/docs/preview/iter5-calendar.html) — Calendar 修复 + 年度进度

## 设计文档

- [v1 设计定稿](EightSix86/@Resources/docs/v1-design.md) — 设计哲学、调色板、视觉语法、组件规格
- [v2 迭代日志](EightSix86/@Resources/docs/v2-iteration-log.md) — 逐轮迭代记录与验证

## 设计哲学

**Wallpaper 是主体，HUD 是参谋。** 所有组件无背景填充，仅以线条 / 文字 / glow 构造可读性。
不喧宾夺主，颜色、构图、动画都为壁纸让位。每个组件只保留一个记忆点，其余克制、留白。
视觉语言严格对齐动画截图：编号前缀、月相状态点、DESTROYED 红戳、scan stripe、菱形端点。

## License

MIT
