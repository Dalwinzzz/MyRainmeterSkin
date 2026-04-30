; ============================================================
;  86 HUD · Shared Variables
;  Included by every skin via:
;    [Rainmeter]
;    @include=#@#Variables.inc
; ============================================================

[Variables]

; ===== Palette (RGBA, 0-255) =====
ColorCyan=126,229,245,255
ColorCyanEdge=126,229,245,242
ColorCyanDim=126,229,245,115
ColorCyanDeep=126,229,245,46
ColorRed=255,82,82,255
ColorRedDim=255,82,82,217
ColorText=245,251,255,255
ColorTextDim=245,251,255,179
ColorShadow=0,8,18,242
ColorPanel=10,22,38,128

; ===== Fonts =====
; Bahnschrift ships with Windows 10/11 by default.
; Falls back to Trebuchet MS / Arial if missing.
FontFace=Bahnschrift
FontFaceLight=Bahnschrift Light
FontFaceCondensed=Bahnschrift Condensed

; ===== Dock launcher target paths =====
; Edit these to your own folders / apps.
DockDevPath=C:\Users\Public\Documents
DockDocPath=C:\Users\Public\Documents
DockGamePath=C:\Program Files (x86)\Steam\Steam.exe
DockMediaPath=C:\Users\Public\Videos
; Recycle Bin shell CLSID — universal across Windows installs
DockBinPath=::{645FF040-5081-101B-9F08-00AA002F954E}

; ===== Music source =====
; Values:
;   WNP        = WebNowPlaying-Redux third-party plugin (recommended; supports
;                NetEase Cloud Music / QQ Music desktop via SMTC adapter,
;                plus Spotify / YTM / etc via browser extension)
;   Spotify    = built-in NowPlaying plugin with PlayerType=Spotify (no setup)
;   TitleSniff = degraded mode reading focus-window title (no metadata)
MusicSource=WNP
