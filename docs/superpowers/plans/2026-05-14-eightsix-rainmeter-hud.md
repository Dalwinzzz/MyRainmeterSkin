# EightSix86 Rainmeter HUD Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rework the existing EightSix86 Rainmeter skin into a red-blue 86 HUD with fixed encoding, working search, WNP/SMTC music controls, and a multi-level Dock folder menu.

**Architecture:** Keep the existing skin folder layout and centralize shared choices in `EightSix86/@Resources/Variables.inc`. Add small support scripts for validation and Dock target routing, then update each Rainmeter component independently. `DockMenu` uses Rainmeter `FileView` parent/child measures for folder navigation and pagination.

**Tech Stack:** Rainmeter INI skins, Rainmeter `InputText`, Rainmeter `FileView`, WebNowPlaying-Redux Rainmeter plugin, PowerShell, Python 3 standard library, Git.

---

## File Structure

- Modify: `EightSix86/@Resources/Variables.inc`
  - Owns palette, fonts, search URLs, Dock paths, Dock menu defaults, and WNP labels.
- Modify: `EightSix86/@Resources/fix-encoding.py`
  - Re-stamps `.ini`, `.inc`, and selected `.md` files as UTF-8 BOM.
- Create: `EightSix86/@Resources/check-skin.py`
  - Static validation for BOM, mojibake signatures, and missing shared variables.
- Create: `EightSix86/@Resources/Scripts/DockRoute.ps1`
  - Routes Dock clicks: folders open `DockMenu`; direct files, shortcuts, executables, and shell targets open directly.
- Modify: `EightSix86/Clock/Clock.ini`
  - Applies red-blue palette and mixed CJK/English typography.
- Modify: `EightSix86/Calendar/Calendar.ini`
  - Applies red-blue palette and clean Chinese footer text.
- Modify: `EightSix86/System/System.ini`
  - Applies roster styling and removes always-red network row behavior.
- Modify: `EightSix86/SearchGoogle/SearchGoogle.ini`
  - Uses shared URL and corrected click/input region.
- Modify: `EightSix86/SearchBing/SearchBing.ini`
  - Mirrors Google search behavior with Bing URL.
- Modify: `EightSix86/Music/Music.ini`
  - Uses WNP/SMTC measures, support flags, offline status, and control commands.
- Modify: `EightSix86/Dock/Dock.ini`
  - Routes non-bin launchers through `DockRoute.ps1`; keeps Bin special behavior.
- Create: `EightSix86/DockMenu/DockMenu.ini`
  - Multi-level folder roster using `FileView`.
- Create: `EightSix86/@Resources/docs/install.md`
  - Documents WNP/SMTC install, search behavior, Dock menu routing, and encoding commands.
- Modify: `README.md`
  - Replaces mojibake with a short bilingual project summary and setup link.
- Modify: `EightSix86/@Resources/docs/v1-design.md`
  - Replaces corrupted text with a brief note that v1 is superseded by the committed spec.

---

## Task 1: Add Static Validation And Encoding Coverage

**Files:**
- Create: `EightSix86/@Resources/check-skin.py`
- Modify: `EightSix86/@Resources/fix-encoding.py`
- Test: command-line validation script

- [ ] **Step 1: Verify the static checker is absent**

Run:

```powershell
python EightSix86/@Resources/check-skin.py --self-test
```

Expected: FAIL because `EightSix86/@Resources/check-skin.py` does not exist.

- [ ] **Step 2: Create `check-skin.py`**

Create `EightSix86/@Resources/check-skin.py` with:

```python
#!/usr/bin/env python3
"""Static checks for the EightSix86 Rainmeter skin."""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

BOM_UTF8 = b"\xef\xbb\xbf"

MOJIBAKE_PATTERNS = (
    "\ufffd",
    "涓",
    "鈥",
    "鈻",
    "璺",
    "鏄",
    "浠",
    "鎵",
    "杈",
    "妫",
)

BUILT_IN_VARIABLES = {
    "CRLF",
    "CURRENTCONFIG",
    "CURRENTCONFIGX",
    "CURRENTCONFIGY",
    "CURRENTCONFIGWIDTH",
    "CURRENTCONFIGHEIGHT",
    "CURRENTCONFIGZPOS",
    "CURRENTFILE",
    "CURRENTPATH",
    "CURRENTSECTION",
    "PROGRAMPATH",
    "PROGRAMDRIVE",
    "SETTINGSPATH",
    "SKINSPATH",
    "PLUGINSPATH",
}

VAR_RE = re.compile(r"#([A-Za-z][A-Za-z0-9_]*)#")
CJK_RE = re.compile(r"[\u3400-\u9fff]")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def read_text(path: Path) -> str:
    data = read_bytes(path)
    if data.startswith(BOM_UTF8):
        data = data[len(BOM_UTF8):]
    return data.decode("utf-8", errors="replace")


def skin_files(root: Path) -> list[Path]:
    eight = root / "EightSix86"
    files = list(eight.rglob("*.ini")) + list(eight.rglob("*.inc"))
    docs = [root / "README.md"]
    docs += list((eight / "@Resources" / "docs").glob("*.md"))
    docs += list((root / "docs" / "superpowers").rglob("*.md"))
    return sorted({p for p in files + docs if p.exists()})


def needs_bom(path: Path, text: str) -> bool:
    if path.suffix.lower() in {".ini", ".inc"}:
        return True
    return bool(CJK_RE.search(text))


def parse_variables(path: Path) -> set[str]:
    text = read_text(path)
    keys: set[str] = set()
    in_vars = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(";"):
            continue
        if line.startswith("[") and line.endswith("]"):
            in_vars = line.lower() == "[variables]"
            continue
        if in_vars and "=" in line:
            keys.add(line.split("=", 1)[0].strip())
    return keys


def check(root: Path) -> list[str]:
    errors: list[str] = []
    variables_path = root / "EightSix86" / "@Resources" / "Variables.inc"
    variables = parse_variables(variables_path) if variables_path.exists() else set()

    for path in skin_files(root):
        rel = path.relative_to(root)
        data = read_bytes(path)
        text = read_text(path)

        if needs_bom(path, text) and not data.startswith(BOM_UTF8):
            errors.append(f"{rel}: missing UTF-8 BOM")

        for pattern in MOJIBAKE_PATTERNS:
            if pattern in text:
                errors.append(f"{rel}: probable mojibake marker {pattern!r}")
                break

        if path.suffix.lower() in {".ini", ".inc"}:
            for name in sorted(set(VAR_RE.findall(text))):
                if name in BUILT_IN_VARIABLES:
                    continue
                if name not in variables:
                    errors.append(f"{rel}: undefined shared variable #{name}#")

    return errors


def self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        res = root / "EightSix86" / "@Resources"
        res.mkdir(parents=True)
        (res / "Variables.inc").write_bytes(
            BOM_UTF8 + b"[Variables]\nColorText=255,255,255,255\n"
        )
        clock = root / "EightSix86" / "Clock"
        clock.mkdir()
        (clock / "Clock.ini").write_bytes(
            BOM_UTF8 + b"[Rainmeter]\n[Meter]\nFontColor=#ColorText#\n"
        )
        errors = check(root)
        if errors:
            print("\n".join(errors))
            return 1
    print("self-test passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    errors = check(repo_root())
    if errors:
        print("Static check failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("Static check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Run checker self-test**

Run:

```powershell
python EightSix86/@Resources/check-skin.py --self-test
```

Expected: PASS with `self-test passed`.

- [ ] **Step 4: Update `fix-encoding.py` scan targets**

Modify the `files = sorted(set(...))` block in `EightSix86/@Resources/fix-encoding.py` to:

```python
files = sorted(set(
    glob.glob('EightSix86/**/*.ini', recursive=True) +
    glob.glob('EightSix86/**/*.inc', recursive=True) +
    glob.glob('EightSix86/@Resources/docs/*.md', recursive=True) +
    glob.glob('docs/superpowers/specs/*.md', recursive=True) +
    glob.glob('docs/superpowers/plans/*.md', recursive=True) +
    ['README.md']
))
```

- [ ] **Step 5: Run encoding restamp**

Run:

```powershell
python EightSix86/@Resources/fix-encoding.py
```

Expected: command lists restamped `.ini`, `.inc`, and markdown files as `utf8-bom`.

- [ ] **Step 6: Run current full static check**

Run:

```powershell
python EightSix86/@Resources/check-skin.py
```

Expected: FAIL listing existing mojibake documentation and missing variables that later tasks will fix.

- [ ] **Step 7: Commit validation tooling**

```powershell
git add -- EightSix86/@Resources/check-skin.py EightSix86/@Resources/fix-encoding.py
git commit -m "test: add EightSix86 skin validation"
```

---

## Task 2: Centralize Theme Variables

**Files:**
- Modify: `EightSix86/@Resources/Variables.inc`
- Test: `python EightSix86/@Resources/check-skin.py`

- [ ] **Step 1: Inspect current shared variables**

Run:

```powershell
Get-Content -LiteralPath 'EightSix86/@Resources/Variables.inc' -Encoding UTF8
```

Expected: file still contains old cobalt-oriented values such as `ColorBlue=30,90,200,255`.

- [ ] **Step 2: Replace `Variables.inc` content**

Replace the file with:

```ini
; ============================================================
;  86 HUD · Shared Variables
;  Red lycoris field × saturated battlefield blue
; ============================================================

[Variables]

; ===== Palette =====
ColorRed=238,28,36,255
ColorRedEdge=255,64,72,242
ColorRedDim=238,28,36,150
ColorRedDeep=238,28,36,54
ColorRedDark=126,14,24,255

ColorBlue=0,58,220,255
ColorBlueEdge=22,96,255,242
ColorBlueDim=0,58,220,150
ColorBlueDeep=0,58,220,54
ColorBlueDark=4,20,92,255

ColorCyan=40,198,255,255
ColorCyanEdge=40,198,255,242
ColorCyanDim=40,198,255,120
ColorCyanDeep=40,198,255,46

ColorText=245,251,255,255
ColorTextDim=184,192,204,242
ColorShadow=0,5,16,242
ColorPanel=5,9,18,128
ColorPanelDeep=5,9,18,196

; ===== Fonts =====
FontFace=Bahnschrift
FontFaceLight=Bahnschrift Light
FontFaceCondensed=Bahnschrift Condensed
FontFaceCN=Microsoft YaHei UI
FontFaceIcon=Segoe MDL2 Assets

; ===== Search =====
SearchGoogleUrl=https://www.google.com/search?q=
SearchBingUrl=https://www.bing.com/search?q=

; ===== Dock launcher target paths =====
DockDevPath=C:\Users\Public\Documents
DockDocPath=C:\Users\Public\Documents
DockGamePath=C:\Program Files (x86)\Steam\Steam.exe
DockMediaPath=C:\Users\Public\Videos
DockBinPath=::{645FF040-5081-101B-9F08-00AA002F954E}

; ===== Dock menu =====
DockMenuRoot=C:\Users\Public\Documents
DockMenuError=
DockMenuRows=8
DockMenuConfig=EightSix86\DockMenu
DockMenuFile=DockMenu.ini

; ===== Music source =====
MusicSource=WNP
MusicSourceLabel=WNP / SMTC
MusicOfflineText=WNP OFFLINE / 检查 SMTC
```

- [ ] **Step 3: Restamp encoding**

Run:

```powershell
python EightSix86/@Resources/fix-encoding.py
```

Expected: `Variables.inc` is reported as UTF-8 BOM.

- [ ] **Step 4: Run static check**

Run:

```powershell
python EightSix86/@Resources/check-skin.py
```

Expected: no missing-variable errors for new variables added in this task; documentation mojibake may still be reported.

- [ ] **Step 5: Commit shared variables**

```powershell
git add -- EightSix86/@Resources/Variables.inc
git commit -m "style: centralize EightSix86 red blue palette"
```

---

## Task 3: Repair Project Documentation

**Files:**
- Modify: `README.md`
- Modify: `EightSix86/@Resources/docs/v1-design.md`
- Create: `EightSix86/@Resources/docs/install.md`
- Test: `python EightSix86/@Resources/check-skin.py`

- [ ] **Step 1: Confirm docs currently fail mojibake scan**

Run:

```powershell
python EightSix86/@Resources/check-skin.py
```

Expected: FAIL includes `README.md` and `EightSix86/@Resources/docs/v1-design.md`.

- [ ] **Step 2: Replace `README.md`**

Use:

```markdown
# MyRainmeterSkin

个人自制 Rainmeter 皮肤集合。

## EightSix86

`EightSix86` 是一个基于《86 -Eighty Six-》视觉语言的桌面 HUD 皮肤。当前重整目标：

- 修复中文乱码与 UTF-8 BOM 编码问题。
- 使用彼岸花红 × 高饱和战场蓝作为主题色。
- 支持 Google / Bing 输入搜索并跳转系统默认浏览器。
- 支持 WebNowPlaying-Redux + SMTC adapter 联动网易云音乐 / QQ 音乐桌面客户端。
- 支持 Dock 文件夹入口展开多级菜单。

配置与安装说明见 `EightSix86/@Resources/docs/install.md`。
```

- [ ] **Step 3: Replace `v1-design.md`**

Use:

```markdown
# EightSix86 v1 Design Note

这份文档替换了早期已经损坏编码的 v1 设计稿。

当前实现以仓库中的正式 spec 为准：

- `docs/superpowers/specs/2026-05-14-eightsix-rainmeter-hud-design.md`

核心方向：

- 深色透明 Rainmeter HUD。
- 彼岸花红 × 高饱和战场蓝主题色。
- 中英混排，英文用于战术标签，中文用于用户可读状态。
- 搜索、音乐、Dock 多级菜单都必须可交互。
```

- [ ] **Step 4: Create `install.md`**

Create `EightSix86/@Resources/docs/install.md`:

```markdown
# EightSix86 安装与配置

## 编码

Rainmeter 在中文 Windows 环境下可能把无 BOM 的 UTF-8 文件按系统代码页读取。每次编辑 `.ini`、`.inc` 或含中文的 Markdown 后，运行：

```powershell
python EightSix86/@Resources/fix-encoding.py
python EightSix86/@Resources/check-skin.py
```

## 搜索

`SearchGoogle` 和 `SearchBing` 使用 Rainmeter `InputText`：

- 点击输入框进入输入。
- 按回车执行搜索。
- URL 前缀在 `EightSix86/@Resources/Variables.inc` 中配置。

## 音乐

网易云音乐 / QQ 音乐桌面客户端联动依赖：

- WebNowPlaying-Redux Rainmeter plugin。
- WebNowPlaying SMTC / Desktop Players support。

安装后播放音乐，`Music` 组件会显示标题、歌手、进度和状态。若显示 `WNP OFFLINE / 检查 SMTC`，检查插件、SMTC adapter 和播放器系统媒体控制是否可用。

## Dock

Dock 路径在 `Variables.inc` 中配置：

```ini
DockDevPath=C:\Users\Public\Documents
DockDocPath=C:\Users\Public\Documents
DockGamePath=C:\Program Files (x86)\Steam\Steam.exe
DockMediaPath=C:\Users\Public\Videos
```

点击行为：

- 文件夹：打开 `DockMenu` 多级菜单。
- 文件、快捷方式、可执行程序：直接打开。
- 回收站：左键打开，右键清空。
```

- [ ] **Step 5: Restamp and run static check**

Run:

```powershell
python EightSix86/@Resources/fix-encoding.py
python EightSix86/@Resources/check-skin.py
```

Expected: documentation mojibake errors are gone; remaining failures are tied to component implementation not finished yet.

- [ ] **Step 6: Commit documentation**

```powershell
git add -- README.md EightSix86/@Resources/docs/v1-design.md EightSix86/@Resources/docs/install.md
git commit -m "docs: repair EightSix86 setup documentation"
```

---

## Task 4: Update Clock And Calendar Visuals

**Files:**
- Modify: `EightSix86/Clock/Clock.ini`
- Modify: `EightSix86/Calendar/Calendar.ini`
- Test: static check and manual Rainmeter refresh

- [ ] **Step 1: Verify old palette usage**

Run:

```powershell
Select-String -Path 'EightSix86/Clock/Clock.ini','EightSix86/Calendar/Calendar.ini' -Pattern 'ColorBlue=|ColorBlueEdge|ColorRed|ColorCyan'
```

Expected: current files reference old color semantics.

- [ ] **Step 2: Update Clock styles**

In `Clock.ini`, ensure these style blocks match:

```ini
[stDigits]
StringAlign=CenterCenter
FontFace=#FontFaceLight#
FontSize=96
FontColor=#ColorText#
FontEffectColor=#ColorShadow#
StringEffect=Shadow
AntiAlias=1
InlineSetting=Color | #ColorRed#
InlinePattern=:

[stDateCN]
StringAlign=CenterCenter
FontFace=#FontFaceCN#
FontSize=16
FontColor=#ColorText#
FontEffectColor=#ColorShadow#
StringEffect=Shadow
StringStyle=Bold
AntiAlias=1

[stDoyCN]
StringAlign=LeftCenter
FontFace=#FontFaceCN#
FontSize=9
FontColor=#ColorCyanEdge#
FontEffectColor=#ColorShadow#
StringEffect=Shadow
StringStyle=Bold
AntiAlias=1
```

- [ ] **Step 3: Update Clock chrome**

Set the Clock diamond and scan line colors to:

```ini
Shape=Rectangle 0,0,18,18 | Rotate 45,9,9 | StrokeWidth 1 | Stroke Color #ColorBlueEdge# | Fill Color #ColorPanel#
```

and:

```ini
Shape=Line 0,3,260,3 | StrokeWidth 1 | Stroke LinearGradient ScanGrad
ScanGrad=0 | #ColorCyanEdge# ; 0.0 | 40,198,255,0 ; 1.0
```

- [ ] **Step 4: Update Calendar current-day focus**

In `Calendar.ini`, keep current month text white and current day red:

```ini
[stMonthCur]
FontFace=#FontFace#
FontSize=18
FontColor=#ColorText#
FontEffectColor=#ColorShadow#
StringEffect=Shadow
StringCase=Upper
StringStyle=Bold
AntiAlias=1
StringAlign=Right

[stNumCur]
FontFace=#FontFace#
FontSize=22
FontColor=#ColorRed#
FontEffectColor=#ColorShadow#
StringEffect=Shadow
StringStyle=Bold
AntiAlias=1
StringAlign=Left
```

- [ ] **Step 5: Run checks**

Run:

```powershell
python EightSix86/@Resources/fix-encoding.py
python EightSix86/@Resources/check-skin.py
```

Expected: no new errors from `Clock.ini` or `Calendar.ini`.

- [ ] **Step 6: Manual Rainmeter check**

In Rainmeter, refresh:

- `EightSix86\Clock`
- `EightSix86\Calendar`

Expected: no parse errors; colon/current day are red; structural lines are blue/cyan.

- [ ] **Step 7: Commit Clock and Calendar**

```powershell
git add -- EightSix86/Clock/Clock.ini EightSix86/Calendar/Calendar.ini
git commit -m "style: refresh EightSix86 clock and calendar"
```

---

## Task 5: Update System Roster

**Files:**
- Modify: `EightSix86/System/System.ini`
- Test: static check and manual Rainmeter refresh

- [ ] **Step 1: Verify current forced alert row**

Run:

```powershell
Select-String -LiteralPath 'EightSix86/System/System.ini' -Pattern 'NET DOWN|stRowValAlert|ColorRed|ColorCyan'
```

Expected: `NET DOWN` currently uses alert styles unconditionally.

- [ ] **Step 2: Normalize roster colors**

Keep the existing measures and rows, but change row 4 to the normal style:

```ini
[mtrR4Pwr]
Meter=String
MeterStyle=stMoon
X=180
Y=129
Text=○

[mtrR4Val]
Meter=String
MeterStyle=stRowVal
MeasureName=mNetIn
X=212
Y=124
Text=%1
AutoScale=1
NumOfDecimals=0

[mtrR4Rate]
Meter=String
MeterStyle=stRowRate
X=246
Y=124
Text=──

[mtrR4Sta]
Meter=Shape
X=271
Y=129
Shape=Ellipse 4,4,4 | StrokeWidth 0 | Fill Color #ColorBlueEdge#

[mtrR4Sep]
Meter=Shape
X=14
Y=142
Shape=Line 0,0,312,0 | StrokeWidth 1 | Stroke Color #ColorBlueDeep#
```

- [ ] **Step 3: Update roster structural styles**

Make these style and divider choices consistent:

```ini
[stColHead]
FontColor=#ColorBlueEdge#

[stRowNum]
FontColor=#ColorBlueEdge#

[stMoon]
FontFace=Segoe UI Symbol
FontSize=10
FontColor=#ColorBlueEdge#

[mtrDivider1]
Shape=Line 0,0,312,0 | StrokeWidth 1 | Stroke Color #ColorBlueEdge#

[mtrDivider2]
Shape=Line 0,0,312,0 | StrokeWidth 1 | Stroke Color #ColorBlueDim#
```

- [ ] **Step 4: Keep red alert styles available**

Leave these styles in the file for future threshold-driven alert use:

```ini
[stRowValAlert]
FontFace=#FontFace#
FontSize=10
FontColor=#ColorRed#
FontEffectColor=#ColorShadow#
StringEffect=Shadow
StringStyle=Bold
StringAlign=Center
AntiAlias=1

[stRowRateAlert]
FontFace=#FontFace#
FontSize=8
FontColor=#ColorRed#
FontEffectColor=#ColorShadow#
StringEffect=Shadow
StringAlign=Center
AntiAlias=1
```

- [ ] **Step 5: Run checks**

Run:

```powershell
python EightSix86/@Resources/fix-encoding.py
python EightSix86/@Resources/check-skin.py
```

Expected: no System-specific errors.

- [ ] **Step 6: Manual Rainmeter check**

Refresh `EightSix86\System`.

Expected: roster uses blue structure; no row is red unless a future threshold explicitly switches it.

- [ ] **Step 7: Commit System roster**

```powershell
git add -- EightSix86/System/System.ini
git commit -m "style: align system roster with red blue HUD"
```

---

## Task 6: Fix Search Interactions

**Files:**
- Modify: `EightSix86/SearchGoogle/SearchGoogle.ini`
- Modify: `EightSix86/SearchBing/SearchBing.ini`
- Test: static check and manual browser search

- [ ] **Step 1: Verify search command does not use shared URL**

Run:

```powershell
Select-String -Path 'EightSix86/SearchGoogle/SearchGoogle.ini','EightSix86/SearchBing/SearchBing.ini' -Pattern 'Command1|google.com|bing.com'
```

Expected: direct URLs are currently embedded in each file.

- [ ] **Step 2: Update Google InputText**

In `SearchGoogle.ini`, set:

```ini
[mInput]
Measure=Plugin
Plugin=InputText
SolidColor=5,9,18,230
StringStyle=Bold
StringAlign=LeftCenter
FontFace=#FontFaceCN#
FontSize=11
FontColor=#ColorText#
AntiAlias=1
DefaultValue=""
FocusDismiss=1
Command1=["#SearchGoogleUrl#$UserInput$"]
X=130
Y=10
W=320
H=22
UpdateDivider=86400
DynamicVariables=1
```

- [ ] **Step 3: Update Bing InputText**

In `SearchBing.ini`, set:

```ini
[mInput]
Measure=Plugin
Plugin=InputText
SolidColor=5,9,18,230
StringStyle=Bold
StringAlign=LeftCenter
FontFace=#FontFaceCN#
FontSize=11
FontColor=#ColorText#
AntiAlias=1
DefaultValue=""
FocusDismiss=1
Command1=["#SearchBingUrl#$UserInput$"]
X=130
Y=10
W=320
H=22
UpdateDivider=86400
DynamicVariables=1
```

- [ ] **Step 4: Align visible boxes and hit areas in both files**

Use these values in both search skins:

```ini
[mtrInputBox]
Meter=Shape
X=126
Y=8
Shape=Rectangle 0,0,322,24 | StrokeWidth 1 | Stroke Color #ColorBlueEdge# | Fill Color #ColorPanel#

[mtrInputLine]
Meter=Shape
X=128
Y=33
Shape=Line 0,0,318,0 | StrokeWidth 1 | Stroke Color #ColorCyanEdge#

[mtrInputHit]
Meter=Image
SolidColor=0,0,0,1
X=126
Y=8
W=322
H=24
LeftMouseUpAction=[!CommandMeasure mInput "ExecuteBatch 1"]
```

- [ ] **Step 5: Update visible labels**

Google:

```ini
[mtrInputHint]
Text=输入搜索词 · google.com

[mtrDispatch]
Text=执行
```

Bing:

```ini
[mtrInputHint]
Text=输入搜索词 · bing.com

[mtrDispatch]
Text=执行
```

- [ ] **Step 6: Run checks**

Run:

```powershell
python EightSix86/@Resources/fix-encoding.py
python EightSix86/@Resources/check-skin.py
```

Expected: no Search-specific errors.

- [ ] **Step 7: Manual search check**

Refresh:

- `EightSix86\SearchGoogle`
- `EightSix86\SearchBing`

Click each input field, type `86 anime`, press Enter.

Expected: system default browser opens the matching Google or Bing search results.

- [ ] **Step 8: Commit Search**

```powershell
git add -- EightSix86/SearchGoogle/SearchGoogle.ini EightSix86/SearchBing/SearchBing.ini
git commit -m "fix: make EightSix86 search bars interactive"
```

---

## Task 7: Rework Music For WNP / SMTC

**Files:**
- Modify: `EightSix86/Music/Music.ini`
- Test: static check and manual WNP/SMTC playback

- [ ] **Step 1: Verify existing WNP measure names**

Run:

```powershell
Select-String -LiteralPath 'EightSix86/Music/Music.ini' -Pattern 'Plugin=WebNowPlaying|PlayerType=|CommandMeasure'
```

Expected: WNP measures exist, but status handling and support flags are incomplete.

- [ ] **Step 2: Replace WNP measures with explicit status/support set**

Use these measure blocks:

```ini
[mPlayerTitle]
Measure=Plugin
Plugin=WebNowPlaying
PlayerType=Title
Substitute="":"——"

[mPlayerArtist]
Measure=Plugin
Plugin=WebNowPlaying
PlayerType=Artist
Substitute="":"未在播放"

[mPlayerStatus]
Measure=Plugin
Plugin=WebNowPlaying
PlayerType=Status

[mPlayerState]
Measure=Plugin
Plugin=WebNowPlaying
PlayerType=State

[mPlayerStateLabel]
Measure=Plugin
Plugin=WebNowPlaying
PlayerType=State
Substitute="0":"已停止","1":"正在播放","2":"已暂停","":"WNP OFFLINE"

[mPlayerPosition]
Measure=Plugin
Plugin=WebNowPlaying
PlayerType=Position

[mPlayerDuration]
Measure=Plugin
Plugin=WebNowPlaying
PlayerType=Duration

[mPlayerProgress]
Measure=Plugin
Plugin=WebNowPlaying
PlayerType=Progress

[mSupportsPrev]
Measure=Plugin
Plugin=WebNowPlaying
PlayerType=SupportsSkipPrevious

[mSupportsPlayPause]
Measure=Plugin
Plugin=WebNowPlaying
PlayerType=SupportsPlayPause

[mSupportsNext]
Measure=Plugin
Plugin=WebNowPlaying
PlayerType=SupportsSkipNext
```

- [ ] **Step 3: Update header source and offline text**

Use:

```ini
[mtrHead]
Meter=String
MeterStyle=stHead
MeasureName=mPlayerStateLabel
X=18
Y=12
Text=▶ %1

[mtrHeadSrc]
Meter=String
MeterStyle=stHeadSrc
X=522
Y=12
Text=#MusicSourceLabel#
DynamicVariables=1
```

If WNP is disconnected, the title/artist row already displays `—— / 未在播放`; the source label stays `WNP / SMTC` so the user knows which bridge is expected.

- [ ] **Step 4: Update progress color**

Use:

```ini
[mtrProgressBar]
Meter=Bar
MeasureName=mPlayerProgress
X=18
Y=72
W=304
H=3
BarOrientation=HORIZONTAL
BarColor=#ColorRed#
SolidColor=#ColorBlueDeep#

[mtrProgressPin]
Meter=Shape
X=326
Y=70
Shape=Rectangle 0,0,7,7 | Rotate 45,3.5,3.5 | StrokeWidth 1 | Stroke Color #ColorRed# | Fill Color #ColorRed#
```

- [ ] **Step 5: Keep controls wired to a WNP measure**

Use `mPlayerTitle` as the command target:

```ini
LeftMouseUpAction=[!CommandMeasure mPlayerTitle "Previous"]
LeftMouseUpAction=[!CommandMeasure mPlayerTitle "PlayPause"]
LeftMouseUpAction=[!CommandMeasure mPlayerTitle "Next"]
```

Apply those three actions to `mtrPrevHit`, `mtrPlayHit`, and `mtrNextHit` respectively.

- [ ] **Step 6: Run checks**

Run:

```powershell
python EightSix86/@Resources/fix-encoding.py
python EightSix86/@Resources/check-skin.py
```

Expected: no Music-specific errors.

- [ ] **Step 7: Manual disconnected check**

Refresh `EightSix86\Music` while WNP/SMTC is not connected.

Expected: no blank component; title shows `——`, artist shows `未在播放`, source shows `WNP / SMTC`.

- [ ] **Step 8: Manual connected check**

With WebNowPlaying-Redux and SMTC support installed, start NetEase Cloud Music or QQ Music playback and refresh `EightSix86\Music`.

Expected: title, artist, position, duration, and progress update; previous/play-next controls work when the player supports them.

- [ ] **Step 9: Commit Music**

```powershell
git add -- EightSix86/Music/Music.ini
git commit -m "fix: wire music skin to WNP SMTC"
```

---

## Task 8: Add Dock Routing Script

**Files:**
- Create: `EightSix86/@Resources/Scripts/DockRoute.ps1`
- Modify: `EightSix86/Dock/Dock.ini`
- Test: static check and manual direct/folder routing

- [ ] **Step 1: Create script directory**

Run:

```powershell
New-Item -ItemType Directory -Force -Path 'EightSix86/@Resources/Scripts'
```

Expected: directory exists.

- [ ] **Step 2: Create `DockRoute.ps1`**

Create:

```powershell
param(
    [Parameter(Mandatory=$true)][string]$Target,
    [Parameter(Mandatory=$true)][string]$RainmeterExe,
    [string]$MenuConfig = 'EightSix86\DockMenu',
    [string]$MenuFile = 'DockMenu.ini'
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($Target)) {
    exit 2
}

if ($Target.StartsWith('::{')) {
    Start-Process -FilePath 'explorer.exe' -ArgumentList $Target
    exit 0
}

if (Test-Path -LiteralPath $Target -PathType Container) {
    & $RainmeterExe '!ActivateConfig' $MenuConfig $MenuFile
    Start-Sleep -Milliseconds 100
    & $RainmeterExe '!SetVariable' 'DockMenuRoot' $Target $MenuConfig
    & $RainmeterExe '!SetVariable' 'DockMenuError' '' $MenuConfig
    & $RainmeterExe '!CommandMeasure' 'mPath' 'Update' $MenuConfig
    & $RainmeterExe '!Update' $MenuConfig
    & $RainmeterExe '!Redraw' $MenuConfig
    exit 0
}

if (Test-Path -LiteralPath $Target -PathType Leaf) {
    Start-Process -FilePath $Target
    exit 0
}

& $RainmeterExe '!ActivateConfig' $MenuConfig $MenuFile
Start-Sleep -Milliseconds 100
& $RainmeterExe '!SetVariable' 'DockMenuRoot' $Target $MenuConfig
& $RainmeterExe '!SetVariable' 'DockMenuError' 'PATH LOST' $MenuConfig
& $RainmeterExe '!CommandMeasure' 'mPath' 'Update' $MenuConfig
& $RainmeterExe '!Update' $MenuConfig
& $RainmeterExe '!Redraw' $MenuConfig
exit 3
```

- [ ] **Step 3: Add Dock route action pattern**

In `Dock.ini`, route DEV/DOC/GAME/MEDIA with this action pattern:

```ini
LeftMouseUpAction=["powershell.exe" "-NoProfile" "-ExecutionPolicy" "Bypass" "-File" "#@#Scripts\DockRoute.ps1" "#DockDevPath#" "#PROGRAMPATH#Rainmeter.exe" "#DockMenuConfig#" "#DockMenuFile#"]
```

Use the matching path variable for each launcher:

- DEV: `#DockDevPath#`
- DOC: `#DockDocPath#`
- GAME: `#DockGamePath#`
- MEDIA: `#DockMediaPath#`

- [ ] **Step 4: Keep Bin special behavior**

Leave BIN actions as:

```ini
LeftMouseUpAction=["explorer.exe" "#DockBinPath#"]
RightMouseUpAction=[!CommandMeasure mBinEmpty "EmptyBin"]
```

- [ ] **Step 5: Update Dock colors**

Use `#ColorBlueEdge#` for non-bin marks and `#ColorRedDim#` for BIN mark. Replace old `30,90,200` fills with `#ColorBlueDeep#` where possible.

- [ ] **Step 6: Run checks**

Run:

```powershell
python EightSix86/@Resources/fix-encoding.py
python EightSix86/@Resources/check-skin.py
```

Expected: no Dock-specific missing variable errors.

- [ ] **Step 7: Manual routing check**

Set `DockDevPath=C:\Users\Public\Documents` and `DockGamePath=C:\Windows\System32\notepad.exe` in `Variables.inc`, refresh `EightSix86\Dock`, then click DEV and GAME.

Expected:

- DEV opens or activates `DockMenu`.
- GAME launches Notepad directly.

- [ ] **Step 8: Commit Dock routing**

```powershell
git add -- EightSix86/@Resources/Scripts/DockRoute.ps1 EightSix86/Dock/Dock.ini
git commit -m "feat: route dock targets by path type"
```

---

## Task 9: Add DockMenu FileView Skin

**Files:**
- Create: `EightSix86/DockMenu/DockMenu.ini`
- Test: static check and manual FileView navigation

- [ ] **Step 1: Create DockMenu directory**

Run:

```powershell
New-Item -ItemType Directory -Force -Path 'EightSix86/DockMenu'
```

Expected: directory exists.

- [ ] **Step 2: Create `DockMenu.ini`**

Create:

```ini
; ============================================================
;  86 HUD · DockMenu
;  Multi-level FileView roster for Dock folder targets.
; ============================================================

[Rainmeter]
Update=1000
AccurateText=1
DynamicWindowSize=1
MouseScrollUpAction=[!CommandMeasure mPath "IndexUp"][!UpdateMeasure mPath][!UpdateMeasureGroup Children][!UpdateMeter *][!Redraw]
MouseScrollDownAction=[!CommandMeasure mPath "IndexDown"][!UpdateMeasure mPath][!UpdateMeasureGroup Children][!UpdateMeter *][!Redraw]
@include=#@#Variables.inc

[Metadata]
Name=86 DockMenu
Author=Dalwin
Information=FileView-powered multi-level menu for EightSix86 Dock folders.
Version=1.0.0
License=MIT

[mPath]
Measure=Plugin
Plugin=FileView
Path="#DockMenuRoot#"
Count=#DockMenuRows#
ShowDotDot=0
ShowFolder=1
ShowFile=1
ShowHidden=0
ShowSystem=0
SortType=Type
SortAscending=1
FinishAction=[!UpdateMeasureGroup Children][!UpdateMeter *][!Redraw]
DynamicVariables=1

[mFolderCount]
Measure=Plugin
Plugin=FileView
Path=[mPath]
Type=FolderCount
Group=Children

[mFileCount]
Measure=Plugin
Plugin=FileView
Path=[mPath]
Type=FileCount
Group=Children

[mFolderPath]
Measure=Plugin
Plugin=FileView
Path=[mPath]
Type=FolderPath
Group=Children

[mTotalItems]
Measure=Calc
Formula=(mFolderCount + mFileCount)
DynamicVariables=1
IfCondition=(mTotalItems = 0)
IfTrueAction=[!ShowMeter mtrEmpty][!UpdateMeter mtrEmpty][!Redraw]
IfFalseAction=[!HideMeter mtrEmpty][!UpdateMeter mtrEmpty][!Redraw]

[stHead]
FontFace=#FontFace#
FontSize=9
FontColor=#ColorBlueEdge#
FontEffectColor=#ColorShadow#
StringEffect=Shadow
StringStyle=Bold
StringCase=Upper
AntiAlias=1

[stPath]
FontFace=#FontFaceCN#
FontSize=9
FontColor=#ColorTextDim#
FontEffectColor=#ColorShadow#
StringEffect=Shadow
AntiAlias=1
ClipString=1

[stCol]
FontFace=#FontFace#
FontSize=7
FontColor=#ColorCyanEdge#
FontEffectColor=#ColorShadow#
StringEffect=Shadow
StringStyle=Bold
StringCase=Upper
AntiAlias=1

[stRowNo]
FontFace=#FontFace#
FontSize=8
FontColor=#ColorBlueEdge#
FontEffectColor=#ColorShadow#
StringEffect=Shadow
StringStyle=Bold
AntiAlias=1

[stRowText]
FontFace=#FontFaceCN#
FontSize=9
FontColor=#ColorText#
FontEffectColor=#ColorShadow#
StringEffect=Shadow
ClipString=1
AntiAlias=1

[stRowType]
FontFace=#FontFace#
FontSize=8
FontColor=#ColorCyanEdge#
FontEffectColor=#ColorShadow#
StringEffect=Shadow
StringCase=Upper
AntiAlias=1

[mtrPanel]
Meter=Shape
X=0
Y=0
Shape=Rectangle 0,0,360,292,4 | StrokeWidth 1 | Stroke Color #ColorBlueEdge# | Fill Color #ColorPanelDeep#

[mtrScan]
Meter=Shape
X=12
Y=8
Shape=Line 0,0,336,0 | StrokeWidth 2 | Stroke LinearGradient ScanGrad
ScanGrad=0 | #ColorCyanEdge# ; 0.0 | 40,198,255,0 ; 1.0

[mtrHead]
Meter=String
MeterStyle=stHead
X=14
Y=18
Text=/ DOCK MENU · FILEVIEW

[mtrClose]
Meter=String
MeterStyle=stHead
StringAlign=Right
FontColor=#ColorRed#
X=344
Y=18
Text=CLOSE
LeftMouseUpAction=[!DeactivateConfig "#CURRENTCONFIG#"]

[mtrPath]
Meter=String
MeterStyle=stPath
MeasureName=mFolderPath
X=14
Y=40
W=332
H=16
Text=%1

[mtrCols]
Meter=String
MeterStyle=stCol
X=14
Y=64
Text=NO      TYPE        NAME

[mtrDivider]
Meter=Shape
X=14
Y=81
Shape=Line 0,0,332,0 | StrokeWidth 1 | Stroke Color #ColorBlueDim#

[mtrError]
Meter=String
MeterStyle=stHead
FontColor=#ColorRed#
X=14
Y=84
W=332
H=18
Text=#DockMenuError#
DynamicVariables=1

[mtrEmpty]
Meter=String
MeterStyle=stHead
FontColor=#ColorRed#
StringAlign=CenterCenter
X=180
Y=176
W=320
H=24
Text=NO TARGETS
Hidden=1
```

- [ ] **Step 3: Add eight child measure sets**

For each index 1 through 8, add the same pattern with the index number changed. This is the exact index 1 block:

```ini
[mIndex1Name]
Measure=Plugin
Plugin=FileView
Path=[mPath]
Type=FileName
Index=1
Group=Children

[mIndex1Type]
Measure=Plugin
Plugin=FileView
Path=[mPath]
Type=FileType
Index=1
Group=Children

[mIndex1Path]
Measure=Plugin
Plugin=FileView
Path=[mPath]
Type=FilePath
Index=1
Group=Children
```

Repeat as `mIndex2Name/mIndex2Type/mIndex2Path` through `mIndex8Name/mIndex8Type/mIndex8Path`, changing only the number and `Index=`.

- [ ] **Step 4: Add eight row meter sets**

Use this row 1 block and repeat through row 8 by changing section names, measure names, row number text, and Y values. Row Y values are `92, 112, 132, 152, 172, 192, 212, 232`.

```ini
[mtrRow1Hit]
Meter=Image
SolidColor=0,0,0,1
X=10
Y=90
W=340
H=18
LeftMouseUpAction=[!CommandMeasure mIndex1Name "FollowPath"][!UpdateMeasure mPath][!UpdateMeasureGroup Children][!UpdateMeter *][!Redraw]
RightMouseUpAction=[!CommandMeasure mIndex1Name "Open"]
MouseOverAction=[!SetOption mtrRow1Line Shape "Line 0,0,332,0 | StrokeWidth 1 | Stroke Color #ColorRed#"][!UpdateMeter mtrRow1Line][!Redraw]
MouseLeaveAction=[!SetOption mtrRow1Line Shape "Line 0,0,332,0 | StrokeWidth 1 | Stroke Color #ColorBlueDeep#"][!UpdateMeter mtrRow1Line][!Redraw]

[mtrRow1No]
Meter=String
MeterStyle=stRowNo
X=14
Y=92
Text=001

[mtrRow1Type]
Meter=String
MeterStyle=stRowType
MeasureName=mIndex1Type
X=58
Y=92
W=54
H=14
Text=%1
Substitute="":"DIR"

[mtrRow1Name]
Meter=String
MeterStyle=stRowText
MeasureName=mIndex1Name
X=126
Y=92
W=218
H=14
Text=%1

[mtrRow1Line]
Meter=Shape
X=14
Y=108
Shape=Line 0,0,332,0 | StrokeWidth 1 | Stroke Color #ColorBlueDeep#
```

- [ ] **Step 5: Add paging and back controls**

Append:

```ini
[mtrBack]
Meter=String
MeterStyle=stHead
X=14
Y=262
Text=< BACK
LeftMouseUpAction=[!CommandMeasure mPath "PreviousFolder"][!UpdateMeasure mPath][!UpdateMeasureGroup Children][!UpdateMeter *][!Redraw]

[mtrPageUp]
Meter=String
MeterStyle=stHead
X=112
Y=262
Text=PAGE -
LeftMouseUpAction=[!CommandMeasure mPath "PageUp"][!UpdateMeasure mPath][!UpdateMeasureGroup Children][!UpdateMeter *][!Redraw]

[mtrPageDown]
Meter=String
MeterStyle=stHead
X=196
Y=262
Text=PAGE +
LeftMouseUpAction=[!CommandMeasure mPath "PageDown"][!UpdateMeasure mPath][!UpdateMeasureGroup Children][!UpdateMeter *][!Redraw]

[mtrCounts]
Meter=String
MeterStyle=stPath
MeasureName=mFolderCount
MeasureName2=mFileCount
StringAlign=Right
X=344
Y=264
Text=F:%1 / X:%2
```

- [ ] **Step 6: Run checks**

Run:

```powershell
python EightSix86/@Resources/fix-encoding.py
python EightSix86/@Resources/check-skin.py
```

Expected: no DockMenu-specific errors.

- [ ] **Step 7: Manual DockMenu check**

Activate `EightSix86\DockMenu` directly in Rainmeter after setting:

```ini
DockMenuRoot=C:\Users\Public\Documents
```

Expected:

- Menu lists files/folders.
- Left click on folder navigates into it.
- Back returns to parent.
- Page buttons change page when more than eight entries exist.
- Right click opens the item in Explorer/default app.

- [ ] **Step 8: Commit DockMenu**

```powershell
git add -- EightSix86/DockMenu/DockMenu.ini
git commit -m "feat: add dock fileview menu"
```

---

## Task 10: Final Verification And Polish

**Files:**
- Modify only files that fail checks or manual verification.
- Test: full static check, git diff review, Rainmeter manual smoke test.

- [ ] **Step 1: Run full encoding and static validation**

Run:

```powershell
python EightSix86/@Resources/fix-encoding.py
python EightSix86/@Resources/check-skin.py
```

Expected: PASS with `Static check passed`.

- [ ] **Step 2: Run git whitespace check**

Run:

```powershell
git diff --check
```

Expected: no output.

- [ ] **Step 3: Review changed files**

Run:

```powershell
git status --short
git diff --stat
```

Expected: changes are limited to files listed in this plan.

- [ ] **Step 4: Manual Rainmeter smoke test**

Refresh or activate:

- `EightSix86\Clock`
- `EightSix86\System`
- `EightSix86\Calendar`
- `EightSix86\SearchGoogle`
- `EightSix86\SearchBing`
- `EightSix86\Music`
- `EightSix86\Dock`
- `EightSix86\DockMenu`

Expected:

- No Rainmeter parse errors.
- Chinese text renders correctly.
- Red-blue palette matches the approved swatch.
- Search opens the system default browser.
- Music shows offline state without WNP and metadata/controls with WNP+SMTC.
- Dock folder target opens `DockMenu`; direct executable target opens directly.

- [ ] **Step 5: Commit final polish**

If Step 1-4 required fixes:

```powershell
git add -- EightSix86 README.md docs/superpowers/plans/2026-05-14-eightsix-rainmeter-hud.md
git commit -m "chore: verify EightSix86 HUD redesign"
```

If no fixes were needed, leave this step uncommitted and record the verification output in the final implementation summary.

---

## References

- Rainmeter FileView plugin: `https://docs.rainmeter.net/manual/plugins/fileview/`
- Rainmeter InputText plugin: `https://docs.rainmeter.net/manual/plugins/inputtext/`
- Rainmeter built-in path variables: `https://docs.rainmeter.net/manual/variables/built-in-variables/`
- WebNowPlaying Rainmeter usage: `https://wnp.keifufu.dev/rainmeter/usage`
- WebNowPlaying Rainmeter install notes: `https://wnp.keifufu.dev/rainmeter/getting-started`
