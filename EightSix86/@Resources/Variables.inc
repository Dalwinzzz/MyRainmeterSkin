; ============================================================
;  86 HUD · Shared Variables  (v5 — 左侧指挥栏 + 主视觉留白)
;  Included by every skin via:
;    [Rainmeter]
;    @include=#@#Variables.inc
;
;  v5 配色翻转: 旧版红蓝赛博朋克 → 86 真·冷蓝银白军用数据台。
;  规则: 冰蓝/钢蓝/银白 统治画面;
;        猩红 = 仅 CRITICAL / 今日 / 当前歌词 / hover 时刺出, 绝不平分。
;  对应 v5 预览: @Resources/docs/preview/v5/index.html
; ============================================================

[Variables]

; ===== v5 5 色板 (RGBA, 0-255) =====
; ice     #dbe9fb  冰蓝白 — 主文字 / 雷娜银白
; steel   #6fa8e0  钢蓝   — 主色 / 编号 / 线条 / 强调蓝
; steel-d #3f6fa0  深钢蓝 — 渐变深端 / 次强调
; mist    #8da6c4  雾蓝灰 — 次要文字 / 单位
; crimson #ff3b3b  猩红   — 唯一暖强调
; gold    #e8b94a  徽章金 — 极少量点缀

; --- Ice / 银白文字 ---
ColorIce=219,233,251,255
ColorIceDim=219,233,251,150
ColorIceFaint=219,233,251,80
ColorWhite=255,255,255,255

; --- Steel / 钢蓝 ---
ColorSteel=111,168,224,255
ColorSteelEdge=111,168,224,235
ColorSteelDim=111,168,224,150
ColorSteelDeep=111,168,224,46
ColorSteelDark=63,111,160,255
ColorSteelD=63,111,160,255

; --- Mist / 雾蓝灰 ---
ColorMist=141,166,196,255
ColorMistDim=141,166,196,170

; --- Crimson / 猩红 (唯一暖强调) ---
ColorRed=255,59,59,255
ColorRedEdge=255,59,59,235
ColorRedDim=255,59,59,150
ColorRedDeep=255,59,59,46
ColorRedGlow=255,90,80,140

; --- Gold / 徽章金 ---
ColorGold=232,185,74,255

; --- 结构 / 线条 / 玻璃底 ---
ColorLine=141,166,196,40          ; 分隔线 (mist 低 alpha)
ColorLine2=141,166,196,80
ColorGlow=120,180,240,150
ColorShadow=0,5,16,235

; --- 指挥栏毛玻璃底 (可调透明度) ---
; GlassAlpha 控制左侧栏底色不透明度。对应 v5 顶部"指挥栏透明度"滑块。
; 0 = 全透明叠壁纸; 56 ≈ v5 默认 22%(56/255≈.22)。调大更实, 调小更透。
GlassAlpha=56
ColorGlass=12,22,38,56            ; 暗蓝玻璃底 (alpha=GlassAlpha 同值, 见下注)
ColorGlassHi=120,170,230,20       ; 玻璃顶部高光
; 注: ColorGlass 的 alpha 需与 GlassAlpha 保持一致。若改 GlassAlpha,
;     同步改这里第 4 位; 或在 Rail.ini 里用 12,22,38,#GlassAlpha# 动态引用。

; --- 旧版别名 (向后兼容: 旧 ini 里的 Cyan*/Blue* 引用映射到 steel) ---
ColorCyan=111,168,224,255
ColorCyanEdge=111,168,224,235
ColorCyanDim=111,168,224,150
ColorCyanDeep=111,168,224,46
ColorBlue=111,168,224,255
ColorBlueEdge=111,168,224,235
ColorBlueDim=111,168,224,150
ColorBlueDeep=111,168,224,46
ColorBlueIce=219,233,251,255
ColorText=219,233,251,255
ColorTextDim=141,166,196,235
ColorPanel=12,22,38,56

; ===== Fonts =====
; v5 设计字体: Oxanium(数字/标题) + Chakra Petch(标签/表格)。
; 这两个是 Google Fonts, 不随 Windows 自带 → 随包分发到 @Resources\Fonts\,
; 各 skin 用 [Rainmeter] FontFile / 或本地安装。若字体缺失, Rainmeter
; 回退到 FontFace 兜底 (Bahnschrift, Win10/11 自带)。
FontFace=Oxanium
FontFaceLight=Oxanium Light
FontFaceData=Chakra Petch
FontFaceFallback=Bahnschrift
; 中文: 思源黑 (随包) 优先, YaHei 兜底。
FontFaceCN=Noto Sans SC
FontFaceCNFallback=Microsoft YaHei UI
; HUD 图标字形 (播放控件等)
FontFaceIcon=Segoe MDL2 Assets

; ===== 字体文件 (随包分发, 各 skin @include 引用) =====
; 见 @Resources\Fonts\  (Oxanium / Chakra Petch / Noto Sans SC subset)
FontFileDisplay=#@#Fonts\Oxanium-Light.ttf
FontFileDisplayB=#@#Fonts\Oxanium-SemiBold.ttf
FontFileData=#@#Fonts\ChakraPetch-Medium.ttf
FontFileDataB=#@#Fonts\ChakraPetch-SemiBold.ttf
FontFileCN=#@#Fonts\NotoSansSC-Regular.otf

; ===== Dock launcher target paths =====
; Edit these to your own folders / apps.
DockUndertakerPath=C:\Users\Public\Documents
DockBlackDogPath=C:\Users\Public\Documents
DockGunSnakePath=C:\Program Files (x86)\Steam\Steam.exe
DockLaughingFoxPath=C:\Users\Public\Videos
DockSnowWitchPath=::{645FF040-5081-101B-9F08-00AA002F954E}

; ===== Music source =====
;   WNP        = WebNowPlaying-Redux (推荐: 网易云/QQ音乐/Spotify/浏览器)
;   Spotify    = 内置 NowPlaying 插件 PlayerType=Spotify
;   TitleSniff = 降级模式读焦点窗口标题
MusicSource=WNP
