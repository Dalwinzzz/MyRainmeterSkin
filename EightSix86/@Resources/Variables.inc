; ============================================================
;  86 HUD · Shared Variables
;  Included by every skin via:
;    [Rainmeter]
;    @include=#@#Variables.inc
; ============================================================

[Variables]

; ===== Palette (RGBA, 0-255) — Red Lycoris × Cobalt Blue =====
; Reference: 86 EIGHTY-SIX — red lycoris field × Republic HUD blue
; Rule: 红 = focal points / accents / alerts
;       蓝 = HUD chrome / structure / dividers
;       中性白 = data values

; --- Reds (彼岸花鲜红 #C81E3A) ---
ColorRed=200,30,58,255
ColorRedEdge=200,30,58,242
ColorRedDim=200,30,58,150
ColorRedDeep=200,30,58,46
ColorRedDark=126,20,36,255
ColorRedLight=232,74,106,255
ColorRedAlert=160,24,40,255

; --- Blues (钴蓝 #1E5AC8) ---
ColorBlue=30,90,200,255
ColorBlueEdge=30,90,200,242
ColorBlueDim=30,90,200,150
ColorBlueDeep=30,90,200,46
ColorBlueDark=20,44,126,255
ColorBlueLight=74,138,232,255
ColorBlueIce=93,162,242,255

; --- Aliases — legacy "Cyan*" names retained for backward compatibility,
;     mapped to Blue* values so existing meter references render as cobalt.
ColorCyan=30,90,200,255
ColorCyanEdge=30,90,200,242
ColorCyanDim=30,90,200,150
ColorCyanDeep=30,90,200,46

; --- Neutrals ---
ColorText=245,251,255,255
ColorTextDim=184,192,204,242
ColorShadow=0,5,16,242
ColorPanel=5,9,18,128

; ===== Fonts =====
; Bahnschrift ships with Windows 10/11 by default.
; Falls back to Trebuchet MS / Arial if missing.
FontFace=Bahnschrift
FontFaceLight=Bahnschrift Light
FontFaceCondensed=Bahnschrift Condensed
; Microsoft YaHei UI ships with Windows. Used for any Chinese-character text
; (Bahnschrift has no CJK glyphs, so we fall back to YaHei for those meters).
FontFaceCN=Microsoft YaHei UI
; Segoe MDL2 Assets ships with Windows 10/11. Provides reliable HUD glyphs
; (PrevTrack=E892, PlayPause=E768, NextTrack=E893, etc.)
FontFaceIcon=Segoe MDL2 Assets

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
