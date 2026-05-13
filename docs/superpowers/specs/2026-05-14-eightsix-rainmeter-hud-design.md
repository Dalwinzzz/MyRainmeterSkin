# EightSix86 Rainmeter HUD Design

Date: 2026-05-14

## Scope

This design updates the existing `EightSix86` Rainmeter skin at the component level. It does not replace the repository structure or rebuild the skin as a new product. The target components are:

- `Clock`
- `System`
- `Calendar`
- `SearchGoogle`
- `SearchBing`
- `Music`
- `Dock`
- new `DockMenu`
- shared resources and documentation under `EightSix86/@Resources`

Legacy `Disk`, `Network`, `Recycle Bin`, and `Google` skins remain as compatibility backups. The redesigned core experience is the component set above.

## Goals

1. Fix Chinese mojibake in Rainmeter and repository documentation.
2. Make search and music components actually interactive.
3. Redesign the visual system around the 86 anime red-blue collision aesthetic, not the current cobalt-only HUD.
4. Add a multi-level folder-style launcher menu to the Dock.
5. Keep the implementation maintainable and configurable through shared variables.

## Visual Direction

The skin should feel like a transparent desktop HUD mixed with 86 military terminal language. It should sit over wallpapers without becoming a full opaque app surface.

The main palette is based on a red-blue collision frame from the anime:

- `ColorRed`: high-saturation lycoris / battlefield red.
- `ColorRedEdge`: brighter red edge glow.
- `ColorBlue`: deep saturated battlefield blue.
- `ColorBlueEdge`: brighter electric blue structure line.
- `ColorCyan`: cyan impact edge used only as transition light.
- `ColorText`: near-white primary text.
- `ColorTextDim`: muted secondary text.
- `ColorPanel`: dark blue-black transparent panel base.

Approximate starting values:

```ini
ColorRed=238,28,36,255
ColorRedEdge=255,64,72,242
ColorRedDeep=238,28,36,54

ColorBlue=0,58,220,255
ColorBlueEdge=22,96,255,242
ColorBlueDeep=0,58,220,54

ColorCyan=40,198,255,255
ColorCyanDim=40,198,255,120

ColorText=245,251,255,255
ColorTextDim=184,192,204,242
ColorPanel=5,9,18,128
```

Usage rule:

- Blue owns structure: frames, roster lines, numbering, status dots, non-selected icons.
- Red owns focus: current date, clock colon, music main control, selected menu row, alerts.
- Cyan is a small transition accent: scan stripe, hover edge, progress highlight.
- White is for primary readable values.
- Dark panel color is only used as transparent backing for interactive areas.

The review swatch lives at `.superpowers/brainstorm/eightsix-palette-v1.svg`.

## Typography And Encoding

All `.ini`, `.inc`, and project markdown files that contain Chinese must be UTF-8 with BOM where Rainmeter reads them. This is required because Chinese-locale Rainmeter can otherwise treat plain UTF-8 as the system code page and display mojibake.

Font strategy:

- English, numbers, labels: `Bahnschrift`, `Bahnschrift Light`, `Bahnschrift Condensed`.
- Chinese: `Microsoft YaHei UI`.
- Icons where needed: `Segoe MDL2 Assets` or proven glyphs with fallback.

Interface language is mixed:

- Component headers and tactical labels use English: `SYSTEM ROSTER`, `CHRONOS`, `NOW PLAYING`, `DISPATCH`.
- User-facing status and tooltips may use Chinese.
- Avoid dense Chinese in tiny HUD labels.

## Shared Configuration

`EightSix86/@Resources/Variables.inc` is the single shared configuration source for:

- palette
- fonts
- Dock root paths
- search engine URLs
- music source labels
- menu sizing defaults

Component `.ini` files consume these variables and should not duplicate theme constants unless a local override is unavoidable.

## Component Design

### System

`System/System.ini` becomes the top-left 86 roster panel:

- Header: `/ S-1 · SYSTEM ROSTER` and online status.
- Columns: `NO / PERS / PWR / VAL / RATE / STA`.
- Rows:
  - `001 CPU LOAD`
  - `002 MEM USE`
  - `003 DSK C:\`
  - `004 NET DOWN`
  - `005 NET UP`
- Disk row opens `C:\`.
- Header/status area opens Task Manager.
- Red only appears for actual alert states or selected focus, not every row.

### Clock

`Clock/Clock.ini` remains the center visual anchor:

- Large `HH:MM:SS`.
- Red colon.
- Clean date row: `星期四 · 2026年05月14日`.
- Day-of-year row.
- Thin side diamonds and a short scan line.
- Click action opens Windows time/date settings where practical.

### Calendar

`Calendar/Calendar.ini` remains top-right:

- Header: `/ CHRONOS · WK-xx`.
- Three month stack.
- Current day in red.
- Footer: day-of-year and `今日`.
- Click action opens Windows calendar or date UI.

### Search

`SearchGoogle/SearchGoogle.ini` and `SearchBing/SearchBing.ini` use Rainmeter `InputText`.

Behavior:

- Clicking the input area starts text entry.
- Pressing Enter opens the configured search URL in the system default browser.
- Clicking `执行` also triggers the same input flow.
- Input hit areas must match the visible field.
- Placeholders are mixed language, e.g. `输入搜索词 · google.com`.

URLs are configurable through shared variables.

### Music

`Music/Music.ini` defaults to `WebNowPlaying-Redux + SMTC adapter` for NetEase Cloud Music and QQ Music desktop clients.

Behavior:

- Display title, artist, state, position, duration, and progress.
- Controls:
  - previous: `Previous`
  - play/pause: `PlayPause`
  - next: `Next`
- Header source label: `WNP / SMTC`.
- If WNP or SMTC is unavailable, show a clear state such as `WNP OFFLINE / 检查 SMTC` instead of blank text.

Documentation must explain that NetEase / QQ desktop support depends on the third-party WNP Redux and SMTC adapter install.

### Dock

`Dock/Dock.ini` remains a five-item Spearhead launcher row:

- `DEV / UNDERTAKER`
- `DOC / BLACK DOG`
- `GAME / LAUGHING FOX`
- `MEDIA / GUN SNAKE`
- `BIN / SNOW WITCH`

Each root target comes from `Variables.inc`.

Behavior:

- If the configured target is a file, shortcut, executable, or shell target, open it directly.
- If the configured target is a folder, open the new `DockMenu` skin pointed at that folder.
- Recycle Bin keeps its special open / empty behavior.

### DockMenu

Add a new `DockMenu/DockMenu.ini` skin using Rainmeter's built-in `FileView` plugin.

Behavior:

- Displays current path as a compact roster menu.
- Shows rows with `NO / TYPE / NAME`.
- Folders appear before files.
- Clicking a folder follows into that folder.
- Clicking a final file, shortcut, or executable opens it and closes or hides the menu.
- Provides back / previous folder action.
- Provides page up / page down for large folders.
- Shows `PATH LOST` when the root path is invalid.
- Shows `NO TARGETS` for empty folders.

The menu uses blue structure, red hover/selected line, white item text, and a transparent dark panel.

## Data Flow

```text
Variables.inc
  -> palette / fonts / paths / URLs / source labels
  -> component .ini files

Search component
  -> InputText
  -> configured search URL
  -> system default browser

Music component
  -> WebNowPlaying-Redux + SMTC adapter
  -> Rainmeter measures
  -> title / artist / state / progress / controls

Dock component
  -> configured path
  -> direct open OR DockMenu
  -> FileView
  -> FollowPath / PreviousFolder / Open
```

## Error Handling

Encoding:

- Re-stamp Rainmeter-readable files as UTF-8 BOM.
- Keep `EightSix86/@Resources/fix-encoding.py`.
- Add a static check that reports files without BOM and obvious mojibake text.

Music:

- Empty title / artist should render as meaningful fallback text.
- Missing or disconnected WNP should render an offline state.
- Control buttons remain visible, but the state must not imply connected playback when no source exists.

Dock:

- Invalid configured path renders `PATH LOST`.
- Empty folder renders `NO TARGETS`.
- Large directories use pagination instead of expanding indefinitely.
- Final item launch hides the menu to keep the desktop clean.

Search:

- Empty input should not produce broken UI. It may open the engine home/search page or do nothing, depending on implementation feasibility.
- The clickable input area must match the visible input box.

## Testing

Static checks:

- Verify `.ini` and `.inc` files are UTF-8 BOM.
- Scan markdown and skin files for mojibake patterns.
- Check common variable references exist in `Variables.inc`.

Rainmeter smoke tests:

- Refresh each core skin:
  - `Clock`
  - `System`
  - `Calendar`
  - `SearchGoogle`
  - `SearchBing`
  - `Music`
  - `Dock`
  - `DockMenu`
- Confirm no parse errors are shown in Rainmeter logs.

Manual interaction tests:

- Google and Bing search open in the system default browser.
- WNP + SMTC can read and control NetEase / QQ Music desktop playback.
- Music offline state is readable when WNP / SMTC is absent.
- Dock direct file targets open directly.
- Dock folder targets open `DockMenu`.
- `DockMenu` can enter subfolders, go back, page through long lists, and open final shortcuts / executables.

## Deliverables

- Updated `@Resources/Variables.inc`.
- Updated core skin `.ini` files.
- New `DockMenu/DockMenu.ini`.
- Documentation for install and configuration.
- Encoding fix/check tooling.
- Optional visual reference swatch retained under `.superpowers/brainstorm/` and excluded from git by `.gitignore`.
